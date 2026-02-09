<script setup lang="ts">
export interface MediaItem {
  url: string
  type: 'image' | 'video'
}

defineProps<{
  items: MediaItem[]
}>()

const emit = defineEmits<{
  remove: [index: number]
}>()
</script>

<template>
  <div v-if="items.length" class="media-grid">
    <div v-for="(item, index) in items" :key="index" class="media-item">
      <img v-if="item.type === 'image'" :src="item.url" class="media-thumb" alt="Preview" />
      <video v-else :src="item.url" controls class="media-thumb"></video>
      <button class="remove-btn" type="button" @click="emit('remove', index)">&times;</button>
    </div>
  </div>
</template>

<style scoped>
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.media-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
}

.media-thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
}

.remove-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #dc2626;
  color: white;
  border: none;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  background: #b91c1c;
}
</style>
