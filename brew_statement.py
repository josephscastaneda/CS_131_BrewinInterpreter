from element import Element

def get_statements(func_node):
    #Get Statement list from given func node
    statements = func_node.dict['statements']
    return statements