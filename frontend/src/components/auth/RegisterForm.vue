<template>
  <div class="card shadow">
    <div class="card-body">
      <h3 class="card-title text-center mb-4">Register</h3>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <form @submit.prevent="handleSubmit">
        <!-- Common fields for all users -->
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" v-model="formData.username" required />
        </div>
        <div class="mb-3">
          <label for="full_name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="full_name" v-model="formData.full_name" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" v-model="formData.email" required />
        </div>
        <div class="mb-3">
          <label for="phone_number" class="form-label">Phone Number</label>
          <input type="tel" class="form-control" id="phone_number" v-model="formData.phone_number" required />
        </div>
        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <input type="text" class="form-control" id="address" v-model="formData.address" required />
        </div>
        <div class="mb-3">
          <label for="pin_code" class="form-label">PIN Code</label>
          <input type="text" class="form-control" id="pin_code" v-model="formData.pin_code" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="formData.password" required />
        </div>
        <div class="mb-3">
          <label for="role" class="form-label">Register as</label>
          <select class="form-select" id="role" v-model="formData.role" required>
            <option value="customer">Customer</option>
            <option value="professional">Service Professional</option>
          </select>
        </div>

        <!-- Professional specific fields -->
        <div v-if="formData.role === 'professional'">
          <div class="mb-3">
            <label for="service_type" class="form-label">Service Type</label>
            <select class="form-select" id="service_type" v-model="formData.service" required>
              <option value="">Select a service</option>
              <option v-for="service in services" :key="service.id" :value="service.name">
                {{ service.name }}
              </option>
            </select>
          </div>
          <div class="mb-3">
            <label for="experience" class="form-label">Years of Experience</label>
            <input type="number" class="form-control" id="experience" v-model="formData.experience" min="0" required />
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea class="form-control" id="description" v-model="formData.description" rows="3" required></textarea>
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Register
        </button>
      </form>
      <div class="mt-3 text-center">
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterForm',
  data() {
    return {
      loading: false,
      error: null,
      formData: {
        username: '',
        email: '',
        full_name: '',
        phone_number: '',
        address: '',
        pin_code: '',
        password: '',
        role: 'customer',
        service: '',
        experience: 0,
        description: ''
      },
      services: [] // Stores fetched services
    };
  },
  async mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/services');
        this.services = response.data;
        console.log("Services fetched:", this.services);
      } catch (err) {
        console.error('Error fetching services:', err);
        this.error = 'Failed to load services. Please try again.';
      }
    },
    
    validateForm() {
      // Basic validation
      if (!this.formData.username || this.formData.username.length < 3) {
        this.error = 'Username must be at least 3 characters long';
        return false;
      }
      
      if (!this.formData.email || !this.isValidEmail(this.formData.email)) {
        this.error = 'Please enter a valid email address';
        return false;
      }
      
      if (!this.formData.password || this.formData.password.length < 6) {
        this.error = 'Password must be at least 6 characters long';
        return false;
      }
      
      if (!this.formData.full_name || this.formData.full_name.length < 2) {
        this.error = 'Full name must be at least 2 characters long';
        return false;
      }
      
      if (!this.formData.phone_number || this.formData.phone_number.length < 10) {
        this.error = 'Please enter a valid phone number';
        return false;
      }
      
      if (!this.formData.address || this.formData.address.length < 5) {
        this.error = 'Please enter a valid address';
        return false;
      }
      
      if (!this.formData.pin_code || this.formData.pin_code.length < 6) {
        this.error = 'Please enter a valid PIN code';
        return false;
      }
      
      // Professional-specific validation
      if (this.formData.role === 'professional') {
        if (!this.formData.service) {
          this.error = 'Please select a service type';
          return false;
        }
        
        if (this.formData.experience < 0) {
          this.error = 'Experience must be a positive number';
          return false;
        }
        
        if (!this.formData.description || this.formData.description.length < 10) {
          this.error = 'Description must be at least 10 characters long';
          return false;
        }
      }
      
      return true;
    },
    
    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    
    async handleSubmit() {
      if (this.loading) return; // Prevent duplicate submission
      
      this.error = null;
      
      // Validate form
      if (!this.validateForm()) {
        return;
      }
      
      this.loading = true;

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/register', this.formData);
        console.log('Registration successful:', response.data);
        
        // Show success message
        alert('Registration successful! Please login with your credentials.');
        
        // Redirect to login
        this.$router.push('/login');

      } catch (err) {
        console.error('Registration error:', err);
        
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = 'Registration failed. Please try again.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>