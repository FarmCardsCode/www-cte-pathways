// Theme menu: Auto / Light / Dark. "Auto" follows the device setting;
// light/dark set data-theme on <html>, which style.css reads. Keyboard:
// Enter/Space/Down opens, arrows move, Escape or Tab closes.
(() => {
  // Plain geometric characters (no emoji forms): half, empty, full circle.
  const ICONS = { auto: "◐", light: "○", dark: "●" };
  const LABELS = { auto: "Auto", light: "Light", dark: "Dark" };

  const root = document.documentElement;
  const wrapper = document.querySelector("[data-theme-menu]");
  if (!wrapper) return;
  const button = wrapper.querySelector(".theme-toggle");
  const menu = wrapper.querySelector("[role=menu]");
  const items = [...menu.querySelectorAll("[role=menuitemradio]")];

  const current = () => root.dataset.theme || "auto";

  const show = (mode) => {
    button.querySelector(".theme-toggle-icon").textContent = ICONS[mode];
    button.querySelector(".theme-toggle-text").textContent = LABELS[mode];
    button.setAttribute("aria-label", `Color theme: ${LABELS[mode].toLowerCase()}`);
    items.forEach((item) => item.setAttribute("aria-checked", String(item.dataset.mode === mode)));
  };

  const apply = (mode) => {
    if (mode === "auto") delete root.dataset.theme;
    else root.dataset.theme = mode;
    try {
      if (mode === "auto") localStorage.removeItem("theme");
      else localStorage.setItem("theme", mode);
    } catch (e) {}
    show(mode);
  };

  const isOpen = () => !menu.hidden;

  const open = (focusIndex) => {
    menu.hidden = false;
    button.setAttribute("aria-expanded", "true");
    const index = focusIndex ?? items.findIndex((item) => item.dataset.mode === current());
    items[(index + items.length) % items.length].focus();
  };

  const close = (returnFocus = true) => {
    if (!isOpen()) return;
    menu.hidden = true;
    button.setAttribute("aria-expanded", "false");
    if (returnFocus) button.focus();
  };

  button.addEventListener("click", () => (isOpen() ? close() : open()));
  button.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") { event.preventDefault(); open(); }
    if (event.key === "ArrowUp") { event.preventDefault(); open(items.length - 1); }
  });

  items.forEach((item, i) => {
    item.addEventListener("click", () => { apply(item.dataset.mode); close(); });
    item.addEventListener("keydown", (event) => {
      const moves = { ArrowDown: i + 1, ArrowUp: i - 1, Home: 0, End: items.length - 1 };
      if (event.key in moves) {
        event.preventDefault();
        items[(moves[event.key] + items.length) % items.length].focus();
      } else if (event.key === "Escape") {
        event.preventDefault();
        close();
      } else if (event.key === "Tab") {
        close(false);
      }
    });
  });

  document.addEventListener("click", (event) => {
    if (!wrapper.contains(event.target)) close(false);
  });

  show(current());
  wrapper.hidden = false;
})();
