"""
Code Generator for OPLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from .emitter import Emitter, is_void_type, is_int_type, is_string_type, is_bool_type, is_float_type, is_reference_type
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
# from .utils import Access, Symbol, SubBody, FunctionType, Index
# from .utils import ClassType as UtilsClassType
from .utils import *
from ..utils.nodes import *

from functools import *


class CodeGenerator(ASTVisitor):
    """
    Code generator for OPLang.
    Traverses AST and generates JVM bytecode.
    """
    
    def __init__(self):
        self.current_class = None
        self.emit = None  # Will be initialized per class
        self.instance_init_buffer = [] # List[Tuple(name, type, expr)]
        self.static_init_buffer = []   # List[Tuple(name, type, expr)]
    # ============================================================================
    # Program and Class Declarations
    # ============================================================================

    def visit_program(self, node: "Program", o: Any = None):
        """
        Visit program node - generate code for all classes.
        """
        # Process all class declarations
        self.class_table = {c.name: c for c in node.class_decls}
        for class_decl in node.class_decls:
            self.visit(class_decl, o)

    def visit_class_decl(self, node: "ClassDecl", o: Any = None):
        """
        Visit class declaration - generate class structure.
        """
        self.current_class = node.name
        class_file = node.name + ".j"
        self.emit = Emitter(class_file)
        
        self.superclass = node.superclass if node.superclass else "java/lang/Object"
        
        # Reset buffers
        self.instance_init_buffer = []
        self.static_init_buffer = []
        
        self.emit.print_out(self.emit.emit_prolog(node.name, self.superclass))
        
        # Tách các loại member
        attributes = [m for m in node.members if isinstance(m, AttributeDecl)]
        methods = [m for m in node.members if isinstance(m, MethodDecl)]
        constructors = [m for m in node.members if isinstance(m, ConstructorDecl)]
        destructors = [m for m in node.members if isinstance(m, DestructorDecl)]
        
        # 1. Visit Attributes
        for attr in attributes:
            self.visit(attr, o)
            
        # 2. Generate <clinit>
        self.generate_clinit(o)
        
        # 3. Visit Constructors
        if constructors:
            for constructor in constructors:
                self.visit(constructor, o)
        else:

            has_instance_attrs = any(not attr.is_static for attr in attributes)
            if has_instance_attrs or not constructors: 
                 self.generate_default_constructor(o)
        
        # 4. Visit Methods
        for method in methods:
            self.visit(method, o)
            
        if destructors:
            for destructor in destructors:
                self.visit(destructor, o)
        else:
            self.generate_default_destructor(o)
            
        self.emit.emit_epilog()
    def generate_default_destructor(self, o: Any): 
        method_name = "destructor"
        void_type = PrimitiveType("void")
        frame = Frame(method_name, void_type)
        
        # Emit method header
        func_type = FunctionType([], void_type)
        self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        frame.enter_scope(True)
        # Setup 'this'
        this_idx = frame.get_new_index()
        self.emit.print_out(self.emit.emit_var(this_idx, "this", ClassType(self.current_class), frame.get_start_label(), frame.get_end_label()))
        
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
        
        if self.superclass and self.superclass != "java/lang/Object":
             self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
             self.emit.print_out(self.emit.emit_invoke_special(frame, f"{self.superclass}/destructor", func_type))

        # Return
        self.emit.print_out(self.emit.emit_return(void_type, frame))
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()
    def has_user_defined_constructor(self, class_node):
        """Check if class has user-defined constructor"""
        for member in class_node.members:
            if type(member).__name__ == 'ConstructorDecl':
                return True
        return False
    def generate_default_constructor(self, o: Any):
        """
        Sinh mã cho constructor mặc định để khởi tạo instance fields.
        """
        # method_name = "<init>"
        # void_type = PrimitiveType("void")
        # func_type = FunctionType([], void_type)
        # frame = Frame(method_name, void_type)
        
        # self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        # frame.enter_scope(True)
        # from_label = frame.get_start_label()
        # to_label = frame.get_end_label()
        
        # this_idx = frame.get_new_index()
        # self.emit.print_out(
        #     self.emit.emit_var(
        #         this_idx,
        #         "this",
        #         ClassType(self.current_class),
        #         from_label,
        #         to_label
        #     )
        # )
        
        # self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
        
        # super_init_name = f"{self.superclass}/<init>"
        # super_init_type = FunctionType([], PrimitiveType("void"))
        # self.emit.print_out(self.emit.emit_invoke_special(frame, super_init_name, super_init_type))
        
        # sym_list = [Symbol("this", ClassType(self.current_class), Index(this_idx))] + IO_SYMBOL_LIST
        
        # for name, typ, expr in self.instance_init_buffer:
        #     self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
        #     code, _ = self.visit(expr, Access(frame, sym_list, False, True))
        #     self.emit.print_out(code)
        #     field_name = f"{self.current_class}/{name}"
        #     self.emit.print_out(self.emit.emit_put_field(field_name, typ, frame))
        
        # self.emit.print_out(self.emit.emit_return(void_type, frame))
        # self.emit.print_out(self.emit.emit_label(to_label, frame))
        # self.emit.print_out(self.emit.emit_end_method(frame))
        # frame.exit_scope()
        method_name = "<init>"
        void_type = PrimitiveType("void")
        func_type = FunctionType([], void_type)
        frame = Frame(method_name, void_type)
        
        self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        this_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                this_idx,
                "this",
                ClassType(self.current_class),
                from_label,
                to_label
            )
        )
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # ✅ Load 'this' cho super constructor
        self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
        
        super_init_name = f"{self.superclass}/<init>"
        super_init_type = FunctionType([], PrimitiveType("void"))
        self.emit.print_out(self.emit.emit_invoke_special(frame, super_init_name, super_init_type))
        
        # ✅ Khởi tạo instance fields
        sym_list = [Symbol("this", ClassType(self.current_class), Index(this_idx))] + IO_SYMBOL_LIST
        
        for name, typ, expr in self.instance_init_buffer:
            # Load 'this'
            self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
            
            # Tính giá trị init
            code, _ = self.visit(expr, Access(frame, sym_list, False, True))
            self.emit.print_out(code)
            
            # Store vào field
            field_name = f"{self.current_class}/{name}"
            self.emit.print_out(self.emit.emit_put_field(field_name, typ, frame))
        
        self.emit.print_out(self.emit.emit_return(void_type, frame))
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()
    def generate_clinit(self, o: Any): # sinh ma cho <clinit>
        """
        Sinh mã cho phương thức static <clinit> để khởi tạo static fields.
        """
        method_name = "<clinit>"
        void_type = PrimitiveType("void")
        func_type = FunctionType([], void_type)
        frame = Frame(method_name, void_type)
        
        self.emit.print_out(self.emit.emit_method(method_name, func_type, True))
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        if self.static_init_buffer:
            sym_list = IO_SYMBOL_LIST
            for name, typ, expr in self.static_init_buffer:
                code, _ = self.visit(expr, Access(frame, sym_list, False, True)) 
                self.emit.print_out(code)
                field_name = f"{self.current_class}/{name}"
                self.emit.print_out(self.emit.emit_put_static(field_name, typ, frame))
            
        self.emit.print_out(self.emit.emit_return(void_type, frame))
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()
    # ============================================================================
    # Attribute Declarations
    # ============================================================================

    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None):
        """
        Visit attribute declaration - generate field directives.
        TODO: Implement attribute initialization if needed
        """
        for attr in node.attributes:
            self.visit(attr, node)

    def visit_attribute(self, node: "Attribute", o: Any = None):
        """
        Visit individual attribute - generate field directive.
        """
        attr_decl = o  # AttributeDecl node
        field_name = node.name
        
        if attr_decl.attr_type is None:
            raise IllegalOperandException(f"Attribute '{field_name}' has no type")
        
        # [NOTE] Emitter giờ đã có thể xử lý attr_decl.attr_type dù nó là nodes.ClassType
        if attr_decl.is_static:
            self.emit.print_out(
                self.emit.emit_attribute(
                    field_name,
                    attr_decl.attr_type,
                    attr_decl.is_final
                )
            )
            if node.init_value is not None:
                self.static_init_buffer.append((node.name, attr_decl.attr_type, node.init_value))
        else:
            jvm_type = self.emit.get_jvm_type(attr_decl.attr_type) # Safe now
            
            self.emit.print_out(
                self.emit.jvm.emitINSTANCEFIELD(field_name, jvm_type)
            )
            if node.init_value is not None:
                self.instance_init_buffer.append((node.name, attr_decl.attr_type, node.init_value))
    # ============================================================================
    # Method Declarations
    # ============================================================================
    def emit_box_primitive(self, frame, type_node):
        """
        Sinh mã tạo mảng 1 phần tử để chứa primitive.
        Stack change: ... -> ..., size (1) -> ..., array_ref
        """
        code = ""
        
        # [FIX] Bước 1: Push kích thước mảng (1) lên stack
        # Điều này giúp Frame cập nhật stack size (+1) và JVM có tham số cho newarray
        code += self.emit.emit_push_iconst(1, frame)

        # Bước 2: Sinh lệnh newarray
        # Lưu ý: emit_new_array trong emitter.py không thay đổi stack frame,
        # nhưng vì ta đã push 1 (size) ở trên, và newarray thực tế pop 1 (size) push 1 (ref),
        # nên trạng thái stack size hiện tại (+1) là đúng (đang chứa Array Ref).
        if is_int_type(type_node):
            code += self.emit.emit_new_array("int")
        elif is_float_type(type_node):
            code += self.emit.emit_new_array("float")
        elif is_bool_type(type_node):
            code += self.emit.emit_new_array("boolean")
        elif is_string_type(type_node):
            code += self.emit.jvm.emitANEWARRAY("java/lang/String")
        else:
             # ClassType/ArrayType bản chất đã là Reference, không cần box thêm
             # Nếu không box, ta phải pop số 1 vừa push thừa đi để tránh rác stack
             # Tuy nhiên logic gọi hàm này thường đã check type trước rồi.
             return "" 
             
        return code
    def visit_method_decl(self, node: "MethodDecl", o: Any = None):
        """
        Visit method declaration - generate method code.
        """
        # frame = Frame(node.name, node.return_type)
        # self.generate_method(node, frame, node.is_static)
        """
        Visit method declaration - generate method code.
        Updated to support Reference Types by boxing primitive parameters.
        """
        frame = Frame(node.name, node.return_type)
        class_name = self.current_class
        method_name = node.name
        
        param_types = [p.param_type for p in node.params]
        return_type = node.return_type
        
        # 1. Xử lý hàm Main
        is_main = (method_name == "main" and len(param_types) == 0 and is_void_type(return_type) and node.is_static)
        
        if is_main:
            args_type = ArrayType(PrimitiveType("string"), 0)
            func_type = FunctionType([args_type], return_type)
        else:
            func_type = FunctionType(param_types, return_type)

        # 2. Emit method header
        self.emit.print_out(
            self.emit.emit_method(
                method_name,
                func_type,
                node.is_static
            )
        )
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        sym_list = []

        # 3. Setup 'this' (nếu không phải static)
        if not node.is_static:
            this_idx = frame.get_new_index() # idx 0
            self.emit.print_out(
                self.emit.emit_var(
                    this_idx,
                    "this",
                    ClassType(class_name),
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol("this", ClassType(class_name), Index(this_idx)))
        elif is_main:
            args_idx = frame.get_new_index() 
            args_type = ArrayType(PrimitiveType("string"), 0)
            self.emit.print_out(self.emit.emit_var(args_idx, "args", args_type, from_label, to_label))

        # 4. Declare Parameters (Khai báo tham số ban đầu)
        # Lưu ý: Lúc này kiểu dữ liệu vẫn là kiểu gốc (VD: int là I)
        for i, param in enumerate(node.params):
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    param.name,
                    param.param_type,
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # 5. [QUAN TRỌNG] BOXING PARAMETERS
        # Duyệt qua các symbol vừa tạo, nếu là Primitive (int, float...) -> Tạo Wrapper Array
        for sym in sym_list:
            # Bỏ qua 'this' và các loại đã là Reference (Class, Array, ReferenceType)
            # Lưu ý: String trong OPLang cũng cần box nếu muốn hỗ trợ string &
            if sym.name == "this" or isinstance(sym.type, (ReferenceType, ArrayType, ClassType)):
                continue

            # Kiểm tra xem có phải primitive cần box không
            original_type = sym.type
            if is_int_type(original_type) or is_float_type(original_type) or is_bool_type(original_type) or is_string_type(original_type):
                
                # A. Lấy giá trị từ biến tham số gốc (đang nằm ở slot cũ)
                old_idx = sym.value.value
                load_code = self.emit.emit_read_var(sym.name, original_type, old_idx, frame)
                
                # B. Tạo Wrapper mới (Mảng 1 phần tử)
                # Hàm emit_box_primitive cần được thêm vào class CodeGenerator (như hướng dẫn trước)
                self.emit.print_out(self.emit_box_primitive(frame, original_type)) # Stack: [ArrRef]
                
                # C. Setup stack để gán giá trị vào mảng: [ArrRef, ArrRef, 0, Value]
                self.emit.print_out(self.emit.emit_dup(frame))       # Stack: [ArrRef, ArrRef]
                self.emit.print_out(self.emit.emit_push_iconst(0, frame)) # Stack: [ArrRef, ArrRef, 0]
                self.emit.print_out(load_code)                       # Stack: [ArrRef, ArrRef, 0, Value]
                
                # D. Store giá trị vào mảng
                self.emit.print_out(self.emit.emit_astore(original_type, frame)) # Stack: [ArrRef]
                
                # E. Cấp phát biến cục bộ MỚI để chứa Wrapper này
                new_idx = frame.get_new_index()
                
                # F. Tạo kiểu ReferenceType để cập nhật vào SymbolTable
                # Hack: Dùng ReferenceType để báo hiệu cho các hàm visit khác biết biến này đã được box
                wrapper_type = ReferenceType(original_type)
                
                # G. Lưu ArrRef vào biến cục bộ mới
                self.emit.print_out(self.emit.emit_write_var(sym.name, wrapper_type, new_idx, frame))
                
                # H. Cập nhật Symbol Table để các lệnh sau dùng biến mới
                sym.type = wrapper_type
                sym.value.value = new_idx

        # 6. Add IO symbols and generate body
        full_sym_list = IO_SYMBOL_LIST + sym_list
        o_body = SubBody(frame, full_sym_list)
        
        self.visit(node.body, o_body)
        
        # 7. Emit return if void
        if is_void_type(return_type):
            self.emit.print_out(self.emit.emit_return(return_type, frame))
        
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()

    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
        """
        Visit constructor declaration - generate constructor code.
        """
        frame = Frame("<init>", PrimitiveType("void"))
        self.generate_constructor(node, frame)

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None):
        """
        Visit destructor declaration - generate destructor code.
        """
        # method_name = f"~{self.current_class}" # Hoặc mapping thành "finalize" tùy yêu cầu
        # void_type = PrimitiveType("void")
        # frame = Frame(method_name, void_type)
        
        # # Emit method
        # func_type = FunctionType([], void_type)
        # self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        # frame.enter_scope(True)
        # # Setup 'this' variable
        # this_idx = frame.get_new_index()
        # self.emit.print_out(self.emit.emit_var(this_idx, "this", ClassType(self.current_class), frame.get_start_label(), frame.get_end_label()))
        
        # self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
        
        # # Body
        # sym_list = [Symbol("this", ClassType(self.current_class), Index(this_idx))] + IO_SYMBOL_LIST
        # self.visit(node.body, SubBody(frame, sym_list))
        
        # self.emit.print_out(self.emit.emit_return(void_type, frame))
        # self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        # self.emit.print_out(self.emit.emit_end_method(frame))
        # frame.exit_scope()
        # [FIX] Đổi tên method từ ~ClassName thành "destructor" để hợp lệ với JVM
        method_name = "destructor" 
        void_type = PrimitiveType("void")
        frame = Frame(method_name, void_type)
        
        # Emit method
        func_type = FunctionType([], void_type)
        self.emit.print_out(self.emit.emit_method(method_name, func_type, False))
        
        frame.enter_scope(True)
        # Setup 'this' variable
        this_idx = frame.get_new_index()
        self.emit.print_out(self.emit.emit_var(this_idx, "this", ClassType(self.current_class), frame.get_start_label(), frame.get_end_label()))
        
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
        
        # [FIX] Tự động gọi destructor của lớp cha (nếu có) TRƯỚC khi chạy body
        if self.superclass and self.superclass != "java/lang/Object":
             self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.current_class), this_idx, frame))
             self.emit.print_out(self.emit.emit_invoke_special(frame, f"{self.superclass}/destructor", func_type))

        # Body
        sym_list = [Symbol("this", ClassType(self.current_class), Index(this_idx))] + IO_SYMBOL_LIST
        self.visit(node.body, SubBody(frame, sym_list))
        
        self.emit.print_out(self.emit.emit_return(void_type, frame))
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()
    def generate_constructor(self, node: "ConstructorDecl", frame: Frame):
        """
        Generate code for a constructor.
        
        Args:
            node: Constructor declaration node
            frame: Frame for this constructor
        """
        class_name = self.current_class
        meclass_name = self.current_class
        method_name = "<init>"
        
        # Build constructor signature
        param_types = [p.param_type for p in node.params]
        return_type = PrimitiveType("void")
        
        func_type = FunctionType(param_types, return_type)
        
        self.emit.print_out(
            self.emit.emit_method(
                method_name,
                func_type,
                False
            )
        )
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        # 'this' parameter
        this_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                this_idx,
                "this",
                ClassType(class_name),
                from_label,
                to_label
            )
        )
        
        sym_list = [Symbol("this", ClassType(class_name), Index(this_idx))]
        
        # Parameters - Lưu lại index để load sau này
        param_indices = []
        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    param.name,
                    param.param_type,
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))
            param_indices.append(idx)
        
        sym_list = IO_SYMBOL_LIST + sym_list
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # --- [FIX] LOGIC GỌI SUPER CONSTRUCTOR ---
        # 1. Load 'this'
        self.emit.print_out(self.emit.emit_read_var("this", ClassType(class_name), this_idx, frame))
        
        # 2. Tìm constructor phù hợp của lớp cha
        matched_super_ctor = None
        
        if self.superclass == "java/lang/Object":
            # Nếu cha là Object, chỉ có constructor mặc định
            matched_super_ctor = None
        else:
            try:
                # Cố gắng tìm constructor cha có cùng kiểu tham số
                matched_super_ctor = self.resolve_constructor(self.superclass, param_types)
            except IllegalOperandException:
                # Không tìm thấy khớp chính xác -> sẽ dùng default
                matched_super_ctor = None

        if matched_super_ctor:
            # Nếu tìm thấy constructor khớp signature: Load tham số và gọi nó
            for i, p_idx in enumerate(param_indices):
                param_name = node.params[i].name
                param_type = node.params[i].param_type
                self.emit.print_out(self.emit.emit_read_var(param_name, param_type, p_idx, frame))
            
            self.emit.print_out(self.emit.emit_invoke_special(frame, f"{self.superclass}/<init>", matched_super_ctor))
        else:
            # Nếu không tìm thấy hoặc cha là Object -> Gọi constructor mặc định (không tham số)
            default_ctor_type = FunctionType([], PrimitiveType("void"))
            self.emit.print_out(self.emit.emit_invoke_special(frame, f"{self.superclass}/<init>", default_ctor_type))
        
        # --- END FIX ---

        # 3. Initialize instance fields
        for field_name, field_type, init_expr in self.instance_init_buffer:
            self.emit.print_out(self.emit.emit_read_var("this", ClassType(class_name), this_idx, frame))
            code, _ = self.visit(init_expr, Access(frame, sym_list, False, True))
            self.emit.print_out(code)
            full_field_name = f"{class_name}/{field_name}"
            self.emit.print_out(self.emit.emit_put_field(full_field_name, field_type, frame))
        
        # 4. Generate code for constructor body
        o = SubBody(frame, sym_list)
        self.visit(node.body, o)
        
        self.emit.print_out(self.emit.emit_return(return_type, frame))
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()
    def visit_parameter(self, node: "Parameter", o: Any = None):
        """
        Visit parameter - register parameter in frame.
        """
        # This is handled in generate_method
        pass

    def generate_method(self, node: "MethodDecl", frame: Frame, is_static: bool):
        """
        Generate code for a method.
        
        Args:
            node: Method declaration node
            frame: Frame for this method
            is_static: Whether method is static
        """
        class_name = self.current_class
        method_name = node.name
        
        param_types = [p.param_type for p in node.params]
        return_type = node.return_type
        
        # --- FIX START: Xử lý hàm main ---
        is_main = (method_name == "main" and len(param_types) == 0 and is_void_type(return_type) and is_static)
        
        if is_main:
            
            args_type = ArrayType(PrimitiveType("string"), 0)
            func_type = FunctionType([args_type], return_type)
        else:
            func_type = FunctionType(param_types, return_type)
        # --- FIX END ---

        # Emit method directive
        self.emit.print_out(
            self.emit.emit_method(
                method_name,
                func_type,
                is_static
            )
        )
        
        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        sym_list = []

        if not is_static:
            this_idx = frame.get_new_index() # idx 0
            self.emit.print_out(
                self.emit.emit_var(
                    this_idx,
                    "this",
                    ClassType(class_name),
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol("this", ClassType(class_name), Index(this_idx)))
        elif is_main:
            args_idx = frame.get_new_index() 
            args_type = ArrayType(PrimitiveType("string"), 0)
            self.emit.print_out(self.emit.emit_var(args_idx, "args", args_type, from_label, to_label))

        # 2. Generate code for parameters
        for i, param in enumerate(node.params):
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    param.name,
                    param.param_type,
                    from_label,
                    to_label
                )
            )
            sym_list.append(Symbol(param.name, param.param_type, Index(idx)))
        
        # Add IO symbols
        sym_list = IO_SYMBOL_LIST + sym_list
        
        self.emit.print_out(self.emit.emit_label(from_label, frame))
        
        # Generate code for method body
        o = SubBody(frame, sym_list)
        self.visit(node.body, o)
        
        # Emit return if void
        if is_void_type(return_type):
            self.emit.print_out(self.emit.emit_return(return_type, frame))
        
        self.emit.print_out(self.emit.emit_label(to_label, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()
    
    # ============================================================================
    # Type System
    # ============================================================================

    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    def visit_class_type(self, node: "ClassType", o: Any = None):
        pass

    def visit_reference_type(self, node: "ReferenceType", o: Any = None):
        pass

    # ============================================================================
    # Statements
    # ============================================================================

    def visit_block_statement(self, node: "BlockStatement", o: SubBody = None):
        """
        Visit block statement - process variable declarations and statements.
        """
        if o is None: return
        
        for var_decl in node.var_decls:
            o = self.visit(var_decl, o)
        
        for stmt in node.statements:
            self.visit(stmt, o)

        # [FIX] Dùng ClassType (của nodes) để kiểm tra node trong AST
        for var_decl in node.var_decls:
            if isinstance(var_decl.var_type, ClassType):
                for var in var_decl.variables:
                    sym = next(filter(lambda x: x.name == var.name, o.sym), None)
                    if sym:
                        self.emit.print_out(self.emit.emit_read_var(var.name, var_decl.var_type, sym.value.value, o.frame))
                        # UtilsClassType hay ClassType đều được nếu Emitter đã fix, 
                        # nhưng dùng đúng loại node đang có là tốt nhất.
                        self.emit.print_out(self.emit.emit_invoke_virtual(f"{var_decl.var_type.class_name}/destructor", FunctionType([], PrimitiveType("void")), o.frame))
    def visit_variable_decl(self, node: "VariableDecl", o: SubBody = None):
        """
        Visit variable declaration - register local variables.
        """
        # if o is None:
        #     return o
        
        # frame = o.frame
        # from_label = frame.get_start_label()
        # to_label = frame.get_end_label()
        
        # new_sym = []
        # for var in node.variables:
        #     idx = frame.get_new_index()
            
        #     self.emit.print_out(
        #         self.emit.emit_var(
        #             idx,
        #             var.name,
        #             node.var_type,
        #             from_label,
        #             to_label
        #         )
        #     )
            
        #     new_sym.append(Symbol(var.name, node.var_type, Index(idx)))
            
        #     if var.init_value is not None:
        #         code, typ = self.visit(var.init_value, Access(frame, o.sym))
        #         self.emit.print_out(code)
        #         self.emit.print_out(
        #             self.emit.emit_write_var(var.name, node.var_type, idx, frame)
        #         )
        
        # return SubBody(frame, new_sym + o.sym)
        if o is None: return o
        
        frame = o.frame
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()
        
        new_sym = []
        
        for var in node.variables:
            idx = frame.get_new_index()
            actual_type = node.var_type
            stored_type = actual_type 
            
            # --- CASE 1: Reference Declaration (int & ref = x) ---
            if isinstance(node.var_type, ReferenceType):
                self.emit.print_out(self.emit.emit_var(idx, var.name, stored_type, from_label, to_label))
                if var.init_value:
                    #  val_code, val_type = self.visit(var.init_value, Access(frame, o.sym, False, False, True)) 
                    access_obj = Access(frame, o.sym, False, False)
                    access_obj.is_ref_needed = True
                    val_code, val_type = self.visit(var.init_value, access_obj)
                    self.emit.print_out(val_code)
                    self.emit.print_out(self.emit.emit_write_var(var.name, stored_type, idx, frame))
            
            # --- CASE 2: Primitive Declaration (int a = 1) -> Box thành Array ---
            elif is_int_type(actual_type) or is_float_type(actual_type) or is_bool_type(actual_type) or is_string_type(actual_type):
                stored_type = ReferenceType(actual_type)
                # Emit var directive cho biến wrapper
                self.emit.print_out(self.emit.emit_var(idx, var.name, stored_type, from_label, to_label))
                
                # 1. Tạo mảng [1]
                self.emit.print_out(self.emit_box_primitive(frame, actual_type))
                self.emit.print_out(self.emit.emit_dup(frame)) 
                
                # 2. Init value
                if var.init_value:
                    self.emit.print_out(self.emit.emit_push_iconst(0, frame))
                    val_code, val_type = self.visit(var.init_value, Access(frame, o.sym))
                    self.emit.print_out(val_code)
                    
                    # Coercion
                    if is_float_type(actual_type) and is_int_type(val_type):
                        self.emit.print_out(self.emit.emit_i2f(frame))
                        
                    self.emit.print_out(self.emit.emit_astore(actual_type, frame))
                else:
                    self.emit.print_out(self.emit.emit_pop(frame)) # Pop dup nếu ko init

                # 3. Store wrapper vào biến local
                self.emit.print_out(self.emit.emit_write_var(var.name, stored_type, idx, frame))

            # --- CASE 3 [NEW]: Object/Array Declaration (A a = new A()) ---
            else:
                # Đây là phần bạn bị thiếu!
                self.emit.print_out(self.emit.emit_var(idx, var.name, stored_type, from_label, to_label))
                
                if var.init_value:
                    val_code, val_type = self.visit(var.init_value, Access(frame, o.sym))
                    self.emit.print_out(val_code)
                    self.emit.print_out(self.emit.emit_write_var(var.name, stored_type, idx, frame))
                else:
                    self.emit.print_out(self.emit.jvm.emitPUSHNULL())
                    o.frame.push()  # Cập nhật frame stack
                    self.emit.print_out(self.emit.emit_write_var(var.name, stored_type, idx, frame))

            new_sym.append(Symbol(var.name, stored_type, Index(idx)))

        return SubBody(frame, new_sym + o.sym)

    def visit_variable(self, node: "Variable", o: Any = None):
        pass

    def visit_assignment_statement(self, node: "AssignmentStatement", o: SubBody = None):
        """
        Visit assignment statement - generate assignment code.
        """
      
        # rhs_code, rhs_type = self.visit(node.rhs, Access(o.frame, o.sym, False))
  
        # lhs_code, lhs_type = self.visit(node.lhs, Access(o.frame, o.sym, True))
        
        # if rhs_code is None: rhs_code = ""
        # if lhs_code is None: lhs_code = ""
        
        # self.emit.print_out(rhs_code)
        # lhs_code, lhs_type = self.visit(node.lhs, Access(o.frame, o.sym, True))
        
        # # RHS visit
        # rhs_code, rhs_type = self.visit(node.rhs, Access(o.frame, o.sym, False))

        # self.emit.print_out(lhs_code) # Stack: [ArrRef, 0]
        # self.emit.print_out(rhs_code) # Stack: [ArrRef, 0, Val]
        # if is_float_type(lhs_type) and is_int_type(rhs_type):
        #     self.emit.print_out(self.emit.emit_i2f(o.frame))
            
        # self.emit.print_out(lhs_code)
        if o is None:
            return
        
        # 1. Visit RHS trước để có giá trị trên stack
        rhs_code, rhs_type = self.visit(node.rhs, Access(o.frame, o.sym, False))
        
        # 2. Visit LHS để có địa chỉ/index
        lhs_code, lhs_type = self.visit(node.lhs, Access(o.frame, o.sym, True))
        
        # 3. Emit code theo thứ tự
        self.emit.print_out(rhs_code)  # Stack: [value]
        
        # Coercion nếu cần
        if is_float_type(lhs_type) and is_int_type(rhs_type):
            self.emit.print_out(self.emit.emit_i2f(o.frame))
        
        self.emit.print_out(lhs_code)
    def visit_if_statement(self, node: "IfStatement", o: Any = None):
        """
        Visit if statement.
        TODO: Implement if statement code generation
        """
        if o is None:
            return

        # 1. Tạo các nhãn
        else_label = o.frame.get_new_label()
        exit_label = o.frame.get_new_label()

        # 2. Sinh mã cho biểu thức điều kiện
        # Kết quả (boolean) sẽ nằm trên đỉnh stack
        cond_code, cond_type = self.visit(node.condition, Access(o.frame, o.sym))
        self.emit.print_out(cond_code)

        # 3. Kiểm tra điều kiện: Nếu False (0) thì nhảy tới else_label
        # emit_if_false sẽ pop giá trị từ stack và kiểm tra
        self.emit.print_out(self.emit.emit_if_false(else_label, o.frame))

        # 4. Sinh mã cho phần THEN
        self.visit(node.then_stmt, o)
        
        # Sau khi thực hiện xong Then, nhảy tới cuối (Exit) để bỏ qua phần Else
        self.emit.print_out(self.emit.emit_goto(exit_label, o.frame))

        # 5. Đặt nhãn ELSE
        self.emit.print_out(self.emit.emit_label(else_label, o.frame))

        # 6. Sinh mã cho phần ELSE (nếu có)
        if node.else_stmt:
            self.visit(node.else_stmt, o)

        # 7. Đặt nhãn EXIT
        self.emit.print_out(self.emit.emit_label(exit_label, o.frame))

    def visit_for_statement(self, node: "ForStatement", o: Any = None):
        """
        Visit for statement.
        TODO: Implement for statement code generation
        """
        if o is None:
            return

        frame = o.frame
        sym = o.sym
        
        # 1. Tìm biến vô hướng (scalar variable) trong bảng ký hiệu
        loop_var_sym = next(filter(lambda x: x.name == node.variable, sym), None)
        if loop_var_sym is None:
            raise IllegalOperandException(f"Undeclared variable: {node.variable}")
        
        # ✅ FIX: Unwrap ReferenceType để check inner type
        loop_var_type = loop_var_sym.type
        if isinstance(loop_var_type, ReferenceType):
            inner_type = loop_var_type.referenced_type
        else:
            inner_type = loop_var_type
        
        # Biến chạy vòng lặp phải là kiểu int (theo spec)
        if not is_int_type(inner_type):
            raise IllegalOperandException(f"Loop variable '{node.variable}' must be integer type")

        var_index = loop_var_sym.value.value
        is_wrapper = isinstance(loop_var_type, ReferenceType)

        # 2. Khởi tạo: scalar_var := start_expr
        start_code, start_type = self.visit(node.start_expr, Access(frame, sym))
        if not is_int_type(start_type):
            raise IllegalOperandException("Start expression in for loop must be integer")
        
        self.emit.print_out(start_code)
        
        # ✅ Store vào wrapper nếu cần
        if is_wrapper:
            # Load wrapper array
            self.emit.print_out(self.emit.emit_read_var(node.variable, loop_var_type, var_index, frame))
            self.emit.print_out(self.emit.jvm.INDENT + "swap\n")  # [arrref, value]
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))  # [arrref, value, 0]
            self.emit.print_out(self.emit.jvm.INDENT + "swap\n")  # [arrref, 0, value]
            self.emit.print_out(self.emit.jvm.emitIASTORE())
            frame.pop()
            frame.pop()
            frame.pop()
        else:
            self.emit.print_out(self.emit.emit_write_var(node.variable, loop_var_type, var_index, frame))

        # 3. Vào vòng lặp
        frame.enter_loop()
        
        loop_start_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()

        self.emit.print_out(self.emit.emit_label(loop_start_label, frame))

        # 4. Kiểm tra điều kiện dừng
        # Load giá trị hiện tại của biến chạy
        if is_wrapper:
            # Load wrapper -> load value from index 0
            self.emit.print_out(self.emit.emit_read_var(node.variable, loop_var_type, var_index, frame))
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            self.emit.print_out(self.emit.emit_aload(inner_type, frame))
        else:
            self.emit.print_out(self.emit.emit_read_var(node.variable, loop_var_type, var_index, frame))
        
        # Tính giá trị biểu thức đích (end_expr)
        end_code, end_type = self.visit(node.end_expr, Access(frame, sym))
        if not is_int_type(end_type):
            raise IllegalOperandException("End expression in for loop must be integer")
        self.emit.print_out(end_code)

        # So sánh
        if node.direction == "to":
            self.emit.print_out(self.emit.emit_ificmpgt(break_label, frame))
        else:
            self.emit.print_out(self.emit.emit_ificmplt(break_label, frame))

        # 5. Thực thi thân vòng lặp
        self.visit(node.body, o)

        # 6. Cập nhật biến chạy (Continue label đặt ở đây)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        
        # Load biến chạy
        if is_wrapper:
            self.emit.print_out(self.emit.emit_read_var(node.variable, loop_var_type, var_index, frame))
            self.emit.print_out(self.emit.emit_dup(frame))  # Dup wrapper ref
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            self.emit.print_out(self.emit.emit_aload(inner_type, frame))  # Load current value
        else:
            self.emit.print_out(self.emit.emit_read_var(node.variable, loop_var_type, var_index, frame))
        
        # Push 1
        self.emit.print_out(self.emit.emit_push_iconst(1, frame))
        
        # Cộng hoặc trừ
        if node.direction == "to":
            self.emit.print_out(self.emit.emit_add_op("+", PrimitiveType("int"), frame))
        else:
            self.emit.print_out(self.emit.emit_add_op("-", PrimitiveType("int"), frame))

        # Lưu ngược lại vào biến
        if is_wrapper:
            # Stack: [arrref, new_value]
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))  # [arrref, new_value, 0]
            self.emit.print_out(self.emit.jvm.INDENT + "swap\n")  # [arrref, 0, new_value]
            self.emit.print_out(self.emit.jvm.emitIASTORE())
            frame.pop()
            frame.pop()
            frame.pop()
        else:
            self.emit.print_out(self.emit.emit_write_var(node.variable, loop_var_type, var_index, frame))

        # 7. Quay lại đầu vòng lặp
        self.emit.print_out(self.emit.emit_goto(loop_start_label, frame))

        # 8. Đặt nhãn thoát (Break label)
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.exit_loop()

    def visit_break_statement(self, node: "BreakStatement", o: Any = None):
        """
        Visit break statement.
        TODO: Implement break statement code generation
        """
        if o is None:
            return
        
        try:
            break_label = o.frame.get_break_label()
            self.emit.print_out(self.emit.emit_goto(break_label, o.frame))
        except IllegalRuntimeException:
            # Trường hợp break được gọi bên ngoài vòng lặp (thường đã được bắt ở Semantic Check)
            raise IllegalOperandException("Break statement used outside of loop")

    def visit_continue_statement(self, node: "ContinueStatement", o: Any = None):
        """
        Visit continue statement.
        TODO: Implement continue statement code generation
        """
        if o is None:
            return

        try:
            continue_label = o.frame.get_continue_label()
            self.emit.print_out(self.emit.emit_goto(continue_label, o.frame))
        except IllegalRuntimeException:
            # Trường hợp continue được gọi bên ngoài vòng lặp
            raise IllegalOperandException("Continue statement used outside of loop")

    def visit_return_statement(self, node: "ReturnStatement", o: SubBody = None):
        """
        Visit return statement - generate return code.
        """
        # if o is None:
        #     return
        
        # # Generate code for return value
        # code, typ = self.visit(node.value, Access(o.frame, o.sym))
        # self.emit.print_out(code)
        
        # # Emit return instruction
        # self.emit.print_out(self.emit.emit_return(typ, o.frame))
        
        
        
        # if o is None:
        #     return
        
        # # 1. Sinh mã cho biểu thức trả về
        # code, typ = self.visit(node.value, Access(o.frame, o.sym))
        # self.emit.print_out(code)
        
        # # 2. [FIX] Lấy kiểu trả về mong muốn từ Frame
        # return_type = o.frame.return_type
        
        # # 3. [FIX] Kiểm tra và ép kiểu Int -> Float nếu cần
        # if is_float_type(return_type) and is_int_type(typ):
        #     self.emit.print_out(self.emit.emit_i2f(o.frame))
        #     # Sau khi ép kiểu, dùng return_type (float) để sinh freturn
        #     self.emit.print_out(self.emit.emit_return(return_type, o.frame))
        # else:
        #     # Trường hợp bình thường
        #     self.emit.print_out(self.emit.emit_return(typ, o.frame))
        if o is None:
            return
        
        frame_return_type = o.frame.return_type
        is_ref_return = isinstance(frame_return_type, ReferenceType)
        
        # Tạo Access context
        new_access = Access(o.frame, o.sym, False, False)
        new_access.is_ref_needed = is_ref_return 
        
        # Sinh mã cho biểu thức trả về
        code, typ = self.visit(node.value, new_access)
        self.emit.print_out(code)
        
        # ✅ FIX: Không coerce khi return reference
        if not is_ref_return:
            if is_float_type(frame_return_type) and is_int_type(typ):
                self.emit.print_out(self.emit.emit_i2f(o.frame))
                self.emit.print_out(self.emit.emit_return(frame_return_type, o.frame))
            else:
                self.emit.print_out(self.emit.emit_return(typ, o.frame))
        else:
            # Return reference - typ phải là ReferenceType (wrapper array)
            # ✅ Đảm bảo emitter biết return ARETURN thay vì IRETURN
            self.emit.print_out(self.emit.emit_return(frame_return_type, o.frame))
    def lookup_method(self, class_name: str, method_name: str):
        """
        Tìm kiếm thông tin method trong class hoặc thư viện IO.
        Trả về: (method_type, is_static) hoặc raise Exception
        """
        # 1. Kiểm tra trong thư viện IO
        if class_name == "io":
            for sym in IO_SYMBOL_LIST:
                if sym.name == method_name:
                    # IO methods are static
                    return sym.type, True # type is FunctionType
            raise IllegalOperandException(f"Method '{method_name}' not found in io")

        # 2. Kiểm tra trong Class Table
        if class_name not in self.class_table:
            raise IllegalOperandException(f"Undeclared class: {class_name}")

        class_decl = self.class_table[class_name]
        
        # Tìm trong các member của class hiện tại
        # Lưu ý: Cần xử lý kế thừa (inheritance) nếu OPLang yêu cầu (theo spec là có extends)
        # Ở đây cài đặt tìm kiếm đệ quy lên superclass
        current_decl = class_decl
        while current_decl:
            for member in current_decl.members:
                if isinstance(member, MethodDecl) and member.name == method_name:
                    # Tạo FunctionType từ MethodDecl để dùng cho emitter
                    param_types = [p.param_type for p in member.params]
                    func_type = FunctionType(param_types, member.return_type)
                    return func_type, member.is_static
            
            # Leo lên cha
            if current_decl.superclass and current_decl.superclass != "java/lang/Object": #
                 if current_decl.superclass in self.class_table:
                     current_decl = self.class_table[current_decl.superclass]
                 else:
                     break # Superclass not found
            else:
                break
                
        raise IllegalOperandException(f"Method '{method_name}' not found in class '{class_name}'")
    def visit_method_invocation_statement(
        self, node: "MethodInvocationStatement", o: Any = None
    ):
        """
        Visit method invocation statement.
        """
        if o is None:
            return

        # ✅ FIX: Phải truyền Access object, không phải SubBody!
        code, ret_type = self.visit(node.method_call, Access(o.frame, o.sym))
        self.emit.print_out(code)

        # 2. Nếu hàm trả về giá trị (không phải void), cần pop khỏi stack
        # vì đây là statement, giá trị trả về bị bỏ qua.
        if not is_void_type(ret_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))

    # ============================================================================
    # Left-hand Side (LHS)
    # ============================================================================

    def visit_id_lhs(self, node: "IdLHS", o: Access = None):
        """
        Visit identifier LHS - generate code to write to variable.
        """
        # if o is None:
        #     return "", None
        
        # # Find symbol
        # sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        # if sym is None:
        #     raise IllegalOperandException(f"Undeclared variable: {node.name}")
        
        # if type(sym.value) is Index:
        #     code = self.emit.emit_write_var(
        #         sym.name, sym.type, sym.value.value, o.frame
        #     )
        #     return code, sym.type
        # else:
        #     raise IllegalOperandException(f"Cannot assign to: {node.name}")
        if o is None: 
            return "", None
        
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared variable: {node.name}")
            
        # CASE: Assign vào biến Wrapper (Reference Type)
        if isinstance(sym.type, ReferenceType):
            # Stack hiện tại (sau visit RHS): [Value]
            # Cần tạo: [ArrRef, 0, Value] cho IASTORE/FASTORE/...
            
            code = ""
            
            # 1. Load địa chỉ mảng (Wrapper) -> Stack: [Value, ArrRef]
            code += self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
            
            # 2. Push index 0 -> Stack: [Value, ArrRef, 0]
            code += self.emit.emit_push_iconst(0, o.frame)
            
            # 3. Đổi thành [ArrRef, 0, Value] bằng dup2_x1 + pop2
            code += self.emit.jvm.INDENT + "dup2_x1\n"  # [ArrRef, 0, Value, ArrRef, 0]
            code += self.emit.jvm.INDENT + "pop2\n"     # [ArrRef, 0, Value]
            
            # 4. Emit ASTORE instruction trực tiếp
            inner_type = sym.type.referenced_type
            if is_int_type(inner_type):
                code += self.emit.jvm.emitIASTORE()
            elif is_float_type(inner_type):
                code += self.emit.jvm.emitFASTORE()
            elif is_bool_type(inner_type):
                code += self.emit.jvm.emitBASTORE()
            elif is_reference_type(inner_type):
                code += self.emit.jvm.emitAASTORE()
            
            # 5. Manually update frame stack
            o.frame.pop()  # Pop value
            o.frame.pop()  # Pop index
            o.frame.pop()  # Pop arrref
            
            return code, inner_type
            
        # CASE: Assign vào biến thường (Object/Array variable)
        elif type(sym.value) is Index:
            code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
            return code, sym.type
            
        else:
            raise IllegalOperandException(f"Cannot assign to: {node.name}")

    def visit_postfix_lhs(self, node: "PostfixLHS", o: Any = None):
        """
        Visit postfix LHS (for member access, array access).
        """
        # if o is None: return "", None
            
        # primary = node.postfix_expr.primary
        # ops = node.postfix_expr.postfix_ops
        
        # if not ops:
        #     raise IllegalOperandException("Invalid LHS expression")

        # last_op = ops[-1]
        # prev_ops = ops[:-1]
        
        # # --- CASE 1: Array Assignment (arr[index] := val) ---
        # if isinstance(last_op, ArrayAccess):
        #     temp_expr = PostfixExpression(primary, prev_ops)
        #     # Truy cập mảng để lấy tham chiếu -> is_left=False
        #     new_o = Access(o.frame, o.sym, False)
        #     arr_code, arr_type = self.visit(temp_expr, new_o) 
            
        #     if not isinstance(arr_type, ArrayType):
        #         raise IllegalOperandException("Indexing assign on non-array type")

        #     idx_code, idx_type = self.visit(last_op.index, new_o)
            
        #     full_code = (arr_code or "") + (idx_code or "")
        #     full_code += self.emit.jvm.INDENT + "dup2_x1\n"
        #     full_code += self.emit.jvm.INDENT + "pop2\n"
            
        #     full_code += self.emit.emit_astore(arr_type.element_type, o.frame)
        #     return full_code, arr_type.element_type

        # # --- CASE 2: Field Assignment (obj.field := val) ---
        # elif isinstance(last_op, MemberAccess):
        #     field_name = last_op.member_name
            
        #     # Check Static assign
        #     is_static_assign = False
        #     class_name = ""
        #     if not prev_ops and isinstance(primary, Identifier):
        #         if primary.name in self.class_table:
        #             is_static_assign = True
        #             class_name = primary.name
            
        #     if is_static_assign:
        #         field_type, is_static_field = self.lookup_field(class_name, field_name)
        #         full_code = self.emit.emit_put_static(f"{class_name}/{field_name}", field_type, o.frame)
        #         return full_code, field_type
        #     else:
        #         temp_expr = PostfixExpression(primary, prev_ops)
                
        #         new_o = Access(o.frame, o.sym, False) 
        #         obj_code, obj_type = self.visit(temp_expr, new_o)
                
        #         # [FIX] Check type name to avoid conflict between nodes.ClassType and utils.ClassType
        #         if not isinstance(obj_type, ClassType):
        #             raise IllegalOperandException(f"Assign field on non-object")

        #         field_type, is_static_field = self.lookup_field(obj_type.class_name, field_name)
                
        #         full_code = obj_code if obj_code else ""

        #         if is_static_field:
        #             full_code += self.emit.emit_pop(o.frame)
        #             full_code += self.emit.emit_put_static(f"{obj_type.class_name}/{field_name}", field_type, o.frame)
        #         else:
        #             full_code += self.emit.jvm.INDENT + "swap\n"
        #             put_code = self.emit.emit_put_field(f"{obj_type.class_name}/{field_name}", field_type, o.frame)
        #             full_code += put_code

        #         return full_code, field_type
        
        # else:
        #     raise IllegalOperandException("Invalid assignment target")
        if o is None: 
            return "", None
            
        primary = node.postfix_expr.primary
        ops = node.postfix_expr.postfix_ops
        
        if not ops:
            raise IllegalOperandException("Invalid LHS expression")

        last_op = ops[-1]
        prev_ops = ops[:-1]
        
        # --- CASE 1: Array Assignment ---
        if isinstance(last_op, ArrayAccess):
            temp_expr = PostfixExpression(primary, prev_ops)
            new_o = Access(o.frame, o.sym, False)
            arr_code, arr_type = self.visit(temp_expr, new_o) 
            
            if not isinstance(arr_type, ArrayType):
                raise IllegalOperandException("Indexing assign on non-array type")

            idx_code, idx_type = self.visit(last_op.index, new_o)
            
            # Stack sau arr_code + idx_code: [value, arrref, index]
            # Cần: [arrref, index, value]
            full_code = (arr_code or "") + (idx_code or "")
            full_code += self.emit.jvm.INDENT + "dup2_x1\n"  # [arrref, index, value, arrref, index]
            full_code += self.emit.jvm.INDENT + "pop2\n"     # [arrref, index, value]
            
            # ❌ KHÔNG gọi emit_astore vì nó sẽ pop thêm 3 lần!
            # ✅ Chỉ cần instruction ASTORE
            if is_int_type(arr_type.element_type):
                full_code += self.emit.jvm.emitIASTORE()
            elif is_float_type(arr_type.element_type):
                full_code += self.emit.jvm.emitFASTORE()
            elif is_bool_type(arr_type.element_type):
                full_code += self.emit.jvm.emitBASTORE()
            elif is_reference_type(arr_type.element_type):
                full_code += self.emit.jvm.emitAASTORE()
            
            # Manually pop frame 3 lần
            o.frame.pop()
            o.frame.pop()
            o.frame.pop()
            
            return full_code, arr_type.element_type

        # --- CASE 2: Field Assignment ---
        elif isinstance(last_op, MemberAccess):
            field_name = last_op.member_name
            
            # Check Static assign
            is_static_assign = False
            class_name = ""
            if not prev_ops and isinstance(primary, Identifier):
                if primary.name in self.class_table:
                    is_static_assign = True
                    class_name = primary.name
            
            if is_static_assign:
                field_type, is_static_field = self.lookup_field(class_name, field_name)
                # Stack: [value]
                full_code = self.emit.emit_put_static(f"{class_name}/{field_name}", field_type, o.frame)
                return full_code, field_type
            else:
                temp_expr = PostfixExpression(primary, prev_ops)
                new_o = Access(o.frame, o.sym, False) 
                obj_code, obj_type = self.visit(temp_expr, new_o)
                
                if not isinstance(obj_type, ClassType):
                    raise IllegalOperandException(f"Assign field on non-object")

                field_type, is_static_field = self.lookup_field(obj_type.class_name, field_name)
                
                # Stack sau obj_code: [value, objref]
                # Cần: [objref, value] cho PUTFIELD
                full_code = obj_code if obj_code else ""
                full_code += self.emit.jvm.INDENT + "swap\n"  # [objref, value]

                if is_static_field:
                    full_code += self.emit.emit_pop(o.frame)  # Pop objref
                    full_code += self.emit.emit_put_static(f"{obj_type.class_name}/{field_name}", field_type, o.frame)
                else:
                    # ✅ emit_put_field đã fix, chỉ pop 2 lần
                    put_code = self.emit.emit_put_field(f"{obj_type.class_name}/{field_name}", field_type, o.frame)
                    full_code += put_code

                return full_code, field_type
        
        else:
            raise IllegalOperandException("Invalid assignment target")

    # ============================================================================
    # Expressions
    # ============================================================================
    def lookup_field(self, class_name: str, field_name: str):
        """
        Tìm kiếm thuộc tính trong class (bao gồm cả lớp cha).
        Trả về: (field_type, is_static)
        """
        if class_name not in self.class_table:
            raise IllegalOperandException(f"Undeclared class: {class_name}")

        current_class = self.class_table[class_name]
        
        while current_class:
            for member in current_class.members:
                # Kiểm tra AttributeDecl
                if isinstance(member, AttributeDecl):
                    # Một AttributeDecl có thể chứa nhiều biến (vd: int x, y;)
                    for attr in member.attributes:
                        if attr.name == field_name:
                            return member.attr_type, member.is_static
            
            # Leo lên lớp cha
            parent_name = current_class.superclass
            if parent_name and parent_name != "java/lang/Object":
                 if parent_name in self.class_table:
                     current_class = self.class_table[parent_name]
                 else:
                     break
            else:
                break
        
        raise IllegalOperandException(f"Field '{field_name}' not found in class '{class_name}'")

    def resolve_constructor(self, class_name: str, arg_types: List[Type]):
        """
        Tìm constructor phù hợp dựa trên danh sách kiểu tham số.
        Trả về: FunctionType của constructor
        """
        """
        Tìm constructor phù hợp dựa trên danh sách kiểu tham số.
        Cập nhật: Thêm kiểm tra kiểu chặt chẽ.
        """
        if class_name not in self.class_table:
            raise IllegalOperandException(f"Undeclared class: {class_name}")
            
        class_decl = self.class_table[class_name]
        constructors = [m for m in class_decl.members if isinstance(m, ConstructorDecl)]
        
        # Nếu không có constructor nào và không có tham số -> Default Constructor
        if not constructors and not arg_types:
             return FunctionType([], PrimitiveType("void"))

        # Tìm constructor khớp tham số
        for constr in constructors:
            if len(constr.params) == len(arg_types):
                match = True
                for i, param in enumerate(constr.params):
                    p_type = param.param_type
                    a_type = arg_types[i]
                    
                    # Unbox ReferenceType (nếu có) để so sánh lõi
                    if isinstance(p_type, ReferenceType): p_type = p_type.referenced_type
                    if isinstance(a_type, ReferenceType): a_type = a_type.referenced_type
                    
                    # Kiểm tra tương thích kiểu
                    if is_int_type(p_type):
                        if not is_int_type(a_type): match = False
                    elif is_float_type(p_type):
                        # Chấp nhận int (coercion) hoặc float
                        if not (is_float_type(a_type) or is_int_type(a_type)): match = False
                    elif is_bool_type(p_type):
                        if not is_bool_type(a_type): match = False
                    elif is_string_type(p_type):
                        if not is_string_type(a_type): match = False
                    elif isinstance(p_type, ClassType):
                        # Kiểm tra: a_type phải là ClassType và cùng tên (hoặc subclass - ở đây check đơn giản cùng tên)
                        # Nếu muốn hỗ trợ null: a_type is None (từ NilLiteral) cũng match
                        if a_type is None: # Nil
                            continue
                        if not isinstance(a_type, ClassType) or p_type.class_name != a_type.class_name:
                            match = False
                    elif isinstance(p_type, ArrayType):
                        # So sánh element type của mảng
                        # (Cần implement hàm so sánh sâu hơn cho mảng)
                        if not isinstance(a_type, ArrayType): match = False
                        # Tạm thời bỏ qua check sâu element type ở đây cho gọn
                    else:
                        match = False
                    
                    if not match: break
                
                if match:
                    param_types = [p.param_type for p in constr.params]
                    return FunctionType(param_types, PrimitiveType("void"))
        
        if not constructors and arg_types:
             raise IllegalOperandException(f"No matching constructor for class {class_name}")
             
        raise IllegalOperandException(f"No matching constructor for class {class_name} with provided arguments")
    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        """
        Visit binary operation.
        TODO: Implement binary operation code generation
        """
        if o is None:
            return "", None
            
        frame = o.frame
        op = node.operator
        
        if op in ["&&", "||"]:
            res_code = []
            exit_label = frame.get_new_label()

            # Evaluate LHS
            lc, lt = self.visit(node.left, o)
            res_code.append(lc)
            
            if op == '&&':
                # Nếu LHS = false (0), push false và skip RHS
                false_label = frame.get_new_label()
                res_code.append(self.emit.emit_if_false(false_label, frame))  # Pop và kiểm tra
                
                # LHS = true, evaluate RHS
                rc, rt = self.visit(node.right, o)
                res_code.append(rc)
                res_code.append(self.emit.emit_goto(exit_label, frame))
                
                # False path: push false
                res_code.append(self.emit.emit_label(false_label, frame))
                res_code.append(self.emit.emit_push_iconst(0, frame))
                
            else:  # ||
                # ✅ FIX: Nếu LHS = true (1), push true và skip RHS
                true_label = frame.get_new_label()
                
                # Duplicate giá trị trước khi kiểm tra
                res_code.append(self.emit.emit_dup(frame))
                res_code.append(self.emit.emit_if_true(true_label, frame))  # Pop bản copy
                
                # LHS = false, pop giá trị false ban đầu và evaluate RHS
                res_code.append(self.emit.emit_pop(frame))  # Pop giá trị false còn lại
                rc, rt = self.visit(node.right, o)
                res_code.append(rc)
                res_code.append(self.emit.emit_goto(exit_label, frame))
                
                # True path: giá trị true vẫn còn trên stack
                res_code.append(self.emit.emit_label(true_label, frame))
                # Không cần push gì thêm, stack đã có giá trị true từ DUP
            
            res_code.append(self.emit.emit_label(exit_label, frame))
            return "".join(res_code), PrimitiveType("boolean")
                
        # 2. Regular operations (Evaluate LHS then RHS)
        lc, lt = self.visit(node.left, o)
        rc, rt = self.visit(node.right, o)
            
        # 3. String concatenation (^)
        if op == "^":
            body_code = []
            body_code.append(lc)
            # Spec: Only operator ^ is used to operate on string operands.
            # Emitter instruction for concatenation usually expects strings.
            body_code.append(rc)
            body_code.append(self.emit.emit_invoke_virtual(
                "java/lang/String/concat",
                FunctionType([PrimitiveType("string")], PrimitiveType("string")),
                frame
            ))
            return "".join(body_code), PrimitiveType("string")
            
        # 4. Arithmetic and Comparison
        # Xác định xem có cần tính toán trên số thực không
        # Spec: phép '/' luôn trả về float. Các phép khác nếu có 1 toán hạng float thì kết quả là float.
        is_float_result = is_float_type(lt) or is_float_type(rt) or op == '/'
        
        # Kiểm tra ràng buộc cho phép chia lấy nguyên và modulo
        if op in ['\\', '%'] and (is_float_type(lt) or is_float_type(rt)):
             raise IllegalOperandException(f"Operator {op} requires integer operands")

        body_c = [lc]
        
        # Coercion: Chuyển đổi Int sang Float nếu cần
        if is_float_result and is_int_type(lt): 
            body_c.append(self.emit.emit_i2f(frame))
            
        body_c.append(rc)
        
        if is_float_result and is_int_type(rt): 
            body_c.append(self.emit.emit_i2f(frame))
        
        # Kiểu dữ liệu dùng cho lệnh emit (IADD/FADD...)
        emit_type = PrimitiveType('float') if is_float_result else PrimitiveType('int')

        # Generate Instruction
        if op in ["+", "-"]:
            body_c.append(self.emit.emit_add_op(op, emit_type, frame))
            return "".join(body_c), emit_type
            
        elif op in ["*", "/"]:
            # Lưu ý: emit_mul_op xử lý cả mul và div (cho float)
            body_c.append(self.emit.emit_mul_op(op, emit_type, frame))
            return "".join(body_c), emit_type
            
        elif op == '\\': # Integer Division
            body_c.append(self.emit.emit_div(frame)) # IDIV
            return "".join(body_c), PrimitiveType('int')
            
        elif op == '%': # Modulo
            body_c.append(self.emit.emit_mod(frame)) # IREM
            return "".join(body_c), PrimitiveType('int')
            
        elif op in [">", "<", ">=", "<=", "==", "!="]:
            # Relational returns boolean
            body_c.append(self.emit.emit_re_op(op, emit_type, frame))
            return "".join(body_c), PrimitiveType("boolean")
 
        raise IllegalOperandException(f"Unknown binary operator: {op}")

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        """
        Visit unary operation.
        TODO: Implement unary operation code generation
        """
        # if o is None:
        #     return "", None
            
        # body_code, body_type = self.visit(node.operand, o) # Sửa node.body thành node.operand
        # op = node.operator # Sửa node.op thành node.operator
        
        # if op == "-":
        #     # Unary minus (negation)
        #     neg_code = self.emit.emit_neg_op(body_type, o.frame)
        #     return body_code + neg_code, body_type
            
        # elif op == "!":
        #     # Logical NOT
        #     if not is_bool_type(body_type):
        #          raise IllegalOperandException(f"Operator ! requires boolean operand")
        #     not_code = self.emit.emit_not(body_type, o.frame)
        #     return body_code + not_code, body_type
        
        # elif op == "+":
        #     # Unary plus (Identity) - Do nothing
        #     return body_code, body_type
            
        # raise IllegalOperandException(f"Unknown unary operator: {op}")
        if o is None:
            return "", None
        
        # [FIX] Kiểm tra tên thuộc tính đúng của UnaryOp (body/op vs operand/operator)
        if hasattr(node, 'body'):
            child = node.body
        else:
            child = node.operand
            
        if hasattr(node, 'op'):
            op_str = node.op
        else:
            op_str = node.operator

        body_code, body_type = self.visit(child, o)
        
        if op_str == "-":
            neg_code = self.emit.emit_neg_op(body_type, o.frame)
            return body_code + neg_code, body_type
            
        elif op_str == "!":
            if not is_bool_type(body_type):
                 raise IllegalOperandException(f"Operator ! requires boolean operand")
            not_code = self.emit.emit_not(body_type, o.frame)
            return body_code + not_code, body_type
        
        elif op_str == "+":
            return body_code, body_type
            
        raise IllegalOperandException(f"Unknown unary operator: {op_str}")

    def visit_postfix_expression(self, node: "PostfixExpression", o: Access = None):
        """
        Visit postfix expression (method calls, member access, array access).
        TODO: Implement postfix expression code generation
        """
        if o is None:
            return "", None

        # 1. Xử lý Primary
        c_code = ""
        c_type = None
        is_static_access = False 

        # Kiểm tra xem Primary có phải là tên Class (Static access) hay không
        if isinstance(node.primary, Identifier):
            name = node.primary.name
            # Kiểm tra 'io' hoặc tên class trong bảng ký hiệu
            if name == "io" or name in self.class_table:
                c_type = ClassType(name)
                is_static_access = True
                c_code = "" # Static access không sinh code load biến
            else:
                # Nếu không phải static context, visit bình thường
                c_code, c_type = self.visit(node.primary, o)
        else:
            c_code, c_type = self.visit(node.primary, o)

        # [FIX] Guard: Đảm bảo c_code không bao giờ là None
        if c_code is None:
            c_code = ""

        # 2. Loop ops
        for op in node.postfix_ops:
            # Gọi visit cho từng Op (MethodCall, MemberAccess, ArrayAccess)
            # Truyền ngữ cảnh hiện tại xuống
            context = (o, c_type, is_static_access)
            op_code, op_type = self.visit(op, context)
            
            # [FIX] Guard: Kiểm tra op_code trước khi cộng
            if op_code:
                c_code += op_code
            
            c_type = op_type
            
            # Sau một phép toán, kết quả trả về là giá trị (instance value), 
            # nên static context sẽ bị tắt
            if isinstance(op, (MethodCall, ArrayAccess, MemberAccess)):
                is_static_access = False

        return c_code, c_type
    def visit_method_call(self, node: "MethodCall", o: Access = None):
        """
        Visit method call.
        TODO: Implement method call code generation
        """
        # if o is None:
        #     return "", None
            
        # access, prev_type, is_static_access = o
        # frame = access.frame
        # method_name = node.method_name

        # # [FIX] Check type name to avoid conflict
        # if type(prev_type).__name__ != "ClassType":
        #      raise IllegalOperandException(f"Cannot invoke method on type: {prev_type}")
        
        # class_name = prev_type.class_name
        
        # # Lookup method info
        # func_type, is_static_method = self.lookup_method(class_name, method_name)
        
        # c_code = ""
        
        # if is_static_access and not is_static_method:
        #     raise IllegalOperandException(f"Cannot invoke instance method '{method_name}' from static context")
        
        # if not is_static_access and is_static_method:
        #      c_code += self.emit.emit_pop(frame)
        
        # # Sinh mã cho các tham số
        # for i, arg_expr in enumerate(node.args):
        #     arg_code, arg_type = self.visit(arg_expr, access)
            
        #     if arg_code:
        #         c_code += arg_code
            
        #     if i < len(func_type.param_types):
        #         param_type = func_type.param_types[i]
        #         if is_float_type(param_type) and is_int_type(arg_type):
        #             c_code += self.emit.emit_i2f(frame)

        # full_method_name = f"{class_name}/{method_name}"
        # if is_static_method:
        #     c_code += self.emit.emit_invoke_static(full_method_name, func_type, frame)
        # else:
        #     c_code += self.emit.emit_invoke_virtual(full_method_name, func_type, frame)
            
        # return c_code, func_type.return_type
        if o is None:
            return "", None
            
        # Unpack context từ visit_postfix_expression
        # context = (access_object, previous_type, is_static_access)
        access, prev_type, is_static_access = o
        frame = access.frame
        method_name = node.method_name

        # 1. Kiểm tra kiểu của đối tượng gọi hàm
        if type(prev_type).__name__ != "ClassType":
             raise IllegalOperandException(f"Cannot invoke method on type: {prev_type}")
        
        class_name = prev_type.class_name
        
        # 2. Lookup method signature
        # func_type chứa param_types và return_type
        func_type, is_static_method = self.lookup_method(class_name, method_name)
        
        c_code = ""
        
        # 3. Xử lý logic gọi Static vs Instance
        if is_static_access and not is_static_method:
            raise IllegalOperandException(f"Cannot invoke instance method '{method_name}' from static context")
        
        # Nếu gọi method tĩnh từ instance (obj.staticMethod()), ta phải POP instance đi
        # vì invokestatic không cần đối tượng 'this'
        if not is_static_access and is_static_method:
             c_code += self.emit.emit_pop(frame)
        
        # 4. Sinh mã cho các tham số (Arguments)
        for i, arg_expr in enumerate(node.args):
            # Lấy kiểu tham số mà hàm định nghĩa
            param_type = func_type.param_types[i]
            
            # Kiểm tra xem tham số này có yêu cầu tham chiếu (int &) hay không
            is_ref_param = isinstance(param_type, ReferenceType)
            
            # Tạo Access mới, bật cờ is_ref_needed nếu tham số là ReferenceType
            # Lưu ý: Bạn cần sửa __init__ của Access để nhận tham số này, 
            # hoặc gán thuộc tính sau khi khởi tạo.
            arg_access = Access(frame, access.sym, False, False)
            arg_access.is_ref_needed = is_ref_param # Gán cờ thủ công nếu không sửa được constructor
            
            # Visit Argument
            arg_code, arg_type = self.visit(arg_expr, arg_access)
            
            if arg_code:
                c_code += arg_code
            
            # 5. Xử lý Coercion (Ép kiểu) & Wrapper Logic
            
            # Trường hợp A: Hàm cần tham chiếu (int &), nhưng truyền vào Wrapper (ReferenceType)
            # -> Code visit_identifier (với is_ref_needed=True) đã trả về Wrapper Array.
            # -> Không cần làm gì thêm (Match).
            
            # Trường hợp B: Hàm cần giá trị (int), truyền vào giá trị (int)
            # -> Coercion Int -> Float nếu cần
            if not is_ref_param:
                if is_float_type(param_type) and is_int_type(arg_type):
                    c_code += self.emit.emit_i2f(frame)
            
            # Trường hợp C: Hàm cần Reference (int &), nhưng truyền vào Value (int) -> LỖI SEMANTIC
            # (Compiler nên chặn từ bước kiểm tra kiểu, nhưng ở đây CodeGen giả định input đúng)

        # 6. Sinh lệnh gọi hàm
        full_method_name = f"{class_name}/{method_name}"
        if is_static_method:
            c_code += self.emit.emit_invoke_static(full_method_name, func_type, frame)
        else:
            c_code += self.emit.emit_invoke_virtual(full_method_name, func_type, frame)
            
        return c_code, func_type.return_type
    def visit_member_access(self, node: "MemberAccess", o: Access = None):
        """
        Visit member access.
        TODO: Implement member access code generation
        """
        # if o is None:
        #     return "", None

        # access, prev_type, is_static_access = o
        # frame = access.frame
        # field_name = node.member_name
        
        # # [FIX] Check type name instead of isinstance
        # if type(prev_type).__name__ != "ClassType":
        #     raise IllegalOperandException(f"Cannot access field '{field_name}' on non-class type: {prev_type}")
        
        # class_name = prev_type.class_name
        
        # # Lookup field info
        # field_type, is_static_field = self.lookup_field(class_name, field_name)
        
        # full_field_name = f"{class_name}/{field_name}"
        # c_code = ""

        # if is_static_access:
        #     if not is_static_field:
        #          raise IllegalOperandException(f"Cannot access instance field '{field_name}' from static context")
        #     c_code += self.emit.emit_get_static(full_field_name, field_type, frame)
        # else:
        #     if is_static_field:
        #         c_code += self.emit.emit_pop(frame)
        #         c_code += self.emit.emit_get_static(full_field_name, field_type, frame)
        #     else:
        #         c_code += self.emit.emit_get_field(full_field_name, field_type, frame)
        
        # return c_code, field_type
        if o is None:
            return "", None

        access, prev_type, is_static_access = o
        frame = access.frame
        field_name = node.member_name
        
        if type(prev_type).__name__ != "ClassType":
            raise IllegalOperandException(f"Cannot access field '{field_name}' on non-class type: {prev_type}")
        
        class_name = prev_type.class_name
        field_type, is_static_field = self.lookup_field(class_name, field_name)
        
        full_field_name = f"{class_name}/{field_name}"
        c_code = ""

        # ✅ CHECK: Nếu cần reference và field là primitive
        # → Cần trả về wrapper thay vì unwrap value
        need_wrapper = hasattr(access, 'is_ref_needed') and access.is_ref_needed
        is_primitive_field = is_int_type(field_type) or is_float_type(field_type) or is_bool_type(field_type) or is_string_type(field_type)
        
        if is_static_access:
            if not is_static_field:
                raise IllegalOperandException(f"Cannot access instance field '{field_name}' from static context")
            c_code += self.emit.emit_get_static(full_field_name, field_type, frame)
            
            # ✅ Nếu cần wrapper cho static primitive field
            if need_wrapper and is_primitive_field:
                # Wrap value vào array
                c_code += self.wrap_value_to_array(field_type, frame)
                return c_code, ReferenceType(field_type)
        else:
            if is_static_field:
                c_code += self.emit.emit_pop(frame)
                c_code += self.emit.emit_get_static(full_field_name, field_type, frame)
                
                if need_wrapper and is_primitive_field:
                    c_code += self.wrap_value_to_array(field_type, frame)
                    return c_code, ReferenceType(field_type)
            else:
                c_code += self.emit.emit_get_field(full_field_name, field_type, frame)
                
                # ✅ FIX: Nếu return reference type và field là primitive
                # → Wrap value thành array
                if need_wrapper and is_primitive_field:
                    c_code += self.wrap_value_to_array(field_type, frame)
                    return c_code, ReferenceType(field_type)
        
        return c_code, field_type

    def wrap_value_to_array(self, elem_type, frame):
        """Helper: Wrap a primitive value on stack into [1] array"""
        code = ""
        # Stack: [value]
        
        # 1. Create array [1]
        code += self.emit.emit_push_iconst(1, frame)
        if is_int_type(elem_type):
            code += self.emit.emit_new_array("int")
        elif is_float_type(elem_type):
            code += self.emit.emit_new_array("float")
        elif is_bool_type(elem_type):
            code += self.emit.emit_new_array("boolean")
        elif is_string_type(elem_type):
            code += self.emit.jvm.emitANEWARRAY("java/lang/String")
        
        # Stack: [value, arrref]
        # 2. Rearrange to [arrref, 0, value]
        code += self.emit.jvm.INDENT + "swap\n"  # [arrref, value]
        code += self.emit.emit_dup(frame)        # [arrref, value, arrref]
        # Manually pop 1 vì dup push 1
        frame.pop()
        
        code += self.emit.jvm.INDENT + "dup_x1\n"  # [arrref, arrref, value, arrref]
        code += self.emit.emit_pop(frame)          # [arrref, arrref, value]
        code += self.emit.emit_push_iconst(0, frame)  # [arrref, arrref, value, 0]
        code += self.emit.jvm.INDENT + "swap\n"     # [arrref, arrref, 0, value]
        
        # 3. Store
        code += self.emit.emit_astore(elem_type, frame)  # [arrref]
        
        return code
    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        """
        Visit array access.
        TODO: Implement array access code generation
        """
        if o is None:
            return "", None
            
        access, prev_type, is_static_access = o
        frame = access.frame
        
        # Unwrap ReferenceType
        actual_type = prev_type
        if isinstance(prev_type, ReferenceType):
            actual_type = prev_type.referenced_type
        
        if not isinstance(actual_type, ArrayType):
            raise IllegalOperandException("Indexing on non-array type")
        
        # Visit index
        idx_code, idx_type = self.visit(node.index, access)
        
        # ✅ FIX: Unwrap idx_type nếu cần
        idx_actual_type = idx_type
        if isinstance(idx_type, ReferenceType):
            idx_actual_type = idx_type.referenced_type
        
        if not is_int_type(idx_actual_type):
            raise IllegalOperandException("Array index must be integer")
        
        c_code = idx_code
        
        # ✅ Nếu cần reference to array element
        if hasattr(access, 'is_ref_needed') and access.is_ref_needed:
            # Return [arrref, index] wrapped
            # Tạo wrapper chứa [arrref, index]
            # CHƯA IMPLEMENT ĐẦY ĐỦ - tạm raise error
            raise IllegalOperandException("Array element reference not fully implemented")
        
        # Load value
        c_code += self.emit.emit_aload(actual_type.element_type, frame)
        
        return c_code, actual_type.element_type

    def visit_object_creation(self, node: "ObjectCreation", o: Access = None):
        """
        Visit object creation.
        """
        if o is None:
            return "", None

        class_name = node.class_name
        
        # 1. Sinh mã NEW
        o.frame.push()
        code = self.emit.jvm.emitNEW(class_name) 

        # 2. DUP (để giữ lại tham chiếu đối tượng sau khi gọi constructor)
        code += self.emit.emit_dup(o.frame)

        # 3. Visit Arguments trước để lấy Code và Type
        # Lưu vào list thay vì cộng chuỗi ngay để còn xử lý Coercion sau này
        arg_results = []
        arg_types = []
        for arg in node.args:
            ac, at = self.visit(arg, o)
            arg_results.append((ac, at))
            arg_types.append(at)
        
        # 4. Tìm Constructor phù hợp
        # Hàm này trả về FunctionType của constructor (chứa param_types chuẩn)
        ctor_type = self.resolve_constructor(class_name, arg_types)
        
        # 5. Sinh mã Argument kèm Coercion (Int -> Float)
        for i, (arg_code, arg_type) in enumerate(arg_results):
            # Append code sinh ra giá trị của tham số
            if arg_code:
                code += arg_code
            
            # Kiểm tra xem có cần ép kiểu không dựa trên chữ ký Constructor
            if i < len(ctor_type.param_types):
                param_type = ctor_type.param_types[i]
                # Nếu tham số yêu cầu Float mà truyền vào Int -> Thêm i2f
                if is_float_type(param_type) and is_int_type(arg_type):
                    code += self.emit.emit_i2f(o.frame)
        
        # 6. INVOKESPECIAL <init>
        code += self.emit.emit_invoke_special(o.frame, f"{class_name}/<init>", ctor_type)

        return code, ClassType(class_name)

    def visit_identifier(self, node: "Identifier", o: Access = None):
        """
        Visit identifier - generate code to read variable.
        """
        if o is None:
            return "", None
        
        # Find symbol
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")
        if isinstance(sym.type, ReferenceType):
            # 1. Load địa chỉ mảng (Wrapper)
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
            
            # Nếu chỉ cần địa chỉ (ví dụ: gán cho int & ref = x) -> Trả về luôn
            if hasattr(o, 'is_ref_needed') and o.is_ref_needed:
                 return code, sym.type

            # Nếu cần giá trị (ví dụ: x + 1) -> Unwrap (Load index 0)
            if not o.is_left:
                code += self.emit.emit_push_iconst(0, o.frame)
                code += self.emit.emit_aload(sym.type.referenced_type, o.frame)
                return code, sym.type.referenced_type
            
            # Nếu là vế trái (x := 5) -> Trả về code load mảng + index 0, 
            # để visit_assignment sinh lệnh store
            else:
                 code += self.emit.emit_push_iconst(0, o.frame)
                 return code, sym.type.referenced_type
        if type(sym.value) is Index:
            # --- SỬA Ở ĐÂY ---
            if o.is_left:
                # Nếu là vế trái (LHS), sinh mã ghi (Write/Store)
                code = self.emit.emit_write_var(
                    sym.name, sym.type, sym.value.value, o.frame
                )
            else:
                # Nếu là biểu thức (RHS), sinh mã đọc (Read/Load)
                code = self.emit.emit_read_var(
                    sym.name, sym.type, sym.value.value, o.frame
                )
            # -----------------
            return code, sym.type
        else:
            raise IllegalOperandException(f"Cannot read/write: {node.name}")
    def visit_this_expression(self, node: "ThisExpression", o: Access = None):
        """
        Visit this expression - load 'this' reference.
        """
        # if o is None:
        #     return "", None
        
        # # Find 'this' in symbol table (should be at index 0 for instance methods)
        # this_sym = next(filter(lambda x: x.name == "this", o.sym), None)
        # if this_sym is None:
        #     raise IllegalOperandException("'this' not available in static context")
        
        # if type(this_sym.value) is Index:
        #     code = self.emit.emit_read_var(
        #         "this", this_sym.type, this_sym.value.value, o.frame
        #     )
        #     return code, this_sym.type
        # else:
        #     raise IllegalOperandException("Invalid 'this' reference")
        if o is None: return "", None
        
        code = self.emit.emit_read_var("this", ClassType(self.current_class), 0, o.frame)
        return code, ClassType(self.current_class)
    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Access = None
    ):
        """
        Visit parenthesized expression - just visit inner expression.
        """
        return self.visit(node.expr, o)

    # ============================================================================
    # Literals
    # ============================================================================

    def visit_int_literal(self, node: "IntLiteral", o: Access = None):
        """
        Visit integer literal - push integer constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_iconst(node.value, o.frame)
        return code, PrimitiveType("int")

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        """
        Visit float literal - push float constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_fconst(str(node.value), o.frame)
        return code, PrimitiveType("float")

    def visit_bool_literal(self, node: "BoolLiteral", o: Access = None):
        """
        Visit boolean literal - push boolean constant.
        """
        if o is None:
            return "", None
        value_str = "1" if node.value else "0"
        code = self.emit.emit_push_iconst(value_str, o.frame)
        return code, PrimitiveType("boolean")

    def visit_string_literal(self, node: "StringLiteral", o: Access = None):
        """
        Visit string literal - push string constant.
        """
        if o is None:
            return "", None
        code = self.emit.emit_push_const('"' + node.value + '"', PrimitiveType("string"), o.frame)
        return code, PrimitiveType("string")

    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None):
        """
        Visit array literal.
        """
        if o is None:
            return "", None
        
        if not node.value:
            raise IllegalOperandException("Empty array literal")

        # 1. Xác định kiểu phần tử từ phần tử đầu tiên
        first_elem = node.value[0]
        elem_type = None
        
        # Kiểm tra nhanh nếu là Literal cơ bản
        if isinstance(first_elem, IntLiteral): 
            elem_type = PrimitiveType("int")
        elif isinstance(first_elem, FloatLiteral): 
            elem_type = PrimitiveType("float")
        elif isinstance(first_elem, BoolLiteral): 
            elem_type = PrimitiveType("boolean")
        elif isinstance(first_elem, StringLiteral): 
            elem_type = PrimitiveType("string")
        
        # Nếu là biểu thức phức tạp, cần visit thử để lấy kiểu
        if elem_type is None:
             old_stack = o.frame.curr_op_stack_size
             _, elem_type = self.visit(first_elem, o)
             o.frame.curr_op_stack_size = old_stack # Restore stack simulation state
        
        # 2. Push kích thước mảng
        size = len(node.value)
        code = self.emit.emit_push_iconst(size, o.frame)
        
        # 3. Tạo mảng (New Array)
        if is_int_type(elem_type):
            code += self.emit.emit_new_array("int")
        elif is_float_type(elem_type):
            code += self.emit.emit_new_array("float")
        elif is_bool_type(elem_type):
            code += self.emit.emit_new_array("boolean")
        elif is_string_type(elem_type):
            code += self.emit.jvm.emitANEWARRAY("java/lang/String")
        elif isinstance(elem_type, ClassType):
             code += self.emit.jvm.emitANEWARRAY(elem_type.class_name)
        else:
             raise IllegalOperandException("Unsupported element type in array literal")

        # 4. Gán từng phần tử
        for i, expr in enumerate(node.value):
            # Duplicate Array Reference (vì astore sẽ pop mất ref)
            code += self.emit.emit_dup(o.frame)
            
            # Push Index
            code += self.emit.emit_push_iconst(i, o.frame)
            
            # Push Value
            val_code, val_type = self.visit(expr, o)
            code += val_code
            
            # Coercion: Int -> Float nếu mảng là float
            if is_float_type(elem_type) and is_int_type(val_type):
                code += self.emit.emit_i2f(o.frame)
            
            # Store (IASTORE, FASTORE, AASTORE, etc.)
            code += self.emit.emit_astore(elem_type, o.frame)
            
        return code, ArrayType(elem_type, size)

    def visit_nil_literal(self, node: "NilLiteral", o: Access = None):
        """
        Visit nil literal - push null reference.
        """
        if o is None:
            return "", None
        o.frame.push()
        code = self.emit.jvm.emitPUSHNULL()
        return code, None  # Type will be determined by context

    def visit_method_invocation(self, node, o = None):
        pass
    def visit_static_member_access(self, node, o = None):
        pass
    def visit_static_method_invocation(self, node, o = None):
        pass