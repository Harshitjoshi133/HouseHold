import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // ✅ Flask backend URL
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
