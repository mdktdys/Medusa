from io import BytesIO
from typing import List

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.text.paragraph import Paragraph


async def parse_zamena_v3(stream: BytesIO):
    docx: DocumentObject = Document(stream)
    all_rows: list[list[str]] = extract_all_tables_to_rows(docx.tables)
    header_paragraphs: List[Paragraph] = docx.paragraphs
    
    work_rows: list = []
    for row in all_rows:
        if isinstance(row, list) and all(isinstance(item, str) for item in row):
            work_rows.extend(row)
        else:
            work_rows.extend([row])
    
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