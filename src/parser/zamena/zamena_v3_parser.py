from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table


async def parse_zamena_v3(stream: BytesIO):
    docx: DocumentObject = Document(stream)
    all_rows: list[list[str]] = extract_all_tables_to_rows(docx.tables)
    # header_paragraphs: List[Paragraph] = docx.paragraphs
    
    # распаковка вложенных таблиц в одну
    work_rows: list = all_rows
    # for row in all_rows:
    #     if isinstance(row, list) and all(isinstance(item, str) for item in row):
    #         work_rows.extend(row)
    #     else:
    #         work_rows.extend([row])
            
    
    # Удаление столбца Время
    first_row = work_rows[0]
    if first_row[0] == 'Время':
        for row in work_rows:
            row.pop(0)
            
    # Удаление строки хедеров
    if first_row[0] == 'Пара':
        work_rows.pop(0)
    
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