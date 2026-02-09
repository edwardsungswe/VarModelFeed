<script setup lang="ts">
import { useRouter } from 'vue-router'
import { usePartnershipsStore } from '@/stores/partnerships'
import PartnershipCard from '@/components/PartnershipCard.vue'

const router = useRouter()
const store = usePartnershipsStore()

function handleLogout() {
  store.logout()
  router.push('/sign-in')
}
</script>

<template>
  <main class="home">
    <section class="header-section">
      <h1 class="page-title">Browse Partnership Ideas</h1>
      <p class="page-subtitle">
        Discover partnership ideas posted by companies and independent professionals, or post your
        own partnership idea!
      </p>
      <div v-if="store.isSignedIn" class="action-buttons">
        <RouterLink to="/post-idea" class="post-btn">+ POST IDEA</RouterLink>
        <button class="logout-btn" @click="handleLogout">LOG OUT</button>
      </div>
    </section>

    <section class="feed">
      <PartnershipCard
        v-for="partnership in store.sortedPartnerships"
        :key="partnership.id"
        :partnership="partnership"
      />
    </section>
  </main>
</template>

<style scoped>
.home {
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
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 0.9rem;
  color: var(--vt-c-text-light-2);
  max-width: 480px;
  margin: 0 auto 1.25rem;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.post-btn {
  display: inline-block;
  background: var(--color-primary);
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s;
}

.post-btn:hover {
  background: var(--color-primary-dark);
  color: white;
}

.logout-btn {
  display: inline-block;
  background: transparent;
  color: var(--color-primary);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  border: 1.5px solid var(--color-primary);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.logout-btn:hover {
  background: var(--color-primary);
  color: white;
}

.feed {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 640px;
  margin: 0 auto;
}
</style>
