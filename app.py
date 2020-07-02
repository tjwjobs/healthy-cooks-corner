import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'healthy_cooks'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-m5hxw.mongodb.net/healthy_cooks?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html",
                           recipes=mongo.db.recipes.find())


@app.route('/add_recipe')
def add_recipe():
    return render_template(
        'addrecipe.html',  meal_types=mongo.db.meal_types.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    meal_types = mongo.db.meal_types.find()
    return render_template('editrecipe.html', recipe=recipes,
                           meal_types=meal_types)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
                 {
        'name': request.form.get('name'),
        'meal_type': request.form.get('meal_type'),
        'description': request.form.get('description'),
        'is_vegan': request.form.get('is_vegan')
    })
    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipes_id)})
    return redirect(url_for('get_recipes'))

@app.route('/get_mealtype')
def get_mealtype():
    return render_template('mealtype.html',
                           mealtypes=mongo.db.meal_types.find())

@app.route('/construction')
def construction():
    return render_template(
        'construction.html')

@app.route('/login')
def login():
    return render_template(
        'login.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)