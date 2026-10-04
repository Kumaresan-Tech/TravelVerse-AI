from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.auth import get_current_user_optional

router = APIRouter()

class AIRequest(BaseModel):
    destination: str
    days: int = 3
    travelers: int = 1
    budget: float = 1000.0
    style: str = "Adventure"
    interests: Optional[List[str]] = []

@router.post("/itinerary")
def generate_ai_itinerary(req: AIRequest, db: Session = Depends(get_db)):
    dest_input = req.destination.strip() or "Bali"
    days_count = max(1, min(14, req.days))
    daily_budget = req.budget / days_count if days_count > 0 else 200.0

    # Query database for exact or fuzzy destination match
    dest_obj = db.query(models.Destination).filter(
        (models.Destination.name.ilike(f"%{dest_input}%")) |
        (models.Destination.country.ilike(f"%{dest_input}%"))
    ).first()

    place_name = dest_obj.name if dest_obj else dest_input
    country_name = dest_obj.country if dest_obj else "Global Spot"

    # Extract real location highlights if available
    highlights = []
    if dest_obj and dest_obj.highlights:
        highlights = [h.strip() for h in dest_obj.highlights.split(",") if h.strip()]

    # Location specific activities mapping
    landmark_activities = {
        "Ooty": [
            [
                ("06:30 AM", "Sunrise View at Doddabetta Peak (2,637m Peak Elevation)", 0.20, "Doddabetta Peak Viewpoint"),
                ("10:00 AM", "UNESCO Heritage Toy Train Ride on Nilgiri Mountain Railway", 0.25, "Ooty Station to Coonoor"),
                ("02:00 PM", "Lush Tea Plantation Estate Walk & Homemade Chocolate Tasting", 0.25, "Doddabetta Tea Factory"),
                ("05:30 PM", "Ooty Lake Paddle Boating & Government Botanical Garden Stroll", 0.30, "Ooty Lake & Gardens")
            ],
            [
                ("08:00 AM", "Pykara Lake Speedboating & Pykara Waterfalls Hike", 0.25, "Pykara Lake Dam"),
                ("11:30 AM", "Avalanche Lake Pine Forest Trek & Photography", 0.25, "Avalanche Valley Sanctuary"),
                ("03:30 PM", "Rose Garden & Wax Planet Museum Tour", 0.20, "Government Rose Garden"),
                ("07:00 PM", "Cozy Nilgiri Mountain Cafe Dining & Fresh Baked Pastries", 0.30, "Ooty Commercial Road")
            ],
            [
                ("08:30 AM", "Emerald Lake Panoramic Valley Walk", 0.25, "Emerald Village Hill"),
                ("12:00 PM", "Needle Rock Viewpoint Cliff Edge Walk", 0.25, "Gudalur Nilgiri Range"),
                ("04:00 PM", "Stone House (First Bungalow of Ooty) & Toda Tribal Huts Visit", 0.25, "Stone House Hill"),
                ("07:30 PM", "Fireside Bonfire & Local South Indian Nilgiri Thali Dinner", 0.25, "Ooty Hill Resort")
            ]
        ],
        "Munnar": [
            [
                ("07:30 AM", "Sunrise Trek at Kolukkumalai Tea Estate (Highest Tea Garden)", 0.25, "Kolukkumalai Peak"),
                ("11:00 AM", "Eravikulam National Park Safari & Endangered Nilgiri Tahr Spotting", 0.25, "Rajamala Hills"),
                ("03:00 PM", "Mattupetty Dam Speedboating & Echo Point Call", 0.25, "Mattupetty Lake"),
                ("07:00 PM", "Traditional Kerala Ayurvedic Spa & Spiced Dinner", 0.25, "Munnar Town")
            ]
        ],
        "Taj Mahal": [
            [
                ("06:00 AM", "Sunrise View of Taj Mahal Marble Monument", 0.20, "Taj Mahal Yamuna Gate"),
                ("10:30 AM", "Agra Fort & Mughal Architecture Walking Tour", 0.25, "Agra Fort Complex"),
                ("02:00 PM", "Authentic Mughlai Cuisine Lunch & Marble Inlay Workshop", 0.25, "Sadak Bazaar"),
                ("05:30 PM", "Mehtab Bagh Sunset Reflection View of Taj Mahal", 0.30, "Mehtab Bagh Gardens")
            ]
        ],
        "Bali": [
            [
                ("07:30 AM", "Ubud Tegallalang Rice Terrace Trek & Jungle Swing", 0.20, "Ubud Valley"),
                ("11:30 AM", "Sacred Monkey Forest Sanctuary Walk", 0.20, "Ubud Center"),
                ("03:30 PM", "Tanah Lot Sea Temple Cliff Walk", 0.25, "Tanah Lot Coast"),
                ("07:00 PM", "Jimbaran Bay Seafood Candlelight Dinner on Beach", 0.35, "Jimbaran Beach")
            ]
        ],
        "Paris": [
            [
                ("09:00 AM", "Eiffel Tower Summit Access & Seine River Cruise", 0.30, "Champ de Mars"),
                ("01:00 PM", "Louvre Museum Guided Mona Lisa & Masterpiece Tour", 0.25, "Louvre Palace"),
                ("04:30 PM", "Montmartre Artist Quarter Walk & Sacré-Cœur View", 0.20, "Montmartre Hill"),
                ("08:00 PM", "French Bistro Wine & Cheese Tasting Dinner", 0.25, "Le Marais District")
            ]
        ],
        "Tokyo": [
            [
                ("08:30 AM", "Senso-ji Temple Walk & Nakamise Shopping Street", 0.15, "Asakusa District"),
                ("11:30 AM", "Shibuya Scramble Crossing & Shibuya Sky View Deck", 0.25, "Shibuya Center"),
                ("03:00 PM", "Akihabara Electric Town & Anime Tech Experience", 0.25, "Akihabara"),
                ("07:30 PM", "Shinjuku Omoide Yokocho Ramen & Yakitori Tasting", 0.35, "Shinjuku Alley")
            ]
        ],
        "Dubai": [
            [
                ("09:30 AM", "Burj Khalifa At The Top 124th Floor View", 0.30, "Downtown Dubai"),
                ("01:30 PM", "Dubai Mall Aquarium & Fountain Show", 0.20, "Dubai Mall"),
                ("04:30 PM", "4x4 Desert Safari, Dune Bashing & Camel Ride", 0.30, "Lahbab Red Dunes"),
                ("08:30 PM", "Bedouin Camp Barbecue Dinner & Fire Show", 0.20, "Desert Camp")
            ]
        ],
        "Swiss Alps": [
            [
                ("08:00 AM", "Matterhorn Glacier Paradise Cable Car Ride", 0.35, "Zermatt Station"),
                ("12:00 PM", "Alpine Fondue Lunch in Mountain Chalet", 0.25, "Gornergrat Peak"),
                ("03:30 PM", "Scenic Glacier Express Mountain Train Journey", 0.25, "Glacier Route"),
                ("07:30 PM", "Stargazing & Cozy Fireside Dinner", 0.15, "Zermatt Alpine Lodge")
            ]
        ]
    }

    # Match landmark activities or build real dynamic multi-day plans
    day_activity_sets = None
    for k in landmark_activities:
        if k.lower() in place_name.lower() or place_name.lower() in k.lower():
            day_activity_sets = landmark_activities[k]
            break

    category_name = dest_obj.category if dest_obj else "Mountains"

    days_list = []
    for d in range(1, days_count + 1):
        if day_activity_sets:
            # Cycle through day activity sets
            acts_template = day_activity_sets[(d - 1) % len(day_activity_sets)]
        else:
            # Dynamically synthesize real-time plans based on category and highlights
            h1 = highlights[0] if len(highlights) > 0 else f"{place_name} Mountain Trail"
            h2 = highlights[1] if len(highlights) > 1 else f"{place_name} Valley Viewpoint"
            h3 = highlights[2] if len(highlights) > 2 else f"Local {place_name} Heritage Site"

            if category_name.lower() == "mountains":
                acts_template = [
                    ("07:00 AM", f"Day {d} Morning Mountain Mist Hike & Sunrise Point ({h1})", 0.25, f"{place_name} Summit Point"),
                    ("11:00 AM", f"Pine Forest & Scenic Valley Walk ({h2})", 0.25, f"{place_name} Mountain Ridge"),
                    ("03:30 PM", f"Local Mountain Craft Village & Tea Tasting ({h3})", 0.25, f"{place_name} Heritage Market"),
                    ("07:30 PM", f"Fireside Alpine Dining & Local Mountain Cuisine", 0.25, f"{place_name} Valley Resort")
                ]
            else:
                acts_template = [
                    ("08:30 AM", f"Morning Exploration: {h1}", 0.25, f"{place_name} Central Area"),
                    ("12:00 PM", f"Authentic Regional Lunch & Culture: {h2}", 0.20, f"{place_name} Square"),
                    ("03:30 PM", f"Afternoon Scenic Highlight: {h3}", 0.30, f"{place_name} Viewpoint"),
                    ("07:30 PM", f"Evening Dining & Sunset Experience in {place_name}", 0.25, f"{place_name} Waterfront")
                ]

        day_acts = []
        for time_slot, title, cost_pct, loc in acts_template:
            cost = round(daily_budget * cost_pct, 2)
            day_acts.append({
                "time": time_slot,
                "activity": title,
                "cost": cost,
                "location": loc
            })

        days_list.append({
            "day": d,
            "title": f"Day {d}: Exploring {place_name}, {country_name} ({req.style} Mountain Experience)",
            "location": place_name,
            "activities": day_acts
        })

    packing_checklist = [
        f"Valid Passport / ID & Visa Documents for {country_name}",
        "Universal Power Adapter & Power Bank",
        "Comfortable Walking / Trekking Shoes",
        "Weather-appropriate Apparel (Layered Clothing)",
        "Sunscreen, Sunglasses & Personal First Aid Kit"
    ]

    local_tips = [
        f"Early morning (7:00 AM - 9:00 AM) is best to avoid crowds at top attractions in {place_name}.",
        f"Use local currency or digital payments accepted in {country_name}.",
        f"Download offline maps via TravelVerse Map Explorer for {place_name} before departure."
    ]

    return {
        "destination": place_name,
        "country": country_name,
        "days_count": days_count,
        "travelers": req.travelers,
        "total_budget": req.budget,
        "travel_style": req.style,
        "days": days_list,
        "packing_checklist": packing_checklist,
        "local_tips": local_tips,
        "ai_generated": True
    }

