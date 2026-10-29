/**
 * Curio Quick Stats HUD Component Controller
 */

export default {
  async init(api) {
    this.api = api;

    const rootEl = api.container.querySelector('#hud-root');
    const catEl = api.container.querySelector('#hud-val-catalog');
    const itemsEl = api.container.querySelector('#hud-val-items');
    const drawersEl = api.container.querySelector('#hud-val-drawers');
    const viewEl = api.container.querySelector('#hud-val-view');
    const toggleBtn = api.container.querySelector('#hud-toggle-btn');
    const closeBtn = api.container.querySelector('#hud-close-btn');
    const pingBtn = api.container.querySelector('#hud-btn-ping');

    // 1. Reactive refresh function
    const updateStats = () => {
      const activeCat = api.state.getActiveCatalog();
      const items = api.state.getItems();
      const drawers = api.state.getDrawers();
      const viewMode = api.state.getActiveView();

      if (catEl) catEl.innerText = activeCat ? (activeCat.icon ? activeCat.icon + ' ' : '') + activeCat.name : 'All Catalogs';
      if (itemsEl) itemsEl.innerText = items.length.toLocaleString();
      if (drawersEl) drawersEl.innerText = drawers.length.toLocaleString();
      if (viewEl) viewEl.innerText = (viewMode || 'GRID').toUpperCase() + ' MODE';
    };

    updateStats();

    // 2. Minimize / Expand toggle with persistent state
    let isMinimized = api.storage.get('minimized', false);
    if (isMinimized && rootEl) rootEl.classList.add('minimized');

    if (toggleBtn && rootEl) {
      toggleBtn.addEventListener('click', () => {
        isMinimized = !isMinimized;
        rootEl.classList.toggle('minimized', isMinimized);
        api.storage.set('minimized', isMinimized);
        toggleBtn.innerText = isMinimized ? '□' : '_';
      });
    }

    // 3. Ping State Button
    if (pingBtn) {
      pingBtn.addEventListener('click', () => {
        const cat = api.state.getActiveCatalog();
        const count = api.state.getItems().length;
        api.showToast(`Catalog "${cat ? cat.name : 'Default'}" contains ${count} items. 📊`, 'info');
      });
    }

    // 4. Dismiss button
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        api.container.style.display = 'none';
        api.showToast('HUD dismissed. Click Refresh in Settings to restore.', 'info');
      });
    }

    // 5. Periodic polling + event listeners
    this._pollTimer = setInterval(updateStats, 1500);

    this._onCatalogChange = () => updateStats();
    this._onThemeChange = () => updateStats();
    api.on('catalog-changed', this._onCatalogChange);
    api.on('theme-changed', this._onThemeChange);
  },

  destroy() {
    if (this._pollTimer) {
      clearInterval(this._pollTimer);
    }
    if (this.api) {
      if (this._onCatalogChange) this.api.off('catalog-changed', this._onCatalogChange);
      if (this._onThemeChange) this.api.off('theme-changed', this._onThemeChange);
    }
  }
};
