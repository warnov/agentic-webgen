using Microsoft.Data.SqlClient;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace SqlQuerier.FX;

public class FxSqlQuerier
{
    private readonly ILogger<FxSqlQuerier> _logger;

    public FxSqlQuerier(ILogger<FxSqlQuerier> logger) => _logger = logger;

    [Function("FxSqlQuerier")]
    public async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req)
    {
        _logger.LogInformation("C# HTTP trigger function processed a request.");

        // Read T-SQL script from request body
        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        if (string.IsNullOrWhiteSpace(requestBody))
            return new BadRequestObjectResult("Request body cannot be empty. Please provide a T-SQL script.");

        // Get connection string from environment variable
        var connStr = Environment.GetEnvironmentVariable("SQLQUERIER_CONNECTION_STRING");
        if (string.IsNullOrWhiteSpace(connStr))
            return new ObjectResult("SQLQUERIER_CONNECTION_STRING environment variable is not set.")
            {
                StatusCode = StatusCodes.Status500InternalServerError
            };

        try
        {
            using var conn = new SqlConnection(connStr);
            // Removed duplicate using directive
            await conn.OpenAsync();

            using var cmd = new SqlCommand(requestBody, conn);
            using var reader = await cmd.ExecuteReaderAsync();

            var results = new List<Dictionary<string, object?>>();
            while (await reader.ReadAsync())
            {
                var row = new Dictionary<string, object?>();
                for (int i = 0; i < reader.FieldCount; i++)
                {
                    row[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                }
                results.Add(row);
            }

            var json = JsonSerializer.Serialize(results, new JsonSerializerOptions { WriteIndented = true });
            return new ContentResult
            {
                Content = json,
                ContentType = "application/json",
                StatusCode = StatusCodes.Status200OK
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error executing SQL query.");
            return new ObjectResult($"Error executing SQL query: {ex.Message}")
            {
                StatusCode = StatusCodes.Status500InternalServerError
            };
        }
    }
}