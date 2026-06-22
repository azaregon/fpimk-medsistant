<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const id = Number(route.params.id)

// Shared history store
const historyData = [
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
]

const item = historyData.find((h) => h.id === id)

// ─── Per-bubble Speech Synthesis ─────────────────────────────────────────────
// We use the native Web Speech API directly so we can queue utterances
// for the sequential "play all" feature on the image button.

const currentBubble = ref(null) // which bubble key is currently playing
let currentUtterance = null

function stopSpeech() {
  window.speechSynthesis.cancel()
  currentBubble.value = null
  currentUtterance = null
}

function speakText(text, bubbleKey, onEnd) {
  // Cancel any ongoing speech first
  window.speechSynthesis.cancel()
  currentUtterance = null

  // Set the active bubble immediately so the UI responds right away
  currentBubble.value = bubbleKey

  // Use a short delay after cancel() before speak() — this is the standard
  // workaround for the Chrome/mobile Web Speech API bug where the engine
  // gets stuck after the first utterance and ignores subsequent speak() calls.
  setTimeout(() => {
    // Guard: if the user already cancelled while we were waiting, bail out
    if (currentBubble.value !== bubbleKey) return

    const utter = new SpeechSynthesisUtterance(text)
    utter.lang = 'id-ID'
    utter.rate = 1.0
    currentUtterance = utter

    utter.onend = () => {
      if (currentBubble.value === bubbleKey) {
        currentBubble.value = null
        currentUtterance = null
      }
      if (onEnd) onEnd()
    }
    utter.onerror = () => {
      if (currentBubble.value === bubbleKey) {
        currentBubble.value = null
        currentUtterance = null
      }
    }

    window.speechSynthesis.speak(utter)
  }, 150)
}

// Single bubble tap handler
function handleBubbleTap(bubbleKey) {
  if (currentBubble.value === bubbleKey) {
    stopSpeech()
    return
  }
  const textMap = {
    bahanAktif: `Bahan Aktif. ${item.bahanAktif}`,
    manfaat: `Manfaat. ${item.manfaat.join('. ')}`,
    dosis: `Dosis. ${item.dosis}`,
    peringatan: `Peringatan. ${item.peringatan}`,
    penyimpanan: `Penyimpanan dan Penanganan. ${item.penyimpanan}`,
  }
  if (textMap[bubbleKey]) {
    speakText(textMap[bubbleKey], bubbleKey)
  }
}

// Sequential "play all" from the image play button
const isPlayingAll = ref(false)

function playAll() {
  if (isPlayingAll.value) {
    stopSpeech()
    isPlayingAll.value = false
    return
  }

  isPlayingAll.value = true
  const sequence = [
    { key: 'bahanAktif', text: `Bahan Aktif. ${item.bahanAktif}` },
    { key: 'manfaat', text: `Manfaat. ${item.manfaat.join('. ')}` },
    { key: 'dosis', text: `Dosis. ${item.dosis}` },
    { key: 'peringatan', text: `Peringatan. ${item.peringatan}` },
    { key: 'penyimpanan', text: `Penyimpanan dan Penanganan. ${item.penyimpanan}` },
  ]

  let index = 0
  function speakNext() {
    if (!isPlayingAll.value || index >= sequence.length) {
      isPlayingAll.value = false
      currentBubble.value = null
      return
    }
    const { key, text } = sequence[index++]
    speakText(text, key, speakNext)
  }
  speakNext()
}

onUnmounted(() => {
  stopSpeech()
  isPlayingAll.value = false
})

const goBack = () => {
  router.push('/histori')
}
</script>

