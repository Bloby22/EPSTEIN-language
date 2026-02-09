export const TOKEN: { [key: string]: string } = {
    'truth': 'true',
    'lie': 'false',
    'plot': 'function',
    'suicide': 'return',
    'escape': 'break',
    'files': 'console.log',
    'loop': 'for',
    'universe': 'null'
}

// 📁 Types EPSTEIN constructors
export const TYPES: { [key: string]: string } = {
    'theory': 'Number',
    'risk': 'parseFloat',
    'ghost': 'String',
    'money': 'Boolean',
    'island': 'Array',
    'secret': 'Set'
};

export class Runtime {
    // 🔗 Type conversion (functions)
    static theory(x: any): number {
        return Number(x);
    }

    static risk(x: any): number {
        return parseFloat(String(x));
    }

    static ghost(x: any): string {
        return String(x);
    }

    static money(x: any): boolean {
        return Boolean(x);
    }

    static island(...args: any[]): any[] {
        return Array.from(args);
    }

    static girl(obj: any): any {
        return obj;
    }

    static mission(...args: any[]): any[] {
        return Array.from(args);
    }

    static secret(...args: any[]): Set<any> {
        return new Set(args);
    }

    static weapon(...args: any[]): any[] {
        return Array.from(args);
    }

    static files(msg: any): void {
        console.log(msg);
    }

    // Boolean constants
    static readonly truth: boolean = true;
    static readonly lie: boolean = false;
    
    // Values
    static readonly universe: null = null;
    static readonly alibi: null = null;
}

// Remove comments EPSTEIN code
export function removeComment(line: string): string {
    const commentIndex = line.indexOf('//');
    if (commentIndex !== -1) {
        return line.substring(0, commentIndex);
    }
    return line;
}

// Check if line is a function definition
export function isFunction(line: string): boolean {
    const trimmed = line.trim();
    return trimmed.startsWith('plot ');
}

// Check if line is conditional
export function isConditional(line: string): boolean {
    const trimmed = line.trim();
    return trimmed.startsWith('if ') || trimmed === 'else:';
}

// Get indentation level
export function getIndent(line: string): number {
    const match = line.match(/^(\s*)/);
    return match ? match[1].length : 0;
}

// Replace EPSTEIN tokens with JS
export function replaceToken(code: string): string {
    let result = code;

    // Replace tokens
    for (const [epstein, js] of Object.entries(TOKEN)) {
        const regex = new RegExp(`\\b${epstein}\\b`, 'g');
        result = result.replace(regex, js);
    }
    
    return result;
}

// Check if line is empty or comment only
export function isEmpty(line: string): boolean {
    const trimmed = line.trim();
    return trimmed === '' || trimmed.startsWith('//');
}

// Extract function name from definition
export function extractFunctionName(line: string): string | null {
    const match = line.match(/(?:plot)\s+(\w+)/);
    return match ? match[1]: null;
}

// Extract loop variable
export function extractLoop(line: string): { variable: string; collection: string } | null {
    const match = line.match(/loop\s+(\w+):/);
    if (match) {
        return {
            variable: 'item',
            collection: match[1]
        };
    }

    return null;
}

// Log debug
export function debug(message: string, data?: any): void {
    if (process.env.DEBUG === 'true') {
        console.log(`[DEBUG] ${message}`, data || '');
    }
}