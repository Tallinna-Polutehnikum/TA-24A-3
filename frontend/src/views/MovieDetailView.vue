<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const movie = ref(null)
const screenings = ref([])
const activeTab = ref('cast')
const loading = ref(true)
const error = ref('')

const year = computed(() => {
  if (!movie.value?.release_date) return '2024'

  const parsed = new Date(movie.value.release_date)
  return Number.isNaN(parsed.getTime()) ? '2024' : parsed.getFullYear()
})

const movieGenres = computed(() => {
  return movie.value?.genres?.map(genre => genre.name).join(' · ') || 'Drama'
})

const ratingStats = computed(() => [
  { value: '8.1', label: 'IMDb' },
  { value: '78', label: 'Metacritic' },
  { value: '61', label: 'Tomatometer' },
])

const cast = computed(() => {
  const fallbackNames = [
    'Audrey Ta', 'Mathieu Ka', 'Rufus', 'Jamel Debb', 'Isabelle Na',
    'Dominique', 'Yolande M.', 'Urbain Car', 'Maurice B.', 'Michel R.'
  ]

  const names = Array.from({ length: 10 }, (_, index) => {
    const generated = fallbackNames[index] || `Cast ${index + 1}`
    const initials = generated
      .split(/\s|\./)
      .filter(Boolean)
      .map(part => part[0]?.toUpperCase() || '')
      .slice(0, 2)
      .join('') || 'A'

    return { name: generated, initials }
  })

  return names
})

