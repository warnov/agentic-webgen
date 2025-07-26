/* ------------------------------------------------------------------------
   Table creation: Products, Sales, SaleItems, Promotions, Campaigns, HolidayCalendar, Reviews
------------------------------------------------------------------------ */
CREATE TABLE dbo.Products
(
    ProductID     INT            IDENTITY(1,1) PRIMARY KEY,
    SKU           NVARCHAR(64)   NOT NULL UNIQUE,
    ProductName   NVARCHAR(255)  NOT NULL,
    Description   NVARCHAR(MAX)  NULL,
    UnitPrice     DECIMAL(18,2)  NOT NULL CHECK (UnitPrice >= 0),
    IsActive      BIT            NOT NULL DEFAULT 1,
    CreatedAt     DATETIME2      NOT NULL DEFAULT SYSDATETIME(),
    UpdatedAt     DATETIME2      NULL
);
GO
CREATE TABLE dbo.Sales
(
    SaleID        INT            IDENTITY(1,1) PRIMARY KEY,
    SaleDate      DATETIME2      NOT NULL DEFAULT SYSDATETIME(),
    CustomerName  NVARCHAR(255)  NULL,
    Subtotal      DECIMAL(18,2)  NOT NULL CHECK (Subtotal >= 0),
    TaxAmount     DECIMAL(18,2)  NOT NULL CHECK (TaxAmount >= 0),
    TotalAmount   AS (Subtotal + TaxAmount) PERSISTED,
    CreatedAt     DATETIME2      NOT NULL DEFAULT SYSDATETIME()
);
GO
CREATE TABLE dbo.SaleItems
(
    SaleItemID    INT            IDENTITY(1,1) PRIMARY KEY,
    SaleID        INT            NOT NULL,
    ProductID     INT            NOT NULL,
    Quantity      INT            NOT NULL CHECK (Quantity > 0),
    UnitPrice     DECIMAL(18,2)  NOT NULL CHECK (UnitPrice >= 0),
    LineTotal     AS (Quantity * UnitPrice) PERSISTED,
    CONSTRAINT FK_SaleItems_Sales FOREIGN KEY (SaleID) REFERENCES dbo.Sales(SaleID) ON DELETE CASCADE,
    CONSTRAINT FK_SaleItems_Products FOREIGN KEY (ProductID) REFERENCES dbo.Products(ProductID) ON DELETE NO ACTION
);
GO
CREATE TABLE dbo.Promotions
(
    PromotionID   INT           IDENTITY(1,1) PRIMARY KEY,
    Name          NVARCHAR(200) NOT NULL,
    Description   NVARCHAR(500) NULL,
    StartDate     DATE          NOT NULL,
    EndDate       DATE          NOT NULL,
    IsActive      AS CASE WHEN CAST(SYSDATETIME() AS DATE) BETWEEN StartDate AND EndDate THEN 1 ELSE 0 END PERSISTED,
    CreatedAt     DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO
CREATE TABLE dbo.Campaigns
(
    CampaignID    INT           IDENTITY(1,1) PRIMARY KEY,
    Name          NVARCHAR(200) NOT NULL,
    Channel       NVARCHAR(100) NOT NULL,
    StartDate     DATE          NOT NULL,
    EndDate       DATE          NOT NULL,
    Budget        DECIMAL(18,2) NULL CHECK (Budget >= 0),
    CreatedAt     DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO
CREATE TABLE dbo.HolidayCalendar
(
    HolidayDate   DATE          PRIMARY KEY,
    Description   NVARCHAR(200) NOT NULL
);
GO
CREATE TABLE dbo.Reviews
(
    ReviewID      INT           IDENTITY(1,1) PRIMARY KEY,
    ProductID     INT           NOT NULL,
    Rating        TINYINT       NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    ReviewDate    DATE          NOT NULL,
    Comments      NVARCHAR(1000) NULL,
    CreatedAt     DATETIME2     NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT FK_Reviews_Products FOREIGN KEY (ProductID) REFERENCES dbo.Products(ProductID) ON DELETE CASCADE
);
GO

SET IDENTITY_INSERT dbo.Products ON;
INSERT INTO dbo.Products (ProductID, SKU, ProductName, Description, UnitPrice) VALUES
(1, 'PROD0001', '15-inch Laptop i7/16GB/512GB SSD', 'High-performance laptop for developers', 1399.00),
(2, 'PROD0002', '13-inch Ultrabook i5/8GB/256GB SSD', 'Lightweight business ultrabook', 999.00),
(3, 'PROD0003', 'Gaming Laptop RTX4060/32GB', 'Portable gaming powerhouse', 1899.00),
(4, 'PROD0004', 'Desktop Tower Ryzen9/32GB', 'Upgradeable desktop workstation', 1499.00),
(5, 'PROD0005', 'All-in-One PC 27-inch', 'Space-saving AIO computer', 1199.00),
(6, 'PROD0006', 'Android Smartphone 256GB', 'Flagship Android phone', 799.00),
(7, 'PROD0007', 'Smartphone Pro 512GB', 'High-end iOS device', 1099.00),
(8, 'PROD0008', '10-inch Tablet 128GB', 'Versatile media tablet', 499.00),
(9, 'PROD0009', '27-inch 4K Monitor', 'Color-accurate UHD display', 449.00),
(10, 'PROD0010', 'Wireless Mouse', 'Ergonomic wireless mouse', 49.99),
(11, 'PROD0011', 'Mechanical Keyboard', 'RGB mechanical keyboard', 129.99),
(12, 'PROD0012', 'USB-C Hub 7-in-1', 'Expand laptop I/O', 79.99),
(13, 'PROD0013', 'External SSD 1TB', 'Portable high-speed storage', 149.99),
(14, 'PROD0014', 'NVMe SSD 2TB', 'Ultra-fast internal storage', 229.99),
(15, 'PROD0015', 'Wi-Fi 6 Router', 'Next-gen wireless router', 179.99),
(16, 'PROD0016', 'Noise-Cancelling Headphones', 'Immersive sound experience', 299.00),
(17, 'PROD0017', 'Bluetooth Speaker', 'Portable wireless speaker', 99.99),
(18, 'PROD0018', 'Smartwatch Series 5', 'Health & fitness companion', 249.00),
(19, 'PROD0019', 'VR Headset', 'Virtual reality system', 399.00),
(20, 'PROD0020', 'HD Webcam', '1080p streaming webcam', 89.99);
SET IDENTITY_INSERT dbo.Products OFF;
GO

SET IDENTITY_INSERT dbo.Sales ON;
INSERT INTO dbo.Sales (SaleID, SaleDate, CustomerName, Subtotal, TaxAmount) VALUES
(1, '2025-06-21T09:01:47', 'Customer 001', 5183.99, 518.40),
(2, '2025-06-24T16:05:37', 'Customer 002', 11992.00, 1199.20),
(3, '2025-06-18T11:45:41', 'Customer 003', 5782.97, 578.30),
(4, '2025-06-05T11:48:21', 'Customer 004', 3798.00, 379.80),
(5, '2025-06-04T13:54:22', 'Customer 005', 8752.95, 875.30),
(6, '2025-06-12T17:12:45', 'Customer 006', 2997.00, 299.70),
(7, '2025-06-08T20:18:05', 'Customer 007', 3297.98, 329.80),
(8, '2025-06-21T13:10:23', 'Customer 008', 6543.00, 654.30),
(9, '2025-06-18T19:15:10', 'Customer 009', 2095.97, 209.60),
(10, '2025-06-02T20:20:25', 'Customer 010', 5455.98, 545.60),
(11, '2025-06-13T18:29:09', 'Customer 011', 5342.00, 534.20),
(12, '2025-06-19T14:57:37', 'Customer 012', 1957.97, 195.80),
(13, '2025-06-05T18:10:50', 'Customer 013', 5015.94, 501.59),
(14, '2025-06-18T08:43:46', 'Customer 014', 498.00, 49.80),
(15, '2025-06-25T18:21:07', 'Customer 015', 3166.96, 316.70),
(16, '2025-06-09T16:48:11', 'Customer 016', 7843.96, 784.40),
(17, '2025-06-20T13:31:01', 'Customer 017', 159.98, 16.00),
(18, '2025-06-08T08:15:56', 'Customer 018', 5162.97, 516.30),
(19, '2025-06-09T16:55:38', 'Customer 019', 3314.95, 331.50),
(20, '2025-06-15T16:28:07', 'Customer 020', 2897.00, 289.70),
(21, '2025-06-19T16:14:37', 'Customer 021', 9894.00, 989.40),
(22, '2025-06-02T11:04:57', 'Customer 022', 129.99, 13.00),
(23, '2025-06-17T11:17:42', 'Customer 023', 4294.00, 429.40),
(24, '2025-06-04T09:42:27', 'Customer 024', 1319.93, 131.99),
(25, '2025-06-21T18:06:03', 'Customer 025', 6723.99, 672.40),
(26, '2025-06-14T10:17:29', 'Customer 026', 5876.99, 587.70),
(27, '2025-06-02T18:34:53', 'Customer 027', 1899.00, 189.90),
(28, '2025-06-06T14:31:30', 'Customer 028', 2147.99, 214.80),
(29, '2025-06-01T14:16:59', 'Customer 029', 1076.98, 107.70),
(30, '2025-06-02T17:47:34', 'Customer 030', 129.99, 13.00),
(31, '2025-06-02T17:30:32', 'Customer 031', 9682.98, 968.30),
(32, '2025-06-13T09:56:36', 'Customer 032', 2196.00, 219.60),
(33, '2025-06-14T18:37:36', 'Customer 033', 4023.95, 402.40),
(34, '2025-06-10T15:20:59', 'Customer 034', 2798.00, 279.80),
(35, '2025-06-20T17:06:04', 'Customer 035', 4574.98, 457.50),
(36, '2025-06-15T16:45:19', 'Customer 036', 7693.98, 769.40),
(37, '2025-06-18T10:17:18', 'Customer 037', 4362.98, 436.30),
(38, '2025-06-09T08:00:21', 'Customer 038', 2945.00, 294.50),
(39, '2025-06-18T19:27:35', 'Customer 039', 1499.00, 149.90),
(40, '2025-06-23T10:34:02', 'Customer 040', 2246.00, 224.60),
(41, '2025-06-10T13:57:59', 'Customer 041', 79.99, 8.00),
(42, '2025-06-22T11:42:06', 'Customer 042', 1677.99, 167.80),
(43, '2025-06-14T08:11:47', 'Customer 043', 2175.99, 217.60),
(44, '2025-06-13T08:54:30', 'Customer 044', 2557.98, 255.80),
(45, '2025-06-08T11:01:42', 'Customer 045', 429.97, 43.00),
(46, '2025-06-25T12:22:41', 'Customer 046', 5235.95, 523.60),
(47, '2025-06-04T17:27:22', 'Customer 047', 2258.95, 225.90),
(48, '2025-06-09T08:45:27', 'Customer 048', 299.97, 30.00),
(49, '2025-06-22T19:47:47', 'Customer 049', 769.96, 77.00),
(50, '2025-06-11T17:20:42', 'Customer 050', 149.97, 15.00);
SET IDENTITY_INSERT dbo.Sales OFF;
GO

INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (1, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (1, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (1, 5, 3, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (2, 2, 1, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (2, 1, 3, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (2, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (2, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 15, 2, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (4, 3, 2, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 9, 1, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 15, 2, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (6, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 4, 2, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (8, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (8, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (8, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 8, 1, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 11, 2, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 5, 3, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 18, 3, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 12, 2, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 8, 1, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 3, 2, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (14, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 6, 3, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 15, 3, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 4, 2, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 17, 3, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (17, 12, 2, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 16, 2, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 19, 3, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (19, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (19, 18, 3, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (19, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (19, 10, 2, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 1, 3, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (22, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 5, 2, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 16, 1, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (24, 14, 3, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (24, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (24, 15, 3, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (26, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (26, 15, 1, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (27, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (28, 13, 1, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (28, 2, 2, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (29, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (29, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (29, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (29, 16, 1, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (30, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 6, 1, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (32, 19, 3, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (32, 2, 1, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 11, 2, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (34, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 5, 2, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 12, 1, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 16, 2, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 6, 2, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (40, 19, 2, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (40, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (40, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (41, 12, 1, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (43, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (43, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (43, 9, 1, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (44, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (44, 15, 2, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (45, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (45, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 11, 3, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (47, 14, 2, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (47, 17, 3, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (47, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 17, 3, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (49, 12, 1, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (49, 14, 3, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (50, 10, 3, 49.99);
GO

/* Promotions and Campaigns */
INSERT INTO dbo.Promotions (Name, Description, StartDate, EndDate) VALUES
('27-inch 4K Monitor Upgrade Campaign','15% off all 27-inch 4K monitors as part of our mid-June Workstation Upgrade Campaign','2025-06-17','2025-06-19'),
('Summer Sound Boost','20% off all Noise-Cancelling Headphones to kick off the summer listening season','2025-06-15','2025-06-22'),
('Mid-Year Tablet Upgrade','Save $50 when you trade in any old tablet for a new 10-inch Tablet 128GB','2025-06-17','2025-06-24'),
('Father’s Day 4K Monitor Special','15% off 27-inch 4K Monitors during Father’s Day weekend upgrade event','2025-06-14','2025-06-21'),
('Buy One Get Second 50% Off – Wireless Mouse','Clearance deal: buy one Wireless Mouse and get a second at half price','2025-06-20','2025-06-27'),
('Ryzen Desktop Bundle Deal','Bundle a Desktop Tower Ryzen9/32GB with an NVMe SSD upgrade and save 10%','2025-06-21','2025-06-28');
GO

/* Holidays */
INSERT INTO dbo.HolidayCalendar (HolidayDate, Description) VALUES
('2025-06-09','National Mid-Year Technology Refresh Day'),
('2025-06-22','National Car-Free Day: residents encouraged to avoid driving and stay home');
GO

/* Reviews: Negative Mouse */
INSERT INTO dbo.Reviews (ProductID, Rating, ReviewDate, Comments) VALUES
(10,1,'2025-06-23','The Bluetooth connection drops every few minutes; it’s very frustrating for work.'),
(10,1,'2025-06-24','The mouse loses signal constantly, especially if I move slightly away from the receiver.'),
(10,2,'2025-06-25','Battery life barely lasts a full day; I expected more based on the description.'),
(10,1,'2025-06-26','Right-click sometimes doesn’t register at all.'),
(10,2,'2025-06-27','The optical sensor skips on smooth surfaces; it’s useless on my glass desk.'),
(10,1,'2025-06-28','Unstable connection: I have to re-pair the dongle multiple times a day.'),
(10,1,'2025-06-29','Unstable connection: it disconnects mid-video call and reconnects on its own.'),
(10,2,'2025-06-30','The plastic feels cheap and heats up after a few minutes of use.'),
(10,1,'2025-07-01','Turning it on at startup takes too many clicks; it’s slow and tedious.'),
(10,2,'2025-07-02','Cursor movement is erratic: it jumps instead of gliding smoothly.');
GO

/* Reviews: Neutral Mouse */
INSERT INTO dbo.Reviews (ProductID, Rating, ReviewDate, Comments) VALUES
(10,3,'2025-07-03','The mouse performs adequately for everyday tasks.'),
(10,3,'2025-07-04','Battery life is acceptable, I get about a day of use without issues.'),
(10,3,'2025-07-05','Ergonomically it feels fine, neither exceptional nor uncomfortable.'),
(10,3,'2025-07-06','Buttons click responsively, overall a standard experience.'),
(10,3,'2025-07-07','Connection setup is straightforward and generally stable.');
GO

/* Reviews: Positive Gaming Laptop */
INSERT INTO dbo.Reviews (ProductID, Rating, ReviewDate, Comments) VALUES
(3,5,'2025-07-08','Absolutely love the performance; handles everything I throw at it with ease.'),
(3,4,'2025-07-09','Great laptop for gaming and work, battery life could be a bit better.'),
(3,5,'2025-07-10','The RTX4060 delivers smooth frame rates and the build feels solid.'),
(3,4,'2025-07-11','Very happy with the 32GB RAM, multitasking is seamless.'),
(3,5,'2025-07-12','Superb display and keyboard responsiveness—highly recommend.'),
(3,3,'2025-07-13','Good overall, but the fans run loudly under heavy load.'),
(3,4,'2025-07-14','Excellent specs for the price; only minor gripe is the webcam quality.'),
(3,5,'2025-07-15','This has become my go-to machine for both development and gaming.'),
(3,4,'2025-07-16','Solid build and performance, the SSD is blazing fast.'),
(3,5,'2025-07-17','Runs AAA titles effortlessly and stays cool thanks to efficient cooling.'),
(3,3,'2025-07-18','Decent laptop but wish it came with a bit more USB ports.'),
(3,4,'2025-07-19','The design is sleek and the RGB lighting is a nice touch.'),
(3,5,'2025-07-20','Rock-solid performance; I haven’t experienced a single crash.'),
(3,4,'2025-07-21','Great machine, though the power brick is quite bulky.'),
(3,5,'2025-07-22','Exceeded my expectations—perfect balance of power and portability.');
GO

/* Reviews: Other Products */
INSERT INTO dbo.Reviews (ProductID, Rating, ReviewDate, Comments) VALUES
(1,4,'2025-07-23','Solid performance and crisp display for everyday tasks.'),
(1,3,'2025-07-24','Runs smoothly, but gets warm under heavy load.'),
(1,5,'2025-07-25','Keyboard feels great and battery lasts through my workday.'),
(2,4,'2025-07-26','Lightweight design makes it very portable.'),
(2,3,'2025-07-27','Good battery life but could use a brighter screen.'),
(2,5,'2025-07-28','Perfect balance of performance and portability.'),
(4,5,'2025-07-29','Plenty of power for my development workloads.'),
(4,4,'2025-07-30','Easy to upgrade components, very flexible.'),
(4,3,'2025-07-31','A bit bulky but performance is top-notch.'),
(5,4,'2025-08-01','Clean setup, no separate tower needed.'),
(5,3,'2025-08-02','Touchscreen responsiveness could improve.'),
(5,5,'2025-08-03','Great for video calls and office tasks.'),
(6,4,'2025-08-04','Camera quality is impressive in low light.'),
(6,5,'2025-08-05','Storage space is ample for all my apps.'),
(6,3,'2025-08-06','Battery drains quickly when gaming.'),
(7,5,'2025-08-07','Sleek design and powerful performance.');
GO
