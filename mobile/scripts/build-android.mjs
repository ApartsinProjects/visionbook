import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';

const androidDir = resolve('android');
const command = process.platform === 'win32' ? 'gradlew.bat' : './gradlew';
const result = spawnSync(command, ['assembleDebug'], {
  cwd: androidDir,
  stdio: 'inherit',
  shell: process.platform === 'win32'
});

process.exit(result.status ?? 1);
