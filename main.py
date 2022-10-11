from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random


def strtobool(value):
    if value in ['True', ' true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # using dictionary comprehension
        # Loop through each column in the data record

        # Create a new dictionary entry;
        # where the key is the name of the column
        # and the value is the value of the column
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/search')
def search():
    location = request.args.get('loc')
    cafe = Cafe.query.filter_by(location=location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


# @app.route('/random')
# def get_random_cafe():
#     cafes =db.session.query(Cafe).all()
#     random_cafe = random.choice(cafes)
#     return jsonify(cafe={
#         'id': random_cafe.id,
#         'name': random_cafe.name,
#         "map_url": random_cafe.map_url,
#         "img_url": random_cafe.img_url,
#         "location": random_cafe.location,
#         "seats": random_cafe.seats,
#         "has_toilet": random_cafe.has_toilet,
#         "has_wifi": random_cafe.has_wifi,
#         "has_sockets": random_cafe.has_sockets,
#         "can_take_calls": random_cafe.can_take_calls,
#         "coffee_price": random_cafe.coffee_price,
#     })


@app.route('/random')
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def patch_new_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == 'TopSecretAPIKey':
        cafe = Cafe.query.filter_by(id=cafe_id).first()
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={'error': "Sorry, that's not allowed. Make sure you have the correct api-key."}), 403


@app.route('/add', methods=['POST'])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.args.get('name'),
        map_url=request.args.get('map_url'),
        img_url=request.args.get('img_url'),
        location=request.args.get('location'),
        seats=request.args.get('seats'),
        has_toilet=strtobool(request.args.get('has_toilet')),
        has_wifi=strtobool(request.args.get('has_wifi')),
        has_sockets=strtobool(request.args.get('has sockets')),
        can_take_calls=strtobool(request.args.get('can_take_Calls')),
        coffee_price=request.args.get('coffee_price'),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": 'Successfully added the new cafe.'})


@app.route('/all')
def get_all():
    cafes = Cafe.query.all()
    return jsonify(cafe=[cafe.to_dict() for cafe in cafes])




if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


