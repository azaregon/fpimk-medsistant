<template>
    <div class="menu-content-area">
        <div class="button-stack">

            <button @click="goTo('/histori')" class="menu-btn histori-btn">
                <ClipboardList class="icon" :size="64" :stroke-width="2.5" />
                <span class="label">Histori</span>
            </button>

            <button @click="goTo('/jadwal')" class="menu-btn jadwal-btn">
                <CalendarPlus class="icon" :size="64" :stroke-width="2.5" />
                <span class="label">Jadwal</span>
            </button>

            <button @click="goTo('/camera')" class="menu-btn kamera-btn">
                <Camera class="icon" :size="64" :stroke-width="2.5" />
                <span class="label">Kamera</span>
            </button>

        </div>
    </div>
</template>

<script src="./MainMenu.js"></script>
<style scoped src="./MainMenu.css"></style>