"""
Static Semantic Checker for OPLang Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the OPLang object-oriented programming language. It performs type checking,
scope management, inheritance validation, and detects all semantic errors as 
specified in the OPLang language specification.
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ClassDecl, AttributeDecl, Attribute, MethodDecl,
    ConstructorDecl, DestructorDecl, Parameter, VariableDecl, Variable,
    AssignmentStatement, IfStatement, ForStatement, BreakStatement,
    ContinueStatement, ReturnStatement, MethodInvocationStatement,
    BlockStatement, PrimitiveType, ArrayType, ClassType, ReferenceType,
    IdLHS, PostfixLHS, BinaryOp, UnaryOp, PostfixExpression, PostfixOp,
    MethodCall, MemberAccess, ArrayAccess, ObjectCreation, Identifier,
    ThisExpression, ParenthesizedExpression, IntLiteral, FloatLiteral,
    BoolLiteral, StringLiteral, ArrayLiteral, NilLiteral
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredClass,
    UndeclaredAttribute, UndeclaredMethod, CannotAssignToConstant,
    TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
    MustInLoop, IllegalConstantExpression, IllegalArrayLiteral,
    IllegalMemberAccess, NoEntryPoint
)

# import pprint

# def print_env(env):
#     print("======= GLOBAL ENVIRONMENT =======")
#     pprint.pprint(env, sort_dicts=False, width=80)
#     print("==================================")
class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value 
    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.mtype}, value={self.value})"

class SymbolTable: 
    
    def __init__(self): 
        self.scopes = []
    
    def enter_scope(self):
        self.scopes.append({}) 
    
    def exit_scope(self): 
        if self.scopes: 
            self.scopes.pop()
    
    def add_symbol(self, symbol: Symbol): 
        if not self.scopes:
            return False
        current_scope = self.scopes[-1]
        if symbol.name in current_scope: 
            return False
        
        current_scope[symbol.name] = symbol 
        return True
    
    def lookup(self, name):
        for i in range(len(self.scopes) - 1, -1, -1):  
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None
    
    def lookup_from_cur(self, name):
        """Tìm chỉ trong scope hiện tại"""
        if self.scopes:
            return self.scopes[-1].get(name)
        return None
    
    def __repr__(self):
        result = "SymbolTable:\n"
        for i, scope in enumerate(self.scopes):
            result += f"  Scope {i}:\n"
            if not scope:
                result += "    (empty)\n"
            else:
                for name, sym in scope.items():
                    result += f"    {name}: type={sym.mtype}, value={sym.value}\n"
        return result

class Phase1(ASTVisitor): # take static method and variable
    def _is_type_equal(self,type1,type2):
        if type(type1) != type(type2): 
            return False
        if isinstance(type1, PrimitiveType): 
            return type1.type_name == type2.type_name
        if isinstance(type1, ArrayType): 
            return type1.size == type2.size and self._is_type_equal(type1.element_type, type2.element_type)
        if isinstance(type1,ReferenceType): 
            return type1.referenced_type == type2.referenced_type
        if isinstance(type1,ClassType): 
            return type1.class_name == type2.class_name
        return False
    def _is_type_compatible(self,target_type, source_type,o): # phai vs trai (var vs expr)
        if self._is_type_equal(target_type, source_type): # target: node.attr_type ; source: init_value 
            return True
    
        if isinstance(target_type, PrimitiveType) and isinstance(source_type, PrimitiveType):
            if target_type.type_name == 'float' and source_type.type_name == 'int':
                return True
        if isinstance(target_type, ReferenceType) and isinstance(source_type, PrimitiveType):
            return self._is_type_equal(target_type.referenced_type, source_type)
        if isinstance(target_type, ReferenceType) and isinstance(source_type, ClassType):
            return self._is_type_equal(target_type.referenced_type, source_type)
        if isinstance(target_type, ClassType) and isinstance(source_type, ReferenceType):
            return self._is_type_equal(target_type, source_type.referenced_type)
        if isinstance(target_type, ReferenceType) and isinstance(source_type, ReferenceType):
            return self._is_type_equal(target_type.referenced_type, source_type.referenced_type)

        if isinstance(target_type, ClassType) and isinstance(source_type, ClassType):
            return self._is_sub_class(target_type, source_type, o)  
        
        if isinstance(source_type, NilLiteral):
            if isinstance(target_type, (ReferenceType, ClassType, ArrayType)):
                return True
        return False
    def _is_sub_class(self,target_type,source_type,o): # a=b 
        env = o['global_env'] if 'global_env' in o else o
        target_name = target_type.class_name
        source_name = source_type.class_name
        if source_name not in env: 
            return False
        cur_name = source_name
        visited = set()
        while cur_name: 
            if cur_name in visited: 
                break
            visited.add(cur_name)

            if cur_name == target_name: 
                return True
            
            if cur_name not in env: 
                break
            cur_name = env[cur_name]['parent']  
        return False
    def _is_constant_expr(self,expr,o=None): 
        if isinstance(expr, (IntLiteral, FloatLiteral,BoolLiteral, StringLiteral)):
            return True
        if isinstance(expr,NilLiteral): 
            return False
        if isinstance(expr, BinaryOp): 
            return  self._is_constant_expr(expr.right,o) and self._is_constant_expr(expr.left,o) 
        if isinstance(expr,UnaryOp): 
            return self._is_constant_expr(expr.operand,o)
        if isinstance(expr,ParenthesizedExpression): 
            return self._is_constant_expr(expr.expr,self.env)
        return False
    def __init__(self): 
        self.env = {
            'io': {
                'parent': None,
                "attributes": {}, 
                "methods": {}, 
                "constructor": {}, 
                "destructor": None
            }
        }
        self.env['io']['methods'] = {

            'readInt': {'is_static': True, 'return_type': PrimitiveType('int'), 'params': []},
            'writeInt': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('int'))]},
            'writeIntLn': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('int'))]},
            'readFloat': {'is_static': True, 'return_type': PrimitiveType('float'), 'params': []},
            'writeFloat': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('float'))]},
            'writeFloatLn': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('float'))]},
            'readBool': {'is_static': True, 'return_type': PrimitiveType('boolean'), 'params': []},
            'writeBool': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('boolean'))]},
            'writeBoolLn': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('boolean'))]},
            'readStr': {'is_static': True, 'return_type': PrimitiveType('string'), 'params': []},
            'writeStr': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('string'))]},
            'writeStrLn': {'is_static': True, 'return_type': PrimitiveType('void'), 'params': [('x', PrimitiveType('string'))]},
        }
        self.env['io']['visited'] = True

    def visit_program(self, node, o = None):
        o = self.env
        if 'global_vars' not in o: 
            o['global_vars'] = {}
        decls = node.decls if hasattr(node, 'decls') else node.class_decls
        declared_names = set(o.keys())

        for decl in decls:         
            if isinstance(decl, ClassDecl):
                classname = decl.name
                if classname in declared_names:
                    raise Redeclared('Class', classname)    
                o[classname] = {
                    'name': classname,
                    'parent': None,
                    "attributes": {},
                    "methods": {},
                    "constructor": {},
                    "destructor": None,
                    'static': {}
                }
                declared_names.add(classname)
            elif isinstance(decl, VariableDecl):
                for var in decl.variables:
                    var_name = var.name
                    # 1. Check Redeclared (trùng tên Class hoặc biến khác)
                    if var_name in declared_names or var_name in o['global_vars']:
                        kind = 'Constant' if decl.is_final else 'Variable'
                        raise Redeclared(kind, var_name)
                    
                    o['global_vars'][var_name] = {
                        'type': decl.var_type,       # Kiểu dữ liệu
                        'is_final': decl.is_final,   # Có phải hằng số không
                        'kind': 'Constant' if decl.is_final else 'Variable',
                        'init_val': var.init_value,  # Giá trị khởi tạo (để Phase 2 check type)
                        'decl_node': decl            # Node gốc (để báo lỗi nếu cần)
                    }
                    declared_names.add(var_name)
        # for class_decl in node.class_decls: 
        #     classname = class_decl.name
        #     if classname in o: 
        #         raise Redeclared('Class', classname)
        #     o[classname] = {
        #         'name': classname, 
        #         'parent': None, 
        #         "attributes": {}, 
        #         "methods": {}, 
        #         "constructor": {}, 
        #         "destructor": None, 
        #         'static': {} # 'attr', 'var', ' method 
        #     }
        for class_decl in node.class_decls: 
            self.visit(class_decl,o)
        return o
    
    def visit_class_decl(self, node, o = None):
        classname = node.name
        parent = node.superclass
        if parent: 
            if parent not in o: 
                raise UndeclaredClass(parent)
            if parent == classname: 

                raise UndeclaredClass(parent)
            if not o[parent].get('visited',False): 
                raise UndeclaredClass(parent)
        o[classname]['parent'] = parent
        for member in node.members: 
            self.visit(member,o[classname])
        o[classname]['visited'] = True
        return o[classname]

    def visit_attribute_decl(self, node, o = None): #(is_static, is_final, type, init_value)
        # checking cho type trc 
        if isinstance(node.attr_type, ClassType):
            if node.attr_type.class_name not in self.env: 
                raise UndeclaredClass(node.attr_type.class_name)    
        if isinstance(node.attr_type, ReferenceType):
            ref_type = node.attr_type.referenced_type
            if isinstance(ref_type, ClassType):
                if ref_type.class_name not in self.env: 
                    raise UndeclaredClass(ref_type.class_name)
        
        for attr in node.attributes: 
            attr_name = attr.name

            if attr_name in o['attributes']: 
                raise Redeclared('Attribute',attr_name)
            if attr_name in o['methods']: 
                raise Redeclared('Attribute',attr_name)
            if attr_name == o.get('name'):
                raise Redeclared('Attribute', attr_name)
            if isinstance(attr.init_value,Identifier): 
                raise UndeclaredIdentifier(attr.init_value.name)
            if isinstance(attr.init_value, ObjectCreation):
                init_class = attr.init_value.class_name
                if init_class not in self.env or not self.env[init_class].get('visited', False):
                    raise UndeclaredClass(init_class)            
            if node.is_static:
                if 'attr' not in o['static']:
                    o['static']['attr'] = {}
                o['static']['attr'][attr_name] = {'type': str(node.attr_type)}
            o['attributes'][attr_name] = {
                'is_static': node.is_static, 
                'is_final': node.is_final, 
                'type': node.attr_type, 
                'init_val': attr.init_value
            }
    
    def visit_method_decl(self, node, o = None): # allow method overriding
        method_name = node.name
        
        if method_name in o['methods']: 
            raise Redeclared('Method', method_name)
        if method_name in o['attributes']: 
            raise Redeclared('Method', method_name)
        if method_name == o.get('name'):
            raise Redeclared('Method', method_name)
        # checking param
        param_list = []
        param_names = set()
        for param in node.params: 
            if param.name in param_names: 
                raise Redeclared('Parameter', param.name)
            param_names.add(param.name)
            # checkng for param type is class type of reference type to class type
            if isinstance(param.param_type, ClassType):
                if param.param_type.class_name not in self.env: 
                    raise UndeclaredClass(param.param_type.class_name)
            if isinstance(param.param_type, ReferenceType):
                ref_type = param.param_type.referenced_type
                if isinstance(ref_type, ClassType):
                    if ref_type.class_name not in self.env: 
                        raise UndeclaredClass(ref_type.class_name)
                    
            param_list.append((param.name, param.param_type))
        # checking return type if it is in [class type, reference type to class type]
        if isinstance(node.return_type, ClassType):
            if node.return_type.class_name not in self.env: 
                raise UndeclaredClass(node.return_type.class_name)
        if isinstance(node.return_type, ReferenceType):
            ref_type = node.return_type.referenced_type 
            if isinstance(ref_type, ClassType):
                if ref_type.class_name not in self.env: 
                    raise UndeclaredClass(ref_type.class_name)
            if node.is_static:
                if 'methods' not in o['static']:
                    o['static']['methods'] = {}
                o['static']['methods'][method_name] = {'type': str(node.return_type)}
        

        o['methods'][method_name] = {
            'is_static': node.is_static, 
            'return_type': node.return_type, 
            'params': param_list
        }



    def __type_infer_constructor(self,node, paramlist): # testcase
        if len(paramlist) == 0: 
            return 'default'
        if len(paramlist) == 1:
            _, param_type = paramlist[0]
            if isinstance(param_type, ClassType) and param_type.class_name == node.name:
                return 'copy'
        return 'user-defined'
    def _is_same_args_construct(self,construct1, node,o): 
        if len(node.params) != len(construct1['params']): 
            return False
        constructor1_paramlist = [construct1['params'][i][1] for i in range(len(construct1['params']))]
        # construct1_type = [self.visit(param) for param in constructor1_paramlist]
        for arg, param_type in zip(node.params,constructor1_paramlist):
            arg_type = arg.param_type
            if not self._is_type_compatible(param_type,arg_type,o): 
                return False
        return True 
    
    def visit_constructor_decl(self, node, o=None):
        constructor_name = node.name
        # checking for outer of contructor
        param_list = []
        param_names = set()
        for param in node.params: 
            if param.name in param_names: 
                raise Redeclared('Parameter', param.name)
            param_names.add(param.name)
            param_list.append((param.name, param.param_type))
        constructor_type = self.__type_infer_constructor(node,param_list)
        if constructor_type not in o['constructor']: # chi co khi trong main co khai bao constructor
            o['constructor'][constructor_type] = []
        for construct in o['constructor'][constructor_type]: 
            if construct['name'] == constructor_name and self._is_same_args_construct(construct, node,o): 
                raise Redeclared('Constructor', constructor_name)
        o['constructor'][constructor_type].append({
            'params': param_list, 
            'name': constructor_name
        })
    
    def visit_destructor_decl(self, node, o=None):
        if o['destructor'] is not None:
            raise Redeclared('Destructor', node.name)
        # destructor chi co mot nen co loi la raise ngay 
        o['destructor'] = {
            'name': node.name
        }

    def visit_bool_literal(self, node, o=None): return PrimitiveType('boolean')
    def visit_int_literal(self, node, o=None): return PrimitiveType('int')
    def visit_float_literal(self, node, o=None): return PrimitiveType('float')
    def visit_string_literal(self, node, o=None): return PrimitiveType('string')
    def visit_nil_literal(self, node, o=None): return NilLiteral()
    def visit_primitive_type(self, node, o=None): return node
    def visit_reference_type(self, node, o=None): return node
    def visit_array_type(self, node, o=None): return node
    def visit_class_type(self, node, o=None): return node
    def visit_parameter(self, node, o = None): return None
# ==================== Default empty visitor methods ====================
    def visit_array_access(self, node, o=None): return None
    def visit_array_literal(self, node, o=None): return None
    def visit_assignment_statement(self, node, o=None): return None
    def visit_attribute(self, node, o=None): return None
    def visit_binary_op(self, node, o=None): return None
    def visit_block_statement(self, node, o=None): return None
    def visit_break_statement(self, node, o=None): return None
    def visit_continue_statement(self, node, o=None): return None
    def visit_for_statement(self, node, o=None): return None
    def visit_id_lhs(self, node, o=None): return None
    def visit_identifier(self, node, o=None): return None
    def visit_if_statement(self, node, o=None): return None
    def visit_member_access(self, node, o=None): return None
    def visit_method_call(self, node, o=None): return None
    def visit_method_invocation_statement(self, node, o=None): return None
    def visit_object_creation(self, node, o=None): return None
    def visit_postfix_expression(self, node, o=None): return None
    def visit_return_statement(self, node, o=None): return None
    def visit_static_member_access(self, node, o=None): return None
    def visit_static_method_invocation(self, node, o=None): return None
    def visit_unary_op(self, node, o=None): return None
    def visit_variable_decl(self, node, o=None): return None
    def visit_parenthesized_expression(self, node, o = None): return None
    def visit_postfix_lhs(self, node, o = None): return None
    def visit_this_expression(self, node, o = None): return None
    def visit_variable(self, node, o = None): return None
    def visit_method_invocation(self, node, o = None): return None 
class StaticChecker(ASTVisitor):
    """
    Stateless static semantic checker for OPLang using visitor pattern.
    
    Checks for all 10 error types specified in OPLang semantic constraints:
    1. Redeclared - Variables, constants, attributes, classes, methods, parameters
    2. Undeclared - Identifiers, classes, attributes, methods  
    3. CannotAssignToConstant - Assignment to final variables/attributes
    4. TypeMismatchInStatement - Type incompatibilities in statements
    5. TypeMismatchInExpression - Type incompatibilities in expressions
    6. TypeMismatchInConstant - Type incompatibilities in constant declarations
    7. MustInLoop - Break/continue outside loop contexts
    8. IllegalConstantExpression - Invalid expressions in constant initialization
    9. IllegalArrayLiteral - Inconsistent types in array literals
    10. IllegalMemberAccess - Improper access to static/instance members

    Also checks for valid entry point: static void main() with no parameters.
    """

    def _is_type_equal(self,type1,type2):
        if type(type1) != type(type2): 
            return False
        if isinstance(type1, PrimitiveType): 
            return type1.type_name == type2.type_name
        if isinstance(type1, ArrayType): 
            return type1.size == type2.size and self._is_type_equal(type1.element_type, type2.element_type)
        if isinstance(type1,ReferenceType): 
            return type1.referenced_type == type2.referenced_type
        if isinstance(type1,ClassType): 
            return type1.class_name == type2.class_name
        return False
    def _is_type_compatible(self,target_type, source_type,o): # phai vs trai (var vs expr)
        # suy luan kieu tu ParenthesizedExpression, BinaryOp, UnaryOp
        if isinstance(source_type, (ParenthesizedExpression, BinaryOp, UnaryOp)):
            source_type = self.visit(source_type, o)
        if self._is_type_equal(target_type, source_type): # target: node.attr_type ; source: init_value 
            return True
        # kiem tra type corce -> con gi nua khong? 
        if isinstance(target_type, PrimitiveType) and isinstance(source_type, PrimitiveType):
            if target_type.type_name == 'float' and source_type.type_name == 'int':
                return True
        if isinstance(target_type, ArrayType):
            
            #(A[2] a = b)
            if isinstance(source_type, ArrayType):
                if target_type.size != source_type.size:
                    return False
                return self._is_type_equal(target_type.element_type, source_type.element_type)
            elif isinstance(source_type, ArrayLiteral):
                if len(source_type.value) == 0:
                    return True
                if target_type.size != len(source_type.value):
                    return False
                target_el_type = target_type.element_type
                for expr in source_type.value:
                    expr_type = self.visit(expr, o)
                    if isinstance(target_el_type, PrimitiveType):
                        if not isinstance(expr_type, PrimitiveType):
                            return False
                        if target_el_type.type_name != expr_type.type_name:
                            return False
                    elif isinstance(target_el_type, ClassType):
                        if not isinstance(expr_type, ClassType):
                            return False
                        if target_el_type.class_name != expr_type.class_name:
                            return False
                    elif not self._is_type_equal(target_el_type, expr_type):
                        return False
                return True
            else:
                return False
        if not isinstance(target_type, ArrayType) and isinstance(source_type, ArrayLiteral):
            return False



        if isinstance(source_type, ReferenceType):
            return self._is_type_compatible(target_type, source_type.referenced_type, o)
        # class vs ref vs prim
        if isinstance(target_type, ReferenceType) and isinstance(source_type, PrimitiveType):
            return self._is_type_equal(target_type.referenced_type, source_type)
        if isinstance(target_type, ReferenceType) and isinstance(source_type, ClassType):
            return self._is_type_equal(target_type.referenced_type, source_type)
        if isinstance(target_type, ClassType) and isinstance(source_type, ReferenceType):
            return self._is_type_equal(target_type, source_type.referenced_type)
        if isinstance(target_type, ReferenceType) and isinstance(source_type, ReferenceType):
            return self._is_type_equal(target_type.referenced_type, source_type.referenced_type)
        if isinstance(target_type, ClassType) and isinstance(source_type, ClassType):
            return self._is_sub_class(target_type, source_type, o)  
        # nil literal
        if isinstance(source_type, NilLiteral):
            if isinstance(target_type, (ReferenceType, ClassType, ArrayType)):
                return True
        # checking literal
        literal_map = {
        IntLiteral: PrimitiveType('int'),
        FloatLiteral: PrimitiveType('float'),
        BoolLiteral: PrimitiveType('boolean'),
        StringLiteral: PrimitiveType('string'),
    }
        for lit_class, lit_type in literal_map.items():
            if isinstance(source_type, lit_class):
                return self._is_type_compatible(target_type, lit_type, o)
        return False
    
    def _is_sub_class(self,target_type,source_type,o): # a=b 
        env = o['global_env'] if 'global_env' in o else o
        target_name = target_type.class_name
        source_name = source_type.class_name
        if source_name not in env: 
            return False
        cur_name = source_name
        visited = set()
        while cur_name: 
            if cur_name in visited: 
                break
            visited.add(cur_name)

            if cur_name == target_name: 
                return True
            if cur_name not in env: 
                break
            cur_name = env[cur_name]['parent']  
        return False
    def _is_valid_constant_expr(self, expr, o):
        """
        Check if expression is valid for constant initialization.
        Valid: literals, immutable attributes, operators (no method calls)
        Invalid: method calls, mutable variables/attributes, this, object creation
        """
        # Literals are always valid
        if isinstance(expr, (IntLiteral, FloatLiteral, BoolLiteral, StringLiteral)):
            return True
        
        # Array literals - check all elements
        if isinstance(expr, ArrayLiteral):
            return all(self._is_valid_constant_expr(elem, o) for elem in expr.value)
        
        # Nil is not valid for constants
        if isinstance(expr, NilLiteral):
            return False
        
        # Binary operations - check both sides
        if isinstance(expr, BinaryOp):
            return self._is_valid_constant_expr(expr.left, o) and self._is_valid_constant_expr(expr.right, o)
        
        # Unary operations - check operand
        if isinstance(expr, UnaryOp):
            return self._is_valid_constant_expr(expr.operand, o)
        
        # Parenthesized expressions - check inner expression
        if isinstance(expr, ParenthesizedExpression):
            return self._is_valid_constant_expr(expr.expr, o)
        
        # Identifier - check if it's an immutable attribute
        if isinstance(expr, Identifier):
            if o is None:
                return False
            symbol_table = o.get('symbol_table')
            if symbol_table:
                symbol = symbol_table.lookup(expr.name)
                if symbol:
                    # Only immutable (final) attributes are allowed
                    return symbol.value.get('is_final', False)
            return False
        
        # PostfixExpression - check for method calls or mutable access
        if isinstance(expr, PostfixExpression):
            # Check for method calls first
            for op in expr.postfix_ops:
                if isinstance(op, MethodCall):
                    return False
            if isinstance(expr.primary, Identifier):
                if o is None:
                    return False
                symbol_table = o.get('symbol_table')
                if symbol_table:
                    symbol = symbol_table.lookup(expr.primary.name)
                    if symbol:
                        for op in expr.postfix_ops:
                            if isinstance(op, ArrayAccess):
                                if not self._is_valid_constant_expr(op.index, o):                                    # Attribute doesn't exist or is mutable
                                    return False
                            else: 
                                return False
                        # All checks passed - obj.finalAttr is OK
                        return True
            # If primary is 'this', check if accessing final attributes only
            if isinstance(expr.primary, ThisExpression):
                # Verify all member accesses are to final attributes
                for op in expr.postfix_ops:
                    if isinstance(op, MemberAccess):
                        member_name = op.member_name
                        class_name = o.get('class_name')
                        if class_name:
                            global_env = o.get('global_env')
                            if global_env:
                                attr_info = self._find_attribute_in_hierarchy(class_name, member_name, global_env)
                                if attr_info is None or not attr_info.get('is_final', False):
                                    # Attribute doesn't exist or is mutable
                                    return False
                    elif isinstance(op, ArrayAccess):
                        # Array access in constant expression is not allowed
                        return False
                # All checks passed - this.finalAttr is OK
                return True
            
            # For other PostfixExpressions, be conservative
            return False
            
        # neu la this dung mot minh thi ko hop le
        if isinstance(expr, ThisExpression): 
            return False
            
        # Object creation is immutable
        if isinstance(expr, ObjectCreation):
            return all(self._is_valid_constant_expr(arg, o) for arg in expr.args)
        return False
    def _get_inherited_attributes(self, classname, global_env): # only protected or public, read spec carefully
        inherited = {}
        current = classname
        
        visited = set()
        while current and current in global_env:
            if current in visited:
                break  
            visited.add(current)
            
            parent = global_env[current]['parent']
            if parent and parent in global_env:
                for attr_name, attr_data in global_env[parent]['attributes'].items():
                    if attr_name not in inherited:
                        inherited[attr_name] = attr_data
            
            current = parent
        
        return inherited
    def __check_for_entry_point(self,node,o): 
        flag = False
        specify_flag = False
        for name,classfeature in o.items():    
            if name == 'global_vars': 
                continue
            entry_to_check = classfeature['methods']
            if 'main' in entry_to_check:
                main_candidate_info = entry_to_check['main']
                flag = True
                if len(main_candidate_info['params']) == 0 and str(main_candidate_info['return_type']) == 'PrimitiveType(void)' and main_candidate_info['is_static'] == True: 
                    specify_flag = True
                    break

        if flag == False or specify_flag == False: 
            raise NoEntryPoint()
    def _error_priority(self,e): 
        if isinstance(e, (Redeclared, UndeclaredIdentifier, UndeclaredClass, UndeclaredAttribute, UndeclaredMethod)):
            return 1
        if isinstance(e, (TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant)):
            return 2
        if isinstance(e, IllegalMemberAccess):
            return 3
        if isinstance(e, MustInLoop):
            return 4
        if isinstance(e, (CannotAssignToConstant, IllegalConstantExpression)):
            return 5
        if isinstance(e, IllegalArrayLiteral):
            return 6
        return 7 
    def _get_primary_type(self,primary,o): 
        if isinstance(primary,ThisExpression): 
            if o.get('is_in_static_method',False): 
                raise IllegalMemberAccess(primary)
            classname = o['class_name']
            return ClassType(classname)
        if isinstance(primary,Identifier): # 1. object; 2.class_name 
            symbol_table = o['symbol_table']
            symbol = symbol_table.lookup(primary.name)
            if symbol: # obj 
                return symbol.mtype
            
            global_env = o['global_env']
            if primary.name in global_env: 
                return ClassType(primary.name)

            #    raise UndeclaredClass(primary.name)
            return None
            
        if isinstance(primary,ParenthesizedExpression): 
            return self.visit(primary,o)
        if isinstance(primary,UnaryOp): 
            return self.visit(primary,o)
        if isinstance(primary,BinaryOp): 
            return self.visit(primary,o)
        if isinstance(primary,PostfixExpression): 
            return self.visit(primary,o)
        if isinstance(primary,ObjectCreation):
            if primary.class_name not in o['global_env']:
                raise UndeclaredClass(primary.class_name)
            return ClassType(primary.class_name)
        
        if isinstance(primary, IntLiteral):
            return PrimitiveType('int')
        if isinstance(primary, FloatLiteral):
            return PrimitiveType('float')
        if isinstance(primary, BoolLiteral):
            return PrimitiveType('boolean')
        if isinstance(primary, StringLiteral):
            return PrimitiveType('string')
        if isinstance(primary, NilLiteral):
            return NilLiteral()
        return None
    
    def _find_attribute_in_hierarchy(self,class_name, attr_name, global_env):
        visited = set()
        current = class_name 
        while current and current in global_env: 
            if current in visited: 
                break
            visited.add(current)
            class_info = global_env[current]
            if attr_name in class_info['attributes']: 
                return class_info['attributes'][attr_name]
            current = class_info['parent']
        return None
    
    def _find_method_in_hierarchy(self,class_name, method_name, global_env): 
        visited = set()
        current = class_name 
        while current and current in global_env: 
            if current in visited: 
                break
            visited.add(current)
            class_info = global_env[current]
            if method_name in class_info['methods']: 
                return class_info['methods'][method_name]
            current = class_info['parent']
        return None
    
    def _check_method_args(self,args,params,o,context_node = None): 
        if len(args) != len(params): 
            if o.get('target_error') == 'Statement' and context_node:
                raise TypeMismatchInStatement(o['target_node'])
            if context_node:
                raise TypeMismatchInExpression(context_node)
            return False
        for arg, (param_name,param_type) in zip(args,params):
            arg_context = o.copy()
            if 'target_error' in arg_context:
                del arg_context['target_error'] 

            arg_type = self.visit(arg,o)
            if not self._is_type_compatible(param_type,arg_type,o['global_env']): 
                if o.get('target_error') == 'Statement' and context_node:
                    raise TypeMismatchInStatement(o['target_node'])
                if context_node is not None : 
                    raise TypeMismatchInExpression(context_node)
                if o.get('target_error') == 'Statement':
                    raise TypeMismatchInStatement(o['target_node']) # Hoặc node phù hợp
                raise TypeMismatchInStatement(arg)
            
        return True 
    

    def _apply_postfix_op(self,op,current_context,o, postfix_expr =None): 
        current_type = current_context['type']
        is_class_access = current_context.get('is_class_access', False) # Lấy cờ ra
        if isinstance(op,MemberAccess): 
            member_name = op.member_name
            if not isinstance(current_type,ClassType): 
               # sua cho nay 
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
              #  raise TypeMismatchInExpression(postfix_expr if postfix_expr else op)
            class_name = current_type.class_name
            global_env = o['global_env']
            if class_name not in global_env: 
                raise UndeclaredClass(class_name)
            attr_info = self._find_attribute_in_hierarchy(class_name, member_name, global_env)
            if attr_info is None: # chi kiem tra static sau khi biet nos da ton tai testcase 40
                raise UndeclaredAttribute(member_name)
            
            if not is_class_access and attr_info['is_static']:
                 raise IllegalMemberAccess(postfix_expr if postfix_expr else op)
            if is_class_access and not attr_info['is_static']:
                 raise IllegalMemberAccess(postfix_expr if postfix_expr else op)
            
            member_type = attr_info['type']
            return {
                'type': member_type, 
                'is_final': attr_info['is_final'],
                'is_static': attr_info['is_static'],
                'kind': 'attribute',
                'name': member_name, 
                'is_class_access': False
            }
        
        if isinstance(op,MethodCall):
            method_name = op.method_name
            if not isinstance(current_type,ClassType): 
                # thuc ra cho nay tra ve Type mismatchin expression moi dung
                # [unit test] tao test phan undecl phai raise ra trc Type mismatch
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
            class_name = current_type.class_name
            global_env = o['global_env']
            if class_name not in global_env: 
                raise UndeclaredClass(class_name)
            method_info = self._find_method_in_hierarchy(class_name, method_name, global_env)
            
            if method_info is None: 
                raise UndeclaredMethod(method_name)
            self._check_method_args(op.args, method_info['params'],o,postfix_expr)
            if not is_class_access and method_info['is_static']:
                raise IllegalMemberAccess(postfix_expr if postfix_expr else op)
            if is_class_access and not method_info['is_static']:
                raise IllegalMemberAccess(postfix_expr if postfix_expr else op)
           
            self._check_method_args(op.args,method_info['params'],o)
            return_type = method_info['return_type']
            return {
                'type': return_type, 
                'is_final': False,
                'is_static': method_info['is_static'],
                'kind': 'method_res', 
                'is_class_access': False
            }
        
        if isinstance(op,ArrayAccess): 
            index_type = self.visit(op.index,o)
            if not isinstance(index_type,PrimitiveType) or index_type.type_name != 'int': 
                raise TypeMismatchInExpression(op)
            if not isinstance(current_type,ArrayType): 
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
                #raise TypeMismatchInExpression(postfix_expr if postfix_expr else op)
            element_type = current_type.element_type
            return {
                'type': element_type, 
                'is_final': False, 
                'is_static': False, 
                'kind': 'array_element'
           }
        return current_context
    

    def _apply_postfix_op_lhs(self,op,current_context,o,postfix_expr = None): 
        current_type = current_context['type']
        is_class_access = current_context.get('is_class_access', False)
        if isinstance(op,MemberAccess): 
            member_name = op.member_name
            
            if not isinstance(current_type,ClassType): 
               # sua cho nay 
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
            class_name = current_type.class_name
            global_env = o['global_env']
            
            attr_info = self._find_attribute_in_hierarchy(class_name, member_name, global_env)
            if attr_info is None: 
                raise UndeclaredAttribute(member_name)
            if not is_class_access and attr_info['is_static']:
                raise IllegalMemberAccess(postfix_expr if postfix_expr else op)
            if is_class_access and not attr_info['is_static']:
                raise IllegalMemberAccess(postfix_expr)
            member_type = attr_info['type']
            return {
                'type': member_type, 
                'is_final': attr_info['is_final'],
                'is_static': attr_info['is_static'],
                'kind': 'attribute',
                'name': member_name, 
                'is_class_access': False
            }
        if isinstance(op,MethodCall):

            method_name = op.method_name
            if not isinstance(current_type,ClassType): 
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
            
            class_name = current_type.class_name
            global_env = o['global_env']

            if class_name not in global_env: 
                raise UndeclaredClass(class_name)

            method_info = self._find_method_in_hierarchy(class_name, method_name, global_env)
            if method_info is None: 
                raise UndeclaredMethod(method_name)
            if is_class_access and not method_info['is_static']:
                 raise IllegalMemberAccess(op)
            if o.get('is_in_static_method',False) and not method_info['is_static']: 
                raise IllegalMemberAccess(op)
            
            self._check_method_args(op.args,method_info['params'],o)
            return_type = method_info['return_type']

            return {
                'type': return_type, 
                'is_final': False,
                'is_static': method_info['is_static'],
                'kind': 'method_res', 
                'is_class_access': is_class_access
            }
        
        if isinstance(op,ArrayAccess): 
            index_type = self.visit(op.index,o)
            if not isinstance(index_type,PrimitiveType) or index_type.type_name != 'int': 
                raise TypeMismatchInExpression(op)
            if not isinstance(current_type,ArrayType): 
                node_to_report = postfix_expr.primary if postfix_expr else op
                raise TypeMismatchInExpression(node_to_report)
            element_type = current_type.element_type
            return {
                'type': element_type, 
                'is_final': False, 
                'is_static': False, 
                'kind': 'array_element', 
                'is_class_access': False
            }
        return current_context
    def _type_infer(a): 
        if isinstance(a,PrimitiveType): 
            return a.type_name
        if isinstance(a,ArrayType): 
            return a.element_type
        if isinstance(a,ClassType): 
            return a.class_name
        if isinstance(a,ReferenceType): 
            return a.referenced_typ
    def check_variable_declaration(self, vardecl, context):
        var_type = vardecl.var_type
        is_final = vardecl.is_final
        symbol_table = context['symbol_table']
        # checking for var_type validity
        if isinstance(var_type,ClassDecl): 
            if var_type.name not in context['global_env']: 
                raise UndeclaredClass(var_type.name)
        if isinstance(var_type, ReferenceType):
            ref_type = var_type.referenced_type
            if isinstance(ref_type, ClassType):
                if ref_type.class_name not in context['global_env']:
                    raise UndeclaredClass(ref_type.class_name)  

        if isinstance(var_type, PrimitiveType) and var_type.type_name == 'void':
            raise TypeMismatchInStatement(vardecl)
        
        if isinstance(var_type, ClassType):
            if var_type.class_name not in context['global_env']:
                raise UndeclaredClass(var_type.class_name)
        
        if isinstance(var_type, ArrayType):
            element_type = var_type.element_type
            if isinstance(element_type, PrimitiveType) and element_type.type_name == 'void':
                raise TypeMismatchInStatement(vardecl)
            if isinstance(element_type, ArrayType):
                raise TypeMismatchInStatement(vardecl)
            if isinstance(element_type,ClassType): 
                if element_type.class_name not in self.env: 
                    raise UndeclaredClass(element_type.class_name)
            if isinstance(element_type,ReferenceType) and isinstance(element_type.referenced_type,ClassType): 
                if element_type.referenced_type.class_name not in self.env: 
                    raise UndeclaredClass(element_type.referenced_type.class_name)
        # declare symbol first
        for var in vardecl.variables:
            varname = var.name
            if symbol_table.lookup_from_cur(varname) is not None:
                if is_final:
                    raise Redeclared('Constant', varname)
                raise Redeclared('Variable', varname)
            symbol = Symbol( # add trc ddeer co no thay da
                name=varname,
                mtype=var_type,
                value={
                    'kind': 'variable',
                    'is_final': is_final,
                    'init_type': None
                }
            )
            symbol_table.add_symbol(symbol)

            init_type = None
            if var.init_value:
                init_type = self.visit(var.init_value, context)
                if not self._is_type_compatible(var_type, init_type, context):
                    if is_final:
                        raise TypeMismatchInConstant(var.init_value)
                    if isinstance(init_type, PrimitiveType) and init_type.type_name == 'void':
                         raise TypeMismatchInExpression(var.init_value)
                    raise TypeMismatchInStatement(vardecl)
                
                if is_final and not self._is_valid_constant_expr(var.init_value, context):
                    raise IllegalConstantExpression(var.init_value)
            else:
                if is_final:
                    raise IllegalConstantExpression(NilLiteral())
    def _check_always_return(self, stmt):
        if isinstance(stmt, ReturnStatement):
            return True
        
        if isinstance(stmt, BlockStatement):
            for s in stmt.statements:
                if self._check_always_return(s):
                    return True
            return False
            
        if isinstance(stmt, IfStatement):
            if stmt.else_stmt is None:
                return False
            return self._check_always_return(stmt.then_stmt) and self._check_always_return(stmt.else_stmt)
            
        return False
     # ==================== PROGRAM & CLASS DECLARATIONS ====================
    def visit(self, node, o=None):
        return super().visit(node, o)
    def check_program(self, node):
        return self.visit_program(node)
    def visit_program(self, node, o=None):
        phase1 = Phase1()
        self.env = phase1.visit_program(node)
        """
        {
        'Test': {
                'parent': None, 
                'attributes': {}, 
                'methods': {'main': {'is_static': True, 'return_type': 'PrimitiveType(void)', 'params': []}}, 
                'contructor': {}, 
                'destructor': None
                'static': 
                }
        }
        """
        global_symbol_table = SymbolTable()
        global_symbol_table.enter_scope()
        
        global_context = {
            'global_env': self.env,
            'symbol_table': global_symbol_table,
            'loop_depth': 0,
            'is_in_static_method': False,
            'is_in_constructor': False,
            'is_in_destructor': False,
            'current_method_return_type': None
        }
        if 'global_vars' in self.env:
            for var_name, info in self.env['global_vars'].items():
                
                # 1. Nạp vào Symbol Table
                symbol = Symbol(
                    name=var_name,
                    mtype=info['type'],
                    value={
                        'kind': 'variable', # hoặc attribute tuỳ ngữ cảnh, ở đây là global var
                        'is_final': info['is_final'],
                        'init_type': None # Sẽ cập nhật sau khi check xong
                    }
                )
                global_symbol_table.add_symbol(symbol)
                
                if info['init_val']:
                    init_type = self.visit(info['init_val'], global_context)
                    if not self._is_type_compatible(info['type'], init_type, global_context):
                        if info['is_final']:
                            raise TypeMismatchInConstant(info['decl_node']) # Hoặc dùng info['init_val'] tuỳ spec báo lỗi node nào
                        else:
                            raise TypeMismatchInStatement(info['decl_node'])

                    if info['is_final'] and not self._is_valid_constant_expr(info['init_val'], global_context):
                        raise IllegalConstantExpression(info['init_val'])
                else:
                    if info['is_final']:
                        raise IllegalConstantExpression(NilLiteral())

        # --- XỬ LÝ CLASS ---
        # Lúc này Global Symbol Table đã có đủ biến toàn cục, Class có thể sử dụng chúng
        decls = node.decls if hasattr(node, 'decls') else node.class_decls
        for decl in decls: 
            if isinstance(decl, ClassDecl):
                self.visit_class_decl(decl, self.env)
                # Lưu ý: Không cần visit VariableDecl ở đây nữa vì đã xử lý ở trên
        self.__check_for_entry_point(node, self.env)

        # for classdecl in node.class_decls: 
        #     self.visit_class_decl(classdecl,self.env)
        # print_env( self.env)
        # self.__check_for_entry_point(node, self.env)


        for classname, classinfo in self.env.items():
            if classname == 'io' and classname == 'global_vars':
                continue
            
            final_attrs_status = classinfo.get('final_attrs_status', {})
            final_attr_nodes = classinfo.get('final_attr_nodes', {})
            
            for attr_name, init_val in final_attrs_status.items():
                if init_val is None:
                    # Dùng node gốc đã lưu
                    node = final_attr_nodes.get(attr_name)
                    if node:
                        raise IllegalConstantExpression(node)
    def visit_class_decl(self, node, o=None):
        """
        o is dict contain all info of a class
        """

        classname = node.name
        class_info = o[classname]
        symbol_table = SymbolTable()
        symbol_table.enter_scope()
        if 'global_vars' in o:
            for var_name, info in o['global_vars'].items():
                # Kiểm tra trùng tên: Nếu class có attribute trùng tên biến global thì attribute sẽ che khuất (shadow)
                # Nhưng ở bước init scope này, ta cứ add vào trước (scope đáy)
                symbol = Symbol(
                    name=var_name,
                    mtype=info['type'],
                    value={
                        'kind': 'variable', # Global variable/constant
                        'is_final': info['is_final'],
                        'is_static': False, # Global không phải static member
                        'init_val': info['init_val']
                    }
                )
                symbol_table.add_symbol(symbol)
        inherited_attrs = self._get_inherited_attributes(classname,o)
        for attr_name, attr_data in inherited_attrs.items(): 
            symbol = Symbol(
                name=attr_name, 
                mtype=attr_data['type'],
                value ={
                    'kind': 'attribute', 
                    'is_static': attr_data['is_static'],
                    'is_final': attr_data['is_final'],
                    'from_parent': True
                }
            )
            symbol_table.add_symbol(symbol)

        for attr_name, attr_data in class_info['attributes'].items(): 
            # existing = symbol_table.lookup_from_cur(attr_name)
            # if existing and existing.value.get('from_parent'): 
            #     # do type checking
            #     pass 
            symbol = Symbol(
                name=attr_name, 
                mtype=attr_data['type'], 
                value = {
                    'kind': 'attribute', 
                    'is_static': attr_data['is_static'], 
                    'is_final': attr_data['is_final'],
                    'from_parent': False,
                    'init_val': attr_data.get('init_val')
                }
            )
            symbol_table.add_symbol(symbol) # khong can check redecl vi da check o phase 1
        for method_name, method_data in class_info['methods'].items(): 
            if symbol_table.lookup_from_cur(method_name) is not None: 
                raise Redeclared('Method',method_name)
            symbol = Symbol(
                name=method_name, 
                mtype=method_data['return_type'], 
                value = {
                    'kind': 'method', 
                    'is_static': method_data['is_static'], 
                    'from_parent': False
                }
            ) 
            symbol_table.add_symbol(symbol) 

        class_context = {
            'global_env': o, 
            'class_name': classname, 
            'class_info': class_info, 
            'symbol_table': symbol_table, 
            'loop_depth': 0,
            'is_in_static_method': False,
            'is_in_constructor': False,
            'is_in_destructor': False, 
            'current_method_return_type': None
        }
        
        for member in node.members: 
            self.visit(member,class_context)
        # luu thong tin cuar symbol table vao de lat sau check
        final_attrs_status = {}   # attr_name -> (is_final, init_val)

        for name, sym in symbol_table.scopes[0].items():  
            if sym.value['kind'] == 'attribute' and sym.value['is_final'] and not sym.value.get('from_parent',False):
                final_attrs_status[name] = sym.value['init_val']
        class_info['final_attrs_status'] = final_attrs_status

        symbol_table.exit_scope()

    # ==================== MEMBER DECLARATIONS ====================
    def _is_method_call(self, expr,o):
        if isinstance(expr, PostfixExpression):
            for op in expr.postfix_ops:
                if isinstance(op, MethodCall):
                    return True
                if isinstance(op, ArrayAccess):
                    return False
            return False
        
        if isinstance(expr, (ThisExpression, ObjectCreation)):
            return False
        return False
    def visit_attribute_decl(self, node, o=None):
        for attr in node.attributes:
            if node.is_final:
                if 'final_attr_nodes' not in o['class_info']:
                    o['class_info']['final_attr_nodes'] = {}
                o['class_info']['final_attr_nodes'][attr.name] = node

            if attr.init_value is not None: 
                if isinstance(attr.init_value, Identifier): 
                    init_type = self.visit_identifier(attr.init_value, o)
                else: 
                    init_type = self.visit(attr.init_value, o)

                if not self._is_type_compatible(node.attr_type, init_type, o): 
                    if node.is_final: 
                        raise TypeMismatchInConstant(node)
                    raise TypeMismatchInStatement(node)
                
                # Check if expression is valid for constant
                if node.is_final:
                    if not self._is_valid_constant_expr(attr.init_value, o):
                        raise IllegalConstantExpression(attr.init_value)
                    
        return None
    
    def visit_attribute(self, node, o=None):
        return None
    

    # symbol table quanr lys param, attribut, local var -> global env manage method
    def visit_method_decl(self, node, o=None):
        symbol_table = o['symbol_table']
        symbol_table.enter_scope()
        
        for param in node.params: # param da duoc them vao
            param_symbol = Symbol(
                name = param.name, 
                mtype= param.param_type, 
                value = {
                    'kind': 'parameter', 
                    'is_final': False
                }
            )
            if not symbol_table.add_symbol(param_symbol):
                raise Redeclared('Parameter', param.name)
            
        method_context = o.copy()
        method_context['symbol_table'] = symbol_table
        method_context['is_in_static_method'] = node.is_static
        method_context['current_method_return_type'] = node.return_type
        method_context['is_in_constructor'] = False
        method_context['is_in_destructor'] = False
        method_context['is_method_body_scope'] = True

        if node.body: 
            self.visit(node.body, method_context)
    
        symbol_table.exit_scope()
        return None
    
    def visit_constructor_decl(self, node, o=None):
        symbol_table = o['symbol_table']
        # scope 2
        symbol_table.enter_scope()
        
        for param in node.params:
            param_symbol = Symbol(
                name=param.name,
                mtype=param.param_type,
                value={
                    'kind': 'parameter',
                    'is_final': False
                }
            )
            
            if not symbol_table.add_symbol(param_symbol):
                raise Redeclared('Parameter', param.name)
        if node.name != o['class_name']:
            raise TypeMismatchInStatement(node)
        constructor_context = o.copy()
        constructor_context['is_in_static_method'] = False
        constructor_context['is_in_constructor'] = True
        constructor_context['is_in_destructor'] = False
        constructor_context['current_method_return_type'] = None
        constructor_context['symbol_table'] = symbol_table
        constructor_context['is_method_body_scope'] = True
        
        if node.body:
            self.visit(node.body, constructor_context)
        
        symbol_table.exit_scope()
        return None
    
    def visit_destructor_decl(self, node, o=None):
        if node.name != o['class_name']: 
            raise TypeMismatchInStatement(node)
        symbol_table = o['symbol_table']
        symbol_table.enter_scope()
        destructor_context = o.copy()
        destructor_context['is_in_static_method'] = False
        destructor_context['is_in_constructor'] = False
        destructor_context['is_in_destructor'] = True
        destructor_context['current_method_return_type'] = None
        destructor_context['symbol_table'] = symbol_table
        destructor_context['is_method_body_scope'] = True
        
        if node.body:
            self.visit(node.body, destructor_context)
        symbol_table.exit_scope()
        return None
    
    def visit_parameter(self, node, o=None):
        return None
    
    # ==================== VARIABLE DECLARATIONS ====================
    
    def visit_variable_decl(self, node, o=None):
        return node.var_type
    def visit_variable(self, node, o=None):
        return None
    # ==================== STATEMENTS ====================
    

    def visit_assignment_statement(self, node, o=None):
        """
        An **assignment statement** assigns a value to a local variable, a mutable attribute,
          an element of an array, or a reference.
          An assignment takes the following form:  
        <lhs> := <expression>;
        
