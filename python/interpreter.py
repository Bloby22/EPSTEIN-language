"""
EPSTEIN Language Interpreter - Executes AST
"""

from __future__ import annotations
import sys
from typing import Any, Dict, List, Optional
from python.parser import *
from python.runtime import get_runtime_globals


class BreakException(Exception):
    """Exception for break/escape statement"""
    pass


class ReturnException(Exception):
    """Exception for return/suicide statement"""
    def __init__(self, value: Any = None):
        self.value = value
        super().__init__()


class Interpreter:
    """Interpreter for EPSTEIN language"""
    
    def __init__(self):
        self.globals = get_runtime_globals()
        self.locals_stack: List[Dict[str, Any]] = [{}]
    
    def error(self, msg: str):
        raise RuntimeError(f"EPSTEIN Runtime Error: {msg}")
    
    @property
    def current_scope(self) -> Dict[str, Any]:
        """Get current local scope"""
        return self.locals_stack[-1]
    
    def get_variable(self, name: str) -> Any:
        """Get variable value from scope chain"""
        # Check local scopes (reverse order)
        for scope in reversed(self.locals_stack):
            if name in scope:
                return scope[name]
        
        # Check globals
        if name in self.globals:
            return self.globals[name]
        
        self.error(f"Undefined variable: {name}")
    
    def set_variable(self, name: str, value: Any):
        """Set variable in current scope"""
        self.current_scope[name] = value
    
    def push_scope(self):
        """Enter new scope"""
        self.locals_stack.append({})
    
    def pop_scope(self):
        """Exit scope"""
        if len(self.locals_stack) > 1:
            self.locals_stack.pop()
    
    def execute(self, program: Program) -> None:
        """Execute program"""
        try:
            for statement in program.statements:
                self.eval_node(statement)
        except ReturnException as e:
            # Top-level return/suicide
            if e.value is not None:
                sys.exit(int(e.value) if isinstance(e.value, (int, float)) else 0)
            sys.exit(0)
        except BreakException:
            self.error("'escape' outside loop")
    
    def eval_node(self, node: ASTNode) -> Any:
        """Evaluate AST node"""
        
        # Literals
        if isinstance(node, Number):
            return node.value
        
        if isinstance(node, String):
            return node.value
        
        if isinstance(node, Boolean):
            return node.value
        
        if isinstance(node, Null):
            return None
        
        # Identifier
        if isinstance(node, Identifier):
            return self.get_variable(node.name)
        
        # List
        if isinstance(node, List):
            return [self.eval_node(elem) for elem in node.elements]
        
        # Dict
        if isinstance(node, Dict):
            result = {}
            for key_node, value_node in node.pairs:
                key = self.eval_node(key_node)
                value = self.eval_node(value_node)
                result[key] = value
            return result
        
        # Binary operations
        if isinstance(node, BinaryOp):
            return self.eval_binary_op(node)
        
        # Unary operations
        if isinstance(node, UnaryOp):
            return self.eval_unary_op(node)
        
        # Assignment
        if isinstance(node, Assignment):
            value = self.eval_node(node.value)
            self.set_variable(node.name, value)
            return value
        
        # Function call
        if isinstance(node, FunctionCall):
            return self.eval_function_call(node)
        
        # Function definition
        if isinstance(node, FunctionDef):
            self.eval_function_def(node)
            return None
        
        # If statement
        if isinstance(node, IfStatement):
            self.eval_if_statement(node)
            return None
        
        # Loop statement
        if isinstance(node, LoopStatement):
            self.eval_loop(node)
            return None
        
        # Return statement
        if isinstance(node, ReturnStatement):
            value = None
            if node.value:
                value = self.eval_node(node.value)
            raise ReturnException(value)
        
        # Break statement
        if isinstance(node, BreakStatement):
            raise BreakException()
        
        self.error(f"Unknown node type: {type(node).__name__}")
    
    def eval_binary_op(self, node: BinaryOp) -> Any:
        """Evaluate binary operation"""
        left = self.eval_node(node.left)
        
        # Short-circuit evaluation for logical operators
        if node.op == 'and':
            if not left:
                return False
            return bool(self.eval_node(node.right))
        
        if node.op == 'or':
            if left:
                return True
            return bool(self.eval_node(node.right))
        
        right = self.eval_node(node.right)
        
        # Arithmetic
        if node.op == '+':
            return left + right
        if node.op == '-':
            return left - right
        if node.op == '*':
            return left * right
        if node.op == '/':
            if right == 0:
                self.error("Division by zero")
            return left / right
        if node.op == '%':
            return left % right
        
        # Comparison
        if node.op == '==':
            return left == right
        if node.op == '!=':
            return left != right
        if node.op == '<':
            return left < right
        if node.op == '>':
            return left > right
        if node.op == '<=':
            return left <= right
        if node.op == '>=':
            return left >= right
        
        self.error(f"Unknown binary operator: {node.op}")
    
    def eval_unary_op(self, node: UnaryOp) -> Any:
        """Evaluate unary operation"""
        operand = self.eval_node(node.operand)
        
        if node.op == '-':
            return -operand
        
        if node.op == 'not':
            return not operand
        
        self.error(f"Unknown unary operator: {node.op}")
    
    def eval_function_call(self, node: FunctionCall) -> Any:
        """Evaluate function call"""
        # Evaluate arguments
        args = [self.eval_node(arg) for arg in node.args]
        
        # Get function
        func = self.get_variable(node.name)
        
        # Check if it's a user-defined function
        if isinstance(func, tuple) and len(func) == 2:
            params, body = func
            
            # Create new scope
            self.push_scope()
            
            # Bind parameters
            if len(args) != len(params):
                self.error(f"Function {node.name} expects {len(params)} arguments, got {len(args)}")
            
            for param, arg in zip(params, args):
                self.set_variable(param, arg)
            
            # Execute body
            result = None
            try:
                for stmt in body:
                    self.eval_node(stmt)
            except ReturnException as e:
                result = e.value
            finally:
                self.pop_scope()
            
            return result
        
        # Built-in or Python function
        if callable(func):
            try:
                return func(*args)
            except Exception as e:
                self.error(f"Error calling {node.name}: {e}")
        
        self.error(f"{node.name} is not callable")
    
    def eval_function_def(self, node: FunctionDef):
        """Define a function"""
        # Store as tuple of (params, body)
        self.set_variable(node.name, (node.params, node.body))
    
    def eval_if_statement(self, node: IfStatement):
        """Evaluate if statement"""
        condition = self.eval_node(node.condition)
        
        if condition:
            for stmt in node.then_body:
                self.eval_node(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.eval_node(stmt)
    
    def eval_loop(self, node: LoopStatement):
        """Evaluate loop statement"""
        collection = self.eval_node(node.collection)
        
        # Ensure it's iterable
        if not hasattr(collection, '__iter__'):
            self.error(f"Cannot loop over non-iterable: {type(collection).__name__}")
        
        # Create new scope for loop
        self.push_scope()
        
        try:
            for item in collection:
                # Set the implicit 'item' variable
                self.set_variable('item', item)
                
                # Execute body
                try:
                    for stmt in node.body:
                        self.eval_node(stmt)
                except BreakException:
                    break
        finally:
            self.pop_scope()
