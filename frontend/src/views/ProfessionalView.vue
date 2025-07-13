<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-2 bg-success min-vh-100">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-4 text-white">
          <span class="fs-4 mb-4">Professional Dashboard</span>
          <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start w-100">
            <li class="nav-item w-100">
              <router-link to="/professional/dashboard" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-house-door me-2"></i> Dashboard
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/professional/requests" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-list-check me-2"></i> Service Requests
              </router-link>
            </li>
          </ul>
          <hr class="w-100">
          <div class="w-100 mb-3">
            <button class="btn btn-outline-light w-100" @click="handleLogout">
              <i class="bi bi-box-arrow-right me-2"></i> Logout
            </button>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="col-md-10 p-4">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfessionalView',
  methods: {
    async handleLogout() {
      try {
        localStorage.removeItem('token');
        this.$router.push('/login');
        console.log('✅ Logged out successfully');
      } catch (error) {
        console.error('❌ Logout failed:', error.response?.data || error.message);
        alert('Failed to log out. Please try again.');
      }
    }
  },
  async beforeMount() {
    try {
      if (!localStorage.getItem('token')) {
        this.$router.push('/login');
      }
    } catch (error) {
      console.error('❌ Authentication check failed:', error.response?.data || error.message);
      this.$router.push('/login');
    }
  }
};
</script>
