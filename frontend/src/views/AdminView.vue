<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-2 bg-dark min-vh-100">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-4 text-white">
          <span class="fs-4 mb-4">Admin Dashboard</span>
          <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start w-100">
            <li class="nav-item w-100">
              <router-link to="/admin/dashboard" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-speedometer2 me-2"></i> Dashboard
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/admin/services" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-tools me-2"></i> Service Management
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/admin/users" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-people me-2"></i> User Management
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/admin/export" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-file-earmark-arrow-down me-2"></i> Export Data
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
  name: 'AdminView',
  data() {
    return {
      userRole: localStorage.getItem('role') || '',
    };
  },
  methods: {
    async handleLogout() {
      try {
        console.log("🔍 Logging out...");
        localStorage.clear()
        this.$router.push('/login');
      } catch (error) {
        console.error("❌ Logout Failed:", error);
      }
    }
  },
  created() {
    console.log("🔍 Checking admin role:", this.userRole);
    if (this.userRole !== 'admin') {
      console.warn("⛔ Unauthorized! Redirecting to login...");
      this.$router.push('/login');
    }
  }
};
</script>
