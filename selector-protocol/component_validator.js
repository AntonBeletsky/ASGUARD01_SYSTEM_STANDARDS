/*
═══════════════════════════════════════════════════════════════════════════════
  COMPONENT SELECTOR VALIDATOR
  Validates component integrity against selector map
  
  Usage:
    node validate.js ./components/Button/
═══════════════════════════════════════════════════════════════════════════════
*/

const fs = require('fs');
const path = require('path');

class ComponentValidator {
  constructor(componentDir) {
    this.componentDir = componentDir;
    this.errors = [];
    this.warnings = [];
    this.results = {};
    
    // Load files
    this.mapPath = path.join(componentDir, 'component.selectors.json');
    this.map = JSON.parse(fs.readFileSync(this.mapPath, 'utf-8'));
    
    this.files = {
      html: this.readFile('*.html'),
      css: this.readFile('*.css'),
      js: this.readFile('*.js'),
      test: this.readFile('*.test.js')
    };
  }

  readFile(pattern) {
    const files = fs.readdirSync(this.componentDir);
    const regex = pattern.replace('*', '[^.]+');
    const matches = files.filter(f => new RegExp(`^${regex}$`).test(f));
    
    if (matches.length === 0) return null;
    
    const content = fs.readFileSync(
      path.join(this.componentDir, matches[0]),
      'utf-8'
    );
    return { name: matches[0], content };
  }

  // =========================================================================
  // VALIDATION 1: All selectors exist in code
  // =========================================================================
  validateSelectorsExist() {
    console.log('\n[1] Validating selectors exist in code...');
    
    for (const [key, selector] of Object.entries(this.map.selectors)) {
      const selectorStr = selector.selector;
      const foundIn = [];

      // Check HTML
      if (this.files.html && this.contains(this.files.html.content, selectorStr)) {
        foundIn.push('HTML');
      }

      // Check CSS
      if (this.files.css && this.contains(this.files.css.content, selectorStr)) {
        foundIn.push('CSS');
      }

      // Check JS
      if (this.files.js && this.contains(this.files.js.content, selectorStr)) {
        foundIn.push('JS');
      }

      if (foundIn.length === 0) {
        this.errors.push(
          `✗ ORPHANED: "${selectorStr}" (${key}) not found in any file`
        );
      } else {
        console.log(`  ✓ "${selectorStr}": found in ${foundIn.join(', ')}`);
      }
    }
  }

  // =========================================================================
  // VALIDATION 2: All usedIn references are accurate
  // =========================================================================
  validateUsedInReferences() {
    console.log('\n[2] Validating usedIn references...');
    
    for (const [key, selector] of Object.entries(this.map.selectors)) {
      const selectorStr = selector.selector;
      
      if (selector.usedIn.html) {
        for (const ref of selector.usedIn.html) {
          if (!this.findLineInFile(this.files.html, ref, selectorStr)) {
            this.errors.push(
              `✗ BROKEN: "${selectorStr}" referenced in ${ref} but line not found`
            );
          }
        }
      }

      if (selector.usedIn.css) {
        for (const ref of selector.usedIn.css) {
          if (!this.findLineInFile(this.files.css, ref, selectorStr)) {
            this.errors.push(
              `✗ BROKEN: "${selectorStr}" referenced in ${ref} but line not found`
            );
          }
        }
      }

      if (selector.usedIn.js) {
        for (const ref of selector.usedIn.js) {
          if (!this.findLineInFile(this.files.js, ref, selectorStr)) {
            this.errors.push(
              `✗ BROKEN: "${selectorStr}" referenced in ${ref} but line not found`
            );
          }
        }
      }
    }
    
    if (this.errors.length === 0) {
      console.log('  ✓ All usedIn references valid');
    }
  }

  // =========================================================================
  // VALIDATION 3: BEM consistency
  // =========================================================================
  validateBEMConsistency() {
    console.log('\n[3] Validating BEM naming...');
    
    const rootSelector = this.map.selectors.root?.selector;
    if (!rootSelector) {
      this.warnings.push('⚠ No root selector defined');
      return;
    }

    const blockName = rootSelector.replace('.', '');

    for (const [key, selector] of Object.entries(this.map.selectors)) {
      if (key === 'root') continue;
      
      const selectorStr = selector.selector;
      
      // Check element naming (.button__element)
      if (selector.parent === rootSelector) {
        if (!selectorStr.includes(`${blockName}__`)) {
          this.warnings.push(
            `⚠ BEM: "${selectorStr}" should follow "${blockName}__*" pattern`
          );
        }
      }
      
      // Check modifier naming (.button--modifier)
      if (selector.type === 'modifier' || selector.type === 'state') {
        if (!selectorStr.includes(`${blockName}--`)) {
          this.warnings.push(
            `⚠ BEM: "${selectorStr}" should follow "${blockName}--*" pattern`
          );
        }
      }
    }

    console.log('  ✓ BEM validation complete');
  }

