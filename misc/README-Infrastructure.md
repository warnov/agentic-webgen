# Azure Infrastructure Templates

Este directorio contiene los templates de ARM y scripts para desplegar la infraestructura de Azure necesaria para el proyecto Agentic Web Generator.

## Archivos

- **`infrastructure.json`** - ARM template principal que crea:
  - Resource Group parametrizado
  - Storage Account (LRS) para blobs y Azure Functions
  - Containers de blob: `templates` y `cards`
  
- **`infrastructure.parameters.json`** - Archivo de parámetros de ejemplo
- **`deploy-infrastructure.ps1`** - Script de PowerShell para deployment automatizado

## Parámetros Configurables

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `resourceGroupName` | Nombre del Resource Group | `rg-agentic-webgen` |
| `location` | Región de Azure | `East US` |
| `storageAccountName` | Nombre de la cuenta de almacenamiento | **Requerido** |
| `environment` | Etiqueta de ambiente | `dev` |

## Uso

### Opción 1: Usando el Script de PowerShell (Recomendado)

```powershell
# Desde el directorio misc/
.\deploy-infrastructure.ps1
```

### Opción 2: Usando Azure CLI directamente

```bash
# Validar template
az deployment sub validate \
  --location "East US" \
  --template-file infrastructure.json \
  --parameters infrastructure.parameters.json

# Desplegar
az deployment sub create \
  --location "East US" \
  --name "AgenticWebGen-Infrastructure" \
  --template-file infrastructure.json \
  --parameters infrastructure.parameters.json
```

### Opción 3: Personalizar parámetros en línea

```powershell
.\deploy-infrastructure.ps1 -ParametersFile "mi-config.parameters.json"
```

O con Azure CLI:

```bash
az deployment sub create \
  --location "East US" \
  --name "AgenticWebGen-Infrastructure" \
  --template-file infrastructure.json \
  --parameters resourceGroupName="mi-rg" storageAccountName="mistorage123" location="West US 2"
```

## Configuración de la Storage Account

La cuenta de almacenamiento se configura con:

- **SKU**: Standard_LRS (Locally Redundant Storage)
- **Kind**: StorageV2 (General Purpose v2)
- **Access Tier**: Hot
- **Public Access**: Habilitado para blobs
- **HTTPS Only**: Sí
- **TLS Version**: 1.2 mínimo

### Containers Creados

1. **`templates`** - Para almacenar plantillas HTML
   - Public Access: Blob level
   
2. **`cards`** - Para almacenar las tarjetas generadas
   - Public Access: Blob level

## Outputs del Template

Después del deployment, obtienes:

- `resourceGroupName` - Nombre del Resource Group creado
- `storageAccountName` - Nombre de la Storage Account
- `storageAccountId` - ID completo de la Storage Account
- `primaryEndpoints` - Todos los endpoints primarios
- `primaryBlobEndpoint` - Endpoint específico de blobs

## Configuración para Azure Functions

Esta storage account está optimizada para ser usada como:

1. **WebJobs Storage** - Para el runtime de Azure Functions
2. **Blob Storage** - Para almacenar templates y cards generadas

### Variables de Entorno Requeridas

```
AzureWebJobsStorage=DefaultEndpointsProtocol=https;AccountName={storageAccountName};AccountKey={key};EndpointSuffix=core.windows.net
WEBSITE_CONTENTAZUREFILECONNECTIONSTRING={misma connection string}
WEBSITE_CONTENTSHARE={function-app-name}
```

## Seguridad

- La storage account permite acceso público a nivel de blob para servir las cards como páginas web
- Se recomienda configurar CORS apropiadamente para producción
- Considerar usar Azure CDN para mejor rendimiento en producción

## Troubleshooting

### Error: Storage Account name already exists
Los nombres de storage account deben ser únicos globalmente. Modifica el parámetro `storageAccountName`.

### Error: Location not available
Verifica que la región especificada soporte todos los servicios requeridos.

### Error: Insufficient permissions
Asegúrate de tener permisos de Contributor en la suscripción.
