import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const mobileDir = resolve(scriptDir, '..');
const rootDir = resolve(mobileDir, '..');
const outDir = resolve(mobileDir, 'www');

const entries = [
  'index.html',
  'toc.html',
  'robots.txt',
  'sitemap.xml',
  'appendices',
  'capstone',
  'front-matter',
  'images',
  'pagefind',
  'part-1-image-processing',
  'part-2-classical-computer-vision',
  'part-3-deep-learning-for-vision',
  'part-4-generative-vision-models',
  'scripts',
  'styles',
  'vendor'
];

rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

for (const entry of entries) {
  const source = resolve(rootDir, entry);
  if (!existsSync(source)) {
    continue;
  }
  cpSync(source, resolve(outDir, entry), {
    recursive: true,
    force: true,
    filter: (sourcePath) => !sourcePath.includes(`${resolve(rootDir, 'KDP')}`)
  });
}

console.log(`Prepared bundled web assets in ${outDir}`);
