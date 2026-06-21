<script setup>
import { useRouter } from 'vue-router'
import { usePointerSwipe, 
    useEventListener, 
    useSpeechSynthesis,
    onLongPress
} from '@vueuse/core'
import { Camera } from '@lucide/vue';
import { useTemplateRef, watch, onUnmounted } from 'vue'

const router = useRouter()

const props = defineProps({
  toread: {
    type: String,
    required: true
  }
})


var { isSupported, isSpeaking, speak, stop } = useSpeechSynthesis("berhasil membaca obat. geser kanan untuk kembali, tekan dan tahan setengah detik untuk membacakan hasil, geser kiri untuk menambahkan ke jadwal", {lang: 'id-ID', rate: 2})
speak()

const toread = props.toread

// const toread = `Berikut adalah deskripsi mengenai obat Mefinal:
// Kandungan Aktif: Asam mefenamat (Mefenamic acid).
// Golongan: Obat Anti-Inflamasi Non-Steroid (OAINS). Di Indonesia, obat ini termasuk dalam kategori obat keras (berlogo lingkaran merah) sehingga penggunaannya harus menggunakan resep dokter.
// Indikasi dan Kegunaan: Berfungsi untuk meredakan nyeri ringan hingga sedang dan mengurangi peradangan. Mefinal umum digunakan untuk mengatasi sakit gigi, sakit kepala, nyeri haid (dismenore), nyeri otot, nyeri sendi, serta nyeri pasca operasi atau cedera.
// Cara Kerja: Obat ini bekerja dengan cara menghambat produksi prostaglandin, yaitu zat kimia alami dalam tubuh yang memicu rasa sakit dan reaksi peradangan saat terjadi kerusakan jaringan.
// Perhatian Penggunaan: Mefinal sangat disarankan untuk dikonsumsi setelah makan guna mencegah atau meminimalkan efek samping pada saluran pencernaan, seperti iritasi lambung atau mual.
// Catatan: Informasi ini hanya untuk tujuan edukasi. Selalu konsultasikan dengan dokter atau apoteker dan ikuti dosis yang diresepkan sebelum mengonsumsi obat ini.`

var { isSupported, isPlaying, speak, stop } = useSpeechSynthesis(toread, { lang: 'id-ID' })

const swipe_elem = useTemplateRef('swipe_elem')
const { isSwiping, direction } = usePointerSwipe(swipe_elem)

watch(direction, (newval, oldval) => {
    if (newval == "right") {
        console.log("right")
        router.push("/")
    } else if (newval == "left") {
        console.log("left")
        router.push("/jadwal")
    }
})

onLongPress(swipe_elem,() => {
    if (!isPlaying.value) {
        speak()
    }
}, {
    delay: 1000
})

onUnmounted(() => {
    stop()
  if (isPlaying.value) {
        
    }
});

</script>

<style scoped>
  .font-body-text {
    font-family: 'DM Sans', sans-serif;
  }
</style>


<template>
    <div class=" absolute left-0 top-0 w-full h-screen flex items-center justify-center p-4 select-none " ref="swipe_elem">
        <div class="flex items-center justify-center rounded-xl w-md h-full bg-linear-to-br overflow-clip bg-black/60 ">
            <div class="flex flex-col justify-between items-center p-6 bg-slate-50 h-100 w-[calc(100%-2rem)] rounded-lg ">
                
                <div>
                    <Camera class="w-23 h-23 text-green-500"/>
                </div>
                
                <span class="text-2xl font-body text-black font-bold">gambar Sukses Terbaca</span>
                
                <div>
                    <p class="text-lg text-black">
                        <b>Sukses mendeteksi obat</b> <br>
                        - geser kanan untuk kembali <br> 
                        - tekan dan tahan untuk membacakan hasil <br> 
                        - geser kiri untuk menambahkan ke jadwal
                    </p>
                </div>

                <div>&nbsp;&nbsp;</div>
                <!-- {{ direction }} -->
            </div>
        </div>
    </div>
</template>