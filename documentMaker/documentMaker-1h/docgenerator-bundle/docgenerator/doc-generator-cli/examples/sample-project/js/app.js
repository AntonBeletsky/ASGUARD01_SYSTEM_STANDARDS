import { isValidEmail, debounce, ThemeStore } from "./utils.js";

// TODO: wire this up to a real backend endpoint

const themeStore = new ThemeStore("light");

/**
 * Sets up the theme toggle button.
 */
function initThemeToggle() {
  const button = document.getElementById("theme-toggle");
  if (!button) return;
  button.addEventListener("click", () => {
    const next = themeStore.toggle();
    document.documentElement.dataset.theme = next;
  });
}

/**
 * Sets up the lead-capture form: validation and submission.
 * @param {string} formSelector - CSS selector for the form
 */
function initLeadForm(formSelector) {
  const form = document.querySelector(formSelector);
  if (!form) return;

  const emailInput = document.getElementById("lead-email");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!isValidEmail(emailInput.value)) {
      emailInput.classList.add("input--error");
      return;
    }
    console.log("Sending catalog to", emailInput.value);
  });
}

/**
 * Highlights the active nav item while scrolling.
 */
function initScrollSpy() {
  const sections = document.querySelectorAll(".features, .pricing");
  const onScroll = debounce(() => {
    sections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top < 120 && rect.bottom > 120) {
        section.classList.add("is-active");
      } else {
        section.classList.remove("is-active");
      }
    });
  }, 100);
  window.addEventListener("scroll", onScroll);
}

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initLeadForm("#lead-form");
  initScrollSpy();
});
