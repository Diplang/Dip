from parser import *
from tokens import *
from nodes import *
from lexer import *
from interpreter import *
from symbol_table import *
from context import *    
from runtime_result import *
import os
import math
import random
from position import *
import dreamscript as ds
from voice_recognition import * 
from Dreamshell import *

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()
        
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
        
    def set_context(self, context=None):
        self.context = context
        return self
        
    def added_to(self, other):
        return None, self.illegal_operation(other)
        
    def subbed_by(self, other):
        return None, self.illegal_operation(other)
        
    def multed_by(self, other):
        return None, self.illegal_operation(other)
        
    def dived_by(self, other):
        return None, self.illegal_operation(other)
    
    def powed_by(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)
        
    def anded_by(self, other):
        return None, self.illegal_operation(other)
        
    def ored_by(self, other):
        return None, self.illegal_operation(other)
        
    def notted(self, other):
        return None, self.illegal_operation(other)
    
    def execute(self, args):
        return RTResult().failure(self.illegal_operation())
        
    def copy(self):
        raise Exception('No copy method defined')
    
    def is_true(self):
        return False
        
    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation - check you are comparing two different data types (eg. integer and string)',
            self.context
		)


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self


    def set_context(self, context=None):
        self.context = context
        return self


    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modulise(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def raiseto(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Cannot divide by zero!",
                    self.context
                )
            else:
                return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)


    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_pi = Number(math.pi)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value 

    def added_to(self, other):
        if isinstance (other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
            
    def multed_by(self, other):
        if isinstance (other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
        
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Element at this index could not be removed from the list, because the index is out of bounds",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Element at this index could not be retrieved from the list, because the index is out of bounds",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or '<anonymous>'
    
    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many arguments passed into '{self.name}'",
                self.context
			))
            
        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few arguments passed into '{self.name}'",
                self.context
            ))
        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()

        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res
            
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)
        
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res

        return res.success(return_value)
        
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
        
    def __repr__(self):
        return f"<built-in function {self.name}>"

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        toprint = str(exec_ctx.symbol_table.get('value'))
        return RTResult().success(String(toprint))
    execute_print.arg_names = ["value"]

    def execute_say(self, exec_ctx):
        os.system(f"say '{exec_ctx.symbol_table.get('value')}'")
        return RTResult().success(Number.null)
    execute_say.arg_names = ["value"]

    def execute_randint(self, exec_ctx):
        listA = int(str(exec_ctx.symbol_table.get("argA")))
        listB = int(str(exec_ctx.symbol_table.get("argB")))
        random_int = random.randint(listA, listB)
        return RTResult().success(Number(random_int))
    execute_randint.arg_names = ["argA", "argB"]


    def execute_root(self, exec_ctx):
        root = math.sqrt(float(str(exec_ctx.symbol_table.get('value'))))
        ans = Number(root)       
        return RTResult().success(ans)
    execute_root.arg_names = ["value"]

    def execute_sin(self, exec_ctx):
        smt = math.sin(float(str(exec_ctx.symbol_table.get('value'))))
        ans = Number(smt)
        return RTResult().success(ans)
    execute_sin.arg_names = ["value"]

    def execute_cos(self, exec_ctx):
        smt = math.cos(float(str(exec_ctx.symbol_table.get('value'))))
        ans = Number(smt)        
        return RTResult().success(ans)
    execute_cos.arg_names = ["value"]

    def execute_tan(self, exec_ctx):
        smt = math.tan(float(str(exec_ctx.symbol_table.get('value'))))
        ans = Number(smt)
        return RTResult().success(ans)
    execute_tan.arg_names = ["value"]

    def execute_input(self, exec_ctx):
        text = input(str(exec_ctx.symbol_table.get('value')))
        ans = String(text)
        return RTResult().success(ans)
        TextConsole.eval_current.self.insert('insert', f'{ans}')
    execute_input.arg_names = ["value"]

    def execute_input_integer(self, exec_ctx):
        while True:
            text = input(str(exec_ctx.symbol_table.get('value')))
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))
    execute_input_integer.arg_names = ["value"]

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear') 
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_exitprompt(self, exec_ctx):
        exit() 
        return RTResult().success(Number.null)
    execute_exitprompt.arg_names = []
    
    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]
    
    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]
    
    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]
    
    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_to_int(self, exec_ctx):
        text = str(exec_ctx.symbol_table.get('value'))
        try:
            number = int(text)
            return RTResult().success(Number(text))
        except ValueError:
            print(f"ValueError: Invalid literal for integer() with base 10: '{text}'")
        return RTResult().success(Number.null)
    execute_to_int.arg_names = ["value"]

    def execute_to_float(self, exec_ctx):
        text = str(exec_ctx.symbol_table.get('value'))
        try:
            number = float(text)
            return RTResult().success(Number(text))
        except ValueError:
            print(f"ValueError: Invalid literal for decimal(): '{text}'")
        return RTResult().success(Number.null)
    execute_to_float.arg_names = ["value"]

    def execute_to_string(self, exec_ctx):
        is_number = str(exec_ctx.symbol_table.get("value"))
        return RTResult().success(String(is_number))
    execute_to_string.arg_names = ["value"]

    
    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
                
            ))
            
        list_.elements.append(value)
        return RTResult().success(list_)
    execute_append.arg_names = ["list", "value"]
        
    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
                
            ))
            
        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
                
            ))
            
        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
            
        return RTResult().success(element)
            
    execute_pop.arg_names = ["list", "index"]

    def execute_reverse(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get("value"))
        s1 = ''
        for c in value:
            s1 = c + s1  # appending chars in reverse order
        return RTResult().success(String(s1))

    execute_reverse.arg_names = ["value"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")
        
        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                 "First argument must be list",
                 exec_ctx
            ))
            
        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
                
            ))
            
        listA.elements.extend(listB.elements)
        return RTResult().success(listA.elements)
        
    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        
        if isinstance(value, List):
            return RTResult().success(Number(len(value.elements)))
        elif isinstance(value, String):
            string = str(value)
            length = len(string)
            return RTResult().success(Number(length))
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list or string",
                exec_ctx
            ))

    execute_len.arg_names = ["value"]

    def execute_lsn(self, exec_ctx):
        command = listen_to_command()
        return RTResult().success(String(command))

    execute_lsn.arg_names = []

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")
        
        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))
            
        fn = fn.value
        
        try:
            with open(fn, "r") as f:
                script = f.read()
                
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
                ))
        
        _, error = ds.run(fn, script)
        
        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
                
            ))
        
        return RTResult().success(Number.null)

    execute_run.arg_names = ["fn"]

    def execute_import_(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")
        
        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))
            
        fn = fn.value
        
        try:
            with open(fn, "r") as f:
                script = f.read()
                
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
                ))
        
        _, error = ds.run(fn, script)
        
        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
                
            ))
        
        return RTResult().success(Number.null)

    execute_import_.arg_names = ["fn"]