#!/usr/bin/env python3
"""Flask application entry point.

Version: 6.0.0
"""
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "6.0.0"})


@app.route('/api/v1/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    # Authentication logic here
    return jsonify({"message": "Login endpoint"})


@app.route('/api/v1/users')
@jwt_required()
def list_users():
    """List all users (protected endpoint)."""
    return jsonify({"users": []})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
