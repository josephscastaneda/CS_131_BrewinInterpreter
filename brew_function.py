from element import Element


def get_func_list(ast):
    #Get function list from the program at head of ast
    func_nodes = ast.dict['functions']
    return func_nodes