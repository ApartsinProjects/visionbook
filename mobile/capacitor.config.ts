import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.apartsinprojects.visionbook',
  appName: 'VisionBook',
  webDir: 'www',
  bundledWebRuntime: false,
  android: {
    allowMixedContent: false,
    captureInput: true
  },
  server: {
    androidScheme: 'https'
  }
};

export default config;
