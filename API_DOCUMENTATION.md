# API Documentation - LLM Weight Loss Expert

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Response:**
```json
{
    "status": "healthy",
    "service": "LLM Weight Loss Expert API",
    "version": "1.0.0"
}
```

---

### 2. Ask Diet Expert

**Endpoint:** `POST /api/diet-expert`

**Description:** Ask the AI diet expert any question about weight loss, nutrition, or training

**Request Body:**
```json
{
    "question": "Jak mogę przyspieszyć spalanie tłuszczu?",
    "context": {
        "weight": 80,
        "height": 180,
        "age": 30,
        "gender": "male",
        "activity_level": "moderate"
    }
}
```

**Parameters:**
- `question` (string, required): Your question
- `context` (object, optional): User context information
  - `weight` (number): Weight in kg
  - `height` (number): Height in cm
  - `age` (number): Age in years
  - `gender` (string): "male" or "female"
  - `activity_level` (string): Activity level

**Response:**
```json
{
    "question": "Jak mogę przyspieszyć spalanie tłuszczu?",
    "answer": "Aby przyspieszyć spalanie tłuszczu...",
    "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/diet-expert \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Ile białka powinienem jeść?",
    "context": {
      "weight": 80,
      "activity_level": "moderate"
    }
  }'
```

---

### 3. Calculate Caloric Deficit

**Endpoint:** `POST /api/calculate-deficit`

**Description:** Calculate BMR, TDEE, target calories, and macronutrients

**Request Body:**
```json
{
    "weight": 80,
    "height": 180,
    "age": 30,
    "gender": "male",
    "activity_level": "moderate",
    "goal": "weight_loss",
    "weekly_goal": 0.5
}
```

**Parameters:**
- `weight` (number, required): Weight in kg
- `height` (number, required): Height in cm
- `age` (number, required): Age in years
- `gender` (string, required): "male" or "female"
- `activity_level` (string, required): 
  - "sedentary" - No exercise
  - "light" - 1-3 days/week
  - "moderate" - 3-5 days/week
  - "high" - 6-7 days/week
  - "very_high" - 2x per day, physical job
- `goal` (string, optional): "weight_loss" (default), "maintenance", "muscle_gain"
- `weekly_goal` (number, optional): kg per week for weight loss (default: 0.5)

**Response:**
```json
{
    "calculations": {
        "bmr": 1905.0,
        "tdee": 2953.3,
        "target_calories": 2403.3,
        "deficit": 550.0,
        "macros": {
            "protein": {
                "grams": 176.0,
                "calories": 704.0,
                "percentage": 40
            },
            "carbs": {
                "grams": 210.3,
                "calories": 841.2,
                "percentage": 35
            },
            "fats": {
                "grams": 66.8,
                "calories": 600.8,
                "percentage": 25
            }
        },
        "weekly_change": 0.5,
        "recommendations": [
            "✅ Optymalne tempo redukcji (0.5-1 kg/tydzień)",
            "💪 Priorytet: trening siłowy 3-4x/tydzień",
            ...
        ]
    },
    "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/calculate-deficit \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 80,
    "height": 180,
    "age": 30,
    "gender": "male",
    "activity_level": "moderate",
    "goal": "weight_loss"
  }'
```

---

### 4. Generate Meal Plan

**Endpoint:** `POST /api/meal-plan`

**Description:** Generate a personalized daily meal plan

**Request Body:**
```json
{
    "calories": 2000,
    "protein": 150,
    "carbs": 200,
    "fats": 60,
    "meals": 3,
    "preferences": ["chicken", "rice", "vegetables"],
    "restrictions": ["lactose"]
}
```

**Parameters:**
- `calories` (number, required): Target daily calories
- `protein` (number, optional): Target protein in grams
- `carbs` (number, optional): Target carbohydrates in grams
- `fats` (number, optional): Target fats in grams
- `meals` (number, optional): Number of meals per day (default: 3)
- `preferences` (array, optional): Preferred foods
- `restrictions` (array, optional): Allergies or restrictions

