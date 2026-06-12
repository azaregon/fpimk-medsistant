<script setup>
    import { twMerge } from 'tailwind-merge'

    const variantMap = {
        default : "p-2 bg-slate-200 border-slate-300 border-4 items-center rounded-xl"
        ,yellow : "p-2 bg-yellow-200 border-yellow-300 border-4 items-center rounded-xl"
        ,green : "p-2 bg-green-300 border-green-400 border-4 items-center rounded-xl"
        ,blue : "p-2 bg-yellow-200 border-yellow-300 border-4 items-center rounded-xl"
    }
    const props = defineProps({
        variant : {
            type: String,
            required: false,
            default: 'default'
        },
        msg: {
            type: String,
            required: true,
        },
        class:String,

    })
</script>

<template>
    <div :class="twMerge(
        'text-black font-body',
        variantMap[variant], 
        props.class)">
        {{props.msg}}
<!-- 
        <div class="text-black bg-slate-200">
            ajshdasjd
        </div> -->
    </div>
</template>