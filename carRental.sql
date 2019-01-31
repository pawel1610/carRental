CREATE DATABASE carRental;
#drop DATABASE carRental;
#drop table ;
USE carRental;

CREATE TABLE carRental.users (
  user_id INT NOT NULL AUTO_INCREMENT,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  login VARCHAR(30) NOT NULL UNIQUE,
  passw TEXT NOT NULL,
  adress TEXT  NOT NULL,
  phone BIGINT NOT NULL,
  type SET('admin', 'customer') NOT NULL,
  PRIMARY  KEY (user_id));
  


CREATE TABLE carRental.cars (
  car_id INT NOT NULL AUTO_INCREMENT,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  class SET('mini', 'compact', 'medium', 'standard', 'premium') NOT NULL,
  year INT NOT NULL,
  reg_nr TEXT NOT NULL,
  price  FLOAT NOT NULL,
  PRIMARY KEY (car_id));
  
CREATE TABLE carRental.rents (
  rent_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  car_id INT NOT NULL,
  order_date DATE NOT NULL,
  rent_start DATE NOT NULL,
  rent_end DATE NOT NULL,
  PRIMARY KEY (rent_id),
  INDEX car_id_idx (car_id ASC),
  INDEX user_id_idx (user_id ASC),
  CONSTRAINT car_id
    FOREIGN KEY (car_id)
    REFERENCES carRental.cars (car_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT user_id
    FOREIGN KEY (user_id)
    REFERENCES carRental.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

# #####################################


INSERT INTO users values(0,"admin", "admin","admin", "admin", "xxxxx", 000000000,"admin");
INSERT INTO users values(0,"Jan", "Kowalski","jan83", "zima", "ul.Nowa 1 02-869 Warszawa", 510033213,"customer");
INSERT INTO users values(0,"Michal", "Nowak","michal99", "mucha", "ul.Jasna 30 01-869 Wroclaw", 500555121,"customer");
INSERT INTO users values(0,"Ryszard", "Kaczynski","rysiek12", "kot", "ul.Krotka 2 32-449 Pila", 586999125,"customer");
INSERT INTO users values(0,"Piotr", "Janik","Janeczek", "12345", "ul.Wiejska 455 01-001 Warszawa", 533034277,"customer");
INSERT INTO users values(0,"Hanna", "Piotrowska","hanka123", "czolg", "ul.Mila 7A 55-500 Wronki", 550033255,"customer");



INSERT INTO cars values(0,"Skoda", "CitiGo", "mini", 2017, "WW65666", 90);
INSERT INTO cars values(0,"Fiat", "500", "mini", 2018, "WW64556", 110);
INSERT INTO cars values(0,"Skoda", "Fabia", "compact", 2017, "WW64777", 150);
INSERT INTO cars values(0,"VW", "Polo", "compact", 2018, "WN5647L", 160);
INSERT INTO cars values(0,"VW", "Golf", "medium", 2019, "WW89897", 200);
INSERT INTO cars values(0,"Ford", "Focus", "medium", 2018, "WN44588", 200);
INSERT INTO cars values(0,"VW", "Passat", "standard", 2018, "WW77889", 250);
INSERT INTO cars values(0,"Opel", "Insignia", "standard", 2018, "WW33211", 260);
INSERT INTO cars values(0,"Audi", "A6", "premium", 2018, "WW99999", 400);
INSERT INTO cars values(0,"BMW", "530", "premium", 2017, "WW12222", 430);


INSERT INTO cars values(0,'mercedes','s500','premium',2019,'ww34234',600);



INSERT INTO rents values(0,4,7,'2019-01-31','2019-03-10','2019-03-17');
INSERT INTO rents values(0,2,3,'2019-01-31','2019-02-01','2019-02-27');
INSERT INTO rents values(0,3,5,'2019-01-31','2019-02-14','2019-02-15');


select * from users;
select * from cars;
select * from rents;


SELECT * from rents, users WHERE rents.user_id = users.user_id and users.login = jan83;








