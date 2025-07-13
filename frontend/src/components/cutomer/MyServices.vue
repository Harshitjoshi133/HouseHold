<template>
  <div class="my-services">
    <h1>My Services</h1>

    <div class="service-stats">
      <div class="stat-card">
        <h3>All Service Requests</h3>
        <p class="stat-number">{{ serviceRequests.length }}</p>
      </div>
      <div class="stat-card">
        <h3>Accepted Services</h3>
        <p class="stat-number">{{ acceptedRequests.length }}</p>
      </div>
      <div class="stat-card">
        <h3>Completed Services</h3>
        <p class="stat-number">{{ completedRequests.length }}</p>
      </div>
    </div>

<div class="request-list">
  <h2>Service Requests</h2>
  <div v-if="serviceRequests.length > 0">
    <div v-for="request in serviceRequests" :key="request.id" class="request-item">
      <div class="request-header">
        <h3>{{ request.service.name }}</h3>
        <span :class="['status-badge', request.status.toLowerCase()]">{{ request.status }}</span>
      </div>
      <p class="request-date">Requested on: {{ request.scheduled_date }}</p>
      <p class="professional">
        Professional ID: {{ request.professional_id }}
      </p>

      <div class="request-actions" v-if="request.status !== 'completed'">
        <button @click="openEditModal(request)" class="btn btn-secondary">✏️ Edit Service</button>
      </div>
      <div class="request-actions" v-if="request.status === 'completed'">
        <button @click="openRemarkModal(request)" class="btn btn-dark">📝 Post Remark</button>
      </div>
    </div>
  </div>
  <p v-else>No service requests found.</p>
</div>

<!-- Edit Service Modal -->
<!-- Edit Service Modal -->
<b-modal v-model="showEditModal" title="Edit Service">
  <b-form @submit.prevent="editService">
    <!-- Scheduled Date -->
    <b-form-group label="Scheduled Date">
      <b-form-input type="date" v-model="editServiceData.scheduled_date" required></b-form-input>
    </b-form-group>

    <!-- Remarks -->
    <b-form-group label="Remarks">
      <b-form-textarea v-model="editServiceData.remarks"></b-form-textarea>
    </b-form-group>

    <b-button type="submit" variant="primary" :disabled="editServiceData.status === 'closed'">
      Save Changes
    </b-button>
  </b-form>
</b-modal>


<!-- Post Remark Modal -->
<b-modal v-model="showRemarkModal" title="Post Remark">
  <b-form @submit.prevent="postRemark">
    <!-- Remark Input -->
    <b-form-group label="Your Remark">
      <b-form-textarea v-model="remarkData.remark" required></b-form-textarea>
    </b-form-group>

    <!-- Rating Input -->
    <b-form-group label="Rate the Service">
      <b-form-rating v-model="remarkData.rating" stars="5" variant="warning"></b-form-rating>
    </b-form-group>
    <b-button type="submit" variant="success">Submit Remark</b-button>
  </b-form>
</b-modal>


  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "MyServices",
  data() {
    return {
      serviceRequests: [],
      showEditModal: false,
      showRemarkModal: false,
      editServiceData: {
        id: null,
        service_name: ""
      },
      remarkData: {
        id: null,
        remark: ""
      }
    };
  },
  computed: {
    acceptedRequests() {
      return this.serviceRequests.filter(request => request.status === 'Accepted');
    },
    completedRequests() {
      return this.serviceRequests.filter(request => request.status === 'Completed');
    }
  },
  created() {
    this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      try {
        console.log("🔄 Fetching service requests...");
        const user_id = localStorage.getItem('user_id'); 
        const response = await axios.get(`http://127.0.0.1:5000/api/customer/service-requests/${user_id}`);
        this.serviceRequests = response.data;
        console.log(this.serviceRequests)
      } catch (error) {
        console.error("❌ Error fetching requests:", error);
      }
    },
    
    openEditModal(request) {
      this.editServiceData.id = request.id;
      this.editServiceData.service_name = request.service.name;
      this.showEditModal = true;
    },
    
    openRemarkModal(request) {
      this.remarkData.id = request.id;
      this.remarkData.remark = "";
      this.showRemarkModal = true;
    },

    async editService() {
  try {
    console.log(`✏️ Editing service ID: ${this.editServiceData.id}`);
    const user_id=localStorage.getItem('user_id');
    await axios.put(`http://127.0.0.1:5000/api/customer/service-requests/${this.editServiceData.id}`, {
      user_id:user_id,
      scheduled_date: this.editServiceData.scheduled_date,
      remarks: this.editServiceData.remarks
    });

    alert('Service updated successfully');
    this.showEditModal = false;
    this.fetchRequests();
  } catch (error) {
    console.error("❌ Failed to update service:", error);
    alert('Failed to update service');
  }
},

    async postRemark() {
  try {
    console.log(`📝 Posting remark for request ID: ${this.remarkData.id}`);
    const user_id=localStorage.getItem('user_id');
    await axios.post(`http://127.0.0.1:5000/api/customer/service-requests/${this.remarkData.id}/reviews`, {
      user_id: user_id,
      remark: this.remarkData.remark,
      rating: this.remarkData.rating // Include rating in the request
    });

    alert('Remark and rating posted successfully');
    this.showRemarkModal = false;
    this.fetchRequests(); // Refresh service requests

  } catch (error) {
    console.error("❌ Failed to post remark and rating:", error);
    alert('Failed to post remark and rating');
  }
}

  }
};
</script>

<style scoped>
.my-services {
  padding: 20px;
}
.service-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}
.stat-number {
  font-size: 24px;
  font-weight: bold;
}
.request-list {
  margin-top: 20px;
}
.request-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
}
.request-actions {
  margin-top: 10px;
}
</style>
