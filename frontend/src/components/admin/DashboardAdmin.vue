<template>
  <div class="dashboard-admin">
    <!-- Overview Section -->
    <div class="overview-tab">
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <p class="card-text display-4">{{ users.length }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Services</h5>
              <p class="card-text display-4">{{ services.length }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Open Requests</h5>
              <p class="card-text display-4">{{ openRequests.length }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h5>Recent Requests</h5>
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>User</th>
                <th>Service</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in recentRequests" :key="request.id">
                <td>{{ formatDate(request.date_of_request) }}</td>
                <td>{{ request.customer_id }}</td>
                <td>{{ request.service_id }}</td>
                <td>
                  <span class="badge" :class="getStatusClass(request.status)">
                    {{ request.service_status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardAdmin',
  data() {
    return {
      users: [],
      services: [],
      allRequests: []
    };
  },
  computed: {
    openRequests() {
      return this.allRequests.filter(r => r.service_status !== 'closed');
    },
    recentRequests() {
      return [...this.allRequests]
        .sort((a, b) => new Date(b.date_of_request) - new Date(a.date_of_request))
        .slice(0, 5);
    }
  },
  methods: {
    async loadData() {
      console.log("🔄 Fetching data...");
      try {
        const [servicesRes, requestsRes, usersRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/admin/services'),
          axios.get('http://127.0.0.1:5000/api/admin/requests'),
          axios.get('http://127.0.0.1:5000/api/admin/users')
        ]);

        this.services = Array.isArray(servicesRes.data) ? servicesRes.data : Object.values(servicesRes.data);
        this.allRequests = Array.isArray(requestsRes.data) ? requestsRes.data : Object.values(requestsRes.data);
        this.users = Array.isArray(usersRes.data.users) ? usersRes.data.users : Object.values(usersRes.data);

        console.log("✅ Data loaded:", {
          services: this.services,
          requests: this.allRequests,
          users: this.users
        });
      } catch (error) {
        console.error("❌ Error fetching data:", error.response?.data || error.message);
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'requested': return 'bg-warning text-dark';
        case 'accepted': return 'bg-primary';
        case 'completed': return 'bg-success';
        default: return 'bg-secondary';
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    }
  },
  mounted() {
    this.loadData();
  }
};
</script>
