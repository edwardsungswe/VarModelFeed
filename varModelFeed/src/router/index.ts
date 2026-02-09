import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: () => import('../views/SignInView.vue'),
    },
    {
      path: '/post-idea',
      name: 'post-idea',
      component: () => import('../views/PostIdeaView.vue'),
    },
    {
      path: '/partnership/:id',
      name: 'partnership-detail',
      component: () => import('../views/PartnershipDetailView.vue'),
    },
  ],
})

export default router
