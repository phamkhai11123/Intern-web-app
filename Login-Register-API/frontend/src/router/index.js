import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../components/Register.vue')
    },
    {
      path: '/info',
      name: 'info',
      component: () => import('../components/UserInfo.vue')
    },
    {
      path: '/list',
      name: 'list',
      component: () => import('../components/ListUser.vue')
    }
  ]
})

export default router
