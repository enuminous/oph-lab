import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadSeo } from './seo-module.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const seo = await loadSeo();
const template = await readFile(path.join(dist, 'index.html'), 'utf8');

function escapeHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function pageHtml(pathname) {
  const meta = seo.getSeoMeta(pathname);
  const canonical = seo.getCanonicalUrl(pathname);
  let html = template.replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(meta.title)}</title>`);
  const values = {
    title: meta.title,
    description: meta.description,
    'og:title': meta.title,
    'og:description': meta.description,
    'og:url': canonical,
    'og:site_name': seo.SEO_SITE.name,
    'twitter:title': meta.title,
    'twitter:description': meta.description,
    'twitter:url': canonical,
  };
  for (const [key, value] of Object.entries(values)) {
    const pattern = new RegExp(`(<meta (?:name|property)="${key}" content=")[^"]*("\\s*/?>)`);
    if (!pattern.test(html)) throw new Error(`Missing metadata placeholder: ${key}`);
    html = html.replace(pattern, (_, before, after) => `${before}${escapeHtml(value)}${after}`);
  }
  html = html.replace(/(<link rel="canonical" href=")[^"]*("\s*\/?>)/, `$1${canonical}$2`);
  const schema = JSON.stringify(seo.getStructuredData(pathname)).replaceAll('<', '\\u003c');
  return html.replace(/(<script type="application\/ld\+json" id="page-schema">)[\s\S]*?(<\/script>)/, (_, before, after) => `${before}${schema}${after}`);
}

for (const pathname of Object.keys(seo.SEO_ROUTES)) {
  const directory = path.join(dist, pathname === '/' ? '' : pathname.slice(1));
  await mkdir(directory, { recursive: true });
  await writeFile(path.join(directory, 'index.html'), pageHtml(pathname));
}

// No verified per-page publication dates are maintained. Omit optional lastmod
// instead of claiming that an unchanged page was updated on each build.
const sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  Object.keys(seo.SEO_ROUTES).map(route => `  <url><loc>${seo.getCanonicalUrl(route)}</loc></url>`).join('\n') +
  '\n</urlset>\n';
await writeFile(path.join(dist, 'sitemap.xml'), sitemap);
console.log(`Static metadata and sitemap generated for ${Object.keys(seo.SEO_ROUTES).length} OPH Lab routes.`);
