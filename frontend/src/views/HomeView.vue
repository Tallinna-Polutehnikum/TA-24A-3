<template>
  <div class="home-page">
    <section class="intro">
      <p class="eyebrow">KINOKAVA <span aria-hidden="true">/</span> FILMIVALIK</p>
      <h1>Elamused algavad <span>siit.</span></h1>
      <p class="intro-copy">
        Avasta filmid, mida saad meie kinodes juba täna vaatama minna.
      </p>
    </section>

    <section class="movies-section" aria-labelledby="movies-heading">
      <div class="section-heading">
        <div>
          <p class="eyebrow">SUUREL EKRAANIL</p>
          <h2 id="movies-heading">Praegu kinos</h2>
        </div>
        <span v-if="!loading && !error && movies.length" class="movie-count">
          {{ movies.length }} {{ movies.length === 1 ? 'film' : 'filmi' }}
        </span>
      </div>

      <p v-if="loading" class="notice">Laen filme...</p>

      <p v-else-if="error" class="notice notice-error">
        Filmide laadimine ebaõnnestus: {{ error }}
      </p>

      <p v-else-if="movies.length === 0" class="notice">
        Hetkel ei leitud tulevaste seanssidega filme.
      </p>

      <ul v-else class="movie-grid">
        <li v-for="movie in movies" :key="movie.id" class="movie-card">
          <RouterLink :to="{ name: 'MovieDetail', params: { id: movie.id } }" class="movie-link">
            <div class="poster">
              <img
                v-if="movie.poster_url"
                :src="movie.poster_url"
                :alt="`${movie.title} filmi plakat`"
                loading="lazy"
              >
              <div v-else class="poster-placeholder" aria-hidden="true">
                <span>K</span>
                <small>KINOKAVA</small>
              </div>
              <span class="now-showing">KINOS</span>
            </div>

            <div class="movie-info">
              <div class="movie-meta">
                <span v-if="movie.age_rating">{{ movie.age_rating }}</span>
                <span v-if="movie.duration">{{ movie.duration }} min</span>
              </div>
              <h3>{{ movie.title }}</h3>
              <p v-if="movie.genres?.length" class="movie-genres">
                {{ movie.genres.map(genre => genre.name).join(' · ') }}
              </p>
              <p v-if="movie.description" class="movie-description">
                {{ movie.description }}
              </p>
            </div>
          </RouterLink>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const movies = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

    const [moviesResponse, screeningsResponse] = await Promise.all([
      fetch(`${apiUrl}/api/cinema/movies/`),
      fetch(`${apiUrl}/api/cinema/screenings/`),
    ])

    if (!moviesResponse.ok || !screeningsResponse.ok) {
      throw new Error('Filmide või seansside päring ebaõnnestus')
    }

    const moviesData = await moviesResponse.json()
    const screeningsData = await screeningsResponse.json()
    const now = Date.now()

    const movieIdsWithFutureScreenings = new Set(
      screeningsData.results
        .filter(screening => new Date(screening.start_time).getTime() >= now)
        .map(screening => screening.movie_id)
    )

    movies.value = moviesData.results.filter(movie =>
      movieIdsWithFutureScreenings.has(movie.id)
    )
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-page {
  --cinema-ink: #100d0e;
  --cinema-panel: #1b1517;
  --cinema-paper: #f5eeee;
  --cinema-muted: #b7a9a9;
  --cinema-wine: #8e2639;

  min-height: calc(100vh - 72px);
  padding: clamp(2.5rem, 7vw, 6rem) max(1.25rem, calc((100% - 1180px) / 2));
  box-sizing: border-box;
  color: var(--cinema-paper);
  background:
    radial-gradient(ellipse at 82% 0%, rgba(142, 38, 57, 0.2), transparent 34rem),
    var(--cinema-ink);
  text-align: left;
}

.intro {
  max-width: 760px;
  margin: 0 auto clamp(3.5rem, 8vw, 6.5rem);
  text-align: center;
}

.eyebrow {
  margin: 0 0 0.9rem;
  color: #d78a96;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.2em;
}

.eyebrow span {
  padding: 0 0.35rem;
  color: #74535a;
}

.intro h1 {
  margin: 0;
  color: var(--cinema-paper);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: clamp(2.6rem, 7vw, 5rem);
  font-weight: 500;
  letter-spacing: -0.055em;
  line-height: 1.05;
}

.intro h1 span {
  color: #d97788;
}

.intro-copy {
  max-width: 540px;
  margin: 1.25rem auto 0;
  color: var(--cinema-muted);
  font-size: clamp(0.95rem, 2vw, 1.1rem);
}

.movies-section {
  max-width: 1180px;
  margin: 0 auto;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(245, 238, 238, 0.14);
}

.section-heading .eyebrow {
  margin-bottom: 0.4rem;
}

.section-heading h2 {
  margin: 0;
  color: var(--cinema-paper);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 500;
}

.movie-count {
  padding: 0.35rem 0.7rem;
  border: 1px solid rgba(245, 238, 238, 0.18);
  border-radius: 999px;
  color: var(--cinema-muted);
  font-size: 0.8rem;
  white-space: nowrap;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 225px), 1fr));
  gap: 1.5rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.movie-card {
  overflow: hidden;
  border: 1px solid rgba(245, 238, 238, 0.1);
  border-radius: 0.85rem;
  background: var(--cinema-panel);
  transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

.movie-card:hover {
  transform: translateY(-5px);
  border-color: rgba(217, 119, 136, 0.55);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
}

.movie-link {
  display: block;
  color: inherit;
  text-decoration: none;
}

.poster {
  position: relative;
  overflow: hidden;
  aspect-ratio: 2 / 3;
  background: linear-gradient(145deg, #44232b, #191315 70%);
}

.poster img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 300ms ease;
}

.movie-card:hover .poster img {
  transform: scale(1.04);
}

.poster-placeholder {
  display: flex;
  width: 100%;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(245, 238, 238, 0.78);
}

.poster-placeholder span {
  display: grid;
  width: 4rem;
  height: 4rem;
  place-items: center;
  border: 1px solid rgba(245, 238, 238, 0.5);
  border-radius: 50%;
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 2rem;
}

.poster-placeholder small {
  margin-top: 0.7rem;
  font-size: 0.58rem;
  font-weight: 800;
  letter-spacing: 0.16em;
}

.now-showing {
  position: absolute;
  right: 0.75rem;
  bottom: 0.75rem;
  padding: 0.28rem 0.55rem;
  border: 1px solid rgba(245, 238, 238, 0.25);
  border-radius: 999px;
  background: rgba(16, 13, 14, 0.55);
  color: var(--cinema-paper);
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.movie-info {
  padding: 1rem 1rem 1.15rem;
}

.movie-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 0.85rem;
  color: #d78a96;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.movie-info h3 {
  margin: 0.7rem 0 0;
  color: var(--cinema-paper);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.3rem;
  line-height: 1.25;
}

.movie-genres,
.movie-description {
  margin-top: 0.55rem;
  color: var(--cinema-muted);
  font-size: 0.82rem;
  line-height: 1.5;
}

.movie-description {
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 700px) {
  .movie-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
  }

  .movie-info {
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .section-heading {
    flex-direction: column;
    align-items: flex-start;
  }

  .movie-grid {
    grid-template-columns: 1fr;
  }
}
</style>