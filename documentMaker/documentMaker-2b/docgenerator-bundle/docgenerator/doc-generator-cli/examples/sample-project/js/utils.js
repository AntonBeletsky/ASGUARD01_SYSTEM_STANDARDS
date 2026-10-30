// Small reusable helpers with no side effects.

/**
 * Checks whether a string looks like an email address.
 * @param {string} value - the value to check
 * @returns {boolean} true if the string looks like an email
 */
export function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

/**
 * Limits how often a function can run to once every `wait` ms.
 * @param {Function} fn - the source function
 * @param {number} wait - delay in milliseconds
 * @returns {Function} the wrapped function
 * @example
 * const onScroll = debounce(() => console.log('scroll'), 200);
 */
export function debounce(fn, wait) {
  let timer = null;
  return function debounced(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), wait);
  };
}

/**
 * A simple in-memory store for the current tab's theme.
 */
export class ThemeStore {
  /**
   * @param {string} initial - starting theme ('light' | 'dark')
   */
  constructor(initial = "light") {
    this.theme = initial;
  }

  /** Flips the theme to the opposite value. */
  toggle() {
    this.theme = this.theme === "light" ? "dark" : "light";
    return this.theme;
  }
}
