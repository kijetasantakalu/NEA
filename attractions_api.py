from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    rating = db.Column(db.Float)
    is_free = db.Column(db.Boolean)


db.create_all()



@app.route('/attractions', methods=['GET'])
def get_attractions():
    attractions = Attraction.query.all()
    attractions_list = []
    for attraction in attractions:
        attractions_list.append({
            'id': attraction.id,
            'name': attraction.name,
            'description': attraction.description,
            'image_url': attraction.image_url,
            'location': attraction.location,
            'rating': attraction.rating,
            'is_free': attraction.is_free
        })
    return jsonify(attractions_list)

@app.route('/attractions', methods=['POST'])
def add_attraction():
    data = request.get_json()

    new_attraction = Attraction(
        name=data['name'],
        description=data['description'],
        image_url=data['image_url'],
        location=data['location'],
        rating=data['rating'],
        is_free=data['is_free']
    )

    db.session.add(new_attraction)
    db.session.commit()

    return jsonify({'message': 'Attraction added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)