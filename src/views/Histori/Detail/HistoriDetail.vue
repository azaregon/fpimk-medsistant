<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePointerSwipe, useSpeechSynthesis, onLongPress } from '@vueuse/core'
import { useTemplateRef, watch } from 'vue'
import { ChevronLeft, Pill, Clock, CalendarPlus, Volume2 } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const id = Number(route.query.id)

// Shared history store — same data as list page
// In production this would be from a shared store (Pinia/localStorage)
const historyData = [
  {
    id: 1,
    name: 'Mefinal (Asam Mefenamat)',
    shortDesc: 'Obat Anti-Inflamasi Non-Steroid (OAINS) untuk meredakan nyeri ringan hingga sedang.',
    all_desc: `Berikut adalah deskripsi mengenai obat Mefinal:
Kandungan Aktif: Asam mefenamat (Mefenamic acid).
Golongan: Obat Anti-Inflamasi Non-Steroid (OAINS). Di Indonesia, obat ini termasuk dalam kategori obat keras (berlogo lingkaran merah) sehingga penggunaannya harus menggunakan resep dokter.
Indikasi dan Kegunaan: Berfungsi untuk meredakan nyeri ringan hingga sedang dan mengurangi peradangan. Mefinal umum digunakan untuk mengatasi sakit gigi, sakit kepala, nyeri haid (dismenore), nyeri otot, nyeri sendi, serta nyeri pasca operasi atau cedera.
Cara Kerja: Obat ini bekerja dengan cara menghambat produksi prostaglandin, yaitu zat kimia alami dalam tubuh yang memicu rasa sakit dan reaksi peradangan saat terjadi kerusakan jaringan.
Perhatian Penggunaan: Mefinal sangat disarankan untuk dikonsumsi setelah makan guna mencegah atau meminimalkan efek samping pada saluran pencernaan, seperti iritasi lambung atau mual.
Catatan: Informasi ini hanya untuk tujuan edukasi. Selalu konsultasikan dengan dokter atau apoteker dan ikuti dosis yang diresepkan sebelum mengonsumsi obat ini.`,
    date: '2026-06-20',
    time: '14:32',
    color: '#FCAF33',
  },
  {
    id: 2,
    name: 'Paracetamol 500mg',
    shortDesc: 'Analgesik dan antipiretik untuk meredakan demam dan nyeri kepala.',
    all_desc: `Berikut adalah deskripsi mengenai obat Paracetamol:
Kandungan Aktif: Paracetamol (Acetaminophen) 500mg.
Golongan: Analgesik dan antipiretik bebas. Dapat dibeli tanpa resep dokter.
Indikasi dan Kegunaan: Digunakan untuk meredakan demam, sakit kepala, sakit gigi, nyeri otot ringan, dan nyeri haid.
Cara Kerja: Bekerja dengan menghambat prostaglandin di sistem saraf pusat serta menurunkan suhu tubuh melalui efek pada pusat termoregulasi di hipotalamus.
Perhatian Penggunaan: Jangan melebihi dosis 4 gram per hari. Hindari konsumsi alkohol selama penggunaan. Hati-hati pada pasien dengan gangguan fungsi hati.
Catatan: Informasi ini hanya untuk tujuan edukasi. Selalu ikuti petunjuk dosis pada kemasan atau konsultasikan dengan dokter atau apoteker.`,
    date: '2026-06-18',
    time: '09:15',
    color: '#55C622',
  },
  {
    id: 3,
    name: 'Amoxicillin 500mg',
    shortDesc: 'Antibiotik penisilin untuk infeksi bakteri saluran napas dan saluran kemih.',
    all_desc: `Berikut adalah deskripsi mengenai obat Amoxicillin:
Kandungan Aktif: Amoxicillin trihydrate setara dengan Amoxicillin 500mg.
Golongan: Antibiotik golongan Penisilin. Termasuk obat keras yang harus dengan resep dokter.
Indikasi dan Kegunaan: Digunakan untuk mengatasi infeksi bakteri seperti infeksi saluran pernapasan (radang tenggorokan, bronkitis, pneumonia), infeksi saluran kemih, infeksi kulit, dan infeksi telinga.
Cara Kerja: Menghambat sintesis dinding sel bakteri sehingga bakteri tidak dapat berkembang biak dan mati.
Perhatian Penggunaan: Habiskan antibiotik sesuai resep dokter meskipun sudah merasa sembuh. Beritahu dokter jika memiliki riwayat alergi penisilin.
Catatan: Informasi ini hanya untuk tujuan edukasi. Penggunaan antibiotik tanpa resep dokter sangat tidak dianjurkan karena dapat menyebabkan resistensi antibiotik.`,
    date: '2026-06-15',
    time: '19:47',
    color: '#4978E7',
  },
]

const item = historyData.find((h) => h.id === id)

// Speech synthesis
var { isPlaying, speak, stop } = useSpeechSynthesis(
  item ? `${item.name}. ${item.all_desc}` : 'Data tidak ditemukan',
  { lang: 'id-ID' },
)

// Announce on load
var { speak: announceNav } = useSpeechSynthesis(
  'Detail obat. Geser kanan untuk kembali ke histori. Tekan dan tahan untuk membacakan informasi obat. Geser kiri untuk tambahkan ke jadwal.',
  { lang: 'id-ID', rate: 1.8 },
)
announceNav()

