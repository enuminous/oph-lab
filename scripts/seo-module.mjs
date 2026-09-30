import { readFile } from 'node:fs/promises';
import ts from 'typescript';

// Execute the browser's pure metadata functions during builds, using the
// project's TypeScript dependency rather than maintaining another route table.
export async function loadSeo() {
  const data = JSON.parse(await readFile(new URL('../src/seo-data.json', import.meta.url), 'utf8'));
  const source = await readFile(new URL('../src/seo.ts', import.meta.url), 'utf8');
  const inlined = source.replace("import seoData from './seo-data.json';", `const seoData = ${JSON.stringify(data)};`);
  const { outputText } = ts.transpileModule(inlined, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext },
  });
  return import(`data:text/javascript,${encodeURIComponent(outputText)}`);
}
