from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the app and database
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
db = SQLAlchemy(app)

# Models
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    users = db.relationship('User', backref='company', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

# Routes for managing companies
@app.route('/companies', methods=['GET', 'POST'])
def handle_companies():
    if request.method == 'GET':
        companies = Company.query.all()
        return jsonify([{
            'id': company.id,
            'name': company.name,
            'address': company.address,
            'latitude': company.latitude,
            'longitude': company.longitude
        } for company in companies])
    
    elif request.method == 'POST':
        data = request.get_json()
        new_company = Company(
            name=data['name'],
            address=data['address'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(new_company)
        db.session.commit()
        return jsonify({'message': 'Company created successfully'}), 201

# Routes for managing users
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'username': user.username,
            'company_id': user.company_id
        } for user in users])
    
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            username=data['username'],
            company_id=data['company_id']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

# Route for migrating a user to another company
@app.route('/migrate_user', methods=['POST'])
def migrate_user():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    if user:
        user.company_id = data['new_company_id']
        db.session.commit()
        return jsonify({'message': 'User migrated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
