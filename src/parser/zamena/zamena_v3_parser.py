from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table

from utils.logger import logger


def clean_trash(string: str) -> str:
    return string.replace('(улзвалиди7а)','')

def all_equal(items: list[str]) -> bool:
    return len(set(items)) <= 1


def clean_dirty_string(string: str) -> str:
    return (
        string.replace(" ", "")
        .replace(".", "")
        .replace(",", "")
        .replace("-", "")
        .replace("_", "")
        .replace("\n", " ")
        .replace("\t", "")
        .replace("—", "")
        .replace("—", "")
    ).lower().replace(' ','')


async def parse_zamena_v3(stream: BytesIO, session):
    exceptions: list = []
    
    docx: DocumentObject = Document(stream)
    all_rows: list[list[str]] = extract_all_tables_to_rows(docx.tables)
    work_rows: list = all_rows
    # header_paragraphs: List[Paragraph] = docx.paragraphs    
    
    # Удаление столбца Время
    first_row = work_rows[0]
    if first_row[0] == 'Время':
        for row in work_rows:
            row.pop(0)
            
    # Удаление строки хедеров
    if first_row[0] == 'Пара':
        work_rows.pop(0)
        
    # Очистка пустых строк
    work_rows = [sublist for sublist in work_rows if any(item != "" for item in sublist)]

    from src.api_v1.groups.crud import get_groups_normalized_contains

    # Восстановление строк с полной заменой ['','','21П-2','',''] -> ['21П-2','21П-2','21П-2','21П-2','21П-2']
    for row in work_rows:
        non_empty_cells: list[str] = [cell for cell in row if isinstance(cell, str) and cell.strip()]
        if not non_empty_cells:
            continue
        if len(non_empty_cells) == 1:
            non_empty_cell: str = clean_dirty_string(non_empty_cells[0])
            groups = await get_groups_normalized_contains(session=session, raw_name=non_empty_cell)
            if groups:
                group = groups[0]
                row[:] = [group.name] * len(row)
            else:
                print(f'🔴 Не найдена группа -> {non_empty_cell}')
            
    # Восстановление оторванных строк
    # ['4,5', '', '', 'Правовые основы оперативно-', 'Музафаров Ф.Ф.', '112']
    # ['', '', '', 'розыскной \nдеятельности', '', '']
    # -> ['4,5', '', '', 'Правовые основы оперативно-розыскной \nдеятельности', 'Музафаров Ф.Ф.', '112']
    merged_rows: list[list[str]] = []
    for row in work_rows:
        if row[0] == '' and merged_rows:
            prev_row: list[str] = merged_rows[-1]
            prev_row[3] = (prev_row[3] + row[3]).strip()
        else:
            merged_rows.append(row)
    work_rows = list(merged_rows)
        
    # перевод пар 3,4 на отдельные строки
    extracted: list = []
    for row in work_rows:
        timings_text = row[0]

        if not timings_text.replace(',','').isdigit():
            extracted.append(row)
            continue
    
        cell: str = timings_text.replace('.', ',')
    
        if cell[0] == ',':
            cell = cell[1:]
        
        if cell[-1] == ',':
            cell = cell[:-1]
        
        timings: list[str] = cell.split(',')
    
        if len(timings) > 1:
            for timing in timings:
                copy_row = row.copy()
                copy_row[0] = timing
                extracted.append(copy_row)
        else:
            extracted.append(row)

    work_rows = list(extracted)


    # Очистка от лишних символов
    work_rows = [[clean_dirty_string(cell) for cell in row] for row in work_rows]
    
    # Перевод в айдишники
    from src.api_v1.disciplines.crud import find_disciplines_by_alias_or_name
    for row in work_rows:
        if all_equal(row):
            group_text: str = clean_trash(row[0])
            groups = await get_groups_normalized_contains(
                session=session,
                raw_name=group_text
            )

            if not groups:
                raise Exception(f'🔴 Не найдена группа {group_text}')
            if len(groups) > 1:
                raise Exception(f'🔴 Больше 1 совпадения группы {group_text}')

            group_id = str(groups[0].id)
            row[:] = [group_id] * len(row)

        else:
            course_text: str = row[3]
            founded_disciplines = await find_disciplines_by_alias_or_name(
                session = session,
                raw = course_text
            )
            
            if not founded_disciplines:
                exceptions.append(f'🔴 Не найдена дисциплина {course_text}')
                continue
            if len(founded_disciplines) > 1:
                raise Exception(f'🔴 Больше 1 совпадения дисциплин {course_text}')
            
    if len(exceptions) > 0:
        for exception in exceptions:
            logger.error(exception)

        raise Exception(exceptions)
            
    
    for row in work_rows:
        print(row)
    
    return {
        'result': 'completed',
        'work_rows': str(work_rows)
    }
    
    
def extract_all_tables_to_rows(tables: list[Table]) -> list[list[str]]:
    rows: list = []
    for table in tables:
        for row in table.rows:
            data: list = []
            for cell in row.cells:
                cell_text: str = cell.text.strip()
                if cell.tables:
                    nested_table_rows: list = extract_all_tables_to_rows(cell.tables)
                    data.extend(nested_table_rows)
                else:
                    data.append(cell_text)
            rows.append(data)
    return rows
