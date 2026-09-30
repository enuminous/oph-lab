import seoData from './seo-data.json';

export type SeoMeta = {
  title: string;
  description: string;
};

export const SEO_ROUTES: Record<string, SeoMeta> = seoData.routes;
export const SEO_SITE = {
  origin: seoData.origin,
  name: seoData.siteName,
  image: seoData.image,
  imageAlt: seoData.imageAlt,
};

function normalizePathname(pathname: string): string {
  return pathname.split(/[?#]/, 1)[0].replace(/\/+$/, '') || '/';
}

export function hasSeoRoute(pathname: string): boolean {
  return Object.hasOwn(SEO_ROUTES, normalizePathname(pathname));
}

export function getSeoMeta(pathname: string): SeoMeta {
  return SEO_ROUTES[normalizePathname(pathname)] ?? {
    title: 'Page not found | OPH Lab',
    description: 'The requested OPH Lab page was not found. Return to the research overview or choose a lesson.',
  };
}

export function getCanonicalUrl(pathname: string): string | null {
  if (!hasSeoRoute(pathname)) return null;
  const normalized = normalizePathname(pathname);
  return `${SEO_SITE.origin}${normalized === '/' ? '/' : `${normalized}/`}`;
}

export function getStructuredData(pathname: string) {
  if (!hasSeoRoute(pathname)) return null;
  const meta = getSeoMeta(pathname);
  const canonical = getCanonicalUrl(pathname);
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    '@id': `${canonical}#webpage`,
    url: canonical,
    name: meta.title,
    description: meta.description,
    inLanguage: 'en',
    image: SEO_SITE.image,
    isPartOf: {
      '@type': 'WebSite',
      '@id': `${SEO_SITE.origin}/#website`,
      name: 'OPH Lab',
      url: `${SEO_SITE.origin}/`,
      publisher: {
        '@type': 'Organization',
        name: SEO_SITE.name,
        url: 'https://floatingpragma.io/',
      },
    },
    about: {
      '@type': 'Thing',
      name: 'Observer Patch Holography',
      url: 'https://floatingpragma.io/physics/',
    },
    citation: {
      '@type': 'ScholarlyArticle',
      name: 'Finite Observer Consensus as a Reconstruction Principle: Normal Forms, the Standard Model Lie Type, and a Route to the Einstein Field Equation',
      author: { '@type': 'Person', name: 'Bernhard Mueller' },
      url: 'https://philpapers.org/rec/MUEFOC',
    },
  };
}
