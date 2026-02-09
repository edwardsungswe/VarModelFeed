<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePartnershipsStore } from '@/stores/partnerships'

const router = useRouter()
const store = usePartnershipsStore()

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

async function handleLogin() {
  console.log('handleLogin triggered', { email: email.value })
  if (!email.value.trim() || !password.value.trim()) {
    error.value = 'Please fill in all fields.'
    return
  }

  isLoading.value = true
  error.value = ''

  console.log('store object:', store)
  console.log('store.login type:', typeof (store as any).login)
  let result = null
  try {
    result = await store.login(email.value.trim(), password.value)
  } catch (e) {
    console.error('Error during store.login:', e)
    result = 'An unexpected error occurred.'
  }
  isLoading.value = false

  if (result) {
    error.value = result
    return
  }

  router.push('/')
}
</script>

<template>
  <main class="sign-in">
    <section class="header-section">
      <h1 class="page-title">Log In to Your Account</h1>
    </section>

    <form class="login-form" @submit.prevent="handleLogin">
      <div class="form-group">
        <label class="form-label" for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="form-input"
          placeholder="Enter your email..."
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="form-input"
          placeholder="Enter your password..."
        />
      </div>

      <div class="form-row">
        <label class="remember-me">
          <input type="checkbox" />
          <span>Remember me</span>
        </label>
        <a href="#" class="forgot-link">Forgot password?</a>
      </div>

      <p v-if="error" class="form-error">{{ error }}</p>

      <button type="submit" class="submit-btn" :disabled="isLoading">
        {{ isLoading ? 'LOGGING IN...' : 'LOG IN' }}
      </button>

      <p class="sign-up-text">Don't have an account? <a href="#">Sign Up</a></p>
    </form>
  </main>
</template>

<style scoped>
.sign-in {
  padding: 2rem 1rem;
}

.header-section {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-heading);
}

.login-form {
  max-width: 440px;
  margin: 0 auto;
  background: var(--color-background);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.375rem;
}

.form-input {
  width: 100%;
  padding: 0.65rem 0.875rem;
  font-size: 0.875rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
  color: var(--color-text);
}

.form-input::placeholder {
  color: #aaa;
}

.form-input:focus {
  border-color: var(--color-primary-light);
}

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  font-size: 0.8rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--vt-c-text-light-2);
  cursor: pointer;
}

.remember-me input {
  accent-color: var(--color-primary);
}

.forgot-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  color: var(--color-primary-dark);
}

.form-error {
  color: #dc2626;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
}

.submit-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: var(--color-primary);
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: var(--color-primary-dark);
}

.sign-up-text {
  text-align: center;
  font-size: 0.8rem;
  color: var(--vt-c-text-light-2);
  margin-top: 1.25rem;
}

.sign-up-text a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
</style>
