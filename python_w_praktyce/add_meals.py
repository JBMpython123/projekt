from app import app, db, Meal, Product, MealProduct

def add_product_to_meal(meal_name, product_id, grams):
    with app.app_context():
        meal = Meal.query.filter_by(name=meal_name).first()
        if not meal:
            print(f"Posiłek '{meal_name}' nie istnieje.")
            return

        product = Product.query.get(product_id)
        if not product:
            print(f"Produkt o ID {product_id} nie istnieje.")
            return

        connection = MealProduct.query.filter_by(meal_id=meal.id, product_id=product.id).first()
        if connection:
            print(f"Produkt '{product.name}' już istnieje w posiłku '{meal.name}'.")
        else:
            new_connection = MealProduct(meal_id=meal.id, product_id=product.id, grams=grams)
            db.session.add(new_connection)
            db.session.commit()
            print(f"Produkt '{product.name}' dodany do posiłku '{meal.name}' z ilością {grams}g.")

if __name__ == '__main__':
    produkty_do_dodania = [
        {"meal_name": "Śniadanie", "product_id": 1, "grams": 100},
        {"meal_name": "Obiad", "product_id": 2, "grams": 150},
        {"meal_name": "Kolacja", "product_id": 3, "grams": 200},
    ]

    with app.app_context():
        for item in produkty_do_dodania:
            add_product_to_meal(item["meal_name"], item["product_id"], item["grams"])

