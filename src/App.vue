<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="w-full h-screen flex items-center justify-center p-4">
    <div class="flex flex-col-reverse rounded-xl w-md h-full bg-linear-to-br from-blue-500 to-blue-700 overflow-clip">
      <div class="rounded-t-[5rem] bg-slate-100 h-[90%] px-6 pt-21 pb-10 overflow-clip">
        <RouterView class=" overflow-clip"/>
      </div>

      <div class="flex justify-center items-center flex-1">
        <span class="text-3xl font-black font-heading text-white">MedSistant</span>
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>
