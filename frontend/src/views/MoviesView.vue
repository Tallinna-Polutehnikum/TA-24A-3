<script setup>
import { ref } from 'vue'

const selectedDate = ref('fresh')
const selectedGenre = ref('all')
const selectedSessionType = ref('all')
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
                            <option value="action">Märul</option>
                            <option value="comedy">Komöödia</option>
                            <option value="drama">Draama</option>
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
    </div>
</template>

<style scoped>
.movies-page {
    padding-top: 2rem;
}

.movie-filters {
    display: flex;
    min-height: 5.5rem;
    align-items: stretch;
    gap: clamp(2rem, 8vw, 8rem);
    padding: 1rem clamp(1.25rem, 3vw, 2rem);
    color: var(--paper);
    background: var(--ink);
    border-radius: 0.55rem;
    box-shadow: 0 0.6rem 1.5rem rgba(10, 9, 8, 0.16);
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
    stroke: var(--paper-muted);
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
    color: var(--paper-muted);
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
    color: var(--paper);
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
    color: var(--paper);
}

.date-options button.is-selected::after {
    background: var(--wine);
}

.date-options button:focus-visible,
.select-group:focus-within {
    outline: 2px solid var(--paper);
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
    border-right: 2px solid var(--paper);
    border-bottom: 2px solid var(--paper);
    content: '';
    pointer-events: none;
    transform: rotate(45deg);
}

select {
    max-width: 9rem;
    padding: 0;
    border: 0;
    color: var(--paper);
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
    background: var(--paper);
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
</style>