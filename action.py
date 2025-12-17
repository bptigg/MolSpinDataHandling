class Node:
    def __init__(self, str):
        self.id = str
        self.contents = []
        self.parents = []
        self.children = []
    def AddParents(self,parents):
        for i in parents:
            self.parents.append(i)
    def AddChildren(self,children):
        for i in children:
            self.children.append(i)
    def GetParents(self):
        return self.parents
    def GetChildren(self):
        return self.children
    
class Network:
    def __init__ (self, nodes : dict):
        self.nodes = nodes
    def traverse(self, path, exception):
        nodes = []
        if (not path[0] in self.nodes):
            return False
        prevnode = self.nodes[path[0]]
        nextnode = None
        for i in range(1,len(path)):
            print(self.nodes.keys())
            if not path[i] in self.nodes.keys(): #need to fix
                nextnode = exception(path[i])
                if nextnode == None:
                    return False
            else:
                nextnode = self.nodes[path[i]]
            if(prevnode in nextnode.GetParents() and nextnode in prevnode.GetChildren()):
                prevnode = nextnode
                nodes.append(prevnode)
                continue
            else:
                return False
        nodes.append(next)
        return nodes
    
