<template>
  <div class="service-search">
    <h1>Find Services</h1>

    <div class="search-container">
      <div class="search-form">
        <div class="form-row">
          <div class="form-group">
            <label for="search">Search</label>
            <input 
              type="text" 
              id="search" 
              v-model="searchQuery" 
              placeholder="Plumbing, Electrical, Cleaning, etc."
              @input="debounceSearch"
            >
          </div>          
        </div>
        <div class="form-row">    
        </div>

        <div class="form-buttons">
          <button @click="resetFilters" class="btn btn-secondary">Reset Filters</button>
          <button @click="searchServices" class="btn btn-primary">Search</button>
        </div>
      </div>
    </div>

    <div class="results-container" v-if="isSearched">
      <div class="results-header">
        <h2>{{ services.length }} Services Found</h2>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Searching for services...</p>
      </div>

      <div v-else-if="services.length === 0" class="no-results">
        <p>No services found matching your criteria. Try adjusting your filters.</p>
      </div>

      <div v-else class="service-list">
        <service-card 
          v-for="service in services" 
          :key="service.id" 
          :service="service"
          @click="viewServiceDetails(service.id)"
        />
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)" 
          class="btn-page"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)" 
          class="btn-page"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ServiceCard from '../shared/ServiceCard.vue';

export default {
  name: "ServiceSearch",
  components: {
    ServiceCard
  },
  data() {
    return {
      searchQuery: '',

      sortOption: 'relevance',
      services: [],
      isSearched: false,
      loading: false,
      currentPage: 1,
      totalPages: 0,
      itemsPerPage: 10,
      debounceTimeout: null
    };
  },
  created() {
    this.checkURLParams();
  },
  computed: {
    sortedServices() {
      console.log(`Sorting the Services`)
      if (!this.services.length) return [];

      return [...this.services].sort((a, b) => {
        switch (this.sortOption) {
          case "rating":
            return b.rating - a.rating;
          default:
            return 0; // Default to relevance (original order)
        }
      });
    },
  },
  watch: {
    sortOption() {
      console.log(`🔄 Sorting changed to: ${this.sortOption}`);
    },
  },
  methods: {
    checkURLParams() {
      const query = this.$route.query;
      if (query.search) this.searchQuery = query.search;

      if (query.search) {
        this.searchServices();
      }
    },
    debounceSearch() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchServices();
      }, 500);
    },
    async searchServices() {
      this.loading = true;
      this.isSearched = true;
      this.currentPage = 1;

      const query = {
        ...(this.searchQuery && { search: this.searchQuery }),
      };

      // Avoid redundant navigation
      if (JSON.stringify(this.$route.query) !== JSON.stringify(query)) {
        this.$router.push({ query }).catch(err => {
          if (err.name !== 'NavigationDuplicated') console.error(err);
        });
      }

      try {
        const token = localStorage.getItem('token');
        console.log("🔎 Searching services with filters:", query);
        const response = await axios.get('http://127.0.0.1:5000/api/customer/services', {
          params: { ...query, page: this.currentPage },
          headers: { Authorization: `Bearer ${token}` }
        });
        this.services = response.data.services;
        this.totalPages = response.data.totalPages;
        console.log("✅ Services found:", this.services);
      } catch (error) {
        console.error("❌ Error searching services:", error);
      } finally {
        this.loading = false;
      }
    },
    resetFilters() {
      this.searchQuery = '';
      this.sortOption = 'relevance';
      this.searchServices();
    },
    viewServiceDetails(serviceId) {
      console.log(serviceId)
      this.$router.push(`/requests/${serviceId}`);
    }
  }
};
</script>


  <style scoped>
  .service-search {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .search-container {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .search-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-row {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
  }
  
  .form-group {
    flex: 1;
    min-width: 200px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
  }
  
  input, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .form-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
  
  .btn {
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    border: none;
  }
  
  .btn-primary {
    background-color: #3273dc;
    color: white;
  }
  
  .btn-secondary {
    background-color: #f5f5f5;
    color: #333;
    border: 1px solid #ddd;
  }
  
  .results-container {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
  }
  
  .sort-options {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .service-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50px 0;
  }
  
  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 4px solid #3273dc;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .no-results {
    text-align: center;
    padding: 50px 0;
    color: #666;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    gap: 15px;
  }
  
  .btn-page {
    padding: 8px 16px;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .page-info {
    font-weight: 600;
  }
  </style>