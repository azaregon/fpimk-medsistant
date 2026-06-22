<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { ArrowLeft } from 'lucide-vue-next' // Import icon panah

const route = useRoute()
const router = useRouter()

// Cek apakah saat ini sedang di halaman utama (Home)
// Catatan: Sesuaikan '/' jika route home Anda berbeda namanya
const isHome = computed(() => route.path === '/')

// Ubah judul otomatis berdasarkan halaman saat ini
const pageTitle = computed(() => {
  // Jika URL adalah detail jadwal (mengandung ID)
  if (route.path.startsWith('/jadwal/') && route.path !== '/jadwal') {
    return route.query.name || 'Detail Obat' // Ambil nama dari URL query
  }
  
  if (route.path === '/jadwal') return 'Jadwal Obat'
  if (route.path.includes('/histori')) return 'Histori'
  if (route.path.includes('/camera')) return 'Kamera'
  
  return 'MedSistant' // Default untuk home
})
</script>

<template>
  <div class="w-full h-screen flex items-center justify-center p-4">
    <div class="flex flex-col-reverse rounded-xl w-md h-full bg-linear-to-br from-blue-500 to-blue-700 overflow-clip">
      
      <!-- Area Putih (RouterView) -->
      <div class="rounded-t-[5rem] bg-slate-100 h-[90%] px-6 pt-10 pb-10 overflow-clip">
        <RouterView class=" overflow-clip h-full"/>
      </div>

      <!-- Area Biru (Header Dinamis) -->
      <div class="flex justify-center items-center flex-1 relative px-6 w-full">
        
        <!-- Tombol Back: Hanya muncul jika BUKAN di halaman Home -->
        <button v-if="!isHome" @click="router.back()" 
                class="absolute left-6 text-white w-10 h-10 rounded-full border-2 border-white flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer">
          <ArrowLeft class="w-6 h-6" :stroke-width="2.5" />
        </button>

        <!-- Judul Dinamis -->
        <span class="text-3xl font-black font-heading text-white">
          {{ pageTitle }}
        </span>
        
      </div>
    </div>
  </div>
</template>