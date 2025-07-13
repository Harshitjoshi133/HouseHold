<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-2 bg-info min-vh-100">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-4 text-white">
          <span class="fs-4 mb-4">Customer Dashboard</span>
          <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start w-100">
            <li class="nav-item w-100">
              <router-link to="/customer/dashboard" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-house-door me-2"></i> Dashboard
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/customer/search" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-search me-2"></i> Search Services
              </router-link>
            </li>
            <li class="nav-item w-100">
              <router-link to="/customer/services" class="nav-link px-0 text-white" active-class="active bg-primary">
                <i class="bi bi-search me-2"></i> My Services
              </router-link>
            </li>
          </ul>
          <hr class="w-100">
          <div class="w-100 mb-3">
            <button class="btn btn-outline-light w-100" @click="logout">
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
  name: 'CustomerView',
  methods: {
    logout() {
      console.log("🚪 Logging out...");
      localStorage.removeItem('token'); // ✅ Clear Token
      localStorage.removeItem('role');  // ✅ Clear Role
      this.$router.push('/login');
    }
  },
  beforeMount() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    console.log("🔍 Checking Authentication -> Token:", token, "Role:", role);

    if (!token || role !== 'customer') {
      console.warn("🚨 Unauthorized access! Redirecting to /login...");
      this.$router.push('/login');
    }
  }
}
</script>
