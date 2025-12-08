import { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator, TouchableOpacity, Share } from 'react-native';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';
import { useMemeStore } from '../store/memeStore';
import { apiClient } from '../api/client';
import { CONFIG } from '../core/config';

export default function ResultScreen({ navigation }) {
  const { currentJobId, jobStatus, updateStatus, memeUrl, error, setError, reset } = useMemeStore();
  const [polling, setPolling] = useState(true);
  const pollInterval = useRef(null);

  useEffect(() => {
    if (currentJobId) {
      startPolling();
    }
    return () => stopPolling();
  }, [currentJobId]);

  const startPolling = () => {
    setPolling(true);
    pollInterval.current = setInterval(checkStatus, 3000); // Check every 3 seconds
  };

  const stopPolling = () => {
    if (pollInterval.current) {
      clearInterval(pollInterval.current);
      pollInterval.current = null;
    }
    setPolling(false);
  };

  const checkStatus = async () => {
    try {
      const response = await apiClient.get(`/jobs/${currentJobId}`);
      const { status, result_url } = response.data;
      
      let finalUrl = result_url;
      if (finalUrl && finalUrl.includes('localhost')) {
        finalUrl = finalUrl.replace('http://localhost:8080', CONFIG.API_BASE_URL);
      }
      
      updateStatus(status, finalUrl);

      if (status === 'completed' || status === 'failed') {
        stopPolling();
      }
    } catch (err) {
      console.error(err);
      // Don't stop polling immediately on network error, retry a few times?
      // For now, let it keep trying or show error if consistent.
      // setError('Failed to fetch status');
    }
  };

  const handleShare = async () => {
    if (memeUrl) {
      try {
        // Android often fails to share remote URLs directly to apps like WhatsApp
        // We need to download it locally first
        const fileUri = FileSystem.cacheDirectory + 'meme_share.png';
        
        const { uri } = await FileSystem.downloadAsync(
          memeUrl,
          fileUri
        );
        
        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(uri, {
             mimeType: 'image/png',
             dialogTitle: 'Share your meme'
          });
        } else {
           // Fallback
            await Share.share({
              message: 'Check out my meme!',
              url: memeUrl, // iOS might handle this better
            });
        }
      } catch (error) {
        console.error("Share failed:", error.message);
        alert("Could not share image: " + error.message);
      }
    }
  };

  const handleHome = () => {
    reset();
    navigation.navigate('Home');
  };

  const renderContent = () => {
    if (jobStatus === 'failed') {
      return (
        <View style={styles.center}>
          <Text style={styles.errorText}>Generation Failed 😢</Text>
          <Text style={styles.subText}>Please try again.</Text>
        </View>
      );
    }

    if (jobStatus === 'completed' && memeUrl) {
      return (
        <View style={styles.resultContainer}>
          <Image source={{ uri: memeUrl }} style={styles.memeImage} />
          <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
            <Text style={styles.buttonText}>Share Meme 📤</Text>
          </TouchableOpacity>
        </View>
      );
    }

    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.statusText}>
          {jobStatus === 'queued' ? 'In Queue...' : 'Processing...'}
        </Text>
        <Text style={styles.subText}>Working our AI magic ✨</Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {renderContent()}
      
      {(jobStatus === 'completed' || jobStatus === 'failed') && (
        <TouchableOpacity style={styles.homeButton} onPress={handleHome}>
          <Text style={styles.homeButtonText}>Create New Meme</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  center: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  resultContainer: {
    width: '100%',
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
  },
  memeImage: {
    width: '100%',
    height: 400,
    resizeMode: 'contain',
    borderRadius: 10,
    marginBottom: 20,
    backgroundColor: '#f0f0f0',
  },
  statusText: {
    fontSize: 22,
    fontWeight: 'bold',
    marginTop: 20,
    color: '#333',
  },
  subText: {
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
  errorText: {
    fontSize: 22,
    fontWeight: 'bold',
    color: 'red',
  },
  shareButton: {
    backgroundColor: '#34C759',
    paddingHorizontal: 30,
    paddingVertical: 12,
    borderRadius: 25,
    marginTop: 10,
    width: '80%',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  homeButton: {
    marginTop: 20,
    padding: 15,
  },
  homeButtonText: {
    color: '#007AFF',
    fontSize: 16,
    fontWeight: '500',
  },
});
