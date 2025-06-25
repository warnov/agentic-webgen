import json
import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any


def parse_azure_function_url_and_modify_spec(openapi_spec_path: str) -> Dict[str, Any]:
    """
    Parse Azure Function URL from environment variable and modify OpenAPI spec with base URL and function code.
    
    Args:
        openapi_spec_path: Path to the OpenAPI specification file
        
    Returns:
        Modified OpenAPI specification dictionary
        
    Raises:
        ValueError: If URL format is invalid or function code is missing
    """
    # Get Azure Function URL from environment variable
    azure_function_url = os.environ.get("AZURE_FUNCTION_URL")
    if not azure_function_url:
        raise ValueError("AZURE_FUNCTION_URL environment variable is required")
    
    if not os.path.exists(openapi_spec_path):
        raise ValueError(f"OpenAPI spec file not found: {openapi_spec_path}")
    
    # Parse the Azure Function URL
    parsed_url = urlparse(azure_function_url)
    
    # Extract base URL (scheme + netloc)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Extract function code from query parameters
    function_code = parse_qs(parsed_url.query).get('code', [None])[0]
    
    if not function_code:
        raise ValueError("Function code not found in AZURE_FUNCTION_URL. URL must include ?code=... parameter")
    
    # Load the OpenAPI specification
    with open(openapi_spec_path, 'r') as f:
        openapi_spec = json.load(f)
    
    # Replace the base URL placeholder
    if "servers" in openapi_spec and len(openapi_spec["servers"]) > 0:
        openapi_spec["servers"][0]["url"] = base_url
    
    # Modify all paths to include the function code as query parameter
    if "paths" in openapi_spec:
        modified_paths = {}
        for path, path_definition in openapi_spec["paths"].items():
            # Add the function code as query parameter to each path
            modified_path = f"{path}?code={function_code}"
            modified_paths[modified_path] = path_definition
        
        # Replace the paths with the modified ones
        openapi_spec["paths"] = modified_paths
    
    return openapi_spec


def extract_base_url_and_code() -> tuple[str, str]:
    """
    Extract base URL and function code from Azure Function URL environment variable.
        
    Returns:
        Tuple containing (base_url, function_code)
        
    Raises:
        ValueError: If URL format is invalid or function code is missing
    """
    # Get Azure Function URL from environment variable
    azure_function_url = os.environ.get("AZURE_FUNCTION_URL")
    if not azure_function_url:
        raise ValueError("AZURE_FUNCTION_URL environment variable is required")
    
    # Parse the Azure Function URL
    parsed_url = urlparse(azure_function_url)
    
    # Extract base URL (scheme + netloc)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Extract function code from query parameters
    function_code = parse_qs(parsed_url.query).get('code', [None])[0]
    
    if not function_code:
        raise ValueError("Function code not found in AZURE_FUNCTION_URL. URL must include ?code=... parameter")
    
    return base_url, function_code
