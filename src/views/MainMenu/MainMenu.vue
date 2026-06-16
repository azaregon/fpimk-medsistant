<script setup>
import { useRouter } from 'vue-router'
import { ClipboardList, CalendarPlus, Camera } from 'lucide-vue-next'

const router = useRouter()

const goTo = (path) => {
    router.push(path)
}
</script>

<template>
    <div class="bg-white rounded-t-[32px] w-full flex-1 px-6 py-8 flex flex-col items-center justify-center">

        <div class="flex flex-col gap-5 w-full max-w-[320px]">

            <button @click="goTo('/histori')"
                class="bg-[#FCAF33] flex flex-col items-center justify-center py-10 px-5 rounded-[24px] transition-transform duration-100 active:scale-95">
                <ClipboardList class="text-white mb-1.5" :size="64" :stroke-width="2.5" />
                <span class="text-white text-[22px] font-bold tracking-[0.5px]">Histori</span>
            </button>

            <button @click="goTo('/jadwal')"
                class="bg-[#55C622] flex flex-col items-center justify-center py-10 px-5 rounded-[24px] transition-transform duration-100 active:scale-95">
                <CalendarPlus class="text-white mb-1.5" :size="64" :stroke-width="2.5" />
                <span class="text-white text-[22px] font-bold tracking-[0.5px]">Jadwal</span>
            </button>

            <button @click="goTo('/camera')"
                class="bg-[#4978E7] flex flex-col items-center justify-center py-10 px-5 rounded-[24px] transition-transform duration-100 active:scale-95">
                <Camera class="text-white mb-1.5" :size="64" :stroke-width="2.5" />
                <span class="text-white text-[22px] font-bold tracking-[0.5px]">Kamera</span>
            </button>

        </div>
    </div>
</template>