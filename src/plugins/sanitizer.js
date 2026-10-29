/**
 * Curio Plugin Security Sanitizer
 * Enforces contract security constraints on third-party and AI-generated plugins.
 */

// Forbidden CSS patterns that could cause remote code execution or data leakage
const FORBIDDEN_CSS_PATTERNS = [
  { pattern: /@import\b/i, reason: "External CSS imports (@import) are prohibited." },
  { pattern: /url\s*\(\s*(?!['"]?data:)[^)]+\)/i, reason: "External network URLs in url() are prohibited (only data: URIs allowed)." },
  { pattern: /expression\s*\(/i, reason: "CSS expressions are prohibited." },
  { pattern: /behavior\s*:/i, reason: "CSS behaviors are prohibited." },
  { pattern: /-moz-binding\s*:/i, reason: "XBL bindings are prohibited." },
  { pattern: /javascript\s*:/i, reason: "javascript: pseudo-protocols are prohibited." }
];

/**
 * Sanitizes and validates plugin CSS against security rules and scoping.
 * @param {string} cssContent - Raw CSS text
 * @param {string} themeId - The unique theme identifier (e.g. 'curio-theme-win95')
 * @returns {{ valid: boolean, sanitizedCss: string, errors: string[], warnings: string[] }}
 */
export function sanitizeThemeCSS(cssContent, themeId) {
  const errors = [];
  const warnings = [];

  if (typeof cssContent !== 'string') {
    return { valid: false, sanitizedCss: '', errors: ['Invalid CSS content provided.'], warnings: [] };
  }

  // 1. Check for malicious or remote-loading patterns
  for (const rule of FORBIDDEN_CSS_PATTERNS) {
    if (rule.pattern.test(cssContent)) {
      errors.push(`Security Violation: ${rule.reason}`);
    }
  }

  if (errors.length > 0) {
    return { valid: false, sanitizedCss: '', errors, warnings };
  }

  // 2. Ensure CSS is scoped to the theme ID
  // If selectors don't start with [data-theme="..."], wrap or warn
  const scopePrefix = `[data-theme="${themeId}"]`;
  let processedCss = cssContent;

  // Check if root styles or unscoped selectors exist
  if (!cssContent.includes(scopePrefix) && !cssContent.includes(`data-theme="${themeId}"`)) {
    warnings.push(`CSS does not contain explicit scope ${scopePrefix}. Auto-scoping will be applied.`);
    // Basic auto-scoping for simple CSS blocks
    processedCss = `${scopePrefix} {\n${cssContent}\n}`;
  }

  return {
    valid: true,
    sanitizedCss: processedCss,
    errors: [],
    warnings
  };
}

/**
 * Sanitizes SVG icons or ornament markup.
 * Strips script tags, event handlers, and foreign objects.
 * @param {string} svgContent - Raw SVG string
 * @returns {{ valid: boolean, sanitizedSvg: string, errors: string[] }}
 */
export function sanitizeSVG(svgContent) {
  if (typeof svgContent !== 'string' || !svgContent.trim()) {
    return { valid: true, sanitizedSvg: '', errors: [] };
  }

  const errors = [];

  // Prohibit script tags and foreignObject outright
  if (/<script\b/i.test(svgContent)) {
    errors.push("SVG contains forbidden <script> element.");
  }
  if (/<foreignObject\b/i.test(svgContent)) {
    errors.push("SVG contains forbidden <foreignObject> element.");
  }
  if (/\bon[a-z]+\s*=/i.test(svgContent)) {
    errors.push("SVG contains forbidden inline event handlers (e.g. onclick, onload).");
  }

  if (errors.length > 0) {
    return { valid: false, sanitizedSvg: '', errors };
  }

  // Basic cleanup of external links
  const sanitized = svgContent
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/\s+on[a-z]+\s*=\s*(['"]).*?\1/gi, '')
    .replace(/\s+href\s*=\s*(['"])(?!data:|#).*?\1/gi, ' href="#"');

  return { valid: true, sanitizedSvg: sanitized, errors: [] };
}
