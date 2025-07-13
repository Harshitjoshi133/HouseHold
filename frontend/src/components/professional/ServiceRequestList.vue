<template>
  <div class="service-request-list">
    <h1>Accepted Service Requests</h1>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading service requests...</p>
    </div>

    <div v-else-if="filteredRequests.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>No accepted service requests found</h3>
      <p>Try again later.</p>
    </div>

    <div v-else class="request-grid">
      <div v-for="request in paginatedRequests" :key="request.id" class="request-card">
        <div class="request-header">
          <h3>{{ request.serviceType }}</h3>
          <span :class="['status-badge', request.status.toLowerCase()]">{{ request.status }}</span>
        </div>

        <div class="request-info">
          <p><strong>Customer:</strong> {{ request.customer_name }}</p>
          <p><strong>Phone:</strong> {{ request.customer_phone}}</p>
          <p><strong>Location:</strong> {{ request.address }}</p>
          <p><strong>Requested:</strong> {{ request.date_of_request }}</p>
          <p v-if="request.scheduledDate"><strong>Scheduled:</strong> {{ request.scheduledDate}} ({{ request.timeSlot }})</p>
          <p><strong>Description:</strong> {{ request.service.description}}</p>
        </div>

        <div class="request-actions">
          <button @click="completeJob(request.id)" class="btn btn-info">Completed</button>
        </div>
      </div>
    </div>

    <div class="pagination-controls" v-if="filteredRequests.length > 0">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="page-btn">Previous</button>
      <div class="page-numbers">
        <button v-for="page in totalPages" :key="page" :class="['page-number', currentPage === page ? 'active' : '']" @click="changePage(page)">
          {{ page }}
        </button>
      </div>
      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="page-btn">Next</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ServiceRequestList",
  data() {
    return {
      loading: true,
      serviceRequests: [],
      filteredRequests: [],
      currentPage: 1,
      itemsPerPage: 10
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredRequests.length / this.itemsPerPage);
    },
    paginatedRequests() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredRequests.slice(start, start + this.itemsPerPage);
    }
  },
  created() {
    this.fetchServiceRequests();
  },
  methods: {
    async fetchServiceRequests() {
      try {
        this.loading = true;
        console.log("Fetching accepted service requests...");
        const user_id=localStorage.getItem('user_id')
        const response = await axios.get(`http://127.0.0.1:5000/api/professional/service-requests/accepted/${user_id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });

        this.serviceRequests = response.data;
        this.filteredRequests = response.data;
        console.log(`Response`,this.serviceRequests)
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },
    changePage(page) {
      this.currentPage = page;
    },
    async updateRequestStatus(requestId,user_id) {
      try {
        console.log(`Updating status of request ${requestId} to...${user_id}`);

        await axios.put(`http://127.0.0.1:5000/api/professional/service-requests/${requestId}/complete/${user_id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        
        alert("Completed Request")
        this.fetchServiceRequests();
      } catch (error) {
        alert("Failed to mark")
        console.error("Error updating request status:", error);
      }
    },
    completeJob(requestId) {
      const user_id=localStorage.getItem('user_id');
      this.updateRequestStatus(requestId,user_id);
    }
  }
};
</script>

<style scoped>
.service-request-list {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 5px solid #ddd;
  border-top: 5px solid dodgerblue;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #777;
}

.empty-icon {
  font-size: 40px;
}

.request-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.request-card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background: white;
  transition: transform 0.2s ease-in-out;
}

.request-card:hover {
  transform: translateY(-5px);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 5px;
  font-weight: bold;
  text-transform: capitalize;
}

.status-badge.accepted {
  background: orange;
  color: white;
}

.status-badge.in-progress {
  background: royalblue;
  color: white;
}

.status-badge.completed {
  background: green;
  color: white;
}

.request-info p {
  margin: 5px 0;
  font-size: 14px;
}

.request-actions {
  margin-top: 15px;
}

.btn {
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.btn-info {
  background: dodgerblue;
  color: white;
}

.btn-info:hover {
  background: #007bff;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.page-btn, .page-number {
  padding: 8px 12px;
  margin: 5px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  background: #ddd;
  transition: background 0.3s ease;
}

.page-number.active, .page-btn:hover {
  background: dodgerblue;
  color: white;
}
</style>
