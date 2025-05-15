-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (aarch64)
--
-- Host: localhost    Database: BarbotDB
-- ------------------------------------------------------
-- Server version       10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cocktail`
--

DROP TABLE IF EXISTS `Cocktail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cocktail` (
  `CocktailID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Beschreibung` varchar(250) DEFAULT NULL,
  `ExtLink` varchar(200) DEFAULT NULL,
  `Bild` blob DEFAULT NULL,
  PRIMARY KEY (`CocktailID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cocktail`
--

LOCK TABLES `Cocktail` WRITE;
/*!40000 ALTER TABLE `Cocktail` DISABLE KEYS */;
INSERT INTO `Cocktail` VALUES
(1,'Ipanema',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Cocktail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rezept`
--

DROP TABLE IF EXISTS `Rezept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Rezept` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CocktailID` int(11) NOT NULL,
  `RezeptPos` int(11) NOT NULL,
  `ZutatID` int(11) NOT NULL,
  `Menge` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_RezeptCocktail` (`CocktailID`),
  KEY `FK_RezeptZutat` (`ZutatID`),
  CONSTRAINT `FK_RezeptCocktail` FOREIGN KEY (`CocktailID`) REFERENCES `Cocktail` (`CocktailID`),
  CONSTRAINT `FK_RezeptZutat` FOREIGN KEY (`ZutatID`) REFERENCES `Zutat` (`ZutatID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rezept`
--

LOCK TABLES `Rezept` WRITE;
/*!40000 ALTER TABLE `Rezept` DISABLE KEYS */;
INSERT INTO `Rezept` VALUES
(1,1,1,1,100),
(2,1,2,2,20);
/*!40000 ALTER TABLE `Rezept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Zapfstelle`
--

DROP TABLE IF EXISTS `Zapfstelle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Zapfstelle` (
  `ZapfstelleID` int(11) NOT NULL AUTO_INCREMENT,
  `SchienenPos` int(11) NOT NULL,
  `Pumpe` tinyint(1) DEFAULT NULL,
  `PumpenNR` int(11) DEFAULT NULL,
  `Fuellmenge` int(11) DEFAULT NULL,
  PRIMARY KEY (`ZapfstelleID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Zapfstelle`
--

LOCK TABLES `Zapfstelle` WRITE;
/*!40000 ALTER TABLE `Zapfstelle` DISABLE KEYS */;
INSERT INTO `Zapfstelle` VALUES
(1,50,1,1,NULL),
(2,100,1,4,NULL),
(3,1,1,2,100);
/*!40000 ALTER TABLE `Zapfstelle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Zutat`
--

DROP TABLE IF EXISTS `Zutat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Zutat` (
  `ZutatID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) DEFAULT NULL,
  `Zapfstelle` int(11) DEFAULT NULL,
  `Alkohol` tinyint(1) NOT NULL,
  PRIMARY KEY (`ZutatID`),
  KEY `FK_ZutatenZapfstelle` (`Zapfstelle`),
  CONSTRAINT `FK_ZutatenZapfstelle` FOREIGN KEY (`Zapfstelle`) REFERENCES `Zapfstelle` (`ZapfstelleID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Zutat`
--

LOCK TABLES `Zutat` WRITE;
/*!40000 ALTER TABLE `Zutat` DISABLE KEYS */;
INSERT INTO `Zutat` VALUES
(1,'Ginger Ale',1,0),
(2,'Maracujasaft',2,0);
/*!40000 ALTER TABLE `Zutat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15  8:39:11