function formatScreeningDate(startTime) {
  return new Intl.DateTimeFormat('et-EE', {
    weekday: 'short',
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(startTime))
}

async function fetchMovieData() {
  loading.value = true
  error.value = ''

  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/cinema/movies/${route.params.id}/`)

    if (!response.ok) {
      throw new Error('Filmi andmete laadimine ebaõnnestus')
    }

    const movieData = await response.json()
    movie.value = movieData

    const screeningsResponse = await fetch(`${apiUrl}/api/cinema/screenings/`)
    if (screeningsResponse.ok) {
      const screeningsData = await screeningsResponse.json()
      screenings.value = screeningsData.results.filter(
        screening => Number(screening.movie_id) === Number(movieData.id)
      )
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

watch(
  () => route.params.id,
  () => {
    fetchMovieData()
  },
  { immediate: true }
)
</script>

<template>
  <section v-if="loading" class="detail-shell detail-shell--status">
    <p>Laen filmiandmeid...</p>
  </section>

  <section v-else-if="error" class="detail-shell detail-shell--status detail-shell--error">
    <p>{{ error }}</p>
  </section>

  <article v-else-if="movie" class="movie-detail">
    <div class="detail-hero">
      <div class="detail-poster">
        <img
          v-if="movie.poster_url"
          :src="movie.poster_url"
          :alt="`${movie.title} filmi plakat`"
        >
        <div v-else class="poster-placeholder">
          <span>{{ movie.title.slice(0, 1) }}</span>
        </div>
        <div class="poster-caption">
          <strong>{{ movie.title }}</strong>
          <span>{{ year }}</span>
        </div>
      </div>

      <div
        class="detail-visual"
        :style="movie.poster_url ? { backgroundImage: `linear-gradient(90deg, rgba(10,9,8,0.56), rgba(10,9,8,0.12)), url(${movie.poster_url})` } : null"
      >
        <div class="detail-visual__content">
          <span class="eyebrow">Featured</span>
          <h1>{{ movie.title }}</h1>
        </div>
      </div>
    </div>

    <div class="detail-body">
      <p class="movie-summary">
        {{ movie.description || 'Filmi üksikasjad on hetkel kättesaadavad.' }}
      </p>

      <div class="stats-row" aria-label="Filmi reitingud">
        <div v-for="stat in ratingStats" :key="stat.label" class="stat-item">
          <strong>{{ stat.value }}</strong>
          <span>{{ stat.label }}</span>
        </div>
      </div>

      <div class="detail-tabs" aria-label="Filmiteabe vahelehed">
        <button
          type="button"
          class="tab-button"
          :class="{ 'is-active': activeTab === 'cast' }"
          @click="activeTab = 'cast'"
        >
          Režissöör ja näitlejad
        </button>
        <button
          type="button"
          class="tab-button"
          :class="{ 'is-active': activeTab === 'screenings' }"
          @click="activeTab = 'screenings'"
        >
          Seansiajad
        </button>
        <button type="button" class="tab-button">Hinnangud</button>
      </div>

      <div v-if="activeTab === 'cast'" class="cast-grid">
        <div v-for="person in cast" :key="person.name" class="cast-card">
          <div class="cast-avatar" :aria-label="person.name">
            {{ person.initials }}
          </div>
          <span>{{ person.name }}</span>
        </div>
      </div>

      <div v-else-if="activeTab === 'screenings'" class="screening-box">
        <h2>Kinokavad</h2>
        <p v-if="!screenings.length" class="screening-empty">
          Sellele filmile ei ole hetkel seansse saadaval.
        </p>
        <ul v-else class="screening-list">
          <li v-for="screening in screenings" :key="screening.id" class="screening-item">
            <time :datetime="screening.start_time">
              {{ formatScreeningDate(screening.start_time) }}
            </time>
            <span>{{ screening.cinema_name }} · {{ screening.hall_name }}</span>
            <small>
              {{ screening.screen_type }}
              <template v-if="screening.language"> · {{ screening.language }}</template>
              <template v-if="screening.subtitles"> · subtiitrid: {{ screening.subtitles }}</template>
            </small>
          </li>
        </ul>
      </div>
    </div>
  </article>
</template>

<style scoped>
:global(:root) {
  --screen-bg: rgba(10, 9, 8, 0.94);
  --screen-panel: rgba(239, 232, 232, 0.96);
  --screen-panel-muted: rgba(239, 232, 232, 0.72);
  --screen-border: rgba(73, 17, 28, 0.14);
  --screen-text: var(--ink);
  --screen-subtle: rgba(10, 9, 8, 0.64);
  --screen-heading: var(--wine);
  --screen-accent: var(--wine);
}

.movie-detail {
  width: min(100%, 62rem);
  margin: 2rem auto 4rem;
  padding: 0.5rem 0 0;
  background: var(--screen-panel);
  border: 1px solid var(--screen-border);
  border-radius: 1rem;
  box-shadow: 0 24px 48px rgba(10, 9, 8, 0.12);
}

.detail-hero {
  display: grid;
  grid-template-columns: minmax(220px, 31%) minmax(0, 1fr);
  min-height: 26rem;
}

.detail-poster {
  position: relative;
  display: flex;
  min-height: 100%;
  background: linear-gradient(180deg, #1f1b1c 0%, #0d0d0f 100%);
}

.detail-poster img,
.poster-placeholder {
  width: 100%;
  height: 100%;
  min-height: 26rem;
  object-fit: cover;
}

.poster-placeholder {
  display: grid;
  place-items: center;
  font-size: clamp(4rem, 7vw, 7rem);
  color: var(--paper);
  font-family: var(--serif);
  background: linear-gradient(160deg, var(--wine), var(--ink));
}

.poster-caption {
  position: absolute;
  right: 0.75rem;
  bottom: 0.9rem;
  left: 0.75rem;
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 0.75rem;
  color: var(--paper);
  text-shadow: 0 2px 12px rgba(10, 9, 8, 0.7);
}

.poster-caption strong {
  font-size: clamp(1.1rem, 2vw, 2rem);
  font-weight: 700;
  letter-spacing: -0.04em;
}

.poster-caption span {
  font-size: 0.76rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.9;
}

.detail-visual {
  position: relative;
  min-height: 26rem;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}

.detail-visual::before {
  position: absolute;
  inset: 0;
  background: rgba(10, 9, 8, 0.18);
  content: '';
}

.detail-visual__content {
  position: absolute;
  right: 1.5rem;
  bottom: 1.25rem;
  left: 1.5rem;
  z-index: 1;
  color: var(--paper);
}

.eyebrow {
  display: inline-block;
  margin-bottom: 0.9rem;
  color: rgba(239, 232, 232, 0.82);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.detail-visual__content h1 {
  color: var(--paper);
  font-size: clamp(2.2rem, 4.8vw, 4rem);
  line-height: 1.02;
  letter-spacing: -0.05em;
}

.detail-body {
  padding: 1.5rem 1.4rem 1.9rem;
  color: var(--screen-text);
}

.movie-summary {
  max-width: 47rem;
  color: var(--screen-subtle);
  font-size: 1.08rem;
  line-height: 1.55;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(10, 9, 8, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  align-items: center;
  text-align: center;
}

.stat-item strong {
  color: var(--screen-heading);
  font-size: clamp(1.8rem, 3vw, 2.5rem);
  font-weight: 700;
  letter-spacing: -0.05em;
}

.stat-item span {
  color: var(--screen-subtle);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.detail-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  margin-top: 1.75rem;
  padding-top: 0.2rem;
}

.tab-button {
  padding: 0;
  border: 0;
  border-bottom: 2px solid transparent;
  background: transparent;
  color: var(--screen-subtle);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 700;
}

.tab-button.is-active {
  border-color: var(--screen-accent);
  color: var(--screen-text);
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 1rem 0.9rem;
  margin-top: 1.4rem;
}

.cast-card {
  display: grid;
  justify-items: center;
  gap: 0.6rem;
  text-align: center;
}

.cast-avatar {
  display: grid;
  width: 4.8rem;
  height: 4.8rem;
  place-items: center;
  border: 1px solid rgba(73, 17, 28, 0.18);
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(73, 17, 28, 0.12), rgba(10, 9, 8, 0.08));
  color: var(--screen-heading);
  font-size: 1.1rem;
  font-weight: 700;
}

.cast-card span {
  max-width: 7rem;
  color: var(--screen-subtle);
  font-size: 0.78rem;
  line-height: 1.3;
}

.screening-box {
  margin-top: 2rem;
  padding-top: 1.4rem;
  border-top: 1px solid rgba(10, 9, 8, 0.1);
}

.screening-box h2 {
  margin: 0 0 0.8rem;
  color: var(--screen-text);
  font-size: 1.1rem;
}

.screening-box ul {
  margin: 0;
  padding-left: 1.2rem;
  color: var(--screen-subtle);
  line-height: 1.8;
}

.screening-list {
  display: grid;
  gap: 0.7rem;
  padding-left: 0 !important;
  list-style: none;
}

.screening-item {
  display: grid;
  gap: 0.2rem;
  padding: 0.8rem 1rem;
  border: 1px solid var(--screen-border);
  border-radius: 0.45rem;
  background: rgba(73, 17, 28, 0.04);
}

.screening-item time {
  color: var(--screen-heading);
  font-weight: 700;
}

.screening-item span {
  color: var(--screen-text);
  font-size: 0.9rem;
}

.screening-item small,
.screening-empty {
  color: var(--screen-subtle);
  font-size: 0.78rem;
}

.screening-empty {
  margin: 0;
}

.detail-shell--status {
  display: grid;
  min-height: 18rem;
  place-items: center;
  padding: 2rem 1.5rem;
  color: var(--ink);
}

.detail-shell--error p {
  color: var(--wine);
}

@media (max-width: 720px) {
  .detail-hero {
    grid-template-columns: 1fr;
  }

  .detail-poster,
  .detail-poster img,
  .poster-placeholder {
    min-height: 20rem;
  }

  .detail-visual {
    min-height: 14rem;
  }

  .detail-visual__content {
    right: 1rem;
    bottom: 1rem;
    left: 1rem;
  }

  .movie-summary {
    font-size: 1rem;
  }
}
</style>
