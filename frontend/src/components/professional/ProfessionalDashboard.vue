<template>
  <div class="professional-dashboard">
    <h1>Professional Dashboard</h1>

    <div class="dashboard-stats">
      <div class="stat-card">
        <h3>Pending Requests</h3>
        <p class="stat-number">{{ stats.pendingRequests }}</p>
      </div>
      <div class="stat-card">
        <h3>Accepted Requests</h3>
        <p class="stat-number">{{ stats.acceptedRequests }}</p>
      </div>
      <div class="stat-card">
        <h3>Completed Jobs</h3>
        <p class="stat-number">{{ stats.completedRequests }}</p>
      </div>
    </div>

    <!-- Document Upload Section -->
    <div v-if="!professional.is_verified" class="upload-section">
      <h2>Upload Verification Document</h2>
      <input type="file" ref="documentFile" @change="handleFileUpload" />
      <button @click="uploadDocument" class="btn btn-primary">Upload</button>
      <p v-if="uploadMessage" class="upload-message">{{ uploadMessage }}</p>
    </div>

    <div class="dashboard-content">
      <!-- Pending Requests Section -->
      <div class="requests-panel">
        <div class="panel-header">
          <h2>Pending Service Requests</h2>
          <button @click="fetchRequests" class="refresh-btn">
            <span class="refresh-icon">↻</span> Refresh
          </button>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading requests...</p>
        </div>
        <div v-else-if="newRequests.length === 0" class="empty-state">
          <p>No pending service requests available.</p>
        </div>

        <div v-else class="request-list">
          <div v-for="request in newRequests" :key="request.id" class="request-card">
            <div class="request-header">
              <h3>{{ request.service.name }}</h3>
              <span class="request-date">{{ formatDate(request.scheduled_date) }}</span>
            </div>
            <div class="request-info">
              <p><strong>Customer:</strong> {{ request.customer_id }}</p>
              <p><strong>Location:</strong> {{ request.address }}</p>
              <p><strong>Scheduled:</strong> {{ formatDate(request.scheduled_date) }}</p>
            </div>
            <div class="request-actions">
              <button @click="acceptService(request.id)" class="btn btn-success">Accept</button>
              <button @click="rejectService(request.id)" class="btn btn-danger">Reject</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Accepted Requests Section -->
      <div class="requests-panel">
        <h2>Accepted Jobs</h2>
        <div v-if="acceptedRequests.length === 0" class="empty-state">
          <p>No accepted jobs yet.</p>
        </div>
        <div v-else class="request-list">
          <div v-for="request in acceptedRequests" :key="request.id" class="request-card">
            <div class="request-header">
              <h3>{{ request.service.name }}</h3>
              <span class="request-date">{{ formatDate(request.scheduled_date) }}</span>
            </div>
            <div class="request-info">
              <p><strong>Customer:</strong> {{ request.customer_id }}</p>
              <p><strong>Location:</strong> {{ request.address }}</p>
              <p><strong>Scheduled:</strong> {{ formatDate(request.scheduled_date) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Requests Section -->
      <div class="requests-panel">
        <h2>Completed Jobs</h2>
        <div v-if="completedRequests.length === 0" class="empty-state">
          <p>No completed jobs yet.</p>
        </div>
        <div v-else class="request-list">
          <div v-for="request in completedRequests" :key="request.id" class="request-card completed">
            <div class="request-header">
              <h3>{{ request.service.name }}</h3>
              <span class="request-date">{{ formatDate(request.scheduled_date) }}</span>
            </div>
            <div class="request-info">
              <p><strong>Customer:</strong> {{ request.customer_id }}</p>
              <p><strong>Location:</strong> {{ request.address }}</p>
              <p><strong>Completed on:</strong> {{ formatDate(request.date_of_completion) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "ProfessionalDashboard",
  data() {
    return {
      loading: true,
      stats: {
        pendingRequests: 0,
        acceptedRequests: 0,
        completedRequests: 0,
      },
      newRequests: [],
      acceptedRequests: [],
      completedRequests: [],
      baseURL: "http://127.0.0.1:5000/api",
      user_id: localStorage.getItem("user_id"),
      professional: {
        is_verified: false,
      },
      uploadMessage: "",
      selectedFile: null,
    };
  },
  created() {
    this.fetchRequests();
    this.fetchProfessionalDetails();
    this.fetchcompletedRequests();
    this.fetchacceptedRequests();
  },
  methods: {
    fetchRequests() {
      this.loading = true;
      axios
        .get(`${this.baseURL}/professional/service-requests/pending/${this.user_id}`)
        .then(response => {
          this.newRequests = response.data;
          this.stats.pendingRequests = this.newRequests.length;
        })
        .catch(error => console.error("Error fetching requests:", error))
        .finally(() => this.loading = false);
    },
    fetchacceptedRequests() {
      this.loading = true;
      axios
        .get(`${this.baseURL}/professional/service-requests/accepted/${this.user_id}`)
        .then(response => {
          this.acceptedRequests = response.data;
          this.stats.acceptedRequests = this.acceptedRequests.length;
        })
        .catch(error => console.error("Error fetching requests:", error))
        .finally(() => this.loading = false);
    },
    fetchcompletedRequests() {
      this.loading = true;
      axios
        .get(`${this.baseURL}/professional/service-requests/completed/${this.user_id}`)
        .then(response => {
          this.completedRequests = response.data;
          this.stats.completedRequests = this.completedRequests.length;
        })
        .catch(error => console.error("Error fetching requests:", error))
        .finally(() => this.loading = false);
    },
    fetchProfessionalDetails() {
      axios
        .get(`${this.baseURL}/professional/details/${this.user_id}`)
        .then(response => {
          this.professional = response.data.professional;
          console.log(this.professional)
        })
        .catch(error => console.error("Error fetching professional details:", error));
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadDocument() {
      if (!this.selectedFile) {
        this.uploadMessage = "Please select a file.";
        return;
      }
      let formData = new FormData();
      formData.append("document", this.selectedFile);
      formData.append("user_id", this.user_id);
      axios.post(`${this.baseURL}/professional/upload-document`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then(response => {
          console.log(response)
          this.uploadMessage = "Document uploaded successfully!";
          this.fetchProfessionalDetails();
          alert(this.uploadMessage)
        })
        .catch(error => {
          console.error("Error uploading document:", error);
          this.uploadMessage = "Failed to upload document.";
          alert(this.uploadMessage)
        });
    },
    acceptService(requestId) {
  axios.put(`${this.baseURL}/professional/service-requests/${requestId}/accept/${this.user_id}`)
    .then(() => {
      console.log(`Service request ${requestId} accepted successfully.`);
      alert("Service accepted successfully");
      this.fetchRequests();
    })
    .catch(error => {
      console.error("Error accepting request:", error);
      alert("Failed to accept service request.");
    });
},

rejectService(requestId) {
  axios.put(`${this.baseURL}/service-requests/professional/${requestId}/reject/${this.user_id}`)
    .then(() => {
      console.log(`Service request ${requestId} rejected successfully.`);
      alert("Service rejected successfully");
      this.fetchRequests();
    })
    .catch(error => {
      console.error("Error rejecting request:", error);
      alert("Failed to reject service request.");
    });
},
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric", month: "short", day: "numeric"
      });
    },
  },
};
</script>

<style scoped>
.professional-dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
}

h1, h2, h3 {
  color: #333;
}

.dashboard-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-card {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #007bff;
}

.requests-panel {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.refresh-btn {
  background: #007bff;
  color: #fff;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #0056b3;
}

.loading-state {
  text-align: center;
  color: #555;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  color: #888;
}

.request-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.request-card {
  padding: 15px;
  border-radius: 8px;
  background: #f9f9f9;
  border-left: 5px solid #007bff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.completed {
  background: #d4edda !important;
  border-left: 5px solid #28a745 !important;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.request-info p {
  margin: 5px 0;
}

.request-actions {
  margin-top: 10px;
}

.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  margin-right: 5px;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}

</style>
