#@(#) script.ddl

DROP TABLE IF EXISTS Media;
DROP TABLE IF EXISTS Viewed_ad;
DROP TABLE IF EXISTS Premises;
DROP TABLE IF EXISTS Plot;
DROP TABLE IF EXISTS House;
DROP TABLE IF EXISTS Garage;
DROP TABLE IF EXISTS Flat;
DROP TABLE IF EXISTS Session;
DROP TABLE IF EXISTS Notification_options;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Advertisement;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Login_device;

CREATE TABLE Login_device
(
	Agent char,
	Ip char,
	Device_id int,
	PRIMARY KEY(Device_id)
);

CREATE TABLE User
(
	Email char,
	Password char,
	Phone_number char,
	PRIMARY KEY(Email)
);

CREATE TABLE Advertisement
(
	Ad_id char,
	Upload_date date,
	Expire_date date,
	Description char,
	Price float,
	Ad_type char (4),
	fk_User_Email char NOT NULL,
	PRIMARY KEY(Ad_id),
	CHECK(Ad_type in ('Sale', 'Rent')),
	FOREIGN KEY(fk_User_Email) REFERENCES User (Email)
);

CREATE TABLE Message
(
	Message_id int,
	Text char,
	fk_Sender_Email char NOT NULL,
	fk_Receiver_Email char NOT NULL,
	PRIMARY KEY(Message_id),
	FOREIGN KEY(fk_Sender_Email) REFERENCES User (Email),
	FOREIGN KEY(fk_Receiver_Email) REFERENCES User (Email)
);

CREATE TABLE Notification_options
(
	Email_notification boolean,
	Phone_notification boolean,
	fk_User_Email char NOT NULL,
	PRIMARY KEY(null),
	UNIQUE(fk_User_Email),
	FOREIGN KEY(fk_User_Email) REFERENCES User (Email)
);

CREATE TABLE Session
(
	Session_id int,
	fk_Login_device_Device_id int NOT NULL,
	fk_User_Email char NOT NULL,
	PRIMARY KEY(Session_id),
	FOREIGN KEY(fk_Login_device_Device_id) REFERENCES Login_device (Device_id),
	FOREIGN KEY(fk_User_Email) REFERENCES User (Email)
);