where the value returned by the `<expression>` is stored in the `<lhs>`,
which can be a local variable, a mutable attribute, an element of an array, or a reference.  
The type of the value returned by the expression must be compatible with the type of lhs.  
        """
        """
        class Test {
            static void main() {
                int x := "hello";
            }
        }  
        current_context = {
                'type': find1.mtype, 
                'is_final': find1.value['is_final'], 
                'is_static': False,
                'kind': find1.value['kind']
            }
        """ # ??
        lhs_info = self.visit(node.lhs, o)
        rhs_type = self.visit(node.rhs, o)
        if isinstance(rhs_type, PrimitiveType) and rhs_type.type_name == 'void':
            raise TypeMismatchInExpression(node.rhs)

        lhs_type = lhs_info['type']
        lhs_is_final = lhs_info.get('is_final', False)
        lhs_is_static = lhs_info.get('is_static', False)
        symbol_table = o['symbol_table']

        # Check final duoc gan trong constructor 
        if lhs_is_final and o['is_in_constructor'] and lhs_info['kind'] == 'attribute': 
            attr_name = lhs_info.get('name')
            if attr_name: 
                symbol = symbol_table.lookup(lhs_info['name'])
                if symbol: 
                    if symbol.value['init_val'] is not None: 
                        raise CannotAssignToConstant(node)
        if not self._is_type_compatible(lhs_type, rhs_type, o['global_env']):
            raise TypeMismatchInStatement(node)            
        if lhs_is_final and not o['is_in_constructor']:
            raise CannotAssignToConstant(node)
        
        # Check static access SAU
        if o.get('is_in_static_method', False):
            if lhs_info.get('kind') == 'attribute' and not lhs_is_static:
                # Nếu đang ở static method và access instance attribute
                if isinstance(node.lhs, PostfixLHS):
                    # is it this.xxx
                    postfix_expr = node.lhs.postfix_expr
                    if isinstance(postfix_expr, PostfixExpression):
                        if isinstance(postfix_expr.primary, ThisExpression):
                            raise IllegalMemberAccess(node.lhs)
        
        
        
        if lhs_info.get('kind') == 'attribute':
            attr_name = lhs_info.get('name')
            if attr_name:
                symbol = symbol_table.lookup(attr_name)
                if symbol:
                    symbol.value['init_val'] = node.rhs

        return None
    
    def visit_block_statement(self, node, o=None):
 

        symbol_table = o['symbol_table']
        is_method_body_scope = o.get('is_method_body_scope', False)

        if not is_method_body_scope:
            symbol_table.enter_scope()
        else:
            o['is_method_body_scope'] = False

        errors = []
        has_return_stmt = False
        for vardecl in node.var_decls:
            try:
                self.check_variable_declaration(vardecl, o)
            except StaticError as e:
                errors.append(e)
        for stmt in node.statements:
            try:
                if not has_return_stmt and self._check_always_return(stmt):
                    has_return_stmt = True
                self.visit(stmt, o)
            except StaticError as e:
                errors.append(e)


        expect_type = o['current_method_return_type']

        if not o.get('is_in_constructor') and not o.get('is_in_destructor') and not has_return_stmt: 
            if expect_type and not (isinstance(expect_type,PrimitiveType) and expect_type.type_name == 'void'):
                err_node = ReturnStatement(NilLiteral())
                errors.append(TypeMismatchInStatement(err_node))
        if errors:
            errors.sort(key=lambda e: self._error_priority(e))
            raise errors[0]

        if not is_method_body_scope:
            symbol_table.exit_scope()
        return None
    




    def visit_if_statement(self, node, o=None):
        condition_type = self.visit(node.condition, o)
        
        if not isinstance(condition_type, PrimitiveType) or condition_type.type_name != 'boolean':
            raise TypeMismatchInStatement(node)
        
        self.visit(node.then_stmt, o)
        
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        
        return None
    
    def visit_for_statement(self, node, o=None): # node.variable is in scalar type
        symbol_table = o['symbol_table']
  
        start_type = self.visit(node.start_expr, o)
        end_type = self.visit(node.end_expr, o)
        if not isinstance(start_type, PrimitiveType) or start_type.type_name != 'int':
            raise TypeMismatchInStatement(node)
        if not isinstance(end_type, PrimitiveType) or end_type.type_name != 'int':
            raise TypeMismatchInStatement(node)

        symbol_table.enter_scope()
        
        if symbol_table.lookup_from_cur(node.variable) is not None:
            raise Redeclared('Variable', node.variable)
        
        existing = symbol_table.lookup(node.variable)
        if existing and existing.value.get('is_final', False):
            raise CannotAssignToConstant(node)
        if existing: 
            var_type = existing.mtype
            if not isinstance(var_type,PrimitiveType) or var_type.type_name != 'int' or (var_type.type_name != start_type.type_name and var_type.type_name != end_type.type_name ):
                raise TypeMismatchInStatement(node)
        
        loop_var_symbol = Symbol(
            name=node.variable,
            mtype=PrimitiveType('int'),
            value={
                'kind': 'variable',
                'is_final': False
            }
        )
        symbol_table.add_symbol(loop_var_symbol)
        
        loop_context = o.copy()
        loop_context['loop_depth'] = o['loop_depth'] + 1
        loop_context['symbol_table'] = symbol_table
        
        self.visit(node.body, loop_context)
        
        symbol_table.exit_scope()
        return None
        
    def visit_break_statement(self, node, o=None):
        loop_count = o['loop_depth']
        if loop_count == 0: 
            raise MustInLoop(node)
        return None
    def visit_continue_statement(self, node, o=None):
        loop_count = o['loop_depth']
        if loop_count == 0: 
            raise MustInLoop(node)
        return None
    def _is_int_float_mismatch(self,a,b): 
        if isinstance(a,PrimitiveType) and isinstance(b,PrimitiveType): 
            if a.type_name == 'float' and b.type_name == 'int': 
                return False
            if a.type_name == 'int' and b.type_name == 'float': 
                return False
        return True
    def visit_return_statement(self, node, o=None):
        
        if o.get('is_in_constructor', False):
            raise TypeMismatchInStatement(node)
                
        if o.get('is_in_destructor', False):
            raise TypeMismatchInStatement(node)   
        if isinstance(node.value,NilLiteral): 
            return_type = NilLiteral()
        else:
            return_type = self.visit(node.value, o)
        expect_type = o['current_method_return_type']
        # if not self._is_int_float_mismatch(return_type,expect_type): 
        #     raise TypeMismatchInStatement(node)
        if isinstance(expect_type, PrimitiveType) and expect_type.type_name == 'void':
            if not isinstance(node.value, NilLiteral):
                raise TypeMismatchInStatement(node)
            return None
        if node.value is None:
             raise TypeMismatchInStatement(node)

        # Kiểm tra kiểu
        if isinstance(return_type, PrimitiveType) and return_type.type_name == 'void':
             raise TypeMismatchInExpression(node.value)
        
        if not self._is_type_compatible(expect_type,return_type,o['global_env']): 
            raise TypeMismatchInStatement(node)
        return None
    
    def visit_method_invocation_statement(self, node, o=None):
        # bo dk nay di vi 
        # if not isinstance(method_type, PrimitiveType) or method_type.type_name != 'void':
        #     raise TypeMismatchInStatement(node)
        stmt_context = o.copy()
        stmt_context['target_error'] = 'Statement' 
        stmt_context['target_node'] = node
        # 2. Truyền context này xuống dưới
        method_type = self.visit(node.method_call, stmt_context)
        return None
    # ==================== LEFT-HAND SIDE EXPRESSIONS ====================
    
    def visit_id_lhs(self, node, o=None): # 
        symbol_table = o['symbol_table']
        symbol = symbol_table.lookup(node.name)
        
        if symbol is None: 
            raise UndeclaredIdentifier(node.name)
        if o.get('is_in_static_method', False):
            if symbol.value.get('kind') == 'attribute' and not symbol.value.get('is_static', False):
                raise UndeclaredIdentifier(node.name)
            
        return {
            'type': symbol.mtype, 
            'is_final': symbol.value.get('is_final', False),
            'is_static': symbol.value.get('is_static', False),
            'kind': symbol.value.get('kind', 'variable'),
            'name': node.name
        }

    def visit_postfix_lhs(self, node, o=None):
        
        if isinstance(node.postfix_expr,PostfixExpression): 
            primary = node.postfix_expr.primary # this, bin, una, id, obj cre, postfix_expr 
            postfix_ops = node.postfix_expr.postfix_ops # member access, method call, array acces 
            
            current_type = self._get_primary_type(primary,o)
            if isinstance(current_type,ClassType): 
                if current_type.class_name not in self.env: 
                    raise UndeclaredClass(current_type.class_name)
            if isinstance(current_type,ReferenceType) and isinstance(current_type.referenced_type,ClassType): 
                if current_type.referenced_type.class_name not in self.env: 
                    raise UndeclaredClass(current_type.referenced_type.class_name)
            is_class_access = False
            if isinstance(primary, Identifier):
                # Nếu không tìm thấy trong symbol table (không phải biến)
                # Nhưng lại có trong global_env (là tên class) -> Đang truy cập qua tên class
                if o['symbol_table'].lookup(primary.name) is None:
                    if primary.name in o['global_env']:
                        is_class_access = True

            current_context = {
                'type': current_type, 
                'is_final': False, 
                'is_static': False,
                'kind': 'expr', 
                'is_class_access': is_class_access
            }
            for op in postfix_ops: 
                current_context = self._apply_postfix_op_lhs(op,current_context,o,node.postfix_expr)

            return current_context
    
    # ==================== EXPRESSIONS ====================

    def visit_binary_op(self, node, o=None):
        """
        remain unary and !
        ['+', '-', '*', '/', '\','%']
        ArrayType, PrimaryType, ClassType, RefType
        """
        # type of operand
        leftn = node.left
        rightn = node.right
        while isinstance(leftn, ParenthesizedExpression):
            leftn = leftn.expr
        while isinstance(rightn, ParenthesizedExpression):
            rightn = rightn.expr
        left = self.visit(leftn,o)
        right = self.visit(rightn,o)
        operator = node.operator
        if (isinstance(left, PrimitiveType) and left.type_name == 'void') or (isinstance(right, PrimitiveType) and right.type_name == 'void'):
            raise TypeMismatchInExpression(node)
        if operator in ['+', '-', '*', '/', '\\', '%']:
            if isinstance(left,PrimitiveType) and isinstance(right,PrimitiveType): 
                lt = left.type_name
                rt = right.type_name
                if operator in ['\\', '%']:
                    if lt != 'int' or rt != 'int': 
                        raise TypeMismatchInExpression(node)
                    return PrimitiveType('int')
                if operator == '/': 
                    if lt not in ['int', 'float'] or rt not in ['int', 'float']: 
                        raise TypeMismatchInExpression(node)
                    return PrimitiveType('float')
                else: 
                    if lt not in ['int', 'float'] or rt not in ['int', 'float']: 
                        raise TypeMismatchInExpression(node)
                    if lt == rt: 
                        return PrimitiveType(lt)
                    else: 
                        return PrimitiveType('float')
            elif isinstance(left, (ArrayType, ReferenceType)) and isinstance(right, (ArrayType, ReferenceType)):
                pass
        if operator in ['&&', '||']: 
            if isinstance(left,PrimitiveType) and isinstance(right,PrimitiveType):
                left_infered_type = left.type_name
                right_infered_type =right.type_name
                if left_infered_type != 'boolean' or right_infered_type != 'boolean': 
                    raise TypeMismatchInExpression(node)
                return PrimitiveType('boolean')
            
        if operator in ['==', '!=', '>', '<', '>=', '<=']:
            if operator in ['==', '!=']: 
                if isinstance(left,PrimitiveType) and isinstance(right,PrimitiveType):
                    lt = left.type_name
                    rt = right.type_name
                    if lt!=rt or lt not in ['int', 'boolean']: 
                        raise TypeMismatchInExpression(node)
                    return PrimitiveType('boolean')
                elif isinstance(left, (ArrayType, ReferenceType)) and isinstance(right, (ArrayType, ReferenceType)):
                    pass
            else: 
                if isinstance(left,PrimitiveType) and isinstance(right,PrimitiveType):
                    lt = left.type_name
                    rt = right.type_name
                    if lt not in ['int', 'float'] or rt not in ['int', 'float']: 
                        raise TypeMismatchInExpression(node)
                    return PrimitiveType('boolean')
                elif isinstance(left, (ArrayType, ReferenceType)) and isinstance(right, (ArrayType, ReferenceType)):
                    pass

        if operator == '^': 
            if isinstance(left,PrimitiveType) and isinstance(right,PrimitiveType):
                left_infered_type = left.type_name
                right_infered_type = right.type_name
                if left_infered_type != 'string' or right_infered_type !='string': 
                    raise TypeMismatchInExpression(node)
                return PrimitiveType('string')
        raise TypeMismatchInExpression(node)  
    def visit_unary_op(self, node, o=None):
        operand = node.operand
        while isinstance(operand, ParenthesizedExpression):
            operand = operand.expr
        operand_type = self.visit(node.operand, o)
        operator = node.operator
        
        if operator == '!':
            if not isinstance(operand_type, PrimitiveType) or operand_type.type_name != 'boolean':
                raise TypeMismatchInExpression(node)
            return PrimitiveType('boolean')
        
        if operator in ['+', '-']:
            if not isinstance(operand_type, PrimitiveType):
                raise TypeMismatchInExpression(node)
            if operand_type.type_name not in ['int', 'float']:
                raise TypeMismatchInExpression(node)
            return operand_type
        
        raise TypeMismatchInExpression(node)    
        
    def visit_parenthesized_expression(self, node, o=None):
        inner = node.expr
        while(isinstance(inner, ParenthesizedExpression)):
            inner = inner.expr
        return self.visit(inner, o)
    # ==================== POSTFIX EXPRESSIONS ====================
    
    def visit_postfix_expression(self, node, o=None):
        primary = node.primary # this, bin, una, id, obj cre, postfix_expr 
        postfix_ops = node.postfix_ops # member access, method call, array acces
        try: 
            current_type = self._get_primary_type(primary,o)
        except UndeclaredIdentifier as e:
            if isinstance(primary, Identifier) and len(postfix_ops) > 0:
                if isinstance(postfix_ops[0], MethodCall):
                    raise UndeclaredMethod(primary.name)
            raise e
        if o.get('is_in_static_method', False) and isinstance(primary, Identifier):
            symbol = o['symbol_table'].lookup(primary.name)
            if symbol and symbol.value.get('kind') == 'attribute' and not symbol.value.get('is_static', False):
                raise IllegalMemberAccess(node) 
        if current_type is None:
            if isinstance(primary, Identifier):
                if len(postfix_ops) > 0 and isinstance(postfix_ops[0], MethodCall) and primary.name == postfix_ops[0].method_name:
                    current_type = ClassType(o['class_name'])
                    
                else:
                    raise UndeclaredIdentifier(primary.name)
            else:
                 pass



        if isinstance(current_type,ClassType): 
            if current_type.class_name not in self.env: 
                raise UndeclaredClass(current_type.class_name)
        if isinstance(current_type,ReferenceType) and isinstance(current_type.referenced_type,ClassType): 
            if current_type.referenced_type.class_name not in self.env: 
                raise UndeclaredClass(current_type.referenced_type.class_name)
        if isinstance(current_type,ClassType) and isinstance(primary,Identifier): 
            # class_attrs = o['global_env'][primary.name]['attributes']
            # for item
            pass
        is_class_access = False
        if isinstance(primary, Identifier):
            if o['symbol_table'].lookup(primary.name) is None:
                if primary.name in o['global_env']:
                    is_class_access = True

        current_context = {
            'type': current_type, 
            'is_final': False, 
            'is_static': False,
            'kind': 'expr', 
            'is_class_access': is_class_access
        }
        for op in postfix_ops: 
            current_context = self._apply_postfix_op(op,current_context,o,node)

        return current_context['type']  
    def visit_array_access(self, node, o=None):
        return None

    def visit_member_access(self, node, o=None):
        return None 
    def visit_method_call(self, node, o=None):
        return None 
    def visit_method_invocation(self, node, o=None):
        return super().visit_method_invocation(node, o)
    
    def visit_static_member_access(self, node, o=None):
        return super().visit_static_member_access(node, o)
    
    def visit_static_method_invocation(self, node, o=None):
        return super().visit_static_method_invocation(node, o)
    
    # ==================== OBJECT & ARRAY CREATION ====================
        
    def visit_object_creation(self, node, o=None):
        class_name = node.class_name
        global_env = o['global_env']
        if class_name not in global_env: 
            raise UndeclaredClass(class_name)
        
        class_info = global_env[class_name]
        constructors = class_info.get('constructor', {})

        num_args = len(node.args)
        arg_types = [self.visit(arg, o) for arg in node.args]

        constructor_type = None
        matched = False
        # neu khong co constructor nao ca thi them vao default
        if not constructors: 
            constructors['default'] = [{
            'params': [], 
            'name': class_name
        }]
    
        if num_args == 0:
            constructor_type = 'default'
            if constructor_type not in constructors:
                raise TypeMismatchInExpression(node)
            matched = True

        elif num_args == 1:
            arg_type = arg_types[0]
            if isinstance(arg_type, ClassType) and arg_type.class_name == class_name:
                constructor_type = 'copy'
                if constructor_type not in constructors:
                    raise TypeMismatchInExpression(node)
                matched = True

        if not matched:
            constructor_type = 'user-defined'
            if constructor_type not in constructors:
                raise TypeMismatchInExpression(node)

            matched = False
            for ctor in constructors[constructor_type]:
                params = ctor['params']
                if len(params) != num_args:
                    continue
                try:
                    self._check_method_args(node.args, params, o,node)
                    matched = True
                    break
                except TypeMismatchInExpression:
                    continue
            
            if not matched:
                raise TypeMismatchInExpression(node)
        return ClassType(class_name)
    def visit_array_literal(self, node, o=None): # khi nao gapj test arraylit thi xem lai
        if len(node.value) == 0: 
            return ArrayLiteral([])  #do
        ret_str = []
        for item in node.value:
            ret_str.append(item)
        type_first = self.visit(node.value[0],o) # ***
        for elem in node.value[1:]:
            temp = self.visit(elem,o)
            if not self._is_type_equal(temp, type_first):
                raise IllegalArrayLiteral(ArrayLiteral(ret_str))
        return ArrayLiteral(node.value)
    # ==================== LITERALS ====================
    
    def visit_bool_literal(self, node, o=None):
        return PrimitiveType('boolean')
    
    def visit_int_literal(self, node, o=None):
        return PrimitiveType('int')
    
    def visit_float_literal(self, node, o=None):
        return PrimitiveType('float')
    
    def visit_string_literal(self, node, o=None):
        return PrimitiveType('string')
    
    def visit_nil_literal(self, node, o=None):
        return NilLiteral()
    
    # ==================== IDENTIFIERS & SPECIAL EXPRESSIONS ====================
    
    def visit_identifier(self, node, o=None, context = None):
        """
        if context in [biến local, parameter, biến vòng for]
        """
        symbol_table = o['symbol_table']
        cur = symbol_table.lookup(node.name)
        if cur is None:
            if context == "attr": # chac chan dc goi tu attribute
                raise UndeclaredAttribute(node.name)  
            if node.name in o['global_env']:
                return ClassType(node.name)
            raise UndeclaredIdentifier(node.name)
        kind = cur.value.get('kind')
        if kind == 'attribute' or kind == 'method':
            raise UndeclaredIdentifier(node.name)
        return cur.mtype
    def visit_this_expression(self, node, o=None):
        """Get type of 'this' expression"""
        if o.get('is_in_static_method', False):
            raise IllegalMemberAccess(node)
        
        return ClassType(o['class_name'])
    # ==================== TYPE NODES ====================
    
    def visit_primitive_type(self, node, o=None):
        return node 
    def visit_array_type(self, node, o=None):
        return node
    def visit_class_type(self, node, o=None):
        return node
    def visit_reference_type(self, node, o=None):
        return node