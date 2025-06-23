using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace AgenticWebGen.Fx
{
    public class FxTemplateFiller(ILogger<FxTemplateFiller> logger)
    {
        private readonly ILogger<FxTemplateFiller> _logger = logger;

        [Function("FxTemplateFiller")]
        public async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req)
        {
            _logger.LogInformation("C# HTTP trigger function processed a request.");

            //Get a json payload from the request with the required validations        
            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();

            if (string.IsNullOrWhiteSpace(requestBody))
            {
                return new BadRequestObjectResult("Request body cannot be empty.");
            }

           
            //Parse the JSON into a dictionary
            Dictionary<string, string>? data;
            try
            {
                data = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, string>>(requestBody);
                if (data == null)
                    return new BadRequestObjectResult("Invalid JSON or not a dictionary of string to string.");
            }
            catch (System.Text.Json.JsonException)
            {
                return new BadRequestObjectResult("Malformed JSON.");
            }


            //Configure Blob Storage settings
            const string containerName = "templates";
            const string templateBlobName = "template1.html";


            var conn = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING")!;
            var blobServiceClient = new BlobServiceClient(conn);            
            var containerClient = blobServiceClient.GetBlobContainerClient(containerName);
            var blobClient = containerClient.GetBlobClient(templateBlobName);


            //Download the HTML template
            string htmlTemplate;
            try
            {
                var downloadInfo = await blobClient.DownloadAsync();
                using var streamReader = new StreamReader(downloadInfo.Value.Content);
                htmlTemplate = await streamReader.ReadToEndAsync();
            }
            catch (Exception ex)
            {
                //Return 500 plus the exception message in the response body
                _logger.LogError(ex, "Error downloading template blob.");
                return new ObjectResult($"Error downloading template blob: {ex.Message}")
                {
                    StatusCode = StatusCodes.Status500InternalServerError
                };
            }


            //Replace placeholders in the HTML template with values from the JSON payload
            foreach (var kvp in data)
            {
                // Use a simple placeholder format like {{key}} in the HTML template
                htmlTemplate = htmlTemplate.Replace($"{{{{{kvp.Key}}}}}", kvp.Value);
            }

            //Upload the filled template
            string timestamp = DateTime.UtcNow.ToString("yyyyMMddHHmmss");
            string outputBlobName = $"filled_template_{timestamp}.html";
            var outputBlobClient = containerClient.GetBlobClient(outputBlobName);
            using var uploadStream = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(htmlTemplate));
            var headers = new BlobHttpHeaders { ContentType = "text/html" };

            // Asegúrate de que el stream está en la posición 0
            uploadStream.Position = 0;

            // Sube el blob con los headers
            await outputBlobClient.UploadAsync(uploadStream, overwrite: true);

            // Refuerza los headers por si acaso
            await outputBlobClient.SetHttpHeadersAsync(new BlobHttpHeaders { ContentType = "text/html" });
            

            _logger.LogInformation("Template uploaded to blob storage: {OutputBlobName}", outputBlobName);

            // Return the full URL of the new blob
            return new OkObjectResult(new
            {
                url = outputBlobClient.Uri.ToString()
            });
        }
    }
}