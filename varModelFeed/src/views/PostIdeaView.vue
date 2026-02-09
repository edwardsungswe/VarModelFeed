<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePartnershipsStore } from '@/stores/partnerships'
import { validateImageFile, validateVideoFile } from '@/utils/fileValidation'
import MediaPreview from '@/components/MediaPreview.vue'

const router = useRouter()
const store = usePartnershipsStore()

const companyName = ref('')
const title = ref('')
const description = ref('')
const detailedDescription = ref('')
const error = ref('')

interface PendingMediaItem {
  url: string
  type: 'image' | 'video'
  file: File
}

const mediaItems = ref<PendingMediaItem[]>([])
const objectUrls = ref<string[]>([])

const imageInput = ref<HTMLInputElement | null>(null)
const videoInput = ref<HTMLInputElement | null>(null)

function onImagesSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files) return

  for (const file of Array.from(input.files)) {
    const result = validateImageFile(file)
    if (!result.valid) {
      error.value = result.error!
      return
    }
    const url = URL.createObjectURL(file)
    objectUrls.value.push(url)
    mediaItems.value.push({ url, type: 'image', file })
  }
  error.value = ''
  input.value = ''
}

function onVideosSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files) return

  for (const file of Array.from(input.files)) {
    const result = validateVideoFile(file)
    if (!result.valid) {
      error.value = result.error!
      return
    }
    const url = URL.createObjectURL(file)
    objectUrls.value.push(url)
    mediaItems.value.push({ url, type: 'video', file })
  }
  error.value = ''
  input.value = ''
}

function removeMedia(index: number) {
  const item = mediaItems.value[index]
  if (!item) return
  URL.revokeObjectURL(item.url)
  objectUrls.value = objectUrls.value.filter((u) => u !== item.url)
  mediaItems.value.splice(index, 1)
}

const isSubmitting = ref(false)

async function submitIdea() {
  if (!companyName.value.trim() || !title.value.trim() || !description.value.trim()) {
    error.value = 'Please fill in all required fields.'
    return
  }

  isSubmitting.value = true
  error.value = ''

  let uploadedMedia: { type: 'image' | 'video'; url: string }[] = []

  try {
    uploadedMedia = await Promise.all(
      mediaItems.value.map(async (item) => {
        const uploadedUrl = await store.uploadMedia(item.file)
        return { type: item.type, url: uploadedUrl }
      }),
    )
  } catch (uploadError) {
    isSubmitting.value = false
    error.value = uploadError instanceof Error ? uploadError.message : 'Failed to upload media.'
    return
  }

  const imageUrls = uploadedMedia.filter((m) => m.type === 'image').map((m) => m.url)
  const videoUrls = uploadedMedia.filter((m) => m.type === 'video').map((m) => m.url)

  const result = await store.addPartnership({
    companyName: companyName.value.trim(),
    title: title.value.trim(),
    description: description.value.trim(),
    detailedDescription: detailedDescription.value.trim(),
    images: imageUrls,
    videos: videoUrls,
  })

  isSubmitting.value = false

  if (result) {
    error.value = result
    return
  }

  mediaItems.value = []
  objectUrls.value = []
  router.push('/')
}

onUnmounted(() => {
  // Revoke any remaining object URLs if the user navigates away without submitting
  objectUrls.value.forEach((url) => URL.revokeObjectURL(url))
})
</script>

<template>
  <main class="post-idea">
    <section class="header-section">
      <h1 class="page-title">Post a Partnership Idea</h1>
      <p class="page-subtitle">
        Tell other companies about your partnership idea to discover new opportunities.
      </p>
    </section>

    <form class="idea-form" @submit.prevent="submitIdea">
      <div class="form-group">
        <label class="form-label" for="companyName">Company Name</label>
        <input
          id="companyName"
          v-model="companyName"
          type="text"
          class="form-input"
          placeholder="Enter your company name..."
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="title">Partnership Idea Title</label>
        <input
          id="title"
          v-model="title"
          type="text"
          class="form-input"
          placeholder="Give your partnership idea a catchy title..."
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="description">Short Description</label>
        <textarea
          id="description"
          v-model="description"
          class="form-input form-textarea"
          placeholder="Briefly describe your partnership idea..."
          rows="3"
        ></textarea>
      </div>

      <div class="form-group">
        <label class="form-label" for="detailedDescription">Detailed Description</label>
        <textarea
          id="detailedDescription"
          v-model="detailedDescription"
          class="form-input form-textarea form-textarea-large"
          placeholder="Provide more details about your partnership idea, goals, and the types of partners you're looking to connect with..."
          rows="8"
        ></textarea>
      </div>

      <div class="form-group">
        <label class="form-label">Media Attachments</label>
        <div class="media-buttons">
          <button type="button" class="media-btn" @click="imageInput?.click()">
            Add Images
          </button>
          <button type="button" class="media-btn" @click="videoInput?.click()">
            Add Videos
          </button>
        </div>
        <input
          ref="imageInput"
          type="file"
          accept="image/jpeg,image/png,image/gif,image/webp"
          multiple
          hidden
          @change="onImagesSelected"
        />
        <input
          ref="videoInput"
          type="file"
          accept="video/mp4,video/webm,video/quicktime"
          multiple
          hidden
          @change="onVideosSelected"
        />
        <MediaPreview :items="mediaItems.map((item) => ({ url: item.url, type: item.type }))" @remove="removeMedia" />
      </div>

      <p v-if="error" class="form-error">{{ error }}</p>

      <button type="submit" class="submit-btn" :disabled="isSubmitting">
        {{ isSubmitting ? 'POSTING...' : 'POST IDEA' }}
      </button>
    </form>
  </main>
</template>

<style scoped>
.post-idea {
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
  margin: 0 auto;
  line-height: 1.5;
}

.idea-form {
  max-width: 560px;
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

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-textarea-large {
  min-height: 160px;
}

.media-buttons {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.media-btn {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-primary);
  background: var(--color-accent-bg);
  border: 1.5px solid var(--color-primary);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.media-btn:hover {
  background: var(--color-primary);
  color: white;
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
</style>