CREATE TABLE Flat
(
	Address char,
	Area float,
	No_rooms int,
	Floor_on int,
	Floor_max int,
	Year_built int,
	Year_renovated int,
	Flat_id int,
	City char (11),
	Building_type char (10),
	Finish char (13),
	Heating char (18),
	Energy_class char (1),
	Furnitured char (4),
	fk_Advertisement_Ad_id char NOT NULL,
	CHECK(City in ('Vilnius', 'Kaunas', 'Klaipëda', 'Ðiauliai', 'Panëvëþys', 'Alytus', 'Marijampolë', 'Maþeikiai', 'Jonava', 'Kita')),
	CHECK(Building_type in ('Block', 'Monolithic', 'Brickwork', 'Wooden', 'Carcass', 'Other')),
	CHECK(Finish in ('Finished', 'Semi_finished', 'Unfinished', 'Unbuilt', 'Foundations', 'Other')),
	CHECK(Heating in ('Central', 'Central_collectral', 'Gas', 'Electric', 'Geothermal', 'Solid_fuel', 'Liquid_fuel', 'Aerothermal', 'Solar')),
	CHECK(Energy_class in ('A', 'B', 'C', 'D')),
	CHECK(Furnitured in ('Full', 'Semi', 'None')),
	PRIMARY KEY(Flat_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE Garage
(
	Address char,
	Area float,
	Cars_fit int,
	Hole boolean,
	Garage_id int,
	City char (11),
	Building_type char (10),
	fk_Advertisement_Ad_id char NOT NULL,
	CHECK(City in ('Vilnius', 'Kaunas', 'Klaipëda', 'Ðiauliai', 'Panëvëþys', 'Alytus', 'Marijampolë', 'Maþeikiai', 'Jonava', 'Kita')),
	CHECK(Building_type in ('Block', 'Monolithic', 'Brickwork', 'Wooden', 'Carcass', 'Other')),
	PRIMARY KEY(Garage_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE House
(
	Address char,
	Area float,
	Floors int,
	Plot_area float,
	Year_built int,
	Year_renovated int,
	House_id int,
	City char (11),
	House_type char (11),
	Building_type char (10),
	Finish char (13),
	Heating char (18),
	Energy_class char (1),
	Furnitured char (4),
	fk_Advertisement_Ad_id char NOT NULL,
	CHECK(City in ('Vilnius', 'Kaunas', 'Klaipëda', 'Ðiauliai', 'Panëvëþys', 'Alytus', 'Marijampolë', 'Maþeikiai', 'Jonava', 'Kita')),
	CHECK(House_type in ('Living', 'Part', 'Summerhouse', 'Farmstead', 'Block_house', 'Other')),
	CHECK(Building_type in ('Block', 'Monolithic', 'Brickwork', 'Wooden', 'Carcass', 'Other')),
	CHECK(Finish in ('Finished', 'Semi_finished', 'Unfinished', 'Unbuilt', 'Foundations', 'Other')),
	CHECK(Heating in ('Central', 'Central_collectral', 'Gas', 'Electric', 'Geothermal', 'Solid_fuel', 'Liquid_fuel', 'Aerothermal', 'Solar')),
	CHECK(Energy_class in ('A', 'B', 'C', 'D')),
	CHECK(Furnitured in ('Full', 'Semi', 'None')),
	PRIMARY KEY(House_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE Plot
(
	Address char,
	Area float,
	Plot_id int,
	City char (11),
	Designation char (12),
	fk_Advertisement_Ad_id char NOT NULL,
	CHECK(City in ('Vilnius', 'Kaunas', 'Klaipëda', 'Ðiauliai', 'Panëvëþys', 'Alytus', 'Marijampolë', 'Maþeikiai', 'Jonava', 'Kita')),
	CHECK(Designation in ('House', 'Storage', 'Forest', 'Commercial', 'Recreational', 'Farm', 'Other')),
	PRIMARY KEY(Plot_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE Premises
(
	Address char,
	Area float,
	Floor int,
	Year_built int,
	Year_renovated int,
	Premise_id int,
	City char (11),
	fk_Advertisement_Ad_id char NOT NULL,
	CHECK(City in ('Vilnius', 'Kaunas', 'Klaipëda', 'Ðiauliai', 'Panëvëþys', 'Alytus', 'Marijampolë', 'Maþeikiai', 'Jonava', 'Kita')),
	PRIMARY KEY(Premise_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE Viewed_ad
(
	Is_saved boolean,
	id_Viewed_ad integer,
	fk_User_Email char NOT NULL,
	fk_Advertisement_Ad_id char NOT NULL,
	PRIMARY KEY(id_Viewed_ad),
	FOREIGN KEY(fk_User_Email) REFERENCES User (Email),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisement (Ad_id)
);

CREATE TABLE Media
(
	link char,
	Media_type char (7),
	fk_House_House_id int,
	fk_Garage_Garage_id int,
	fk_Plot_Plot_id int,
	fk_Premises_Premise_id int,
	fk_Flat_Flat_id int,
	PRIMARY KEY(link),
	CHECK(Media_type in ('Photo', 'Video', '3D_tour')),
	FOREIGN KEY(fk_House_House_id) REFERENCES House (House_id),
	FOREIGN KEY(fk_Garage_Garage_id) REFERENCES Garage (Garage_id),
	FOREIGN KEY(fk_Plot_Plot_id) REFERENCES Plot (Plot_id),
	FOREIGN KEY(fk_Premises_Premise_id) REFERENCES Premises (Premise_id),
	FOREIGN KEY(fk_Flat_Flat_id) REFERENCES Flat (Flat_id)
);
