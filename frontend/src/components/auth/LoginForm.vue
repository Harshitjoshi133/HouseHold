<template>
  <div class="card shadow">
    <div class="card-body">
      <h3 class="card-title text-center mb-4">Login</h3>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" id="email" class="form-control" v-model="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" id="password" class="form-control" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Login
        </button>
      </form>
      <div class="mt-3 text-center">
        <p>Don't have an account? <router-link to="/register">Register</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "LoginForm",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: null
    };
  },
  methods: {
    validateForm() {
      if (!this.email || !this.isValidEmail(this.email)) {
        this.error = 'Please enter a valid email address';
        return false;
      }
      
      if (!this.password || this.password.length < 1) {
        this.error = 'Please enter your password';
        return false;
      }
      
      return true;
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    
    async handleLogin() {
      if (this.loading) return;
      
      this.error = null;
      
      // Validate form
      if (!this.validateForm()) {
        return;
      }
      
      console.log("Logging in with:", this.email);

      this.loading = true;

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
          email: this.email,
          password: this.password
        });

        console.log("Login successful:", response.data);

        const { access_token } = response.data;
        const role = response.data.user.role;
        const user_id = response.data.user.id;
        
        // Store token & user info
        localStorage.setItem('token', access_token);
        localStorage.setItem('role', role);
        localStorage.setItem('user_id', user_id);
        
        // Redirect based on role
        this.$router.push(`/${role}/dashboard`);
        
        console.log('Redirecting to dashboard');
        
      } catch (err) {
        console.error("Login failed:", err);
        
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else if (err.response && err.response.status === 401) {
          this.error = 'Invalid email or password';
        } else if (err.response && err.response.status === 404) {
          this.error = 'User not found';
        } else {
          this.error = 'Login failed. Please try again.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
