# Azure Infrastructure Templates

This directory contains ARM templates and scripts to deploy the complete infrastructure required for the Agentic Web Generator project on Azure.

## Files

- **`infrastructure.json`** - Main ARM template (subscription-level deployment) that creates:
  - Resource Group
  - Storage Account (Standard LRS) with blob containers
  - Azure Function App with Elastic Premium hosting plan (Linux/.NET 8)
  - Azure AI Foundry (Cognitive Services with AIServices kind)
  
- **`infrastructure.parameters.json`** - Sample parameters file with current values
- **`deploy-infrastructure.ps1`** - PowerShell script for automated deployment

## Infrastructure Components

### 1. Resource Group
- **Purpose**: Logical container for all solution resources
- **Current Value**: `rg-agentic-webgen`

### 2. Storage Account
- **Configuration**: 
  - SKU: Standard_LRS (Locally Redundant Storage)
  - Kind: StorageV2 (General Purpose v2)
  - Access Tier: Hot
  - HTTPS Only: Enabled
  - TLS Version: 1.2 minimum
- **Current Value**: `stagenticwebgen`

**Blob Containers Created:**
- `templates` - Private access for HTML templates
- `cards` - Public blob access for generated business cards

### 3. Azure Function App
- **Hosting Plan**: Elastic Premium (EP1) on Linux
- **Runtime**: .NET 8 Isolated Worker (`DOTNET-ISOLATED|8.0`)
- **Configuration**:
  - Scale: Elastic scaling enabled (0-20 instances)
  - Memory: Optimized for workload
  - Storage: Connected to the storage account above
- **Current Value**: `func-agentic-webgen`

**Pre-configured App Settings:**
- `AzureWebJobsStorage`: Storage account connection string
- `AZURE_STORAGE_CONNECTION_STRING`: For custom storage operations
- `FUNCTIONS_WORKER_RUNTIME`: `dotnet-isolated`
- `FUNCTIONS_EXTENSION_VERSION`: `~4`
- `WEBSITE_CONTENTSHARE`: Function app name (lowercase)

### 4. Azure AI Foundry (Cognitive Services)
- **Type**: Microsoft.CognitiveServices/accounts
- **Kind**: AIServices (multi-service AI resource)
- **SKU**: S0 (Standard)
- **Features**:
  - System-assigned managed identity
  - Custom subdomain enabled
  - Public network access enabled
- **Current Value**: `ai-foundry-webgen`

## Configurable Parameters

| Parameter | Description | Current Value | Notes |
|-----------|-------------|---------------|-------|
| `resourceGroupName` | Resource Group name | `rg-agentic-webgen` | Logical container |
| `location` | Azure region | `East US2` | All resources deploy here |
| `storageAccountName` | Storage account name | `stagenticwebgen` | **Must be globally unique** |
| `functionAppName` | Function app name | `func-agentic-webgen` | **Must be globally unique** |
| `aiFoundryName` | AI Foundry resource name | `ai-foundry-webgen` | **Must be globally unique** |
| `environment` | Environment tag | `dev` | For resource organization |

## Configuration

### Step 1: Customize Parameters

Before deploying, update the `infrastructure.parameters.json` file with your custom values. Current configuration:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "resourceGroupName": {
      "value": "rg-agentic-webgen"
    },
    "location": {
      "value": "East US2"
    },
    "storageAccountName": {
      "value": "stagenticwebgen"
    },
    "environment": {
      "value": "dev"
    },
    "functionAppName": {
      "value": "func-agentic-webgen"
    },
    "aiFoundryName": {
      "value": "ai-foundry-webgen"
    }
  }
}
```

### Important Notes:

- **`storageAccountName`**: Must be **globally unique** across all Azure storage accounts
  - Only lowercase letters and numbers
  - 3-24 characters long
  - Current: `stagenticwebgen`

- **`functionAppName`**: Must be **globally unique** for Azure Function Apps
  - Current: `func-agentic-webgen`

- **`aiFoundryName`**: Must be **globally unique** for Cognitive Services
  - Current: `ai-foundry-webgen`

- **`location`**: Currently set to `"East US2"`
  - All resources will be deployed in this region

- **`environment`**: Currently set to `"dev"`
  - Used for resource tagging and organization

## Usage

### Step 2: Deploy the Infrastructure

### Option 1: Using PowerShell Script (Recommended)

```powershell
# From the infra/ directory
.\deploy-infrastructure.ps1
```

### Option 2: Using Azure CLI directly

```bash
# Validate template first
az deployment sub validate \
  --location "East US2" \
  --template-file infrastructure.json \
  --parameters infrastructure.parameters.json

