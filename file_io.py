ENCODING = 'utf-8'


def read_file(filename):
    """Returns content of file"""
    file = open(filename, 'r', encoding=ENCODING)
    content = file.read()
    file.close()
    return content
