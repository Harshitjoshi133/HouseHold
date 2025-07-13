<template>
  <div class="service-details">
    <h2>Service Details</h2>

    <div v-if="service">
      <h3>{{ service.name }}</h3>
      <p>{{ service.description }}</p>
      <p>Base Price: ₹{{ service.price }}</p>

      <!-- Date and Time Picker -->
      <label class="input-label">
        Schedule Date & Time:
        <input type="datetime-local" v-model="requestData.scheduledDateTime" />
      </label>

      <p>Total Estimated Price: ₹{{ calculateTotal() }}</p>

      <h3>Select a Professional</h3>

      <!-- Professional Cards -->
      <div v-if="professionals.length" class="professional-cards">
        <div 
          v-for="pro in professionals" 
          :key="pro.id" 
          class="professional-card"
          :class="{ selected: requestData.professionalId === pro.id }"
          @click="requestData.professionalId = pro.id"
        >
          <h4>{{ pro.user.full_name }}</h4>
          <p>Experience: {{ pro.experience }} years</p>
          <p>Rating: ⭐ {{ pro.avg_rating }}/5</p>
          <p>Address: {{ pro.user.address }}</p>
          <p>Pin Code: {{ pro.user.pin_code }}</p>
          <p>Phone: {{ pro.user.phone_number }}</p>
          <p>Email: {{ pro.user.email }}</p>
          <button 
            class="select-btn"
            :class="{ 'selected-btn': requestData.professionalId === pro.id }"
          >
            Select
          </button>
        </div>
      </div>
      <p v-else class="no-professionals">No professionals found.</p>

      <label class="checkbox-label">
        <input type="checkbox" v-model="termsAgreed" />
        I agree to the Terms of Service
      </label>

      <button @click="submitRequest" :disabled="submitting">
        {{ submitting ? "Submitting..." : "Submit Request" }}
      </button>
    </div>

    <div v-else>
      <p>Loading service details...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      service: null,
      serviceId: null,
      professionals: [],
      requestData: {
        scheduledDateTime: "",
        professionalId: null,
      },
      termsAgreed: false,
      submitting: false,
    };
  },
  async created() {
    this.serviceId = this.$route.params.id || this.$route.query.id;
    if (!this.serviceId) {
      console.error("Service ID is missing from route");
      return;
    }
    console.log("Fetched Service ID:", this.serviceId);
    await this.fetchServiceDetails();
    await this.fetchProfessionals();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/customer/services/${this.serviceId}`
        );
        this.service = response.data.services[0];
        console.log("Service details fetched:", this.service);
      } catch (error) {
        console.error("Error fetching service details:", error);
      }
    },
    async fetchProfessionals() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/customer/services/${this.serviceId}/professionals`
        );
        this.professionals = response.data.professionals;
        console.log("Professionals fetched:", this.professionals);
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    calculateTotal() {
      return this.service ? this.service.price : 0;
    },
    async submitRequest() {
      if (!this.termsAgreed) {
        alert("You must agree to the Terms of Service to continue.");
        return;
      }
      const user_id=localStorage.getItem('user_id');
      this.submitting = true;
      const requestPayload = {
        user_id:user_id,
        service_id: this.serviceId,  // ✅ Fixed API expected key
        scheduled_date: this.requestData.scheduledDateTime,
        professional_id: this.requestData.professionalId,
        estimated_price: this.calculateTotal(),
      };

      try {
        console.log("Submitting request:", requestPayload);
        if(this.requestData.professionalId!==null){
        const response = await axios.post(
          "http://127.0.0.1:5000/api/customer/service-requests",
          requestPayload,
          { headers: { "Content-Type": "application/json" } }
        );

        console.log("Response received:", response.data);
        alert("Service request submitted successfully!");
        this.$router.push('/customer/dashboard');
        }
        else{
          alert('No Proffessional Selected')
        }
        
      } catch (error) {
        console.error("Error submitting request:", error);
        alert("Error submitting request.");
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
.service-details {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

h2, h3 {
  text-align: center;
  color: #333;
}

button {
  display: block;
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}
button:hover {
  background-color: #0056b3;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.input-label {
  display: block;
  margin: 10px 0;
  font-weight: bold;
}

input[type="datetime-local"] {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.professional-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin-top: 15px;
}

.professional-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #f9f9f9;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
}

.professional-card:hover {
  transform: scale(1.03);
}

.professional-card h4 {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 5px;
}

.select-btn {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.select-btn.selected-btn {
  background: #218838;
}

.no-professionals {
  color: #d9534f;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
}

.checkbox-label {
  display: block;
  margin-top: 10px;
  font-size: 14px;
}
</style>
