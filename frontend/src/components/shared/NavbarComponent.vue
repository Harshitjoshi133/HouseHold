<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">A-Z Household Services</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && userRole === 'admin'">
              <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && userRole === 'customer'">
              <router-link class="nav-link" to="/customer">Customer Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && userRole === 'professional'">
              <router-link class="nav-link" to="/professional">Professional Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && userRole === 'customer'">
              <router-link class="nav-link" to="/services">Find Services</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <template v-if="isAuthenticated">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                  {{ username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li><a class="dropdown-item" href="#" @click="logout">Logout</a></li>
                </ul>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/login">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/register">Register</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  <script>
  export default {
    name: 'NavbarComponent',
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('token'); // ✅ Check if token exists
    },

      userRole() {
        return !!localStorage.getItem('role')
      },
      username() {
        return 'Daksh 21f3001236';
      }
    },
    methods: {
      logout() {
        this.$store.dispatch('auth/logout');
        this.$router.push('/');
      }
    }
  }
  </script>
  
  