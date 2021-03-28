import ftplib
from ftplib import FTP
import os

def help(args):
    print('Доступные команды:')
    for item in commands.keys():
        print(item)

def available_directory(args):
    ftp.dir()

def change_directory(args):
    if args == None:
        print('Необходимо указать директорию')
        return 
    try:
        ftp.cwd(args[0])
    except ftplib.error_perm as exception:
        print(exception)

def download(args):
    if args == None:
        print('Необходимо указать имя файла')
        return 
    
    filename = args[0]
    path_items = filename.split('/')
    if len(path_items) == 1:
        path_items = filename.split('\\')
    new_filename = path_items[len(path_items)-1]
    
    path = '.'
    if len(args) > 1:
        path = args[1] 
    if not os.path.exists(path):
        os.mkdir(path)
        
    try:
        with open(path + '/' + new_filename, 'wb') as f:
            print(ftp.retrbinary('RETR ' + filename, f.write))
    except ftplib.error_perm as exception:
        print(exception)

def upload(args):
    if args == None:
        print('Необходимо указать имя файла')
        return 
    
    path = args[0]
    path_items = path.split('/')
    if len(path_items) == 1:
        path_items = path.split('\\')
    filename = path_items[len(path_items)-1]
    if not os.path.exists(path):
        print('Файл не найден')
        return
		
    try:    
        with open(path, 'rb') as fobj:
            print(ftp.storbinary('STOR ' + filename, fobj))
    except ftplib.error_perm as exception:
        print(exception)

def make_directory(args):
    if args == None:
        print('Необходимо указать имя новой директории')
        return 
    
    try:
        print(ftp.mkd(args[0]))
    except ftplib.error_perm as exception:
        print(exception)

def remove_directory(args):
    if args == None:
        print('Необходимо указать имя директории')
        return 
    try:
        print(ftp.rmd(args[0]))
    except ftplib.error_perm as exception:
        print(exception)

def delete(args):
    if args == None:
        print('Необходимо указать имя файла')
        return 
    try:
        print(ftp.delete(args[0]))
    except ftplib.error_perm as exception:
        print(exception)

def change_mode(args):
    if args == None:
        print('Необходимо указать режим (active/passive)')
        return
    
    mode = args[0]
    if mode[0] == 'a':
        ftp.set_pasv(False)
    else:
        ftp.set_pasv(True)

def exit(args):
    print(ftp.quit())
    return 0

commands = {
    '?': help,
    'cd': change_directory,
    'mode': change_mode,
    'dir': available_directory,
    'exit': exit,
    'download': download,
    'upload': upload,
    'mkdir': make_directory,
    'del': delete,
    'rmdir': remove_directory
}



first_connection = True
while True:
    ftp = FTP('127.0.0.1')
    if first_connection:
        print(ftp.getwelcome())
        print()
        first_connection = False

    while True:
        username = input('Имя пользователя: ')            
        passwd = ''
        if username != '' and username != 'anonymous':
            passwd = input('Пароль: ')
        try:
            print(ftp.login(username, passwd))
            break
        except ftplib.error_perm as exception:
            print(exception)
    
    while True:
        print()
        query = input('> ')
        query = query.split()
        cmd = commands.get(query[0])
        args = query[1:] if len(query) > 1 else None
        if cmd == None:
            print('Команда введена неверно')
        else:
            
            if cmd(args) == 0:
                break
    
    res = input('Войти заново? y/n ')
    print()
    if len(res) == 0 or res[0] == 'n':
        break

    