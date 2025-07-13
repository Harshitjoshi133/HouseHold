<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title mb-4">User Management</h4>

      <!-- Navigation Tabs -->
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'customers' }" href="#" @click.prevent="activeTab = 'customers'">
            Customers
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'professionals' }" href="#" @click.prevent="activeTab = 'professionals'">
            Service Professionals
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'pending' }" href="#" @click.prevent="activeTab = 'pending'">
            Pending Approvals
            <span v-if="pendingProfessionals.length" class="badge bg-danger ms-2">{{ pendingProfessionals.length }}</span>
          </a>
        </li>
      </ul>

      <!-- Search Input -->
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Search by name or email" v-model="searchQuery" />
      </div>

      <!-- Customers Table -->
      <div v-if="activeTab === 'customers'">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Verified</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredCustomers" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.user.full_name }}</td>
              <td>{{ user.user.email }}</td>
              <td>
                <span class="badge" :class="user.is_verified ? 'bg-success' : 'bg-warning'">
                  {{ user.is_verified ? 'Verified' : 'Not Verified' }}
                </span>
              </td>
              <td>
                <span class="badge" :class="user.is_blocked ? 'bg-danger' : 'bg-success'">
                  {{ user.is_blocked ? 'Blocked' : 'Active' }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm" :class="user.is_blocked ? 'btn-success' : 'btn-danger'" @click="toggleUserStatus(user)">
                  {{ user.is_blocked ? 'Unblock' : 'Block' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Service Professionals Table -->
      <div v-if="activeTab === 'professionals'">
        <table class="table table-striped">
          <thead>
            <tr> 
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Experience</th>
              <th>Service ID</th>
              <th>Average Rating</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pro in filteredProfessionals" :key="pro.id">
              <td>{{ pro.id }}</td>
              <td>{{ pro.name }}</td>
              <td>{{ pro.email }}</td>
              <td>{{ pro.experience }} years</td>
              <td>{{ pro.service_id }}</td>
              <td>{{ "⭐".repeat(pro.avg_rating) }}</td>
              <td>
                <span class="badge" :class="pro.is_blocked ? 'bg-danger' : 'bg-success'">
                  {{ pro.is_blocked ? 'Blocked' : 'Active' }}
                </span>
              </td>
              <td>
                <button v-if="!pro.is_verified" class="btn btn-sm btn-primary" @click="approveProfessional(pro.id)">
                  Approve
                </button>
                <button class="btn btn-sm" :class="pro.is_verified ? 'btn-success' : 'btn-danger'" @click="approveProfessional(pro.id)">
                  {{ pro.is_blocked ? 'Unblock' : 'Block' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pending Professionals -->
      <div v-if="activeTab === 'pending'">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Document</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pro in pendingProfessionals" :key="pro.id">
              <td>{{ pro.id }}</td>
              <td>{{ pro.name }}</td>
              <td>{{ pro.email }}</td>
              <td>
  <a v-if="pro.document_path" @click.prevent="downloadDocument(pro.document_path)">
    View Document
  </a>
  <span v-else>No Document Available</span>
</td>

              <td>
                <button class="btn btn-sm btn-success" @click="approveProfessional(pro.id)">Approve</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserManagement',
  data() {
    return {
      activeTab: 'customers',
      searchQuery: '',
      customers: [],
      professionals: []
    };
  },
  computed: {
    filteredCustomers() {
      if (!this.searchQuery) return this.customers;
      const query = this.searchQuery.toLowerCase();
      return this.customers.filter(user =>
        user.user.full_name.toLowerCase().includes(query) || 
        user.user.email.toLowerCase().includes(query)
      );
    },
    filteredProfessionals() {
      return this.professionals.map(pro => ({
        id: pro.id,
        name: pro.user.full_name,
        email: pro.user.email,
        experience: pro.experience,
        service_id: pro.service_id || 'N/A',
        avg_rating:pro.avg_rating,
        is_verified: pro.is_verified,
        is_blocked: pro.is_blocked,
        document_path:pro.document_path
      }));
    },
    pendingProfessionals() {
      console.log(this.filteredProfessionals.filter(pro => !pro.is_verified));
      return this.filteredProfessionals.filter(pro => !pro.is_verified);
    }
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async downloadDocument(documentPath) {
    if (!documentPath) return; // Prevent download if no path

    try {
      const url = `http://127.0.0.1:5000/uploads/${documentPath}`;
      const link = document.createElement('a');
      link.href = url;
      const filename = documentPath.substring(documentPath.lastIndexOf('/') + 1);
      link.setAttribute('download', filename); // Set download filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Clean up
      window.URL.revokeObjectURL(url); // Clean up
    } catch (error) {
      console.error('❌ Error downloading document:', error);
      alert('Failed to download document.');
    }
  },
    async fetchUsers() {
      try {
        const [customersResponse, professionalsResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/admin/customers'),
          axios.get('http://127.0.0.1:5000/api/admin/professionals')
        ]);

        this.customers = customersResponse.data;
        this.professionals = professionalsResponse.data;

        console.log("✅ Customers fetched:", this.customers);
        console.log("✅ Professionals fetched:", this.professionals);
        console.log(this.professionals[1].name)
      } catch (error) {
        console.error("❌ Error fetching users:", error.response?.data || error.message);
      }
    },
    async approveProfessional(user_id) {
      try {
        const response=await axios.put(`http://127.0.0.1:5000/api/admin/professionals/${user_id}/verify`);
        console.log(response.data);

        alert("Succesful")
      } catch (error) {
        alert("Failed")
        console.error("❌ Error fetching users:", error.response?.data || error.message);
      }
    },
    async toggleUserStatus(user) {
      try {
        const endpoint = user.is_blocked
          ? `http://127.0.0.1:5000/api/admin/users/${user.id}/unblock`
          : `http://127.0.0.1:5000/api/admin/users/${user.id}/block`;

        await axios.put(endpoint);

        user.is_blocked = !user.is_blocked;
        console.log(`🔄 User ${user.id} status changed to: ${user.is_blocked ? 'Blocked' : 'Active'}`);
        alert(`User ${user.id} is now ${user.is_blocked ? 'Blocked' : 'Active'}`);
      } catch (error) {
        console.error("❌ Error updating user status:", error.response?.data || error.message);
        alert("Failed to update user status. Please try again.");
      }
    }
  }
};
</script>
