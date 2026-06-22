<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const base_url = 'http://127.0.0.1:5000'

// Mock history data as fallback
const mockHistory = [
  {
    id: 1,
    name: 'Imboost',
    image: null,
    bahanAktif: 'Echinacea purpurea, Vitamin C 500mg, Vitamin D3 400IU, Zinc 10mg.',
    manfaat: [
      'Membantu memelihara daya tahan tubuh',
      'Membantu memulihkan kondisi tubuh',
      'Membantu memenuhi kebutuhan Vitamin C & D3',
    ],
    dosis: '1 tablet effervescent, 3 kali sehari, sesudah makan.',
    peringatan: 'Tidak untuk penyakit autoimun, AIDS, tuberkulosis. Hentikan penggunaan segera jika terjadi reaksi alergi. Penggunaan maksimum yang dianjurkan adalah 8 minggu.',
    penyimpanan: 'Simpan di bawah suhu 30°C di tempat yang kering. Lindungi dari sinar matahari langsung.',
  },
  {
    id: 2,
    name: 'Paracetamol',
    image: null,
    bahanAktif: 'Paracetamol (Acetaminophen) 500mg.',
    manfaat: [
      'Meredakan demam',
      'Meredakan sakit kepala',
      'Meredakan nyeri otot ringan',
    ],
    dosis: '1 tablet, 3–4 kali sehari, sesudah makan.',
    peringatan: 'Jangan melebihi dosis 4 gram per hari. Hindari konsumsi alkohol. Hati-hati pada pasien dengan gangguan fungsi hati.',
    penyimpanan: 'Simpan pada suhu kamar, jauhkan dari cahaya langsung dan kelembapan.',
  },
  {
    id: 3,
    name: 'Panadol',
    image: null,
    bahanAktif: 'Paracetamol 500mg.',
    manfaat: [
      'Meredakan nyeri ringan hingga sedang',
      'Menurunkan demam',
      'Meredakan sakit kepala tegang',
    ],
    dosis: '1–2 tablet setiap 4–6 jam. Maksimum 8 tablet per hari.',
    peringatan: 'Tidak boleh dikonsumsi bersama obat lain yang mengandung paracetamol. Konsultasikan dokter jika digunakan lebih dari 10 hari.',
    penyimpanan: 'Simpan di tempat sejuk dan kering, jauh dari jangkauan anak-anak.',
  },
  {
    id: 4,
    name: 'Ambroxol',
    image: null,
    bahanAktif: 'Ambroxol hydrochloride 30mg.',
    manfaat: [
      'Mengencerkan dahak',
      'Memudahkan pengeluaran dahak dari saluran napas',
      'Meredakan batuk berdahak',
    ],
    dosis: '1 tablet, 3 kali sehari, sesudah makan.',
    peringatan: 'Tidak dianjurkan untuk ibu hamil trimester pertama tanpa rekomendasi dokter. Hati-hati pada pasien dengan gangguan ginjal.',
    penyimpanan: 'Simpan pada suhu di bawah 30°C, di tempat yang kering.',
  },
  {
    id: 5,
    name: 'Diapet',
    image: null,
    bahanAktif: 'Ekstrak daun jambu biji, Ekstrak rimpang kunyit, Attapulgit.',
    manfaat: [
      'Mengatasi diare',
      'Meredakan kram perut',
      'Memadatkan feses',
    ],
    dosis: '2 kapsul, 3 kali sehari.',
    peringatan: 'Hentikan penggunaan jika diare disertai darah atau lebih dari 2 hari. Konsultasikan dokter.',
    penyimpanan: 'Simpan di tempat sejuk, kering, dan terhindar dari sinar matahari langsung.',
  },
  {
    id: 6,
    name: 'Metformin',
    image: null,
    bahanAktif: 'Metformin hydrochloride 500mg.',
    manfaat: [
      'Mengontrol kadar gula darah pada diabetes tipe 2',
      'Mengurangi produksi glukosa di hati',
      'Meningkatkan sensitivitas insulin',
    ],
    dosis: '1 tablet, 2–3 kali sehari, sesudah makan.',
    peringatan: 'Harus dengan resep dokter. Hentikan jika terjadi gejala asidosis laktat. Tidak untuk pasien gagal ginjal berat.',
    penyimpanan: 'Simpan pada suhu kamar (15–30°C), jauh dari kelembapan dan panas.',
  },
// End of mockHistory array
]
const historyItems = ref([...mockHistory])

const fetchHistory = async () => {
  const use_backend = localStorage.getItem('use_backend') === 'true'
  if (use_backend) {
    try {
      const response = await fetch(`${base_url}/api/history`)
      const data = await response.json()
      historyItems.value = data
    } catch (e) {
      console.error('Failed to fetch history from backend:', e)
      historyItems.value = [...mockHistory]
    }
  } else {
    historyItems.value = [...mockHistory]
  }
}

onMounted(() => {
  fetchHistory()
  window.addEventListener('use-backend-changed', fetchHistory)
})

onUnmounted(() => {
  window.removeEventListener('use-backend-changed', fetchHistory)
})

const goToDetail = (item) => {
  router.push({ path: `/histori/${item.id}` })
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="flex flex-col w-full h-full">

    <!-- History list -->
    <div class="flex flex-col gap-4 overflow-y-auto flex-1 pb-2 px-1 pt-1">
      <button
        v-for="item in historyItems"
        :key="item.id"
        class="histori-btn flex items-center gap-4 w-full px-5 py-4 rounded-[2rem] active:scale-[0.97] transition-transform duration-100 cursor-pointer"
        @click="goToDetail(item)"
        :aria-label="`Lihat detail ${item.name}`"
      >
        <!-- Clipboard icon -->
        <div class="flex-shrink-0 w-12 h-12 flex items-center justify-center">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- clipboard body -->
            <rect x="7" y="9" width="26" height="30" rx="3" fill="white" fill-opacity="0.25"/>
            <rect x="7" y="9" width="26" height="30" rx="3" stroke="white" stroke-width="2.2"/>
            <!-- clipboard clip -->
            <rect x="15" y="5" width="10" height="7" rx="2" fill="white" fill-opacity="0.25" stroke="white" stroke-width="2"/>
            <!-- lines -->
            <line x1="13" y1="20" x2="27" y2="20" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <line x1="13" y1="26" x2="22" y2="26" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <!-- arrow right on bottom right -->
            <polyline points="24,29 28,32 24,35" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

        <!-- Medicine name -->
        <span class="text-white font-black text-xl tracking-wide" style="font-family: 'Outfit', sans-serif;">
          {{ item.name }}
        </span>
      </button>
    </div>

  </div>
</template>

<style scoped>
.histori-btn {
  background: linear-gradient(135deg, #FCAF33 0%, #F59E0B 100%);
  box-shadow: 0 4px 15px rgba(252, 175, 51, 0.4);
}
.histori-btn:active {
  box-shadow: 0 2px 8px rgba(252, 175, 51, 0.3);
}

/* hide scrollbar */
div::-webkit-scrollbar { display: none; }
div { -ms-overflow-style: none; scrollbar-width: none; }
</style>