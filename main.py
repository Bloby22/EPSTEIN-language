#!/usr/bin/env python3
"""
EPSTEIN Programming Language Interpreter
A conspiracy-themed programming language with custom syntax

Usage:
    python epstein.py <file.epc>
    python epstein.py --help
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from python.lexer import Lexer
from python.parser import Parser
from python.interpreter import Interpreter


BANNER = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ███████╗██████╗ ███████╗████████╗███████╗██╗███╗   ██╗ ║
║   ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║████╗  ██║ ║
║   █████╗  ██████╔╝███████╗   ██║   █████╗  ██║██╔██╗ ██║ ║
║   ██╔══╝  ██╔═══╝ ╚════██║   ██║   ██╔══╝  ██║██║╚██╗██║ ║
║   ███████╗██║     ███████║   ██║   ███████╗██║██║ ╚████║ ║
║   ╚══════╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝ ║
║                                                          ║
║        Programming Language v1.0.0                       ║
║        Conspiracy-Themed Interpreted Language            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
EPSTEIN Programming Language

Usage:
    epstein <file.epc>              Execute an EPSTEIN program
    epstein --help                  Show this help message
    epstein --version               Show version information

Examples:
    epstein examples/mission.epc
    epstein my_program.epc

EPSTEIN Syntax Quick Reference:

Variables:
    deal = "Classified"
    power = 9000
    truth = truth
    lie = lie

Output:
    files("Mission started")
    files(deal)

Arrays:
    crew = ["Alice", "Bob", "Charlie"]

Conditionals:
    if truth:
        files("Authenticated")
    else:
        files("Denied")

Loops:
    loop crew:
        files(item)

Functions:
    plot infiltration():
        files("Entering base")
    
    plan extraction():
        files("Collecting data")

For more information, see README.md
"""


class EpsteinCLI:
    """Command-line interface for EPSTEIN"""
    
    def __init__(self):
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    def run(self, args: list):
        """Run CLI with arguments"""
        
        if len(args) == 0:
            self.show_usage()
            return
        
        command = args[0]
        
        # Handle flags
        if command in ('--help', '-h', 'help'):
            self.show_help()
            return
        
        if command in ('--version', '-v', 'version'):
            self.show_version()
            return
        
        # Execute file
        if command.endswith('.epc'):
            self.execute_file(command)
        else:
            print(f"❌ Error: Unknown command or invalid file: {command}")
            print(f"   EPSTEIN files must have .epc extension")
            print()
            self.show_usage()
            sys.exit(1)
    
    def execute_file(self, filepath: str):
        """Execute an EPSTEIN program file"""
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                print(f"❌ Error: File not found: {filepath}")
                sys.exit(1)
            
            # Read source code
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Show banner
            print(BANNER)
            print(f"📁 Executing: {os.path.basename(filepath)}")
            print('━' * 63)
            print()
            
            # Lex
            if self.debug:
                print("=== LEXING ===")
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            if self.debug:
                print(f"Generated {len(tokens)} tokens")
                for token in tokens[:20]:  # Show first 20
                    print(f"  {token}")
                if len(tokens) > 20:
                    print(f"  ... and {len(tokens) - 20} more")
                print()
            
            # Parse
            if self.debug:
                print("=== PARSING ===")
            parser = Parser(tokens)
            ast = parser.parse()
            
            if self.debug:
                print(f"Generated AST with {len(ast.statements)} statements")
                print()
            
            # Interpret
            if self.debug:
                print("=== EXECUTING ===")
            interpreter = Interpreter()
            interpreter.execute(ast)
            
        except SyntaxError as e:
            print(f"\n❌ SYNTAX ERROR")
            print('━' * 63)
            print(f"   {e}")
            print('━' * 63)
            sys.exit(1)
        
        except RuntimeError as e:
            print(f"\n❌ RUNTIME ERROR")
            print('━' * 63)
            print(f"   {e}")
            print('━' * 63)
            sys.exit(1)
        
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR")
            print('━' * 63)
            print(f"   {type(e).__name__}: {e}")
            
            if self.debug:
                import traceback
                print()
                traceback.print_exc()
            
            print('━' * 63)
            sys.exit(1)
    
    def show_usage(self):
        """Show brief usage"""
        print(BANNER)
        print("Usage: epstein <file.epc> | --help | --version")
        print("       epstein --help")
        print()
    
    def show_help(self):
        """Show full help"""
        print(HELP_TEXT)
    
    def show_version(self):
        """Show version"""
        print("EPSTEIN Programming Language v1.0.0")


def main():
    """Main entry point"""
    cli = EpsteinCLI()
    cli.run(sys.argv[1:])


if __name__ == '__main__':
    main()