  // =========================================================================
  // VALIDATION 4: ARIA sync
  // =========================================================================
  validateARIASync() {
    console.log('\n[4] Validating ARIA attributes...');

    for (const [key, aria] of Object.entries(this.map.ariaAttributes)) {
      const attrStr = aria.attribute;
      
      if (!this.files.html || !this.contains(this.files.html.content, attrStr)) {
        this.errors.push(
          `✗ MISSING: "${attrStr}" not found in HTML`
        );
      }

      // Check if aria attribute syncs with CSS class
      if (aria.syncWith) {
        const cssClass = aria.syncWith;
        
        // Find JS code that sets both
        let setsBoth = false;
        
        if (this.files.js) {
          const content = this.files.js.content;
          // Check if setAttribute and classList.add/remove appear close together
          if (this.contains(content, `setAttribute('${attrStr}'`) &&
              this.contains(content, cssClass)) {
            setsBoth = true;
          }
        }

        if (!setsBoth) {
          this.warnings.push(
            `⚠ ARIA: "${attrStr}" should sync with "${cssClass}" in JS`
          );
        }
      }
    }

    console.log('  ✓ ARIA validation complete');
  }

  // =========================================================================
  // VALIDATION 5: Data attributes syntax
  // =========================================================================
  validateDataAttributes() {
    console.log('\n[5] Validating data attributes...');

    for (const [key, dataAttr] of Object.entries(this.map.dataAttributes)) {
      const attrStr = dataAttr.attribute;
      
      // Data attributes should be kebab-case in HTML
      if (/[A-Z]/.test(attrStr.replace('data-', ''))) {
        this.errors.push(
          `✗ DATA ATTR: "${attrStr}" should use kebab-case (data-my-attr not data-myAttr)`
        );
      }

      // Check HTML
      if (this.files.html && !this.contains(this.files.html.content, attrStr)) {
        this.warnings.push(
          `⚠ DATA ATTR: "${attrStr}" not found in HTML`
        );
      }

      // Convert to camelCase for JS check
      const camelCase = attrStr
        .replace('data-', '')
        .split('-')
        .map((word, idx) => idx === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1))
        .join('');

      // Check JS for either getAttribute or dataset
      if (this.files.js) {
        const hasGetAttr = this.contains(this.files.js.content, `getAttribute('${attrStr}'`);
        const hasDataset = this.contains(this.files.js.content, `.${camelCase}`);
        const hasQuery = this.contains(this.files.js.content, `[${attrStr}`);

        if (!hasGetAttr && !hasDataset && !hasQuery) {
          this.warnings.push(
            `⚠ DATA ATTR: "${attrStr}" defined but not used in JS`
          );
        }
      }
    }

