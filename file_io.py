ENCODING = 'utf-8'


def read_file(filename):
    """Returns content of file"""
    file = open(filename, 'r', encoding=ENCODING)
    content = file.read()
    file.close()
    return content


def write_file(filename, content):
    """Writes content to file"""
    file = open(filename, 'w', encoding=ENCODING)
    file.write(str(content))
    file.close()
