from element import Element


class FunctionEnv():
    def __init__(self, func_name):
        self.func_name = func_name
        self.funcscope = {}

    def insert_varname(self, varname):
        if self.variable_exists(varname):
            return False
        self.funcscope[varname] = None
        return True
    def variable_exists(self, varname):
        return varname in self.funcscope
    def variable_assigned(self,varname):
        if self.funcscope[varname] == None or self.variable_exists(varname) == False:
            return False
        else:
            return True
    def assign_variable(self, varname, value):
        if self.variable_exists(varname) == False:
            return False
            #HAVE TO CALL ERROR ON FALSE RETURN
        else:
            self.funcscope[varname] = value
            return True
    def get_func_name(self):
        return self.func_name
    
    