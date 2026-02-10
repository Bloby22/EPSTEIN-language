import sys
from typing import Any, Dict, Callable

TOKENKEY = {
    # Boolean values
    'truth': 'True',
    'lie': 'False',
    
    # Types
    'deal': 'str',
    'alibi': 'None',
    'theory': 'float',
    'money': 'bool',
    'power': 'int',
    'ghost': 'str',
    'time': 'int',
    'light': 'bool',
    'universe': 'None',
    
    # Data structures
    'girl': 'dict',
    'island': 'list',
    'enemy': 'dict',
    'weapon': 'list',
    'mission': 'tuple',
    'crew': 'list',
    'government': 'dict',
    'agenda': 'dict',
    'secret': 'set',
    
    # Functions/Methods
    'files': 'print',
    'risk': 'float',
    
    # Control flow (handled specially in parser)
    'suicide': 'sys.exit',
    'escape': 'break',
    'plot': 'def',
    'plan': 'def',
    'shadow': 'lambda',
    'circle': 'lambda',
    'famous': 'function',
    'loop': 'for'
}

# Keywords that need special handling
KEYWORDS = {
    'FUNCTION_BLOCK': ['plot', 'plan'],
    'LAMBDA': ['shadow', 'circle'],
    'LOOP': 'loop',
    'IF': 'if',
    'ELSE': 'else',
    'ELIF': 'elif',
    'RETURN': 'suicide',
    'BREAK': 'escape',
    'PRINT': 'files',
}

class Runtime:
    """Runtime environment for EPSTEIN (meme-programming language)"""

    @staticmethod
    def files(*args, **kwargs):
        """Print function (EPSTEIN 'files' command)"""
        print(*args, **kwargs)

    @staticmethod
    def suicide(code: int = 0):
        """Exit program (EPSTEIN 'suicide' command)"""
        sys.exit(code)

    @staticmethod
    def escape():
        """Break out of a loop (EPSTEIN 'escape' command)"""
        raise StopIteration("escape")
    
    @staticmethod
    def risk(value: Any) -> float:
        """Convert to float (EPSTEIN 'risk' function)"""
        return float(value)
    
    @staticmethod
    def theory(value: Any) -> float:
        """Convert to float/int (EPSTEIN 'theory' function)"""
        try:
            return int(value)
        except ValueError:
            return float(value)
    
    @staticmethod
    def money(value: Any) -> bool:
        """Convert to bool (EPSTEIN 'money' function)"""
        return bool(value)


def get_runtime_globals() -> Dict[str, Any]:
    """Get global runtime environment for EPSTEIN execution"""
    runtime = {
        # Built-in functions
        'files': Runtime.files,
        'suicide': Runtime.suicide,
        'escape': Runtime.escape,
        'risk': Runtime.risk,
        'theory': Runtime.theory,
        'money': Runtime.money,
        
        # Boolean values
        'truth': True,
        'lie': False,
        'alibi': None,
        'universe': None,
        
        # Type constructors
        'deal': str,
        'ghost': str,
        'power': int,
        'time': int,
        'light': bool,
        'island': list,
        'weapon': list,
        'crew': list,
        'mission': tuple,
        'girl': dict,
        'enemy': dict,
        'government': dict,
        'agenda': dict,
        'secret': set,
        
        # Python built-ins we need
        'range': range,
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
    }
    
    return runtime

def IsKeyword(token: str) -> bool:
    """Check if token is an EPSTEIN keyword"""
    return token in TOKENKEY or any(token in v if isinstance(v, list) else token == v 
                                      for v in KEYWORDS.values())


def IsFunction(token: str) -> bool:
    """Check if token is a function definition keyword"""
    return token in KEYWORDS['FUNCTION_BLOCK']
