<script setup lang="ts">
import router from './router';

</script>

<template>
  <nav>
    <routerLink to="/">Home</routerLink>
    <routerLink to="/about">About</routerLink>
  </nav>
  <main>
      <RouterView />
  </main>
</template>
