<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
              <h3 class="text-center mb-0">A-Z Household Services - Login</h3>
            </div>
            <div class="card-body">
              <LoginForm />
              <div class="text-center mt-3">
                <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import LoginForm from '../components/auth/LoginForm.vue';
  
  export default {
    name: 'LoginView',
    components: {
      LoginForm
    }
  }
  </script>