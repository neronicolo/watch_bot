import os
import zipfile

path = os.getcwd()
content = os.listdir()
base_name = os.path.basename(path)
print(content)
print(base_name)

z = zipfile.ZipFile('test_zip.zip', 'w')
z.write(path)
z.write('hello.py')

