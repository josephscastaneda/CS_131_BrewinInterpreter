from intbase import InterpreterBase, ErrorType
from brewparse import parse_program
from brew_variable import create_variable_map, variable_exists, insert_varname, variable_assigned
from brew_function import get_func_list
from brew_statement import get_statements
from element import Element

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self, program):
        ast = parse_program(program)
        self.var_to_value = create_variable_map()
        self.var_to_type = create_variable_map()
        self.func_nodes = ast.dict['functions']
        main_node = self.func_nodes[0]
        self.run_func(main_node)

    def run_func(self, func_node):
        func_statements = func_node.dict['statements']
        for statement in func_statements:
            self.run_statement(statement)

    def run_statement(self, state_node):
        if state_node.elem_type == self.VAR_DEF_NODE:
            self.insert_var(state_node.dict['name'])
        elif state_node.elem_type == self.ASSIGNMENT_NODE:
            # self.insert_var(state_node.dict['var'])
            self.do_assign(state_node)
        elif state_node.elem_type == self.FCALL_NODE:
            self.call_func(state_node)

    def insert_var(self, name):
        if variable_exists(name, self.var_to_value) == False:
            insert_varname(name, self.var_to_value)
        else:
            super().error(ErrorType.NAME_ERROR)
            return

    def do_assign(self, state_node):
        var_name = state_node.dict['var']
        if variable_exists(var_name, self.var_to_type) == False:
            self.add_type(state_node)
        if variable_exists(var_name, self.var_to_value) == False:
            super().error(ErrorType.NAME_ERROR)
            return
        result = self.eval_exp(state_node)
        self.var_to_value[var_name] = result

    def add_type(self, state_node):
        exp_node = state_node.dict['expression']
        if exp_node.elem_type == self.STRING_NODE:
            self.var_to_type[state_node.dict['var']] = 'string'
        elif exp_node.elem_type == self.INT_NODE:
            self.var_to_type[state_node.dict['var']] = 'int'
        elif exp_node.elem_type == self.QUALIFIED_NAME_NODE:
            if variable_assigned(exp_node.dict['name'], self.var_to_type) == False:
                #ERROR
                return
            self.var_to_type[state_node.dict['var']] = self.var_to_type[exp_node.dict['name']]
        # elif exp_node.elem_type == '+' or exp_node.elem_type == '-':
        #     op1 = exp_node.dict['op1']
        #     op2 = exp_node.dict['op2']
        #     if op1.elem_type == self.QUALIFIED_NAME_NODE and op2.elem_type == self.QUALIFIED_NAME_NODE:
        #         if self.var_to_type[op1.dict['name']] != 'int' or self.var_to_type[op2.dict['name']] != 'int':
        #             super().error(ErrorType.TYPE_ERROR)
        #             return
        #     elif op1.elem_type == self.QUALIFIED_NAME_NODE:
        #         if self.var_to_type[op1.dict['name']] != 'int' or op2.elem_type != self.INT_NODE:
        #             super().error(ErrorType.TYPE_ERROR)
        #             return
        #     elif op2.elem_type == self.QUALIFIED_NAME_NODE:
        #         if self.var_to_type[op2.dict['name']] != 'int' or op1.elem_type != self.INT_NODE:
        #             super().error(ErrorType.TYPE_ERROR)
        #             return
        #     elif op1.elem_type
        #     elif op1.elem_type != self.INT_NODE or op2.elem_type != self.INT_NODE:
        #         super().error(ErrorType.TYPE_ERROR)
        #         return
        #     self.var_to_type[state_node.dict['var']] = 'int'


    def eval_exp(self, exp_node):
        var_holder_name = exp_node.dict['var']
        exp_node = exp_node.dict['expression']

        if exp_node.elem_type == self.INT_NODE:
            result = exp_node.dict['val']
            return result
        
        if exp_node.elem_type == self.STRING_NODE:
            result = exp_node.dict['val']
            return result
        
        if exp_node.elem_type == '+':
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            result = self.eval_binary(op1, op2, '+')
            # if op1.elem_type == self.QUALIFIED_NAME_NODE and op2.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op1.dict['name'], self.var_to_value) == False or variable_assigned(op2.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op1.dict['name']] != 'int' or self.var_to_type[op2.dict['name']] != 'int':
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = self.var_to_value[op1.dict['name']] + self.var_to_value[op2.dict['name']]
            #     return result
            # elif op1.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op1.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op1.dict['name']] != 'int' or op2.elem_type != self.INT_NODE:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = self.var_to_value[op1.dict['name']] + op2.dict['val']
            #     return result
            # elif op2.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op2.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op2.dict['name']] != 'int' or op1.elem_type != self.INT_NODE:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = op1.dict['val'] + self.var_to_value[op2.dict['name']]
            #     return result
            
            # if op1.elem_type != self.INT_NODE or op2.elem_type != self.INT_NODE:
            #     super().error(ErrorType.TYPE_ERROR)
            #     return
            
            # result = op1.dict['val'] + op2.dict['val']
            self.var_to_type[var_holder_name] = 'int'
            return result
        
        if exp_node.elem_type == '-':
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            result = self.eval_binary(op1, op2, '-')
            # if op1.elem_type == self.QUALIFIED_NAME_NODE and op2.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op1.dict['name'], self.var_to_value) == False or variable_assigned(op2.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op1.dict['name']] != 'int' or self.var_to_type[op2.dict['name']] != 'int':
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = self.var_to_value[op1.dict['name']] - self.var_to_value[op2.dict['name']]
            #     return result
            # elif op1.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op2.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op1.dict['name']] != 'int' or op2.elem_type != self.INT_NODE:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = self.var_to_value[op1.dict['name']] - op2.dict['val']
            #     return result
            # elif op2.elem_type == self.QUALIFIED_NAME_NODE:
            #     if variable_assigned(op2.dict['name'], self.var_to_value) == False:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     if self.var_to_type[op2.dict['name']] != 'int' or op1.elem_type != self.INT_NODE:
            #         super().error(ErrorType.TYPE_ERROR)
            #         return
            #     result = op1.dict['val'] - self.var_to_value[op2.dict['name']]
            #     return result
            
            # if op1.elem_type != self.INT_NODE or op2.elem_type != self.INT_NODE:
            #     super().error(ErrorType.TYPE_ERROR)
            #     return
            # result = op1.dict['val'] - op2.dict['val']
            self.var_to_type[var_holder_name] = 'int'
            return result
        
        if exp_node.elem_type == self.QUALIFIED_NAME_NODE:
            if variable_exists(exp_node.dict['name'], self.var_to_value) == False:
                super().error(ErrorType.NAME_ERROR)
                return
            if variable_assigned(exp_node.dict['name'], self.var_to_value) == False:
                super().error(ErrorType.NAME_ERROR)
                return
            result = self.var_to_value[exp_node.dict['name']]
            return result
        
        if exp_node.elem_type == self.FCALL_NODE:
            result = self.call_func(exp_node)
            return result
        
    def eval_binary(self, op1, op2, operation):
        def getop(op):
            if op.elem_type != '+' and op.elem_type != '-':
                if op.elem_type == self.STRING_NODE:
                    super().error(ErrorType.TYPE_ERROR)
                    return
                if op.elem_type == self.QUALIFIED_NAME_NODE:
                    if variable_assigned(op.dict['name'], self.var_to_value) == False or self.var_to_type[op.dict['name']] != 'int':
                        super().error(ErrorType.TYPE_ERROR)
                    return self.var_to_value[op.dict['name']]
                return op.dict['val']
            return self.eval_binary(op.dict['op1'], op.dict['op2'], op.elem_type)
        if operation == '+':
            return getop(op1) + getop(op2)
        if operation == '-':
            return getop(op1) - getop(op2)
     
    def call_func(self, state_node):
        func_name = state_node.dict['name']
        if func_name != 'print' and func_name != 'inputi':
            super().error(ErrorType.NAME_ERROR)
            return
        if func_name == 'print':
            args = state_node.dict['args']
            out_str = ""
            for arg in args:
                if arg.elem_type == self.STRING_NODE or arg.elem_type == self.INT_NODE:
                    out_str = out_str + str(arg.dict['val'])
                elif arg.elem_type == self.QUALIFIED_NAME_NODE:
                    if variable_exists(arg.dict['name'], self.var_to_value) == False:
                        super().error(ErrorType.NAME_ERROR)
                        return
                    if variable_assigned(arg.dict['name'], self.var_to_value) == False:
                        super().error(ErrorType.NAME_ERROR)
                        return
                    out_str = out_str + str(self.var_to_value[arg.dict['name']])
            super().output(out_str)

        if func_name == 'inputi':
            args = state_node.dict['args']
            if len(args) > 1:
                super().error(ErrorType.NAME_ERROR)
            if len(args) == 1:
                super().output(str(args[0].dict['val']))
            return super().get_input()
       
        
