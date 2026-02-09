# CLAUDE.md

## Project Overview

This repository contains the **frontend implementation** of a Feed experience.

The goal is to build a clean, intuitive UI that allows users to:

- View a feed of posts
- Create new posts
- Consume rich media content (images and videos)

For this version, the application uses **dummy / mocked data** to simulate real content.  
The architecture is intentionally designed so that the data layer can later be replaced with API calls to a backend service without significant refactoring.

---

## Scope and Assumptions

- This codebase is **frontend-only**
- No backend logic, database, or authentication is implemented here
- All feed data and post creation behavior is currently simulated
- API integration will be added in a future iteration

---

## Core UI Requirements

### 1. Feed View

- Display a feed of posts in chronological order (latest first)
- Each post may include:
  - Text content
  - Multiple images
  - Multiple videos
- Feed rendering should behave as if data is coming from an external API

### 2. Create Post

- Provide a **Post** button that opens a post creation flow
- Users can:
  - Enter text content
  - Select and preview multiple images and/or videos
- Submission should:
  - Validate supported file types
  - Validate file size limits
  - Simulate a successful post creation by updating the local feed state

### 3. Media Rendering

- Images:
  - Render directly in the feed
  - Support basic preview or gallery behavior
- Videos:
  - Play inline or via a modal
- Performance:
  - Lazy-load media where possible
  - Avoid blocking feed rendering

---

## Technology Stack

- **Framework:** Vue.js
- **Styling:** Flexible (Tailwind, CSS Modules, or standard CSS)
- **State Management:** Local state or lightweight store as needed

---

## Data Strategy (Current)

- Use static or mocked data to represent posts
- Simulate realistic API responses (IDs, timestamps, media arrays)
- Keep data structures aligned with what a backend API would return

Example (conceptual):

- Post ID
- Created timestamp
- Text content
- Media array (type, URL, metadata)

---

## Future API Integration (Not Implemented Here)

This frontend is designed to eventually:

- Fetch feed data from a backend API
- Submit new posts via API requests
- Handle loading, success, and error states from real network calls

**Do not implement API logic in this version.**  
Focus on clean boundaries so the data layer can be swapped later.

---

## Architectural Guidelines

- Separate UI components from data logic
- Avoid tightly coupling components to mocked data sources
- Treat mocked data as if it were asynchronous
- Keep components small and reusable

---

## Non-Goals (for This Repo)

- Backend integration
- Authentication and authorization
- Persistent storage
- Production-grade security
- Server-side rendering

---

## Code Quality Expectations

- Prioritize clarity and maintainability
- Components should be easy to refactor when API integration is added
- Handle empty, loading, and error states gracefully (even if simulated)
- Avoid over-engineering

---

## AI Collaboration Notes

When using AI tools:

- Do not introduce backend or database logic
- Do not assume authentication exists
- Keep data structures API-friendly
- Optimize for extensibility, not completeness

This frontend should feel “real” even though it runs entirely on mocked data.
