import { sanitizeThemeCSS, sanitizeSVG } from './sanitizer.js';
import fs from 'fs';

console.log('--- Testing Sanitizer ---');
// 1. Valid CSS
const res1 = sanitizeThemeCSS('.btn { color: red; }', 'curio-theme-test');
console.log('Normal CSS valid:', res1.valid, '| Auto-scoped:', res1.warnings.length > 0);

// 2. Forbidden @import
const res2 = sanitizeThemeCSS('@import url("evil.css");', 'curio-theme-test');
console.log('Blocked @import:', !res2.valid, '| Error:', res2.errors[0]);

// 3. Forbidden external url
const res3 = sanitizeThemeCSS('.bg { background: url("https://evil.com/bg.png"); }', 'curio-theme-test');
console.log('Blocked external URL:', !res3.valid, '| Error:', res3.errors[0]);

// 4. Allowed data: URI
const res4 = sanitizeThemeCSS('.bg { background: url("data:image/png;base64,iVBORw0KGgo"); }', 'curio-theme-test');
console.log('Allowed data: URI:', res4.valid);

// 5. SVG security check
const svgCheck = sanitizeSVG('<svg><script>alert(1)</script><circle r="5"/></svg>');
console.log('Blocked script in SVG:', !svgCheck.valid, '| Error:', svgCheck.errors[0]);

console.log('--- Checking Token Bridge & Contract ---');
const bridgeCss = fs.readFileSync('src/styles/token-bridge.css', 'utf8');
console.log('Token bridge size:', bridgeCss.length, 'bytes');

const contract = JSON.parse(fs.readFileSync('src/plugins/contract.json', 'utf8'));
console.log('Contract loaded:', contract.contractVersion, '| Required parts:', contract.parts.length);
