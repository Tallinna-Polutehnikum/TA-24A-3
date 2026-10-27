<script setup>
import { computed, onMounted, ref } from 'vue'

const today = new Date()
today.setHours(0, 0, 0, 0)

const lastWeekStart = new Date(today)
lastWeekStart.setDate(lastWeekStart.getDate() + 7)

const weekStart = ref(new Date(today))
const selectedDate = ref(new Date(today))
const selectedCinema = ref('all')
const cinemas = ref([])
const cinemasLoading = ref(true)
const cinemaError = ref('')

const days = computed(() =>
  Array.from({ length: 7 }, (_, index) => {
    const date = new Date(weekStart.value)
    date.setDate(date.getDate() + index)
    return date
  })
)

const isFirstWeek = computed(() => weekStart.value.getTime() <= today.getTime())
const isLastWeek = computed(() => weekStart.value.getTime() >= lastWeekStart.getTime())

function dateKey(date) {
  return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
}

function formatWeekday(date) {
  return new Intl.DateTimeFormat('et-EE', { weekday: 'narrow' }).format(date)
}

function formatDate(date) {
  return new Intl.DateTimeFormat('et-EE', {
    day: 'numeric',
    month: 'short',
  }).format(date)
}

function shiftWeek(amount) {
  const nextStart = new Date(weekStart.value)
  nextStart.setDate(nextStart.getDate() + amount * 7)

  if (nextStart < today || nextStart > lastWeekStart) return

  const nextSelectedDate = new Date(selectedDate.value)
  nextSelectedDate.setDate(nextSelectedDate.getDate() + amount * 7)
  weekStart.value = nextStart
  selectedDate.value = nextSelectedDate
}

