#!/usr/bin/env bash

# ───────────────────────────────────────────────
# Ask for input
read -p "🗂️  Enter the Resource Group: " RG
read -p "📦 Enter the Storage Account name: " SA

echo ""
echo "🔧 Updating configuration for storage account: $SA"
echo "────────────────────────────────────────────────────"

# 1. Enable anonymous blob/container access at account level
az storage account update \
  --resource-group "$RG" \
  --name "$SA" \
  --allow-blob-public-access true

# 2. Allow Shared-Key access
az storage account update \
  --resource-group "$RG" \
  --name "$SA" \
  --allow-shared-key-access true

# 3. Enable public network access from all networks
az storage account update \
  --resource-group "$RG" \
  --name "$SA" \
  --public-network-access Enabled \
  --default-action Allow

echo ""
echo "✅ Storage account '$SA' in resource group '$RG' configured successfully."
