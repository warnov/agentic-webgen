# tools/html_tools.py

import json
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.identity import DefaultAzureCredential
from datetime import datetime
from typing import Annotated

def fill_template_from_json(json_input: Annotated[str, "JSON string with keys and values to fill in the template"]) -> Annotated[str, "URL of the newly generated HTML file in Blob Storage"]:
    """
    Fills an HTML template with data provided in a JSON string.

    Args:
        json_input: JSON string with keys and values to fill in the template.
    
    Returns:
        URL of the newly generated HTML file in Blob Storage.
    """
    try:
        # Parse JSON input
        data = json.loads(json_input)

        # Configure your blob storage access
        account_url = "https://saimpartnerdemo.blob.core.windows.net"
        container_name = "templates"
        template_blob_name = "template1.html"

        # Try multiple authentication methods
        blob_service = None
        auth_method = "unknown"
        
        # Method 1: SAS URL (if provided)
        sas_url = os.environ.get("AZURE_STORAGE_SAS_URL")
        if sas_url:
            blob_service = BlobServiceClient(account_url=sas_url)
            auth_method = "SAS URL"
        
        # Method 2: Connection string
        elif os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
            connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
            blob_service = BlobServiceClient.from_connection_string(connection_string)
            auth_method = "Connection String"
        
        # Method 3: DefaultAzureCredential (fallback)
        else:
            credential = DefaultAzureCredential()
            blob_service = BlobServiceClient(account_url, credential=credential)
            auth_method = "DefaultAzureCredential"
        
        print(f"Using authentication method: {auth_method}")
        container_client = blob_service.get_container_client(container_name)

        # Download template
        blob_client = container_client.get_blob_client(template_blob_name)
        html_template = blob_client.download_blob().readall().decode("utf-8")
        print(f"Template downloaded successfully ({len(html_template)} characters)")

        # Fill the template
        filled_html = html_template
        for key, value in data.items():
            filled_html = filled_html.replace(f"{{{{{key}}}}}", str(value))

        # Generate output file name
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        output_blob_name = f"filled_template_{timestamp}.html"

        # Upload the filled template with correct Content-Type using ContentSettings
        output_blob = container_client.get_blob_client(output_blob_name)
        content_settings = ContentSettings(
            content_type='text/html',
            content_encoding='utf-8'
        )
        
        output_blob.upload_blob(
            filled_html.encode("utf-8"), 
            overwrite=True,
            content_settings=content_settings
        )
        print(f"File uploaded successfully: {output_blob_name}")

        # Return URL (assumes container allows public read or SAS is configured)
        return output_blob.url
        
    except Exception as e:
        error_msg = f"Error processing template: {str(e)}"
        print(error_msg)
        return error_msg