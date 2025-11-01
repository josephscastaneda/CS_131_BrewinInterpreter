from intbase import InterpreterBase, ErrorType
from brewparse import parse_program
from brew_variable import variable_exists, insert_varname, variable_assigned
from brew_function import FunctionEnv


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self, program):
        ast = parse_program(program)
        self.var_to_value = {}
        self.var_to_type = {}
        self.envs_stack = []
        self.func_nodes = ast.dict['functions']
        for func in self.func_nodes:
            if func.dict['name'] == 'main':
                main_node = func
        if main_node.dict['name'] != 'main':
            super().error(ErrorType.NAME_ERROR)
            return
        self.run_func(main_node)

    def run_func(self, func_node):
        #Push new function environment onto our function stack, this will help us support recurion
        self.envs_stack.append(FunctionEnv(func_node.dict['name']))

        func_statements = func_node.dict['statements']
        for statement in func_statements:
            self.run_statement(statement)
        #We must pop our function scope when complete
        self.envs_stack.pop()

    def run_statement(self, state_node):
        if state_node.elem_type == self.VAR_DEF_NODE:
            self.insert_var(state_node.dict['name'])
        elif state_node.elem_type == self.ASSIGNMENT_NODE:
            self.do_assign(state_node)
        elif state_node.elem_type == self.FCALL_NODE:
            self.call_func(state_node)
        elif state_node.elem_type == self.IF_NODE:
            return
        elif state_node.elem_type == self.WHILE_NODE:
            return
        elif state_node.elem_type == self.RETURN_NODE:
            return

    def insert_var(self, name):
        if self.envs_stack[-1].variable_exists(name) == False:
            self.envs_stack[-1].insert_varname(name)
        else:
            super().error(ErrorType.NAME_ERROR)
            return

    def do_assign(self, state_node):
        var_name = state_node.dict['var']
        # if variable_exists(var_name, self.var_to_type) == False:
        #     self.add_type(state_node)
        if self.envs_stack[-1].variable_exists(var_name) == False:
            super().error(ErrorType.NAME_ERROR)
            return
        result = self.eval_exp(state_node)
        self.envs_stack[-1].assign_variable(var_name,result)

    def eval_exp(self, state_node):
        var_holder_name = exp_node.dict['var']
        exp_node = state_node.dict['expression']

        if exp_node.elem_type == self.INT_NODE:
            result = exp_node.dict['val']
            self.envs_stack[-1].add_type(var_holder_name,self.INT_NODE)
            return result
        
        if exp_node.elem_type == self.STRING_NODE:
            result = exp_node.dict['val']
            self.envs_stack[-1].add_type(var_holder_name,self.STRING_NODE)
            return result
        
        if exp_node.elem_type == self.BOOL_NODE:
            result = exp_node.dict['val']
            self.envs_stack[-1].add_type(var_holder_name,self.BOOL_NODE)
            return result
        
        if exp_node.elem_type == self.NIL_NODE:
            result = exp_node.dict['val']
            self.envs_stack[-1].add_type(var_holder_name,self.NIL_NODE)
            return result
        
        if exp_node.elem_type == '+':
            # STRING CONCATENATION?
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            result = self.eval_binary(op1, op2, '+')
            self.envs_stack[-1].add_type(var_holder_name, self.INT_NODE)
            return result
        
        if exp_node.elem_type == '-':
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            result = self.eval_binary(op1, op2, '-')
            self.envs_stack[-1].add_type(var_holder_name, self.INT_NODE)
            return result
        
        if exp_node.elem_type == self.NEG_NODE:
            #TO-DO
            return
        
        if exp_node.elem_type == '*':
            #TO-DO
            return
        
        if exp_node.elem_type == '/':
            #TO-DO
            return
        
        if exp_node.elem_type == '==':
            #TO-DO BOTH BOOLEAN TYPES, STRING TYPES AND INT TYPES
            return
        
        if exp_node.elem_type == '!=':
            #TO-DO BOTH BOOLEAN, STRING, AND INT TYPES
            return
        
        if exp_node.elem_type == '>':
            #TO-DO
            return
        
        if exp_node.elem_type == '<':
            #TO-DO
            return
        
        if exp_node.elem_type == '<=':
            #TO-DO
            return
        
        if exp_node.elem_type == '>=':
            #TO-DO
            return
        
        if exp_node.elem_type == '&&':
            #TO-DO
            return
        
        if exp_node.elem_type == '||':
            #TO-DO
            return
        
        if exp_node.elem_type == '!':
            #TO-DO
            return
        if exp_node.elem_type == self.QUALIFIED_NAME_NODE:
            qname_name = exp_node.dict['name']
            if self.envs_stack[-1].variable_assigned(exp_node.dict['name']) == False:
                super().error(ErrorType.NAME_ERROR)
                return
            result = self.envs_stack[-1].get_var(qname_name)
            qname_type = self.envs_stack.get_type(qname_name) 
            self.envs_stack.add_type(var_holder_name, qname_type)
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
                    if self.envs_stack[-1].variable_assigned(op.dict['name']) == False:
                        super().error(ErrorType.NAME_ERROR)
                    if self.envs_stack[-1].get_type(op.dict['name']) != self.INT_NODE:
                        super().error(ErrorType.TYPE_ERROR)
                    return self.envs_stack[-1].get_var(op.dict['name'])
                if op.elem_type == self.FCALL_NODE:
                    if op.dict['name'] != 'inputi':
                        super().error(ErrorType.TYPE_ERROR)
                    return self.call_func(op)
                return op.dict['val']
            return self.eval_binary(op.dict['op1'], op.dict['op2'], op.elem_type)
        if operation == '+':
            return getop(op1) + getop(op2)
        if operation == '-':
            return getop(op1) - getop(op2)
     
    def call_func(self, state_node):
        func_name = state_node.dict['name']
        #NEED NEW FUNC CALLED inputs, for inputting strings
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
                if args[0].elem_type == self.QUALIFIED_NAME_NODE:
                    super().output(str(self.var_to_value[args[0].dict['name']]))
                else:
                    super().output(str(args[0].dict['val']))
            return int(super().get_input())