(() => {
  const TEXTS = [
    "Explainable",
    "hematology",
    "pattern analysis.",
  ];

  class HemaLensHeroTypewriter {
    constructor() {
      this.root = null;
      this.nodes = [];
      this.values = ["", "", ""];
      this.lineIndex = 0;
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
      this.nodes = Array.from(
        root.querySelectorAll(
          "[data-hemalens-typewriter-line]",
        ),
      );

      if (this.nodes.length !== TEXTS.length) {
        console.error(
          "HemaLens typewriter: jumlah baris tidak sesuai.",
        );
        return;
      }

      if (
        window.matchMedia(
          "(prefers-reduced-motion: reduce)",
        ).matches
      ) {
        this.renderStatic();
        return;
      }

      this.values = ["", "", ""];
      this.lineIndex = 0;
      this.deleting = false;
      this.render();
      this.waitUntilVisible();
    }

    waitUntilVisible() {
      if (!this.root?.isConnected) {
        this.destroy();
        return;
      }

      const visible =
        this.root.getClientRects().length > 0 &&
        window.getComputedStyle(this.root).visibility !==
          "hidden";

      if (!visible) {
        this.schedule(
          () => this.waitUntilVisible(),
          100,
        );
        return;
      }

      this.schedule(() => this.step(), 450);
    }

    step() {
      if (!this.root?.isConnected) {
        this.destroy();
        return;
      }

      if (document.hidden) {
        this.schedule(() => this.step(), 200);
        return;
      }

      const target = TEXTS[this.lineIndex];
      const current = this.values[this.lineIndex];

      if (!this.deleting) {
        if (current.length < target.length) {
          this.values[this.lineIndex] =
            target.slice(0, current.length + 1);

          this.render();

          this.schedule(
            () => this.step(),
            65 + Math.random() * 35,
          );
          return;
        }

        if (this.lineIndex < TEXTS.length - 1) {
          this.lineIndex += 1;
          this.render();
          this.schedule(() => this.step(), 220);
          return;
        }

        this.deleting = true;
        this.schedule(() => this.step(), 1600);
        return;
      }

      if (current.length > 0) {
        this.values[this.lineIndex] =
          current.slice(0, -1);

        this.render();

        this.schedule(
          () => this.step(),
          30 + Math.random() * 18,
        );
        return;
      }

      if (this.lineIndex > 0) {
        this.lineIndex -= 1;
        this.render();
        this.schedule(() => this.step(), 100);
        return;
      }

      this.deleting = false;
      this.lineIndex = 0;
      this.render();
      this.schedule(() => this.step(), 550);
    }

    render() {
      this.nodes.forEach((node, index) => {
        node.textContent = this.values[index];

        if (index === this.lineIndex) {
          node.dataset.active = "true";
        } else {
          delete node.dataset.active;
        }
      });
    }

    renderStatic() {
      this.nodes.forEach((node, index) => {
        node.textContent = TEXTS[index];
        delete node.dataset.active;
      });
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

      this.nodes.forEach((node) => {
        delete node.dataset.active;
      });

      this.root = null;
      this.nodes = [];
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
