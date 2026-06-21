<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ClipboardList, Search, ChevronLeft, Pill, Trash2, Clock } from 'lucide-vue-next'
import { useSpeechSynthesis } from '@vueuse/core'

const router = useRouter()

// Sample history data — in a real app this would come from localStorage / backend
const historyItems = ref([
  {
    id: 1,
    name: 'Mefinal (Asam Mefenamat)',
    shortDesc: 'Obat Anti-Inflamasi Non-Steroid (OAINS) untuk meredakan nyeri ringan hingga sedang.',
    all_desc: `Berikut adalah deskripsi mengenai obat Mefinal:\nKandungan Aktif: Asam mefenamat (Mefenamic acid).\nGolongan: Obat Anti-Inflamasi Non-Steroid (OAINS). Di Indonesia, obat ini termasuk dalam kategori obat keras (berlogo lingkaran merah) sehingga penggunaannya harus menggunakan resep dokter.\nIndikasi dan Kegunaan: Berfungsi untuk meredakan nyeri ringan hingga sedang dan mengurangi peradangan. Mefinal umum digunakan untuk mengatasi sakit gigi, sakit kepala, nyeri haid (dismenore), nyeri otot, nyeri sendi, serta nyeri pasca operasi atau cedera.\nCara Kerja: Obat ini bekerja dengan cara menghambat produksi prostaglandin, yaitu zat kimia alami dalam tubuh yang memicu rasa sakit dan reaksi peradangan saat terjadi kerusakan jaringan.\nPerhatian Penggunaan: Mefinal sangat disarankan untuk dikonsumsi setelah makan guna mencegah atau meminimalkan efek samping pada saluran pencernaan, seperti iritasi lambung atau mual.\nCatatan: Informasi ini hanya untuk tujuan edukasi. Selalu konsultasikan dengan dokter atau apoteker dan ikuti dosis yang diresepkan sebelum mengonsumsi obat ini.`,
    date: '2026-06-20',
    time: '14:32',
    color: '#FCAF33',
  },
  {
    id: 2,
    name: 'Paracetamol 500mg',
    shortDesc: 'Analgesik dan antipiretik untuk meredakan demam dan nyeri kepala.',
    all_desc: `Berikut adalah deskripsi mengenai obat Paracetamol:\nKandungan Aktif: Paracetamol (Acetaminophen) 500mg.\nGolongan: Analgesik dan antipiretik bebas. Dapat dibeli tanpa resep dokter.\nIndikasi dan Kegunaan: Digunakan untuk meredakan demam, sakit kepala, sakit gigi, nyeri otot ringan, dan nyeri haid.\nCara Kerja: Bekerja dengan menghambat prostaglandin di sistem saraf pusat serta menurunkan suhu tubuh melalui efek pada pusat termoregulasi di hipotalamus.\nPerhatian Penggunaan: Jangan melebihi dosis 4 gram per hari. Hindari konsumsi alkohol selama penggunaan. Hati-hati pada pasien dengan gangguan fungsi hati.\nCatatan: Informasi ini hanya untuk tujuan edukasi. Selalu ikuti petunjuk dosis pada kemasan atau konsultasikan dengan dokter atau apoteker.`,
    date: '2026-06-18',
    time: '09:15',
    color: '#55C622',
  },
  {
    id: 3,
    name: 'Amoxicillin 500mg',
    shortDesc: 'Antibiotik penisilin untuk infeksi bakteri saluran napas dan saluran kemih.',
    all_desc: `Berikut adalah deskripsi mengenai obat Amoxicillin:\nKandungan Aktif: Amoxicillin trihydrate setara dengan Amoxicillin 500mg.\nGolongan: Antibiotik golongan Penisilin. Termasuk obat keras yang harus dengan resep dokter.\nIndikasi dan Kegunaan: Digunakan untuk mengatasi infeksi bakteri seperti infeksi saluran pernapasan (radang tenggorokan, bronkitis, pneumonia), infeksi saluran kemih, infeksi kulit, dan infeksi telinga.\nCara Kerja: Menghambat sintesis dinding sel bakteri sehingga bakteri tidak dapat berkembang biak dan mati.\nPerhatian Penggunaan: Habiskan antibiotik sesuai resep dokter meskipun sudah merasa sembuh. Beritahu dokter jika memiliki riwayat alergi penisilin.\nCatatan: Informasi ini hanya untuk tujuan edukasi. Penggunaan antibiotik tanpa resep dokter sangat tidak dianjurkan karena dapat menyebabkan resistensi antibiotik.`,
    date: '2026-06-15',
    time: '19:47',
    color: '#4978E7',
  },
])

const searchQuery = ref('')

