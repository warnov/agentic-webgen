/* =========================================================================
   Schema: Core e-commerce sample
   Target: Azure SQL Database (T-SQL)
   -------------------------------------------------------------------------
   Tables
   ▸ dbo.Products   – catalog of sellable items
   ▸ dbo.Sales      – each completed transaction / invoice
   ▸ dbo.SaleItems  – line-items (resolves the many-to-many)
   ========================================================================= */

-- 1. Product master
CREATE TABLE dbo.Products
(
    ProductID     INT            IDENTITY(1,1) PRIMARY KEY,
    SKU           NVARCHAR(64)   NOT NULL UNIQUE,                  -- human-friendly code
    ProductName   NVARCHAR(255)  NOT NULL,
    Description   NVARCHAR(MAX)  NULL,
    UnitPrice     DECIMAL(18,2)  NOT NULL CHECK (UnitPrice >= 0),  -- currency
    IsActive      BIT            NOT NULL DEFAULT 1,               -- soft-delete flag
    CreatedAt     DATETIME2      NOT NULL DEFAULT SYSDATETIME(),
    UpdatedAt     DATETIME2      NULL
);

-- 2. Sales / billing header (one row per transaction)
CREATE TABLE dbo.Sales
(
    SaleID        INT            IDENTITY(1,1) PRIMARY KEY,
    SaleDate      DATETIME2      NOT NULL DEFAULT SYSDATETIME(),
    CustomerName  NVARCHAR(255)  NULL,                             -- keep it simple
    Subtotal      DECIMAL(18,2)  NOT NULL CHECK (Subtotal >= 0),
    TaxAmount     DECIMAL(18,2)  NOT NULL CHECK (TaxAmount >= 0),
    TotalAmount   AS (Subtotal + TaxAmount) PERSISTED,             -- computed
    CreatedAt     DATETIME2      NOT NULL DEFAULT SYSDATETIME()
);

-- 3. Bridge table – one row per product in a sale
CREATE TABLE dbo.SaleItems
(
    SaleItemID    INT            IDENTITY(1,1) PRIMARY KEY,
    SaleID        INT            NOT NULL,
    ProductID     INT            NOT NULL,
    Quantity      INT            NOT NULL CHECK (Quantity > 0),
    UnitPrice     DECIMAL(18,2)  NOT NULL CHECK (UnitPrice >= 0),
    LineTotal     AS (Quantity * UnitPrice) PERSISTED,

    CONSTRAINT FK_SaleItems_Sales
        FOREIGN KEY (SaleID)
        REFERENCES dbo.Sales (SaleID)
        ON DELETE CASCADE,

    CONSTRAINT FK_SaleItems_Products
        FOREIGN KEY (ProductID)
        REFERENCES dbo.Products (ProductID)
        ON DELETE NO ACTION
);

-- Helpful indexing for typical lookups
CREATE INDEX IX_SaleItems_SaleID    ON dbo.SaleItems (SaleID);
CREATE INDEX IX_SaleItems_ProductID ON dbo.SaleItems (ProductID);

-- Optional: keep Products.UpdatedAt in sync
GO
CREATE OR ALTER TRIGGER trg_Products_SetUpdatedAt
ON dbo.Products
AFTER UPDATE
AS
    SET NOCOUNT ON;
    UPDATE p
      SET UpdatedAt = SYSDATETIME()
    FROM dbo.Products AS p
    JOIN inserted      i ON i.ProductID = p.ProductID;
GO
