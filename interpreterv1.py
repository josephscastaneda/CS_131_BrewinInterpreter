
from intbase import InterpreterBase
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
            self.insert_var(state_node.dict['var'])
            self.do_assign(state_node)   
        elif state_node.elem_type == self.FCALL_NODE:
            #Call the function
            return

    def insert_var(self, name):
        if variable_exists(name, self.var_to_value) == False:
            insert_varname(name, self.var_to_value)

    def do_assign(self, state_node):
        # target_var_name = get_target_variable_name(statement_node)
        #     if !var_name_exists(target_var_name):
        #         generate_error("Undefined variable " + target_var_name)
		# source_node = get_expression_node(statement_node)
		# resulting_value = evaluate_expression(source_node)
		# this.variable_name_to_value[target_var_name] = resulting_value
        var_name = state_node.dict['var']
        if variable_exists(var_name, self.var_to_value) == False:
            # Generate an error for an undefined variable
            return
        result = self.eval_exp(state_node)
        self.var_to_value[var_name] = result
        
    def eval_exp(self, exp_node):
        # if is_value_node(expression_node):
        #         return get_value(expression_node)
        #     else if is_variable_node(expression_node):
        #         return get_value_of_variable(expression_node)
        #     else if is_binary_operator(expression_node):
        #         return evaluate_binary_operator(expression_node)

        #BINARY EXPRESSION
        exp_node = exp_node.dict['expression']
        print(exp_node)
        if exp_node.elem_type == '+':
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            if op1.elem_type != self.INT_NODE or op2 != self.INT_NODE:
                #Type Error
                return
            result = op1.dict['val'] + op2.dict['val']
            return result
            
        if exp_node.elem_type == '-':
            op1 = exp_node.dict['op1']
            op2 = exp_node.dict['op2']
            if op1.elem_type != self.INT_NODE or op2 != self.INT_NODE:
                #TYPE ERROR
                return
            result = op1.dict['val'] - op2.dict['val']
            return result
        
        if exp_node.elem_type == self.QUALIFIED_NAME_NODE:
            if variable_exists(exp_node.dict['name'], self.var_to_value) == False:
                #ERROR
                return
            elif variable_assigned(exp_node.dict['name'], self.var_to_value) == False:
                #ERROR
                return
            result = self.var_to_value[exp_node.dict['name']]
            return result
            
        return
    


#NEXT STEPS:
#vartotype dictionary to check type of qnames for binary ops
#take into account the binary operation on qnames
#Eventually take into account the possibility of nested binary operations
#Implement fcalls
#Implement Error cases correctly