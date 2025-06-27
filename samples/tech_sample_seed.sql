-- Seed data for Products, Sales, and SaleItems
SET NOCOUNT ON;
GO

SET IDENTITY_INSERT dbo.Products ON;
INSERT INTO dbo.Products (ProductID, SKU, ProductName, Description, UnitPrice) VALUES
(1, 'PROD0001', '15‑inch Laptop i7/16GB/512GB SSD', 'High‑performance laptop for developers', 1399.00),
(2, 'PROD0002', '13‑inch Ultrabook i5/8GB/256GB SSD', 'Lightweight business ultrabook', 999.00),
(3, 'PROD0003', 'Gaming Laptop RTX4060/32GB', 'Portable gaming powerhouse', 1899.00),
(4, 'PROD0004', 'Desktop Tower Ryzen9/32GB', 'Upgradeable desktop workstation', 1499.00),
(5, 'PROD0005', 'All‑in‑One PC 27‑inch', 'Space‑saving AIO computer', 1199.00),
(6, 'PROD0006', 'Android Smartphone 256GB', 'Flagship Android phone', 799.00),
(7, 'PROD0007', 'Smartphone Pro 512GB', 'High‑end iOS device', 1099.00),
(8, 'PROD0008', '10‑inch Tablet 128GB', 'Versatile media tablet', 499.00),
(9, 'PROD0009', '27‑inch 4K Monitor', 'Color‑accurate UHD display', 449.00),
(10, 'PROD0010', 'Wireless Mouse', 'Ergonomic wireless mouse', 49.99),
(11, 'PROD0011', 'Mechanical Keyboard', 'RGB mechanical keyboard', 129.99),
(12, 'PROD0012', 'USB‑C Hub 7‑in‑1', 'Expand laptop I/O', 79.99),
(13, 'PROD0013', 'External SSD 1TB', 'Portable high‑speed storage', 149.99),
(14, 'PROD0014', 'NVMe SSD 2TB', 'Ultra‑fast internal storage', 229.99),
(15, 'PROD0015', 'Wi‑Fi 6 Router', 'Next‑gen wireless router', 179.99),
(16, 'PROD0016', 'Noise‑Cancelling Headphones', 'Immersive sound experience', 299.00),
(17, 'PROD0017', 'Bluetooth Speaker', 'Portable wireless speaker', 99.99),
(18, 'PROD0018', 'Smartwatch Series 5', 'Health & fitness companion', 249.00),
(19, 'PROD0019', 'VR Headset', 'Virtual reality system', 399.00),
(20, 'PROD0020', 'HD Webcam', '1080p streaming webcam', 89.99);
SET IDENTITY_INSERT dbo.Products OFF;
GO

