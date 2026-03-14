"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):
     # Visit a parse tree produced by OPLangParser#program.
    def visitProgram(self, ctx:OPLangParser.ProgramContext):
        decls = self.visit(ctx.decllist())
        return Program(decls)
    # decllist: decl decllist | ; 
    def visitDecllist(self, ctx: OPLangParser.DecllistContext):
        
        if ctx.getChildCount() == 0:
            return []
        decl = self.visit(ctx.decl())
        rest = self.visit(ctx.decllist())
        return [decl] + (rest if rest else [])
    def visitDecl(self, ctx:OPLangParser.DeclContext): 
        if ctx.classdecl():
            return self.visit(ctx.classdecl())
        else:
            return self.visit(ctx.vardecl())
    # classdecl: CLASS ID (EXTENDS ID)? memberdecl; 
    def visitClassdecl(self, ctx: OPLangParser.ClassdeclContext):
        name = ctx.ID(0).getText()
        members = self.visit(ctx.memberdecl())
        superclass = ctx.ID(1).getText() if ctx.EXTENDS() else None
        return ClassDecl(name, superclass, members)
    
##########################
# MEMBER
# memberdecl: L_CURL memberlist R_CURL; 
# memberlist: member memberlist| ; 
# member: attributedecl | methoddecl | constructordecl | destructordecl; 
##########################
    def visitMemberdecl(self, ctx:OPLangParser.MemberdeclContext):
        return self.visit(ctx.memberlist())
    
    def visitMemberlist(self, ctx:OPLangParser.MemberlistContext):
        if ctx.getChildCount() == 0 : 
            return []
        return [self.visit(ctx.member())] + self.visit(ctx.memberlist())
    
    def visitMember(self, ctx:OPLangParser.MemberContext):
        if ctx.attributedecl():
            return self.visit(ctx.attributedecl())
        elif ctx.methoddecl():
            return self.visit(ctx.methoddecl())
        elif ctx.constructordecl():
            return self.visit(ctx.constructordecl())
        else:
            return self.visit(ctx.destructordecl())

    def visitStatic_atom(self, ctx:OPLangParser.Static_atomContext):
        return ctx.STATIC() is not None
    
    def visitFinal_atom(self, ctx:OPLangParser.Final_atomContext):
        return ctx.FINAL() is not None
    
    # ampersand_atom: AMPERSAND |; 
    def visitAmpersand_atom(self, ctx:OPLangParser.Ampersand_atomContext):
        return ctx.AMPERSAND() is not None
    # if has return true else return false

    def visitAttributedecl(self, ctx:OPLangParser.AttributedeclContext):
        isStatic = self.visit(ctx.static_atom())
        isFinal = self.visit(ctx.final_atom())
        decl_type2 = self.visit(ctx.decl_type2())
        attributes = self.visit(ctx.attributelist())
        return AttributeDecl(
            is_static= isStatic, 
            is_final= isFinal, 
            attr_type= decl_type2, 
            attributes= attributes
        )
    def visitAttributelist(self, ctx:OPLangParser.AttributelistContext):

        if ctx.COMMA(): 
            return [self.visit(ctx.attributeprime())] + self.visit(ctx.attributelist())
        return [self.visit(ctx.attributeprime())]
#attributeprime:  ID | ID ASSIGN expr; 

    def visitAttributeprime(self, ctx:OPLangParser.AttributeprimeContext):
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.ASSIGN() else None
        return Attribute(name, init_value)

##########################
# METHOD
# methoddecl: static_atom return_type_method ID paramdecl blockstmt_method;    
# return_type_method : return_type ampersand_atom; 
##########################
    def visitMethoddecl(self, ctx:OPLangParser.MethoddeclContext):
        hasStatic = self.visit(ctx.static_atom())
        return_typ = self.visit(ctx.return_type_method())
        id = ctx.ID().getText()
        params= self.visit(ctx.paramdecl())
        blockstmt = self.visit(ctx.blockstmt_method())
        return MethodDecl(
            is_static=hasStatic, 
            return_type=return_typ, 
            name= id, 
            params= params, 
            body= blockstmt
        )
    # Coi lai
    def visitReturn_type_method(self, ctx:OPLangParser.Return_type_methodContext):
        return self.visit(ctx.return_type())
                

