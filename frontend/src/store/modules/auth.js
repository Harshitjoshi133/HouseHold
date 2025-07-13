import api from '../../services/api'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    userRole: state => (state.user ? state.user.role : null)
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.token = null
      state.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login', credentials);
        
        commit('SET_TOKEN', response.data.token);
        commit('SET_USER', response.data.user);
        console.log("User Logged In! Token & User set in Vuex.");
        
        return response.data.user.role; // ✅ Return role so login component can use it
      } catch (error) {
        console.error("Login failed:", error);
        throw error;
      }
    },    

    async register(_, userData) {
      return api.post('/auth/register', userData)
    },

    logout({ commit }) {
      commit('LOGOUT')
    }
  }
}
