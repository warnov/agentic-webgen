# main.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))
from ag_webgen import generate_card_from_data

# Test the webgen agent with specific data
test_data = {
    "title": "Tarjeta Profesional",
    "name": "Walter Novoa", 
    "city": "New York",
    "profession": "Solutions Architect",
    "message": "Especialista en arquitecturas de soluciones en la nube con más de 10 años de experiencia."
}

# Generate the card
print("🔄 Generating card...")
result = generate_card_from_data(test_data)
print("Generated card URL:")
print(result)