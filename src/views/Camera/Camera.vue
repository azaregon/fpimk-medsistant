<script setup lang="js">
import { useDevicesList, useUserMedia } from '@vueuse/core'
import { reactive, ref, shallowRef, useTemplateRef, watchEffect, onMounted, onUnmounted } from 'vue'
import { Circle } from '@lucide/vue';
import { usePointerSwipe, 
    useEventListener, 
    useSpeechSynthesis,
    onLongPress
} from '@vueuse/core'

import SuccessOverlay from './components/SuccessOverlay.vue';
import FailedOverlay from './components/FailedOverlay.vue';


const use_backend = ref(localStorage.getItem('use_backend') === 'true')
const base_url = 'http://127.0.0.1:5000'

const updateBackendState = () => {
  use_backend.value = localStorage.getItem('use_backend') === 'true'
}

onMounted(() => {
  window.addEventListener('use-backend-changed', updateBackendState)
})

onUnmounted(() => {
  window.removeEventListener('use-backend-changed', updateBackendState)
})


const shownOverlay = ref('none')
const medicine_result = ref()
const currentCamera = ref()
const capturedImage = ref()
const canvas = ref(null)    
const { videoInputs: cameras } = useDevicesList({
  requestPermissions: true,
  onUpdated() {
    if (!cameras.value.some(i => i.deviceId === currentCamera.value))
      currentCamera.value = cameras.value[0]?.deviceId
  },
})

const video = useTemplateRef('video')
const { stream, enabled } = useUserMedia({
  constraints: reactive({ video: { deviceId: { exact: currentCamera } } }),
})
enabled.value = true;

watchEffect(() => {
  if (video.value)
    video.value.srcObject = stream.value
})

const sendPhotoAsJson = async () => {
//   if (!capturedImage.value) return;

  try {
    var { isSupported, isSpeaking, speak, stop } = useSpeechSynthesis("melakukan pencarian informasi tentang obat, mohon tunggu", {lang: 'id-ID', rate: 2})
    speak()
    const response = await fetch(`${base_url}/recognize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image: capturedImage.value
      }),
    });
    

    const data = await response.json();
    console.log("Success:", data);
    if (data['status'] === "ok") {
        medicine_result.value = data["data"]
        shownOverlay.value = "success"
    } else {
        console.log("Error uploading image");
        shownOverlay.value = "failed"    
    }
  } catch (error) {
    console.log("Error uploading image:", error);
    shownOverlay.value = "failed"
  }
}


const takePhoto = async () => {
  const ctx = canvas.value.getContext('2d')
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  
  // Draw the current video frame onto the canvas
  ctx.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
  
  // Convert canvas to a data URL (image/jpeg)
  capturedImage.value = canvas.value.toDataURL('image/jpeg')
  if (use_backend.value) {
    sendPhotoAsJson()
  } else {
    medicine_result.value = {
      brand: 'Mefinal',
      all_desc: `Berikut adalah deskripsi mengenai obat Mefinal:
Kandungan Aktif: Asam mefenamat (Mefenamic acid).
Golongan: Obat Anti-Inflamasi Non-Steroid (OAINS). Di Indonesia, obat ini termasuk dalam kategori obat keras (berlogo lingkaran merah) sehingga penggunaannya harus menggunakan resep dokter.
Indikasi dan Kegunaan: Berfungsi untuk meredakan nyeri ringan hingga sedang dan mengurangi peradangan. Mefinal umum digunakan untuk mengatasi sakit gigi, sakit kepala, nyeri haid (dismenore), nyeri otot, nyeri sendi, serta nyeri pasca operasi atau cedera.
Cara Kerja: Obat ini bekerja dengan cara menghambat produksi prostaglandin, yaitu zat kimia alami dalam tubuh yang memicu rasa sakit dan reaksi peradangan saat terjadi kerusakan jaringan.
Perhatian Penggunaan: Mefinal sangat disarankan untuk dikonsumsi setelah makan guna mencegah atau meminimalkan efek samping pada saluran pencernaan, seperti iritasi lambung atau mual.
Catatan: Informasi ini hanya untuk tujuan edukasi. Selalu konsultasikan dengan dokter atau apoteker dan ikuti dosis yang diresepkan sebelum mengonsumsi obat ini.`
    }
  shownOverlay.value = "success"
  }
}
</script>

<template>
    <SuccessOverlay :toread="medicine_result ? medicine_result['all_desc'] : ''" :medicineData="medicine_result" v-if="shownOverlay === 'success'" @close="shownOverlay = 'none'" />
    <FailedOverlay v-else-if="shownOverlay === 'failed'" @close="shownOverlay = 'none'" />   
    <div class="flex flex-col flex-1 h-full justify-between">
        <div class="flex items-center justify-center gap-4 text-center hidden">
            <div>
                <button @click="enabled = !enabled" class="bg-blue-300 py-2 px-6 " >
                    {{ enabled ? 'Stop' : 'Start' }}
                </button>
            </div>
            <div>
                <select name="hahah" id="hhiihi" v-model="currentCamera">
                    <option 
                        v-for="camera of cameras"
                        :key="camera.deviceId"
                        :value="camera.deviceId"
                        class="px-2 py-1 cursor-pointer"
        
                    >
                        {{ camera.label }}
                    </option >
                </select>
            
            </div>
        </div>

        <div class="m-4 h-full w-full bg-black rounded-lg overflow-clip">
            <video ref="video" muted autoplay playsinline class="h-full w-full object-cover "></video>
        </div>


        <div class="flex justify-center items-center p-3">
            <button @click="takePhoto" class="cursor-pointer  active:brightness-80"><Circle fill="white" class="w-20 h-20 " /></button>
        </div>
    </div>


    <canvas ref="canvas" style="display: none;" />
    

</template>