import { Platform } from 'react-native';

// Default to 10.0.2.2 for Android Emulator, localhost for iOS/Web
const DEFAULT_HOST = Platform.OS === 'android' ? '10.0.2.2' : 'localhost';

export const CONFIG = {
  API_BASE_URL: process.env.EXPO_PUBLIC_API_URL || `http://${DEFAULT_HOST}:8080`,
};
