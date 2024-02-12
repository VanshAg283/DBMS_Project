Insert Into Designer (desName, email, password, firstname, lastname) Values ('magnam', 'Subhasini.Guha@yahoo.co.in', '2b602ad0', 'Subhasini', 'Guha');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('soluta', 'Manjusha.Abbott82@hotmail.com', '-62f628b0', 'Manjusha', 'Abbott');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('quibusdam', 'Laxmi_Bhat@gmail.com', '58ca32b7', 'Laxmi', 'Bhat');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('provident', 'Bodhan68@gmail.com', '6cc0d444', 'Bodhan', 'Sinha');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('ducimus', 'Daevika.Khatri46@yahoo.co.in', '-2a801291', 'Daevika', 'Khatri');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('omnis', 'Bishnu91@hotmail.com', '4df1ec2d', 'Bishnu', 'Adiga');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('quaerat', 'Gurdev_Dwivedi@gmail.com', '-53b7bf9b', 'Gurdev', 'Dwivedi');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('rerum', 'Gati41@yahoo.co.in', '2829949f', 'Gati', 'Pandey');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('assumenda', 'Divjot.Bharadwaj@gmail.com', '3f73cd3d', 'Divjot', 'Bharadwaj');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('animi', 'Mohan1@gmail.com', '69ef13ce', 'Mohan', 'Sinha');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('fugit', 'Kamlesh_Panicker@hotmail.com', '2cae3f8d', 'Kamlesh', 'Panicker');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('nihil', 'Purushottam_Joshi@yahoo.co.in', '-74c6756a', 'Purushottam', 'Joshi');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('ullam', 'Sharda.Chopra61@gmail.com', '-200cca4b', 'Sharda', 'Chopra');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('sunt', 'Naveen.Chaturvedi53@gmail.com', '-afa547', 'Naveen', 'Chaturvedi');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('quas', 'Dev77@yahoo.co.in', '7473a905', 'Dev', 'Pillai');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('cumque', 'Avani_Johar@yahoo.co.in', '-71dbc89f', 'Avani', 'Johar');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('minima', 'Gautami70@yahoo.co.in', '-45c25007', 'Gautami', 'Kakkar');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('impedit', 'Divya15@gmail.com', '-30b45dbc', 'Divya', 'Iyengar');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('error', 'Vasudeva59@gmail.com', '5afe560f', 'Vasudeva', 'Sinha');  
Insert Into Designer (desName, email, password, firstname, lastname) Values ('cum', 'Chandrani30@hotmail.com', '1a8cb536', 'Chandrani', 'Chattopadhyay');  


--- Updating portfolioID in Designer
UPDATE Designer
    SET portfolioID = (
    SELECT portfolioID FROM portfolio
    where designer.desName = portfolio.desName
);