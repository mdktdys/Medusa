import magic


def define_file_format_from_bytes(bytes_: bytes) -> str:
    mime = magic.Magic(mime = True)
    return mime.from_buffer(bytes_)

def is_pdf(string: str) -> bool:
    return string == 'application/pdf'

def is_word(string: str) -> bool:
    return string == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
