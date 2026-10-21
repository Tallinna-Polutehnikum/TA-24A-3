<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/KinoKava">KinoKava</RouterLink>
    <RouterLink to="/filmid">Filmid</RouterLink>
    <RouterLink to="/kinod">Kinod</RouterLink>
    <RouterLink to="/kasutaja">Kasutaja</RouterLink>
    <RouterLink to="/zanrid">Žanrid</RouterLink>
    <RouterLink to="/broneerimine">Broneerimine</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>
