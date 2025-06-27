using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace SqlQuerier.FX;

public class FxReportUploader
{
    private readonly ILogger<FxReportUploader> _logger;

    public FxReportUploader(ILogger<FxReportUploader> logger)
    {
        _logger = logger;
    }

    [Function("FxReportUploader")]
    public async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req)
    {
        _logger.LogInformation("C# HTTP trigger function processed a request.");

        // Read HTML content from request body
        string htmlContent = await new StreamReader(req.Body).ReadToEndAsync();
        if (string.IsNullOrWhiteSpace(htmlContent))
        {
            return new BadRequestObjectResult("Request body cannot be empty. Please provide HTML content.");
        }

        // Configure Blob Storage settings
        const string containerName = "reports";
        string blobName = $"report_{DateTime.UtcNow.ToString("yyyyMMddHHmmss")}.html";

        try
        {
            // Get connection string from environment variable
            var connectionString = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");
            if (string.IsNullOrWhiteSpace(connectionString))
            {
                return new ObjectResult("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
                {
                    StatusCode = StatusCodes.Status500InternalServerError
                };
            }

            // Create blob client and upload HTML content
            var blobServiceClient = new BlobServiceClient(connectionString);
            var containerClient = blobServiceClient.GetBlobContainerClient(containerName);
            
            // Create container if it doesn't exist
            await containerClient.CreateIfNotExistsAsync(PublicAccessType.Blob);

            var blobClient = containerClient.GetBlobClient(blobName);
            
            // Upload HTML content with appropriate content type
            using var stream = new MemoryStream(Encoding.UTF8.GetBytes(htmlContent));
            await blobClient.UploadAsync(stream, overwrite: true);
            
            // Set content type to text/html to make it browser-viewable
            await blobClient.SetHttpHeadersAsync(new BlobHttpHeaders { ContentType = "text/html" });
            
            _logger.LogInformation($"HTML content uploaded to {blobName}");
            
            // Return blob URL
            return new OkObjectResult(new { url = blobClient.Uri.ToString() });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error uploading HTML content to blob storage.");
            return new ObjectResult($"Error uploading content: {ex.Message}")
            {
                StatusCode = StatusCodes.Status500InternalServerError
            };
        }
    }
}