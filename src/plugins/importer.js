/**
 * Curio Theme & Plugin Importer
 * Unpacks .zip theme packages in the browser/client, validates them, and registers them.
 */

import { sanitizeThemeCSS } from './sanitizer.js';

export async function importThemeZip(zipFile, curioPluginLoader) {
  if (!window.JSZip) {
    throw new Error('JSZip library is required for importing theme packages.');
  }

  try {
    const zip = await window.JSZip.loadAsync(zipFile);

    // 1. Locate manifest.json (could be at root or inside a top-level directory)
    let manifestFile = null;
    let rootPrefix = '';

    for (const relativePath in zip.files) {
      if (relativePath.endsWith('manifest.json') && !zip.files[relativePath].dir) {
        manifestFile = zip.files[relativePath];
        if (relativePath.includes('/')) {
          rootPrefix = relativePath.substring(0, relativePath.lastIndexOf('/') + 1);
        }
        break;
      }
    }

    if (!manifestFile) {
      throw new Error('Invalid theme package: manifest.json not found in ZIP archive.');
    }

    const manifestText = await manifestFile.async('text');
    const manifest = JSON.parse(manifestText);

    if (!manifest.id || !manifest.name) {
      throw new Error('Invalid manifest: missing "id" or "name".');
    }

    // 2. Locate CSS file
    const cssFileName = manifest.files && manifest.files.css ? manifest.files.css : 'theme.css';
    const fullCssPath = rootPrefix + cssFileName;
    const cssFile = zip.files[fullCssPath];

    if (!cssFile) {
      throw new Error(`CSS file "${cssFileName}" declared in manifest was not found in ZIP archive.`);
    }

    const rawCss = await cssFile.async('text');

    // 3. Security Sanitize
    const check = sanitizeThemeCSS(rawCss, manifest.id);
    if (!check.valid) {
      throw new Error(`Theme failed security validation:\n${check.errors.join('\n')}`);
    }

    // 4. Register in in-memory plugin loader
    const pluginData = {
      ...manifest,
      path: './plugins/' + manifest.id,
      status: 'ready',
      sanitizedCss: check.sanitizedCss,
      importedZip: true
    };

    curioPluginLoader.plugins.set(manifest.id, pluginData);

    // Save imported theme in localStorage for persistence across reloads
    try {
      const stored = JSON.parse(localStorage.getItem('curio_imported_themes') || '{}');
      stored[manifest.id] = pluginData;
      localStorage.setItem('curio_imported_themes', JSON.stringify(stored));
    } catch (e) {
      console.warn('Could not persist imported theme to localStorage:', e);
    }

    return pluginData;
  } catch (err) {
    console.error('[PluginImporter] Import failed:', err);
    throw err;
  }
}

/**
 * Restores user-imported ZIP themes from localStorage.
 */
export function restoreImportedThemes(curioPluginLoader) {
  try {
    const stored = JSON.parse(localStorage.getItem('curio_imported_themes') || '{}');
    for (const [id, pluginData] of Object.entries(stored)) {
      if (!curioPluginLoader.plugins.has(id)) {
        curioPluginLoader.plugins.set(id, pluginData);
      }
    }
  } catch (e) {
    console.warn('[PluginImporter] Error restoring imported themes:', e);
  }
}
