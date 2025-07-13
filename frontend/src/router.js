import Vue from 'vue';
import VueRouter from 'vue-router';


// Import Views
import HomeView from './views/HomeView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import AdminView from './views/AdminView.vue';
import CustomerView from './views/CustomerView.vue';
import ProfessionalView from './views/ProfessionalView.vue';

// Import Admin Components
import DashboardAdmin from './components/admin/DashboardAdmin.vue';
import ServiceManagement from './components/admin/ServiceManagement.vue';
import UserManagement from './components/admin/UserManagement.vue';
import ExportData from './components/admin/ExportData.vue';

// Import Customer Components
import CustomerDashboard from './components/cutomer/CustomerDashboard.vue';
import ServiceSearch from './components/cutomer/ServiceSearch.vue';
import ServiceRequestForm from './components/cutomer/ServiceRequestForm.vue';
import MyServices from './components/cutomer/MyServices.vue';

// Import Professional Components
import ProfessionalDashboard from './components/professional/ProfessionalDashboard.vue';
import ServiceRequestList from './components/professional/ServiceRequestList.vue';

// Use Vue Router
Vue.use(VueRouter);


const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  {
    path: '/admin',
    component: AdminView,
    children: [
      { path: 'dashboard', name: 'DashboardAdmin', component: DashboardAdmin },
      { path: 'services', name: 'ServiceManagement', component: ServiceManagement },
      { path: 'users', name: 'UserManagement', component: UserManagement },
      { path: 'export', name: 'ExportData', component: ExportData },
      { path: '', redirect: '/admin/dashboard' }
    ]
  },
  {
    path: '/customer',
    component: CustomerView,
    children: [
      { path: 'dashboard', name: 'CustomerDashboard', component: CustomerDashboard },
      { path: 'search', name: 'ServiceSearch', component: ServiceSearch },
      { path: 'request/:id', name: 'ServiceRequest', component: ServiceRequestForm },
      { path: 'services', name: 'MyServices', component:MyServices },
      { path: '', redirect: '/customer/dashboard' }
    ]
  },
  {
    path: '/professional',
    component: ProfessionalView,
    children: [
      { path: 'dashboard', name: 'ProfessionalDashboard', component: ProfessionalDashboard },
      { path: 'requests', name: 'ServiceRequests', component: ServiceRequestList },
      { path: '', redirect: '/professional/dashboard' }
    ]
  },
  { path: '*', redirect: '/' } // Catch-all redirect
];


const router = new VueRouter({
  mode: 'history', 
  routes,
  linkActiveClass: 'active'
});

export default router;
