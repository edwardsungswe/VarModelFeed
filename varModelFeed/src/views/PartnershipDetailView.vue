<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePartnershipsStore } from '@/stores/partnerships'
import VideoModal from '@/components/VideoModal.vue'

const route = useRoute()
const router = useRouter()
const store = usePartnershipsStore()

const partnership = computed(() => store.getPartnershipById(route.params.id as string))

if (!partnership.value) {
  router.replace('/')
}

const activeVideoUrl = ref('')
const isVideoModalOpen = ref(false)

function openVideo(url: string) {
  activeVideoUrl.value = url
  isVideoModalOpen.value = true
}

function closeVideo() {
  isVideoModalOpen.value = false
  activeVideoUrl.value = ''
}
</script>

<template>
  <main v-if="partnership" class="detail-page">
    <button class="back-btn" @click="router.push('/')">&larr; Back to Feed</button>

    <section class="header-section">
      <div class="logo-placeholder">
        <span class="logo-text">{{ partnership.logoPlaceholder }}</span>
      </div>
      <div>
        <h1 class="company-name">{{ partnership.companyName }}</h1>
        <h2 class="title">{{ partnership.title }}</h2>
        <p class="short-description">{{ partnership.description }}</p>
      </div>
    </section>

    <section v-if="partnership.detailedDescription" class="section">
      <h3 class="section-title">About This Partnership</h3>
      <p class="detailed-description">{{ partnership.detailedDescription }}</p>
    </section>

    <section v-if="partnership.images.length" class="section">
      <h3 class="section-title">Images</h3>
      <div class="image-gallery">
        <img
          v-for="(img, index) in partnership.images"
          :key="index"
          :src="img"
          :alt="`${partnership.companyName} image ${index + 1}`"
          loading="lazy"
          class="gallery-image"
        />
      </div>
    </section>

    <section v-if="partnership.videos.length" class="section">
      <h3 class="section-title">Videos</h3>
      <div class="video-grid">
        <button
          v-for="(video, index) in partnership.videos"
          :key="index"
          class="video-thumb-btn"
          @click="openVideo(video)"
        >
          <video :src="video" preload="metadata" class="video-thumb"></video>
          <div class="play-overlay">
            <span class="play-icon">&#9654;</span>
          </div>
        </button>
      </div>
    </section>

    <VideoModal :video-url="activeVideoUrl" :is-open="isVideoModalOpen" @close="closeVideo" />
  </main>
</template>

<style scoped>
.detail-page {
  padding: 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.back-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-bottom: 1.5rem;
}

.back-btn:hover {
  color: var(--color-primary-dark);
}

.header-section {
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.logo-placeholder {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: var(--color-accent-bg);
  border-left: 4px solid var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-primary);
}

.company-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}

.title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.short-description {
  font-size: 0.9rem;
  color: var(--vt-c-text-light-2);
  line-height: 1.5;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.75rem;
}

.detailed-description {
  font-size: 0.9rem;
  color: var(--color-text);
  line-height: 1.7;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.gallery-image {
  width: 100%;
  border-radius: 8px;
  object-fit: cover;
  aspect-ratio: 4/3;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.video-thumb-btn {
  position: relative;
  border: none;
  padding: 0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: #000;
}

.video-thumb {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  display: block;
  pointer-events: none;
}

.play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.35);
  transition: background 0.2s;
}

.video-thumb-btn:hover .play-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.play-icon {
  font-size: 2.5rem;
  color: white;
}
</style>
