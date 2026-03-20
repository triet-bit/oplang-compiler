# Generated from OPLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OPLangParser import OPLangParser
else:
    from OPLangParser import OPLangParser

# This class defines a complete generic visitor for a parse tree produced by OPLangParser.

class OPLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OPLangParser#program.
    def visitProgram(self, ctx:OPLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#decllist.
    def visitDecllist(self, ctx:OPLangParser.DecllistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#decl.
    def visitDecl(self, ctx:OPLangParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#classdecl.
    def visitClassdecl(self, ctx:OPLangParser.ClassdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#memberdecl.
    def visitMemberdecl(self, ctx:OPLangParser.MemberdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#memberlist.
    def visitMemberlist(self, ctx:OPLangParser.MemberlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#member.
    def visitMember(self, ctx:OPLangParser.MemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attributedecl.
    def visitAttributedecl(self, ctx:OPLangParser.AttributedeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#static_atom.
    def visitStatic_atom(self, ctx:OPLangParser.Static_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#final_atom.
    def visitFinal_atom(self, ctx:OPLangParser.Final_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ampersand_atom.
    def visitAmpersand_atom(self, ctx:OPLangParser.Ampersand_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attributelist.
    def visitAttributelist(self, ctx:OPLangParser.AttributelistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attributeprime.
    def visitAttributeprime(self, ctx:OPLangParser.AttributeprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#methoddecl.
    def visitMethoddecl(self, ctx:OPLangParser.MethoddeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#return_type_method.
    def visitReturn_type_method(self, ctx:OPLangParser.Return_type_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#vardecllist.
    def visitVardecllist(self, ctx:OPLangParser.VardecllistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#vardecl.
    def visitVardecl(self, ctx:OPLangParser.VardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#paramdecl.
    def visitParamdecl(self, ctx:OPLangParser.ParamdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#paramlist.
    def visitParamlist(self, ctx:OPLangParser.ParamlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#paramprime.
    def visitParamprime(self, ctx:OPLangParser.ParamprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#param.
    def visitParam(self, ctx:OPLangParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#constructordecl.
    def visitConstructordecl(self, ctx:OPLangParser.ConstructordeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#default_contructor.
    def visitDefault_contructor(self, ctx:OPLangParser.Default_contructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#copy_contructor.
    def visitCopy_contructor(self, ctx:OPLangParser.Copy_contructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#userdef_contructor.
    def visitUserdef_contructor(self, ctx:OPLangParser.Userdef_contructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#destructordecl.
    def visitDestructordecl(self, ctx:OPLangParser.DestructordeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#destructor.
    def visitDestructor(self, ctx:OPLangParser.DestructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#blockstmt.
    def visitBlockstmt(self, ctx:OPLangParser.BlockstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#blockstmt_method.
    def visitBlockstmt_method(self, ctx:OPLangParser.Blockstmt_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#vardeclstmt.
    def visitVardeclstmt(self, ctx:OPLangParser.VardeclstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#varlist.
    def visitVarlist(self, ctx:OPLangParser.VarlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#varitem.
    def visitVaritem(self, ctx:OPLangParser.VaritemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#assignlist.
    def visitAssignlist(self, ctx:OPLangParser.AssignlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#stmtlist.
    def visitStmtlist(self, ctx:OPLangParser.StmtlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#stmt.
    def visitStmt(self, ctx:OPLangParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#funct_call.
    def visitFunct_call(self, ctx:OPLangParser.Funct_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#functparam.
    def visitFunctparam(self, ctx:OPLangParser.FunctparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#functprime.
    def visitFunctprime(self, ctx:OPLangParser.FunctprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ifstmt.
    def visitIfstmt(self, ctx:OPLangParser.IfstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#forstmt.
    def visitForstmt(self, ctx:OPLangParser.ForstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#breakstmt.
    def visitBreakstmt(self, ctx:OPLangParser.BreakstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#continuestmt.
    def visitContinuestmt(self, ctx:OPLangParser.ContinuestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#returnstmt.
    def visitReturnstmt(self, ctx:OPLangParser.ReturnstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#assigndecl.
    def visitAssigndecl(self, ctx:OPLangParser.AssigndeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#assignstmt.
    def visitAssignstmt(self, ctx:OPLangParser.AssignstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#lhs.
    def visitLhs(self, ctx:OPLangParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#expr.
    def visitExpr(self, ctx:OPLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#relexpr.
    def visitRelexpr(self, ctx:OPLangParser.RelexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#equalexpr.
    def visitEqualexpr(self, ctx:OPLangParser.EqualexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#logicexpr.
    def visitLogicexpr(self, ctx:OPLangParser.LogicexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#addsubexpr.
    def visitAddsubexpr(self, ctx:OPLangParser.AddsubexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#muldivexpr.
    def visitMuldivexpr(self, ctx:OPLangParser.MuldivexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#expoexpr.
    def visitExpoexpr(self, ctx:OPLangParser.ExpoexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#notexpr.
    def visitNotexpr(self, ctx:OPLangParser.NotexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#unaryexpr.
    def visitUnaryexpr(self, ctx:OPLangParser.UnaryexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#indexingexpr.
    def visitIndexingexpr(self, ctx:OPLangParser.IndexingexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#dotexpr.
    def visitDotexpr(self, ctx:OPLangParser.DotexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#primaryexpr.
    def visitPrimaryexpr(self, ctx:OPLangParser.PrimaryexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#exprlist.
    def visitExprlist(self, ctx:OPLangParser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#exprprime.
    def visitExprprime(self, ctx:OPLangParser.ExprprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#dotchain.
    def visitDotchain(self, ctx:OPLangParser.DotchainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#literal.
    def visitLiteral(self, ctx:OPLangParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#array_lit.
    def visitArray_lit(self, ctx:OPLangParser.Array_litContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#arraylist.
    def visitArraylist(self, ctx:OPLangParser.ArraylistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#arrayprime.
    def visitArrayprime(self, ctx:OPLangParser.ArrayprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#array_element.
    def visitArray_element(self, ctx:OPLangParser.Array_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#idlist.
    def visitIdlist(self, ctx:OPLangParser.IdlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#primitive_type.
    def visitPrimitive_type(self, ctx:OPLangParser.Primitive_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#return_type.
    def visitReturn_type(self, ctx:OPLangParser.Return_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#array_type.
    def visitArray_type(self, ctx:OPLangParser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#decl_type.
    def visitDecl_type(self, ctx:OPLangParser.Decl_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#decl_type2.
    def visitDecl_type2(self, ctx:OPLangParser.Decl_type2Context):
        return self.visitChildren(ctx)



del OPLangParser