"""
Streamlit Cloud entry point for GenAI Courtroom.
This file is required by Streamlit Cloud which expects streamlit_app.py in the root.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main frontend app
from frontend.App import *