##########################
# PARAM
# paramdecl: L_PAREN paramlist R_PAREN; 
# paramlist: paramprime |; 
# paramprime: param SEMI paramprime| param; 
# param: decl_type ampersand_atom idlist;
##########################
    def visitParamdecl(self, ctx:OPLangParser.ParamdeclContext):
        return self.visit(ctx.paramlist())


    # Visit a parse tree produced by OPLangParser#paramlist.
    def visitParamlist(self, ctx:OPLangParser.ParamlistContext):
        if ctx.getChildCount() == 0: 
            return []
        return self.visit(ctx.paramprime())

    def visitParamprime(self, ctx:OPLangParser.ParamprimeContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.param())
        return self.visit(ctx.param()) + self.visit(ctx.paramprime())


    def visitParam(self, ctx:OPLangParser.ParamContext):
        # Get base type from decl_type2 (already handles ampersand internally)
        base_type = self.visit(ctx.decl_type2())
        
        if base_type is None:
            raise Exception("Parameter must have a type")
        
        # Check for additional ampersand after decl_type2
        has_ampersand = self.visit(ctx.ampersand_atom())
        if has_ampersand and not isinstance(base_type, ReferenceType):
            base_type = ReferenceType(base_type)
        
        # Get parameter names
        idlist = self.visit(ctx.idlist())
        param_names = [var.name for var in idlist]
        
        # Create parameters with the same type
        return [Parameter(base_type, name) for name in param_names]
##########################
# CONSTRUCTOR
# constructordecl: default_contructor | copy_contructor | userdef_contructor; 
# default_contructor: ID L_PAREN R_PAREN blockstmt;  
# copy_contructor: ID L_PAREN ID ID R_PAREN blockstmt; 
# userdef_contructor: ID paramdecl blockstmt; 
# destructordecl: destructor; 
# destructor: TILDE ID L_PAREN R_PAREN blockstmt; 
##########################

    def visitConstructordecl(self, ctx:OPLangParser.ConstructordeclContext):
        if ctx.default_contructor(): 
            return self.visit(ctx.default_contructor())
        elif ctx.copy_contructor(): 
            return self.visit(ctx.copy_contructor())
        else: 
            return self.visit(ctx.userdef_contructor())

    def visitDefault_contructor(self, ctx:OPLangParser.Default_contructorContext):
        params = []
        name = ctx.ID().getText()
        blockstmt = self.visit(ctx.blockstmt())
        return ConstructorDecl(
            params= params, 
            name=name, 
            body = blockstmt
        )
    
    def visitCopy_contructor(self, ctx:OPLangParser.Copy_contructorContext):
        name = ctx.ID(0).getText()
        type_name = ctx.ID(1).getText()
        param_name = ctx.ID(2).getText()
        param_type = ClassType(type_name)
        body = self.visit(ctx.blockstmt())
        return ConstructorDecl(name, [Parameter(param_type, param_name)], body)

    def visitUserdef_contructor(self, ctx:OPLangParser.Userdef_contructorContext):
        paramdecl = self.visit(ctx.paramdecl())
        blockstmt = self.visit(ctx.blockstmt())
        name = ctx.ID().getText()
        return ConstructorDecl(
            params= paramdecl, 
            name=name, 
            body=blockstmt
        )

    # Visit a parse tree produced by OPLangParser#destructordecl.
    def visitDestructordecl(self, ctx:OPLangParser.DestructordeclContext):
        return self.visit(ctx.destructor())


    # Visit a parse tree produced by OPLangParser#destructor.
    def visitDestructor(self, ctx:OPLangParser.DestructorContext):
        name = ctx.ID().getText()
        blockstmt = self.visit(ctx.blockstmt())
        return DestructorDecl(name=name, body=blockstmt)


##########################
# BLOCK
# blockstmt: L_CURL vardecllist stmtlist R_CURL; 
# blockstmt_method: L_CURL vardecllist stmtlist R_CURL; 
########################## check kix laij 2 casse nayf 
    def visitBlockstmt(self, ctx:OPLangParser.BlockstmtContext):
        vardecls = self.visit(ctx.vardecllist())
        stmt = self.visit(ctx.stmtlist())
        if isinstance(ctx.stmtlist(),list): 
            vars_in_stmt = [s for s in ctx.stmtlist() if isinstance(s,VariableDecl)]
            stmt = [s for s in ctx.stmtlist() if not isinstance(s,VariableDecl)]
            vardecls = (vardecls or []) + vars_in_stmt
        return BlockStatement(vardecls if vardecls else [], stmt if stmt else [])

    #blockstmt_method: L_CURL vardecllist stmtlist R_CURL; 

    def visitBlockstmt_method(self, ctx:OPLangParser.Blockstmt_methodContext):
        stmtlist = self.visit(ctx.stmtlist())
        vardecls = self.visit(ctx.vardecllist())

        # Tách vardeclstmt trong stmtlist ra thành vars
        vars_in_stmt = [s for s in stmtlist if isinstance(s, VariableDecl)]
        stmts = [s for s in stmtlist if not isinstance(s, VariableDecl)]

        all_vars = (vardecls or []) + vars_in_stmt

        return BlockStatement(all_vars, stmts)
