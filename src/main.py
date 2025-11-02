"""
YAZIO Calorie Calculator using Mifflin-St Jeor Equation
Main module containing the Flask application
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from calculator import CalorieCalculator

app = Flask(__name__)
CORS(app)

# API Routes
@app.route('/')
def home():
    """API information endpoint"""
    return jsonify({
        'api': 'YAZIO Calorie Calculator',
        'version': '2.0',
        'endpoints': {
            '/calculate': 'POST - Calculate calorie goal',
            '/calculate-bmr': 'POST - Calculate BMR only',
            '/activity-factors': 'GET - Get activity factor values',
            '/health': 'GET - API health check'
        },
        'method': 'Mifflin-St Jeor Equation',
        'note': 'Uses the same formula as YAZIO official calculator'
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/activity-factors', methods=['GET'])
def get_activity_factors():
    """Get available activity factors"""
    return jsonify({
        'activity_factors': CalorieCalculator.ACTIVITY_FACTORS,
        'aliases': CalorieCalculator.ACTIVITY_ALIASES,
        'description': {
            'sedentary': 'Lightly active - Mostly sitting during the day (office work) - 1.2',
            'lightly_active': 'Moderately active - Mostly standing during the day (teacher, cashier) - 1.375',
            'moderately_active': 'Active - Mostly walking during the day (sales rep, server) - 1.55',
            'active': 'Very Active - Physically demanding job (builder, construction) - 1.725',
            'very_active': 'Extremely active - Very intense physical activity daily - 1.9'
        }
    })

@app.route('/calculate-bmr', methods=['POST'])
def calculate_bmr_only():
    """Calculate BMR only using Mifflin-St Jeor Equation"""
    try:
        data = request.get_json()
        required = ['weight_kg', 'height_cm', 'age', 'gender']
        missing = [field for field in required if field not in data]
        
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        bmr = CalorieCalculator.calculate_bmr(
            weight_kg=float(data['weight_kg']),
            height_cm=float(data['height_cm']),
            age=int(data['age']),
            gender=data['gender']
        )
        
        return jsonify({
            'bmr': bmr,
            'unit': 'calories/day',
            'method': 'Mifflin-St Jeor Equation'
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate_calorie_goal():
    """Calculate complete calorie goal using Mifflin-St Jeor Equation"""
    try:
        data = request.get_json()
        required = ['weight_kg', 'height_cm', 'age', 'gender', 'activity_level',
                   'starting_weight', 'goal_weight', 'weekly_goal']
        missing = [field for field in required if field not in data]
        
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        if data['gender'].lower() not in ['male', 'female']:
            return jsonify({'error': 'Gender must be "male" or "female"'}), 400
        
        activity = data['activity_level'].lower()
        valid_activities = list(CalorieCalculator.ACTIVITY_FACTORS.keys()) + list(CalorieCalculator.ACTIVITY_ALIASES.keys())
        if activity not in valid_activities:
            return jsonify({
                'error': f'Activity level must be one of: {", ".join(valid_activities)}'
            }), 400
        
        result = CalorieCalculator.calculate_calorie_goal(
            weight_kg=float(data['weight_kg']),
            height_cm=float(data['height_cm']),
            age=int(data['age']),
            gender=data['gender'],
            activity_level=data['activity_level'],
            starting_weight=float(data['starting_weight']),
            goal_weight=float(data['goal_weight']),
            weekly_goal=float(data['weekly_goal'])
        )
        
        macros = CalorieCalculator.calculate_macros(
            calorie_goal=result['daily_calorie_goal'],
            carb_percent=data.get('carb_percent', 50),
            protein_percent=data.get('protein_percent', 20),
            fat_percent=data.get('fat_percent', 30)
        )
        
        warnings = []
        if result['bmi'] > 30:
            warnings.append('BMI > 30: Consider consulting with a healthcare provider.')
        if result['bmi'] < 18.5:
            warnings.append('BMI < 18.5: Consider consulting with a healthcare provider.')
        if result['daily_calorie_goal'] < result['bmr']:
            warnings.append('WARNING: Calorie goal is below BMR. This may not be sustainable or healthy.')
        
        weight_diff = result['weight_difference']
        if weight_diff > 0:
            goal_display = f"-{abs(data['weekly_goal'])} kg/week (weight loss)"
        elif weight_diff < 0:
            goal_display = f"+{abs(data['weekly_goal'])} kg/week (weight gain)"
        else:
            goal_display = "Maintain weight"
        
        response = {
            'success': True,
            'calculation': result,
            'macronutrients': macros,
            'recommendations': {
                'daily_calorie_goal': round(result['daily_calorie_goal']),
                'maintenance_calories': round(result['tdee']),
                'weekly_goal': goal_display,
                'estimated_time_to_goal': calculate_time_to_goal(
                    result['weight_difference'], 
                    data['weekly_goal']
                )
            },
            'warnings': warnings if warnings else None,
            'method': 'Mifflin-St Jeor Equation',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_time_to_goal(weight_difference, weekly_goal):
    """Calculate estimated time to reach goal weight"""
    if weight_difference == 0 or weekly_goal == 0:
        return "Maintaining current weight"
    
    weeks = abs(weight_difference / weekly_goal)
    
    if weeks < 1:
        return "Less than 1 week"
    elif weeks < 4:
        return f"Approximately {round(weeks)} weeks"
    else:
        months = weeks / 4.33
        return f"Approximately {round(months, 1)} months"

if __name__ == '__main__':
    print("🚀 Starting YAZIO Calorie Calculator API...")
    print("📊 Using Mifflin-St Jeor Equation (Official YAZIO Method)")
    print("🌐 API running on http://localhost:5000")
    print("\nActivity Levels:")
    print("  - sedentary/low: 1.2 (lightly active - mostly sitting)")
    print("  - lightly_active: 1.375 (moderately active - mostly standing)")
    print("  - moderately_active/moderate: 1.55 (active - mostly walking)")
    print("  - active/high: 1.725 (very active - physical work)")
    print("  - very_active/very_high: 1.9 (extremely active - intense activity)")
    print("\nAvailable endpoints:")
    print("  GET  / - API information")
    print("  GET  /health - Health check")
    print("  GET  /activity-factors - View activity factors")
    print("  POST /calculate-bmr - Calculate BMR only")
    print("  POST /calculate - Calculate complete calorie goal")
    app.run(debug=True, host='0.0.0.0', port=5000)