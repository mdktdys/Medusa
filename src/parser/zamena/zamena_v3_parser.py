import asyncio
from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table


def all_equal(items: list[str]) -> bool:
    return len(set(items)) <= 1


def clean_dirty_string(string: str):
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
    
    from src.api_v1.groups.crud import get_groups_like

    # Восстановление строк с полной заменой ['','','21П-2','',''] -> ['21П-2','21П-2','21П-2','21П-2','21П-2']
    for row in work_rows:
        non_empty_cell: str | None = next((cell for cell in row if isinstance(cell, str) and cell.strip()), None)
        if non_empty_cell is None:
            continue
        
        precised_group_name: str = clean_dirty_string(non_empty_cell)
        groups = await get_groups_like(session=session, pattern=f"%{precised_group_name}%")
        group = groups[0]
        row[:] = [group.name] * len(row)
    
    
    # перевод пар 3,4 на отдельные строки
    extracted: list = []
    for row in work_rows:
        cell: str = row[0].replace('.', ',')
        
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
    groups: list
    for row in work_rows:
        # строка полной замены
        if all_equal(row):
            groups: list = await get_groups_like(
                session = session,
                pattern = row[0]
            )
            
            if len(groups) > 1:
                raise Exception(f'Больше 1 совпадения группы {row[0]}')
            
            group_id: int = groups[0].id
            for cell in row:
                cell = str(group_id)
        else:
            course_text: str = row[3]
            teacher_text: str = row[4]
            cabinet_text: str = row[5]
            
    
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



# if __name__ == '__main__':
#     with open("../samples/response.docx", "rb") as fh:
#         stream = BytesIO(fh.read())
#         asyncio.run(parse_zamena_v3(stream = stream))
    
            
        