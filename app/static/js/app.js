window.hemalensApp = function hemalensApp() {
  return {
    showSplash: false,
    workspace: "landing",

    init() {
      const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
      ).matches;

      this.showSplash = !reduceMotion;
      if (this.showSplash) {
        window.setTimeout(() => {
          this.showSplash = false;
        }, 2200);
      }
    },
  };
};

document.addEventListener("htmx:beforeSwap", (event) => {
  if (event.detail.xhr.status === 422) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});

document.addEventListener("htmx:afterSwap", () => {
  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
});