    console.log('  ✓ Data attribute validation complete');
  }

  // =========================================================================
  // VALIDATION 6: CSS variables
  // =========================================================================
  validateCSSVariables() {
    console.log('\n[6] Validating CSS variables...');

    for (const [key, cssVar] of Object.entries(this.map.cssVariables)) {
      const varName = cssVar.variable;
      
      // Should be used in CSS
      if (!this.files.css) {
        this.warnings.push(`⚠ No CSS file found`);
        continue;
      }

      const varUsage = this.countOccurrences(this.files.css.content, varName);
      
      if (varUsage === 0) {
        this.warnings.push(
          `⚠ CSS VAR: "${varName}" defined but never used`
        );
      } else {
        console.log(`  ✓ "${varName}": used ${varUsage} times`);
      }
    }
  }

  // =========================================================================
  // VALIDATION 7: JavaScript variables
  // =========================================================================
  validateJSVariables() {
    console.log('\n[7] Validating JS variables...');

    if (!this.files.js) {
      console.log('  ⚠ No JS file found');
      return;
    }

    for (const [key, jsVar] of Object.entries(this.map.jsVariables)) {
      const varStr = jsVar.variable;
      const varUsage = this.countOccurrences(this.files.js.content, varStr);

      if (varUsage === 0) {
        this.warnings.push(
          `⚠ JS VAR: "${varStr}" defined in map but not found in code`
        );
      } else {
        console.log(`  ✓ "${varStr}": used ${varUsage} times`);
      }
    }
  }

  // =========================================================================
  // VALIDATION 8: Method signatures
  // =========================================================================
  validateMethods() {
    console.log('\n[8] Validating method signatures...');

    if (!this.files.js) {
      console.log('  ⚠ No JS file found');
      return;
    }

    for (const [methodName, methodDef] of Object.entries(this.map.methods)) {
      // Simple check - look for method name in JS
      if (!this.contains(this.files.js.content, methodName + '(')) {
        this.warnings.push(
          `⚠ METHOD: "${methodName}" not found in JS`
        );
      } else {
        console.log(`  ✓ Method "${methodName}" found`);
      }
    }
  }

  // =========================================================================
  // VALIDATION 9: Event definitions
  // =========================================================================
  validateEvents() {
    console.log('\n[9] Validating events...');

    if (!this.files.js) {
      console.log('  ⚠ No JS file found');
      return;
    }

    for (const [eventKey, eventDef] of Object.entries(this.map.events || {})) {
      const eventName = eventDef.eventName;

      if (!this.contains(this.files.js.content, eventName)) {
        this.warnings.push(
          `⚠ EVENT: "${eventName}" defined but not found in JS`
        );
      } else {
        console.log(`  ✓ Event "${eventName}" found`);
      }
    }
  }

  // =========================================================================
  // HELPER METHODS
  // =========================================================================

  contains(text, substring) {
    return text.includes(substring);
  }

  countOccurrences(text, substring) {
    const regex = new RegExp(substring.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    const matches = text.match(regex);
    return matches ? matches.length : 0;
  }

  findLineInFile(file, lineRef, selector) {
    if (!file) return false;
    
    const [filename, lineNumber] = lineRef.split(':');
    const lines = file.content.split('\n');
    
    if (!lineNumber) {
      // No line number specified, just check if selector exists
      return this.contains(file.content, selector);
    }

    const lineIdx = parseInt(lineNumber) - 1;
    if (lineIdx >= lines.length) return false;

    return this.contains(lines[lineIdx], selector);
  }

  // =========================================================================
  // SUMMARY & REPORT
  // =========================================================================

  validate() {
    console.log('═'.repeat(70));
    console.log(`VALIDATING: ${this.map.componentName} (v${this.map.version})`);
    console.log('═'.repeat(70));

    this.validateSelectorsExist();
    this.validateUsedInReferences();
    this.validateBEMConsistency();
    this.validateARIASync();
    this.validateDataAttributes();
    this.validateCSSVariables();
    this.validateJSVariables();
    this.validateMethods();
    this.validateEvents();

    this.generateReport();
  }

  generateReport() {
    console.log('\n' + '═'.repeat(70));
    console.log('VALIDATION REPORT');
    console.log('═'.repeat(70));

    if (this.errors.length > 0) {
      console.log(`\n❌ ERRORS (${this.errors.length}):`);
      this.errors.forEach(e => console.log(`  ${e}`));
    }

    if (this.warnings.length > 0) {
      console.log(`\n⚠️  WARNINGS (${this.warnings.length}):`);
      this.warnings.forEach(w => console.log(`  ${w}`));
    }

    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log('\n✅ VALIDATION PASSED');
      console.log('All selectors, references, and syncs are valid!');
    }

    console.log('\n' + '═'.repeat(70));
    console.log(`Status: ${this.errors.length === 0 ? 'VALID ✓' : 'INVALID ✗'}`);
    console.log('═'.repeat(70));

    return {
      isValid: this.errors.length === 0,
      errorCount: this.errors.length,
      warningCount: this.warnings.length,
      errors: this.errors,
      warnings: this.warnings
    };
  }
}

// ============================================================================
// USAGE
// ============================================================================

/*
COMMAND LINE:
  node validator.js ./components/Button

PROGRAMMATIC:
  const validator = new ComponentValidator('./components/Button');
  const report = validator.validate();
  
  if (report.isValid) {
    console.log('Component is valid!');
  } else {
    console.log(`Found ${report.errorCount} errors`);
  }

EXPECTED OUTPUT:
  [1] Validating selectors exist in code...
    ✓ ".button": found in HTML, CSS, JS
    ✓ ".button__icon": found in HTML, CSS, JS
    ...
  
  [2] Validating usedIn references...
    ✓ All usedIn references valid
  
  [3] Validating BEM naming...
    ✓ BEM validation complete
  
  ... (more validations)
  
  ═══════════════════════════════════════════════════════════════════════════
  VALIDATION REPORT
  ═══════════════════════════════════════════════════════════════════════════
  
  ✅ VALIDATION PASSED
  All selectors, references, and syncs are valid!
*/

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ComponentValidator;
}

// Run if called directly
if (require.main === module) {
  const componentDir = process.argv[2];
  
  if (!componentDir) {
    console.error('Usage: node validator.js <component-directory>');
    process.exit(1);
  }

  const validator = new ComponentValidator(componentDir);
  const report = validator.validate();

  process.exit(report.isValid ? 0 : 1);
}
