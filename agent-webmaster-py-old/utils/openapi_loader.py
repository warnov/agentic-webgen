# utils/openapi_loader.py

import json
import urllib.parse
from pathlib import Path

def load_openapi_spec(spec_file_path: str, azure_function_url: str) -> dict:
    """
    Load OpenAPI specification from a JSON file and customize it for the Azure Function URL.
    
    Args:
        spec_file_path: Path to the OpenAPI JSON file
        azure_function_url: Complete Azure Function URL with authentication
        
    Returns:
        Customized OpenAPI specification dictionary
    """
    # Load the base OpenAPI spec
    with open(spec_file_path, 'r') as f:
        openapi_spec = json.load(f)
    
    # Parse the Azure Function URL
    parsed_url = urllib.parse.urlparse(azure_function_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path_with_query = f"{parsed_url.path}?{parsed_url.query}" if parsed_url.query else parsed_url.path
    
    # Replace placeholders in the spec
    spec_str = json.dumps(openapi_spec)
    spec_str = spec_str.replace("{base_url}", base_url)
    spec_str = spec_str.replace("{path_with_query}", path_with_query)
    
    return json.loads(spec_str)
