<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Bell, Clock, Sun, Cloud } from 'lucide-vue-next'

const route = useRoute()

// Mengambil nama obat dari URL query (dari halaman list)
const medicineName = route.query.name || 'Mefinal'

// Data tiruan (mockup) untuk detail obat
const medicine = ref({
  image: 'https://placehold.co/600x400/pink/white?text=Gambar+Obat', // Ganti dengan path/URL gambar asli Anda
  nextDose: {
    countdown: '04:05:33',
    time: '13:00',
    period: 'Siang',
    instruction: 'Sesudah Makan'
  },
  schedules: [
    { id: 1, time: '08:00 AM', period: 'Pagi', instruction: 'Sesudah Makan', icon: 'sun', isActive: true },
    { id: 2, time: '01:00 PM', period: 'Siang', instruction: 'Sesudah Makan', icon: 'cloud', isActive: true }
  ]
})
</script>

<template>
  <div class="flex flex-col w-full h-full font-body pt-2 space-y-5 overflow-y-auto pb-10">

    <!-- Foto Obat -->
    <div class="w-full h-48 rounded-2xl overflow-hidden shadow-sm border border-gray-200 shrink-0">
      <img :src="medicine.image" alt="Foto Obat" class="w-full h-full object-cover" />
    </div>

    <!-- Card: Minum Berikutnya -->
    <div class="bg-[#F5F7FF] border-l-[5px] border-[#3b82f6] rounded-2xl p-4 shadow-sm relative shrink-0">
      <div class="flex justify-between items-start mb-1">
        <div>
          <p class="text-gray-700 text-xs font-semibold mb-0.5">Minum Berikutnya</p>
          <p class="text-[#3b82f6] font-bold text-base leading-tight">{{ medicineName }}</p>
        </div>
        <Bell class="text-[#3b82f6] w-5 h-5" />
      </div>

      <div class="flex items-center gap-2 mt-4 mb-2">
        <Clock class="text-[#3b82f6] w-[22px] h-[22px]" />
        <span class="text-2xl font-black text-black tracking-wide">{{ medicine.nextDose.countdown }}</span>
      </div>

      <p class="text-gray-700 text-sm font-medium">
        Pukul {{ medicine.nextDose.time }} {{ medicine.nextDose.period }} - {{ medicine.nextDose.instruction }}
      </p>
    </div>

    <!-- Section: Jadwal Harian -->
    <div class="flex flex-col gap-3 shrink-0 pt-2">
      <div class="flex justify-between items-center px-1">
        <h3 class="font-bold text-black text-[17px]">Jadwal Harian</h3>
        <button class="text-[#3b82f6] text-sm font-bold hover:opacity-80">Ubah Semua</button>
      </div>

      <!-- List Waktu Minum -->
      <div v-for="sched in medicine.schedules" :key="sched.id"
           class="bg-[#F5F7FF] border border-blue-100/50 rounded-2xl p-4 flex items-center justify-between shadow-sm">

        <div class="flex items-center gap-4">
          <!-- Ikon Waktu (Pagi/Siang) -->
          <div class="bg-[#3b82f6] p-2.5 rounded-full text-white shadow-sm">
            <Sun v-if="sched.icon === 'sun'" class="w-6 h-6" :stroke-width="2.5" />
            <Cloud v-else-if="sched.icon === 'cloud'" class="w-6 h-6" :stroke-width="2.5" />
          </div>

          <!-- Keterangan Waktu -->
          <div class="flex flex-col">
            <span class="font-bold text-black text-[15px] mb-0.5">{{ sched.time }}</span>
            <span class="text-xs text-gray-600 font-medium">{{ sched.period }} - {{ sched.instruction }}</span>
          </div>
        </div>

        <!-- Tombol Toggle (On/Off) -->
        <button @click="sched.isActive = !sched.isActive"
                :class="sched.isActive ? 'bg-[#3b82f6]' : 'bg-gray-300'"
                class="w-12 h-[26px] rounded-full flex items-center px-1 transition-colors duration-300 ease-in-out cursor-pointer">
          <div :class="sched.isActive ? 'translate-x-5' : 'translate-x-0'"
               class="bg-white w-5 h-5 rounded-full shadow-sm transform transition-transform duration-300 ease-in-out"></div>
        </button>

      </div>
    </div>

  </div>
</template>

<style scoped>
/* Sembunyikan scrollbar agar rapi tapi tetap bisa di-scroll */
div::-webkit-scrollbar {
  display: none;
}
div {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>