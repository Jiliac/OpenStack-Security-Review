from scapy.all import *
import json

def analyze(load):
    start = -1
    end = -1
    i = 0
    toanalyze = str(load)
    for char in toanalyze:
        if start == -1 and char == '{':
            start = i
        elif char == '}':
            end = i
        i+=1

    token = -1
    if start != -1 and end != -1:
        toanalyze = toanalyze[start:end+1]
        tree = Node()
        tree.sons = build_tree(toanalyze)
        result = search_tree(tree, 'context_auth_token')
        if len(result.sons) > 0 and result.sons[0] != 'None':
            print("Found a token! --> " + str(result.sons[0]))
            token = int(result.sons[0], 16)
        #print_json(toanalyze, 0)
        #print("\n\n")
        #print(tree)
    return token

def print_json(json_str, depth):
    j = -1 
    try:
        j = json.loads(json_str)
    except:
        j = json_str
    if j!=-1 and type(j) == dict:
        for entry in j:
            print("  " * depth + entry)
            print_json(j[entry], depth + 1)
    elif j != -1 and type(j) == list:
        for elt in j:
            print_json(elt, depth)
    else:
        print("  " * depth + str(j))

class Node():
    name = ''
    sons = []
    def __str__(self):
        result = ' ' + self.name + ': {'
        if type(self.sons) != types.NoneType:
            for elt in self.sons:
                result += str(elt)
        else:
            result += 'None'
        result += '}'
        return result

def build_tree(json_str):
    sons = []
    j = -1 
    try:
        j = json.loads(json_str)
    except:
        j = json_str
    if j!=-1 and type(j) == dict:
        for entry in j:
            new_node = Node()
            new_node.name = entry
            new_node.sons = build_tree(j[entry])
            sons.append(new_node)
        return sons
    elif j != -1 and type(j) == list:
        for elt in j:
            sons.append(build_tree(elt))
    else:
        return [str(j)]

def search_tree(tree, word):
    if tree.name.find(word) != -1:
        return tree
    elif type(tree.sons) != types.NoneType:
        for son in tree.sons:
            if isinstance(son, Node):
                result = search_tree(son, word)
                if result.name.find(word) != -1 :
                    return result
    default_result = Node()
    return default_result

