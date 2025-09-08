from datetime import date, timedelta
from io import BytesIO

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from alchemy.database_local import Cabinet, Group
from src.api_v1.cabinets.crud import get_cabinets_normalized_contains
from src.api_v1.groups.crud import get_groups_normalized_contains


async def parse_teacher_rows(session: AsyncSession, teacher_rows: list[list[str]], monday_date: date):
    teacher_name: str = teacher_rows[0][0].replace('Преподаватель - ', '')
    
    # teacher name
    teacher_rows.pop(0)
    # gap
    teacher_rows.pop(0)
    # date
    teacher_rows.pop(0)
    # gap
    teacher_rows.pop(0)
    # column names
    teacher_rows.pop(0)
    teacher_rows.pop(0)
    # 8 lessons
    teacher_rows.pop(-1)
    
    # merge nan rows
    merged_rows: list[list[str]] = []
    buffer = None
    for row in teacher_rows:
        if pd.notna(row[0]):  
            if buffer is not None:
                merged_rows.append(buffer)
            buffer = row.copy()
        else:  
            for i, val in enumerate(row):
                if pd.notna(val):
                    if pd.isna(buffer[i]): # type: ignore
                        buffer[i] = val # type: ignore
                    else:
                        buffer[i] = f"{buffer[i]} {val}" # type: ignore

    if buffer is not None:
        merged_rows.append(buffer)
        
    if len(merged_rows) != 7:
        raise Exception(f'🔴 Несовпадение количества пар для преподавателя {teacher_name}')
    
    for row in merged_rows:
        row.pop(0)
        row.pop(0)
        row.pop(-1)
        row.pop(-1)
    
    lessons = []
    for timing_index in range(len(merged_rows)):
        timing_row: list[str] = merged_rows[timing_index]
        
        for day_index in range(5):
            value: str = timing_row[0 + day_index * 2]
            discipline_and_group_text: str | None = None if pd.isna(value) else str(value)
            
            if discipline_and_group_text is None:
                continue
            
            precised_group: list[Group] = await get_groups_normalized_contains(
                raw_name = discipline_and_group_text,
                session = session,
            )
            
            if not precised_group:
                raise Exception(f'🔴 Не найдена группа {discipline_and_group_text}')
            if len(precised_group) > 1:
                raise Exception(f'🔴 Больше 1 совпадения группы {discipline_and_group_text}')
            
            value: str = timing_row[1 + day_index * 2]
            cabinet_text: str | None = None if pd.isna(value) else str(value)
            
            cabinet: Cabinet | None
            if cabinet_text is None:
                cabinet = None
            else:
                precised_cabinet: list[Cabinet] = await get_cabinets_normalized_contains(
                    raw_name = cabinet_text,
                    session = session
                )
                
                if not cabinet_text:
                    raise Exception(f'🔴 Не найден кабинет {cabinet_text}')
                if len(cabinet_text) > 1:
                    raise Exception(f'🔴 Больше 1 совпадения кабинета {cabinet_text}')
                
                cabinet = precised_cabinet[0]
                
            
            date_: date = monday_date + timedelta(days = day_index)
            lesson = {
                'number': timing_index,
                'teacher': teacher_name,
                'discipline': discipline_and_group_text,
                'group': precised_group[0].id,
                'cabinet': None if cabinet is None else cabinet.id,
                'date': date_,           
            }

            lessons.append(lesson)

    return lessons
        

async def parse_sheet(session: AsyncSession, sheet: pd.DataFrame, monday_date: date) -> list:
    rows: list[list[str]] = sheet.values.tolist() # type: ignore
    
    rows.pop(0)
    rows.pop(0)
    rows.pop(0)
    
    teachers_count: int = 0
    for row in rows:
        cell_text = row[0]
        
        if not pd.notna(cell_text):
            continue
        
        if isinstance(cell_text, str) and row[0].__contains__('Преподаватель'):
            teachers_count = teachers_count + 1
        
    teachers_lessons = []

    for teacher_index in range(teachers_count):
        teacher_rows: list[list[str]] = rows[(teacher_index * 20) + (teacher_index * 2): (teacher_index + 1) * 20 + (teacher_index * 2)]
        teacher_lessons = await parse_teacher_rows(
            teacher_rows = teacher_rows,
            monday_date = monday_date,
            session = session
        )
        teachers_lessons.extend(teacher_lessons)
            
    return teachers_lessons


async def parse_teacher_schedule_v3(stream: BytesIO, session: AsyncSession, monday_date: date):
    excel_raw = pd.ExcelFile(stream)

    teachers_lessons: list = []
    for sheet_index in range(8):
        sheet: pd.DataFrame = excel_raw.parse(sheet_index)
        sheet_teachers_lessons: list = await parse_sheet(sheet = sheet, monday_date = monday_date, session = session)
        teachers_lessons.extend(sheet_teachers_lessons)

    return teachers_lessons