<template>
  <!-- Not found state -->
  <div
    v-if="!item"
    class="flex flex-col items-center justify-center h-full gap-4 text-slate-400"
  >
    <p class="text-sm" style="font-family: 'DM Sans', sans-serif;">Data tidak ditemukan</p>
    <button
      @click="goBack"
      class="px-5 py-2 rounded-2xl bg-[#FCAF33] text-white text-sm font-bold"
      style="font-family: 'DM Sans', sans-serif;"
    >
      Kembali
    </button>
  </div>

  <!-- Detail view -->
  <div
    v-else
    class="flex flex-col h-full select-none overflow-y-auto pb-6 gap-4"
    style="-ms-overflow-style: none; scrollbar-width: none;"
  >

    <!-- Medicine image with play-all button overlay -->
    <div class="relative w-full rounded-3xl overflow-hidden flex-shrink-0" style="height: 220px;">
      <!-- Placeholder grey background when no image -->
      <div
        class="absolute inset-0 bg-slate-200 flex items-center justify-center"
        :class="{ 'bg-slate-300': !item.image }"
      >
        <svg v-if="!item.image" width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="8" y="16" width="48" height="36" rx="4" stroke="#94a3b8" stroke-width="3" fill="none"/>
          <circle cx="22" cy="28" r="5" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
          <path d="M8 42 L20 30 L30 40 L40 28 L56 44" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
        <img v-else :src="item.image" :alt="item.name" class="w-full h-full object-cover" />
      </div>

      <!-- Dimming overlay -->
      <div class="absolute inset-0 bg-black/25"></div>

      <!-- Play all button (centered) -->
      <button
        @click="playAll"
        class="absolute inset-0 flex items-center justify-center group"
        :aria-label="isPlayingAll ? 'Hentikan audio semua informasi' : 'Putar audio semua informasi'"
      >
        <div
          class="w-20 h-20 rounded-full flex items-center justify-center transition-transform duration-150 active:scale-90"
          :class="isPlayingAll ? 'bg-red-500/80' : 'bg-white/80'"
        >
          <!-- Stop icon when playing -->
          <svg v-if="isPlayingAll" width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="8" y="8" width="16" height="16" rx="2" fill="#ef4444"/>
          </svg>
          <!-- Play triangle when paused -->
          <svg v-else width="36" height="36" viewBox="0 0 36 36" fill="none">
            <polygon points="12,8 30,18 12,28" fill="#1e40af"/>
          </svg>
        </div>
      </button>
    </div>

    <!-- Medicine name card -->
    <div class="bg-white rounded-3xl px-5 py-4 flex-shrink-0 shadow-sm border border-slate-100">
      <p class="text-xl font-black text-slate-800" style="font-family: 'Outfit', sans-serif;">
        {{ item.name }}
      </p>
    </div>

    <!-- BAHAN AKTIF bubble -->
    <button
      class="info-bubble text-left w-full"
      :class="{ 'bubble-active': currentBubble === 'bahanAktif' }"
      @click="handleBubbleTap('bahanAktif')"
      aria-label="Bahan Aktif - ketuk untuk memutar audio"
    >
      <div class="flex items-center gap-2 mb-2">
        <!-- Flask icon -->
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 3h6M9 3v6L5 16a2 2 0 001.8 3h8.4A2 2 0 0017 16l-4-7V3" stroke="#4978E7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="9" cy="15" r="1" fill="#4978E7"/>
          <circle cx="13" cy="17" r="0.8" fill="#4978E7"/>
        </svg>
        <span class="text-xs font-black text-slate-700 tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.1em;">
          Bahan Aktif
        </span>
        <!-- Audio wave indicator when playing -->
        <span v-if="currentBubble === 'bahanAktif'" class="ml-auto audio-wave">
          <span></span><span></span><span></span>
        </span>
      </div>
      <p class="text-sm text-slate-600 leading-relaxed" style="font-family: 'DM Sans', sans-serif;">
        {{ item.bahanAktif }}
      </p>
    </button>

    <!-- MANFAAT bubble -->
    <button
      class="info-bubble text-left w-full"
      :class="{ 'bubble-active': currentBubble === 'manfaat' }"
      @click="handleBubbleTap('manfaat')"
      aria-label="Manfaat - ketuk untuk memutar audio"
    >
      <div class="flex items-center gap-2 mb-3">
        <span class="text-xs font-black text-slate-700 tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.1em;">
          Manfaat
        </span>
        <span v-if="currentBubble === 'manfaat'" class="ml-auto audio-wave">
          <span></span><span></span><span></span>
        </span>
      </div>
      <ul class="flex flex-col gap-2">
        <li
          v-for="(m, idx) in item.manfaat"
          :key="idx"
          class="flex items-start gap-2"
        >
          <!-- Green checkmark -->
          <svg class="flex-shrink-0 mt-0.5" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8.5L6.5 12L13 5" stroke="#22c55e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="text-sm text-slate-600 leading-snug" style="font-family: 'DM Sans', sans-serif;">{{ m }}</span>
        </li>
      </ul>
    </button>

    <!-- DOSIS bubble -->
    <button
      class="info-bubble text-left w-full"
      :class="{ 'bubble-active': currentBubble === 'dosis' }"
      @click="handleBubbleTap('dosis')"
      aria-label="Dosis - ketuk untuk memutar audio"
    >
      <div class="flex items-center gap-2 mb-2">
        <!-- Clock icon -->
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="11" cy="11" r="8" stroke="#4978E7" stroke-width="1.8"/>
          <path d="M11 7v4l3 2" stroke="#4978E7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="text-xs font-black text-slate-700 tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.1em;">
          Dosis
        </span>
        <span v-if="currentBubble === 'dosis'" class="ml-auto audio-wave">
          <span></span><span></span><span></span>
        </span>
      </div>
      <p class="text-sm font-black text-slate-800 leading-relaxed" style="font-family: 'Outfit', sans-serif;">
        {{ item.dosis }}
      </p>
    </button>

    <!-- PERINGATAN bubble -->
    <button
      class="info-bubble text-left w-full"
      :class="{ 'bubble-active': currentBubble === 'peringatan' }"
      @click="handleBubbleTap('peringatan')"
      aria-label="Peringatan - ketuk untuk memutar audio"
    >
      <div class="flex items-center gap-2 mb-2">
        <!-- Warning triangle icon -->
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11 3L20 19H2L11 3z" stroke="#ef4444" stroke-width="1.8" stroke-linejoin="round"/>
          <line x1="11" y1="10" x2="11" y2="14" stroke="#ef4444" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="11" cy="16.5" r="0.8" fill="#ef4444"/>
        </svg>
        <span class="text-xs font-black text-red-500 tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.1em;">
          Peringatan
        </span>
        <span v-if="currentBubble === 'peringatan'" class="ml-auto audio-wave warning">
          <span></span><span></span><span></span>
        </span>
      </div>
      <p class="text-sm text-red-500 leading-relaxed" style="font-family: 'DM Sans', sans-serif;">
        {{ item.peringatan }}
      </p>
    </button>

    <!-- PENYIMPANAN & PENANGANAN bubble -->
    <button
      class="info-bubble text-left w-full"
      :class="{ 'bubble-active': currentBubble === 'penyimpanan' }"
      @click="handleBubbleTap('penyimpanan')"
      aria-label="Penyimpanan dan Penanganan - ketuk untuk memutar audio"
    >
      <div class="flex items-center gap-2 mb-2">
        <!-- Box icon -->
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 8H2l1.5 11h15L20 8z" stroke="#4978E7" stroke-width="1.8" stroke-linejoin="round"/>
          <path d="M2 8l2-5h14l2 5" stroke="#4978E7" stroke-width="1.8" stroke-linejoin="round"/>
          <line x1="8" y1="8" x2="8" y2="14" stroke="#4978E7" stroke-width="1.8" stroke-linecap="round"/>
          <line x1="14" y1="8" x2="14" y2="14" stroke="#4978E7" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
        <span class="text-xs font-black text-slate-700 tracking-widest uppercase" style="font-family: 'Outfit', sans-serif; letter-spacing: 0.1em;">
          Penyimpanan &amp; Penanganan
        </span>
        <span v-if="currentBubble === 'penyimpanan'" class="ml-auto audio-wave">
          <span></span><span></span><span></span>
        </span>
      </div>
      <p class="text-sm text-slate-600 leading-relaxed" style="font-family: 'DM Sans', sans-serif;">
        {{ item.penyimpanan }}
      </p>
    </button>

  </div>
</template>

<style scoped>
/* Hide scrollbar */
div::-webkit-scrollbar { display: none; }

/* Info bubble card */
.info-bubble {
  background: white;
  border-radius: 1.5rem;
  padding: 1.1rem 1.25rem;
  border: 2px solid transparent;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
  flex-shrink: 0;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.1s;
}

.info-bubble:active {
  transform: scale(0.98);
}

.bubble-active {
  border-color: #4978E7;
  box-shadow: 0 2px 16px rgba(73, 120, 231, 0.18);
}

/* Audio wave animation */
.audio-wave {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 16px;
}
.audio-wave span {
  display: block;
  width: 3px;
  border-radius: 2px;
  background: #4978E7;
  animation: wave 0.8s ease-in-out infinite;
}
.audio-wave span:nth-child(1) { height: 6px; animation-delay: 0s; }
.audio-wave span:nth-child(2) { height: 12px; animation-delay: 0.15s; }
.audio-wave span:nth-child(3) { height: 8px; animation-delay: 0.3s; }

.audio-wave.warning span {
  background: #ef4444;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}
</style>