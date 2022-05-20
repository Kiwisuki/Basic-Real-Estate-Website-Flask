#@(#) script.ddl

DROP TABLE IF EXISTS Media;
DROP TABLE IF EXISTS Viewed_Ads;
DROP TABLE IF EXISTS Premises;
DROP TABLE IF EXISTS Plots;
DROP TABLE IF EXISTS Houses;
DROP TABLE IF EXISTS Garages;
DROP TABLE IF EXISTS Flats;
DROP TABLE IF EXISTS Login_Sessions;
DROP TABLE IF EXISTS Notification_Options;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Advertisements;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Login_Devices;

CREATE TABLE Login_Devices
(
	Agent char (255),
	Ip char (255),
	Device_id char (255),
	PRIMARY KEY(Device_id)
);

CREATE TABLE Users
(
	Email char (255) NOT NULL,
	User_password char (255) NOT NULL,
	Phone_number char (255),
  	Email_notification boolean,
	Phone_notification boolean,
	PRIMARY KEY(Email)
);

CREATE TABLE Advertisements
(
	Ad_id char (255),
	Upload_date date,
	Expire_date date,
	Ad_description char (255),
	Price float NOT NULL,
	Ad_type char (255) NOT NULL,
	fk_User_Email char (255) NOT NULL,
	Ad_name char (255) NOT NULL,
	PRIMARY KEY(Ad_id),
	CHECK(Ad_type in ('Sale', 'Rent')),
	FOREIGN KEY(fk_User_Email) REFERENCES Users (Email)
);

CREATE TABLE Messages
(
	Message_id CHAR (255),
	Message_text char (255) NOT NULL,
	Sent_date date NOT NULL,
	fk_Sender_Email char (255) NOT NULL,
	fk_Receiver_Email char (255) NOT NULL,
	PRIMARY KEY(Message_id),
	FOREIGN KEY(fk_Sender_Email) REFERENCES Users (Email),
	FOREIGN KEY(fk_Receiver_Email) REFERENCES Users (Email)
);

CREATE TABLE Login_Sessions
(
	Login_session_id char (255),
	fk_Login_device_Device_id char (255) NOT NULL,
	fk_User_Email char (255) NOT NULL,
	PRIMARY KEY(Login_session_id),
	FOREIGN KEY(fk_Login_device_Device_id) REFERENCES Login_Devices (Device_id),
	FOREIGN KEY(fk_User_Email) REFERENCES Users (Email)
);

CREATE TABLE Flats
(
	Address_line char (255) NOT NULL,
	Area float NOT NULL,
	No_rooms int (255),
	Floor_on int (255),
	Floor_max int (255),
	Year_built int (255),
	Year_renovated int (255),
	Flat_id char (255),
	City char (255) NOT NULL,
	Building_type char (255),
	Finish char (255),
	Heating char (255),
	Energy_class char (255),
	Furnitured char (255),
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(Flat_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Garages
(
	Address_line char (255) NOT NULL,
	Area float NOT NULL,
	Cars_fit int (255),
	Hole boolean,
	Garage_id char (255),
	City char (255) NOT NULL,
	Building_type char (255),
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(Garage_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Houses
(
	Address_line char (255) NOT NULL,
	Area float NOT NULL,
	Floors int (255),
	Rooms int (255),
	Plot_Area float NOT NULL,
	Year_built int (255),
	Year_renovated int (255),
	House_id char (255),
	City char (255) NOT NULL,
	House_type char (255),
	Building_type char (255),
	Finish char (255),
	Heating char (255),
	Energy_class char (255),
	Furnitured char (255),
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(House_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Plots
(
	Address_line char (255) NOT NULL,
	Area float NOT NULL,
	Plot_id char (255),
	City char (255) NOT NULL,
	Designation char (255),
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(Plot_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Premises
(
	Address_line char (255) NOT NULL,
	Area float NOT NULL,
	Floor_on int (255),
  	Floor_max int (255),
	Year_built int (255),
	Year_renovated int (255),
	Premise_id char (255),
	City char (255) NOT NULL,
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(Premise_id),
	UNIQUE(fk_Advertisement_Ad_id),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Viewed_Ads
(
	id_Viewed_ad char (255),
	fk_User_Email char (255) NOT NULL,
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(id_Viewed_ad),
	FOREIGN KEY(fk_User_Email) REFERENCES Users (Email),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);

CREATE TABLE Media
(
	link char (255),
	Media_type char (255),
	fk_House_House_id char (255),
	fk_Garage_Garage_id char (255),
	fk_Plot_Plot_id char (255),
	fk_Premises_Premise_id char (255),
	fk_Flat_Flat_id char (255),
	PRIMARY KEY(link),
	FOREIGN KEY(fk_House_House_id) REFERENCES Houses (House_id),
	FOREIGN KEY(fk_Garage_Garage_id) REFERENCES Garages (Garage_id),
	FOREIGN KEY(fk_Plot_Plot_id) REFERENCES Plots (Plot_id),
	FOREIGN KEY(fk_Premises_Premise_id) REFERENCES Premises (Premise_id),
	FOREIGN KEY(fk_Flat_Flat_id) REFERENCES Flats (Flat_id)
);

CREATE TABLE Saved_Ads
(
	Saved_ad_id char (255),
	fk_User_Email char (255) NOT NULL,
	fk_Advertisement_Ad_id char (255) NOT NULL,
	PRIMARY KEY(Saved_ad_id),
	FOREIGN KEY(fk_User_Email) REFERENCES Users (Email),
	FOREIGN KEY(fk_Advertisement_Ad_id) REFERENCES Advertisements (Ad_id)
);
