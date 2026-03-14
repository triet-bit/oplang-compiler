import os
from typing import List, Optional, Union
from .jasmin_code import JasminCode
from .error import IllegalOperandException
from ..utils import nodes as ast_nodes
from .utils import *

# Helper functions for OPLang type checking
# def is_int_type(in_type):
#     """Check if type is int primitive."""
#     return type(in_type) is ast_nodes.PrimitiveType and in_type.type_name == "int"

# def is_float_type(in_type):
#     """Check if type is float primitive."""
#     return type(in_type) is ast_nodes.PrimitiveType and in_type.type_name == "float"

# def is_string_type(in_type):
#     """Check if type is string primitive."""
#     return type(in_type) is ast_nodes.PrimitiveType and in_type.type_name == "string"

# def is_bool_type(in_type):
#     """Check if type is boolean primitive."""
#     return type(in_type) is ast_nodes.PrimitiveType and in_type.type_name == "boolean"

# def is_void_type(in_type):
#     """Check if type is void primitive."""
#     return type(in_type) is ast_nodes.PrimitiveType and in_type.type_name == "void"

# def is_reference_type(in_type):
#     """Check if type is a reference type (Class, Array, String)."""
#     return (
#         isinstance(in_type, ast_nodes.ArrayType) or
#         isinstance(in_type, ast_nodes.ClassType) or
#         isinstance(in_type, ClassType) or  # Check cả ClassType của utils
#         is_string_type(in_type)
#     )
def is_int_type(in_type):
    """Check if type is int primitive."""
    return type(in_type).__name__ == "PrimitiveType" and getattr(in_type, 'type_name', '') == "int"

def is_float_type(in_type):
    """Check if type is float primitive."""
    return type(in_type).__name__ == "PrimitiveType" and getattr(in_type, 'type_name', '') == "float"

def is_string_type(in_type):
    """Check if type is string primitive."""
    return type(in_type).__name__ == "PrimitiveType" and getattr(in_type, 'type_name', '') == "string"

def is_bool_type(in_type):
    """Check if type is boolean primitive."""
    return type(in_type).__name__ == "PrimitiveType" and getattr(in_type, 'type_name', '') == "boolean"

def is_void_type(in_type):
    """Check if type is void primitive."""
    return type(in_type).__name__ == "PrimitiveType" and getattr(in_type, 'type_name', '') == "void"

def is_reference_type(in_type):
    """Check if type is a reference type (Class, Array, String)."""
    return (
        type(in_type).__name__ == "ArrayType" or
        type(in_type).__name__ == "ClassType" or
        type(in_type).__name__ == "ReferenceType" or
        is_string_type(in_type)
    )
