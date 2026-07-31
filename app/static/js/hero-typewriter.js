(() => {
  const TEXT =
    "Explainable hematology pattern analysis.";

  class HemaLensHeroTypewriter {
    constructor() {
      this.root = null;
      this.node = null;
      this.index = 0;
      this.deleting = false;
      this.timerId = null;
    }

    mount() {
      const root = document.querySelector(
        "[data-hemalens-typewriter]",
      );

      if (!root) {
        this.destroy();
        return;
      }

      if (this.root === root && this.timerId !== null) {
        return;
      }

      this.destroy();

      this.root = root;
      this.node = root.querySelector(
        "[data-hemalens-typewriter-line]",
      );

      if (!this.node) {
        console.error(
          "HemaLens typewriter node tidak ditemukan.",
        );
        return;
      }

      if (
        window.matchMedia(
          "(prefers-reduced-motion: reduce)",
        ).matches
      ) {
        this.node.textContent = TEXT;
        return;
      }

      this.index = 0;
      this.deleting = false;
      this.node.textContent = "";
      this.node.dataset.active = "true";

      this.waitUntilLandingVisible();
    }

    waitUntilLandingVisible() {
      if (!this.root?.isConnected) {
        this.destroy();
        return;
      }

      const splash = document.querySelector(
        "[data-hemalens-splash], [role='status']",
      );

      const splashVisible =
        splash &&
        splash.getClientRects().length > 0 &&
        window.getComputedStyle(splash).display !==
          "none" &&
        Number.parseFloat(
          window.getComputedStyle(splash).opacity || "1",
        ) > 0.05;

      const headingVisible =
        this.root.getClientRects().length > 0;

      if (splashVisible || !headingVisible) {
        this.schedule(
          () => this.waitUntilLandingVisible(),
          100,
        );
        return;
      }

      this.schedule(() => this.step(), 400);
    }

    step() {
      if (!this.node?.isConnected) {
        this.destroy();
        return;
      }

      if (document.hidden) {
        this.schedule(() => this.step(), 200);
        return;
      }

      if (!this.deleting) {
        if (this.index < TEXT.length) {
          this.index += 1;
          this.node.textContent = TEXT.slice(
            0,
            this.index,
          );

          this.schedule(
            () => this.step(),
            52 + Math.random() * 28,
          );
          return;
        }

        this.deleting = true;
        this.schedule(() => this.step(), 1600);
        return;
      }

      if (this.index > 0) {
        this.index -= 1;
        this.node.textContent = TEXT.slice(
          0,
          this.index,
        );

        this.schedule(
          () => this.step(),
          25 + Math.random() * 14,
        );
        return;
      }

      this.deleting = false;
      this.schedule(() => this.step(), 500);
    }

    schedule(callback, delay) {
      window.clearTimeout(this.timerId);

      this.timerId = window.setTimeout(
        callback,
        delay,
      );
    }

    destroy() {
      window.clearTimeout(this.timerId);
      this.timerId = null;

      if (this.node) {
        delete this.node.dataset.active;
      }

      this.root = null;
      this.node = null;
      this.index = 0;
      this.deleting = false;
    }
  }

  const controller =
    new HemaLensHeroTypewriter();

  window.HemaLensHeroTypewriter = controller;

  const mount = () => controller.mount();

  document.addEventListener(
    "DOMContentLoaded",
    mount,
  );

  document.addEventListener(
    "htmx:afterSwap",
    mount,
  );

  document.addEventListener(
    "htmx:afterSettle",
    mount,
  );

  document.addEventListener(
    "htmx:beforeSwap",
    (event) => {
      if (
        event.detail.target?.id ===
        "main-workspace"
      ) {
        controller.destroy();
      }
    },
  );

  window.addEventListener("pageshow", mount);
})();
