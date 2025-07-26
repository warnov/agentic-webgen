# Install Visual Studio Code
Write-Host "`nInstalling Visual Studio Code..." -ForegroundColor Cyan
winget install --id Microsoft.VisualStudioCode -e --accept-package-agreements --accept-source-agreements

# Install Git for Windows
Write-Host "`nInstalling Git for Windows..." -ForegroundColor Cyan
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements

# Install Python 3.12
Write-Host "`nInstalling Python 3.12..." -ForegroundColor Cyan
winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
Write-Host "`nPython was installed successfully." -ForegroundColor Green

# Install .NET SDK (latest stable version)
Write-Host "`nInstalling .NET SDK..." -ForegroundColor Cyan
winget install --id Microsoft.DotNet.SDK.8 -e --accept-package-agreements --accept-source-agreements
Write-Host "`n.NET SDK was installed successfully." -ForegroundColor Green

# Install VSCode extensions
Write-Host "`nInstalling VSCode extensions..." -ForegroundColor Cyan

# Ensure 'code' command is available in current session
$env:Path += ";$env:USERPROFILE\AppData\Local\Programs\Microsoft VS Code\bin"

# Install Python extension for VSCode
code --install-extension ms-python.python

# Install Azure Functions extension for VSCode
code --install-extension ms-azuretools.vscode-azurefunctions

# Install REST Client extension for VSCode
code --install-extension humao.rest-client

# Install C# extension for VSCode
code --install-extension ms-dotnettools.csharp

# Done
Write-Host "`nAll components installed successfully." -ForegroundColor Green

# Notify user to restart terminal before using installed apps
Write-Host "Please close and reopen your terminal before running installed apps." -ForegroundColor Yellow
