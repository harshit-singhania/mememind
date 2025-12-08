import { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Image, TouchableOpacity, ActivityIndicator, Alert, ScrollView } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { useMemeStore } from '../store/memeStore';
import { apiClient, uploadImage } from '../api/client';

export default function UploadScreen({ navigation }) {
  const [mood, setMood] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const setJob = useMemeStore((state) => state.setJob);

  const pickImage = async () => {
    try {
      console.log('Requesting permissions...');
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      console.log('Permission status:', status);
      
      if (status !== 'granted') {
        Alert.alert('Permission Denied', 'Sorry, we need camera roll permissions to make this work!');
        return;
      }

      console.log('Launching image library...');
      let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 1,
      });
      console.log('Image Picker Result:', JSON.stringify(result));

      if (!result.canceled) {
        setImage(result.assets[0].uri);
      } else {
        console.log('User cancelled image picker');
      }
    } catch (error) {
      console.error('Pick Image Error:', error);
      Alert.alert('Error', 'Failed to pick image: ' + error.message);
    }
  };

  const generateMeme = async () => {
    if (!image) {
      Alert.alert('Missing Image', 'Please select an image first.');
      return;
    }

    setLoading(true);
    try {
      console.log('Uploading image...');
      const uploadedUrl = await uploadImage(image);
      console.log('Image uploaded:', uploadedUrl);

      const payload = {
        user_id: "mobile-user-" + Math.floor(Math.random() * 1000),
        mood_hint: mood,
        media_url: uploadedUrl
      };

      const response = await apiClient.post('/generate-meme', payload);
      
      if (response.data && response.data.job_id) {
        setJob(response.data.job_id, response.data.status);
        navigation.navigate('Result');
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error(error);
      Alert.alert('Error', 'Failed to generate meme. Check your connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>1. Pick an Image</Text>
      <TouchableOpacity style={styles.imageContainer} onPress={pickImage}>
        {image ? (
          <Image source={{ uri: image }} style={styles.preview} />
        ) : (
          <View style={styles.placeholder}>
            <Text style={styles.placeholderText}>Tap to Select Photo 📸</Text>
          </View>
        )}
      </TouchableOpacity>

      <Text style={styles.label}>2. Describe the Mood (Optional)</Text>
      <TextInput
        style={styles.input}
        placeholder="e.g. Sarcastic, Happy, Dank..."
        value={mood}
        onChangeText={setMood}
      />

      <TouchableOpacity 
        style={[styles.button, (!image || loading) && styles.disabled]} 
        onPress={generateMeme}
        disabled={!image || loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Generate Meme 🚀</Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  label: {
    fontSize: 18,
    fontWeight: '600',
    marginTop: 20,
    marginBottom: 10,
    alignSelf: 'flex-start',
    width: '100%',
  },
  imageContainer: {
    width: '100%',
    height: 300,
    borderRadius: 15,
    overflow: 'hidden',
    backgroundColor: '#f0f0f0',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  preview: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  placeholder: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholderText: {
    color: '#888',
    fontSize: 16,
  },
  input: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    paddingHorizontal: 15,
    fontSize: 16,
    marginBottom: 30,
  },
  button: {
    backgroundColor: '#007AFF',
    width: '100%',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  disabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
