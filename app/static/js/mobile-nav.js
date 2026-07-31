(() => {
  const NAV_SELECTOR = "[data-mobile-nav]";
  const FOCUSABLE_SELECTOR = [
    "a[href]",
    "button:not([disabled])",
    "input:not([disabled])",
    "select:not([disabled])",
    "textarea:not([disabled])",
    "[tabindex]:not([tabindex='-1'])",
  ].join(",");

  class MobileNavigation {
    constructor(root) {
      this.root = root;
      this.toggle = root.querySelector("[data-mobile-nav-toggle]");
      this.panel = root.querySelector("[data-mobile-nav-panel]");
      this.closeControls = Array.from(
        root.querySelectorAll("[data-mobile-nav-close]"),
      );
      this.links = Array.from(
        root.querySelectorAll("[data-mobile-nav-link]"),
      );
      this.previousFocus = null;
      this.closeTimer = null;
      this.open = false;

      this.handleToggle = this.handleToggle.bind(this);
      this.handleKeydown = this.handleKeydown.bind(this);
      this.handleDesktopChange = this.handleDesktopChange.bind(this);
      this.desktopQuery = window.matchMedia("(min-width: 640px)");
    }

    init() {
      if (!this.toggle || !this.panel) {
        return;
      }

      this.toggle.addEventListener("click", this.handleToggle);
      this.closeControls.forEach((control) => {
        control.addEventListener("click", () => this.close());
      });
      this.links.forEach((link) => {
        link.addEventListener("click", () => this.close(false));
      });
      this.panel.addEventListener("keydown", this.handleKeydown);
      this.desktopQuery.addEventListener?.("change", this.handleDesktopChange);
    }

    handleToggle() {
      if (this.open) {
        this.close();
      } else {
        this.show();
      }
    }

    show() {
      if (this.open || !this.panel) {
        return;
      }

      window.clearTimeout(this.closeTimer);
      this.previousFocus = document.activeElement;
      this.open = true;
      this.panel.hidden = false;
      this.toggle.setAttribute("aria-expanded", "true");
      this.toggle.setAttribute("aria-label", "Tutup menu navigasi");
      document.body.classList.add("mobile-nav-open");
      document.querySelector("main")?.setAttribute("inert", "");

      window.requestAnimationFrame(() => {
        this.panel.classList.add("is-open");
        const firstTarget =
          this.panel.querySelector("[data-mobile-nav-autofocus]") ||
          this.getFocusable()[0];
        firstTarget?.focus({ preventScroll: true });
      });
    }

    close(restoreFocus = true) {
      if (!this.open || !this.panel) {
        return;
      }

      this.open = false;
      this.panel.classList.remove("is-open");
      this.toggle.setAttribute("aria-expanded", "false");
      this.toggle.setAttribute("aria-label", "Buka menu navigasi");
      document.body.classList.remove("mobile-nav-open");
      document.querySelector("main")?.removeAttribute("inert");

      window.clearTimeout(this.closeTimer);
      this.closeTimer = window.setTimeout(() => {
        if (!this.open) {
          this.panel.hidden = true;
        }
      }, 260);

      if (restoreFocus && this.previousFocus instanceof HTMLElement) {
        this.previousFocus.focus({ preventScroll: true });
      }
    }

    getFocusable() {
      return Array.from(this.panel.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
        (element) =>
          !element.hasAttribute("hidden") &&
          element.offsetParent &&
          element.tabIndex >= 0,
      );
    }

    handleKeydown(event) {
      if (event.key === "Escape") {
        event.preventDefault();
        this.close();
        return;
      }

      if (event.key !== "Tab") {
        return;
      }

      const focusable = this.getFocusable();
      if (!focusable.length) {
        event.preventDefault();
        return;
      }

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    handleDesktopChange(event) {
      if (event.matches && this.open) {
        this.close(false);
      }
    }
  }

  const controllers = Array.from(document.querySelectorAll(NAV_SELECTOR)).map(
    (root) => {
      const controller = new MobileNavigation(root);
      controller.init();
      return controller;
    },
  );

  document.addEventListener("htmx:beforeRequest", () => {
    controllers.forEach((controller) => controller.close(false));
  });

  window.addEventListener("pagehide", () => {
    controllers.forEach((controller) => controller.close(false));
  });
})();
