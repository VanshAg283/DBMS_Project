Insert Into Portfolio (portfolioID,desName) Values ('Xfepz','magnam');  
Insert Into Portfolio (portfolioID, desName) Values ('aNPmG','soluta');  
Insert Into Portfolio (portfolioID, desName) Values ('JOrWa','quibusdam');  
Insert Into Portfolio (portfolioID, desName) Values ('hbbzK','provident');  
Insert Into Portfolio (portfolioID, desName) Values ('fLwqV','ducimus');  
Insert Into Portfolio (portfolioID, desName) Values ('zRhTW','omnis');  
Insert Into Portfolio (portfolioID, desName) Values ('kSMVb','quaerat');  
Insert Into Portfolio (portfolioID, desName) Values ('mmSnz','rerum');  
Insert Into Portfolio (portfolioID, desName) Values ('AqlOX','assumenda');  
Insert Into Portfolio (portfolioID, desName) Values ('MKZOu','animi');  
Insert Into Portfolio (portfolioID, desName) Values ('EcBOS','fugit');  
Insert Into Portfolio (portfolioID, desName) Values ('cPZbP','nihil');  
Insert Into Portfolio (portfolioID, desName) Values ('athvf','ullam');  
Insert Into Portfolio (portfolioID, desName) Values ('lrsAp','sunt');  
Insert Into Portfolio (portfolioID, desName) Values ('khOpW','quas');  
Insert Into Portfolio (portfolioID, desName) Values ('tmVxq','cumque');  
Insert Into Portfolio (portfolioID, desName) Values ('OVxDc','minima');  
Insert Into Portfolio (portfolioID, desName) Values ('AUuyD','impedit');  
Insert Into Portfolio (portfolioID, desName) Values ('YaBPi','error');  
Insert Into Portfolio (portfolioID, desName) Values ('sBOQd','cum');  

--- Update likes in Portfolio
UPDATE Portfolio p
SET likes = (
    SELECT COUNT(l.productID)
    FROM Likes l
    WHERE l.productID IN (
        SELECT productID
        FROM Product
        WHERE portfolioID = p.portfolioID
    )
);