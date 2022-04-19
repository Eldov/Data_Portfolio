#Criando a Tabela Person_Person_R:
CREATE TABLE person_person_r(
BusinessEntityID INT PRIMARY KEY NOT NULL,
PersonType VARCHAR(10),
Title VARCHAR(10),
FirstName VARCHAR(50),
MiddleName VARCHAR(50),
LastName VARCHAR(50),
Suffix VARCHAR(10),
EmailPromotioN INT,
AdditionalContactInfo TEXT, 
Demographics VARCHAR(100),
rowguid VARCHAR(100),
ModifiedDate DATE
);

#Povoando a Tabela Person_Person_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Person_Person_R.csv' INTO TABLE smarttbot.person_person_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Person_Person_R:
SELECT * FROM smarttbot.person_person_r;

#Criando a Tabela Production_Product_R:
CREATE TABLE production_product_r(
ProductID INT PRIMARY KEY NOT NULL,
ProductName VARCHAR(100),
ProductNumber VARCHAR(20),
MakeFlag INT,
FinishedGoodsFlag INT,
Color VARCHAR(50),
SafetyStockLevel INT,
ReorderPoint INT,
StandardCost INT, 
ListPrice INT,
Size VARCHAR(20),
SizeUnitMeasureCode VARCHAR(20),
WeightUnitMeasureCode VARCHAR(20),
Weight FLOAT,
DaysToManufacture INT,
ProductLine VARCHAR(10),
Class VARCHAR(10),
Style VARCHAR(10),
ProductSubcategoryID INT,
ProductModelID INT,
SellStartDate DATE,
SellEndDate DATE,
rowguid VARCHAR(100),
ModifiedDate DATE
);

#Povoando a Tabela Production_Product_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Production_Product_R.csv' INTO TABLE smarttbot.production_product_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Production_Product_R:
SELECT * FROM smarttbot.production_product_r;

#Criando a Tabela Sales_Customer_R:
CREATE TABLE sales_customer_r(
CustomerID INT PRIMARY KEY NOT NULL,
PersonID INT,
StoreID INT,
TerritoryID INT,
AccountNumber VARCHAR(100),
rowguid VARCHAR(100),
ModifiedDate DATE,
FOREIGN KEY (PersonID) REFERENCES person_person_r(BusinessEntityID)
);

#Povoando a Tabela Sales_Customer_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Sales_Customer_R.csv' INTO TABLE smarttbot.sales_customer_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Sales_Customer_R:
SELECT * FROM smarttbot.sales_customer_r;

#Criando a Tabela Sales_Sales_Order_Detail_R:
CREATE TABLE sales_sales_order_detail_r(
SalesOrderDetailID INT PRIMARY KEY NOT NULL,
SalesOrderID INT PRIMARY KEY NOT NULL,
CarrierTrackingNumber VARCHAR(20),
OrderQty INT,
ProductID INT,
SpecialOfferID INT,
UnitPrice INT,
UnitPriceDiscount INT,
LineTotal FLOAT,
rowguid VARCHAR(100),
ModifiedDate DATE,
FOREIGN KEY (ProductID) REFERENCES production_product_r(ProductID),
FOREIGN KEY (SalesOrderID) REFERENCES sales_sales_order_header_r(SalesOrderID),
FOREIGN KEY (SpecialOfferID) REFERENCES sales_special_offer_product_r(SpecialOfferID)
);

#Povoando a Tabela Sales_Sales_Order_Detail_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Sales_SalesOrderDetail_R.csv' INTO TABLE smarttbot.sales_sales_order_detail_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Sales_Sales_Order_Detail_R:
SELECT * FROM smarttbot.sales_sales_order_detail_r;