const filteredItems = computed(() => {
  if (!searchQuery.value.trim()) return historyItems.value
  const q = searchQuery.value.toLowerCase()
  return historyItems.value.filter(
    (item) =>
      item.name.toLowerCase().includes(q) ||
      item.shortDesc.toLowerCase().includes(q),
  )
})

const deleteItem = (id) => {
  historyItems.value = historyItems.value.filter((item) => item.id !== id)
}

const goToDetail = (item) => {
  router.push({ path: '/histori/item', query: { id: item.id } })
}

const goBack = () => {
  router.push('/')
}

// Announce page on load
const { speak } = useSpeechSynthesis('Halaman Histori. Menampilkan daftar riwayat pemindaian obat.', {
  lang: 'id-ID',
  rate: 1.8,
})
speak()
</script>

<template>
  <div class="flex flex-col w-full h-full">

    <!-- Header -->
    <div class="flex items-center gap-3 mb-5">
      <button
        @click="goBack"
        class="p-2 rounded-2xl bg-[#FCAF33]/15 active:scale-90 transition-transform duration-100 cursor-pointer"
        aria-label="Kembali ke menu utama"
      >
        <ChevronLeft class="w-5 h-5 text-[#FCAF33]" :stroke-width="2.5" />
      </button>
      <div class="flex items-center gap-2 flex-1">
        <ClipboardList class="w-6 h-6 text-[#FCAF33]" :stroke-width="2.5" />
        <h1 class="text-xl font-black text-slate-800" style="font-family: 'Outfit', sans-serif;">
          Histori
        </h1>
      </div>
    </div>

    <!-- Search bar -->
    <div class="relative mb-4">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari riwayat obat..."
        class="w-full pl-9 pr-4 py-2.5 rounded-2xl bg-white border border-slate-200 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-[#FCAF33] focus:ring-2 focus:ring-[#FCAF33]/20 transition-all duration-200"
        style="font-family: 'DM Sans', sans-serif;"
      />
    </div>

    <!-- Empty state -->
    <div
      v-if="filteredItems.length === 0"
      class="flex-1 flex flex-col items-center justify-center gap-3 text-slate-400 select-none"
    >
      <ClipboardList class="w-16 h-16 opacity-30" />
      <p class="text-sm font-medium" style="font-family: 'DM Sans', sans-serif;">
        {{ searchQuery ? 'Tidak ada hasil ditemukan' : 'Belum ada histori pemindaian' }}
      </p>
    </div>

    <!-- History list -->
    <div v-else class="flex flex-col gap-3 overflow-y-auto flex-1 pb-2">
      <div
        v-for="item in filteredItems"
        :key="item.id"
        class="group relative bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden active:scale-[0.98] transition-transform duration-100 cursor-pointer"
        @click="goToDetail(item)"
      >
        <!-- Colored left accent bar -->
        <div
          class="absolute left-0 top-0 bottom-0 w-1.5 rounded-l-3xl"
          :style="{ backgroundColor: item.color }"
        />

        <div class="flex items-start gap-3 pl-4 pr-3 py-3.5">
          <!-- Icon -->
          <div
            class="flex-shrink-0 w-11 h-11 rounded-2xl flex items-center justify-center mt-0.5"
            :style="{ backgroundColor: item.color + '22' }"
          >
            <Pill class="w-5 h-5" :style="{ color: item.color }" :stroke-width="2" />
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <p
              class="text-sm font-bold text-slate-800 leading-snug truncate"
              style="font-family: 'Outfit', sans-serif;"
            >
              {{ item.name }}
            </p>
            <p
              class="text-xs text-slate-500 mt-0.5 line-clamp-2 leading-relaxed"
              style="font-family: 'DM Sans', sans-serif;"
            >
              {{ item.shortDesc }}
            </p>
            <div class="flex items-center gap-1 mt-1.5">
              <Clock class="w-3 h-3 text-slate-400" />
              <span class="text-[11px] text-slate-400" style="font-family: 'DM Sans', sans-serif;">
                {{ item.date }} · {{ item.time }}
              </span>
            </div>
          </div>

          <!-- Delete button -->
          <button
            class="flex-shrink-0 p-1.5 rounded-xl text-slate-300 hover:text-red-400 hover:bg-red-50 active:scale-90 transition-all duration-150"
            @click.stop="deleteItem(item.id)"
            aria-label="Hapus histori"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- Count badge -->
    <div
      v-if="historyItems.length > 0"
      class="mt-3 text-center"
    >
      <span
        class="text-xs text-slate-400"
        style="font-family: 'DM Sans', sans-serif;"
      >
        {{ filteredItems.length }} dari {{ historyItems.length }} riwayat
      </span>
    </div>

  </div>
</template>