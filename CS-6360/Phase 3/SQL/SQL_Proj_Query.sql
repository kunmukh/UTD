--> QUERY 1
SELECT DISTINCT P.PID, P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState, A.StoreID, S.StoreName
FROM PERSON AS P, PHONE_NUMBER AS PH, PRSN_ADDRESS AS PA, MANAGER AS M, ASSIGNMENT AS A, STORE AS S
WHERE PH.PID=P.PID AND PA.PID=P.PID AND P.PID = M.ManagerPID AND M.ManagerPID = A.EmployeePID AND S.StoreID = A.StoreID
AND A.AssignmentDate >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 2, 0)
GO

--> QUERY 2
SELECT DISTINCT P.PID, P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState
FROM PERSON AS P, PHONE_NUMBER AS PH, PRSN_ADDRESS AS PA
WHERE PH.PID=P.PID AND PA.PID=P.PID
AND NOT EXISTS ((
                SELECT DISTINCT AR.ProductID
                FROM ASSIGNMENT AS ASS, FLOOR_STAFF AS F, 
                ARRANGEMENT AS AR, PERI_PRODUCT AS PE1
                WHERE ASS.EmployeePID = F.FloorStaffPID AND 
                F.FloorStaffPID = AR.FloorStaffPID AND 
                AR.ProductID = PE1.PerishableProductID
                GROUP BY ASS.StoreID, AR.ProductID
                ) 
                EXCEPT 
                (
                SELECT DISTINCT SO.ProductID
                FROM STORE_ORDER AS SO, PERI_PRODUCT AS PE
                WHERE SO.ProductID = PE.PerishableProductID AND SO.PID = P.PID
                GROUP BY SO.StoreID, SO.ProductID
                ))
GO

--> QUERY 3
SELECT AVG(NumOfPurchase) AS AvgPurchase
FROM
(
    SELECT P1.PID, COUNT(*) AS NumOfPurchase
    FROM PERSON AS P1, STORE_ORDER as SO
    WHERE P1.PID IN 
        (
            SELECT TOP 5 P.PID AS PID1 
            FROM PERSON AS P, GOLD_CUST AS G
            WHERE P.PID = G.GoldPID AND 
            (SELECT COUNT(*)
            FROM STORE_ORDER as SO
            WHERE G.GoldPID = SO.PID AND 
            SO.DatePurchase >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 1, 0)
            ) >= 12
            GROUP BY P.PID
        )
    AND P1.PID = SO.PID
    GROUP BY P1.PID
) AS Counts
GO

--> QUERY 4
SELECT TOP 1 PE.ExpiraryDate, COUNT(*) AS PeriItemCount, PE.PerishableProductID
FROM STORE_ORDER AS SO, PERI_PRODUCT AS PE
WHERE SO.ProductID = PE.PerishableProductID
GROUP BY PE.PerishableProductID, PE.ExpiraryDate
ORDER BY COUNT(*) DESC
GO

--> QUERY 5
SELECT S.SupplierID, S.SupplierName, S.SupplierLocation, S.SupplierPhoneNo
FROM PRODUCT AS P, SUPPLIER AS S
WHERE P.ProductQuantity = 0 AND P.ProductSupplierID = S.SupplierID
GO

--> QUERY 6
SELECT COUNT(*) AS TotalTrans, S.StoreID, S.StoreName
FROM STORE AS S, STORE_ORDER AS SO
WHERE S.StoreID = SO.StoreID
GROUP BY S.StoreID, S.StoreName
ORDER BY COUNT(*) DESC
GO

--> QUERY 7
SELECT DISTINCT PAY.EmployeePID, P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState
FROM PERSON AS P, PHONE_NUMBER AS PH, 
PRSN_ADDRESS AS PA, EMPLOYEE AS E, PAY AS PAY
WHERE PH.PID=P.PID AND 
PA.PID=P.PID AND
E.EmployeePID=P.PID AND 
PAY.EmployeePID = E.EmployeePID AND 
E.EmployeePID=P.PID AND
PAY.PayDate >= DATEADD(WEEK, DATEDIFF(WEEK, 0, GETDATE()) - 1, 0)
GROUP BY PAY.EmployeePID, P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState
HAVING COUNT(*) =7
GO

