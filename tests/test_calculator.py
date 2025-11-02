"""
Test cases for the CalorieCalculator class
"""
import pytest
from calculator import CalorieCalculator

def test_calculate_bmr():
    """Test BMR calculation for both male and female"""
    # Test male BMR calculation
    male_bmr = CalorieCalculator.calculate_bmr(
        weight_kg=70,
        height_cm=175,
        age=30,
        gender='male'
    )
    assert isinstance(male_bmr, float)
    assert male_bmr > 0
    
    # Test female BMR calculation
    female_bmr = CalorieCalculator.calculate_bmr(
        weight_kg=60,
        height_cm=165,
        age=30,
        gender='female'
    )
    assert isinstance(female_bmr, float)
    assert female_bmr > 0

def test_calculate_calorie_goal():
    """Test complete calorie goal calculation"""
    result = CalorieCalculator.calculate_calorie_goal(
        weight_kg=70,
        height_cm=175,
        age=30,
        gender='male',
        activity_level='moderately_active',
        starting_weight=70,
        goal_weight=65,
        weekly_goal=0.5
    )
    
    assert isinstance(result, dict)
    assert 'bmr' in result
    assert 'daily_calorie_goal' in result
    assert 'bmi' in result
    assert result['goal_type'] == 'weight_loss'

def test_calculate_macros():
    """Test macronutrient calculation"""
    macros = CalorieCalculator.calculate_macros(2000)
    
    assert isinstance(macros, dict)
    assert all(nutrient in macros for nutrient in ['carbs', 'protein', 'fat'])
    assert all(key in macros['carbs'] for key in ['grams', 'calories', 'percent'])