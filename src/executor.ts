/**
 * EPSTEIN Language - Executor
 * Executes parsed and converted JavaScript code
 */

import { Runtime } from './utils';

export class Executor {
  private runtime: typeof Runtime;
  private globalScope: { [key: string]: any } = {};

  constructor() {
    this.runtime = Runtime;
    this.setupGlobalScope();
  }

  /**
   * Setup global scope with EPSTEIN runtime
   */
  private setupGlobalScope(): void {
    // Add EPSTEIN type constructors
    this.globalScope.theory = Runtime.theory;
    this.globalScope.risk = Runtime.risk;
    this.globalScope.ghost = Runtime.ghost;
    this.globalScope.money = Runtime.money;
    this.globalScope.island = Runtime.island;
    this.globalScope.girl = Runtime.girl;
    this.globalScope.mission = Runtime.mission;
    this.globalScope.secret = Runtime.secret;
    this.globalScope.weapon = Runtime.weapon;
    this.globalScope.files = Runtime.files;

    // Add boolean constants
    this.globalScope.truestory = Runtime.truth;
    this.globalScope.falsestory = Runtime.lie;
    this.globalScope.truth = Runtime.truth;
    this.globalScope.lie = Runtime.lie;

    // Add special values
    this.globalScope.universe = Runtime.universe;
    this.globalScope.alibi = Runtime.alibi;

    // Add console for debugging
    this.globalScope.console = console;
  }

  /**
   * Execute JavaScript code with EPSTEIN runtime
   */
  execute(jsCode: string): void {
    try {
      // Create function with global scope
      const func = new Function(...Object.keys(this.globalScope), jsCode);
      
      // Execute with runtime values
      func(...Object.values(this.globalScope));
    } catch (error) {
      console.error('🔴 EPSTEIN Execution Error:');
      console.error(error);
      throw error;
    }
  }

  /**
   * Execute with custom scope
   */
  executeWithScope(jsCode: string, customScope: { [key: string]: any }): void {
    const mergedScope = { ...this.globalScope, ...customScope };

    try {
      const func = new Function(...Object.keys(mergedScope), jsCode);
      func(...Object.values(mergedScope));
    } catch (error) {
      console.error('🔴 EPSTEIN Execution Error:');
      console.error(error);
      throw error;
    }
  }

  /**
   * Execute and return result
   */
  executeWithReturn(jsCode: string): any {
    try {
      const func = new Function(...Object.keys(this.globalScope), `return (function() { ${jsCode} })();`);
      return func(...Object.values(this.globalScope));
    } catch (error) {
      console.error('🔴 EPSTEIN Execution Error:');
      console.error(error);
      throw error;
    }
  }

  /**
   * Get current global scope
   */
  getScope(): { [key: string]: any } {
    return { ...this.globalScope };
  }

  /**
   * Update global scope
   */
  updateScope(key: string, value: any): void {
    this.globalScope[key] = value;
  }
}