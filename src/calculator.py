"""
YAZIO Calorie Calculator core functionality
Contains the CalorieCalculator class with all calculation methods
"""

class CalorieCalculator:
    """
    YAZIO Calorie Calculator using Mifflin-St Jeor Equation
    Formula: Calorie Goal = (BMR × Activity Factor) + Energy Difference
    
    YAZIO uses the Mifflin-St Jeor equation, which is more accurate than Harris-Benedict
    """
    
    # Activity level factors (matching YAZIO exactly)
    ACTIVITY_FACTORS = {
        'sedentary': 1.2,        # Lightly active - Mostly sitting (office work)
        'lightly_active': 1.375, # Moderately active - Mostly standing (teacher, cashier)
        'moderately_active': 1.55, # Active - Mostly walking (sales, server)
        'active': 1.725,         # Very Active - Physical work (builder)
        'very_active': 1.9       # Extremely active - Very intense physical activity
    }
    
    # Aliases for common terms
    ACTIVITY_ALIASES = {
        'low': 'sedentary',
        'moderate': 'moderately_active',
        'high': 'active',
        'very_high': 'very_active'
    }
    
    @staticmethod
    def calculate_bmr(weight_kg, height_cm, age, gender):
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        This is the formula YAZIO uses for more accurate results
        
        Men: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
        Women: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161
        """
        if gender.lower() == 'male':
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
            
        return round(bmr, 2)
    
    @staticmethod
    def calculate_energy_difference(starting_weight, goal_weight, weekly_goal_kg):
        """Calculate energy difference for weight gain/loss"""
        weight_diff = starting_weight - goal_weight
        
        if weight_diff > 0:
            # Weight loss: need DEFICIT (negative)
            energy_diff = -abs(weekly_goal_kg) * 750
        elif weight_diff < 0:
            # Weight gain: need SURPLUS (positive)
            energy_diff = abs(weekly_goal_kg) * 750
        else:
            # Maintaining weight but might still want to adjust
            energy_diff = weekly_goal_kg * 750
        
        return round(energy_diff, 2)
    
    @staticmethod
    def calculate_calorie_goal(weight_kg, height_cm, age, gender, 
                              activity_level, starting_weight, goal_weight, 
                              weekly_goal):
        """Complete calorie goal calculation using Harris-Benedict Formula"""
        # Step 1: Calculate BMR
        bmr = CalorieCalculator.calculate_bmr(weight_kg, height_cm, age, gender)
        
        # Step 2: Get activity factor
        activity_key = CalorieCalculator.ACTIVITY_ALIASES.get(
            activity_level.lower(), 
            activity_level.lower()
        )
        activity_factor = CalorieCalculator.ACTIVITY_FACTORS.get(activity_key, 1.2)
        
        # Step 3: Calculate TDEE (maintenance calories)
        tdee = bmr * activity_factor
        
        # Step 4: Calculate energy difference
        energy_difference = CalorieCalculator.calculate_energy_difference(
            starting_weight, goal_weight, weekly_goal
        )
        
        # Step 5: Final calorie goal
        calorie_goal = tdee + energy_difference
        
        # Calculate BMI
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # Determine goal type
        weight_diff = starting_weight - goal_weight
        if weight_diff > 0:
            goal_type = "weight_loss"
        elif weight_diff < 0:
            goal_type = "weight_gain"
        else:
            goal_type = "maintain"
        
        return {
            'bmr': round(bmr, 2),
            'activity_factor': activity_factor,
            'tdee': round(tdee, 2),
            'energy_difference': round(energy_difference, 2),
            'daily_calorie_goal': round(calorie_goal, 2),
            'bmi': round(bmi, 2),
            'goal_type': goal_type,
            'weekly_goal_kg': weekly_goal,
            'weight_difference': round(weight_diff, 2)
        }
    
    @staticmethod
    def calculate_macros(calorie_goal, carb_percent=50, protein_percent=20, fat_percent=30):
        """Calculate macronutrient distribution"""
        carb_calories = calorie_goal * (carb_percent / 100)
        protein_calories = calorie_goal * (protein_percent / 100)
        fat_calories = calorie_goal * (fat_percent / 100)
        
        return {
            'carbs': {
                'grams': round(carb_calories / 4, 1),
                'calories': round(carb_calories, 1),
                'percent': carb_percent
            },
            'protein': {
                'grams': round(protein_calories / 4, 1),
                'calories': round(protein_calories, 1),
                'percent': protein_percent
            },
            'fat': {
                'grams': round(fat_calories / 9, 1),
                'calories': round(fat_calories, 1),
                'percent': fat_percent
            }
        }