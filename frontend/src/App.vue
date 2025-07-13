<template>
    <div id="app">
      <NavbarComponent />
      <main class="container py-4">
        <router-view />
      </main>
      <FooterComponent />
    </div>
  </template>
  
  <script>
  import NavbarComponent from './components/shared/NavbarComponent.vue'
  import FooterComponent from './components/shared/FooterComponent.vue'
  
  export default {
    name: 'App',
    components: {
      NavbarComponent,
      FooterComponent
    }
  }
  </script>
  