onMounted(async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/cinema/cinemas/`)

    if (!response.ok) {
      throw new Error('Kinode päring ebaõnnestus')
    }

    const data = await response.json()
    cinemas.value = data.results
  } catch (error) {
    cinemaError.value = error.message
  } finally {
    cinemasLoading.value = false
  }
})
</script>

<template>
  <section class="schedule-page" aria-label="Kinokava valikud">
    <div class="schedule-bar">
      <label class="cinema-picker">
        <svg class="cinema-icon" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z" />
          <circle cx="12" cy="10" r="2.5" />
        </svg>
        <span class="cinema-field">
          <span class="field-label">Kino</span>
          <span class="select-wrap">
            <select v-model="selectedCinema" aria-label="Vali kino"            >
              <option value="all">Tallinn - kõik kinod</option>
              <option
                v-for="cinema in cinemas"
                :key="cinema.id"
                :value="String(cinema.id)"
              >
                {{ cinema.city }} - {{ cinema.name }}
              </option>
            </select>
          </span>
        </span>
      </label>

      <div class="date-picker" aria-label="Vali nädalapäev">
        <button
          class="week-arrow"
          type="button"
          aria-label="Eelmine nädal"
          :disabled="isFirstWeek"
          @click="shiftWeek(-1)"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="m15 4-8 8 8 8" />
          </svg>
        </button>

        <div class="days-list">
          <button
            v-for="day in days"
            :key="dateKey(day)"
            class="day-option"
            :class="{ 'is-selected': dateKey(day) === dateKey(selectedDate) }"
            type="button"
            :aria-pressed="dateKey(day) === dateKey(selectedDate)"
            :aria-label="new Intl.DateTimeFormat('et-EE', { dateStyle: 'full' }).format(day)"
            @click="selectedDate = day"
          >
            <strong>{{ formatWeekday(day) }}</strong>
            <span>{{ formatDate(day) }}</span>
          </button>
        </div>

        <button
          class="week-arrow"
          type="button"
          aria-label="Järgmine nädal"
          :disabled="isLastWeek"
          @click="shiftWeek(1)"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="m9 4 8 8-8 8" />
          </svg>
        </button>
      </div>
    </div>

    <p v-if="cinemasLoading" class="cinema-status" role="status">Laen kinode nimekirja...</p>
    <p v-else-if="cinemaError" class="cinema-status cinema-error" role="alert">
      Kinode laadimine ebaõnnestus: {{ cinemaError }}
    </p>
  </section>
</template>

<style scoped>
.schedule-page {
  min-height: calc(100vh - 72px);
  padding: 2rem max(1.25rem, calc((100% - 1180px) / 2));
  box-sizing: border-box;
  color: var(--paper);
  background:
    radial-gradient(ellipse at 82% 0%, var(--wine-soft), transparent 34rem),
    var(--ink);
}

.schedule-bar {
  display: grid;
  grid-template-columns: minmax(17rem, 1fr) minmax(0, 3.2fr);
  min-height: 5.5rem;
  overflow: hidden;
  border: 1px solid var(--paper-subtle);
  border-radius: 0.85rem;
  background: rgba(239, 232, 232, 0.04);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
}

.cinema-picker,
.date-picker,
.week-arrow,
.day-option {
  display: flex;
  align-items: center;
}

.cinema-picker {
  min-width: 0;
  gap: 0.9rem;
  padding: 1rem clamp(1.25rem, 3vw, 2rem);
}

.cinema-icon {
  width: 1.65rem;
  height: 1.65rem;
  flex: 0 0 auto;
  fill: none;
  stroke: var(--paper-muted);
  stroke-width: 1.6;
}

.cinema-field {
  display: grid;
  min-width: 0;
  gap: 0.05rem;
}

.field-label {
  color: var(--paper-muted);
  font-size: 0.75rem;
}

.select-wrap {
  position: relative;
  min-width: 0;
}

.select-wrap select {
  width: 100%;
  min-width: 0;
  padding: 0 1.5rem 0 0;
  border: 0;
  appearance: none;
  background: transparent;
  color: var(--paper);
  cursor: pointer;
  font: inherit;
  font-weight: 700;
  text-overflow: ellipsis;
}

.select-wrap option {
  color: var(--ink);
  background: var(--paper);
}

.select-wrap:after {
  position: absolute;
  top: 0.3rem;
  right: 0.2rem;
  width: 0.5rem;
  height: 0.5rem;
  border-right: 2px solid var(--paper);
  border-bottom: 2px solid var(--paper);
  content: '';
  pointer-events: none;
  transform: rotate(45deg);
}

.date-picker {
  min-width: 0;
  align-items: stretch;
  border-left: 1px solid var(--paper-subtle);
}

.days-list {
  display: grid;
  min-width: 0;
  flex: 1;
  grid-template-columns: repeat(7, minmax(3.5rem, 1fr));
  overflow-x: auto;
  scrollbar-width: none;
}

.days-list::-webkit-scrollbar { display: none; }

.week-arrow,
.day-option {
  justify-content: center;
  border: 0;
  color: var(--paper);
  font: inherit;
}

.week-arrow {
  width: 3rem;
  flex: 0 0 auto;
  background: transparent;
  cursor: pointer;
}

.week-arrow svg {
  width: 1.25rem;
  height: 1.25rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.5;
}

.week-arrow:hover:not(:disabled),
.day-option:hover {
  color: var(--paper-muted);
}

.week-arrow:disabled {
  color: var(--paper-muted);
  cursor: default;
}

.day-option {
  position: relative;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.8rem 0.25rem;
  background: transparent;
  cursor: pointer;
}

.day-option:after {
  position: absolute;
  right: 0.55rem;
  bottom: 0;
  left: 0.55rem;
  height: 0.2rem;
  border-radius: 0.2rem 0.2rem 0 0;
  background: transparent;
  content: '';
}

.day-option strong {
  font-size: 1.5rem;
  font-weight: 600;
}

.day-option span {
  color: var(--paper-muted);
  font-size: 0.875rem;
  white-space: nowrap;
}

.day-option.is-selected {
  color: var(--paper);
}

.day-option.is-selected:after {
  background: var(--wine);
}

.cinema-status {
  margin: 0.5rem 0 0;
  color: var(--paper-muted);
  font-size: 0.875rem;
}

.cinema-error {
  color: var(--paper);
}

.cinema-picker:focus-within,
.week-arrow:focus-visible,
.day-option:focus-visible {
  outline: 2px solid var(--paper);
  outline-offset: 3px;
}

@media (max-width: 800px) {
  .schedule-bar {
    grid-template-columns: 1fr;
  }

  .cinema-picker {
    min-height: 4.5rem;
    border-bottom: 1px solid var(--paper-subtle);
  }

  .date-picker {
    min-height: 5rem;
    border-left: 0;
  }

  .week-arrow {
    width: 2.75rem;
  }

  .day-option strong {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .schedule-page {
    padding: 1rem;
  }

  .week-arrow {
    width: 2.25rem;
  }

  .day-option {
    padding-inline: 0.15rem;
  }

  .day-option span {
    font-size: 0.8rem;
  }

  .day-option:after {
    right: 0.25rem;
    left: 0.25rem;
  }
}
</style>
