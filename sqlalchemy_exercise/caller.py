from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Recipe, Chef

engine = create_engine('postgresql+psycopg2://postgres-user:56932957eH10@localhost:5432/sqlalchemy_exercise')
Session = sessionmaker(bind=engine)


def create_recipe(name: str, ingredients: str, instructions: str):
    with Session() as session:
        recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
        session.add(recipe)
        session.commit()


def update_recipe_by_name(name: str, new_name: str, new_ingredients: str, new_instructions: str):
    with Session() as session:
        recipe = session.query(Recipe).filter_by(name=name).first()
        recipe.name = new_name
        recipe.ingredients = new_ingredients
        recipe.instructions = new_instructions
        session.commit()


def delete_recipe_by_name(name: str):
    with Session() as session:
        recipe = session.query(Recipe).filter_by(name=name).first()
        session.delete(recipe)
        session.commit()


def get_recipes_by_ingredient(ingredient_name: str):
    with Session() as session:
        return session.query(Recipe).filter(Recipe.ingredients.ilike(f'%{ingredient_name}%')).all()


def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
    with Session() as session:
        try:
            session.begin()

            first_food = session.query(Recipe).filter_by(name=first_recipe_name).first()
            second_food = session.query(Recipe).filter_by(name=second_recipe_name).first()

            if first_food and second_food:
                first_food.ingredients, second_food.ingredients = second_food.ingredients, first_food.ingredients
                session.commit()
            else:
                raise Exception('Rollback the action!')

        except Exception as e:
            session.rollback()
            print(f'An exception occurred: {str(e)}')

