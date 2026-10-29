/**
 * Curio Data Extension Architecture & API (v1.0.0)
 * Enables modular, drop-in data adapters for importing and exporting Curio catalog items
 * (Markdown, CSV, Notion, JSON-LD, etc.) without altering core app.html logic.
 */

export class DataExtensionAPI {
  /**
   * @param {string} pluginId - Unique ID of the data extension plugin
   * @param {Object} hostContext - Safe accessors to Curio state and actions
   */
  constructor(pluginId, hostContext = {}) {
    this.pluginId = pluginId;
    this._host = hostContext;
  }

  /**
   * Safe item factory ensuring all required Curio item fields are present.
   * @param {Object} data - Raw item properties
   * @returns {Object} Complete Curio item structure
   */
  createItem(data = {}) {
    const now = new Date().toISOString();
    return {
      id: data.id || `item-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      title: (data.title || 'Untitled Item').trim(),
      drawer: data.drawer || this.getDefaultDrawer(),
      status: data.status || 'Idea',
      tags: Array.isArray(data.tags) ? data.tags.map(t => String(t).trim()).filter(Boolean) : [],
      rating: Number(data.rating) || 0,
      link: data.link || '',
      notes: data.notes || '',
      logo: data.logo || '',
      gallery: Array.isArray(data.gallery) ? data.gallery : [],
      dateAdded: data.dateAdded || now,
      dateModified: data.dateModified || now
    };
  }

  /**
   * Get active catalog summary.
   */
  getActiveCatalog() {
    if (this._host.getActiveCatalog) return this._host.getActiveCatalog();
    if (typeof window !== 'undefined' && window.State && window.State.activeCatalog) {
      return window.State.activeCatalog;
    }
    return { id: 'default', name: 'Default', drawers: [], items: [] };
  }

  /**
   * Get drawers in active catalog.
   */
  getDrawers() {
    if (this._host.getDrawers) return this._host.getDrawers();
    if (typeof window !== 'undefined' && window.State && window.State.drawers) {
      return [...window.State.drawers];
    }
    return [];
  }

  /**
   * Get default drawer name.
   */
  getDefaultDrawer() {
    const drawers = this.getDrawers();
    return drawers.length > 0 ? drawers[0] : 'Inbox';
  }

  /**
   * Trigger a user-facing toast notification.
   */
  showToast(message, type = 'info') {
    if (typeof window !== 'undefined' && typeof window.showToast === 'function') {
      window.showToast(message, type);
    } else {
      console.log(`[DataExtension:${this.pluginId}] [${type}] ${message}`);
    }
  }

  /**
   * Sanitize text against XSS/injection before injecting into notes/titles.
   */
  sanitizeText(text) {
    if (!text) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
}

export class DataExtensionManager {
  constructor(hostContext = {}) {
    this._host = hostContext;
    this._adapters = new Map(); // id -> { manifest, adapter, api }
  }

  /**
   * Register a new data adapter plugin.
   * @param {Object} manifest - Plugin manifest
   * @param {Object} adapter - Implementation with parse() and/or serialize()
   */
  register(manifest, adapter) {
    if (!manifest || !manifest.id) {
      throw new Error('[DataExtensionManager] Manifest must provide a valid id');
    }
    if (!adapter || (typeof adapter.parse !== 'function' && typeof adapter.serialize !== 'function')) {
      throw new Error(`[DataExtensionManager] Adapter '${manifest.id}' must provide parse() and/or serialize()`);
    }

    const api = new DataExtensionAPI(manifest.id, this._host);
    this._adapters.set(manifest.id, {
      manifest,
      adapter,
      api
    });

    console.log(`[DataExtensionManager] Registered data extension '${manifest.name || manifest.id}'`);
    return api;
  }

  /**
   * Unregister an adapter by plugin ID.
   */
  unregister(id) {
    return this._adapters.delete(id);
  }

  /**
   * Get registration record by ID.
   */
  get(id) {
    return this._adapters.get(id);
  }

  /**
   * Find matching adapter by file extension (e.g. '.md', '.csv').
   */
  findByExtension(ext) {
    const cleanExt = ext.startsWith('.') ? ext.toLowerCase() : `.${ext.toLowerCase()}`;
    for (const [id, record] of this._adapters.entries()) {
      const de = record.manifest.dataExtension;
      if (de && Array.isArray(de.fileExtensions) && de.fileExtensions.includes(cleanExt)) {
        return record;
      }
    }
    return null;
  }

  /**
   * Find matching adapter by format key (e.g. 'markdown', 'csv').
   */
  findByFormat(format) {
    const cleanFmt = format.toLowerCase().trim();
    for (const [id, record] of this._adapters.entries()) {
      if (id === cleanFmt || id === `curio-data-${cleanFmt}`) return record;
      const de = record.manifest.dataExtension;
      if (de && Array.isArray(de.formats) && de.formats.includes(cleanFmt)) {
        return record;
      }
    }
    return null;
  }

  /**
   * List all registered data adapters.
   */
  list() {
    return Array.from(this._adapters.values()).map(r => ({
      id: r.manifest.id,
      name: r.manifest.name,
      description: r.manifest.description,
      dataExtension: r.manifest.dataExtension,
      modes: (r.manifest.dataExtension && r.manifest.dataExtension.modes) || ['import']
    }));
  }

  /**
   * Parse raw text content and import items into the active Curio catalog.
   * @param {string} raw - File content
   * @param {string} formatOrId - Extension or adapter ID
   * @param {Object} options - Custom options (e.g. default drawer)
   * @returns {Promise<Object>} Import summary { success, count, items, errors }
   */
  async importData(raw, formatOrId, options = {}) {
    const record = this.findByFormat(formatOrId) || this.findByExtension(formatOrId) || this.get(formatOrId);
    if (!record) {
      throw new Error(`[DataExtensionManager] No adapter found for format/id '${formatOrId}'`);
    }

    if (typeof record.adapter.parse !== 'function') {
      throw new Error(`[DataExtensionManager] Adapter '${record.manifest.id}' does not support import`);
    }

    const rawItems = await record.adapter.parse(raw, record.api, options);
    if (!Array.isArray(rawItems)) {
      throw new Error(`[DataExtensionManager] Adapter did not return an array of items`);
    }

    const sanitizedItems = rawItems.map(item => record.api.createItem(item));

    // If running in browser environment with live Curio State, insert directly
    if (typeof window !== 'undefined' && window.State && Array.isArray(window.State.items)) {
      // Ensure any newly introduced drawers exist in catalog
      const existingDrawers = new Set(window.State.drawers || []);
      sanitizedItems.forEach(item => {
        if (item.drawer && !existingDrawers.has(item.drawer)) {
          window.State.drawers.push(item.drawer);
          existingDrawers.add(item.drawer);
        }
      });

      // Insert at top of items
      window.State.items.unshift(...sanitizedItems);

      if (typeof window.saveState === 'function') await window.saveState();
      if (typeof window.renderAll === 'function') window.renderAll();
      if (typeof window.renderDrawers === 'function') window.renderDrawers();

      record.api.showToast(`Imported ${sanitizedItems.length} items via ${record.manifest.name}`, 'success');
    }

    return {
      success: true,
      count: sanitizedItems.length,
      items: sanitizedItems
    };
  }

  /**
   * Export active catalog items to text format using an adapter.
   * @param {string} formatOrId - Extension or adapter ID
   * @param {Object} options - Options (e.g. filter by drawer)
   * @returns {Promise<string>} Serialized output
   */
  async exportData(formatOrId, options = {}) {
    const record = this.findByFormat(formatOrId) || this.findByExtension(formatOrId) || this.get(formatOrId);
    if (!record) {
      throw new Error(`[DataExtensionManager] No adapter found for format/id '${formatOrId}'`);
    }

    if (typeof record.adapter.serialize !== 'function') {
      throw new Error(`[DataExtensionManager] Adapter '${record.manifest.id}' does not support export`);
    }

    const items = options.items || (typeof window !== 'undefined' && window.State ? window.State.items : []);
    const catalog = options.catalog || record.api.getActiveCatalog();

    return await record.adapter.serialize(items, catalog, record.api, options);
  }
}

// Global browser instance
if (typeof window !== 'undefined') {
  window.CurioData = window.CurioData || new DataExtensionManager();
}
