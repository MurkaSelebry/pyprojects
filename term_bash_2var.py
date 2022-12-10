import zipfile
import sys

def checkDirectory(addres,pWay,allFiles):           #функция двигает дерикторию
    if addres=="~":                                 #абсолютный адрес
        return ""
    elif addres==".." or addres=="-":
        if addres=='':
            return pWay
        else:
            pWay="/"+pWay
            k=len(pWay)-1
            while pWay[k]!="/":
                pWay=pWay[:-1]
                k-=1
            pWay=pWay[:-1]
            pWay=pWay[1:]
            return pWay
    elif  "/root" in addres:
        addres=addres.replace("/root",'')
        if addres in allFiles:
            return addres
        return "sh: cd: can't cd to "+addres+": No such file or directory"
    elif pWay=='' and (addres+'/') in allFiles:         #последовательный адрес
        return addres
    elif pWay+'/'+addres+'/' in allFiles:
        return pWay+'/'+addres
    else:
        return "sh: cd: can't cd to "+addres+": No such file or directory"

def checkFile(addres,pWay,allFiles):                #функция двигает дерикторию
    if  "/root" in addres:
        addres=addres.replace("/root/",'')
        if addres in allFiles:
            return addres
        return "cat: can't open"+addres+": No such file or directory"
    elif pWay+'/'+addres in allFiles:
        return pWay+'/'+addres
    else:
        return "cat: can't open"+addres+": No such file or directory"

def CAT(outAdr,nameArch):
        flag = False
        with zipfile.ZipFile(nameArch) as myzip:
            with myzip.open(outAdr,'r') as myfile:
                lines = [x.decode('utf8').strip() for x in myfile.readlines()]#декод в текст
                for line in lines:
                    flag = True
                    print(line)
        if flag == False:
            "cat: can't open" + outAdr +": No such file or directory"

def PWD(help_way):
    if help_way=="":
        print ("/root")
    else:
        print("/root/"+help_way+"/")


def listFile(wayL,option,allFiles):
    if(option!=""):
        wayL+=option
    counter=wayL.count('/')
    wayL+='/'
    flag = False
    for i in allFiles:
        if wayL=='/':
            if wayL in i and i!=wayL:
                if counter== (i.count('/')):
                    if i[-1]!='/':
                        flag = True
                        print(i,end="    ")
                    else:
                        flag = True
                        print(i[:-1],end="    ")
                elif (counter== ((i.count('/')-1)) and (i[-1]=='/')):
                    flag = True
                    print(i[:-1],end="    ")
        else:
            if wayL in i and i!=wayL:
                if counter== (i.count('/')-1):
                    if i[-1]!='/':
                        flag = True
                        print(i,end="    ")
                    else:
                        flag = True
                        print(i[:-1],end="    ")
                elif (counter== ((i.count('/')-2)) and (i[-1]=='/')):
                    flag = True
                    print(i[:-1],end="    ")
    if flag == False:
        print(f"sh: ls can't open {wayL}: No such file or directory")



def main():
    try:
        a = sys.argv[1]
    except IndexError:
        exit()
    constWay='/root> '
    way=''
    pWay=""
    z = zipfile.ZipFile(a, 'r')                     #переменная с открытым архивом
    allFiles=(z.namelist())                         #Возвращает список участников архива по имени.
    cmd = input(constWay)
    while cmd != "exit":
        cmd=cmd.split(" ")
        if cmd[0] == "pwd":
            PWD(pWay)
        elif cmd[0] == "cat":
            if len(cmd)==1:
                cmd.append("")
            temp_out=checkFile(cmd[1],pWay,allFiles)
            if "cat: can't open" in temp_out:
                print(temp_out)
            else:
                CAT(temp_out,a)
        elif cmd[0] == "ls":
            if len(cmd)==1:
                cmd.append("")
            _=pWay
            listFile(_,cmd[1],allFiles)
            print()
        elif cmd[0] == "cd":
            if len(cmd)==1:
                cmd.append("")
            temp=(checkDirectory(cmd[1],pWay,allFiles))
            if "can't cd to " in temp:
                pass
                print(temp)
            else:
                pWay=temp
        else:
            print("sh: "+cmd[0]+ " not found")
        cmd = input("root/"+pWay+"> ")
    return
main()