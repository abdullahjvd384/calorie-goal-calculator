# 🍏 Calorie Goal Calculator API

A professional Flask-based API for calculating daily calorie goals using the Mifflin-St Jeor Equation. This calculator provides the same results as the official YAZIO calculator and helps determine optimal daily calorie intake based on various factors including BMR (Basal Metabolic Rate), activity level, and weight goals.

## ✨ Features

- Calculate BMR using Mifflin-St Jeor Equation (same as YAZIO)
- Determine daily calorie needs based on activity level
- Calculate calorie goals for weight loss/gain
- Provide macronutrient distribution
- BMI calculation and health warnings
- RESTful API with detailed documentation
- Matches YAZIO official calculator results exactly

## 🛠️ Technology Stack

- Python 3.8+
- Flask
- Flask-CORS
- Pytest for testing

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/abdullahjvd384/calorie-goal-calculator.git
cd calorie-goal-calculator
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Unix/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

The API will be available at `http://localhost:5000`

## 📝 API Endpoints

### GET /
- API information and available endpoints

### GET /health
- Health check endpoint

### GET /activity-factors
- List available activity factors and their descriptions

### POST /calculate-bmr
Calculate BMR only
```json
{
    "weight_kg": 70,
    "height_cm": 175,
    "age": 25,
    "gender": "male"
}
```

### POST /calculate
Calculate complete calorie goal
```json
{
    "weight_kg": 70,
    "height_cm": 175,
    "age": 25,
    "gender": "male",
    "activity_level": "moderate",
    "starting_weight": 70,
    "goal_weight": 65,
    "weekly_goal": 0.5,
    "carb_percent": 50,
    "protein_percent": 30,
    "fat_percent": 20
}
```

## 🧪 Running Tests

```bash
pytest tests/
```

## 📚 Documentation

The API uses the Mifflin-St Jeor Equation for BMR calculation, which is the same formula used by YAZIO:

### For Men:
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5

### For Women:
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161

### Activity Factors (matching YAZIO):
- Lightly Active (sedentary): 1.2 - Mostly sitting (e.g., office worker)
- Moderately Active (lightly_active): 1.375 - Mostly standing (e.g., teacher, cashier)
- Active (moderately_active): 1.55 - Mostly walking (e.g., sales, server)
- Very Active (active): 1.725 - Physically demanding job (e.g., builder)
- Extremely Active (very_active): 1.9 - Very intense physical activity

### Calorie Goal Calculation:
Daily Calorie Goal = (BMR × Activity Factor) ± Calorie Adjustment

For weight loss: Subtract 375 kcal per 0.5 kg/week goal
For weight gain: Add 375 kcal per 0.5 kg/week goal

## 📄 License

MIT License

## 👤 Author

Abdullah Javed

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!