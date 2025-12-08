import { NativeModules } from 'react-native';

const scriptURL = NativeModules.SourceCode.scriptURL;
let hostname = '192.168.29.65'; // Fallback to last known IP

if (scriptURL) {
  try {
    const address = scriptURL.split('://')[1].split('/')[0];
    hostname = address.split(':')[0];
  } catch (e) {
    console.log('Failed to parse scriptURL:', e);
  }
}

export const CONFIG = {
  API_BASE_URL: process.env.EXPO_PUBLIC_API_URL || `http://${hostname}:8080`,
};
