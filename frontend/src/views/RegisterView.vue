<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="text-center mb-0">A-Z Household Services - Register</h3>
          </div>
          <div class="card-body">
            <RegisterForm />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RegisterForm from '../components/auth/RegisterForm.vue';

export default {
  name: 'RegisterView',
  components: {
    RegisterForm
  }
};
</script>
