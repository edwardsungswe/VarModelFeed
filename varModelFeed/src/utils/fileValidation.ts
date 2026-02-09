const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const ACCEPTED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/quicktime']

const MAX_IMAGE_SIZE = 5 * 1024 * 1024 // 5MB
const MAX_VIDEO_SIZE = 50 * 1024 * 1024 // 50MB

export interface ValidationResult {
  valid: boolean
  error?: string
}

export function validateImageFile(file: File): ValidationResult {
  if (!ACCEPTED_IMAGE_TYPES.includes(file.type)) {
    return { valid: false, error: `Unsupported image type: ${file.type}. Accepted: JPG, PNG, GIF, WebP.` }
  }
  if (file.size > MAX_IMAGE_SIZE) {
    return { valid: false, error: `Image "${file.name}" exceeds the 5MB size limit.` }
  }
  return { valid: true }
}

export function validateVideoFile(file: File): ValidationResult {
  if (!ACCEPTED_VIDEO_TYPES.includes(file.type)) {
    return { valid: false, error: `Unsupported video type: ${file.type}. Accepted: MP4, WebM, MOV.` }
  }
  if (file.size > MAX_VIDEO_SIZE) {
    return { valid: false, error: `Video "${file.name}" exceeds the 50MB size limit.` }
  }
  return { valid: true }
}
