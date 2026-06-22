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
  },
  medicineData: {
    type: Object,
    default: () => ({})
  }
})


var { isSupported, isSpeaking, speak, stop } = useSpeechSynthesis("berhasil membaca obat. geser kanan untuk kembali, tekan dan tahan setengah detik untuk membacakan hasil, geser kiri untuk menambahkan ke jadwal", {lang: 'id-ID', rate: 2})
speak()

const toread = props.toread

var { isSupported, isPlaying, speak, stop } = useSpeechSynthesis(toread, { lang: 'id-ID' })

const swipe_elem = useTemplateRef('swipe_elem')
const { isSwiping, direction } = usePointerSwipe(swipe_elem)

const saveToBackendAndRedirect = async () => {
  const use_backend = localStorage.getItem('use_backend') === 'true'
  if (use_backend) {
    try {
      const base_url = 'http://127.0.0.1:5000'
      const payload = {
        name: props.medicineData?.brand || 'Obat Baru',
        time: props.medicineData?.schedule?.interval_h ? `${props.medicineData.schedule.interval_h}:00` : '08:00',
        dose: props.medicineData?.dosage || '1 Tablet',
        qty: '1 Pcs',
        all_desc: props.toread
      }
      await fetch(`${base_url}/api/schedules`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    } catch (e) {
      console.error("Failed to save schedule to backend:", e)
    }
  }
  router.push("/jadwal")
}

watch(direction, (newval, oldval) => {
    if (newval == "right") {
        console.log("right")
        router.push("/")
    } else if (newval == "left") {
        console.log("left")
        saveToBackendAndRedirect()
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