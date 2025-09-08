import asyncio
import sys
from datetime import date
from io import BytesIO
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.parser.schedule.schedule_parser_v3 import parse_schedule_v3

from .session_maker import async_session_maker


async def excecute():
    monday_date = date(2025, 9, 8)
    with open("samples/rasp_preps с 08.09.2025 г. (1).xls", "rb") as fh:
        stream = BytesIO(fh.read())

    async with async_session_maker() as session:
        await parse_schedule_v3(stream = stream, session = session, monday_date = monday_date)

if __name__ == '__main__':
    asyncio.run(excecute())
        
        
        
    
        