import { createRouter, createWebHistory } from 'vue-router'

import MainMenu from '../views/MainMenu/MainMenu.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main-menu',
      component: MainMenu,
    },
    {
      path: '/histori',
      name: 'histori',
      component: () => import('../views/Histori/List/HIstoriList.vue'),
    },
    {
      path: '/histori/item',
      name: 'histori-item',
      component: () => import('../views/Histori/Detail/HistoriDetail.vue'),
    },
    {
      path: '/jadwal',
      name: 'jadwal',
      component: () => import('../views/Jadwal/List/JadwalList.vue'),
    },
    {
      path: '/jadwal/item',
      name: 'jadwal-item',
      // component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/camera',
      name: 'camera',
      component: () => import('../views/Camera/Camera.vue'),
    },
  ],
})

export default router
