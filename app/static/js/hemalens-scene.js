import * as THREE from "/static/vendor/three.module.js";

const SCENE_ID = "hemalens-scene";
const LANDING_PATH = "/partials/landing";

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function supportsWebGL() {
  try {
    const canvas = document.createElement("canvas");
    return Boolean(
      window.WebGLRenderingContext &&
        (canvas.getContext("webgl2") || canvas.getContext("webgl")),
    );
  } catch {
    return false;
  }
}

function requestPath(event) {
  const rawPath =
    event.detail?.pathInfo?.requestPath ??
    event.detail?.requestConfig?.path ??
    "";

  if (!rawPath) {
    return "";
  }

  try {
    return new URL(rawPath, window.location.href).pathname;
  } catch {
    return rawPath;
  }
}

class HemaLensSceneController {
  constructor() {
    this.active = false;
    this.animationFrame = null;
    this.root = null;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.geometry = null;
    this.materials = [];
    this.cells = [];
    this.clock = null;
    this.pointerTarget = new THREE.Vector2(0, 0);
    this.pointerCurrent = new THREE.Vector2(0, 0);
    this.resizeObserver = null;
    this.paused = false;

    this.handlePointerMove = this.handlePointerMove.bind(this);
    this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
    this.handleResize = this.handleResize.bind(this);
    this.animate = this.animate.bind(this);
  }

  init() {
    if (this.active || prefersReducedMotion() || !supportsWebGL()) {
      return;
    }

    const root = document.getElementById(SCENE_ID);
    if (!root) {
      return;
    }

    this.root = root;
    this.scene = new THREE.Scene();
    this.clock = new THREE.Clock();

    const width = Math.max(root.clientWidth, window.innerWidth);
    const height = Math.max(root.clientHeight, window.innerHeight);

    this.camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 120);
    this.camera.position.set(0, 0, 14);

    this.renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: window.innerWidth >= 768,
      powerPreference: "high-performance",
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    this.renderer.setSize(width, height, false);
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.domElement.setAttribute("aria-hidden", "true");
    this.renderer.domElement.className = "hemalens-scene__canvas";
    root.replaceChildren(this.renderer.domElement);

    this.addLighting();
    this.addCells(width);

    window.addEventListener("pointermove", this.handlePointerMove, {
      passive: true,
    });
    document.addEventListener("visibilitychange", this.handleVisibilityChange);

    this.resizeObserver = new ResizeObserver(this.handleResize);
    this.resizeObserver.observe(root);

