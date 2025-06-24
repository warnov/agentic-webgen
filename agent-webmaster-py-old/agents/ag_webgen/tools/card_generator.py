# tools/card_generator.py

import json
import random
from typing import Annotated
from datetime import datetime

# Sample data for random generation
SAMPLE_NAMES = [
    "María González", "Carlos Rodríguez", "Ana Martínez", "Luis López", 
    "Carmen Fernández", "José García", "Laura Sánchez", "Miguel Torres",
    "Elena Ruiz", "David Moreno", "Isabel Jiménez", "Roberto Álvarez"
]

SAMPLE_CITIES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga",
    "New York", "London", "Paris", "Berlin", "Tokyo", "Sydney",
    "Mexico City", "Buenos Aires", "São Paulo", "Lima", "Bogotá"
]

SAMPLE_PROFESSIONS = [
    "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
    "Marketing Specialist", "Sales Manager", "Financial Analyst", "DevOps Engineer",
    "Solutions Architect", "Business Analyst", "Project Manager", "Consultant",
    "Cybersecurity Specialist", "Cloud Engineer", "AI Researcher"
]

SAMPLE_TITLES = [
    "Tarjeta Profesional", "Business Card", "Professional Profile", 
    "Perfil Ejecutivo", "Corporate Card", "Expert Profile"
]

SAMPLE_MESSAGES = [
    "Experto en tecnologías emergentes con más de 10 años de experiencia.",
    "Especialista en transformación digital y soluciones innovadoras.",
    "Líder en desarrollo de productos y estrategias de mercado.",
    "Consultor senior con amplia experiencia internacional.",
    "Profesional dedicado a la excelencia y la innovación continua.",
    "Especialista en análisis de datos y business intelligence.",
    "Experto en arquitecturas cloud y desarrollo ágil.",
    "Líder en equipos multiculturales y proyectos globales."
]

def generate_random_card() -> Annotated[str, "JSON string with random card data"]:
    """
    Generates a random professional card with sample data.
    
    Returns:
        JSON string containing random card data with title, name, city, profession, and message.
    """
    try:
        # Generate random data
        card_data = {
            "title": random.choice(SAMPLE_TITLES),
            "name": random.choice(SAMPLE_NAMES),
            "city": random.choice(SAMPLE_CITIES),
            "profession": random.choice(SAMPLE_PROFESSIONS),
            "message": random.choice(SAMPLE_MESSAGES)
        }
        
        # Convert to JSON string
        return json.dumps(card_data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_msg = f"Error generating random card: {str(e)}"
        print(error_msg)
        return json.dumps({"error": error_msg})

def create_custom_card(
    title: Annotated[str, "Title for the card"],
    name: Annotated[str, "Full name of the person"], 
    city: Annotated[str, "City where the person lives"],
    profession: Annotated[str, "Professional title or job"],
    message: Annotated[str, "Personal message or description"]
) -> Annotated[str, "JSON string with custom card data"]:
    """
    Creates a custom professional card with provided data.
    
    Args:
        title: Title for the card
        name: Full name of the person
        city: City where the person lives
        profession: Professional title or job
        message: Personal message or description
    
    Returns:
        JSON string containing the card data.
    """
    try:
        card_data = {
            "title": title,
            "name": name,
            "city": city,
            "profession": profession,
            "message": message
        }
        
        return json.dumps(card_data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_msg = f"Error creating custom card: {str(e)}"
        print(error_msg)
        return json.dumps({"error": error_msg})
