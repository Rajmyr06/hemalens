window.hemalensApp = function hemalensApp() {
  return {
    showSplash: false,
    contentReady: false,
    landingEntered: false,
    workspace: "landing",

    init() {
      const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
      ).matches;

      if (reduceMotion) {
        this.contentReady = true;
        this.landingEntered = true;
        return;
      }

      this.showSplash = true;

      window.setTimeout(() => {
        this.contentReady = true;

        window.requestAnimationFrame(() => {
          window.requestAnimationFrame(() => {
            this.landingEntered = true;
            this.showSplash = false;
          });
        });
      }, 2200);
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
