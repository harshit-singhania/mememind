import axios from 'axios';
import { CONFIG } from '../core/config';

export const apiClient = axios.create({
  baseURL: CONFIG.API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Health check function
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.status === 200;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

export const uploadImage = async (uri) => {
  const formData = new FormData();
  formData.append('file', {
    uri: uri,
    type: 'image/jpeg',
    name: 'upload.jpg',
  });

  try {
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      transformRequest: (data, headers) => {
        return formData; // useful for React Native to prevent some data transformation issues
      },
    });
    return response.data.url;
  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
};