SET IDENTITY_INSERT dbo.Sales ON;
INSERT INTO dbo.Sales (SaleID, SaleDate, CustomerName, Subtotal, TaxAmount) VALUES
(1, '2025-06-09T11:14:08', 'Customer 001', 4197.00, 419.70),
(2, '2025-06-19T14:02:01', 'Customer 002', 249.00, 24.90),
(3, '2025-06-17T17:01:35', 'Customer 003', 1099.00, 109.90),
(4, '2025-06-19T12:51:55', 'Customer 004', 708.98, 70.90),
(5, '2025-06-14T13:17:09', 'Customer 005', 2397.00, 239.70),
(6, '2025-06-04T13:54:22', 'Customer 006', 3127.99, 312.80),
(7, '2025-06-12T17:12:45', 'Customer 007', 8752.95, 875.30),
(8, '2025-06-08T20:18:05', 'Customer 008', 2997.00, 299.70),
(9, '2025-06-21T13:10:23', 'Customer 009', 3297.98, 329.80),
(10, '2025-06-18T19:15:10', 'Customer 010', 6543.00, 654.30),
(11, '2025-06-02T20:20:25', 'Customer 011', 2095.97, 209.60),
(12, '2025-06-13T18:29:09', 'Customer 012', 5455.98, 545.60),
(13, '2025-06-19T14:57:37', 'Customer 013', 5342.00, 534.20),
(14, '2025-06-05T18:10:50', 'Customer 014', 1957.97, 195.80),
(15, '2025-06-18T08:43:46', 'Customer 015', 5015.94, 501.59),
(16, '2025-06-25T18:21:07', 'Customer 016', 498.00, 49.80),
(17, '2025-06-09T16:48:11', 'Customer 017', 3166.96, 316.70),
(18, '2025-06-20T13:31:01', 'Customer 018', 7843.96, 784.40),
(19, '2025-06-08T08:15:56', 'Customer 019', 159.98, 16.00),
(20, '2025-06-09T16:55:38', 'Customer 020', 5162.97, 516.30),
(21, '2025-06-15T16:28:07', 'Customer 021', 3314.95, 331.50),
(22, '2025-06-19T16:14:37', 'Customer 022', 2897.00, 289.70),
(23, '2025-06-02T11:04:57', 'Customer 023', 9894.00, 989.40),
(24, '2025-06-17T11:17:42', 'Customer 024', 129.99, 13.00),
(25, '2025-06-04T09:42:27', 'Customer 025', 4294.00, 429.40),
(26, '2025-06-21T18:06:03', 'Customer 026', 1319.93, 131.99),
(27, '2025-06-14T10:17:29', 'Customer 027', 6723.99, 672.40),
(28, '2025-06-02T18:34:53', 'Customer 028', 5876.99, 587.70),
(29, '2025-06-06T14:31:30', 'Customer 029', 1899.00, 189.90),
(30, '2025-06-01T14:16:59', 'Customer 030', 2147.99, 214.80),
(31, '2025-06-02T17:47:34', 'Customer 031', 1076.98, 107.70),
(32, '2025-06-02T17:30:32', 'Customer 032', 129.99, 13.00),
(33, '2025-06-13T09:56:36', 'Customer 033', 9682.98, 968.30),
(34, '2025-06-14T18:37:36', 'Customer 034', 2196.00, 219.60),
(35, '2025-06-10T15:20:59', 'Customer 035', 4023.95, 402.40),
(36, '2025-06-20T17:06:04', 'Customer 036', 2798.00, 279.80),
(37, '2025-06-15T16:45:19', 'Customer 037', 4574.98, 457.50),
(38, '2025-06-18T10:17:18', 'Customer 038', 7693.98, 769.40),
(39, '2025-06-09T08:00:21', 'Customer 039', 4362.98, 436.30),
(40, '2025-06-18T19:27:35', 'Customer 040', 2945.00, 294.50),
(41, '2025-06-23T10:34:02', 'Customer 041', 1499.00, 149.90),
(42, '2025-06-10T13:57:59', 'Customer 042', 2246.00, 224.60),
(43, '2025-06-22T11:42:06', 'Customer 043', 79.99, 8.00),
(44, '2025-06-14T08:11:47', 'Customer 044', 1677.99, 167.80),
(45, '2025-06-13T08:54:30', 'Customer 045', 2175.99, 217.60),
(46, '2025-06-08T11:01:42', 'Customer 046', 2557.98, 255.80),
(47, '2025-06-25T12:22:41', 'Customer 047', 429.97, 43.00),
(48, '2025-06-04T17:27:22', 'Customer 048', 5235.95, 523.60),
(49, '2025-06-09T08:45:27', 'Customer 049', 2258.95, 225.90),
(50, '2025-06-22T19:47:47', 'Customer 050', 299.97, 30.00);
SET IDENTITY_INSERT dbo.Sales OFF;
GO

INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (1, 1, 3, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (2, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (3, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (4, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (4, 14, 2, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (5, 6, 3, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (6, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (6, 4, 2, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 9, 1, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 15, 2, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (7, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (8, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 4, 2, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (9, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (10, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (11, 8, 1, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (12, 11, 2, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 5, 3, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (13, 18, 3, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (14, 12, 2, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (14, 8, 1, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (14, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (14, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 3, 2, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 13, 3, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (15, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (16, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (17, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (17, 6, 3, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (17, 15, 3, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 4, 2, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 17, 3, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 7, 3, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (18, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (19, 12, 2, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 16, 2, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 19, 3, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (20, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 18, 3, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (21, 10, 2, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (22, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (22, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 1, 3, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (23, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (24, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 5, 2, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (25, 16, 1, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (26, 14, 3, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (26, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (26, 15, 3, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (27, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (27, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (27, 8, 2, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (27, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (28, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (28, 15, 1, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (29, 3, 1, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (30, 13, 1, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (30, 2, 2, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 18, 2, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (31, 16, 1, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (32, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 6, 1, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 2, 3, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 3, 3, 1899.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (33, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (34, 19, 3, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (34, 2, 1, 999.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 11, 2, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 20, 3, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (35, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (36, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 7, 1, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 9, 2, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 5, 2, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (37, 12, 1, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 17, 1, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 10, 1, 49.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (38, 4, 3, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 20, 1, 89.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (39, 16, 2, 299.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (40, 9, 3, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (40, 6, 2, 799.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (41, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 19, 2, 399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (42, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (43, 12, 1, 79.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (44, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (44, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (44, 5, 1, 1199.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (45, 14, 1, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (45, 8, 3, 499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (45, 9, 1, 449.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 7, 2, 1099.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (46, 15, 2, 179.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (47, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (47, 11, 1, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 13, 2, 149.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 18, 1, 249.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 11, 3, 129.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 1, 2, 1399.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (48, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (49, 14, 2, 229.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (49, 17, 3, 99.99);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (49, 4, 1, 1499.00);
INSERT INTO dbo.SaleItems (SaleID, ProductID, Quantity, UnitPrice) VALUES (50, 17, 3, 99.99);
GO