    this.active = true;
    root.dataset.active = "true";
    this.animate();
  }

  addLighting() {
    const ambient = new THREE.AmbientLight(0x5b1b24, 1.25);
    const key = new THREE.DirectionalLight(0xff9aa7, 2.8);
    key.position.set(5, 7, 9);
    const rim = new THREE.PointLight(0xa60f2c, 45, 28, 2);
    rim.position.set(-7, -3, 6);

    this.scene.add(ambient, key, rim);
  }

  addCells(width) {
    this.geometry = new THREE.TorusGeometry(0.52, 0.19, 10, 28);

    const deepMaterial = new THREE.MeshStandardMaterial({
      color: 0x6e111d,
      roughness: 0.58,
      metalness: 0.02,
      transparent: true,
      opacity: 0.78,
    });
    const brightMaterial = new THREE.MeshStandardMaterial({
      color: 0xa61e31,
      roughness: 0.52,
      metalness: 0.01,
      transparent: true,
      opacity: 0.72,
    });
    this.materials = [deepMaterial, brightMaterial];

    const mobile = width < 768;
    const count = mobile ? 16 : 34;
    const horizontalSpread = mobile ? 12 : 24;
    const verticalSpread = mobile ? 16 : 14;

    for (let index = 0; index < count; index += 1) {
      const material = this.materials[index % this.materials.length];
      const cell = new THREE.Mesh(this.geometry, material);
      const scale = 0.55 + Math.random() * 1.25;

      cell.scale.set(scale, scale, 0.46 + Math.random() * 0.22);
      cell.position.set(
        (Math.random() - 0.5) * horizontalSpread,
        (Math.random() - 0.5) * verticalSpread,
        -4 + Math.random() * 10,
      );
      cell.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        Math.random() * Math.PI,
      );
      cell.userData = {
        driftX: (Math.random() - 0.5) * 0.0024,
        driftY: 0.0015 + Math.random() * 0.004,
        rotationX: (Math.random() - 0.5) * 0.0018,
        rotationY: (Math.random() - 0.5) * 0.0022,
        baseX: cell.position.x,
        phase: Math.random() * Math.PI * 2,
      };

      this.cells.push(cell);
      this.scene.add(cell);
    }
  }

  handlePointerMove(event) {
    this.pointerTarget.set(
      (event.clientX / window.innerWidth - 0.5) * 2,
      (event.clientY / window.innerHeight - 0.5) * 2,
    );
  }

  handleVisibilityChange() {
    this.paused = document.hidden;
    if (!this.paused && this.active) {
      this.clock.getDelta();
    }
  }

  handleResize() {
    if (!this.root || !this.camera || !this.renderer) {
      return;
    }

    const width = Math.max(this.root.clientWidth, 1);
    const height = Math.max(this.root.clientHeight, 1);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }

  animate() {
    if (!this.active) {
      return;
    }

    this.animationFrame = window.requestAnimationFrame(this.animate);
    if (this.paused) {
      return;
    }

    const elapsed = this.clock.getElapsedTime();
    this.pointerCurrent.lerp(this.pointerTarget, 0.035);

    this.cells.forEach((cell, index) => {
      const data = cell.userData;
      cell.position.y += data.driftY;
      cell.position.x += data.driftX;
      cell.position.x =
        data.baseX + Math.sin(elapsed * 0.18 + data.phase) * 0.55;
      cell.rotation.x += data.rotationX;
      cell.rotation.y += data.rotationY;
      cell.rotation.z += 0.0008 + index * 0.000003;

      if (cell.position.y > 8.5) {
        cell.position.y = -8.5;
      }
    });

    this.camera.position.x +=
      (this.pointerCurrent.x * 0.8 - this.camera.position.x) * 0.025;
    this.camera.position.y +=
      (-this.pointerCurrent.y * 0.5 - this.camera.position.y) * 0.025;
    this.camera.lookAt(0, 0, 0);
    this.renderer.render(this.scene, this.camera);
  }

  destroy() {
    if (!this.active && !this.root) {
      return;
    }

    this.active = false;
    this.paused = false;

    if (this.animationFrame !== null) {
      window.cancelAnimationFrame(this.animationFrame);
      this.animationFrame = null;
    }

    window.removeEventListener("pointermove", this.handlePointerMove);
    document.removeEventListener(
      "visibilitychange",
      this.handleVisibilityChange,
    );
    this.resizeObserver?.disconnect();
    this.resizeObserver = null;

    this.cells.forEach((cell) => this.scene?.remove(cell));
    this.cells = [];

    this.geometry?.dispose();
    this.geometry = null;
    this.materials.forEach((material) => material.dispose());
    this.materials = [];

    if (this.renderer) {
      this.renderer.renderLists?.dispose();
      this.renderer.dispose();
      this.renderer.forceContextLoss?.();
      this.renderer.domElement.remove();
    }

    if (this.root) {
      this.root.dataset.active = "false";
      this.root.replaceChildren();
    }

    this.scene?.clear();
    this.root = null;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.clock = null;
    this.pointerTarget.set(0, 0);
    this.pointerCurrent.set(0, 0);
  }
}

const controller = new HemaLensSceneController();
window.HemaLensScene = controller;

function initializeScene() {
  if (document.querySelector("#main-workspace section")) {
    controller.init();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeScene, { once: true });
} else {
  initializeScene();
}

document.addEventListener("htmx:beforeRequest", (event) => {
  const path = requestPath(event);
  if (path && path !== LANDING_PATH) {
    controller.destroy();
  }
});

document.addEventListener("htmx:afterSwap", (event) => {
  const path = requestPath(event);
  if (path === LANDING_PATH) {
    controller.init();
  } else if (path) {
    controller.destroy();
  }
});

window.addEventListener("pagehide", () => controller.destroy(), { once: true });
