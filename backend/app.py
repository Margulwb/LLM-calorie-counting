"""
Flask Backend API for LLM Weight Loss Expert
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from services.llm_service import LLMService
from services.calculator_service import CalculatorService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
llm_service = LLMService()
calculator_service = CalculatorService()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'LLM Weight Loss Expert API',
        'version': '1.0.0'
    })


@app.route('/api/diet-expert', methods=['POST'])
def diet_expert():
    """
    Ask diet expert questions
    
    Request body:
    {
        "question": "Your question here",
        "context": {  # optional
            "weight": 80,
            "height": 180,
            "age": 30,
            "gender": "male",
            "activity_level": "moderate"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        question = data['question']
        context = data.get('context', {})
        
        # Get answer from LLM
        answer = llm_service.ask_expert(question, context)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meal-plan', methods=['POST'])
def generate_meal_plan():
    """
    Generate personalized meal plan
    
    Request body:
    {
        "calories": 2000,
        "protein": 150,
        "carbs": 200,
        "fats": 60,
        "meals": 3,  # number of meals per day
        "preferences": ["chicken", "rice", "vegetables"],  # optional
        "restrictions": ["lactose"]  # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'calories' not in data:
            return jsonify({'error': 'Calories are required'}), 400
        
        meal_plan = llm_service.generate_meal_plan(data)
        
        return jsonify({
            'meal_plan': meal_plan,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-deficit', methods=['POST'])
def calculate_deficit():
    """
    Calculate caloric deficit and macros
    
    Request body:
    {
        "weight": 80,  # kg
        "height": 180,  # cm
        "age": 30,
        "gender": "male",  # male or female
        "activity_level": "moderate",  # sedentary, light, moderate, high, very_high
        "goal": "weight_loss",  # weight_loss, maintenance, muscle_gain
        "weekly_goal": 0.5  # kg per week (for weight_loss)
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['weight', 'height', 'age', 'gender', 'activity_level']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        result = calculator_service.calculate_calories_and_macros(data)
        
        return jsonify({
            'calculations': result,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/workout-plan', methods=['POST'])
def generate_workout_plan():
    """
    Generate workout plan (strength/cardio)
    
    Request body:
    {
        "goal": "weight_loss",  # weight_loss, muscle_gain, general_fitness
        "experience": "beginner",  # beginner, intermediate, advanced
        "days_per_week": 3,
        "duration": 60,  # minutes per session
        "type": "both"  # strength, cardio, both
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'goal' not in data:
            return jsonify({'error': 'Goal is required'}), 400
        
        workout_plan = llm_service.generate_workout_plan(data)
        
        return jsonify({
            'workout_plan': workout_plan,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-progress', methods=['POST'])
def analyze_progress():
    """
    Analyze progress and provide recommendations
    
    Request body:
    {
        "current_weight": 80,
        "starting_weight": 85,
        "goal_weight": 75,
        "weeks_elapsed": 4,
        "calories": 2000,
        "activity": "moderate",
        "issue": "weight_plateau"  # optional: weight_plateau, slow_progress, too_fast
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['current_weight', 'starting_weight', 'weeks_elapsed']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        analysis = llm_service.analyze_progress(data)
        
        return jsonify({
            'analysis': analysis,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Starting LLM Weight Loss Expert API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
