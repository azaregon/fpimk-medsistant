<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Pill } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const base_url = 'http://127.0.0.1:5000'

const mockSchedules = [
  { id: 1, name: 'Paracetamol', time: '08:00', dose: '500mg', qty: '1 Tablet' },
  { id: 2, name: 'Amoxicillin', time: '12:00', dose: '250mg', qty: '1 Kapsul' },
  { id: 3, name: 'Sirup Batuk', time: '14:00', dose: '15ml', qty: '1 Sendok Makan' },
  { id: 4, name: 'Vitamin C', time: '18:00', dose: '1000mg', qty: '2 Pil' },
]

const schedules = ref([...mockSchedules])

const fetchSchedules = async () => {
  const use_backend = localStorage.getItem('use_backend') === 'true'
  if (use_backend) {
    try {
      const response = await fetch(`${base_url}/api/schedules`)
      const data = await response.json()
      schedules.value = data
    } catch (e) {
      console.error("Failed to fetch schedules from backend:", e)
      schedules.value = [...mockSchedules]
    }
  } else {
    schedules.value = [...mockSchedules]
  }
}

onMounted(() => {
  fetchSchedules()
  window.addEventListener('use-backend-changed', fetchSchedules)
})

onUnmounted(() => {
  window.removeEventListener('use-backend-changed', fetchSchedules)
})
</script>

<template>
  <div class="flex flex-col w-full h-full font-body pt-2 px-6 gap-5 overflow-y-auto pb-10">
    
    <button v-for="item in schedules" :key="item.id" 
         @click="router.push({ path: `/jadwal/${item.id}`, query: { name: item.name } })"
         class="bg-[#55C622] flex items-center text-left w-full gap-5 p-5 rounded-3xl transition-transform duration-100 active:scale-95 border-none outline-none cursor-pointer">
      
      <Pill class="text-white flex-shrink-0" :size="48" :stroke-width="2.5" />

      <div class="flex flex-col text-white">
        <span class="text-[22px] font-bold tracking-[0.5px] leading-none mb-1.5">
          {{ item.name }}
        </span>
        
        <div class="flex flex-col opacity-90">
          <span class="text-base font-semibold">Jam: {{ item.time }}</span>
          <span class="text-sm">{{ item.dose }} • {{ item.qty }}</span>
        </div>
      </div>

    </button>

  </div>
</template>

<style scoped>
/* Mengkustomisasi scrollbar agar rapi dan tidak terlihat */
div::-webkit-scrollbar {
  display: none;
}
div {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>