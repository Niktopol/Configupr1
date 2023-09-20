import zipfile
import getpass
import sys
def cmd_input(currloc):
    return input(getpass.getuser() +":~"+currloc+"$ ")

def pwd(currloc):
    print("/home/"+getpass.getuser()+currloc)

def make_path(path, fin_name):
    p = []
    while(path.name != fin_name):
        p.append("/" + path.name)
        path = path.parent
    p.reverse()
    return "".join(p)
    
def move_path(path, way, is_file):
    way = way.split("/")
    for i in range(len(way)):
        k = path.iterdir()
        f = True
        for j in k:
            if (j.name == way[i]):
                if (j.is_dir() or ((i == (len(way)-1)) and is_file)):
                    path = j
                    f = False
                    break
                else:
                    raise BaseException
        if (f):
            raise BaseException
    return path

with zipfile.ZipFile(sys.argv[1]) as zipf:
    dir = zipfile.Path(zipf)
    prev_dir = dir
    zip_name = dir.name
    while True:
        p = cmd_input(make_path(dir, zip_name)).split()
        if (p[0] == "cd"):
            if (len(p) == 2):
                if (p[1] == "-"):
                    dir, prev_dir = prev_dir, dir
                elif (p[1]  == "~"):
                    dir, prev_dir = zipfile.Path(zipf), dir
                elif (p[1]  == ".."):
                    dir, prev_dir = dir.parent if (dir.name != zip_name) else dir, dir
                else:
                    try:
                        dir, prev_dir = move_path(dir, p[1], False), dir
                    except BaseException:
                        print("-bash: cd: " +p[1]+": No such file or directory")
                        continue
            else:
                dir, prev_dir = zipfile.Path(zipf), dir
        elif (p[0] == "pwd"):
            pwd(make_path(dir, zip_name))
        elif (p[0] == "ls"):
            if (len(p) == 1):
                k = dir.iterdir()
                for i in k:
                    print(i.name, end = " ")
                print()
            elif(len(p) >= 2):
                for i in range(1, len(p)):
                    try:
                        k = move_path(dir, p[i], False).iterdir()
                        for i in k:
                            print(i.name, end = " ")
                        print()
                    except BaseException:
                        print("ls: cannot access '"+p[i]+"': No such file or directory")
                        continue
        elif (p[0] == "cat" and len(p) >= 2):
            for i in range(1, len(p)):
                try:
                    file = move_path(dir, p[i], True)
                    if (file.is_dir()):
                        print("cat: " +p[i]+": Is a directory")
                        continue
                    else:
                        with zipf.open(make_path(file, zip_name)[1:]) as fl:
                            lines = [x.decode('utf8') for x in fl.readlines()]
                            for line in lines:
                                print(line, end = "")
                            print()
                except BaseException:
                    print("cat: " +p[i]+": No such file or directory")
                    continue