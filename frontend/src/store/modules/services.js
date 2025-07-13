import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    services: [],
    loading: false
  },
  getters: {
    allServices: state => state.services,
    serviceById: state => id => state.services.find(service => service.id === id)
  },
  mutations: {
    SET_SERVICES(state, services) {
      state.services = services
    },
    ADD_SERVICE(state, service) {
      state.services.push(service)
    },
    UPDATE_SERVICE(state, updatedService) {
      const index = state.services.findIndex(s => s.id === updatedService.id)
      if (index !== -1) {
        state.services.splice(index, 1, updatedService)
      }
    },
    DELETE_SERVICE(state, id) {
      state.services = state.services.filter(service => service.id !== id)
    },
    SET_LOADING(state, status) {
      state.loading = status
    }
  },
  actions: {
    async fetchServices({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/services')
        commit('SET_SERVICES', response.data)
      } catch (error) {
        console.error('Error fetching services:', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createService({ commit }, serviceData) {
      
        const response = await api.post('/services', serviceData)
        commit('ADD_SERVICE', response.data)
        return response
      
    },
    async updateService({ commit }, { id, data }) {
      
        const response = await api.put(`/services/${id}`, data)
        commit('UPDATE_SERVICE', response.data)
        return response
    },
    async deleteService({ commit }, id) {
      
        await api.delete(`/services/${id}`)
        commit('DELETE_SERVICE', id)
      
    }
  }
}