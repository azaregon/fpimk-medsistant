<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { ArrowLeft } from 'lucide-vue-next' // Import icon panah

const route = useRoute()
const router = useRouter()

// Shared history names for title lookup
const historyNames = {
  1: 'Imboost',
  2: 'Paracetamol',
  3: 'Panadol',
  4: 'Ambroxol',
  5: 'Diapet',
  6: 'Metformin',
}

// Cek apakah saat ini sedang di halaman utama (Home)
const isHome = computed(() => route.path === '/')

// Ubah judul otomatis berdasarkan halaman saat ini
const pageTitle = computed(() => {
  // Detail histori — show medicine name
  if (route.path.startsWith('/histori/') && route.params.id) {
    const id = Number(route.params.id)
    return historyNames[id] || 'Detail Obat'
  }

  // Jika URL adalah detail jadwal (mengandung ID)
  if (route.path.startsWith('/jadwal/') && route.path !== '/jadwal') {
    return route.query.name || 'Detail Obat'
  }

  if (route.path === '/jadwal') return 'Jadwal Obat'
  if (route.path === '/histori') return 'Histori'
  if (route.path.includes('/camera')) return 'Kamera'

  return 'MedSistant' // Default untuk home
})
</script>

<template>
  <div class="w-full h-screen flex items-center justify-center p-4">
    <div class="flex flex-col-reverse rounded-xl w-md h-full bg-linear-to-br from-blue-500 to-blue-700 overflow-clip">
      
      <!-- Area Putih (RouterView) -->
      <div class="rounded-t-[5rem] bg-white h-[90%] px-6 pt-10 pb-10 overflow-clip">
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