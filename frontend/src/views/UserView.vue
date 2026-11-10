<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const user = ref(null)
const mode = ref('login')
const loading = ref(false)
const message = ref('')
const errors = ref({})

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  phone_number: '',
  first_name: '',
  last_name: '',
  date_of_birth: '',
})
const profileForm = reactive({
  email: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  date_of_birth: '',
})

const title = computed(() => user.value ? 'Minu profiil' : mode.value === 'login' ? 'Logi sisse' : 'Loo konto')

function csrfCookie() {
  return document.cookie.split('; ').find((row) => row.startsWith('csrftoken='))?.split('=')[1]
}

async function ensureCsrfToken() {
  if (!csrfCookie()) await fetch(`${apiUrl}/api/cinema/auth/csrf/`, { credentials: 'include' })
  return csrfCookie()
}

async function request(path, options = {}) {
  const method = options.method || 'GET'
  const csrfToken = ['GET', 'HEAD', 'OPTIONS'].includes(method) ? null : await ensureCsrfToken()
  const response = await fetch(`${apiUrl}/api/cinema${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}), ...(options.headers || {}) },
    ...options,
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const error = new Error(data.error || data.errors?.detail || 'Päring ebaõnnestus.')
    error.fields = data.errors || {}
    throw error
  }
  return data
}

function showError(error) {
  errors.value = error.fields || {}
  message.value = error.message
}

function updateProfileForm(value) {
  Object.assign(profileForm, {
    email: value.email || '',
    first_name: value.first_name || '',
    last_name: value.last_name || '',
    phone_number: value.phone_number || '',
    date_of_birth: value.date_of_birth || '',
  })
}

async function loadUser() {
  try {
    const data = await request('/auth/me/')
    user.value = data.user
    updateProfileForm(data.user)
  } catch (error) {
    if (error.message !== 'Autentimine on vajalik.') showError(error)
  }
}

async function submitLogin() {
  loading.value = true
  message.value = ''
  errors.value = {}
  try {
    const data = await request('/auth/login/', { method: 'POST', body: JSON.stringify(loginForm) })
    user.value = data.user
    updateProfileForm(data.user)
    message.value = 'Oled sisse logitud.'
  } catch (error) {
    showError(error)
  } finally {
    loading.value = false
  }
}

async function submitRegistration() {
  loading.value = true
  message.value = ''
  errors.value = {}
  try {
    const data = await request('/auth/register/', { method: 'POST', body: JSON.stringify(registerForm) })
    user.value = data.user
    updateProfileForm(data.user)
    message.value = 'Konto on loodud ja oled sisse logitud.'
  } catch (error) {
    showError(error)
  } finally {
    loading.value = false
  }
}

async function saveProfile() {
  loading.value = true
  message.value = ''
  errors.value = {}
  try {
    const data = await request('/auth/me/', { method: 'PATCH', body: JSON.stringify(profileForm) })
    user.value = data.user
    updateProfileForm(data.user)
    message.value = 'Profiil on salvestatud.'
  } catch (error) {
    showError(error)
  } finally {
    loading.value = false
  }
}

async function logout() {
  loading.value = true
  try {
    await request('/auth/logout/', { method: 'POST', body: '{}' })
    user.value = null
    mode.value = 'login'
    message.value = 'Oled välja logitud.'
  } catch (error) {
    showError(error)
  } finally {
    loading.value = false
  }
}

onMounted(loadUser)
</script>

<template>
  <main class="user-page">
    <section class="user-card">
      <h1>{{ title }}</h1>
      <p v-if="message" class="message" role="status">{{ message }}</p>

      <div v-if="user" class="profile">
        <p class="signed-in">Sisse logitud kasutajana <strong>{{ user.username }}</strong></p>
        <form @submit.prevent="saveProfile">
          <label>E-post <input v-model="profileForm.email" type="email" required></label>
          <small v-if="errors.email" class="error">{{ errors.email }}</small>
          <label>Eesnimi <input v-model="profileForm.first_name"></label>
          <label>Perekonnanimi <input v-model="profileForm.last_name"></label>
          <label>Telefon <input v-model="profileForm.phone_number" type="tel" required></label>
          <small v-if="errors.phone_number" class="error">{{ errors.phone_number }}</small>
          <label>Sünnikuupäev <input v-model="profileForm.date_of_birth" type="date"></label>
          <button :disabled="loading" type="submit">Salvesta muudatused</button>
        </form>
        <button class="secondary" :disabled="loading" type="button" @click="logout">Logi välja</button>
      </div>

      <template v-else>
        <form v-if="mode === 'login'" @submit.prevent="submitLogin">
          <label>Kasutajanimi <input v-model="loginForm.username" autocomplete="username" required></label>
          <label>Parool <input v-model="loginForm.password" type="password" autocomplete="current-password" required></label>
          <button :disabled="loading" type="submit">Logi sisse</button>
          <button class="link-button" type="button" @click="mode = 'register'; message = ''">Loo uus konto</button>
        </form>
        <form v-else @submit.prevent="submitRegistration">
          <label>Kasutajanimi <input v-model="registerForm.username" autocomplete="username" required></label>
          <small v-if="errors.username" class="error">{{ errors.username }}</small>
          <label>E-post <input v-model="registerForm.email" type="email" autocomplete="email" required></label>
          <small v-if="errors.email" class="error">{{ errors.email }}</small>
          <label>Parool <input v-model="registerForm.password" type="password" autocomplete="new-password" required></label>
          <small v-if="errors.password" class="error">{{ [].concat(errors.password).join(' ') }}</small>
          <label>Telefon <input v-model="registerForm.phone_number" type="tel" required></label>
          <small v-if="errors.phone_number" class="error">{{ errors.phone_number }}</small>
          <label>Eesnimi <input v-model="registerForm.first_name"></label>
          <label>Perekonnanimi <input v-model="registerForm.last_name"></label>
          <label>Sünnikuupäev <input v-model="registerForm.date_of_birth" type="date"></label>
          <button :disabled="loading" type="submit">Loo konto</button>
          <button class="link-button" type="button" @click="mode = 'login'; message = ''">Mul on juba konto</button>
        </form>
        <p v-if="errors.detail" class="error">{{ errors.detail }}</p>
      </template>
    </section>
  </main>
</template>

<style scoped>
.user-page { max-width: 42rem; margin: 3rem auto; padding: 0 1rem; }
.user-card { padding: 2rem; background: var(--paper, #fff); border-radius: 0.75rem; box-shadow: 0 4px 20px #0002; }
form { display: grid; gap: 0.75rem; }
label { display: grid; gap: 0.3rem; font-weight: 700; }
input { padding: 0.65rem; border: 1px solid #bbb; border-radius: 0.35rem; font: inherit; }
button { padding: 0.7rem 1rem; border: 0; border-radius: 0.35rem; background: var(--wine, #7a1f35); color: white; font: inherit; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: wait; }
.secondary, .link-button { margin-top: 1rem; background: transparent; color: var(--wine, #7a1f35); }
.link-button { padding: 0; text-align: left; }
.message { color: #176b3a; }
.error { color: #a32121; }
.signed-in { margin-bottom: 1.5rem; }
</style>
