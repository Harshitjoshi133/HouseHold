import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    requests: [],
    loading: false
  },
  getters: {
    allRequests: state => state.requests,
    requestById: state => id => state.requests.find(request => request.id === id),
    requestsByStatus: state => status => state.requests.filter(request => request.service_status === status),
    customerRequests: (state, getters, rootState) => {
      const userId = rootState.auth.user ? rootState.auth.user.id : null
      return state.requests.filter(request => request.customer_id === userId)
    },
    professionalRequests: (state, getters, rootState) => {
      const userId = rootState.auth.user ? rootState.auth.user.id : null
      return state.requests.filter(request => request.professional_id === userId)
    }
  },
  mutations: {
    SET_REQUESTS(state, requests) {
      state.requests = requests
    },
    ADD_REQUEST(state, request) {
      state.requests.push(request)
    },
    UPDATE_REQUEST(state, updatedRequest) {
      const index = state.requests.findIndex(r => r.id === updatedRequest.id)
      if (index !== -1) {
        state.requests.splice(index, 1, updatedRequest)
      }
    },
    SET_LOADING(state, status) {
      state.loading = status
    }
  },
  actions: {
    async fetchRequests({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/service-requests')
        commit('SET_REQUESTS', response.data)
      } catch (error) {
        console.error('Error fetching service requests:', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createRequest({ commit }, requestData) {
      
        const response = await api.post('/service-requests', requestData)
        commit('ADD_REQUEST', response.data)
        return response
    },
    async updateRequest({ commit }, { id, data }) {
      
        const response = await api.put(`/service-requests/${id}`, data)
        commit('UPDATE_REQUEST', response.data)
        return response

    },
    async changeRequestStatus({ commit }, { id, status }) {
      
        const response = await api.patch(`/service-requests/${id}/status`, { status })
        commit('UPDATE_REQUEST', response.data)
        return response
      
    }
  }
}