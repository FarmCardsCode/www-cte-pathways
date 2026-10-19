// Apply filters as soon as a choice changes. Without JS, the
// "Show pathways" button still submits the form.
document.querySelectorAll("form[data-autosubmit]").forEach((form) => {
  form.addEventListener("change", () => form.submit());
  form.querySelector("button[type=submit]")?.classList.add("visually-hidden");
});
