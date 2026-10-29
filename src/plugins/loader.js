/**
 * Curio Universal Plugin Loader (Zero-Build ES Module)
 * Discovers, sanitizes, activates, and manages Curio themes and plugins.
 */

import { sanitizeThemeCSS, sanitizeSVG } from './sanitizer.js';

export class PluginLoader {
  constructor(options = {}) {
    this.indexUrl = options.indexUrl || './plugins/plugin-index.json';
    this.contractUrl = options.contractUrl || './src/plugins/contract.json';
    this.plugins = new Map(); // id -> { manifest, css, status, path }
    this.activeThemeId = null;
    this.contract = null;
    this.styleTagId = 'curio-active-theme-styles';
  }

  /**
   * Initializes the loader by reading the contract and registry index.
   */
  async init() {
    try {
      const contractRes = await fetch(this.contractUrl);
      if (contractRes.ok) {
        this.contract = await contractRes.json();
      }
    } catch (err) {
      console.warn('[PluginLoader] Could not load contract.json, using fallback defaults.', err);
    }

    await this.refreshIndex();
  }

  /**
   * Reads plugins/plugin-index.json to discover available plugins.
   */
  async refreshIndex() {
    try {
      const res = await fetch(this.indexUrl + '?t=' + Date.now());
      if (!res.ok) {
        console.warn('[PluginLoader] No plugin-index.json found or unreadable.');
        return [];
      }
      const data = await res.json();
      const list = Array.isArray(data.plugins) ? data.plugins : [];

      for (const item of list) {
        if (item.id && !this.plugins.has(item.id)) {
          this.plugins.set(item.id, {
            ...item,
            status: 'registered',
            loadedCss: null
          });
        }
      }
      return Array.from(this.plugins.values());
    } catch (err) {
      console.warn('[PluginLoader] Error reading plugin index:', err);
      return [];
    }
  }

  /**
   * Returns list of all registered plugins, optionally filtered by type.
   */
  getPlugins(type = null) {
    const all = Array.from(this.plugins.values());
    return type ? all.filter(p => p.type === type) : all;
  }

  /**
   * Loads a plugin's manifest and assets from its relative path.
   */
  async loadPluginFromPath(pluginPath) {
    try {
      const manifestUrl = `${pluginPath}/manifest.json`;
      const mRes = await fetch(manifestUrl);
      if (!mRes.ok) throw new Error(`Failed to load manifest at ${manifestUrl}`);
      const manifest = await mRes.json();

      let cssContent = '';
      if (manifest.files && manifest.files.css) {
        const cssUrl = `${pluginPath}/${manifest.files.css}`;
        const cRes = await fetch(cssUrl);
        if (cRes.ok) {
          cssContent = await cRes.text();
        }
      }

      // Security check
      const check = sanitizeThemeCSS(cssContent, manifest.id);
      if (!check.valid) {
        throw new Error(`Plugin ${manifest.id} failed security validation:\n${check.errors.join('\n')}`);
      }

      const pluginData = {
        ...manifest,
        path: pluginPath,
        status: 'ready',
        sanitizedCss: check.sanitizedCss,
        warnings: check.warnings
      };

      this.plugins.set(manifest.id, pluginData);
      return pluginData;
    } catch (err) {
      console.error(`[PluginLoader] Failed loading plugin at ${pluginPath}:`, err);
      throw err;
    }
  }

  /**
   * Activates a theme plugin by injecting its tokens and scoped CSS.
   */
  async activateTheme(themeId) {
    // If selecting built-in 'cyber' or default, clear plugin styles
    if (!themeId || themeId === 'cyber') {
      this.clearActivePluginStyle();
      this.activeThemeId = 'cyber';
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('curio_active_theme', 'cyber');
      this.notifyThemeChanged('cyber');
      return true;
    }

    let plugin = this.plugins.get(themeId);

    // If registered but not yet loaded, load it
    if (plugin && !plugin.sanitizedCss && plugin.path) {
      plugin = await this.loadPluginFromPath(plugin.path);
    }

    if (!plugin) {
      console.warn(`[PluginLoader] Theme plugin "${themeId}" not found in registry.`);
      return false;
    }

    // 1. Build Token Variable Block
    let tokenCss = '';
    if (plugin.tokens && typeof plugin.tokens === 'object') {
      const tokenEntries = Object.entries(plugin.tokens)
        .map(([k, v]) => `  ${k}: ${v};`)
        .join('\n');
      tokenCss = `[data-theme="${themeId}"] {\n${tokenEntries}\n}\n`;
    }

    // 2. Inject Combined Styles into DOM
    const fullCss = `${tokenCss}\n${plugin.sanitizedCss || ''}`;
    this.injectStyleTag(fullCss);

    // 3. Set root attribute
    document.documentElement.setAttribute('data-theme', themeId);
    this.activeThemeId = themeId;
    localStorage.setItem('curio_active_theme', themeId);

    this.notifyThemeChanged(themeId, plugin);
    return true;
  }

  /**
   * Injects or replaces the active theme stylesheet.
   */
  injectStyleTag(cssText) {
    let tag = document.getElementById(this.styleTagId);
    if (!tag) {
      tag = document.createElement('style');
      tag.id = this.styleTagId;
      document.head.appendChild(tag);
    }
    tag.textContent = cssText;
  }

  /**
   * Removes injected theme stylesheet.
   */
  clearActivePluginStyle() {
    const tag = document.getElementById(this.styleTagId);
    if (tag) {
      tag.textContent = '';
    }
  }

  /**
   * Emits custom event for UI updates.
   */
  notifyThemeChanged(themeId, plugin = null) {
    window.dispatchEvent(new CustomEvent('curio:theme-changed', {
      detail: { themeId, plugin }
    }));
  }
}

// Global singleton instance for easy host integration
export const CurioPlugins = new PluginLoader();
