import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { loadSeo } from './seo-module.mjs';

const seo = await loadSeo();
const routes = Object.keys(seo.SEO_ROUTES);
const read = relative => readFile(new URL(`../${relative}`, import.meta.url), 'utf8');
const decode = text => text.replaceAll('&quot;', '"').replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');
const meta = (html, key) => decode(html.match(new RegExp(`<meta (?:name|property)="${key}" content="([^"]*)"`))?.[1] ?? '');

// Compare the build inventory with actual router and navigation declarations.
const app = await read('src/App.tsx');
const appRoutes = [...app.matchAll(/<Route path="([^"]+)"/g)].filter(match => match[1] !== '*').map(match => match[1] === '/' ? '/' : `/${match[1]}`);
assert.deepEqual([...appRoutes].sort(), [...routes].sort());
const walk = await read('src/routes/walkthrough.ts');
const walkRoutes = [...walk.matchAll(/to: '([^']+)'/g)].map(match => match[1].replace(/\/$/, '') || '/');
assert.deepEqual([...walkRoutes].sort(), [...routes].sort());

for (const route of routes) {
  const html = await read(`dist/${route === '/' ? '' : `${route.slice(1)}/`}index.html`);
  const expected = seo.getSeoMeta(route);
  const canonical = `https://oph-lab.floatingpragma.io${route === '/' ? '/' : `${route}/`}`;
  assert.equal(seo.getCanonicalUrl(`${route}/?ignored=true#fragment`), canonical);
  assert.equal(decode(html.match(/<title>([^<]*)<\/title>/)?.[1] ?? ''), expected.title);
  for (const key of ['title', 'og:title', 'twitter:title']) assert.equal(meta(html, key), expected.title, `${route} ${key}`);
  for (const key of ['description', 'og:description', 'twitter:description']) assert.equal(meta(html, key), expected.description, `${route} ${key}`);
  assert.equal((html.match(/rel="canonical"/g) ?? []).length, 1, route);
  assert.equal(html.match(/rel="canonical" href="([^"]+)"/)?.[1], canonical);
  for (const key of ['og:url', 'twitter:url']) assert.equal(meta(html, key), canonical);
  assert.equal(meta(html, 'og:site_name'), 'Pragma Research');
  assert.equal(meta(html, 'og:image'), seo.SEO_SITE.image);
  assert.equal(meta(html, 'twitter:image'), seo.SEO_SITE.image);
  assert.equal(meta(html, 'og:image:alt'), seo.SEO_SITE.imageAlt);
  assert.ok(meta(html, 'robots').includes('max-image-preview:large'));
  const schema = JSON.parse(html.match(/<script type="application\/ld\+json" id="page-schema">([\s\S]*?)<\/script>/)?.[1] ?? '{}');
  assert.equal(schema['@type'], 'WebPage');
  assert.equal(schema.url, canonical);
  assert.equal(schema.name, expected.title);
  assert.equal(schema.description, expected.description);
  assert.equal(schema.isPartOf.publisher.name, 'Pragma Research');
  assert.equal(schema.citation.url, 'https://philpapers.org/rec/MUEFOC');
  assert.deepEqual(schema, seo.getStructuredData(route));
  assert.ok(!html.includes('/oph/papers/') && !html.includes('correct theory of everything'), route);
}

// Root source is meaningful before the app runs, as well as after postbuild.
const source = await read('index.html');
assert.equal(meta(source, 'description'), seo.getSeoMeta('/').description);
assert.equal(source.match(/<title>([^<]*)<\/title>/)?.[1], seo.getSeoMeta('/').title);
assert.equal(meta(source, 'og:site_name'), 'Pragma Research');
assert.deepEqual(JSON.parse(source.match(/<script type="application\/ld\+json" id="page-schema">([\s\S]*?)<\/script>/)[1]), seo.getStructuredData('/'));
assert.equal((seo.getSeoMeta('/').title.match(/OPH Lab/g) ?? []).length, 1);
assert.ok(app.includes('<Route path="*"'), 'Unknown routes need a visible fallback');
for (const unknown of ['/missing-lesson/', '/gravity/extra/', '/unknown/?query=1']) {
  assert.equal(seo.hasSeoRoute(unknown), false);
  assert.equal(seo.getSeoMeta(unknown).title, 'Page not found | OPH Lab');
  assert.equal(seo.getCanonicalUrl(unknown), null);
  assert.equal(seo.getStructuredData(unknown), null);
}

const sitemap = await read('dist/sitemap.xml');
assert.deepEqual([...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(match => match[1]).sort(), routes.map(seo.getCanonicalUrl).sort());
assert.ok(!sitemap.includes('<lastmod>'), 'Do not invent modification dates without verified content history');
assert.ok((await read('dist/robots.txt')).includes('Sitemap: https://oph-lab.floatingpragma.io/sitemap.xml'));
assert.ok((await read('dist/404.html')).includes('noindex'));
assert.equal((await read('dist/CNAME')).trim(), 'oph-lab.floatingpragma.io');
const png = await readFile(new URL(`../dist${new URL(seo.SEO_SITE.image).pathname}`, import.meta.url));
assert.equal(png.subarray(1, 4).toString(), 'PNG');
assert.equal(png.readUInt32BE(16), 1200);
assert.equal(png.readUInt32BE(20), 630);
console.log(`SEO checks passed: ${routes.length} routes, static/runtime metadata, schema, canonical URLs, sitemap and 1200×630 preview.`);
