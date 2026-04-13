from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from helpers.executeSequence import ExecuteSequence
from moveable.stepper import Stepper
from moveable.servo import ServoMotor
from sqlalchemy import create_engine, Column, Integer, String, Float

from pathlib import Path
import json
import glob
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# generates Flask app and defines routes for the cocktail mixing application. 
# It loads pump and position configurations from JSON files, creates a sequence of steps to mix cocktails based on user-selected ingredients, and handles the execution of these steps. 
# The app also includes routes for displaying the status of various components and a shutdown route.
BASE_DIR = Path(__file__).resolve().parent
JSON_DIR = BASE_DIR.parent / 'json'

app = Flask(__name__,
            template_folder=str(BASE_DIR.parent / 'frontend' / 'templates'),
            static_folder=str(BASE_DIR.parent / 'frontend' / 'static'))

# Set a secret key for session management (in production, use a secure random key)
app.secret_key = "test123"