# vardeclstmt:  decl_type2 idlist SEMI
#              | decl_type2 idlist ASSIGN expr SEMI
#              | decl_type2 assignlist SEMI; 
#  assignlist: ID ASSIGN expr COMMA assignlist| ID ASSIGN expr; 
#vardeclstmt cos dc cos final hay khoong, khai bao trong ham co final hay khong 
    def visitVardeclstmt(self, ctx:OPLangParser.VardeclstmtContext):
        decl_type = self.visit(ctx.decl_type2())
        isFinal = False
        variables = self.visit(ctx.varlist())
        return VariableDecl(
                is_final=isFinal, 
                var_type=decl_type, 
                variables=variables  
            )
    def visitAssignlist(self, ctx:OPLangParser.AssignlistContext):
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        if ctx.COMMA():
            rest = self.visit(ctx.assignlist())
            return [(name, expr)] + rest
        return [(name, expr)]
##########################
# VARDECL
# vardecllist: vardecl vardecllist|;
# vardecl: (FINAL)? decl_type ampersand_atom (idlist | idlist ASSIGN expr) SEMI;
##########################
    def visitVardecllist(self, ctx:OPLangParser.VardecllistContext):
        if ctx.getChildCount() == 0:
            return []
        var_decl = self.visit(ctx.vardecl())
        rest = self.visit(ctx.vardecllist())
        return [var_decl] + (rest if rest else [])

    def visitVarlist(self, ctx:OPLangParser.VarlistContext):
        if ctx.COMMA():
            return [self.visit(ctx.varitem())] + self.visit(ctx.varlist())
        return [self.visit(ctx.varitem())]

    def visitVaritem(self, ctx:OPLangParser.VaritemContext):
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.ASSIGN() else None
        return Variable(name, init_value)

    def visitVardecl(self, ctx:OPLangParser.VardeclContext):
        hasFinal = ctx.FINAL() is not None
        base_type = self.visit(ctx.decl_type())
        hasAmper = self.visit(ctx.ampersand_atom())
        if hasAmper: 
            base_type = ReferenceType(base_type)
        
        variables = self.visit(ctx.varlist())
        
        return VariableDecl(
            is_final=hasFinal, 
            var_type=base_type, 
            variables=variables
        )
