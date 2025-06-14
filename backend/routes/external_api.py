from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(
    prefix="/external",
    tags=["External API"]
)

ZEN_QUOTES_URL = "https://zenquotes.io/api/random"
WGER_URL = "https://wger.de/api/v2/exercise/"

@router.get("/motivation")
async def get_motivation():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ZEN_QUOTES_URL)
            response.raise_for_status()
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            return {"quote": quote, "author": author}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch quote: {str(e)}")


@router.get("/suggested-exercises")
async def get_suggested_exercises(muscle: str = Query(..., description="Muscle group, e.g. legs, abs, chest")):
    async with httpx.AsyncClient() as client:
        try:
            params = {
                "language": 2,  # English
                "limit": 20
            }
            response = await client.get(WGER_URL, params=params)
            response.raise_for_status()
            data = response.json()

            exercises = [
                {
                    "id": ex["id"],
                    "name": ex["name"],
                    "description": ex["description"]
                }
                for ex in data["results"]
                if muscle.lower() in ex["name"].lower()
            ]

            return {"muscle": muscle, "count": len(exercises), "exercises": exercises}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch exercises: {str(e)}")
