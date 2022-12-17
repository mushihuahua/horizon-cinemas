-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: Horizon Cinemas
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Booking`
--

DROP TABLE IF EXISTS `Booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Booking` (
  `booking_reference` int NOT NULL,
  `booking_date` date NOT NULL,
  `number_of_tickets` int NOT NULL,
  `cancelled` tinyint NOT NULL,
  `total_cost` int DEFAULT NULL,
  PRIMARY KEY (`booking_reference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Booking`
--

LOCK TABLES `Booking` WRITE;
/*!40000 ALTER TABLE `Booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `Booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cinema`
--

DROP TABLE IF EXISTS `Cinema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cinema` (
  `cinema_ID` int NOT NULL,
  `location` varchar(45) NOT NULL,
  `city_ID` int NOT NULL,
  PRIMARY KEY (`cinema_ID`),
  KEY `city_ID_idx` (`city_ID`),
  CONSTRAINT `city_ID` FOREIGN KEY (`city_ID`) REFERENCES `mydb`.`City` (`city_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cinema`
--

LOCK TABLES `Cinema` WRITE;
/*!40000 ALTER TABLE `Cinema` DISABLE KEYS */;
/*!40000 ALTER TABLE `Cinema` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cinema_Listings`
--

DROP TABLE IF EXISTS `Cinema_Listings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cinema_Listings` (
  `cinema_ID` int NOT NULL,
  `listing_ID` int NOT NULL,
  PRIMARY KEY (`cinema_ID`,`listing_ID`),
  KEY `listing_ID_idx` (`listing_ID`),
  CONSTRAINT `fk_Cinema_Listings_1` FOREIGN KEY (`cinema_ID`) REFERENCES `Cinema` (`cinema_ID`),
  CONSTRAINT `fk_Cinema_Listings_2` FOREIGN KEY (`listing_ID`) REFERENCES `Listing` (`listing_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cinema_Listings`
--

LOCK TABLES `Cinema_Listings` WRITE;
/*!40000 ALTER TABLE `Cinema_Listings` DISABLE KEYS */;
/*!40000 ALTER TABLE `Cinema_Listings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `City`
--

DROP TABLE IF EXISTS `City`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `City` (
  `city_ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `morning_price` int DEFAULT NULL,
  `afternoon_price` int DEFAULT NULL,
  `evening_price` int DEFAULT NULL,
  PRIMARY KEY (`city_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `City`
--

LOCK TABLES `City` WRITE;
/*!40000 ALTER TABLE `City` DISABLE KEYS */;
/*!40000 ALTER TABLE `City` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Listing`
--

DROP TABLE IF EXISTS `Listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Listing` (
  `listing_ID` int NOT NULL,
  `film_name` varchar(45) NOT NULL,
  `film_date` datetime NOT NULL,
  `film_description` varchar(256) NOT NULL,
  `actor_details` varchar(256) NOT NULL,
  `film_genre` varchar(45) NOT NULL,
  `film_age` varchar(45) NOT NULL,
  `film_rating` int NOT NULL,
  PRIMARY KEY (`listing_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Listing`
--

LOCK TABLES `Listing` WRITE;
/*!40000 ALTER TABLE `Listing` DISABLE KEYS */;
/*!40000 ALTER TABLE `Listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Screen`
--

DROP TABLE IF EXISTS `Screen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Screen` (
  `screen_number` int NOT NULL,
  `capacity` int NOT NULL,
  `show_ID` int DEFAULT NULL,
  `cinema_ID` int NOT NULL,
  PRIMARY KEY (`screen_number`),
  KEY `show_ID_idx` (`show_ID`),
  KEY `cinema_ID_idx` (`cinema_ID`),
  CONSTRAINT `fk_Screen_1` FOREIGN KEY (`show_ID`) REFERENCES `Show` (`show_ID`),
  CONSTRAINT `fk_Screen_2` FOREIGN KEY (`cinema_ID`) REFERENCES `Cinema` (`cinema_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Screen`
--

LOCK TABLES `Screen` WRITE;
/*!40000 ALTER TABLE `Screen` DISABLE KEYS */;
/*!40000 ALTER TABLE `Screen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seat`
--

DROP TABLE IF EXISTS `Seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seat` (
  `seat_number` int NOT NULL,
  `available` tinyint NOT NULL,
  `seat_type` varchar(45) NOT NULL,
  `screen_number` int NOT NULL,
  PRIMARY KEY (`seat_number`),
  KEY `screen_number_idx` (`screen_number`),
  CONSTRAINT `fk_Seat_1` FOREIGN KEY (`screen_number`) REFERENCES `Screen` (`screen_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seat`
--

LOCK TABLES `Seat` WRITE;
/*!40000 ALTER TABLE `Seat` DISABLE KEYS */;
/*!40000 ALTER TABLE `Seat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Show`
--

DROP TABLE IF EXISTS `Show`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Show` (
  `show_ID` int NOT NULL,
  `show_date` date NOT NULL,
  `show_time` varchar(45) NOT NULL,
  `listing_ID` int NOT NULL,
  `screen_number` int NOT NULL,
  PRIMARY KEY (`show_ID`),
  KEY `listing_ID_idx` (`listing_ID`),
  KEY `screen_number_idx` (`screen_number`),
  CONSTRAINT `fk_Show_1` FOREIGN KEY (`listing_ID`) REFERENCES `Listing` (`listing_ID`),
  CONSTRAINT `fk_Show_2` FOREIGN KEY (`screen_number`) REFERENCES `Screen` (`screen_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Show`
--

LOCK TABLES `Show` WRITE;
/*!40000 ALTER TABLE `Show` DISABLE KEYS */;
/*!40000 ALTER TABLE `Show` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Staff`
--

DROP TABLE IF EXISTS `Staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `employee_ID` int NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `cinema_ID` int NOT NULL,
  PRIMARY KEY (`employee_ID`),
  KEY `cinema_ID_idx` (`cinema_ID`),
  CONSTRAINT `cinema_ID` FOREIGN KEY (`cinema_ID`) REFERENCES `mydb`.`Cinema` (`cinema_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ticket`
--

DROP TABLE IF EXISTS `Ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ticket` (
  `ticket_ID` int NOT NULL,
  `ticket_type` varchar(45) NOT NULL,
  `booking_reference` int NOT NULL,
  `seat_number` int NOT NULL,
  PRIMARY KEY (`ticket_ID`),
  KEY `booking_reference_idx` (`booking_reference`),
  KEY `seat_number_idx` (`seat_number`),
  CONSTRAINT `fk_Ticket_1` FOREIGN KEY (`booking_reference`) REFERENCES `Booking` (`booking_reference`),
  CONSTRAINT `fk_Ticket_2` FOREIGN KEY (`seat_number`) REFERENCES `Seat` (`seat_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ticket`
--

LOCK TABLES `Ticket` WRITE;
/*!40000 ALTER TABLE `Ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ticket` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-17 20:30:42
