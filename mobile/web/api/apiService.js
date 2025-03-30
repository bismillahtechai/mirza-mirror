import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchThoughts = async () => {
  try {
    const response = await api.get('/thoughts');
    return response.data;
  } catch (error) {
    console.error('Error fetching thoughts:', error);
    throw error;
  }
};

export const fetchThought = async (id) => {
  try {
    const response = await api.get(`/thoughts/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching thought ${id}:`, error);
    throw error;
  }
};

export const createThought = async (content, source = 'web_app') => {
  try {
    const response = await api.post('/thoughts', { content, source });
    return response.data;
  } catch (error) {
    console.error('Error creating thought:', error);
    throw error;
  }
};

export const searchThoughts = async (query) => {
  try {
    const response = await api.get('/thoughts/search', { params: { query } });
    return response.data;
  } catch (error) {
    console.error('Error searching thoughts:', error);
    throw error;
  }
};

export const uploadVoiceRecording = async (audioBlob) => {
  try {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    
    const response = await api.post('/thoughts/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Error uploading voice recording:', error);
    throw error;
  }
};

export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('document', file);
    
    const response = await api.post('/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Error uploading document:', error);
    throw error;
  }
};

export const importConversation = async (file, source) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source', source);
    
    const response = await api.post('/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Error importing conversation:', error);
    throw error;
  }
};

export default api;
