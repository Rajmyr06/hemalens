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

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function setWorkspaceBusy(busy) {
  const workspace = document.getElementById("main-workspace");
  workspace?.setAttribute("aria-busy", String(busy));
}

function focusSwappedContent(target) {
  if (!(target instanceof HTMLElement) || target.id !== "main-workspace") {
    return;
  }

  const heading = target.querySelector("[data-page-heading]");
  if (!(heading instanceof HTMLElement)) {
    return;
  }

  window.requestAnimationFrame(() => {
    heading.focus({ preventScroll: true });
  });
}

document.addEventListener("htmx:beforeRequest", () => {
  setWorkspaceBusy(true);
});

document.addEventListener("htmx:afterRequest", () => {
  setWorkspaceBusy(false);
});

document.addEventListener("htmx:responseError", () => {
  setWorkspaceBusy(false);
});

document.addEventListener("htmx:beforeSwap", (event) => {
  if (event.detail.xhr.status === 422) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});

document.addEventListener("htmx:afterSwap", (event) => {
  setWorkspaceBusy(false);
  window.scrollTo({
    top: 0,
    behavior: prefersReducedMotion() ? "auto" : "smooth",
  });
  focusSwappedContent(event.detail.target);
});