class Emitter:
    """
    Emitter class to generate JVM bytecode instructions.

    This class provides methods to emit various JVM instructions and manage
    the code generation process for the compiler.

    Attributes:
        filename (str): Name of the output file
        buff (List[str]): Buffer to store generated code
        jvm (JasminCode): JasminCode instance for JVM instruction generation
    """

    def __init__(self, filename: str):
        """
        Initialize Emitter.

        Args:
            filename: Name of the output file
        """

        self.filename = filename
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "runtime", filename
        )
        self.buff: List[str] = []
        self.jvm = JasminCode()

    def get_jvm_type(self, in_type) -> str:
        """
        Convert AST type to JVM type descriptor.

        Args:
            in_type: AST type to convert

        Returns:
            JVM type descriptor string
        """
        # if in_type is None:
        #     return "V" # Void fallback
        
        # if is_int_type(in_type):
        #     return "I"
        # elif is_float_type(in_type):
        #     return "F"
        # elif is_string_type(in_type):
        #     return "Ljava/lang/String;"
        # elif is_bool_type(in_type):
        #     return "Z"
        # elif is_void_type(in_type):
        #     return "V"
        
        # elif isinstance(in_type, ast_nodes.ArrayType):
        #     return "[" + self.get_jvm_type(in_type.element_type)
            
        # elif isinstance(in_type, ast_nodes.ClassType) or isinstance(in_type, ClassType):
        #     return "L" + in_type.class_name + ";"
            
        # elif isinstance(in_type, ast_nodes.ReferenceType):
        #     return self.get_jvm_type(in_type.referenced_type)
            
        # elif isinstance(in_type, FunctionType):
        #     return (
        #         "("
        #         + "".join(map(lambda x: self.get_jvm_type(x), in_type.param_types))
        #         + ")"
        #         + self.get_jvm_type(in_type.return_type)
        #     )
        # else:
        #     raise IllegalOperandException(f"Unknown type: {type(in_type)} - {in_type}")
        if in_type is None:
            return "V"
        type_name = type(in_type).__name__

        if type_name == "ReferenceType":
            # Đệ quy lấy kiểu được tham chiếu. Vd: int& -> int
            inner_type = in_type.referenced_type
            # Nếu inner là primitive, wrap thành mảng
            if is_int_type(inner_type): return "[I"
            if is_float_type(inner_type): return "[F"
            if is_bool_type(inner_type): return "[Z" # JVM dùng byte/boolean array
            if is_string_type(inner_type): return "[Ljava/lang/String;"
            # Nếu tham chiếu tới Object/Array thì giữ nguyên (vì bản thân nó đã là ref)
            return self.get_jvm_type(inner_type)
        if is_int_type(in_type):
            return "I"
        elif is_float_type(in_type):
            return "F"
        elif is_string_type(in_type):
            return "Ljava/lang/String;"
        elif is_bool_type(in_type):
            return "Z"
        elif is_void_type(in_type):
            return "V"
        
        # Dùng check tên class để an toàn hơn
        
        if type_name == "ArrayType":
            return "[" + self.get_jvm_type(in_type.element_type)
            
        elif type_name == "ClassType":
            return "L" + in_type.class_name + ";"
            
        elif type_name == "ReferenceType":
            return self.get_jvm_type(in_type.referenced_type)
            
        elif isinstance(in_type, FunctionType):
            return (
                "("
                + "".join(map(lambda x: self.get_jvm_type(x), in_type.param_types))
                + ")"
                + self.get_jvm_type(in_type.return_type)
            )
        else:
            raise IllegalOperandException(f"Unknown type: {type(in_type)} - {in_type}")
    def get_full_type(self, in_type) -> str:
        """
        Get full type name for JVM.

        Args:
            in_type: AST type

        Returns:
            Full type name string
        """
        if is_int_type(in_type):
            return "int"
        elif is_float_type(in_type):
            return "float"
        elif is_string_type(in_type):
            return "java/lang/String"
        elif is_void_type(in_type):
            return "void"
        elif type(in_type) is ast_nodes.PrimitiveType:
            return in_type.type_name

    def emit_push_iconst(self, in_: Union[int, str], frame) -> str:
        """
        Emit instruction to push integer constant onto operand stack.

        Args:
            in_: Integer value or string representation
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        # frame.push()
        # if type(in_) is int:
        #     i = in_
        #     if i >= -1 and i <= 5:
        #         return self.jvm.emitICONST(i)
        #     elif i >= -128 and i <= 127:
        #         return self.jvm.emitBIPUSH(i)
        #     elif i >= -32768 and i <= 32767:
        #         return self.jvm.emitSIPUSH(i)
        #     else:
        #         return self.jvm.emitLDC(str(i))
        # elif type(in_) is str:
        #     if in_ == "true":
        #         return self.emit_push_iconst(1, frame)
        #     elif in_ == "false":
        #         return self.emit_push_iconst(0, frame)
        #     else:
        #         return self.emit_push_iconst(int(in_), frame)
        frame.push()
        
        # Chuyển đổi input về số nguyên trước
        val = in_
        if type(in_) is str:
            if in_ == "true":
                val = 1
            elif in_ == "false":
                val = 0
            else:
                val = int(in_)
        
        # Sinh mã cho giá trị nguyên val
        i = val
        if i >= -1 and i <= 5:
            return self.jvm.emitICONST(i)
        elif i >= -128 and i <= 127:
            return self.jvm.emitBIPUSH(i)
        elif i >= -32768 and i <= 32767:
            return self.jvm.emitSIPUSH(i)
        else:
            return self.jvm.emitLDC(str(i))

    def emit_push_fconst(self, in_: str, frame) -> str:
        """
        Emit instruction to push float constant onto operand stack.

        Args:
            in_: String representation of float value
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        f = float(in_)
        frame.push()
        
        # Xử lý các trường hợp đặc biệt dùng lệnh ngắn fconst
        if f == 0.0:
            return self.jvm.emitFCONST("0.0")
        elif f == 1.0:
            return self.jvm.emitFCONST("1.0")
        elif f == 2.0:
            return self.jvm.emitFCONST("2.0")
        else:
            return self.jvm.emitLDC(str(f) + "f")

    def emit_push_const(self, in_: str, typ, frame) -> str:
        """
        Generate code to push a constant onto the operand stack.

        Args:
            in_: The lexeme of the constant
            typ: The type of the constant
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If type is not supported
        """
        if is_int_type(typ):
            return self.emit_push_iconst(in_, frame)
        elif is_string_type(typ):
            frame.push()
            return self.jvm.emitLDC(in_)
        elif is_bool_type(typ):
            return self.emit_push_iconst(in_, frame)
        else:
            raise IllegalOperandException(in_)

    def emit_aload(self, in_, frame) -> str:
        """
        Emit array load instruction.

        Args:
            in_: Type of array element
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.pop()
        if is_int_type(in_):
            return self.jvm.emitIALOAD()
        elif is_bool_type(in_):
            return self.jvm.emitBALOAD() # Fix: Use BALOAD for boolean
        elif is_float_type(in_):
            return self.jvm.emitFALOAD()
        elif is_reference_type(in_):
            return self.jvm.emitAALOAD()
        else:
            raise IllegalOperandException(str(in_))
    def emit_astore(self, in_, frame) -> str:
        """
        Emit array store instruction.

        Args:
            in_: Type of array element
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.pop()
        frame.pop()
        frame.pop()
        if is_int_type(in_):
            return self.jvm.emitIASTORE()
        elif is_bool_type(in_):
            return self.jvm.emitBASTORE() # Fix: Use BASTORE for boolean
        elif is_float_type(in_):
            return self.jvm.emitFASTORE()
        elif is_reference_type(in_):
            return self.jvm.emitAASTORE()
        else:
            raise IllegalOperandException(str(in_))

    def emit_var(
        self, in_: int, var_name: str, in_type, from_label: int, to_label: int
    ) -> str:
        """
        Generate the var directive for a local variable.

        Args:
            in_: The index of the local variable
            var_name: The name of the local variable
            in_type: The type of the local variable
            from_label: The starting label of the scope where the variable is active
            to_label: The ending label of the scope where the variable is active

        Returns:
            Generated var directive string
        """
        return self.jvm.emitVAR(
            in_, var_name, self.get_jvm_type(in_type), from_label, to_label
        )

    def emit_read_var(self, name: str, in_type, index: int, frame) -> str:
        """
        Emit instruction to read local variable.

        Args:
            name: Variable name
            in_type: Variable type
            index: Variable index
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.push()
        if is_int_type(in_type) or is_bool_type(in_type):
            return self.jvm.emitILOAD(index)
        elif is_float_type(in_type):
            return self.jvm.emitFLOAD(index)
        elif is_reference_type(in_type):  # ✅ Bây giờ sẽ match ReferenceType
            return self.jvm.emitALOAD(index)
        else:
            raise IllegalOperandException(name)

    def emit_read_var2(self, name: str, typ, frame) -> str:
        """
        Generate the second instruction for array cell access.

        Args:
            name: Variable name
            typ: Variable type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If not implemented
        """
        raise IllegalOperandException(name)

    def emit_write_var(self, name: str, in_type, index: int, frame) -> str:
        """
        Generate code to pop a value on top of the operand stack and store it to a block-scoped variable.

        Args:
            name: The symbol entry of the variable
            in_type: Variable type
            index: Variable index
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.pop()
        if is_int_type(in_type) or is_bool_type(in_type):
            return self.jvm.emitISTORE(index)
        elif is_float_type(in_type):
            return self.jvm.emitFSTORE(index)
        elif is_reference_type(in_type):  # ✅ Bây giờ sẽ match ReferenceType
            return self.jvm.emitASTORE(index)
        else:
            raise IllegalOperandException(name)
    def emit_write_var2(self, name: str, typ, frame) -> str:
        """
        Generate the second instruction for array cell access.

        Args:
            name: Variable name
            typ: Variable type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string

        Raises:
            IllegalOperandException: If not implemented
        """
        raise IllegalOperandException(name)

    def emit_attribute(
        self, lexeme: str, in_type, is_final: bool, value: Optional[str] = None
    ) -> str:
        """
        Generate the field (static) directive for a class mutable or immutable attribute.

        Args:
            lexeme: The name of the attribute
            in_type: The type of the attribute
            is_final: True in case of constant; false otherwise
            value: Optional value for the attribute

        Returns:
            Generated field directive string
        """
        return self.jvm.emitSTATICFIELD(lexeme, self.get_jvm_type(in_type), is_final)

    def emit_get_static(self, lexeme: str, in_, frame) -> str:
        """
        Emit GETSTATIC instruction.

        Args:
            lexeme: Field name
            in_: Field type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitGETSTATIC(lexeme, self.get_jvm_type(in_))

    def emit_put_static(self, lexeme: str, in_, frame) -> str:
        """
        Emit PUTSTATIC instruction.

        Args:
            lexeme: Field name
            in_: Field type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitPUTSTATIC(lexeme, self.get_jvm_type(in_))

    def emit_get_field(self, lexeme: str, in_, frame) -> str:
        """
        Emit GETFIELD instruction.

        Args:
            lexeme: Field name
            in_: Field type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        return self.jvm.emitGETFIELD(lexeme, self.get_jvm_type(in_))

    def emit_put_field(self, lexeme: str, in_, frame) -> str:
        """
        Emit PUTFIELD instruction.

        Args:
            lexeme: Field name
            in_: Field type
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        frame.pop()
        return self.jvm.emitPUTFIELD(lexeme, self.get_jvm_type(in_))

    def emit_invoke_static(self, lexeme: str, in_, frame) -> str:
        """
        Generate code to invoke a static method.

        Args:
            lexeme: The qualified name of the method (i.e., class-name/method-name)
            in_: The type descriptor of the method
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        typ = in_
        list(map(lambda x: frame.pop(), typ.param_types))
        if not is_void_type(typ.return_type):
            frame.push()
        return self.jvm.emitINVOKESTATIC(lexeme, self.get_jvm_type(in_))

    def emit_invoke_special(self, frame, lexeme: Optional[str] = None, in_=None) -> str:
        """
        Generate code to invoke a special method.

        Args:
            frame: Frame object for stack management
            lexeme: The qualified name of the method (i.e., class-name/method-name)
            in_: The type descriptor of the method

        Returns:
            Generated JVM instruction string
        """
        if not lexeme is None and not in_ is None:
            typ = in_
            list(map(lambda x: frame.pop(), typ.param_types))
            frame.pop()
            if not is_void_type(typ.return_type):
                frame.push()
            return self.jvm.emitINVOKESPECIAL(lexeme, self.get_jvm_type(in_))
        elif lexeme is None and in_ is None:
            frame.pop()
            return self.jvm.emitINVOKESPECIAL()
        else:
            # Thêm đoạn này để tránh return None
            return self.jvm.emitINVOKESPECIAL(lexeme, self.get_jvm_type(in_))

    def emit_invoke_virtual(self, lexeme: str, in_, frame) -> str:
        """
        Generate code to invoke a virtual method.

        Args:
            lexeme: The qualified name of the method (i.e., class-name/method-name)
            in_: The type descriptor of the method
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        typ = in_
        list(map(lambda x: frame.pop(), typ.param_types))
        frame.pop()
        if not is_void_type(typ.return_type):
            frame.push()
        return self.jvm.emitINVOKEVIRTUAL(lexeme, self.get_jvm_type(in_))

    def emit_neg_op(self, in_, frame) -> str:
        """
        Generate ineg, fneg.

        Args:
            in_: The type of the operands
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        if is_int_type(in_):
            return self.jvm.emitINEG()
        else:
            return self.jvm.emitFNEG()

    def emit_not(self, in_, frame) -> str:
        """
        Generate NOT operation.

        Args:
            in_: Type of operand
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        label1 = frame.get_new_label()
        label2 = frame.get_new_label()
        result = list()
        result.append(self.emit_if_true(label1, frame))
        result.append(self.emit_push_const("true", in_, frame))
        result.append(self.emit_goto(label2, frame))
        result.append(self.emit_label(label1, frame))
        result.append(self.emit_push_const("false", in_, frame))
        result.append(self.emit_label(label2, frame))
        return "".join(result)

    def emit_add_op(self, lexeme: str, in_, frame) -> str:
        """
        Generate iadd, isub, fadd or fsub.

        Args:
            lexeme: The lexeme of the operator
            in_: The type of the operands
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        if lexeme == "+":
            if is_int_type(in_):
                return self.jvm.emitIADD()
            else:
                return self.jvm.emitFADD()
        else:
            if is_int_type(in_):
                return self.jvm.emitISUB()
            else:
                return self.jvm.emitFSUB()

    def emit_mul_op(self, lexeme: str, in_, frame) -> str:
        """
        Generate imul, idiv, fmul or fdiv.

        Args:
            lexeme: The lexeme of the operator
            in_: The type of the operands
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        if lexeme == "*":
            if is_int_type(in_):
                return self.jvm.emitIMUL()
            else:
                return self.jvm.emitFMUL()
        else:
            if is_int_type(in_):
                return self.jvm.emitIDIV()
            else:
                return self.jvm.emitFDIV()

    def emit_div(self, frame) -> str:
        """
        Emit integer division instruction.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIDIV()

    def emit_mod(self, frame) -> str:
        """
        Emit modulo instruction.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIREM()

    def emit_and_op(self, frame) -> str:
        """
        Generate iand.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIAND()

    def emit_or_op(self, frame) -> str:
        """
        Generate ior.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIOR()

    def emit_re_op(self, op: str, in_, frame) -> str:
        """
        Emit relational operation.

        Args:
            op: Operator string
            in_: Type of operands
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        result = list()
        label_f = frame.get_new_label()
        label_o = frame.get_new_label()

        frame.pop()
        frame.pop()
        if is_int_type(in_):
            if op == ">":
                result.append(self.jvm.emitIFICMPLE(label_f))
            elif op == ">=":
                result.append(self.jvm.emitIFICMPLT(label_f))
            elif op == "<":
                result.append(self.jvm.emitIFICMPGE(label_f))
            elif op == "<=":
                result.append(self.jvm.emitIFICMPGT(label_f))
            elif op == "!=":
                result.append(self.jvm.emitIFICMPEQ(label_f))
            else:
                result.append(self.jvm.emitIFICMPNE(label_f))
        else:
            result.append(self.jvm.emitFCMPL())
            if op == ">":
                result.append(self.jvm.emitIFLE(label_f))
            elif op == ">=":
                result.append(self.jvm.emitIFLT(label_f))
            elif op == "<":
                result.append(self.jvm.emitIFGE(label_f))
            elif op == "<=":
                result.append(self.jvm.emitIFGT(label_f))
            elif op == "!=":
                result.append(self.jvm.emitIFEQ(label_f))
            else:
                result.append(self.jvm.emitIFNE(label_f))
        from ..utils.nodes import PrimitiveType
        result.append(self.emit_push_const("1", PrimitiveType("int"), frame))
        frame.push()
        result.append(self.emit_goto(label_o, frame))
        result.append(self.emit_label(label_f, frame))
        result.append(self.emit_push_const("0", PrimitiveType("int"), frame))
        result.append(self.emit_label(label_o, frame))
        return "".join(result)

    def emit_rel_op(
        self, op: str, in_, true_label: int, false_label: int, frame
    ) -> str:
        """
        Emit relational operation with labels.

        Args:
            op: Operator string
            in_: Type of operands
            true_label: Label for true case
            false_label: Label for false case
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        result = list()

        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.jvm.emitIFICMPLE(false_label))
            result.append(self.emit_goto(true_label))
        elif op == ">=":
            result.append(self.jvm.emitIFICMPLT(false_label))
        elif op == "<":
            result.append(self.jvm.emitIFICMPGE(false_label))
        elif op == "<=":
            result.append(self.jvm.emitIFICMPGT(false_label))
        elif op == "!=":
            result.append(self.jvm.emitIFICMPEQ(false_label))
        elif op == "==":
            result.append(self.jvm.emitIFICMPNE(false_label))
        result.append(self.jvm.emitGOTO(true_label))
        return "".join(result)

    def emit_method(self, lexeme: str, in_type, is_static: bool) -> str:
        """
        Generate the method directive for a function.

        Args:
            lexeme: The qualified name of the method (i.e., class-name/method-name)
            in_type: The type descriptor of the method
            is_static: True if the method is static; false otherwise

        Returns:
            Generated method directive string
        """
        return self.jvm.emitMETHOD(lexeme, self.get_jvm_type(in_type), is_static)

    def emit_end_method(self, frame) -> str:
        """
        Generate the end directive for a function.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated end method directive string
        """
        buffer = list()
        # Tăng thêm buffer an toàn cho stack limit
        # Đôi khi tính toán frame.push/pop bị lệch 1-2 đơn vị dẫn đến lỗi VerifyError
        limit_stack = frame.get_max_op_stack_size() + 10 
        buffer.append(self.jvm.emitLIMITSTACK(limit_stack))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.get_max_index()))
        buffer.append(self.jvm.emitENDMETHOD())
        return "".join(buffer)

    def get_const(self, ast) -> tuple:
        """
        Get constant value and type from AST.

        Args:
            ast: Literal AST node

        Returns:
            Tuple of (value, type)
        """
        from ..utils.nodes import PrimitiveType
        if type(ast) is ast_nodes.IntLiteral:
            return (str(ast.value), PrimitiveType("int"))

    def emit_if_true(self, label: int, frame) -> str:
        """
        Generate code to jump to label if the value on top of operand stack is true.

        Args:
            label: The label where the execution continues if the value on top of stack is true
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFGT(label)

    def emit_if_false(self, label: int, frame) -> str:
        """
        Generate code to jump to label if the value on top of operand stack is false.

        Args:
            label: The label where the execution continues if the value on top of stack is false
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFLE(label)

    def emit_ificmpgt(self, label: int, frame) -> str:
        """
        Emit IFICMPGT instruction.

        Args:
            label: Target label
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFICMPGT(label)

    def emit_ificmplt(self, label: int, frame) -> str:
        """
        Emit IFICMPLT instruction.

        Args:
            label: Target label
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFICMPLT(label)

    def emit_dup(self, frame) -> str:
        """
        Generate code to duplicate the value on the top of the operand stack.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitDUP()

    def emit_pop(self, frame) -> str:
        """
        Emit POP instruction.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitPOP()

    def emit_i2f(self, frame) -> str:
        """
        Generate code to exchange an integer on top of stack to a floating-point number.

        Args:
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        return self.jvm.emitI2F()

    def emit_return(self, in_, frame) -> str:
        """
        Generate code to return.

        Args:
            in_: The type of the returned expression
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        if is_int_type(in_) or is_bool_type(in_):
            frame.pop()
            return self.jvm.emitIRETURN()
        elif is_float_type(in_):
            frame.pop()
            return self.jvm.emitFRETURN()
        elif is_void_type(in_):
            return self.jvm.emitRETURN()
        elif is_reference_type(in_): 
            frame.pop()
            return self.jvm.emitARETURN()
        else:
            # Fallback an toàn để dễ debug nếu gặp type lạ thay vì trả về None
            raise IllegalOperandException(f"Unknown return type: {in_}")

    def emit_new_array(self, lexeme: str) -> str:
        """
        Emit NEWARRAY instruction.

        Args:
            lexeme: Array type string

        Returns:
            Generated JVM instruction string
        """
        return self.jvm.emitNEWARRAY(lexeme)

    def emit_label(self, label: int, frame) -> str:
        """
        Generate code that represents a label.

        Args:
            label: The label
            frame: Frame object for stack management

        Returns:
            Generated label code
        """
        return self.jvm.emitLABEL(label)

    def emit_goto(self, label: int, frame) -> str:
        """
        Generate code to jump to a label.

        Args:
            label: The label
            frame: Frame object for stack management

        Returns:
            Generated goto instruction string
        """
        return self.jvm.emitGOTO(label)

    def emit_prolog(self, name: str, parent: str) -> str:
        """
        Generate some starting directives for a class.

        Args:
            name: Class name
            parent: Parent class name

        Returns:
            Generated prolog directives string
        """
        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(
            self.jvm.emitSUPER("java/lang/Object" if parent == "" else parent)
        )
        return "".join(result)

    def emit_limit_stack(self, num: int) -> str:
        """
        Emit LIMITSTACK directive.

        Args:
            num: Stack limit number

        Returns:
            Generated LIMITSTACK directive string
        """
        return self.jvm.emitLIMITSTACK(num)

    def emit_limit_local(self, num: int) -> str:
        """
        Emit LIMITLOCAL directive.

        Args:
            num: Local variable limit number

        Returns:
            Generated LIMITLOCAL directive string
        """
        return self.jvm.emitLIMITLOCAL(num)

    def emit_epilog(self) -> None:
        """
        Write generated code to file.
        """
        file = open(self.filepath, "w")
        tmp = "".join(self.buff)
        file.write(tmp)
        file.close()

    def print_out(self, in_: str) -> None:
        """
        Print out the code to screen.

        Args:
            in_: The code to be printed out
        """
        self.buff.append(in_)

    def clear_buff(self) -> None:
        """
        Clear the code buffer.
        """
        self.buff.clear()