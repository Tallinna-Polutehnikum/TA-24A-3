<script setup>
import { onMounted, ref } from 'vue'

const cinemas = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/cinema/cinemas/`)

    if (!response.ok) {
      throw new Error('Kinode päring ebaõnnestus')
    }

    const data = await response.json()
    cinemas.value = Array.isArray(data.results) ? data.results : []
  } catch (error) {
    errorMessage.value = error instanceof Error
      ? error.message
      : 'Kinode laadimine ebaõnnestus'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section class="cinemas-page" aria-labelledby="cinemas-title">
    <div class="cinemas-heading">
      <p class="eyebrow">Meie asukohad</p>
      <h1 id="cinemas-title">Kinod</h1>
      <p class="intro">Leia endale sobiv kino ja naudi järgmist filmielamust.</p>
    </div>

    <p v-if="isLoading" class="cinema-status" role="status">Laen kinode nimekirja...</p>
    <p v-else-if="errorMessage" class="cinema-status cinema-error" role="alert">
      Kinode laadimine ebaõnnestus: {{ errorMessage }}
    </p>
    <p v-else-if="cinemas.length === 0" class="cinema-status" role="status">
      Kinode nimekiri on hetkel tühi.
    </p>

    <ul v-else class="cinema-list">
      <li v-for="(cinema, index) in cinemas" :key="cinema.id" class="cinema-card">
        <div class="cinema-number" aria-hidden="true">{{ String(index + 1).padStart(2, '0') }}</div>
        <div class="cinema-details">
          <h2>{{ cinema.name }}</h2>
          <address>
            <span>{{ cinema.street_address }}</span>
            <span>{{ cinema.postal_code }} {{ cinema.city }}</span>
            <span>{{ cinema.country }}</span>
          </address>
        </div>
        <RouterLink class="cinema-link" :to="{ name: 'MovieSchedule' }">
          Vaata kava
          <span aria-hidden="true">→</span>
        </RouterLink>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.cinemas-page {
  min-height: calc(100vh - 72px);
  padding: clamp(3.5rem, 8vw, 6.5rem) max(1.25rem, calc((100% - 1120px) / 2)) 5rem;
  color: var(--paper);
  background:
    radial-gradient(ellipse at 82% 0%, rgba(142, 38, 57, 0.28), transparent 34rem),
    var(--ink);
}

.cinemas-heading {
  max-width: 43rem;
  margin-bottom: clamp(2.5rem, 6vw, 4.5rem);
}

.eyebrow {
  margin-bottom: 0.8rem;
  color: #d97788;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

h1,
h2 {
  color: var(--paper);
}

h1 {
  font-size: clamp(3rem, 8vw, 6rem);
}

.intro {
  max-width: 34rem;
  margin-top: 1.25rem;
  color: var(--paper-muted);
  font-size: 1.1rem;
}

.cinema-list {
  display: grid;
  gap: 1rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.cinema-card {
  display: grid;
  grid-template-columns: 4rem minmax(0, 1fr) auto;
  gap: 1.5rem;
  align-items: center;
  padding: clamp(1.25rem, 3vw, 2rem);
  border: 1px solid rgba(239, 232, 232, 0.18);
  border-left: 4px solid var(--wine);
  background: rgba(73, 17, 28, 0.5);
  transition: border-color 160ms ease, background-color 160ms ease, transform 160ms ease;
}

.cinema-card:hover {
  border-color: #d97788;
  background: rgba(73, 17, 28, 0.72);
  transform: translateY(-2px);
}

.cinema-number {
  color: #d97788;
  font-family: var(--serif);
  font-size: 1.8rem;
  font-weight: 700;
}

.cinema-details h2 {
  font-size: clamp(1.4rem, 3vw, 2rem);
}

address {
  display: grid;
  gap: 0.15rem;
  margin-top: 0.55rem;
  color: var(--paper-muted);
  font-size: 0.95rem;
  font-style: normal;
}

.cinema-link {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--paper);
  font-size: 0.9rem;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.cinema-link span {
  color: #d97788;
  font-size: 1.35rem;
  transition: transform 160ms ease;
}

.cinema-link:hover span {
  transform: translateX(0.2rem);
}

.cinema-status {
  padding: 1.25rem;
  border: 1px solid rgba(239, 232, 232, 0.18);
  color: var(--paper-muted);
  background: rgba(73, 17, 28, 0.35);
}

.cinema-error {
  border-color: #d97788;
  color: var(--paper);
}

@media (max-width: 600px) {
  .cinema-card {
    grid-template-columns: 2.5rem minmax(0, 1fr);
    gap: 0.85rem;
  }

  .cinema-link {
    grid-column: 2;
  }
}
</style>
