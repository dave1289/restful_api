"""Flask app for Cupcakes"""
from flask import Flask, redirect, render_template, json, jsonify, session, request, flash
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, db, Cupcake, serialize_cupcake

app = Flask(__name__)

# standardized sqlalchemy init setting and variable structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
# app.debug = True

app.app_context().push()

connect_db(app)

@app.route('/')
def show_home(): 
    data = Cupcake.query.all()
    cupcakes = list(data)
    
    return render_template('home.html', cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    data = Cupcake.query.all()
    
    serialized = [serialize_cupcake(c) for c in data]
    return jsonify(cupcakes=serialized)
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def get_cupcake(cupcake_id):
    data = Cupcake.query.get(cupcake_id)
    dict = serialize_cupcake(data)
    return {"cupcake" : dict}

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json['flavor'],
                          size=request.json['size'],
                           rating=request.json['rating'], image=request.json['image'])
    db.session.add(new_cupcake) 
    db.session.commit()
    response_json = jsonify(cupcake = serialize_cupcake(new_cupcake))
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    
    cupcake.flavor = request.json.get('flavor')
    cupcake.size = request.json.get('size')
    cupcake.rating = request.json.get('rating')
    cupcake.image = request.json.get('image')
    
    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake = serialize_cupcake(cupcake))
    return (response_json, 200)
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    response_json = jsonify({"message" : "entry deleted"})
    return (response_json, 202)

