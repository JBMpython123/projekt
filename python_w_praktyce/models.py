from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)

    meal_products = db.relationship('MealProduct', backref='product', lazy='dynamic')


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    meal_products = db.relationship('MealProduct', backref='meal', lazy=True)

    @property
    def total_calories(self):
        return sum((mp.product.calories * mp.grams / 100) for mp in self.meal_products)

    @property
    def total_protein(self):
        return sum((mp.product.protein * mp.grams / 100) for mp in self.meal_products)

    @property
    def total_fat(self):
        return sum((mp.product.fat * mp.grams / 100) for mp in self.meal_products)

    @property
    def total_carbs(self):
        return sum((mp.product.carbs * mp.grams / 100) for mp in self.meal_products)


class MealProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    grams = db.Column(db.Integer, nullable=False)

