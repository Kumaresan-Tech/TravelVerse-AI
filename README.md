# ✈️ TravelVerse — High-Level AI Travel Intelligence Platform

TravelVerse is a state-of-the-art, full-stack travel platform featuring live database persistence, custom AI trip generation, geospatial interactive map exploration, real-time budget tracking, and an extensive catalog of 35+ iconic tourist destinations.

---

## 🌟 Key Features

- **🌐 150+ Iconic World Destinations**: Fully populated database seeded with top global and regional tourist spots across Asia, Europe, Americas, Middle East, Africa, and Oceania.
- **🎯 Dynamic Filtering & Search**: Instant real-time filtering by experience categories (`Beaches`, `Mountains`, `Culture`, `Cities`, `Luxury`, `Romantic`, `Adventure`, `Nature`), rating, and search terms.
- **🗺️ Interactive Map Explorer (`/map`)**: Geospatial visual layout showing all destination pins with instant popup details and itinerary triggers.
- **✨ AI Trip Itinerary Planner (`/planner`)**: Generates multi-day customized travel plans with time slots, estimated costs, packing checklists, and local travel advice.
- **💼 My Saved Trips (`/trips`)**: Manage custom trip schedules, itinerary items, budget progress, and status filters with complete backend sync.
- **❤️ Instant Wishlist (`/wishlist`)**: Bookmark bucket list destinations with immediate local state feedback and database persistence.
- **🧮 Travel Budget Calculator (`/budget`)**: Expense estimation and category tracking.

---

## 🛠️ Architecture & Tech Stack

### **Backend**
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT & Passlib Password Hashing
- **API Endpoints**:
  - `/api/destinations` (Full catalog with category & search queries)
  - `/api/destinations/{id}` (Detailed destination metadata)
  - `/api/ai/generate` & `/api/ai/save` (AI Itinerary engine)
  - `/api/trips` (User trips & itinerary items CRUD)
  - `/api/wishlist` (Saved destinations CRUD)
  - `/api/expenses` (Trip expense management)

### **Frontend**
- **Framework**: Next.js 16 (App Router) + React 19 + TypeScript
- **Styling**: TailwindCSS 4, Custom CSS Design Tokens, Dynamic Glassmorphism, Responsive Grid System
- **Icons**: Lucide React

---

## 🚀 Quick Start & Production Running

### **1. Backend (FastAPI)**
```bash
cd backend
# Activate virtual environment
.\venv\Scripts\activate
# Start FastAPI server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation available at: `http://127.0.0.1:8000/docs`

### **2. Frontend (Next.js)**
```bash
cd frontend
# Install dependencies
npm install

# Run Development Server
npm run dev

# Or Run Production Build
npm run build
npm run start
```
Frontend Web App available at: `http://localhost:3000`

---

## 📂 Project Structure

```
TravelVerse/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Entrypoint & CORS setup
│   │   ├── seed.py            # Database Seeder (35+ Destinations)
│   │   ├── models/            # SQLAlchemy Database Models
│   │   ├── routes/            # REST API Routers (destinations, ai, trips, wishlist, auth)
│   │   └── schemas/           # Pydantic Request/Response Schemas
│   └── travelverse.db         # SQLite Database File
└── frontend/
    ├── app/                   # Next.js App Router Pages
    │   ├── page.tsx           # Hero Landing Page with Live Search
    │   ├── explore/           # Explore Catalog with Live Search & Pills
    │   ├── destinations/      # Full Catalog Grid & Filters
    │   ├── destinations/[id]/ # Single Destination Deep-Dive
    │   ├── planner/           # AI Itinerary Planner Wizard
    │   ├── map/               # Geospatial Map Explorer
    │   ├── trips/             # User Saved Trips Dashboard
    │   ├── wishlist/          # Saved Wishlist Page
    │   └── budget/            # Budget Calculator Page
    ├── components/            # Reusable Navigation & UI Components
    └── lib/                   # API Integration Client (`api.ts`)
```
