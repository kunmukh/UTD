--> 1>CREATE VIEW FOR TOP GOLD_CUST
CREATE VIEW TOP_GOLD_CUST(Fname, Lname, DOMemEnrol) AS
SELECT DISTINCT TOP 1  P.Fname, P.Lname, G.CardExpiraryDate
FROM PERSON AS P, GOLD_CUST AS G
WHERE P.PID = G.GoldPID AND 
(SELECT COUNT(*)
FROM STORE_ORDER as SO
WHERE G.GoldPID = SO.PID AND 
SO.DatePurchase >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 1, 0)
) >= 12
GO

--> 2>CREATE VIEW FOR TOP_POPULAR_PRODUCT
CREATE VIEW TOP_POPULAR_PRODUCT (NumofItems, ProductID, ProductQuantity, ProductDescription, ProductAgeRestriction, ProductSupplierID) AS
SELECT TOP 1 COUNT(*) AS NumofItems, P.ProductID, P.ProductQuantity, P.ProductDescription, P.ProductAgeRestriction, P.ProductSupplierID
FROM PRODUCT AS P,  STORE_ORDER AS SO
WHERE P.ProductID = SO.ProductID AND SO.DatePurchase >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 2, 0)
GROUP BY P.ProductID, P.ProductQuantity, P.ProductDescription, P.ProductAgeRestriction, P.ProductSupplierID
ORDER BY COUNT(*) DESC
GO

--> 3>CREATE VIEW FOR TOP_STORE
CREATE VIEW TOP_STORE (NumofItems, StoreID, StoreName, StoreStreet, StoreCity, StoreState) AS
SELECT TOP 1 COUNT(*) AS NumofItems, S.StoreID, S.StoreName, S.StoreStreet, S.StoreCity, S.StoreState
FROM STORE AS S,  STORE_ORDER AS SO
WHERE S.StoreID = SO.StoreID AND SO.DatePurchase >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 1, 0)
GROUP BY S.StoreID, S.StoreName, S.StoreStreet, S.StoreCity, S.StoreState
ORDER BY COUNT(*) DESC
GO

--> 4>CREATE VIEW FOR POTENTIAL_GOLD_CUST
CREATE VIEW POTENTIAL_GOLD_CUST (Fname, Lname, PhoneNo, PID) AS
SELECT DISTINCT P.Fname, P.Lname, PO.PhoneNo, P.PID
FROM PERSON AS P, PHONE_NUMBER AS PO, SILVER_CUST AS S, NON_ONLINE_CUST AS NC
WHERE PO.PID = P.PID AND P.PID = S.SilverPID AND S.SilverPID = NC.NonOnlinePID 
AND
(SELECT COUNT(*)
FROM BUY as B
WHERE B.NonOnlinePID = NC.NonOnlinePID AND 
B.DatePurchase >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 1, 0)
) >= 10
GO

--> 5>CREATE VIEW FOR TOP_SUPPLIER
CREATE VIEW TOP_SUPPLIER (NumofItems, SupplierID, SupplierName, SupplierLocation, SupplierPhoneNo) AS
SELECT TOP 1 COUNT(*) AS NumofItems, S.SupplierID, S.SupplierName, S.SupplierLocation, S.SupplierPhoneNo
FROM SUPPLIER AS S, SUPPLY_DATE AS SD
WHERE S.SupplierID = SD.SupplierID AND SD.SupplyDate >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 1, 0)
GROUP BY S.SupplierID, S.SupplierName, S.SupplierLocation, S.SupplierPhoneNo
ORDER BY COUNT(*) DESC
GO