#Criando a Tabela Sales_Sales_Order_Header_R:
CREATE TABLE sales_sales_order_header_r(
SalesOrderHeader_PK INT PRIMARY KEY NOT NULL,
SalesOrderID INT,
RevisionNumber INT,
OrderDate DATE,
DueDate DATE,
ShipDate DATE,
OnlineOrderFlag INT,
SalesOrderNumber VARCHAR(100),
PurchaseOrderNumber VARCHAR(100),
AccountNumber VARCHAR(100),
CustomerID INT,
SalesPersonID INT,
TerritoryID INT,
BillToAddressID INT,
ShipToAddressID INT,
ShipMethodID INT,
CreditCardID INT,
CreditCardApprovalCode VARCHAR(100),
CurrencyRateID INT,
SubTotal INT,
TaxAmt INT,
Freight INT,
TotalDue INT,
rowguid VARCHAR(100),
ModifiedDate DATE,
FOREIGN KEY (CustomerID) REFERENCES sales_customer_r(CustomerID)
);


#Povoando a Tabela Sales_Sales_Order_Header_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Sales_SalesOrderHeader_R.csv' INTO TABLE smarttbot.sales_sales_order_header_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Sales_Sales_Order_Header_R:
SELECT * FROM smarttbot.sales_sales_order_header_r;

#Criando a Tabela Sales_Special_Offer_Product_R:
CREATE TABLE sales_special_offer_product_r(
SpecialOfferID INT PRIMARY KEY NOT NULL,
ProductID INT PRIMARY KEY NOT NULL,
rowguid VARCHAR(100),
ModifiedDate DATE,
FOREIGN KEY (ProductID) REFERENCES production_product_r(ProductID)
);

#Povoando a Tabela Sales_Special_Offer_Product_R:
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Sales_SpecialOfferProduct_R.csv' INTO TABLE smarttbot.sales_special_offer_product_r
FIELDS TERMINATED BY ',' 
       OPTIONALLY ENCLOSED BY '"' 
   LINES TERMINATED BY '\r\n' 
   IGNORE 1 ROWS;

#Visualizando a Tabela Sales_Special_Offer_Product_R:
SELECT * FROM smarttbot.sales_special_offer_product_r;

/*Respondendo as Questões:
1. Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail
pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.*/

SELECT SalesOrderID, COUNT(*)
FROM sales_sales_order_detail_r
WHERE SalesOrderID 
GROUP BY SalesOrderID
HAVING SalesOrderID >= 3;

/*
2. Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct 
e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de 
OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).*/

SELECT ppr.ProductName AS Products,
	   sales_sales_order_detail_r.OrderQty AS Qty
FROM sales_sales_order_detail_r, production_product_r AS ppr
INNER JOIN sales_sales_order_detail_r AS ssodr ON ppr.ProductID = ssodr.ProductID
GROUP BY Products
ORDER BY Qty LIMIT 3;

/*3. Escreva uma query ligando as tabelas Person.Person, Sales.Customer e 
Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem 
de pedidos efetuados.*/
SELECT CONCAT(ppr.FirstName, ' ', ppr.MiddleName, ' ', ppr.LastName) AS FullName, 
       COUNT(*) AS Qty 
FROM sales_sales_order_header_r AS ssohr
	INNER JOIN sales_customer_r AS scr ON ssohr.CustomerID = scr.CustomerID
	INNER JOIN person_person_r AS ppr ON PersonID = ppr.BusinessEntityID 
GROUP BY FullName
ORDER BY Qty DESC;

/*4. Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e 
Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e 
OrderDate*/

SELECT ppr.ProductID AS ProductID,
		ppr.ProductName,
	SUM(ssodr.OrderQty) AS Qty,
    ssohr.OrderDate
FROM sales_sales_order_header_r AS ssohr
	INNER JOIN sales_sales_order_detail_r AS ssodr ON ssohr.SalesOrderID = ssodr.SalesOrderID
    INNER JOIN production_product_r AS ppr ON ssodr.ProductID = ppr.ProductID
GROUP BY ProductID
ORDER BY Qty DESC; 

/*5. Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela 
Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante 
o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido 
decrescente.*/

SELECT SalesOrderID,
	OrderDate,
    TotalDue
FROM sales_sales_order_header_r
WHERE MONTH(OrderDate) = 7 AND TotalDue >= 1000
ORDER BY TotalDue DESC;