--> QUERY 8
SELECT COUNT(NumCust) AS CustBuyPopProd
FROM
(
    SELECT SO.PID, COUNT(*) AS NumCust
    FROM STORE_ORDER AS SO, TOP_POPULAR_PRODUCT AS TP
    WHERE SO.ProductID = TP.ProductID 
    GROUP BY SO.PID
) AS CustList
GO

--> QUERY 9
SELECT SO.CashierPID, SO.StoreID, SO.ProductID, SO.PID, SO.StoreBillId, SO.BillAmount, SO.DatePurchase, SO.PaymentMethod
FROM STORE_ORDER AS SO
WHERE SO.DatePurchase >= (
                            SELECT TOP 1 E.CurrStartDate
                            FROM EMPLOYEE AS E
                            ORDER BY E.CurrStartDate DESC
                        )
GO

-- QUERY 10
SELECT DISTINCT P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState
FROM PERSON AS P, PHONE_NUMBER AS PH, PRSN_ADDRESS AS PA, EMPLOYEE AS E, GOLD_CUST AS G
WHERE PH.PID=P.PID AND PA.PID=P.PID AND E.EmployeePID=P.PID AND
E.GoldPID=G.GoldPID AND 
G.CardIssueDate BETWEEN E.CurrStartDate AND DATEADD(MONTH, 1, E.CurrStartDate)
GO

-- QUERY 11
SELECT V1.VoucherID
FROM VOUCHER AS V1
WHERE V1.VoucherID IN (
                        SELECT TOP 1 V.VoucherID
                        FROM VOUCHER AS V, BUY 
                        WHERE V.VoucherID = BUY.VoucherID
                        GROUP BY V.VoucherID
                        ORDER BY COUNT(*) DESC
                        )
GROUP BY V1.VoucherID
GO

-- QUERY 12
SELECT DISTINCT S.SilverPID, P.Fname, P.Mname, P.Lname, P.Gender, PH.PhoneNo, PA.AdStreet, PA.AdCity, PA.AdState
FROM SILVER_CUST AS S, PERSON AS P, PHONE_NUMBER AS PH, PRSN_ADDRESS AS PA
WHERE PH.PID=P.PID AND PA.PID=P.PID and P.PID=S.SilverPID AND
S.DateOfJoin >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 5, 0)
GO

--QUERY 13
SELECT PG.PID, COUNT(*) AS NumOfPurchase
FROM POTENTIAL_GOLD_CUST AS PG, STORE_ORDER AS SO
WHERE PG.PID = SO.PID AND 
SO.DatePurchase >= DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()) - 1, 0)
GROUP BY PG.PID
GO

--QUERY 14
SELECT MAX(SO.BillAmount) AS MaxBillAmount, ST.StoreID, ST.StoreName, ST.StoreState, ST.StoreCity, ST.StoreStreet
FROM STORE AS ST, STORE_ORDER AS SO
WHERE ST.StoreID IN (
                        SELECT TOP 1 SO.StoreID
                        FROM STORE AS S, STORE_ORDER AS SO
                        WHERE S.StoreID = SO.StoreID
                        GROUP BY SO.StoreID
                        ORDER BY COUNT(*) DESC
                    )
GROUP BY ST.StoreID, ST.StoreName, ST.StoreState, ST.StoreCity, ST.StoreStreet
GO

--QUERY 15
SELECT SO.DatePurchase, SO.BillAmount
FROM STORE_ORDER AS SO
WHERE SO.BillAmount >= (
                        SELECT AVG(SO.BillAmount)
                        FROM STORE_ORDER AS SO
                        )
GO