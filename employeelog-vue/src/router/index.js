import { createRouter, createWebHistory } from 'vue-router'
import Onboarding from '../views/Onboarding.vue'
import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ManagerDashboard from '../views/ManagerDashboard.vue'
import EmployeeDashboard from '../views/EmployeeDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/onboard',
    name: 'Onboarding',
    component: Onboarding
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/manager',
    name: 'ManagerDashboard',
    component: ManagerDashboard,
    meta: { requiresAuth: true, role: 'manager' }
  },
  {
    path: '/employee',
    name: 'EmployeeDashboard',
    component: EmployeeDashboard,
    meta: { requiresAuth: true, role: 'employee' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
    } else if (to.meta.role && to.meta.role !== role) {
      // Redirect unauthorized users to their designated role portal
      if (role === 'admin') next('/admin')
      else if (role === 'manager') next('/manager')
      else if (role === 'employee') next('/employee')
      else next('/login')
    } else {
      next()
    }
  } else {
    // If logged in and going to Login/Onboard, skip to respective dashboard
    if (token && (to.path === '/login' || to.path === '/onboard')) {
      if (role === 'admin') next('/admin')
      else if (role === 'manager') next('/manager')
      else if (role === 'employee') next('/employee')
      else next()
    } else {
      next()
    }
  }
})

export default router
