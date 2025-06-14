from fastapi import APIRouter, HTTPException, Query, FastAPI
import httpx


RAPIDAPI_KEY = "4d2489870bmsh762f34a99226f22p19844fjsn35fca53ddae2"
ZEN_QUOTES_URL = "https://zenquotes.io/api/random"
RAPIDAPI_HOST = "exercisedb.p.rapidapi.com"
BASE_URL = "https://exercisedb.p.rapidapi.com"

router = APIRouter(
    prefix="/external",
    tags=["External API"]
)


@router.get("/motivation")
async def get_motivation():
    async with httpx.AsyncClient() as client:
        response = await client.get(ZEN_QUOTES_URL)
        response.raise_for_status()
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return {"quote": quote, "author": author}


MUSCLE_GROUPS = {
    "legs": "lower legs",
    "abs": "abdominals",
    "chest": "chest",
    "back": "back",
    "biceps": "biceps",
    "triceps": "triceps",
}

@router.get("/suggested-exercises")
async def get_suggested_exercises(
    muscle: str = Query(..., description="Muscle group name: legs, abs, chest")
):
    muscle_name = MUSCLE_GROUPS.get(muscle.lower())
    if not muscle_name:
        raise HTTPException(status_code=404, detail=f"Muscle '{muscle}' not found")

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    url = f"{BASE_URL}/exercises/target/{muscle_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch exercises")
        exercises = response.json()

    result = [
        {
            "id": ex.get("id"),
            "name": ex.get("name"),
            "bodyPart": ex.get("bodyPart"),
            "equipment": ex.get("equipment"),
            "gifUrl": ex.get("gifUrl"),
            "instructions": ex.get("instructions", "No instructions provided")
        }
        for ex in exercises
    ]

    return {
        "muscle": muscle,
        "count": len(result),
        "exercises": result
    }


def create_external_api_router(app: FastAPI):
    app.include_router(router)