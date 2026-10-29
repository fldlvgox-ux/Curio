/**
 * Curio Data Adapter Starter Template
 * Implements parse() and serialize() for line-delimited plain text items.
 */

export default {
  /**
   * Parse plain text lines into Curio Item objects.
   * Format: Title | Drawer | Tags (comma-separated) | Notes
   */
  async parse(raw, api, options = {}) {
    if (!raw || typeof raw !== 'string') return [];

    const lines = raw.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    const items = [];

    for (const line of lines) {
      if (line.startsWith('#')) continue; // Skip comments

      const parts = line.split('|').map(p => p.trim());
      const title = parts[0] || 'Untitled Item';
      const drawer = parts[1] || options.defaultDrawer || api.getDefaultDrawer();
      const tags = parts[2] ? parts[2].split(',').map(t => t.trim()).filter(Boolean) : [];
      const notes = parts[3] || '';

      items.push(api.createItem({
        title,
        drawer,
        tags,
        notes
      }));
    }

    return items;
  },

  /**
   * Serialize Curio items into line-delimited text.
   */
  async serialize(items = [], catalog = {}, api, options = {}) {
    let output = `# Curio Export - ${catalog.name || 'Catalog'}\n`;
    output += `# Format: Title | Drawer | Tags | Notes\n\n`;

    for (const item of items) {
      const title = (item.title || '').replace(/\|/g, '-');
      const drawer = (item.drawer || 'Inbox').replace(/\|/g, '-');
      const tags = (item.tags || []).join(', ');
      const notes = (item.notes || '').replace(/\|/g, '-').replace(/\r?\n/g, ' ');

      output += `${title} | ${drawer} | ${tags} | ${notes}\n`;
    }

    return output;
  }
};
