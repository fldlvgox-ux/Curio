/**
 * Curio Component Plugin Architecture & Extension API (v1.0.0)
 * Allows third-party and AI-authored widgets to mount into Curio with a controlled API.
 */

export class ComponentAPI {
  /**
   * @param {string} pluginId - Unique ID of the component plugin
   * @param {HTMLElement} containerElement - Root DOM container for this component
   * @param {Object} hostContext - Accessors to Curio state and actions
   */
  constructor(pluginId, containerElement, hostContext = {}) {
    this.pluginId = pluginId;
    this.container = containerElement;
    this._listeners = new Map();
    this._host = hostContext;

    // Namespaced local storage
    this.storage = {
      get: (key, fallback = null) => {
        try {
          if (typeof localStorage === 'undefined') return fallback;
          const val = localStorage.getItem(`curio_comp_${this.pluginId}_${key}`);
          return val !== null ? JSON.parse(val) : fallback;
        } catch {
          return fallback;
        }
      },
      set: (key, val) => {
        try {
          if (typeof localStorage === 'undefined') return;
          localStorage.setItem(`curio_comp_${this.pluginId}_${key}`, JSON.stringify(val));
        } catch (e) {
          console.warn(`[ComponentAPI:${this.pluginId}] Storage set error:`, e);
        }
      },
      remove: (key) => {
        try {
          if (typeof localStorage === 'undefined') return;
          localStorage.removeItem(`curio_comp_${this.pluginId}_${key}`);
        } catch {}
      }
    };

    // State getters (safe read-only copies)
    this.state = {
      getActiveCatalog: () => this._host.getActiveCatalog ? this._host.getActiveCatalog() : null,
      getCatalogs: () => this._host.getCatalogs ? this._host.getCatalogs() : [],
      getItems: () => this._host.getItems ? this._host.getItems() : [],
      getDrawers: () => this._host.getDrawers ? this._host.getDrawers() : [],
      getActiveView: () => this._host.getActiveView ? this._host.getActiveView() : 'grid'
    };
  }

  /**
   * Show notification toast using Curio's toast engine.
   */
  showToast(message, type = 'info') {
    if (typeof window.showToast === 'function') {
      window.showToast(message, type);
    } else {
      console.log(`[Toast ${type}]`, message);
    }
  }

  /**
   * Subscribe to Curio application events.
   */
  on(eventName, handler) {
    const wrapped = (e) => handler(e.detail);
    this._listeners.set(handler, { eventName, wrapped });
    window.addEventListener(`curio:${eventName}`, wrapped);
  }

  /**
   * Unsubscribe from Curio application events.
   */
  off(eventName, handler) {
    const entry = this._listeners.get(handler);
    if (entry && entry.eventName === eventName) {
      window.removeEventListener(`curio:${eventName}`, entry.wrapped);
      this._listeners.delete(handler);
    }
  }

  /**
   * Emit custom component event.
   */
  emit(eventName, detail = {}) {
    window.dispatchEvent(new CustomEvent(`curio:component:${this.pluginId}:${eventName}`, { detail }));
  }

  /**
   * Cleans up all event listeners when the component unmounts.
   */
  destroy() {
    for (const { eventName, wrapped } of this._listeners.values()) {
      window.removeEventListener(`curio:${eventName}`, wrapped);
    }
    this._listeners.clear();
    if (this.container) {
      this.container.innerHTML = '';
    }
  }
}

/**
 * Manages discovery, mounting, and lifecycle of Component Plugins.
 */
export class ComponentManager {
  constructor(loader) {
    this.loader = loader;
    this.activeComponents = new Map(); // id -> { instance, api, styleTag, container }
    this.mountPoints = {
      'sidebar-top': 'extension-slot-sidebar-top',
      'sidebar-bottom': 'extension-slot-sidebar-bottom',
      'toolbar-actions': 'extension-slot-toolbar-actions',
      'floating-widget': 'extension-slot-floating-widget'
    };
  }

  /**
   * Mounts a component plugin into its declared mount point.
   */
  async mount(componentId, manifest, implementation, templateHtml = '', scopedCss = '') {
    if (this.activeComponents.has(componentId)) {
      this.unmount(componentId);
    }

    const mountSlotId = this.mountPoints[manifest.mountPoint] || this.mountPoints['floating-widget'];
    let container = document.getElementById(mountSlotId);

    // If slot doesn't exist, create it or use body fallback for floating widgets
    if (!container) {
      container = document.createElement('div');
      container.id = mountSlotId;
      if (manifest.mountPoint === 'floating-widget') {
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
      }
      document.body.appendChild(container);
    }

    // 1. Scoped CSS
    let styleTag = null;
    if (scopedCss) {
      styleTag = document.createElement('style');
      styleTag.id = `curio-comp-style-${componentId}`;
      styleTag.textContent = scopedCss;
      document.head.appendChild(styleTag);
    }

    // 2. Component Wrapper
    const wrapper = document.createElement('div');
    wrapper.className = `curio-component-root curio-comp-${componentId}`;
    wrapper.innerHTML = templateHtml;
    container.appendChild(wrapper);

    // 3. API Sandbox
    const api = new ComponentAPI(componentId, wrapper, {
      getActiveCatalog: () => window.State ? window.State.catalogs.find(c => c.id === window.State.activeCatalogId) : null,
      getCatalogs: () => window.State ? window.State.catalogs : [],
      getItems: () => window.State ? (window.State.catalogs.find(c => c.id === window.State.activeCatalogId)?.items || []) : [],
      getDrawers: () => window.State ? (window.State.catalogs.find(c => c.id === window.State.activeCatalogId)?.drawers || []) : [],
      getActiveView: () => window.State ? window.State.viewMode : 'grid'
    });

    // 4. Initialize Lifecycle
    let instance = null;
    if (typeof implementation === 'function') {
      instance = new implementation(api);
    } else if (implementation && typeof implementation.init === 'function') {
      instance = implementation;
      await instance.init(api);
    }

    this.activeComponents.set(componentId, {
      manifest,
      instance,
      api,
      styleTag,
      wrapper,
      container
    });

    console.log(`[ComponentManager] Mounted "${manifest.name}" to slot "${manifest.mountPoint}"`);
    return api;
  }

  /**
   * Unmounts and tears down an active component plugin.
   */
  unmount(componentId) {
    const entry = this.activeComponents.get(componentId);
    if (!entry) return;

    if (entry.instance && typeof entry.instance.destroy === 'function') {
      try {
        entry.instance.destroy();
      } catch (e) {
        console.warn(`[ComponentManager] Error during unmount of ${componentId}:`, e);
      }
    }

    if (entry.api) entry.api.destroy();
    if (entry.styleTag && entry.styleTag.parentNode) entry.styleTag.parentNode.removeChild(entry.styleTag);
    if (entry.wrapper && entry.wrapper.parentNode) entry.wrapper.parentNode.removeChild(entry.wrapper);

    this.activeComponents.delete(componentId);
    console.log(`[ComponentManager] Unmounted "${componentId}"`);
  }
}
