# 数据库建表
# Flight:
CREATE TABLE `Flight`(
	`flightNumber` VARCHAR(20) NOT NULL PRIMARY KEY,
	`sharedFlightNumber` VARCHAR(20),
	`sharedFlightName` VARCHAR(20),
	`airlineCode` VARCHAR(10),
	`airlineName` VARCHAR(20),
	`craftTypeCode` VARCHAR(10),
	`craftKind` VARCHAR(4),
	`craftTypeName` VARCHAR(30),
	`craftTypeKindDisplayName` VARCHAR(20),
	`specialCraft` BOOLEAN,
	`createdTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	);

# AirportInfo:
CREATE TABLE `AirportInfo`(
	`flightNumber` VARCHAR(20) NOT NULL PRIMARY KEY,
	`dcityTlc` VARCHAR(10),
	`dcityName` VARCHAR(20),
	`dairportTlc` VARCHAR(10),
	`dairportName` VARCHAR(30),
	`dterminalName` VARCHAR(10),
	`acityTlc` VARCHAR(10),
	`acityName` VARCHAR(20),
	`aairportTlc` VARCHAR(10),
	`aairportName` VARCHAR(30),
	`aterminalName` VARCHAR(10),
	`departureDate` DATETIME,
	`arrivalDate` DATETIME,
	`comfortHistoryPunctuality` INT,
	`comfortHistoryPunctualityArr` INT,
	`createdTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	);

# CharacteristicsPrice:
CREATE TABLE `CharacteristicsPrice`(
	`flightNumber` VARCHAR(20) NOT NULL PRIMARY KEY,
	`lowestPrice` INT,
	`lowestCfPrice` INT,
	`standardPriceY` INT,
	`standardPriceC` INT,
	`standardPriceF` INT,
	`lowestSalePriceY` INT,
	`lowestSalePriceC` INT,
	`lowestSalePriceF` INT,
	`lowestRateY` FLOAT(3,2),
	`lowestRateC` FLOAT(3,2),
	`lowestRateF` FLOAT(3,2),
	`createdTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
	);
