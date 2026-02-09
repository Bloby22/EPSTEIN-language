import * as path from 'path';
import { Interpreter } from './interpreter';

function main() {
  // Path to main EPSTEIN file
  const epsFile = path.join(__dirname, '..', 'eps', 'main.ep');

  // Create interpreter instance
  const interpreter = new Interpreter();

  try {
    // Run the EPSTEIN program
    interpreter.run(epsFile);

    // Optional: Show debug info if DEBUG env var is set
    if (process.env.DEBUG === 'true') {
      interpreter.showDebugInfo();
    }

  } catch (error) {
    console.error('\n💀 EPSTEIN Program terminated with error');
    process.exit(1);
  }
}

// Run if this is the main module
if (require.main === module) {
  main();
}

export { main };
