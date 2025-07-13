<template>
    <div class="customer-dashboard">
      <h1>Customer Dashboard</h1>
      
      <div class="dashboard-stats">
        <div class="stat-card">
          <h3>Active Requests</h3>
          <p class="stat-number">{{ activeRequests.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Completed Services</h3>
          <p class="stat-number">{{ completedRequests.length }}</p>
        </div>
      </div>
  
      <div class="recent-activity">
        <h2>Recent Activity</h2>
        <div v-if="activeRequests.length > 0" class="request-list">
          <div v-for="request in activeRequests" :key="request.id" class="request-item">
            <div class="request-header">
              <h3>{{ request.serviceName }}</h3>
              <span :class="['status-badge', request.status.toLowerCase()]">{{ request.status }}</span>
            </div>
            <p class="request-date">Requested on: {{ formatDate(request.scheduled_date) }}</p>
            <p class="professional" v-if="request.professional">
              Professional: {{ request.professional.name }}
              <span class="contact-info" v-if="request.status === 'In Progress'">
                Contact: {{ request.professional.phone }}
              </span>
            </p>
            <div class="request-actions">
              <button v-if="request.status === 'Pending'" @click="cancelRequest(request.id)" class="btn btn-danger">Cancel</button>
              <button v-if="request.status === 'Completed'" @click="rateService(request.id)" class="btn btn-primary">Rate Service</button>
              <button v-if="request.status === 'In Progress'" @click="viewDetails(request.id)" class="btn btn-info">View Details</button>
            </div>
          </div>
        </div>
        <p v-else>No active service requests. Start by searching for services.</p>
      </div>
    </div>
  </template>
  
  <script>
import axios from 'axios';

export default {
  name: "CustomerDashboard",
  data() {
    return {
      activeRequests: [],
      completedRequests: []
    };
  },
  created() {
    this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      try {
        console.log("🔄 Fetching customer requests...");
        const user_id=localStorage.getItem('user_id')
        const response = await axios.get(`http://127.0.0.1:5000/api/customer/service/requests/${user_id}`); // ✅ Replace with your actual API endpoint
        const requests = response.data;
        // ✅ Categorize requests
        this.activeRequests = requests.filter(req => 
            ['pending', 'approved', 'in progress','requested'].includes(req.status.toLowerCase())
          );
      this.completedRequests = requests.filter(req => 
        ['completed', 'closed'].includes(req.status.toLowerCase())
      );


        console.log("✅ Requests fetched successfully:", requests);
      } catch (error) {
        console.error("❌ Error fetching requests:", error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    async cancelRequest(requestId) {
      if (confirm('Are you sure you want to cancel this request?')) {
        try {
          console.log(`🚨 Cancelling request ID: ${requestId}`);
          await axios.post(`/api/requests/${requestId}/cancel`); // ✅ Adjust API endpoint if needed
          this.fetchRequests();
          this.$toast.success('Request cancelled successfully');
        } catch (error) {
          console.error("❌ Failed to cancel request:", error);
          this.$toast.error('Failed to cancel request');
        }
      }
    },
    rateService(requestId) {
      this.$router.push(`/requests/${requestId}/rate`);
    },
    viewDetails(requestId) {
      this.$router.push(`/requests/${requestId}`);
    }
  }
};
</script>

  <style scoped>
  .customer-dashboard {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .dashboard-stats {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .stat-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    flex: 1;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #3273dc;
  }
  
  .recent-activity, .quick-actions {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .request-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .request-item {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 15px;
    background-color: #fcfcfc;
  }
  
  .request-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .status-badge {
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
  }
  
  .pending {
    background-color: #ffdd57;
    color: #806600;
  }
  
  .approved {
    background-color: #48c774;
    color: white;
  }
  
  .in.progress {
    background-color: #3298dc;
    color: white;
  }
  
  .completed {
    background-color: #8953E1;
    color: white;
  }
  
  .request-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
  }
  
  .btn {
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    border: none;
  }
  
  .btn-primary {
    background-color: #3273dc;
    color: white;
  }
  
  .btn-success {
    background-color: #48c774;
    color: white;
  }
  
  .btn-danger {
    background-color: #f14668;
    color: white;
  }
  
  .btn-info {
    background-color: #3298dc;
    color: white;
  }
  </style>