SELECT DISTINCT AR.ProductID
FROM ASSIGNMENT AS ASS, FLOOR_STAFF AS F, ARRANGEMENT AS AR, PERI_PRODUCT AS PE1
WHERE ASS.EmployeePID = F.FloorStaffPID AND F.FloorStaffPID = AR.FloorStaffPID AND 
                AR.ProductID = PE1.PerishableProductID
                GROUP BY ASS.StoreID, AR.ProductID
