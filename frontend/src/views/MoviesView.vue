<script setup>
import { computed, onMounted, ref } from 'vue'

const selectedDate = ref('fresh')
const selectedGenre = ref('all')
const selectedSessionType = ref('all')
const movies = ref([])
const loading = ref(true)
const error = ref('')

const genres = [
    'Draama',
    'Komöödia',
    'Põnevik',
    'Ulme',
    'Seiklus',
    'Animatsioon',
    'Krimi',
    'Romantika',
    'Õudus',
    'Dokumentaal',
]

const filteredMovies = computed(() => {
    if (selectedGenre.value === 'all') {
        return movies.value
    }

    return movies.value.filter(movie =>
        movie.genres?.some(genre => genre.name === selectedGenre.value)
    )
})

onMounted(async () => {
    try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/cinema/movies/`)

        if (!response.ok) {
            throw new Error('Filmide päring ebaõnnestus')
        }

        const data = await response.json()
        movies.value = data.results
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="movies-page">
        <section class="movie-filters" aria-label="Filmide filtrid">
            <div class="filter-group screening-date">
                <svg class="filter-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3.5" y="5.5" width="17" height="15" rx="1" />
                    <path d="M7 3.5v4M17 3.5v4M3.5 9.5h17" />
                </svg>
                <div class="filter-content">
                    <span class="filter-label">Linastusaeg</span>
                    <div class="date-options" role="group" aria-label="Linastusaja valik">
                        <button
                            type="button"
                            :class="{ 'is-selected': selectedDate === 'now' }"
                            @click="selectedDate = 'now'"
                        >
                            Hetkel kinos
                        </button>
                        <button
                            type="button"
                            :class="{ 'is-selected': selectedDate === 'fresh' }"
                            @click="selectedDate = 'fresh'"
                        >
                            Värskelt kinos
                        </button>
                    </div>
                </div>
            </div>

            <label class="filter-group select-group">
                <svg class="filter-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <circle cx="12" cy="12" r="9.5" />
                    <circle cx="12" cy="8" r="2" />
                    <circle cx="8" cy="14" r="2" />
                    <circle cx="16" cy="14" r="2" />
                </svg>
                <span class="filter-content">
                    <span class="filter-label">Žanrid</span>
                    <span class="select-wrap">
                        <select v-model="selectedGenre" aria-label="Vali žanr">
                            <option value="all">Kõik</option>
                            <option v-for="genre in genres" :key="genre" :value="genre">
                                {{ genre }}
                            </option>
                        </select>
                    </span>
                </span>
            </label>

            <label class="filter-group select-group">
                <svg class="filter-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M4 5.5h16v11H9l-5 4v-15Z" />
                    <path d="M8 10h.01M12 10h.01M16 10h.01" />
                </svg>
                <span class="filter-content">
                    <span class="filter-label">Seansi tüüp</span>
                    <span class="select-wrap">
                        <select v-model="selectedSessionType" aria-label="Vali seansi tüüp">
                            <option value="all">Kõik</option>
                            <option value="2d">2D</option>
                            <option value="3d">3D</option>
                        </select>
                    </span>
                </span>
            </label>
        </section>

        <h1>Filmid</h1>

        <p v-if="loading" class="movies-notice">Laen filme...</p>
        <p v-else-if="error" class="movies-notice movies-notice-error">
            Filmide laadimine ebaõnnestus: {{ error }}
        </p>
        <p v-else-if="filteredMovies.length === 0" class="movies-notice">
            Valitud žanris filme ei leitud.
        </p>
        <ul v-else class="movie-grid">
            <li v-for="movie in filteredMovies" :key="movie.id" class="movie-card">
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
                </div>
                <div class="movie-info">
                    <div class="movie-meta">
                        <span v-if="movie.age_rating">{{ movie.age_rating }}</span>
                        <span v-if="movie.duration">{{ movie.duration }} min</span>
                    </div>
                    <h2>{{ movie.title }}</h2>
                    <p v-if="movie.genres?.length" class="movie-genres">
                        {{ movie.genres.map(genre => genre.name).join(' · ') }}
                    </p>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.movies-page {
    --cinema-ink: #100d0e;
    --cinema-panel: #1b1517;
    --cinema-paper: #f5eeee;
    --cinema-muted: #b7a9a9;
    --cinema-wine: #8e2639;
    --cinema-highlight: #d97788;

    min-height: calc(100vh - 72px);
    padding-top: 2rem;
    padding-inline: max(1.25rem, calc((100% - 1180px) / 2));
    color: var(--cinema-paper);
    background:
        radial-gradient(ellipse at 82% 0%, rgba(142, 38, 57, 0.2), transparent 34rem),
        var(--cinema-ink);
}

.movies-page > h1 {
    padding-top: clamp(3rem, 8vw, 6rem);
    color: var(--cinema-paper);
    font-family: Georgia, 'Times New Roman', serif;
    font-weight: 500;
    text-align: left;
}

.movie-filters {
    display: flex;
    min-height: 5.5rem;
    align-items: stretch;
    gap: clamp(2rem, 8vw, 8rem);
    padding: 1rem clamp(1.25rem, 3vw, 2rem);
    color: var(--cinema-paper);
    background: var(--cinema-panel);
    border: 1px solid rgba(245, 238, 238, 0.1);
    border-radius: 0.85rem;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
}

.filter-group {
    display: flex;
    min-width: 0;
    align-items: center;
    gap: 0.9rem;
}

.screening-date {
    flex: 1.5 1 22rem;
}

.select-group {
    flex: 1 1 13rem;
}

.filter-icon {
    width: 1.65rem;
    height: 1.65rem;
    flex: 0 0 auto;
    fill: none;
    stroke: var(--cinema-muted);
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-width: 1.6;
}

.filter-content {
    display: flex;
    min-width: 0;
    flex-direction: column;
    justify-content: center;
    gap: 0.05rem;
}

.filter-label {
    color: var(--cinema-muted);
    font-size: 0.75rem;
    line-height: 1.2;
}

.date-options {
    display: flex;
    align-items: stretch;
    gap: 1.8rem;
}

.date-options button {
    position: relative;
    padding: 0;
    border: 0;
    color: var(--cinema-paper);
    background: transparent;
    cursor: pointer;
    font-weight: 700;
    white-space: nowrap;
}

.date-options button::after {
    position: absolute;
    right: 0;
    bottom: -1rem;
    left: 0;
    height: 0.2rem;
    border-radius: 0.2rem 0.2rem 0 0;
    background: transparent;
    content: '';
}

.date-options button:hover,
.date-options button:focus-visible {
    color: var(--cinema-highlight);
}

.date-options button.is-selected::after {
    background: var(--cinema-highlight);
}

.date-options button:focus-visible,
.select-group:focus-within {
    outline: 2px solid var(--cinema-highlight);
    outline-offset: 4px;
}

.select-wrap {
    position: relative;
    width: fit-content;
}

.select-wrap::after {
    position: absolute;
    top: 0.35rem;
    right: -1.15rem;
    width: 0.5rem;
    height: 0.5rem;
    border-right: 2px solid var(--cinema-paper);
    border-bottom: 2px solid var(--cinema-paper);
    content: '';
    pointer-events: none;
    transform: rotate(45deg);
}

select {
    max-width: 9rem;
    padding: 0;
    border: 0;
    color: var(--cinema-paper);
    appearance: none;
    background: transparent;
    cursor: pointer;
    font-weight: 700;
}

select:focus {
    outline: none;
}

option {
    color: var(--ink);
    background: var(--cinema-paper);
}

.movies-notice {
    margin: 2rem 0;
    padding: 1.25rem 1.5rem;
    border: 1px solid rgba(245, 238, 238, 0.12);
    border-radius: 0.65rem;
    color: var(--cinema-muted);
    background: var(--cinema-panel);
    text-align: center;
}

.movies-notice-error {
    border-color: rgba(217, 119, 136, 0.45);
    color: #f1a4b0;
}

.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 225px), 1fr));
    gap: 1.5rem;
    margin: 2rem 0 4rem;
    padding: 0;
    list-style: none;
    text-align: left;
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

.poster {
    position: relative;
    aspect-ratio: 2 / 3;
    overflow: hidden;
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
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: rgba(245, 238, 238, 0.78);
    background:
        linear-gradient(145deg, #44232b, #191315 70%);
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

.movie-info {
    padding: 1rem 1rem 1.15rem;
}

.movie-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    color: #d8a1aa;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
}

.movie-card h2 {
    margin: 0.45rem 0 0;
    color: var(--cinema-paper);
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.25rem;
    line-height: 1.25;
}

.movie-genres {
    margin-top: 0.4rem;
    color: var(--cinema-muted);
    font-size: 0.8rem;
}

@media (max-width: 800px) {
    .movie-filters {
        flex-wrap: wrap;
        gap: 1.5rem 2rem;
    }

    .screening-date {
        flex-basis: 100%;
    }

    .select-group {
        flex: 1 1 calc(50% - 1rem);
    }
}

@media (max-width: 480px) {
    .movies-page {
        padding-top: 1rem;
    }

    .movie-filters {
        gap: 1.25rem;
        padding: 1rem;
    }

    .date-options {
        gap: 1rem;
    }

    .select-group {
        flex-basis: 100%;
    }
}

@media (max-width: 600px) {
    .movies-page {
        padding-inline: 1rem;
    }

    .movie-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.8rem;
    }

    .movie-info {
        padding: 0.75rem;
    }

    .movie-card h2 {
        font-size: 1.05rem;
    }
}
</style>