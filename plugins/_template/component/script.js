/**
 * Curio Component Starter Implementation
 */

export default {
  async init(api) {
    this.api = api;

    // Display active catalog name
    const catEl = api.container.querySelector('#comp-active-cat');
    const updateCatalogDisplay = () => {
      const activeCat = api.state.getActiveCatalog();
      if (catEl) {
        catEl.innerText = activeCat ? activeCat.name : 'None';
      }
    };
    updateCatalogDisplay();

    // Button click interaction
    const actionBtn = api.container.querySelector('.starter-widget-btn');
    if (actionBtn) {
      actionBtn.addEventListener('click', () => {
        const count = (api.storage.get('click_count', 0)) + 1;
        api.storage.set('click_count', count);
        api.showToast(`Widget clicked ${count} time(s)! 🎉`, 'success');
      });
    }

    // Close button
    const closeBtn = api.container.querySelector('.starter-widget-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        api.container.style.display = 'none';
      });
    }

    // Subscribe to catalog change events
    this._onCatalogChange = () => updateCatalogDisplay();
    api.on('catalog-changed', this._onCatalogChange);
  },

  destroy() {
    if (this.api && this._onCatalogChange) {
      this.api.off('catalog-changed', this._onCatalogChange);
    }
  }
};
