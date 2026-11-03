<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const movie = ref(null)
const screenings = ref([])
const activeTab = ref('cast')
const loading = ref(true)
const error = ref('')

function goBack() {
  if (window.history.length > 1) {
    router.back()
    return
  }

  router.push({ name: 'home' })
}

function goToSeatSelection() {
  router.push({
    name: 'Booking',
    query: { movie: String(movie.value.id) },
  })
}

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

const reviews = [
  {
    author: 'Katrin L.',
    rating: 5,
    date: '12. oktoober 2024',
    text: 'Visuaalselt väga ilus film ja muusika jäi veel pikaks ajaks kummitama. Mõnusalt aeglane tempo lubab loole sisse elada.',
  },
  {
    author: 'Marko P.',
    rating: 4,
    date: '3. oktoober 2024',
    text: 'Tugevad näitlejatööd ja hea atmosfäär. Teine vaatus venis natuke, aga lõpp tasus ootamise ära.',
  },
  {
    author: 'Liis T.',
    rating: 4,
    date: '28. september 2024',
    text: 'Hea valik neile, kellele meeldivad vaiksed ja mõtestatud lood. Kinosaalis oli eriti mõjus.',
  },
]

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
  <button type="button" class="back-button" aria-label="Mine tagasi" @click="goBack">
    <span aria-hidden="true">←</span>
    Tagasi
  </button>

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
          role="tab"
          :aria-selected="activeTab === 'cast'"
          aria-controls="cast-panel"
          :class="{ 'is-active': activeTab === 'cast' }"
          @click="activeTab = 'cast'"
        >
          Režissöör ja näitlejad
        </button>
        <button
          type="button"
          class="tab-button"
          role="tab"
          :aria-selected="activeTab === 'screenings'"
          aria-controls="screenings-panel"
          :class="{ 'is-active': activeTab === 'screenings' }"
          @click="activeTab = 'screenings'"
        >
          Seansiajad
        </button>
        <button
          type="button"
          class="tab-button"
          role="tab"
          :aria-selected="activeTab === 'reviews'"
          aria-controls="reviews-panel"
          :class="{ 'is-active': activeTab === 'reviews' }"
          @click="activeTab = 'reviews'"
        >
          Hinnangud
        </button>
      </div>

      <div
        v-if="activeTab === 'cast'"
        id="cast-panel"
        class="cast-grid"
        role="tabpanel"
      >
        <div v-for="person in cast" :key="person.name" class="cast-card">
          <div class="cast-avatar" :aria-label="person.name">
            {{ person.initials }}
          </div>
          <span>{{ person.name }}</span>
        </div>
      </div>

      <div
        v-else-if="activeTab === 'screenings'"
        id="screenings-panel"
        class="screening-box"
        role="tabpanel"
      >
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

      <div
        v-else-if="activeTab === 'reviews'"
        id="reviews-panel"
        class="reviews-box"
        role="tabpanel"
      >
        <h2>Vaatajate arvamused</h2>
        <ul class="review-list">
          <li v-for="review in reviews" :key="review.author" class="review-item">
            <div class="review-heading">
              <strong>{{ review.author }}</strong>
              <span class="review-rating" :aria-label="`${review.rating} tärni viiest`">
                {{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}
              </span>
            </div>
            <p>{{ review.text }}</p>
            <time>{{ review.date }}</time>
          </li>
        </ul>
      </div>

      <button type="button" class="seat-selection-button" @click="goToSeatSelection">
        Vali istekohad
      </button>
    </div>
  </article>
</template>

<style scoped>
:global(:root) {
  --screen-bg: #100d0e;
  --screen-panel: #1b1517;
  --screen-panel-muted: #b7a9a9;
  --screen-border: rgba(245, 238, 238, 0.1);
  --screen-text: var(--cinema-paper);
  --screen-subtle: var(--cinema-muted);
  --screen-heading: var(--cinema-highlight);
  --screen-accent: var(--cinema-highlight);
}

.back-button {
  position: fixed;
  top: 5.5rem;
  left: 1.25rem;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.55rem 0.8rem;
  border: 1px solid rgba(245, 238, 238, 0.2);
  border-radius: 999px;
  background: rgba(27, 21, 23, 0.92);
  color: var(--cinema-paper);
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 700;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
  backdrop-filter: blur(8px);
}

.back-button:hover,
.back-button:focus-visible {
  border-color: rgba(217, 119, 136, 0.7);
  color: #d97788;
}

.back-button span {
  font-size: 1.1rem;
  line-height: 1;
}

.movie-detail {
  width: 100%;
  min-height: calc(100vh - 72px);
  margin: 0;
  padding: clamp(2.5rem, 7vw, 6rem) max(1.25rem, 2vw);
  color: var(--screen-text);
  background:
    radial-gradient(ellipse at 82% 0%, rgba(142, 38, 57, 0.2), transparent 34rem),
    var(--screen-bg);
}

.detail-hero {
  display: grid;
  grid-template-columns: minmax(220px, 31%) minmax(0, 1fr);
  max-width: 980px;
  min-height: 26rem;
  margin: 0 auto;
  overflow: hidden;
  border: 1px solid var(--screen-border);
  border-radius: 0.85rem;
  background: var(--screen-panel);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
}

.detail-poster {
  position: relative;
  display: flex;
  min-height: 100%;
  background: linear-gradient(145deg, #44232b, #191315 70%);
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
  color: var(--cinema-paper);
  font-family: var(--serif);
  background: linear-gradient(145deg, #44232b, #191315 70%);
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
  color: var(--cinema-paper);
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
  background-color: #191315;
}

.detail-visual::before {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(16, 13, 14, 0.82), rgba(16, 13, 14, 0.18));
  content: '';
}

.detail-visual__content {
  position: absolute;
  right: 1.5rem;
  bottom: 1.25rem;
  left: 1.5rem;
  z-index: 1;
  color: var(--cinema-paper);
}

.eyebrow {
  display: inline-block;
  margin-bottom: 0.9rem;
  color: #d78a96;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.detail-visual__content h1 {
  color: var(--cinema-paper);
  font-size: clamp(2.2rem, 4.8vw, 4rem);
  line-height: 1.02;
  letter-spacing: -0.05em;
}

.detail-body {
  max-width: 980px;
  margin: 1.5rem auto 0;
  padding: 1.5rem 0 1.9rem;
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
  border-top: 1px solid rgba(245, 238, 238, 0.14);
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
  border: 1px solid rgba(245, 238, 238, 0.18);
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(142, 38, 57, 0.35), rgba(10, 9, 8, 0.24));
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
  border-top: 1px solid rgba(245, 238, 238, 0.14);
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
  background: rgba(245, 238, 238, 0.04);
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

.reviews-box {
  margin-top: 2rem;
  padding-top: 1.4rem;
  border-top: 1px solid rgba(245, 238, 238, 0.14);
}

.reviews-box h2 {
  margin: 0 0 0.8rem;
  color: var(--screen-text);
  font-size: 1.1rem;
}

.review-list {
  display: grid;
  gap: 0.7rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.review-item {
  padding: 0.9rem 1rem;
  border: 1px solid var(--screen-border);
  border-radius: 0.45rem;
  background: rgba(245, 238, 238, 0.04);
}

.review-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.review-heading strong {
  color: var(--screen-text);
}

.review-rating {
  color: var(--screen-heading);
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.review-item p {
  margin: 0.55rem 0;
  color: var(--screen-subtle);
  font-size: 0.9rem;
  line-height: 1.5;
}

.review-item time {
  color: var(--screen-subtle);
  font-size: 0.75rem;
}

.seat-selection-button {
  display: block;
  margin: 2rem auto 0;
  padding: 0.8rem 1.5rem;
  border: 1px solid var(--screen-accent);
  border-radius: 999px;
  background: var(--screen-accent);
  color: var(--screen-bg);
  cursor: pointer;
  font: inherit;
  font-size: 0.9rem;
  font-weight: 700;
}

.seat-selection-button:hover,
.seat-selection-button:focus-visible {
  border-color: #e7a0ad;
  background: #e7a0ad;
}

.detail-shell--status {
  display: grid;
  place-items: center;
  padding: 2rem 1.5rem;
  min-height: calc(100vh - 72px);
  color: var(--cinema-paper);
  background:
    radial-gradient(ellipse at 82% 0%, rgba(142, 38, 57, 0.2), transparent 34rem),
    var(--screen-bg);
}

.detail-shell--error p {
  color: #d97788;
}

@media (max-width: 720px) {
  .back-button {
    top: 5rem;
    left: 0.75rem;
  }

  .movie-detail {
    padding-right: 1rem;
    padding-left: 1rem;
  }

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

  .detail-body {
    padding-right: 0;
    padding-left: 0;
  }
}
</style>
