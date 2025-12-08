import { create } from 'zustand';

export const useMemeStore = create((set) => ({
  currentJobId: null,
  jobStatus: null,
  memeUrl: null,
  error: null,
  
  setJob: (jobId, status) => set({ 
    currentJobId: jobId, 
    jobStatus: status, 
    error: null 
  }),
  
  updateStatus: (status, url = null) => set({ 
    jobStatus: status, 
    memeUrl: url 
  }),
  
  setError: (error) => set({ error }),
  
  reset: () => set({ 
    currentJobId: null, 
    jobStatus: null, 
    memeUrl: null, 
    error: null 
  }),
}));
