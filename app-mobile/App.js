import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';
import { checkHealth } from './src/api/client';
import { CONFIG } from './src/core/config';

export default function App() {
  const [status, setStatus] = useState('Checking...');
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    setStatus('Connecting to MemeMind API...');
    const isHealthy = await checkHealth();
    if (isHealthy) {
      setStatus('Connected 🟢');
      setConnected(true);
    } else {
      setStatus('Connection Failed 🔴');
      setConnected(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>MemeMind</Text>
      <Text style={styles.subtitle}>Mobile App</Text>
      
      <View style={styles.card}>
        <Text style={styles.label}>Backend Status:</Text>
        <Text style={[styles.status, connected ? styles.success : styles.error]}>
          {status}
        </Text>
        <Text style={styles.url}>{CONFIG.API_BASE_URL}</Text>
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    marginBottom: 40,
  },
  card: {
    padding: 20,
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    alignItems: 'center',
    width: '80%',
  },
  label: {
    fontSize: 14,
    color: '#888',
    marginBottom: 5,
  },
  status: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 10,
  },
  success: {
    color: 'green',
  },
  error: {
    color: 'red',
  },
  url: {
    fontSize: 12,
    color: '#aaa',
  },
});
