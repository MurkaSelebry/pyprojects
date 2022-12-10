import os
import zlib
import binascii
from graphviz import Digraph


class Blob:
    def __init__(self, data):
        self.data = data


class Tree:
    def __init__(self, elements):
        self.elements = elements


class Commit:
    def __init__(self, tree, parent, author, committer, message):
        self.tree = tree
        self.parent = parent
        self.author = author
        self.commiter = committer
        self.message = message


class GitParser:
    def __init__(self, path):
        self.path = path
        self.hashes = []
        self.objects = {}

        if not os.path.isdir(path):
            raise ValueError('Directory does not exist!')
        elif not os.path.isdir(path + '/.git/objects'):
            raise ValueError('Git objects folder does not exist!')

        self.getHashes()
        self.fillObjects()

    def getHashes(self):
        self.hashes.clear()

        for root, dirs, files in os.walk(self.path + '/.git/objects'):
            for name in dirs:
                if name != 'pack' or name != 'info':
                    for root2, dirs2, files2 in os.walk(self.path + '/.git/objects/' + name):
                        for name2 in files2:
                            self.hashes.append(name + name2)

    def fillObjects(self):
        self.objects.clear()

        for hash in self.hashes:
            path = self.path + '/.git/objects/' + hash[:2] + '/' + hash[2:]
            binary_data = open(path, 'rb').read()
            data = zlib.decompress(binary_data)
            object_type = data.split()[0].decode()
            contents = data.split(b'\x00', maxsplit=1)[1]

            if object_type == 'blob':
                #self.objects[hash] = Blob(contents.decode())
                pass
            elif object_type == 'commit':
                rcontents = contents.decode().splitlines()
                tree = None
                parent = None
                author = None
                committer = None

                for item in rcontents:
                    if item.startswith('tree'):
                        tree = item[5:]
                    elif item.startswith('parent'):
                        parent = item[7:]
                    elif item.startswith('author'):
                        author = ' '.join(item.split()[1:4])
                    elif item.startswith('committer'):
                        committer = ' '.join(item.split()[1:4])

                message = rcontents[-1]
                self.objects[hash] = Commit(tree, parent, author, committer, message)
            elif object_type == "tree":
                rcontents = list()
                while contents != b'':
                    filemode, contents = contents.split(b' ', maxsplit=1)
                    filename, contents = contents.split(b'\x00', maxsplit=1)
                    sha1, contents = contents[:20], contents[20:]
                    filemode = filemode.decode()
                    filename = filename.decode()
                    sha1 = binascii.hexlify(sha1).decode()
                    rcontents.append((filemode, filename, sha1))
                    self.objects[hash] = Tree(rcontents)

    def getGraph(self):
        graph = Digraph(name='Commits Graph')

        for h, obj in self.objects.items():
            if type(obj) is Tree:
                graph.node(h, 'TREE' + '\n' + h)
                for item in obj.elements:
                    if item[0] == '100644':  # blob
                        graph.node(item[2], 'BLOB ' + item[1] + '\n' + item[2])
                    graph.edge(h, item[2])
            if type(obj) is Commit:
                graph.node(h, 'COMMIT ' + obj.message + '\n' + h)
                graph.edge(h, obj.tree)
                if obj.parent is not None:
                    graph.edge(h, obj.parent)

        return graph.source