@router.post("/save-trip", response_model=schemas.Trip)
def save_ai_itinerary_as_trip(
    req_data: dict,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else 1
    
    dest_name = req_data.get("destination", "Custom Trip")
    days_count = req_data.get("days_count", 3)
    budget = req_data.get("total_budget", 1000.0)
    style = req_data.get("travel_style", "Adventure")
    travelers = req_data.get("travelers", 1)

    dest_obj = db.query(models.Destination).filter(models.Destination.name.ilike(f"%{dest_name}%")).first()
    image_url = dest_obj.image_url if dest_obj else "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"

    trip = models.Trip(
        user_id=user_id,
        name=f"AI Trip: {dest_name}",
        destination=dest_name,
        start_date="2026-11-01",
        end_date=f"2026-11-0{min(9, days_count + 1)}",
        travelers=travelers,
        budget=budget,
        travel_style=style,
        status="Upcoming",
        image_url=image_url
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    days = req_data.get("days", [])
    for d in days:
        day_num = d.get("day", 1)
        for act in d.get("activities", []):
            item = models.ItineraryItem(
                trip_id=trip.id,
                day=day_num,
                time=act.get("time", "10:00 AM"),
                activity=act.get("activity", "Sightseeing"),
                location=act.get("location", dest_name),
                estimated_cost=act.get("cost", 50.0),
                notes=f"AI Generated activity for Day {day_num}"
            )
            db.add(item)
    
    db.commit()
    db.refresh(trip)
    return trip
