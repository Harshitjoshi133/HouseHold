<template>
  <div class="card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="card-title mb-0">Service Management</h4>
        <button class="btn btn-primary" @click="openAddModal">
          <i class="bi bi-plus"></i> Add New Service
        </button>
      </div>

      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Price (₹)</th>
              <th>Time Required (hrs)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.name }}</td>
              <td>{{ service.price }}</td>
              <td>{{ service.time_required }}</td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button class="btn btn-outline-primary" @click="editService(service)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-outline-danger" @click="confirmDelete(service)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Service Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1" ref="serviceModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Edit Service' : 'Add New Service' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveService">
              <div class="mb-3">
                <label class="form-label">Service Name</label>
                <input type="text" class="form-control" v-model="formData.name" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Price (₹)</label>
                <input type="number" class="form-control" v-model="formData.price" min="0" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Time Required (hrs)</label>
                <input type="number" class="form-control" v-model="formData.time_required" min="0" required />
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="closeModal">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span> Save
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete the service: <strong>{{ selectedService?.name }}</strong>?</p>
            <p class="text-danger">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteService" :disabled="deleteLoading">
              <span v-if="deleteLoading" class="spinner-border spinner-border-sm me-2"></span> Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: 'ServiceManagement',
  data() {
    return {
      services: [],
      loading: false,
      deleteLoading: false,
      isEditing: false,
      selectedService: null,
      serviceModal: null,
      deleteModal: null,
      formData: {
        name: '',
        price: 0,
        time_required: 1
      }
    };
  },
  mounted() {
    this.fetchServices();

    // Initialize Bootstrap modals
    this.$nextTick(() => {
      this.serviceModal = new Modal(this.$refs.serviceModal);
      this.deleteModal = new Modal(this.$refs.deleteModal);
    });
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/services');
        this.services = response.data;
        console.log(this.services)
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    openAddModal() {
      this.isEditing = false;
      this.resetForm();
      this.serviceModal.show();
    },
    editService(service) {
      this.selectedService = service;
      this.isEditing = true;
      this.formData = { ...service };
      this.serviceModal.show();
    },
    async saveService() {
      this.loading = true;
      try {
        if (this.isEditing) {
          await axios.put(`http://127.0.0.1:5000/api/admin/services/${this.selectedService.id}`, this.formData);
        } else {
          await axios.post('http://127.0.0.1:5000/api/admin/services', this.formData);
          alert('New Service Created Successfully')
        }
        this.fetchServices();
        this.closeModal();
      } catch (error) {
        console.error('Error saving service:', error);
        alert('Failed to save service. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    confirmDelete(service) {
      this.selectedService = service;
      this.deleteModal.show();
    },
    async deleteService() {
      this.deleteLoading = true;
      try {
        await axios.delete(`http://127.0.0.1:5000/api/admin/services/${this.selectedService.id}`);
        alert("Service Deleted Successfully")
        this.fetchServices();
        this.closeDeleteModal();
      } catch (error) {
        console.error('Error deleting service:', error);
        alert('Failed to delete service. Please try again.');
      } finally {
        this.deleteLoading = false;
      }
    },
    resetForm() {
      this.formData = {
        name: '',
        price: 0,
        time_required: 1
      };
    },
    closeModal() {
      this.serviceModal.hide();
      this.resetForm();
    },
    closeDeleteModal() {
      this.deleteModal.hide();
      this.selectedService = null;
    }
  }
};
</script>
