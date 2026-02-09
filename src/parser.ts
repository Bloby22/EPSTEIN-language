/**
 * EPSTEIN Language - Parser
 * Parses .eps files and converts them to executable JavaScript/TypeScript
 */

import {
  removeComment,
  isFunction,
  isConditional,
  getIndent,
  isEmpty,
  extractFunctionName,
  extractLoop,
  debug
} from './utils';

export interface ParsedLine {
  original: string;
  cleaned: string;
  indent: number;
  type: 'variable' | 'function' | 'loop' | 'conditional' | 'expression' | 'empty';
}

export class EpsteinParser {
  private lines: string[] = [];
  private currentIndex: number = 0;

  constructor(code: string) {
    this.lines = code.split('\n');
  }

  /**
   * Parse entire EPSTEIN code
   */
  parse(): ParsedLine[] {
    const parsed: ParsedLine[] = [];

    for (const line of this.lines) {
      const parsedLine = this.parseLine(line);
      parsed.push(parsedLine);
    }

    return parsed;
  }

  /**
   * Parse a single line
   */
  private parseLine(line: string): ParsedLine {
    const indent = getIndent(line);
    const cleaned = removeComment(line).trim();

    if (isEmpty(line)) {
      return {
        original: line,
        cleaned: '',
        indent,
        type: 'empty'
      };
    }

    if (isFunction(cleaned)) {
      return {
        original: line,
        cleaned,
        indent,
        type: 'function'
      };
    }


    if (isConditional(cleaned)) {
      return {
        original: line,
        cleaned,
        indent,
        type: 'conditional'
      };
    }

    if (cleaned.includes('=')) {
      return {
        original: line,
        cleaned,
        indent,
        type: 'variable'
      };
    }

    return {
      original: line,
      cleaned,
      indent,
      type: 'expression'
    };
  }

  /**
   * Convert EPSTEIN syntax to JavaScript
   */
  toJavaScript(parsedLines: ParsedLine[]): string {
    const jsLines: string[] = [];
    const indent = '  ';

    for (let i = 0; i < parsedLines.length; i++) {
      const line = parsedLines[i];

      if (line.type === 'empty') {
        jsLines.push('');
        continue;
      }

      const indentation = indent.repeat(line.indent / 2);

      switch (line.type) {
        case 'function':
          jsLines.push(this.convertFunction(line.cleaned, indentation));
          break;

        case 'loop':
          jsLines.push(this.convertLoop(line.cleaned, indentation));
          break;

        case 'conditional':
          jsLines.push(this.convertConditional(line.cleaned, indentation));
          break;

        case 'variable':
          jsLines.push(this.convertVariable(line.cleaned, indentation));
          break;

        case 'expression':
          jsLines.push(this.convertExpression(line.cleaned, indentation));
          break;
      }
    }

    return jsLines.join('\n');
  }

  /**
   * Convert function definition
   */
  private convertFunction(line: string, indent: string): string {
    // plot function_name(params): -> function function_name(params) {
    const match = line.match(/(?:plot|plan)\s+(\w+)\((.*?)\):/);
    if (match) {
      const [, name, params] = match;
      return `${indent}function ${name}(${params}) {`;
    }
    return `${indent}// ERROR: Invalid function syntax`;
  }

  /**
   * Convert loop
   */
  private convertLoop(line: string, indent: string): string {
    // loop collection: -> for (const item of collection) {
    const parts = extractLoop(line);
    if (parts) {
      return `${indent}for (const ${parts.variable} of ${parts.collection}) {`;
    }
    return `${indent}// ERROR: Invalid loop syntax`;
  }

  /**
   * Convert conditional
   */
  private convertConditional(line: string, indent: string): string {
    if (line === 'else:') {
      return `${indent}} else {`;
    }

    // if condition: -> if (condition) {
    const match = line.match(/if\s+(.+):/);
    if (match) {
      return `${indent}if (${match[1]}) {`;
    }

    return `${indent}// ERROR: Invalid conditional syntax`;
  }

  /**
   * Convert variable assignment
   */
  private convertVariable(line: string, indent: string): string {
    // Replace EPSTEIN keywords
    let converted = line;

    // Handle special constructors
    converted = converted.replace(/\btheory\(/g, 'Number(');
    converted = converted.replace(/\brisk\(/g, 'parseFloat(');
    converted = converted.replace(/\bghost\(/g, 'String(');
    converted = converted.replace(/\bmoney\(/g, 'Boolean(');

    // Handle collections
    converted = converted.replace(/\bisland\[/g, '[');
    converted = converted.replace(/\bgirl\{/g, '{');
    converted = converted.replace(/\bmission\(/g, '[');
    converted = converted.replace(/\bweapon\[/g, '[');

    // Handle boolean values
    converted = converted.replace(/\btruestory\b/g, 'true');
    converted = converted.replace(/\bfalsestory\b/g, 'false');
    converted = converted.replace(/\btruth\b/g, 'true');
    converted = converted.replace(/\blie\b/g, 'false');

    // Handle special values
    converted = converted.replace(/\buniverse\b/g, 'null');
    converted = converted.replace(/\balibi\b/g, 'null');

    return `${indent}const ${converted};`;
  }

  /**
   * Convert expression
   */
  private convertExpression(line: string, indent: string): string {
    let converted = line;

    // Handle files (print)
    converted = converted.replace(/\bfiles\(/g, 'console.log(');

    // Handle suicide (return)
    converted = converted.replace(/\bsuicide\s+/g, 'return ');

    // Handle escape (break)
    converted = converted.replace(/\bescape\b/g, 'break');

    // Handle type conversions
    converted = converted.replace(/\btheory\(/g, 'Number(');
    converted = converted.replace(/\brisk\(/g, 'parseFloat(');
    converted = converted.replace(/\bghost\(/g, 'String(');
    converted = converted.replace(/\bmoney\(/g, 'Boolean(');

    // Handle boolean values
    converted = converted.replace(/\btruestory\b/g, 'true');
    converted = converted.replace(/\bfalsestory\b/g, 'false');

    // Handle closing braces
    if (line.trim() === '}') {
      return `${indent}}`;
    }

    return `${indent}${converted};`;
  }
}