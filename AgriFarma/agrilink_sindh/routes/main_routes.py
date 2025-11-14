from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return '<h1>Welcome to AgriLink Sindh 🌾</h1><p><a href="/login">Login</a> | <a href="/register">Register</a></p>'
