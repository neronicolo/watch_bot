import pandas as pd
from pathlib import Path

def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string

def fix_unicode(string):
    string = string.encode('ascii', 'ignore').decode('ascii')
    return string

csv_file_path = Path.home()/'programming/projects/watch_bot/data_prep/file_attribs.csv'
df = pd.read_csv(csv_file_path)
df['name'] = df['name'].apply(remove_umlaut)
df['name'] = df['name'].apply(fix_unicode)
df.to_csv(csv_file_path, index=False)
