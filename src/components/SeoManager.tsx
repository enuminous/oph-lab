import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { getCanonicalUrl, getSeoMeta, getStructuredData, hasSeoRoute, SEO_SITE } from '../seo';

function setMetaContent(key: string, content: string | null) {
  const attribute = key.startsWith('og:') ? 'property' : 'name';
  let node = document.querySelector<HTMLMetaElement>(`meta[${attribute}="${key}"]`);
  if (content === null) {
    node?.remove();
    return;
  }
  if (!node) {
    node = document.createElement('meta');
    node.setAttribute(attribute, key);
    document.head.appendChild(node);
  }
  node.content = content;
}

function setCanonicalHref(href: string | null) {
  let node = document.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (href === null) {
    node?.remove();
    return;
  }
  if (!node) {
    node = document.createElement('link');
    node.rel = 'canonical';
    document.head.appendChild(node);
  }
  node.href = href;
}

export function SeoManager() {
  const location = useLocation();

  useEffect(() => {
    const seo = getSeoMeta(location.pathname);
    const canonical = getCanonicalUrl(location.pathname);
    const robots = hasSeoRoute(location.pathname)
      ? 'index, follow, max-image-preview:large'
      : 'noindex, follow';

    document.title = seo.title;
    setMetaContent('title', seo.title);
    setMetaContent('description', seo.description);
    setMetaContent('robots', robots);
    setMetaContent('googlebot', robots);
    setMetaContent('og:title', seo.title);
    setMetaContent('og:description', seo.description);
    setMetaContent('og:url', canonical);
    setMetaContent('og:site_name', SEO_SITE.name);
    setMetaContent('twitter:title', seo.title);
    setMetaContent('twitter:description', seo.description);
    setMetaContent('twitter:url', canonical);
    setCanonicalHref(canonical);

    const structuredData = getStructuredData(location.pathname);
    let schema = document.querySelector<HTMLScriptElement>('#page-schema');
    if (structuredData === null) {
      schema?.remove();
    } else {
      if (!schema) {
        schema = document.createElement('script');
        schema.type = 'application/ld+json';
        schema.id = 'page-schema';
        document.head.appendChild(schema);
      }
      schema.textContent = JSON.stringify(structuredData);
    }
  }, [location.pathname]);

  return null;
}