# Deploy the infrastructure
az deployment sub create \
  --location "East US2" \
  --name "AgenticWebGen-Infrastructure" \
  --template-file infrastructure.json \
  --parameters infrastructure.parameters.json
```

### Option 3: Customize inline parameters

```powershell
.\deploy-infrastructure.ps1 -ParametersFile "custom-config.parameters.json"
```

Or with Azure CLI:

```bash
az deployment sub create \
  --location "East US2" \
  --name "AgenticWebGen-Infrastructure" \
  --template-file infrastructure.json \
  --parameters resourceGroupName="my-rg" storageAccountName="mystorage123" functionAppName="my-func-app" aiFoundryName="my-ai-foundry"
```

## Pre-Deployment Checklist

Before running the deployment, ensure you have:

- ✅ **Updated** `infrastructure.parameters.json` with your custom values (if needed)
- ✅ **Verified** all resource names are globally unique
- ✅ **Selected** appropriate Azure region for your location
- ✅ **Logged in** to Azure CLI (`az login`)
- ✅ **Set** the correct Azure subscription (`az account set --subscription <id>`)

### Testing Resource Name Availability

You can check if your resource names are available:

```bash
# Check storage account name
az storage account check-name --name stagenticwebgen

# Check function app name
az functionapp show --name func-agentic-webgen --resource-group rg-agentic-webgen
```

## Deployment Architecture

This template uses a **subscription-level deployment** with a nested resource group deployment pattern:

1. **Subscription Level**: Creates the resource group
2. **Resource Group Level**: Deploys all resources within the created resource group

### Resources Created:

1. **Storage Account** (`stagenticwebgen`)
   - Standard LRS with Hot access tier
   - Two blob containers: `templates` (private) and `cards` (public)
   - Connection string automatically configured for Function App

2. **App Service Plan** (`func-agentic-webgen-linux-asp`)
   - Elastic Premium (EP1) tier
   - Linux-based with elastic scaling (0-20 instances)
   - Optimized for Azure Functions workloads

3. **Function App** (`func-agentic-webgen`)
   - .NET 8 Isolated runtime on Linux
   - Pre-configured with storage connection strings
   - Ready for serverless execution

4. **AI Foundry** (`ai-foundry-webgen`)
   - Cognitive Services account with AIServices kind
   - Standard S0 pricing tier
   - System-assigned managed identity enabled

## Post-Deployment Steps

After successful deployment:

1. **AI Foundry Project**: Create an AI project within the AI Foundry resource via Azure Portal
2. **Function Deployment**: Deploy your .NET 8 Function App code
3. **Template Upload**: Upload HTML templates to the `templates` container
4. **Testing**: Verify the complete workflow from agent to web card generation

## Security & Networking

- **Storage**: Public blob access enabled for `cards` container (required for web serving)
- **Function App**: HTTPS only, configured for production use
- **AI Foundry**: Public network access enabled, custom subdomain configured
- **Identity**: System-assigned managed identities where applicable

## Troubleshooting

### Error: Resource name already exists
Resource names must be globally unique. Modify the values in your `infrastructure.parameters.json` file:
- `storageAccountName`: Currently `stagenticwebgen`
- `functionAppName`: Currently `func-agentic-webgen`  
- `aiFoundryName`: Currently `ai-foundry-webgen`

### Error: Location not available
Verify that East US2 supports all required services. You can check service availability by region in the [Azure Products by Region](https://azure.microsoft.com/en-us/global-infrastructure/services/) page.

### Error: Insufficient permissions
Make sure you have Contributor permissions on the subscription for subscription-level deployments.

### Error: Invalid parameter values
- Check that `storageAccountName` contains only lowercase letters and numbers (3-24 characters)
- Verify `functionAppName` follows Azure Function App naming conventions
- Ensure `aiFoundryName` is valid for Cognitive Services resources
- Verify `location` matches exact Azure region names (e.g., `"East US2"`)

### Error: Template validation failed
This template is designed for subscription-level deployment. Ensure you're using:
```bash
az deployment sub create
```
Not:
```bash
az deployment group create
```

### Quick Fix Commands

```bash
# Check available regions
az account list-locations --output table

# Check current subscription
az account show --query "name" -o tsv

# List available subscriptions
az account list --output table

# Set subscription
az account set --subscription "Your Subscription Name"

# Validate template before deployment
az deployment sub validate \
  --location "East US2" \
  --template-file infrastructure.json \
  --parameters infrastructure.parameters.json
```