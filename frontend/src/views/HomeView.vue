<template>
    <div>
      <section class="hero-section bg-primary text-white py-5">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h1 class="display-4 fw-bold">A-Z Household Services</h1>
              <p class="lead">Your one-stop solution for all household service needs</p>
              <div v-if="!isLoggedIn">
                <router-link to="/register" class="btn btn-light btn-lg me-2">Register</router-link>
                <router-link to="/login" class="btn btn-outline-light btn-lg">Login</router-link>
              </div>
              <div v-else>
                <router-link :to="userDashboardLink" class="btn btn-light btn-lg">Go to Dashboard</router-link>
              </div>
            </div>
            <div class="col-md-6 d-none d-md-block">
              <img src="./logo.jpeg" alt="Home Services" class="img-fluid" />

            </div>
          </div>
        </div>
      </section>
  
      <section class="services-section py-5">
        <div class="container">
          <h2 class="text-center mb-4">Our Services</h2>
          <div class="row" v-if="services.length">
            <div class="col-md-4 mb-4" v-for="service in services" :key="service.id">
              <ServiceCard :service="service" />
            </div>
          </div>
          <div v-else class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </section>
  
      <section class="bg-light py-5">
        <div class="container">
          <h2 class="text-center mb-4">How It Works</h2>
          <div class="row">
            <div class="col-md-4 mb-4">
              <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                  <div class="display-1 mb-3 text-primary">1</div>
                  <h3>Book a Service</h3>
                  <p>Choose from our wide range of household services and book at your convenience.</p>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-4">
              <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                  <div class="display-1 mb-3 text-primary">2</div>
                  <h3>Get a Professional</h3>
                  <p>Our verified professionals will accept your request and visit your location.</p>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-4">
              <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                  <div class="display-1 mb-3 text-primary">3</div>
                  <h3>Rate &amp; Review</h3>
                  <p>After service completion, rate your experience and provide feedback.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
import axios from 'axios'
import { mapGetters } from 'vuex'
import ServiceCard from '../components/shared/ServiceCard.vue'

export default {
  name: 'HomeView',
  components: {
    ServiceCard
  },
  data() {
    return {
      services: []
    }
  },
  computed: {
    ...mapGetters('auth', ['isLoggedIn', 'userRole']), // ✅ Ensure 'auth' module exists

    userDashboardLink() {
      switch (this.userRole) {
        case 'admin': return '/admin/dashboard'
        case 'customer': return '/customer/dashboard'
        case 'professional': return '/professional/dashboard'
        default: return '/login'
      }
    }
  },
  methods: {
    async loadServices() {
      try {
        const response = await axios.get('http://localhost:5000/api/services') // ✅ Replace with your actual API URL
        this.services = response.data
        console.log('Fetched services:', this.services) // ✅ Debugging line
      } catch (error) {
        console.error('Failed to load services:', error)
      }
    }
  },
  mounted() {
    this.loadServices()
  }
}
</script>

  