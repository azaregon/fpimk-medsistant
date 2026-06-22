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
      component: () => import('../views/Histori/List/HIstoriList.vue'), // Perhatikan huruf besar 'I' pada HIstoriList, pastikan sesuai dengan nama file Anda
    },
    {
      // Menggunakan parameter :id untuk histori spesifik
      path: '/histori/:id',
      name: 'histori-item',
      component: () => import('../views/Histori/Detail/HistoriDetail.vue'),
    },
    {
      path: '/jadwal',
      name: 'jadwal',
      component: () => import('../views/Jadwal/List/JadwalList.vue'),
    },
    {
      // Menggunakan parameter :id dan menghubungkan ke komponen JadwalDetail.vue
      path: '/jadwal/:id',
      name: 'jadwal-item',
      component: () => import('../views/Jadwal/Detail/JadwalDetail.vue'),
    },
    {
      path: '/camera',
      name: 'camera',
      component: () => import('../views/Camera/Camera.vue'),
    },
  ],
})

export default router