<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Partnership } from '@/types'

defineProps<{
  partnership: Partnership
}>()
</script>

<template>
  <div class="card">
    <div class="card-content">
      <div class="logo-placeholder">
        <span class="logo-text">{{ partnership.logoPlaceholder }}</span>
      </div>
      <div class="card-body">
        <h3 class="company-name">{{ partnership.companyName }}</h3>
        <p class="description">{{ partnership.description }}</p>
        <RouterLink :to="'/partnership/' + partnership.id" class="view-details">VIEW DETAILS</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: var(--color-background);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 1.25rem 1.5rem;
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.logo-placeholder {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--color-accent-bg);
  border-left: 4px solid var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 0.02em;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.company-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}

.description {
  font-size: 0.85rem;
  color: var(--vt-c-text-light-2);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.view-details {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 0.05em;
  text-decoration: none;
}

.view-details:hover {
  color: var(--color-primary-dark);
}
</style>
