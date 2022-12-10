import os
import sys
import traceback
from gitparser import GitParser

args = sys.argv

if len(args) != 2:
    print('Error! Wrong number of arguments')
    exit()

path = args[1]

try:
    parser = GitParser(path)
    print(parser.getGraph())
    with open('in.dot', 'w') as f:
        f.write(parser.getGraph())
    os.system('dot -Tpng in.dot > out.png')
except ValueError:
    traceback.print_exc()