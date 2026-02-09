<script setup lang="ts">
import { usePartnershipsStore } from '@/stores/partnerships'

const store = usePartnershipsStore()
</script>

<template>
  <nav class="navbar">
    <RouterLink to="/" class="navbar-brand">
      <span class="brand-text">varmodel</span>
      <span class="brand-badge">AI</span>
    </RouterLink>

    <div v-if="store.isSignedIn && store.currentUser" class="navbar-user">
      <div class="user-avatar">
        <img
          :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${store.currentUser.name}`"
          alt="User avatar"
          class="avatar-img"
        />
      </div>
      <span class="user-name">{{ store.currentUser.email }}</span>
    </div>

    <RouterLink v-else to="/sign-in" class="sign-in-link">Sign In</RouterLink>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 2rem;
  background: var(--color-background);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  text-decoration: none;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: -0.02em;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--color-accent-bg);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 0.875rem;
  color: var(--color-text);
  font-weight: 500;
}

.sign-in-link {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.sign-in-link:hover {
  color: var(--color-primary-dark);
}
</style>
