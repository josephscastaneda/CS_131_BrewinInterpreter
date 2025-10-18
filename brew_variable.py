

def create_variable_map():
    #Create a variable map so we can map variables to functions
    var_map = {}
    return var_map

def variable_exists(name, var_map):
    if (name in var_map):
        return True
    else:
        return False
def variable_assigned(name, var_map):
    if var_map[name] == None:
        return False
    else:
        return True
def insert_varname(name, var_map):
    var_map[name] = None
