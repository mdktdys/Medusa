import asyncio
from io import BytesIO

import pandas as pd


def define_course(group_name: str) -> int:
   if group_name.__contains__('25'):
        return 1
     
   if group_name.__contains__('24'):
        return 2
   
   if group_name.__contains__('23'):
        return 3
     
   if group_name.__contains__('22'):
        return 4
     
   return -1


def define_group_department(group_name: str) -> int:
    if group_name.__contains__('25'):
        return 1
    
    if group_name.__contains__('ВЕБ'):
       return 4
   
    if group_name.__contains__('ОИБ'):
       return 3
   
    if group_name.__contains__('ИИС'):
       return 4
    
    if group_name.__contains__('ИС'):
       return 4
   
    if group_name.__contains__('КСК'):
       return 3
   
    if group_name.__contains__('СА'):
       return 3
   
    if group_name.__contains__('ПД'):
       return 2
   
    if group_name.__contains__('Ю'):
       return 2
   
    if group_name.__contains__('Э'):
       return 5
   
    if group_name.__contains__('З'):
       return 5
   
    if group_name.__contains__('П'):
       return 4
   
    if group_name.__contains__('Л'):
       return 5
   
    return -1


def define_group_specialization(group_name: str) -> int:
    if group_name.__contains__('ВЕБ'):
       return 4
   
    if group_name.__contains__('ОИБ'):
       return 6
   
    if group_name.__contains__('ИИС'):
       return 5
    
    if group_name.__contains__('ИС'):
       return 3
   
    if group_name.__contains__('КСК'):
       return 1
   
    if group_name.__contains__('СА'):
       return 2
   
    if group_name.__contains__('ПД'):
       return 11
   
    if group_name.__contains__('Ю'):
       return 9
   
    if group_name.__contains__('Э'):
       return 7
   
    if group_name.__contains__('З'):
       return 10
   
    if group_name.__contains__('П'):
       return 3
   
    if group_name.__contains__('Л'):
       return 8
   
    return -1


async def parse_load_from_excel(bytes_: BytesIO) -> list[tuple[str, str, int, int, int]]:
    excel = pd.ExcelFile(bytes_)
    book: pd.DataFrame = excel.parse(0)
    rows: list[list[str]] = book.values.tolist() # type: ignore
    
    # remove semestr header
    rows.pop(0)
    # remove bottom hours
    rows.pop(-1)
    
    groups: list[tuple[str, str]] = []
    for row in rows:
        groups.append((row[0], row[1]))

    seen: set[str] = set()
    unique_groups: list[tuple[str, str, int, int, int]] = []
    for name, commerce in groups:
        if name in seen:
            continue
        seen.add(name)
        
        department_id: int = define_group_department(name)
        specialization_id: int = define_group_specialization(name)
        course: int = define_course(name) 

        unique_groups.append((name, commerce, department_id, specialization_id, course))

    print(unique_groups)
    return unique_groups
