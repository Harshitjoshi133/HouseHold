<template>
  <div class="card h-100 shadow-sm">
    <div class="card-body">
      <h5 class="card-title">{{ service.name }}</h5>
      <h6 class="card-subtitle mb-2 text-muted">₹{{ service.price }}</h6>
      <p class="card-text">{{ service.description }}</p>
      <div class="d-flex justify-content-between align-items-center">
        <span class="badge bg-info text-dark">{{ service.time_required }} hrs</span>
        <button 
          class="btn btn-primary" 
          @click="redirectToService"
          :disabled="!isActionable"
        >
          {{ actionText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServiceCard',
  props: {
    service: {
      type: Object,
      required: true
    },
    actionText: {
      type: String,
      default: 'Book Now'
    },
    isActionable: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    redirectToService() {
  if (!this.service || !this.service.id) {
    console.error("❌ Service ID is undefined:", this.service);
    return;
  }
  console.log("🔗 Redirecting to service:", this.service.id);
  this.$router.push({ name: 'ServiceRequest', params: { id: this.service.id } });
}

  }
}
</script>
