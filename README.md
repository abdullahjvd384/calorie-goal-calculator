# 🍏 Calorie Goal Calculator API

A professional Flask-based API for calculating daily calorie goals using the **Mifflin-St Jeor Equation** - the official YAZIO calculation method. This calculator helps determine optimal daily calorie intake based on various factors including BMR (Basal Metabolic Rate), activity level, and weight goals.

## ✨ Features

- Calculate BMR using Mifflin-St Jeor Equation (most accurate formula)
- Determine daily calorie needs based on activity level
- Calculate calorie goals for weight loss/gain
- Provide macronutrient distribution
- BMI calculation and health warnings
- RESTful API with detailed documentation
- 5% more accurate than Harris-Benedict Formula

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
    "weight_kg": 80,
    "height_cm": 180,
    "age": 29,
    "gender": "male",
    "activity_level": "moderate",
    "starting_weight": 80,
    "goal_weight": 85,
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

The API uses the **Mifflin-St Jeor Equation** for BMR calculation, which is the most current and accurate formula (5% more accurate than Harris-Benedict):

### For Men:
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5

### For Women:
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161

### Activity Factors:
- **Low**: 1.25
- **Moderate**: 1.38
- **High**: 1.52
- **Very High**: 1.65
- **Default (new users)**: 1.36 (male) / 1.33 (female)

### Energy Difference Formula:
Energy difference = (Weight difference × 750) ÷ (Weight difference ÷ Weekly goal)

- For weight loss of 0.5 kg/week: 375 calories deficit
- For weight loss of 1 kg/week: 750 calories deficit

### Complete Formula:
**Calorie Goal = (BMR × Activity Factor) + Energy Difference**

## 📖 Example Calculation

**John Smith:**
- Weight: 80 kg
- Height: 180 cm
- Age: 29
- Activity Level: Moderate (1.38)
- Goal Weight: 85 kg

**Calculation:**
1. BMR = (10 × 80) + (6.25 × 180) - (5 × 29) + 5 = **1,785 Cal**
2. Maintain weight = 1,785 × 1.38 = **2,463.3 Cal**
3. Energy difference = (-5 × 750) ÷ (-5 ÷ 0.5) = **375 Cal**
4. **Final Calorie Goal = 1,785 × 1.38 + 375 = 2,838.3 Cal**

## 📄 License

MIT License

## 👤 Author

Abdullah Javed

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!