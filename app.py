from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    required_fields = ['username']

    # Verificar que todos los campos requeridos están presentes
    if all(field in data for field in required_fields):
        user_id = mongo.db.Perfiles.insert_one(data).inserted_id
        return jsonify({'message': 'Profile added successfully!', 'id': str(user_id)}), 201
    else:
        missing_fields = [field for field in required_fields if field not in data]
        return jsonify({'error': 'Missing data!', 'missing_fields': missing_fields}), 400


@app.route('/users', methods=['GET'])
def get_profiles():
    users = mongo.db.Perfiles.find()
    result = []
    for user in users:
        user['_id'] = str(user['_id'])  
        result.append(user)
    return jsonify(result)

@app.route('/users/<username>', methods=['GET'])
def get_profile_by_username(username):
    profile = mongo.db.Perfiles.find_one({'username': username})
    if profile:
        profile['_id'] = str(profile['_id']) 
        return jsonify(profile)
    else:
        return jsonify({"error": "Profile not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)