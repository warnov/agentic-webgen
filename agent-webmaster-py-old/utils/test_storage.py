# test_storage.py

import json
import os
from dotenv import load_dotenv
from tools.html_tools import fill_template_from_json

# Load environment variables
load_dotenv()

def test_blob_storage():
    """Test the blob storage function directly without agents"""
    
    print("🧪 Testing blob storage function...")
    
    # Test data
    test_json_data = {
        "name": "Walter Novoa",
        "city": "Medellín",
        "profession": "Systems Engineer"
    }
    
    # Convert to JSON string (as the function expects)
    json_input = json.dumps(test_json_data)
    
    print(f"📊 Test data: {json_input}")
    print("\n🔧 Environment variables:")
    print(f"   AZURE_STORAGE_CONNECTION_STRING: {'✅ Set' if os.environ.get('AZURE_STORAGE_CONNECTION_STRING') else '❌ Not set'}")
    
    try:
        print("\n🚀 Calling fill_template_from_json function...")
        result = fill_template_from_json(json_input)
        
        if result.startswith("Error"):
            print(f"❌ Function returned error: {result}")
        else:
            print(f"✅ Function executed successfully!")
            print(f"📄 Generated file URL: {result}")
            
    except Exception as e:
        print(f"💥 Exception occurred: {str(e)}")
        import traceback
        print(f"📋 Full traceback:\n{traceback.format_exc()}")

def test_blob_connection():
    """Test basic blob storage connection"""
    
    print("\n🔍 Testing blob storage connection...")
    
    try:
        from azure.storage.blob import BlobServiceClient
        from azure.identity import DefaultAzureCredential
        
        account_url = "https://saimpartnerdemo.blob.core.windows.net"
        
        # Test connection string approach
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if connection_string:
            print("🔗 Using connection string...")
            blob_service = BlobServiceClient.from_connection_string(connection_string)
        else:
            print("🔐 Using DefaultAzureCredential...")
            credential = DefaultAzureCredential()
            blob_service = BlobServiceClient(account_url, credential=credential)
        
        # Test listing containers
        print("📁 Attempting to list containers...")
        containers = list(blob_service.list_containers())
        print(f"✅ Found {len(containers)} containers:")
        for container in containers:
            print(f"   - {container.name}")
            
        # Test accessing the specific container
        container_name = "templates"
        print(f"\n📂 Testing access to '{container_name}' container...")
        container_client = blob_service.get_container_client(container_name)
        
        # List blobs in the container
        blobs = list(container_client.list_blobs())
        print(f"✅ Found {len(blobs)} blobs in '{container_name}':")
        for blob in blobs:
            print(f"   - {blob.name}")
            
        # Test downloading the template
        template_blob_name = "template1.html"
        if any(blob.name == template_blob_name for blob in blobs):
            print(f"\n📄 Testing download of '{template_blob_name}'...")
            blob_client = container_client.get_blob_client(template_blob_name)
            content = blob_client.download_blob().readall().decode("utf-8")
            print(f"✅ Template downloaded successfully ({len(content)} characters)")
            print(f"📝 Template preview: {content[:200]}...")
        else:
            print(f"❌ Template '{template_blob_name}' not found in container")
            
    except Exception as e:
        print(f"💥 Connection test failed: {str(e)}")
        import traceback
        print(f"📋 Full traceback:\n{traceback.format_exc()}")

if __name__ == "__main__":
    print("🔬 Azure Blob Storage Debug Test")
    print("=" * 50)
    
    # Test 1: Basic connection
    test_blob_connection()
    
    print("\n" + "=" * 50)
    
    # Test 2: Function execution
    test_blob_storage()
    
    print("\n🏁 Test completed!")