**Response:**
```json
{
    "meal_plan": "POSIŁEK 1 - ŚNIADANIE (7:00)\n\nSkładniki:\n- Jajka 3 szt...",
    "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/meal-plan \
  -H "Content-Type: application/json" \
  -d '{
    "calories": 2000,
    "meals": 3
  }'
```

---

### 5. Generate Workout Plan

**Endpoint:** `POST /api/workout-plan`

**Description:** Generate a personalized workout plan

**Request Body:**
```json
{
    "goal": "weight_loss",
    "experience": "beginner",
    "days_per_week": 3,
    "duration": 60,
    "type": "both"
}
```

**Parameters:**
- `goal` (string, required): 
  - "weight_loss" - Focus on fat loss
  - "muscle_gain" - Focus on building muscle
  - "general_fitness" - Overall fitness
- `experience` (string, optional): "beginner", "intermediate", "advanced" (default: "beginner")
- `days_per_week` (number, optional): Training days per week (default: 3)
- `duration` (number, optional): Minutes per session (default: 60)
- `type` (string, optional): "strength", "cardio", "both" (default: "both")

**Response:**
```json
{
    "workout_plan": "PLAN TRENINGOWY - REDUKCJA WAGI...",
    "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/workout-plan \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "weight_loss",
    "experience": "beginner",
    "days_per_week": 3
  }'
```

---

### 6. Analyze Progress

**Endpoint:** `POST /api/analyze-progress`

**Description:** Analyze weight loss progress and get recommendations

**Request Body:**
```json
{
    "current_weight": 80,
    "starting_weight": 85,
    "goal_weight": 75,
    "weeks_elapsed": 4,
    "calories": 2000,
    "activity": "moderate",
    "issue": "weight_plateau"
}
```

**Parameters:**
- `current_weight` (number, required): Current weight in kg
- `starting_weight` (number, required): Starting weight in kg
- `weeks_elapsed` (number, required): Weeks since starting
- `goal_weight` (number, optional): Target weight in kg
- `calories` (number, optional): Current daily calories
- `activity` (string, optional): Activity level
- `issue` (string, optional): 
  - "weight_plateau" - Weight isn't changing
  - "slow_progress" - Too slow progress
  - "too_fast" - Losing too fast

**Response:**
```json
{
    "analysis": "ANALIZA POSTĘPÓW:\n\nAktualna sytuacja:...",
    "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/analyze-progress \
  -H "Content-Type: application/json" \
  -d '{
    "current_weight": 80,
    "starting_weight": 85,
    "weeks_elapsed": 4,
    "issue": "weight_plateau"
  }'
```

---

## Error Responses

All endpoints return error responses in this format:

```json
{
    "error": "Error message description",
    "status": "error"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Missing or invalid parameters
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding rate limiting middleware.

---

## Authentication

Currently no authentication is required. For production, consider adding API key authentication or OAuth2.

---

## CORS

CORS is enabled for all origins in development. For production, configure specific allowed origins.

---

## Testing with Python

```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Ask expert
response = requests.post('http://localhost:5000/api/diet-expert', json={
    'question': 'Ile białka powinienem jeść?',
    'context': {
        'weight': 80,
        'activity_level': 'moderate'
    }
})
print(response.json())

# Calculate deficit
response = requests.post('http://localhost:5000/api/calculate-deficit', json={
    'weight': 80,
    'height': 180,
    'age': 30,
    'gender': 'male',
    'activity_level': 'moderate',
    'goal': 'weight_loss'
})
print(response.json())
```

---

## Notes

1. **Ollama Dependency**: The API requires Ollama to be running with the Mistral model installed
2. **First Request**: The first request may take longer as it initializes the vector database
3. **Knowledge Base**: The RAG system uses documents from the `knowledge_base/` directory
4. **Vector Store**: ChromaDB persists embeddings in the `chroma_db/` directory
