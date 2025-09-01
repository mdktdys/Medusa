import asyncio
from io import BytesIO

from src.parser.zamena.zamena_v3_parser import parse_zamena_v3

if __name__ == '__main__':
    with open("samples/response.docx", "rb") as fh:
        stream = BytesIO(fh.read())
        asyncio.run(parse_zamena_v3(stream = stream))
    
        