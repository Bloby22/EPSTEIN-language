/**
 * EPSTEIN Language - Interpreter
 * Main engine for loading and executing .ep files
 */

import * as fs from 'fs';
import * as path from 'path';
import { Parser } from './parser';
import { Executor } from './executor';
import { debug } from './utils';

export class Interpreter {
  private parser: Parser | null = null;
  private executor: Executor;
  private sourceCode: string = '';
  private jsCode: string = '';

  constructor() {
    this.executor = new Executor();
  }

  /**
   * Load EPSTEIN file from path
   */
  loadFile(filePath: string): void {
    try {
      const absolutePath = path.resolve(filePath);
      
      if (!fs.existsSync(absolutePath)) {
        throw new Error(`File not found: ${absolutePath}`);
      }

      this.sourceCode = fs.readFileSync(absolutePath, 'utf-8');
      debug('File loaded', { path: absolutePath, size: this.sourceCode.length });
    } catch (error) {
      console.error('🔴 Failed to load EPSTEIN file:');
      throw error;
    }
  }

  /**
   * Load EPSTEIN code from string
   */
  loadCode(code: string): void {
    this.sourceCode = code;
    debug('Code loaded', { size: code.length });
  }

  /**
   * Parse loaded EPSTEIN code
   */
  parse(): void {
    if (!this.sourceCode) {
      throw new Error('No source code loaded. Use loadFile() or loadCode() first.');
    }

    console.log('🕵️  Parsing EPSTEIN code...');
    this.parser = new Parser(this.sourceCode);
    
    const parsedLines = this.parser.parse();
    debug('Parsed lines', { count: parsedLines.length });

    // Convert to JavaScript
    this.jsCode = this.parser.toJavaScript(parsedLines);
    debug('Converted to JavaScript', { size: this.jsCode.length });

    console.log('✓ Parsing complete\n');
  }

  /**
   * Execute parsed code
   */
  execute(): void {
    if (!this.jsCode) {
      throw new Error('No code to execute. Call parse() first.');
    }

    console.log('🚀 Executing EPSTEIN code...\n');
    console.log('='.repeat(50));
    
    try {
      this.executor.execute(this.jsCode);
      console.log('='.repeat(50));
      console.log('\n✓ Execution complete');
    } catch (error) {
      console.log('='.repeat(50));
      console.log('\n✗ Execution failed');
      throw error;
    }
  }

  /**
   * Run EPSTEIN file (load, parse, execute)
   */
  run(filePath: string): void {
    console.log(`\n🕵️  EPSTEIN Language Interpreter v1.0`);
    console.log(`📄 File: ${path.basename(filePath)}`);
    console.log('='.repeat(50));
    console.log('');

    this.loadFile(filePath);
    this.parse();
    this.execute();
  }

  /**
   * Run EPSTEIN code from string
   */
  runCode(code: string): void {
    console.log(`\n🕵️  EPSTEIN Language Interpreter v1.0`);
    console.log('='.repeat(50));
    console.log('');

    this.loadCode(code);
    this.parse();
    this.execute();
  }

  /**
   * Get generated JavaScript code
   */
  getJavaScript(): string {
    return this.jsCode;
  }

  /**
   * Get source code
   */
  getSource(): string {
    return this.sourceCode;
  }

  /**
   * Show debug information
   */
  showDebugInfo(): void {
    console.log('\n📊 Debug Information:');
    console.log('='.repeat(50));
    console.log('Source Code:');
    console.log(this.sourceCode);
    console.log('\n' + '='.repeat(50));
    console.log('Generated JavaScript:');
    console.log(this.jsCode);
    console.log('='.repeat(50));
  }
}