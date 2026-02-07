"""
Calculator Service for BMR, TDEE, and Macros Calculations
"""


class CalculatorService:
    
    # Activity level multipliers
    ACTIVITY_MULTIPLIERS = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'high': 1.725,
        'very_high': 1.9
    }
    
    def calculate_bmr(self, weight, height, age, gender):
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        
        Args:
            weight (float): Weight in kg
            height (float): Height in cm
            age (int): Age in years
            gender (str): 'male' or 'female'
            
        Returns:
            float: BMR in kcal
        """
        # Mifflin-St Jeor Equation
        bmr = (10 * weight) + (6.25 * height) - (5 * age)
        
        if gender.lower() == 'male':
            bmr += 5
        else:  # female
            bmr -= 161
            
        return round(bmr, 1)
    
    def calculate_tdee(self, bmr, activity_level):
        """
        Calculate Total Daily Energy Expenditure
        
        Args:
            bmr (float): Basal Metabolic Rate
            activity_level (str): Activity level key
            
        Returns:
            float: TDEE in kcal
        """
        multiplier = self.ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.2)
        tdee = bmr * multiplier
        return round(tdee, 1)
    
    def calculate_calories_and_macros(self, data):
        """
        Calculate calories and macronutrients based on user data
        
        Args:
            data (dict): User data including weight, height, age, gender, 
                        activity_level, goal, and optionally weekly_goal
                        
        Returns:
            dict: Calculations including BMR, TDEE, target calories, and macros
        """
        weight = data['weight']
        height = data['height']
        age = data['age']
        gender = data['gender']
        activity_level = data['activity_level']
        goal = data.get('goal', 'weight_loss')
        
        # Calculate BMR and TDEE
        bmr = self.calculate_bmr(weight, height, age, gender)
        tdee = self.calculate_tdee(bmr, activity_level)
        
        # Calculate target calories based on goal
        if goal == 'weight_loss':
            weekly_goal = data.get('weekly_goal', 0.5)  # kg per week
            # 1 kg fat = ~7700 kcal deficit
            daily_deficit = (weekly_goal * 7700) / 7
            target_calories = tdee - daily_deficit
            
            # Safety checks
            min_calories = 1200 if gender.lower() == 'female' else 1500
            target_calories = max(target_calories, min_calories)
            
        elif goal == 'muscle_gain':
            # Surplus of 200-300 kcal for lean muscle gain
            target_calories = tdee + 250
            
        else:  # maintenance
            target_calories = tdee
        
        target_calories = round(target_calories, 1)
        
        # Calculate macros
        macros = self.calculate_macros(target_calories, weight, goal)
        
        # Calculate weekly expected change
        actual_deficit = tdee - target_calories
        weekly_change = (actual_deficit * 7) / 7700
        
        return {
            'bmr': bmr,
            'tdee': tdee,
            'target_calories': target_calories,
            'deficit': round(actual_deficit, 1) if goal == 'weight_loss' else 0,
            'surplus': round(tdee - target_calories, 1) if goal == 'muscle_gain' else 0,
            'macros': macros,
            'weekly_change': round(weekly_change, 2),
            'recommendations': self.get_recommendations(goal, weekly_change)
        }
    
    def calculate_macros(self, calories, weight, goal):
        """
        Calculate macronutrient distribution
        
        Args:
            calories (float): Target daily calories
            weight (float): Body weight in kg
            goal (str): Fitness goal
            
        Returns:
            dict: Protein, carbs, and fats in grams and percentages
        """
        if goal == 'weight_loss':
            # High protein to preserve muscle
            protein_g = weight * 2.2  # 2.2g per kg
            protein_cal = protein_g * 4
            protein_pct = 40
            
            # Moderate fat for hormones
            fat_pct = 25
            fat_cal = calories * (fat_pct / 100)
            fat_g = fat_cal / 9
            
            # Rest from carbs
            carb_pct = 35
            carb_cal = calories * (carb_pct / 100)
            carb_g = carb_cal / 4
            
        elif goal == 'muscle_gain':
            # High protein for muscle building
            protein_g = weight * 2.0
            protein_cal = protein_g * 4
            protein_pct = 30
            
            # Higher carbs for energy
            carb_pct = 45
            carb_cal = calories * (carb_pct / 100)
            carb_g = carb_cal / 4
            
            # Moderate fat
            fat_pct = 25
            fat_cal = calories * (fat_pct / 100)
            fat_g = fat_cal / 9
            
        else:  # maintenance
            protein_g = weight * 1.8
            protein_cal = protein_g * 4
            protein_pct = 30
            
            carb_pct = 40
            carb_cal = calories * (carb_pct / 100)
            carb_g = carb_cal / 4
            
            fat_pct = 30
            fat_cal = calories * (fat_pct / 100)
            fat_g = fat_cal / 9
        
        return {
            'protein': {
                'grams': round(protein_g, 1),
                'calories': round(protein_cal, 1),
                'percentage': protein_pct
            },
            'carbs': {
                'grams': round(carb_g, 1),
                'calories': round(carb_cal, 1),
                'percentage': carb_pct
            },
            'fats': {
                'grams': round(fat_g, 1),
                'calories': round(fat_cal, 1),
                'percentage': fat_pct
            }
        }
    
    def get_recommendations(self, goal, weekly_change):
        """
        Get recommendations based on goal and expected change
        
        Args:
            goal (str): Fitness goal
            weekly_change (float): Expected weekly weight change in kg
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        if goal == 'weight_loss':
            if weekly_change < 0.25:
                recommendations.append("⚠️ Bardzo powolna redukcja - rozważ zwiększenie deficytu o 100-200 kcal")
            elif weekly_change > 1.0:
                recommendations.append("⚠️ Zbyt szybka redukcja - ryzyko utraty mięśni. Zmniejsz deficyt.")
            else:
                recommendations.append("✅ Optymalne tempo redukcji (0.5-1 kg/tydzień)")
            
            recommendations.append("💪 Priorytet: trening siłowy 3-4x/tydzień (chroni mięśnie)")
            recommendations.append("🥩 Wysokie białko (2-2.2g/kg) - zapobiega utracie mięśni")
            recommendations.append("🚶 Dodatkowa aktywność: spacery 30-45 min dziennie")
            recommendations.append("💧 Nawodnienie: 2-3L wody dziennie")
            recommendations.append("😴 Sen: 7-9 godzin (kluczowy dla regeneracji)")
            
        elif goal == 'muscle_gain':
            recommendations.append("💪 Progresja obciążeń co tydzień - kluczowa dla wzrostu")
            recommendations.append("🥩 Białko: 2g/kg + rozkład równomierny w ciągu dnia")
            recommendations.append("🍚 Węglowodany przed i po treningu")
            recommendations.append("😴 Sen: 8-9 godzin (wzrost mięśni podczas snu)")
            recommendations.append("📊 Monitoruj: jeśli tyjesz >0.5kg/tydzień, zmniejsz kalorie")
            
        else:  # maintenance
            recommendations.append("⚖️ Utrzymanie wagi - monitoruj wagę co tydzień")
            recommendations.append("💪 Trening: utrzymaj regularność")
            recommendations.append("🥗 Zbilansowana dieta: 30/40/30 (P/C/F)")
            
        return recommendations
