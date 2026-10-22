<template>
  <Navbar />
  <main>
    <RouterView />
  </main>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style scoped>
main {
  min-height: calc(100vh - 72px);
  text-align: center;
}
</style>
