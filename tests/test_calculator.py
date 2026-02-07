"""
Basic tests for the calculator service
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.services.calculator_service import CalculatorService


def test_bmr_calculation():
    """Test BMR calculation"""
    calc = CalculatorService()
    
    # Test male BMR
    bmr_male = calc.calculate_bmr(weight=80, height=180, age=30, gender='male')
    assert 1700 < bmr_male < 1850, f"Expected BMR ~1780, got {bmr_male}"
    
    # Test female BMR
    bmr_female = calc.calculate_bmr(weight=60, height=165, age=25, gender='female')
    assert 1250 < bmr_female < 1400, f"Expected BMR ~1320, got {bmr_female}"
    
    print("✅ BMR calculation test passed")


def test_tdee_calculation():
    """Test TDEE calculation"""
    calc = CalculatorService()
    
    bmr = 1900
    
    # Test different activity levels
    tdee_sedentary = calc.calculate_tdee(bmr, 'sedentary')
    assert tdee_sedentary == 1900 * 1.2
    
    tdee_moderate = calc.calculate_tdee(bmr, 'moderate')
    assert tdee_moderate == 1900 * 1.55
    
    print("✅ TDEE calculation test passed")


def test_full_calculation():
    """Test full calculation with macros"""
    calc = CalculatorService()
    
    data = {
        'weight': 80,
        'height': 180,
        'age': 30,
        'gender': 'male',
        'activity_level': 'moderate',
        'goal': 'weight_loss',
        'weekly_goal': 0.5
    }
    
    result = calc.calculate_calories_and_macros(data)
    
    # Verify structure
    assert 'bmr' in result
    assert 'tdee' in result
    assert 'target_calories' in result
    assert 'macros' in result
    assert 'recommendations' in result
    
    # Verify values
    assert result['bmr'] > 0
    assert result['tdee'] > result['bmr']
    assert result['target_calories'] < result['tdee']  # weight loss
    
    # Verify macros structure
    assert 'protein' in result['macros']
    assert 'carbs' in result['macros']
    assert 'fats' in result['macros']
    
    print("✅ Full calculation test passed")
    print(f"   BMR: {result['bmr']} kcal")
    print(f"   TDEE: {result['tdee']} kcal")
    print(f"   Target: {result['target_calories']} kcal")
    print(f"   Protein: {result['macros']['protein']['grams']}g")


def test_macro_distribution():
    """Test macro distribution"""
    calc = CalculatorService()
    
    macros = calc.calculate_macros(calories=2000, weight=80, goal='weight_loss')
    
    # Calculate total calories from macros
    total_cal = (
        macros['protein']['grams'] * 4 +
        macros['carbs']['grams'] * 4 +
        macros['fats']['grams'] * 9
    )
    
    # Should be close to target (within 100 kcal due to rounding)
    assert abs(total_cal - 2000) < 100, f"Macro calories {total_cal} don't match target 2000"
    
    print("✅ Macro distribution test passed")


def run_all_tests():
    """Run all tests"""
    print("Running calculator service tests...\n")
    
    try:
        test_bmr_calculation()
        test_tdee_calculation()
        test_full_calculation()
        test_macro_distribution()
        
        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