// Swipe gesture — matches Camera/SuccessOverlay pattern
const swipe_elem = useTemplateRef('swipe_elem')
const { direction } = usePointerSwipe(swipe_elem)

watch(direction, (newval) => {
  if (newval === 'right') {
    router.push('/histori')
  } else if (newval === 'left') {
    router.push('/jadwal')
  }
})

onLongPress(
  swipe_elem,
  () => {
    if (!isPlaying.value) {
      speak()
    }
  },
  { delay: 500 },
)

const handleReadAloud = () => {
  if (isPlaying.value) {
    stop()
  } else {
    speak()
  }
}

onUnmounted(() => {
  if (isPlaying.value) stop()
})

const goBack = () => {
  router.push('/histori')
}

const addToSchedule = () => {
  router.push('/jadwal')
}
</script>

<template>
  <!-- Not found state -->
  <div
    v-if="!item"
    class="flex flex-col items-center justify-center h-full gap-4 text-slate-400"
  >
    <Pill class="w-16 h-16 opacity-30" />
    <p class="text-sm" style="font-family: 'DM Sans', sans-serif;">Data tidak ditemukan</p>
    <button
      @click="goBack"
      class="px-5 py-2 rounded-2xl bg-[#FCAF33] text-white text-sm font-bold active:scale-95 transition-transform duration-100"
      style="font-family: 'DM Sans', sans-serif;"
    >
      Kembali
    </button>
  </div>

  <!-- Detail view -->
  <div
    v-else
    ref="swipe_elem"
    class="flex flex-col h-full select-none"
  >
    <!-- Header -->
    <div class="flex items-center gap-3 mb-5 flex-shrink-0">
      <button
        @click="goBack"
        class="p-2 rounded-2xl active:scale-90 transition-transform duration-100 cursor-pointer"
        :style="{ backgroundColor: item.color + '22' }"
        aria-label="Kembali ke histori"
      >
        <ChevronLeft class="w-5 h-5" :style="{ color: item.color }" :stroke-width="2.5" />
      </button>
      <h1
        class="text-xl font-black text-slate-800 flex-1 leading-tight"
        style="font-family: 'Outfit', sans-serif;"
      >
        Detail Obat
      </h1>
    </div>

    <!-- Medicine hero card -->
    <div
      class="flex-shrink-0 rounded-3xl p-5 mb-4 flex items-center gap-4"
      :style="{ backgroundColor: item.color + '18' }"
    >
      <div
        class="w-16 h-16 rounded-2xl flex items-center justify-center flex-shrink-0"
        :style="{ backgroundColor: item.color + '33' }"
      >
        <Pill class="w-8 h-8" :style="{ color: item.color }" :stroke-width="2" />
      </div>
      <div class="flex-1 min-w-0">
        <h2
          class="text-base font-black text-slate-800 leading-snug"
          style="font-family: 'Outfit', sans-serif;"
        >
          {{ item.name }}
        </h2>
        <p
          class="text-xs text-slate-500 mt-1 leading-relaxed"
          style="font-family: 'DM Sans', sans-serif;"
        >
          {{ item.shortDesc }}
        </p>
        <div class="flex items-center gap-1 mt-2">
          <Clock class="w-3 h-3 text-slate-400" />
          <span class="text-[11px] text-slate-400" style="font-family: 'DM Sans', sans-serif;">
            {{ item.date }} · {{ item.time }}
          </span>
        </div>
      </div>
    </div>

    <!-- Description card -->
    <div class="flex-1 bg-white rounded-3xl border border-slate-100 shadow-sm overflow-y-auto mb-4">
      <div class="p-4">
        <p
          class="text-sm text-slate-600 leading-relaxed whitespace-pre-line"
          style="font-family: 'DM Sans', sans-serif;"
        >
          {{ item.all_desc }}
        </p>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex gap-3 flex-shrink-0">
      <!-- Read aloud button -->
      <button
        @click="handleReadAloud"
        class="flex-1 flex items-center justify-center gap-2 py-3 rounded-3xl font-bold text-sm transition-all duration-100 active:scale-95"
        :style="{
          backgroundColor: isPlaying ? '#ef444422' : item.color + '22',
          color: isPlaying ? '#ef4444' : item.color,
        }"
        style="font-family: 'DM Sans', sans-serif;"
      >
        <Volume2 class="w-4 h-4" />
        {{ isPlaying ? 'Hentikan' : 'Bacakan' }}
      </button>

      <!-- Add to schedule button -->
      <button
        @click="addToSchedule"
        class="flex-1 flex items-center justify-center gap-2 py-3 rounded-3xl font-bold text-sm text-white transition-all duration-100 active:scale-95"
        style="background-color: #55C622; font-family: 'DM Sans', sans-serif;"
      >
        <CalendarPlus class="w-4 h-4" />
        Ke Jadwal
      </button>
    </div>

    <!-- Swipe hint -->
    <p
      class="text-center text-[10px] text-slate-400 mt-3 flex-shrink-0"
      style="font-family: 'DM Sans', sans-serif;"
    >
      ← geser kanan untuk kembali · tahan untuk membacakan · geser kiri ke jadwal →
    </p>
  </div>
</template>