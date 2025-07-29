# Azure Infrastructure Deployment Script for Agentic Web Generator
# This script deploys the ARM template to create Resource Group and Storage Account

param(
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ParametersFile = "infrastructure.parameters.json",
    
    [Parameter(Mandatory=$false)]
    [string]$TemplateFile = "infrastructure.json",
    
    [Parameter(Mandatory=$false)]
    [string]$DeploymentName = "AgenticWebGen-Infrastructure-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
)

Write-Host "🚀 Starting Azure Infrastructure Deployment for Agentic Web Generator" -ForegroundColor Green

# Check if Azure CLI is installed
if (!(Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Azure CLI is not installed. Please install it from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Check if user is logged in
$account = az account show --query "user.name" -o tsv 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  You are not logged in to Azure. Please log in..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Failed to log in to Azure"
        exit 1
    }
}

Write-Host "✅ Logged in as: $account" -ForegroundColor Green

# Set subscription if provided
if ($SubscriptionId) {
    Write-Host "🔄 Setting subscription to: $SubscriptionId" -ForegroundColor Blue
    az account set --subscription $SubscriptionId
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Failed to set subscription"
        exit 1
    }
}

# Get current subscription
$currentSubscription = az account show --query "name" -o tsv
Write-Host "📋 Current subscription: $currentSubscription" -ForegroundColor Blue

# Validate template files exist
if (!(Test-Path $TemplateFile)) {
    Write-Error "❌ Template file not found: $TemplateFile"
    exit 1
}

if (!(Test-Path $ParametersFile)) {
    Write-Error "❌ Parameters file not found: $ParametersFile"
    exit 1
}

Write-Host "📁 Using template: $TemplateFile" -ForegroundColor Blue
Write-Host "📁 Using parameters: $ParametersFile" -ForegroundColor Blue

# Validate ARM template
Write-Host "🔍 Validating ARM template..." -ForegroundColor Blue
az deployment sub validate `
    --location "East US" `
    --template-file $TemplateFile `
    --parameters $ParametersFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Template validation failed"
    exit 1
}

Write-Host "✅ Template validation passed" -ForegroundColor Green

# Deploy the template
Write-Host "🚀 Deploying infrastructure..." -ForegroundColor Blue
az deployment sub create `
    --location "East US" `
    --name $DeploymentName `
    --template-file $TemplateFile `
    --parameters $ParametersFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Deployment failed"
    exit 1
}

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green