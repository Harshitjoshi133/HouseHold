import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminView from '../views/AdminView.vue'
import CustomerView from '../views/CustomerView.vue'
import ProfessionalView from '../views/ProfessionalView.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/customer',
    name: 'Customer',
    component: CustomerView,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/professional',
    name: 'Professional',
    component: ProfessionalView,
    meta: { requiresAuth: true, role: 'professional' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards to check authentication and role
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated']
  const userRole = store.getters['auth/userRole']
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login')
    } else if (to.meta.role && to.meta.role !== userRole) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router;