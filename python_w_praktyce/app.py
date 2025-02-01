from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Meal, MealProduct

# Inicjalizacja aplikacji
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)





# Strona główna - wyświetlanie wszystkich posiłków i produktów
@app.route('/')
def index():
    meals = Meal.query.all()
    products = Product.query.all()

    # Globalne podsumowanie dnia (dynamiczne obliczenia)
    total_calories = sum(meal.total_calories for meal in meals)
    total_protein = sum(meal.total_protein for meal in meals)
    total_fat = sum(meal.total_fat for meal in meals)
    total_carbs = sum(meal.total_carbs for meal in meals)



    return render_template(
        'index.html',
        meals=meals,
        products=products,
        total_calories=total_calories,
        total_protein=total_protein,
        total_fat=total_fat,
        total_carbs=total_carbs
    )

# Dodawanie produktu do bazy danych
@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    calories = request.form['calories']
    protein = request.form['protein']
    fat = request.form['fat']
    carbs = request.form['carbs']

    new_product = Product(name=product_name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('index'))


# Dodawanie produktu do posiłku
@app.route('/add_to_meal', methods=['POST'])
def add_to_meal():
    meal_id = request.form.get('meal_id', 1)
    product_id = request.form['product_id']
    grams = int(request.form.get('gramy', 0))

    # Sprawdzenie, czy wszystkie wymagane dane zostały przesłane
    if not meal_id or not product_id or not grams:
        return "Nie podano wszystkich wymaganych danych", 400

    try:
        grams = int(grams)
        if grams <= 0:
            return "Gramatura musi być większa niż 0", 400
    except ValueError:
        return "Nieprawidłowa wartość dla gramatury", 400

    # Pobieranie obiektów meal i product
    meal = Meal.query.get(meal_id)
    product = Product.query.get(product_id)


    if product is None:
        return "Produkt nie znaleziony", 404

    if meal is None:
        return "Posiłek nie znaleziony", 404

    existing_entry = MealProduct.query.filter_by(meal_id=meal.id, product_id=product.id).first()
    if existing_entry:
        return f"Produkt '{product.name}' jest już w posiłku '{meal.name}'. Cofnij, aby kontynuować", 400

    # Dodanie produktu do posiłku
    new_connection = MealProduct(meal_id=meal.id, product_id=product.id, grams=grams)
    db.session.add(new_connection)
    db.session.commit()

    return redirect(url_for('index'))


# Funkcja do dodania domyślnych posiłków do bazy danych
def add_default_meals():
    with app.app_context():
        meal1 = Meal(name="Śniadanie")
        meal2 = Meal(name="Obiad")
        meal3 = Meal(name="Kolacja")

        db.session.add(meal1)
        db.session.add(meal2)
        db.session.add(meal3)
        db.session.commit()

        print("Posiłki zostały dodane do bazy danych.")


# Edytowanie gramatury produktu w posiłku
@app.route('/edit_product_in_meal', methods=['POST'])
def edit_product_in_meal():
    meal_id = request.form['meal_id']
    product_id = request.form['product_id']
    new_grams = int(request.form['new_grams'])

    # Znalezienie odpowiedniego rekordu w MealProduct
    connection = MealProduct.query.filter_by(meal_id=meal_id, product_id=product_id).first()

    if not connection:
        return "Nie znaleziono produktu w posiłku.", 404

    connection.grams = new_grams
    db.session.commit()
    return redirect(url_for('index'))




# Usuwanie produktu z posiłku
@app.route('/remove_product_from_meal', methods=['POST'])
def remove_product_from_meal():
    meal_id = request.form['meal_id']
    product_id = request.form['product_id']

    # Znalezienie i usunięcie odpowiedniego rekordu w MealProduct
    connection = MealProduct.query.filter_by(meal_id=meal_id, product_id=product_id).first()

    if connection:
        db.session.delete(connection)
        db.session.commit()

    return redirect(url_for('index'))



if __name__ == '__main__':

    app.run(debug=True)

