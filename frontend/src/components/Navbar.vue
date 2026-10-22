<template>
  <header class="site-header">
    <div class="brand-bar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark" aria-hidden="true">K</span>
        <span class="brand-name">Kinokava</span>
      </RouterLink>
    </div>

    <nav class="navigation" aria-label="Peamine navigatsioon">
      <div class="navigation-inner">
        <RouterLink
          v-for="item in navigationItems"
          :key="item.label"
          class="navigation-link"
          :class="{ 'has-menu': item.hasMenu }"
          exact-active-class="is-active"
          :to="item.to"
        >
          {{ item.label }}
          <span v-if="item.hasMenu" class="chevron" aria-hidden="true"></span>
        </RouterLink>
      </div>
    </nav>
  </header>
</template>

<script setup>
const navigationItems = [
  { label: 'Home', to: '/' },
  { label: 'KinoKava', to: '/KinoKava' },
  { label: 'Filmid', to: '/filmid' },
  { label: 'Kinod', to: '/kinod' },
  { label: 'Kasutaja', to: '/kasutaja' },
  { label: 'Žanrid', to: '/zanrid' },
  { label: 'Broneerimine', to: '/broneerimine' },
]
</script>

<style scoped>
:global(:root) {
  --ink: #0A0908;
  --wine: #49111C;
  --wine-deep: #2e0a12;
  --paper: #EFE8E8;
  --paper-dim: rgba(239, 232, 232, 0.66);
  --paper-faint: rgba(239, 232, 232, 0.12);
  --serif: "Playfair Display", Georgia, "Times New Roman", serif;
  --sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  color: var(--paper);
  background: var(--ink);
  border-top: 4px solid var(--wine);
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.28);
}

.brand-bar {
  display: none;
  background: var(--wine-deep);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--paper);
  text-decoration: none;
}

.brand-mark {
  display: grid;
  width: 2rem;
  height: 2rem;
  place-items: center;
  border: 2px solid var(--paper);
  border-radius: 50%;
  color: var(--paper);
  font-size: 1.15rem;
  font-weight: 800;
  font-family: var(--serif);
}

.brand-name {
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  font-family: var(--sans);
}

.navigation {
  background: var(--ink);
}

.navigation-inner {
  display: flex;
  min-height: 3.8rem;
  align-items: stretch;
  justify-content: center;
  gap: 0.05rem;
  margin: 0 auto;
  padding: 0 1.25rem;
}

.navigation-link {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.2rem 0.72rem 0;
  color: var(--paper-dim);
  font-size: 0.93rem;
  font-weight: 700;
  font-family: var(--sans);
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  transition: color 160ms ease, background-color 160ms ease;
}

.navigation-link::after {
  position: absolute;
  right: 0.72rem;
  bottom: 0;
  left: 0.72rem;
  height: 4px;
  border-radius: 4px 4px 0 0;
  background: transparent;
  content: '';
}

.navigation-link:hover,
.navigation-link.is-active {
  color: var(--paper);
}

.navigation-link.is-active::after {
  background: var(--paper);
}

.chevron {
  width: 0.45rem;
  height: 0.45rem;
  margin-top: -0.25rem;
  border-right: 1.5px solid currentColor;
  border-bottom: 1.5px solid currentColor;
  transform: rotate(45deg);
}

@media (max-width: 1050px) {
  .navigation-inner {
    flex-wrap: wrap;
    justify-content: flex-start;
    padding: 0.4rem 0.75rem;
  }

  .navigation-link {
    min-height: 2.8rem;
  }
}

@media (max-width: 600px) {
  .brand-bar {
    display: block;
    padding: 0.75rem 1rem;
  }

  .navigation-inner {
    min-height: auto;
    gap: 0;
  }

  .navigation-link {
    padding-inline: 0.55rem;
    font-size: 0.82rem;
  }

  .navigation-link::after {
    right: 0.55rem;
    left: 0.55rem;
  }
}
</style>
