// Theme button: cycles auto -> light -> dark. "Auto" follows the device
// setting; light/dark set data-theme on <html>, which style.css reads.
(() => {
  const MODES = ["auto", "light", "dark"];
  // Plain geometric characters (no emoji forms): half, empty, full circle.
  const ICONS = { auto: "◐", light: "○", dark: "●" };
  const LABELS = { auto: "Auto", light: "Light", dark: "Dark" };

  const root = document.documentElement;
  const button = document.querySelector("[data-theme-toggle]");
  if (!button) return;

  const current = () => root.dataset.theme || "auto";

  const show = (mode) => {
    button.querySelector(".theme-toggle-icon").textContent = ICONS[mode];
    button.querySelector(".theme-toggle-text").textContent = LABELS[mode];
    const label = `Color theme: ${LABELS[mode].toLowerCase()}`;
    button.setAttribute("aria-label", label);
    button.title = label;
  };

  button.addEventListener("click", () => {
    const next = MODES[(MODES.indexOf(current()) + 1) % MODES.length];
    if (next === "auto") delete root.dataset.theme;
    else root.dataset.theme = next;
    try {
      if (next === "auto") localStorage.removeItem("theme");
      else localStorage.setItem("theme", next);
    } catch (e) {}
    show(next);
  });

  show(current());
  button.hidden = false;
})();
