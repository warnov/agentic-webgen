import os
from typing import Optional

def load_html_template(template_name: str = "report_template.html") -> Optional[str]:
    """
    Load HTML template content from the tools folder.
    
    Args:
        template_name: Name of the template file to load
        
    Returns:
        String containing the HTML template content, or None if file not found
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        Exception: If there's an error reading the file
    """
    try:
        # Get the directory where this module is located
        tools_dir = os.path.dirname(__file__)
        template_path = os.path.join(tools_dir, template_name)
        
        # Check if file exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")

        print("Template loaded successfully")
        # Read and return the template content
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except FileNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"Error loading template '{template_name}': {str(e)}")

def get_available_templates() -> list:
    """
    Get a list of available HTML template files in the tools folder.
    
    Returns:
        List of template file names
    """
    try:
        tools_dir = os.path.dirname(__file__)
        files = os.listdir(tools_dir)
        # Filter for HTML files only
        html_files = [f for f in files if f.lower().endswith('.html')]
        return html_files
    except Exception:
        return []


