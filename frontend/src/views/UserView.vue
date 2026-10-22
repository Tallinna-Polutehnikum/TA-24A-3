<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const userId = route.params.id
</script>

<template>
    <h1>{{ userId ? `User ID: ${userId}` : 'Kasutaja' }}</h1>
</template>