##########################
#stmtlist
# stmtlist: stmt stmtlist |; 
# stmt
#     : blockstmt                      // { ... }
#     | ifstmt                         // if ... then ... (else ...)
#     | forstmt                        // nested for
#     | breakstmt                      // break;
#     | continuestmt
#     | vardeclstmt
#     | ID L_PAREN expr R_PAREN SEMI #
#     | returnstmt
#     | assignstmt               // ID := ... ;
#     | expr SEMI                      // expression statement, ví dụ function call ;
#     | SEMI                           // empty statement allowed
#     ;
##########################
    def visitStmtlist(self, ctx:OPLangParser.StmtlistContext):
        if ctx.getChildCount() == 0:  # epsilon
            return []
        stmt = self.visit(ctx.stmt())
        rest = self.visit(ctx.stmtlist())
        return [stmt] + (rest if rest else [])

    # Visit a parse tree produced by OPLangParser#stmt.
    def visitStmt(self, ctx: OPLangParser.StmtContext):
        if ctx.blockstmt():
            return self.visit(ctx.blockstmt())
        elif ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        elif ctx.forstmt():
            return self.visit(ctx.forstmt())
        elif ctx.breakstmt():
            return self.visit(ctx.breakstmt())
        elif ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        elif ctx.ID() and ctx.L_PAREN() and ctx.expr():
            # Function call statement: ID(expr);
            func_name = ctx.ID().getText()
            args = [self.visit(ctx.expr())]
            id_expr = Identifier(func_name)
            method_call = PostfixExpression(id_expr, [MethodCall(func_name, args)])
            return MethodInvocationStatement(method_call)
        elif ctx.assignstmt():
            check = self.visit(ctx.assignstmt())
            return check
        elif ctx.vardeclstmt():
            return self.visit(ctx.vardeclstmt())
        elif ctx.returnstmt():
            return self.visit(ctx.returnstmt())
        elif ctx.expr(): 
            expr_result = self.visit(ctx.expr())
            # If it's already a PostfixExpression, wrap it in MethodInvocationStatement
            if isinstance(expr_result, PostfixExpression):
                return MethodInvocationStatement(expr_result)
            return expr_result
        elif ctx.SEMI():
            return NilLiteral()
        else: 
            return NilLiteral()
    # Visit a parse tree produced by OPLangParser#funct_call.
    def visitFunct_call(self, ctx:OPLangParser.Funct_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#functparam.
    def visitFunctparam(self, ctx:OPLangParser.FunctparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#functprime.
    def visitFunctprime(self, ctx:OPLangParser.FunctprimeContext):
        return self.visitChildren(ctx)


#ifstmt: IF expr THEN stmt (ELSE stmt)?; 
    def visitIfstmt(self, ctx:OPLangParser.IfstmtContext):
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        return IfStatement(condition, then_stmt, else_stmt)

# forstmt: FOR ID ASSIGN expr (TO | DOWNTO) expr DO stmt;
    def visitForstmt(self, ctx:OPLangParser.ForstmtContext):
        var = ctx.ID().getText()
        start_expr = self.visit(ctx.expr(0))
        direction = ctx.getChild(4).getText()
        end_expr = self.visit(ctx.expr(1))
        body = self.visit(ctx.stmt())
        return ForStatement(
            variable=var, 
            start_expr=start_expr, 
            direction=direction,
            end_expr=end_expr, 
            body=body
        )

    # Visit a parse tree produced by OPLangParser#breakstmt.
    def visitBreakstmt(self, ctx:OPLangParser.BreakstmtContext):
        return BreakStatement()


    # Visit a parse tree produced by OPLangParser#continuestmt.
    def visitContinuestmt(self, ctx:OPLangParser.ContinuestmtContext):
        return ContinueStatement()


#returnstmt: RETURN ID SEMI | RETURN SEMI | RETURN expr SEMI; 
    def visitReturnstmt(self, ctx:OPLangParser.ReturnstmtContext):
        if ctx.expr(): 
            value = self.visit(ctx.expr())
        elif ctx.ID(): 
            value = Identifier(ctx.ID().getText())
        else: 
            value = NilLiteral()
        return ReturnStatement(value=value)

##########################
# BLOCK
# assigndecl: assignstmt assigndecl | assignstmt; 
# assignstmt: lhs ASSIGN expr SEMI; 
# lhs: ID                              // biến thường
#    | expr                  // arr[0], obj.field[2], ...
#    | THIS DOT ID;    
##########################
    def visitAssignstmt(self, ctx:OPLangParser.AssignstmtContext):
        lhs = self.visit(ctx.lhs())
        expr = self.visit(ctx.expr())
        return AssignmentStatement(lhs=lhs, rhs=expr)

    def visitLhs(self, ctx: OPLangParser.LhsContext):
        if ctx.THIS():
            this_expr = ThisExpression()
            member_access = MemberAccess(ctx.ID().getText())
            postfix_expr = PostfixExpression(this_expr, [member_access])
            return PostfixLHS(postfix_expr)
        elif ctx.ID():
            return IdLHS(ctx.ID().getText())
        else: 
            expr = self.visit(ctx.expr())
            if isinstance(expr, PostfixExpression):
                return PostfixLHS(expr)
            elif isinstance(expr, Identifier):
                return IdLHS(expr.name)
            return PostfixLHS(expr)
    # Visit a parse tree produced by OPLangParser#expr.
    def visitExpr(self, ctx:OPLangParser.ExprContext):
        check = self.visit(ctx.relexpr())
        return check
# expr : relexpr; 

# primaryexpr: literal
#            | ID                                           
#            | THIS                                           
#            | NEW ID L_PAREN exprlist R_PAREN               
#            | L_PAREN expr R_PAREN                      
#            | NIL
#            | ID L_PAREN exprlist R_PAREN
#            | ID L_SQUARE INT_LIT R_SQUARE
#            ;
# exprlist: exprprime | ; 
# exprprime: expr COMMA exprprime | expr; 
# dotchain
#     : DOT ID L_PAREN exprlist R_PAREN dotchain   // method call chaining
#     | DOT ID dotchain                            // field access chaining 
#     |
#     ;

# relexpr: equalexpr (GREATER|GREATER_EQ|LESS|LESS_EQ) equalexpr|equalexpr; 
    def visitRelexpr(self, ctx:OPLangParser.RelexprContext):
        left = self.visit(ctx.equalexpr(0))
        if ctx.getChildCount() > 1:
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.equalexpr(1))
            return BinaryOp(left, operator, right)
        return left
 
    def visitEqualexpr(self, ctx:OPLangParser.EqualexprContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.logicexpr(0))
        left = self.visit(ctx.logicexpr(0))
        right = self.visit(ctx.logicexpr(1))
        op = ctx.getChild(1).getText()
        return BinaryOp(
            left=left, 
            right=right,
            operator=op
        )
# logicexpr: logicexpr (LOGIC_AND| LOGIC_OR) addsubexpr | addsubexpr; 
    def visitLogicexpr(self, ctx:OPLangParser.LogicexprContext):
        if ctx.getChildCount() == 1: 
            check= self.visit(ctx.addsubexpr())
            return check
        left = self.visit(ctx.logicexpr())
        right = self.visit(ctx.addsubexpr())
        op = ctx.getChild(1).getText()
        return BinaryOp(
            left=left, 
            right=right,
            operator=op
        )
# addsubexpr: addsubexpr (ADD|SUB) muldivexpr | muldivexpr; 
    def visitAddsubexpr(self, ctx:OPLangParser.AddsubexprContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.muldivexpr())
        left = self.visit(ctx.addsubexpr())
        right = self.visit(ctx.muldivexpr())
        op = ctx.getChild(1).getText()
        return BinaryOp(
            left=left, 
            right=right,
            operator=op
        )
# muldivexpr: muldivexpr (MUL|FLT_DIV|INT_DIV|MOD) expoexpr | expoexpr; 
    def visitMuldivexpr(self, ctx:OPLangParser.MuldivexprContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.expoexpr())
        left = self.visit(ctx.muldivexpr())
        right = self.visit(ctx.expoexpr())
        op = ctx.getChild(1).getText()
        return BinaryOp(
            left=left, 
            right=right,
            operator=op
        )
# expoexpr: expoexpr CONCAT notexpr | notexpr; 
    def visitExpoexpr(self, ctx:OPLangParser.ExpoexprContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.notexpr())
        left = self.visit(ctx.expoexpr())
        right = self.visit(ctx.notexpr())
        op = ctx.getChild(1).getText()
        return BinaryOp(
            left=left, 
            right=right,
            operator=op
        )
# notexpr: (LOGIC_NOT) notexpr | unaryexpr; 
    def visitNotexpr(self, ctx:OPLangParser.NotexprContext):
        if ctx.getChildCount() == 1: 
            check = self.visit(ctx.unaryexpr())
            return check
        right = self.visit(ctx.notexpr())
        op = ctx.LOGIC_NOT().getText()
        return UnaryOp(
            operator =  op, 
            operand= right
        )
# unaryexpr: (ADD|SUB) unaryexpr | indexingexpr; 
    def visitUnaryexpr(self, ctx:OPLangParser.UnaryexprContext):
        if ctx.getChildCount() == 1: 
            return self.visit(ctx.indexingexpr())
        right = self.visit(ctx.unaryexpr())
        op = ctx.getChild(0).getText()
        return UnaryOp(
            operator =  op, 
            operand= right
        )

    def visitIndexingexpr(self, ctx: OPLangParser.IndexingexprContext):
        if ctx.dotexpr():
            return self.visit(ctx.dotexpr())
        
        base = self.visit(ctx.indexingexpr())
        index_expr = self.visit(ctx.expr())
        result = PostfixExpression(base, [ArrayAccess(index_expr)])
        
        if ctx.dotchain():
            chain = self.visit(ctx.dotchain())
            for op in chain:
                result = PostfixExpression(result, [op])
        
        return result
# dotexpr: primaryexpr dotchain                                       
#        | primaryexpr;
    def visitDotexpr(self, ctx:OPLangParser.DotexprContext):
        """Visit dotexpr rule: primaryexpr dotchain | primaryexpr"""
        primary = self.visit(ctx.primaryexpr())
        if ctx.dotchain():
            chain = self.visit(ctx.dotchain())
            if chain:
                result = primary
                for op in chain: 
                    result = PostfixExpression(result,[op])
                return result
        return primary
 
# primaryexpr: literal
#            | ID                                           
#            | THIS                                           
#            | NEW ID L_PAREN exprlist R_PAREN               
#            | L_PAREN expr R_PAREN                      
#            | NIL
#            | ID L_PAREN exprlist R_PAREN
#            | ID L_SQUARE INT_LIT R_SQUARE
#            ;
    def visitPrimaryexpr(self, ctx:OPLangParser.PrimaryexprContext):
            if ctx.literal():
                return self.visit(ctx.literal())
            elif ctx.NEW(): 
                class_name = ctx.ID().getText()
                args = self.visit(ctx.exprlist())
                return ObjectCreation(class_name, args if args else [])
            elif ctx.THIS(): 
                return ThisExpression()
            elif ctx.NIL(): 
                return NilLiteral()
            elif ctx.L_PAREN() and ctx.expr(): 
                # Parenthesized expression
                paren = self.visit(ctx.expr())
                return ParenthesizedExpression(paren)
            elif ctx.L_SQUARE():
                # Array type declaration: ID[INT_LIT]
                name = Identifier(ctx.ID().getText())
                size = IntLiteral(int(ctx.INT_LIT().getText()))
                return PostfixExpression(name, [ArrayAccess(size)])
                # name = Identifier(ctx.ID().getText())
                # size_list = [[IntLiteral(a)] for a in int(ctx.INT_LIT().getText())]
                # result = PostfixExpression(name,size_list[0])
                # for i in range(1,len(size_list)):
                #     result = PostfixExpression(result,size_list[i])
                # return result
            elif ctx.exprlist():
                # Function call: ID(exprlist)
                func_name = ctx.ID().getText()
                args = self.visit(ctx.exprlist())
                id_expr = Identifier(func_name)
                return PostfixExpression(id_expr, [MethodCall(func_name, args if args else [])])
            else:
                return Identifier(ctx.ID().getText())

# exprlist: exprprime | ; 
# exprprime: expr COMMA exprprime | expr; 
# dotchain
#     : DOT ID L_PAREN exprlist R_PAREN dotchain   // method call chaining
#     | DOT ID dotchain                            // field access chaining 
#     |
#     ;
    def visitExprlist(self, ctx:OPLangParser.ExprlistContext):
        if ctx.exprprime(): 
            return self.visit(ctx.exprprime())
        return []

    def visitExprprime(self, ctx:OPLangParser.ExprprimeContext):
        if ctx.getChildCount() == 1: 
            return [self.visit(ctx.expr())]
        return [self.visit(ctx.expr())] + self.visit(ctx.exprprime())
# dotchain
#     : DOT ID L_PAREN exprlist R_PAREN dotchain   // method call chaining
#     | DOT ID dotchain                            // field access chaining 
#     |
#     ;    
    def visitDotchain(self, ctx:OPLangParser.DotchainContext):
        if ctx.getChildCount() == 0: 
            return []  # Empty chain
        
        if ctx.L_PAREN():  # Method call
            name = ctx.ID().getText()
            args = self.visit(ctx.exprlist()) if ctx.exprlist() else []
            rest = self.visit(ctx.dotchain()) if ctx.dotchain() else []

            return [MethodCall(name, args)] + rest
        else:  # Field access
            name = ctx.ID().getText()
            rest = self.visit(ctx.dotchain()) if ctx.dotchain() else []
            return [MemberAccess(name)] + rest
    # literal: INT_LIT | FLT_LIT | TRUE | FALSE | STR_LIT | array_lit; 
    def visitLiteral(self, ctx:OPLangParser.LiteralContext):
        if ctx.INT_LIT(): 
            value = int(ctx.INT_LIT().getText())
            return IntLiteral(value)
        elif ctx.FLT_LIT(): 
            value = float(ctx.FLT_LIT().getText())
            return FloatLiteral(value)
        elif ctx.TRUE(): 
            return  BoolLiteral(True)
        elif ctx.FALSE(): 
            return BoolLiteral(False)
        elif ctx.STR_LIT():
            value = ctx.STR_LIT().getText()
            return StringLiteral(value)
        else:
            value = self.visit(ctx.array_lit())
            return ArrayLiteral(value) 
# array_lit: L_CURL arraylist R_CURL; 
# arraylist: arrayprime | ; 
# arrayprime: array_element COMMA arrayprime | array_element; 
# array_element: TRUE | FALSE | INT_LIT | FLT_LIT | STR_LIT; 
    def visitArray_lit(self, ctx:OPLangParser.Array_litContext): # -> list of expr
        return self.visit(ctx.arraylist())

    def visitArraylist(self, ctx:OPLangParser.ArraylistContext):
        if ctx.arrayprime(): 
            return self.visit(ctx.arrayprime())
        return []

    def visitArrayprime(self, ctx:OPLangParser.ArrayprimeContext):
        element = self.visitArray_element(ctx.array_element())
        if ctx.COMMA():  
            rest_elements = self.visitArrayprime(ctx.arrayprime())
            return [element] + rest_elements
        else: 
            return [element]
        
    def visitArray_element(self, ctx:OPLangParser.Array_elementContext):
        return self.visit(ctx.expr())
    #idlist: ID COMMA idlist | ID; 
    def visitIdlist(self, ctx: OPLangParser.IdlistContext):
        if ctx.COMMA():
            return [Variable(ctx.ID().getText())] + self.visit(ctx.idlist())
        else:
            return [Variable(ctx.ID().getText())]

    def visitPrimitive_type(self, ctx:OPLangParser.Primitive_typeContext):
        if ctx.INT(): 
            return PrimitiveType("int")
        elif ctx.BOOL(): 
            return PrimitiveType("boolean")
        elif ctx.STR(): 
            return PrimitiveType("string")
        else: 
            return PrimitiveType("float")
 
#return_type:(primitive_type ampersand_atom)|VOID | array_type ampersand_atom | (ID ampersand_atom) ; 
    def visitReturn_type(self, ctx:OPLangParser.Return_typeContext):
        if ctx.VOID(): 
            return PrimitiveType("void")
        elif ctx.array_type(): 
            typ =  self.visit(ctx.array_type())
            hasAmpersand = self.visit(ctx.ampersand_atom())
            return ReferenceType(typ) if hasAmpersand else typ
        elif ctx.primitive_type(): 
            hasAmpersand = self.visit(ctx.ampersand_atom())
            base_typ = self.visit(ctx.primitive_type())
            if hasAmpersand: 
                return ReferenceType(base_typ)
            else:
                return base_typ
        elif ctx.ID(): 
            hasAmpersand = self.visit(ctx.ampersand_atom())
            typ =ClassType(ctx.ID().getText())
            if hasAmpersand: 
                return ReferenceType(typ)
            else: 
                return typ
    #array_type: (primitive_type|ID) L_SQUARE INT_LIT R_SQUARE ; // cos theer cos class
    def visitArray_type(self, ctx: OPLangParser.Array_typeContext):
        size = int(ctx.INT_LIT().getText())
        if ctx.ID():
            typ = ClassType(ctx.ID().getText())
        else:
            typ = self.visit(ctx.primitive_type())
        return ArrayType(typ, size)
#decl_type: primitive_type | array_type | ID; //ID for class, not have void type

    def visitDecl_type(self, ctx:OPLangParser.Decl_typeContext):
        if ctx.array_type(): 
            return self.visit(ctx.array_type())
        elif ctx.primitive_type(): 
            return self.visit(ctx.primitive_type())
        elif ctx.ID(): 
            return ClassType(ctx.ID().getText())

    #decl_type2: ( primitive_type ampersand_atom) | array_type | (ID ampersand_atom) |;
    def visitDecl_type2(self, ctx:OPLangParser.Decl_type2Context):
        if ctx.getChildCount() == 0:  # epsilon
            return None
        
        if ctx.array_type():
            is_ref = self.visit(ctx.ampersand_atom())
            array_type = self.visit(ctx.array_type())
            return ReferenceType(array_type) if is_ref else array_type
        elif ctx.primitive_type():
            prim_type = self.visit(ctx.primitive_type())
            is_ref = self.visit(ctx.ampersand_atom())
            if is_ref:
                return ReferenceType(prim_type)
            return prim_type
        else:
            # ID ampersand_atom
            class_type = ClassType(ctx.ID().getText())
            is_ref = self.visit(ctx.ampersand_atom())
            if is_ref:
                return ReferenceType(class_type)
            return class_type


