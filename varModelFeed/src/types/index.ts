export interface Partnership {
  id: string
  companyName: string
  logoPlaceholder: string
  title: string
  description: string
  detailedDescription: string
  images: string[]
  videos: string[]
  createdAt: string
}

export interface User {
  id: string
  email: string
  password: string
  name: string
}
