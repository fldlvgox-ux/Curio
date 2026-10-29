/**
 * Curio Data Adapter: Markdown Table (curio-data-markdown-table)
 * Standardized adapter for bidirectional import/export between Curio items and Markdown tables.
 */

export default {
  /**
   * Parse Markdown content into Curio Item objects.
   * Supports both GitHub Flavored Markdown (GFM) tables and checklist bullet points.
   *
   * @param {string} raw - Raw markdown text
   * @param {Object} api - DataExtensionAPI sandbox
   * @param {Object} options - Custom options (e.g. defaultDrawer)
   * @returns {Array<Object>} List of parsed items
   */
  parse(raw, api, options = {}) {
    if (!raw || typeof raw !== 'string') return [];

    const lines = raw.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    const items = [];

    // Check if markdown contains a table (lines starting and ending with |)
    const tableLines = lines.filter(l => l.startsWith('|') && l.endsWith('|'));

    if (tableLines.length >= 2) {
      // Parse Table Header
      const headerLine = tableLines[0];
      const headers = headerLine
        .split('|')
        .slice(1, -1)
        .map(h => h.trim().toLowerCase());

      // Find index mapping
      const titleIdx = headers.findIndex(h => h.includes('title') || h.includes('name') || h.includes('item'));
      const drawerIdx = headers.findIndex(h => h.includes('drawer') || h.includes('category') || h.includes('folder'));
      const statusIdx = headers.findIndex(h => h.includes('status') || h.includes('state'));
      const tagsIdx = headers.findIndex(h => h.includes('tag'));
      const ratingIdx = headers.findIndex(h => h.includes('rating') || h.includes('score'));
      const notesIdx = headers.findIndex(h => h.includes('note') || h.includes('desc'));
      const linkIdx = headers.findIndex(h => h.includes('link') || h.includes('url'));

      // Process rows (skip header and separator row)
      const dataRows = tableLines.slice(2);
      for (const row of dataRows) {
        // Skip separator row if not caught
        if (/^\|[-:\s|]+\|$/.test(row)) continue;

        const cells = row.split('|').slice(1, -1).map(c => c.trim());
        const title = (titleIdx !== -1 && cells[titleIdx]) ? cells[titleIdx] : (cells[0] || '');
        if (!title) continue;

        const drawer = (drawerIdx !== -1 && cells[drawerIdx]) ? cells[drawerIdx] : (options.defaultDrawer || api.getDefaultDrawer());
        const status = (statusIdx !== -1 && cells[statusIdx]) ? cells[statusIdx] : 'Idea';
        const rawTags = (tagsIdx !== -1 && cells[tagsIdx]) ? cells[tagsIdx] : '';
        const tags = rawTags.split(/[,;\s]+/).map(t => t.replace(/^#/, '').trim()).filter(Boolean);
        const rating = (ratingIdx !== -1 && cells[ratingIdx]) ? parseInt(cells[ratingIdx], 10) || 0 : 0;
        const notes = (notesIdx !== -1 && cells[notesIdx]) ? cells[notesIdx] : '';
        const link = (linkIdx !== -1 && cells[linkIdx]) ? cells[linkIdx] : '';

        items.push(api.createItem({
          title,
          drawer,
          status,
          tags,
          rating,
          notes,
          link
        }));
      }
    } else {
      // Fallback: Parse task/bullet lists (- [ ] Title #tag (Drawer))
      for (const line of lines) {
        const bulletMatch = line.match(/^[-*+]\s+(?:\[([ xX])\]\s+)?(.+)$/);
        if (bulletMatch) {
          const isDone = bulletMatch[1] && bulletMatch[1].toLowerCase() === 'x';
          let text = bulletMatch[2].trim();

          // Extract tags #tag
          const tags = [];
          text = text.replace(/#([\w-]+)/g, (_, t) => {
            tags.push(t);
            return '';
          });

          // Extract drawer in parentheses (Drawer)
          let drawer = options.defaultDrawer || api.getDefaultDrawer();
          const drawerMatch = text.match(/\(([^)]+)\)$/);
          if (drawerMatch) {
            drawer = drawerMatch[1].trim();
            text = text.replace(/\(([^)]+)\)$/, '').trim();
          }

          items.push(api.createItem({
            title: text || 'Untitled Item',
            drawer,
            status: isDone ? 'Completed' : 'Idea',
            tags,
            notes: ''
          }));
        }
      }
    }

    return items;
  },

  /**
   * Serialize Curio items into Markdown table format.
   *
   * @param {Array<Object>} items - Array of Curio items
   * @param {Object} catalog - Active catalog metadata
   * @param {Object} api - DataExtensionAPI sandbox
   * @param {Object} options - Custom serialize options
   * @returns {string} Markdown text
   */
  serialize(items = [], catalog = {}, api, options = {}) {
    const catalogName = catalog.name || 'Catalog';
    const timestamp = new Date().toLocaleDateString();

    let out = `# ${catalogName}\n`;
    out += `> Exported from Curio on ${timestamp} (${items.length} items)\n\n`;

    out += '| Title | Drawer | Status | Tags | Rating | Notes | Link |\n';
    out += '| :--- | :--- | :--- | :--- | :---: | :--- | :--- |\n';

    for (const item of items) {
      const escapePipe = str => String(str || '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
      const title = escapePipe(item.title);
      const drawer = escapePipe(item.drawer || 'Inbox');
      const status = escapePipe(item.status || 'Idea');
      const tags = (item.tags || []).join(', ');
      const rating = item.rating || 0;
      const notes = escapePipe(item.notes);
      const link = escapePipe(item.link);

      out += `| ${title} | ${drawer} | ${status} | ${tags} | ${rating} | ${notes} | ${link} |\n`;
    }

    return out;
  }
};
