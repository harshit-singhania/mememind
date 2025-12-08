import { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator, TouchableOpacity, Share } from 'react-native';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';
import { Video, ResizeMode } from 'expo-av';
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
    }
  };

  const handleShare = async () => {
    if (memeUrl) {
      try {
        const isVideo = memeUrl.endsWith('.mp4');
        const fileExt = isVideo ? '.mp4' : '.png';
        const mimeType = isVideo ? 'video/mp4' : 'image/png';
        const fileUri = FileSystem.cacheDirectory + 'meme_share' + fileExt;
        
        const { uri } = await FileSystem.downloadAsync(
          memeUrl,
          fileUri
        );
        
        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(uri, {
             mimeType: mimeType,
             dialogTitle: 'Share your meme'
          });
        } else {
            await Share.share({
              message: 'Check out my meme!',
              url: memeUrl, 
            });
        }
      } catch (error) {
        console.error("Share failed:", error.message);
        alert("Could not share: " + error.message);
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
      const isVideo = memeUrl.endsWith('.mp4');
      return (
        <View style={styles.resultContainer}>
          {isVideo ? (
            <Video
              style={styles.memeImage}
              source={{ uri: memeUrl }}
              useNativeControls
              resizeMode={ResizeMode.CONTAIN}
              isLooping
              shouldPlay
            />
          ) : (
            <Image source={{ uri: memeUrl }} style={styles.memeImage} />
          )}
          
          <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
            <Text style={styles.buttonText}>Share {isVideo ? 'Reel' : 'Meme'} 📤</Text>
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
