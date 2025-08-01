# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    # below is old sample code before update:
    # return make_response(
    #     '<h1>Welcome to the pet directory!</h1>',
    #     200
    # )
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/demo_json')
def demo_json():
    # below is old sample code:
    #   pet_json = '{"id": 1, "name" : "Fido", "species" : "Dog"}'
    pet = Pet.query.first()
    pet_dict = {'id': pet.id,
            'name': pet.name,
            'species': pet.species
            }
    return make_response(pet_dict, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        body = {'id': pet.id,
                'name': pet.name,
                'species': pet.species}
        status = 200
    else:
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # array to store a dictionary for each pet
    for pet in Pet.query.filter_by(species=species).all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    }
        pets.append(pet_dict)
    body = {'count': len(pets),
            'pets': pets
            }
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
