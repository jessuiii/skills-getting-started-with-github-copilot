"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team-based soccer practice and weekend matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, technique drills, and friendly swim meets",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu"]
    },
    "Painting Studio": {
        "description": "Explore painting styles, color theory, and gallery-quality work",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu"]
    },
    "Drama Workshop": {
        "description": "Acting exercises, script reading, and stage performance skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for academic competitions in physics, chemistry, and biology",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu"]
    },
    "Debate Club": {
        "description": "Build public speaking, argumentation, and critical thinking skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email and validate
    normalized_email = email.strip().lower()

    # Prevent duplicate signups
    if normalized_email in [p.strip().lower() for p in activity.get("participants", [])]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Prevent over-capacity
    max_participants = activity.get("max_participants")
    if isinstance(max_participants, int) and len(activity.get("participants", [])) >= max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity.setdefault("participants", []).append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()
    participants = activity.get("participants", [])
    normalized_participants = [p.strip().lower() for p in participants]

    if normalized_email not in normalized_participants:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    participants.pop(normalized_participants.index(normalized_email))
    return {"message": f"Removed {normalized_email} from {activity_name}"}
