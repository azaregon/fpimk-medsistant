<script setup>
import { useRoute } from 'vue-router';

const route = useRoute()
const id = route.query.id
</script>


<template>
    <div>
        <span>
            klajdlkajsd
        </span>
        {{ id }}
    </div>
</template>