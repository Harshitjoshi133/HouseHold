// services/auth.js
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

class AuthService {
  login(credentials) {
    return axios
      .post(`${API_URL}/auth/login`, credentials)
      .then(response => {
        if (response.data.token) {
          localStorage.setItem('user', JSON.stringify(response.data));
          this.setAuthHeader(response.data.token);
        }
        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
    this.removeAuthHeader();
  }

  register(user) {
    return axios.post(`${API_URL}/auth/register`, user);
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  isAuthenticated() {
    const user = this.getCurrentUser();
    return !!user && !!user.token;
  }

  getToken() {
    const user = this.getCurrentUser();
    return user ? user.token : null;
  }

  setAuthHeader(token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  removeAuthHeader() {
    delete axios.defaults.headers.common['Authorization'];
  }

  setupInterceptors() {
    // Request interceptor
    axios.interceptors.request.use(
      config => {
        const token = this.getToken();
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    axios.interceptors.response.use(
      response => response,
      error => {
        // Handle 401 Unauthorized
        if (error.response && error.response.status === 401) {
          this.logout();
          router.push('/login');
        }
        return Promise.reject(error);
      }
    );
  }

  forgotPassword(email) {
    return axios.post(`${API_URL}/auth/forgot-password`, { email });
  }

  resetPassword(token, password) {
    return axios.post(`${API_URL}/auth/reset-password`, {
      token,
      password
    });
  }
}

export default new AuthService();