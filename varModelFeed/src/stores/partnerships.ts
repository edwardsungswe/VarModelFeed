import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { type Partnership } from '@/types'
import { type User } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api'

export const usePartnershipsStore = defineStore('partnerships', () => {
  const partnerships = ref<Partnership[]>([])
  const isSignedIn = ref(false)
  const currentUser = ref<User | null>(null)

  const sortedPartnerships = computed(() =>
    [...partnerships.value].sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
    ),
  )

  async function login(email: string, password: string): Promise<string | null> {
    try {
      console.log('🔐 Login attempt:', { email, password })
      const url = `${API_BASE_URL}/user/login/`
      console.log('📍 API URL:', url)

      const payload = { email, password }
      console.log('📤 Request body:', payload)

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      console.log('📥 Response status:', response.status)
      const data = await response.json()
      console.log('📥 Response data:', data)

      if (response.status === 200) {
        console.log('✅ Login successful!')
        currentUser.value = {
          id: data.user_id,
          email: email,
          password: password,
          name: data.name,
        }
        isSignedIn.value = true
        return null
      } else if (response.status === 401) {
        console.log('❌ Unauthorized (401)')
        return 'Invalid email or password.'
      } else {
        console.log('⚠️ Unexpected status code:', response.status)
        return 'An error occurred. Please try again.'
      }
    } catch (error) {
      console.error('❌ Login error:', error)
      return 'Unable to connect to server. Please try again.'
    }
  }

  async function fetchPosts(): Promise<void> {
    try {
      console.log('Fetching posts from API...')
      const resp = await fetch(`${API_BASE_URL}/posts/`)
      if (!resp.ok) {
        console.warn('Failed to fetch posts:', resp.status)
        return
      }
      const body = await resp.json()
      const items = body.results ?? body
      // map server fields (snake_case) to frontend expected camelCase
      const mapped = (items as any[]).map((p) => ({
        id: p.id,
        companyName: p.company_name ?? p.companyName,
        logoPlaceholder: p.logo_placeholder ?? p.logoPlaceholder ?? '',
        title: p.title,
        description: p.description,
        detailedDescription: p.detailed_description ?? p.detailedDescription ?? '',
        images: p.images ?? [],
        videos: p.videos ?? [],
        createdAt: p.created_at ?? p.createdAt,
      }))
      partnerships.value = mapped
      console.log('Loaded posts:', partnerships.value.length)
    } catch (err) {
      console.error('Error fetching posts:', err)
    }
  }

  function logout() {
    currentUser.value = null
    isSignedIn.value = false
  }

  async function uploadMedia(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const resp = await fetch(`${API_BASE_URL}/media/upload/`, {
      method: 'POST',
      body: formData,
    })

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}))
      const message = body.detail ?? 'Failed to upload media.'
      throw new Error(message)
    }

    const body = await resp.json()
    return body.url as string
  }

  async function addPartnership(data: {
    companyName: string
    title: string
    description: string
    detailedDescription?: string
    images?: string[]
    videos?: string[]
  }): Promise<string | null> {
    if (!currentUser.value) {
      return 'You must be signed in to post.'
    }

    const logoPlaceholder = data.companyName
      .split(' ')
      .map((w) => w[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)

    try {
      const resp = await fetch(`${API_BASE_URL}/posts/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          author_id: currentUser.value.id,
          company_name: data.companyName,
          logo_placeholder: logoPlaceholder,
          title: data.title,
          description: data.description,
          detailed_description: data.detailedDescription ?? '',
          images: data.images ?? [],
          videos: data.videos ?? [],
        }),
      })

      if (!resp.ok) {
        const body = await resp.json().catch(() => ({}))
        console.error('Create post failed:', resp.status, body)
        return 'Failed to create post. Please try again.'
      }

      // refresh feed from server so the new post appears
      await fetchPosts()
      return null
    } catch (err) {
      console.error('Create post error:', err)
      return 'Unable to connect to server. Please try again.'
    }
  }

  function getPartnershipById(id: string): Partnership | undefined {
    return partnerships.value.find((p) => p.id === id)
  }

  // initialize feed
  fetchPosts()

  return {
    partnerships,
    isSignedIn,
    currentUser,
    sortedPartnerships,
    login,
    logout,
    uploadMedia,
    addPartnership,
    getPartnershipById,
    fetchPosts,
  }
})
