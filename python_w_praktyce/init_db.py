from app import app, db
from models import Meal

def initialize_db():
    with app.app_context():
        db.create_all()

        if Meal.query.count() == 0:
            default_meals = ["Śniadanie", "Obiad", "Kolacja"]
            for meal_name in default_meals:
                meal = Meal(name=meal_name)
                db.session.add(meal)
            db.session.commit()
            print("Dodano domyślne posiłki.")

        print("Baza danych została zainicjalizowana.")

if __name__ == "__main__":
    initialize_db()
