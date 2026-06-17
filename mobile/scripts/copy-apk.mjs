import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const mobileDir = resolve(scriptDir, '..');
const rootDir = resolve(mobileDir, '..');
const sourceApk = resolve(mobileDir, 'android', 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk');
const outDir = resolve(rootDir, 'dist', 'android');
const outApk = resolve(outDir, 'visionbook.apk');

mkdirSync(outDir, { recursive: true });
copyFileSync(sourceApk, outApk);
console.log(`Copied ${outApk}`);
