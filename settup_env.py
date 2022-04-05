from dotenv import load_dotenv
from pathlib import Path

class EnvironementSettup:
    def __init__(self):
        dotenv_path = Path('.env')
        load_dotenv(dotenv_path=dotenv_path)

