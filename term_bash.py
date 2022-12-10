import zipfile
import sys


def CD(option, curr_path, list_files):
    if option == "~" or option == "":
        return ""
    elif option == ".." or option == "-":
        curr_path = "/" + curr_path
        k = len(curr_path) - 1
        while curr_path[k] != "/":
            curr_path = curr_path[:-1]
            k -= 1
        curr_path = curr_path[:-1]
        curr_path = curr_path[1:]
        return curr_path
    elif "/root" in option:
        option = option.replace("/root", '')
        if option in list_files:
            return option
        return "vshell: cd: can't cd to " + option + ": No such file or directory"
    elif curr_path == '' and (option + '/') in list_files:  
        return option
    elif curr_path + '/' + option + '/' in list_files:
        return curr_path + '/' + option
    else:
        return "vshell: cd: can't cd to " + option + ": No such file or directory"





def CAT(cat_path, nameArch):
    flag = False
    with zipfile.ZipFile(nameArch) as myzip:
        with myzip.open(cat_path, 'r') as myfile:
            lines = [x.decode('utf8').strip() for x in myfile.readlines()]  # декод в текст
            for line in lines:
                print(line)
    if not flag:
        "cat: can't open" + cat_path + ": No such file or directory"

def CAT_control(option, curr_path, list_files):
    if "/" in option:
        if option in list_files:
            return option
        return "cat: can't open " + option + ": No such file or directory"
    elif curr_path + '/' + option in list_files:
        return curr_path + '/' + option
    else:
        return "cat: can't open " + option + ": No such file or directory"

def PWD(addit_path):
    if addit_path == "":
        print("/")
    else:
        print("/" + addit_path + "/")




def LS(joint_path, option, list_files):
    if option != "":
        joint_path += '/'+option
        if joint_path[0]=='/':
            joint_path=joint_path[1:]
    counter = joint_path.count('/')
    joint_path += '/'
    flag = False

    for i in list_files:
        if joint_path == '/':
            if joint_path in i and i != joint_path:
                if counter == (i.count('/')):
                    if i[-1] != '/':
                        flag = True
                        print(i, end='\t')
                    else:
                        flag = True
                        print(i[:-1], end='\t')
                elif (counter == ((i.count('/') - 1)) and (i[-1] == '/')):
                    flag = True
                    print(i[:-1], end='\t')
        else:
            if joint_path in i and i != joint_path:
                if counter == (i.count('/') - 1):
                    if i[-1] != '/':
                        flag = True
                        print(i[i.rfind('/') + 1:], end='\t')
                    else:
                        flag = True
                        print(i[i.rfind('/') + 1:-1], end='\t')
                elif (counter == ((i.count('/') - 2)) and (i[-1] == '/')):
                    flag = True
                    print(i[i[:-2].rfind('/') + 1:-1], end='\t')
    if not flag:
        print(f"vshell: ls can't open {joint_path}: No such file or directory")

def first_dirLayout(list_files):
    t = set()
    for i in list_files:
        t.add(i[:i.find('/')] + '/')
    for el in t:
        if el not in list_files:
            list_files.append(el)

def main():
    try:
        a = sys.argv[1]
    except IndexError:
        exit()
    constPath = '/# '
    curr_path = ""
    z = zipfile.ZipFile(a, 'r')
    list_files = z.namelist()
    first_dirLayout(list_files)
    cmd = input(constPath)
    while cmd != "exit":
        cmd = cmd.split(" ")
        if cmd[0] == "pwd":
            PWD(curr_path)
        elif cmd[0] == "cat":
            if len(cmd) == 1:
                cmd.append("")
            temp_out = CAT_control(cmd[1], curr_path, list_files)
            if "cat: can't open " in temp_out:
                print(temp_out)
            else:
                CAT(temp_out, a)
        elif cmd[0] == "ls":
            if len(cmd) == 1:
                cmd.append("")
            temp = curr_path
            LS(temp, cmd[1], list_files)
            print()
        elif cmd[0] == "cd":
            if len(cmd) == 1:
                cmd.append("")
            temp = (CD(cmd[1], curr_path, list_files))
            if "can't cd to " in temp:
                pass
                print(temp)
            else:
                curr_path = temp
        else:
            print("vshell: " + cmd[0] + " not found")
        cmd = input("/" + curr_path + "# ")
    return
main()



