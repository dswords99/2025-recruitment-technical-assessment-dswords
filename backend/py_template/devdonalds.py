from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = []

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('recipeName', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	
	# From what I can tell, this code should be correct via manual test
	# Not too sure why my tests aren't passing, could be my machine
	# Or something I am overlooking with the servers.
	# I'm on a pretty fresh install of linux and had to install and fix some stuff
	# with environments and so on so not sure if that affects it.

	add_whitespace = "".join(map(lambda c: " " if c in "_-" else c, recipeName))
	remove_nonchar = "".join([c for c in add_whitespace if c.isalpha() or c == " "])

	words = remove_nonchar.split()
	capitalised = " ".join(map(lambda w: w.capitalize(), words))

	if len(capitalised) == 0:
		return None

	return capitalised


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	data = request.get_json()

	if data.name in map(lambda c_ent: c_ent.name, cookbook):
		'entry names must be unique', 400

	if data.type == "recipe":
		items = []

		for r_item in data.requiredItems:
			if r_item.name in map(lambda i: i.name, items):
				return 'Recipe requiredItems can only have one element per name', 400
			
			items.append(RequiredItem(r_item.name, r_item.quantity))


		recipe = Recipe(data.name, items)
		cookbook.append(recipe)
		
	elif data.type == "ingredient":
		if data.cookTime < 0:
			return 'cook time must be >= 0', 400
		
		ing = Ingredient(data.name, data.cook_time)
		cookbook.append(ing)
	else:
		return 'type must be recipe or ingredient', 400
	

	


	return 'success', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)