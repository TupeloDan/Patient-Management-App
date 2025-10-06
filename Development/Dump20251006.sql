CREATE DATABASE  IF NOT EXISTS `PeopleAndLeaveDB` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `PeopleAndLeaveDB`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: PeopleAndLeaveDB
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `AppSettings`
--

DROP TABLE IF EXISTS `AppSettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AppSettings` (
  `SettingName` varchar(255) NOT NULL,
  `SettingValue` text,
  PRIMARY KEY (`SettingName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AppSettings`
--

LOCK TABLES `AppSettings` WRITE;
/*!40000 ALTER TABLE `AppSettings` DISABLE KEYS */;
INSERT INTO `AppSettings` VALUES ('AdminPassword','1476');
/*!40000 ALTER TABLE `AppSettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DelegatedStaff`
--

DROP TABLE IF EXISTS `DelegatedStaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DelegatedStaff` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `StaffID` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DelegatedStaff`
--

LOCK TABLES `DelegatedStaff` WRITE;
/*!40000 ALTER TABLE `DelegatedStaff` DISABLE KEYS */;
INSERT INTO `DelegatedStaff` VALUES (1,32),(2,17),(3,7),(4,2),(5,9),(6,1);
/*!40000 ALTER TABLE `DelegatedStaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LeaveLog`
--

DROP TABLE IF EXISTS `LeaveLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LeaveLog` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NHI` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `LeaveDate` datetime DEFAULT NULL,
  `LeaveType` varchar(255) DEFAULT NULL,
  `LeaveTime` datetime DEFAULT NULL,
  `ReturnTime` datetime DEFAULT NULL,
  `ExpectedReturnTime` datetime DEFAULT NULL,
  `MSE` tinyint(1) DEFAULT NULL,
  `Risk` tinyint(1) DEFAULT NULL,
  `LeaveCondition` tinyint(1) DEFAULT NULL,
  `AWOL` tinyint(1) DEFAULT NULL,
  `OwnPhone` tinyint(1) DEFAULT NULL,
  `ContactPhoneNumber` varchar(255) DEFAULT NULL,
  `HasContactInfo` tinyint(1) DEFAULT NULL,
  `SeniorNurseNotified` int DEFAULT NULL,
  `SeniorNurseID` int DEFAULT NULL,
  `StaffNurseID` int DEFAULT NULL,
  `StaffResponsibleID` int DEFAULT NULL,
  `SignedInByID` int DEFAULT NULL,
  `IsSpecialPatient` tinyint(1) DEFAULT NULL,
  `Is Escorted` tinyint(1) DEFAULT NULL,
  `FileName` varchar(255) DEFAULT NULL,
  `LeaveDescription` text,
  `DurationMinutes` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_nhi` (`NHI`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LeaveLog`
--

LOCK TABLES `LeaveLog` WRITE;
/*!40000 ALTER TABLE `LeaveLog` DISABLE KEYS */;
INSERT INTO `LeaveLog` VALUES (1,'GGG1234','James O\'Reilly','2025-10-06 00:00:00','EGA','2025-10-06 12:53:41',NULL,'2025-10-06 13:23:41',1,1,1,1,NULL,'0212298113',1,1,32,29,29,NULL,1,1,'GGG1234-LeaveEvent-1-06-Oct-25.pdf','ffff',30);
/*!40000 ALTER TABLE `LeaveLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MHA_Sections`
--

DROP TABLE IF EXISTS `MHA_Sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MHA_Sections` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `LegalStatus` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MHA_Sections`
--

LOCK TABLES `MHA_Sections` WRITE;
/*!40000 ALTER TABLE `MHA_Sections` DISABLE KEYS */;
INSERT INTO `MHA_Sections` VALUES (1,'24(2)(a)'),(2,'25 (1)(a)'),(3,'45/30'),(4,'45/13'),(5,'30'),(6,'45/11'),(7,'45/14'),(8,'45/16');
/*!40000 ALTER TABLE `MHA_Sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Notices`
--

DROP TABLE IF EXISTS `Notices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Notices` (
  `NoticeID` int NOT NULL AUTO_INCREMENT,
  `NoticeText` text,
  `ExpiryDate` datetime DEFAULT NULL,
  PRIMARY KEY (`NoticeID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notices`
--

LOCK TABLES `Notices` WRITE;
/*!40000 ALTER TABLE `Notices` DISABLE KEYS */;
INSERT INTO `Notices` VALUES (1,'New Admission expected this Thursday 18/9','2025-09-30 00:00:00'),(2,'BBQ Next Thursday 25/9','2025-09-26 00:00:00'),(3,'Test Note','2025-10-09 00:00:00'),(4,'Test Notice','2025-10-14 00:00:00'),(5,'New Notice','2025-10-08 00:00:00');
/*!40000 ALTER TABLE `Notices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `People`
--

DROP TABLE IF EXISTS `People`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `People` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Room` varchar(255) DEFAULT NULL,
  `NHI` varchar(255) DEFAULT NULL,
  `PersonName` varchar(255) DEFAULT NULL,
  `LegalStatusID` int DEFAULT NULL,
  `TreatmentPlans` datetime DEFAULT NULL,
  `HoNos` datetime DEFAULT NULL,
  `UDSDue` datetime DEFAULT NULL,
  `RelSecurity` tinyint(1) DEFAULT NULL,
  `Profile` tinyint(1) DEFAULT NULL,
  `Metobolic` tinyint(1) DEFAULT NULL,
  `Bloods` tinyint(1) DEFAULT NULL,
  `FlightRisk` tinyint(1) DEFAULT NULL,
  `Progress%` double DEFAULT NULL,
  `UDSFrequency` varchar(255) DEFAULT NULL,
  `LastUDS` datetime DEFAULT NULL,
  `MDTDay` varchar(255) DEFAULT NULL,
  `LeaveReturn` datetime DEFAULT NULL,
  `IsSpecialPatient` tinyint(1) DEFAULT NULL,
  `HasVNR` tinyint(1) DEFAULT NULL,
  `ClinicianID` double DEFAULT NULL,
  `CaseManagerID` double DEFAULT NULL,
  `CaseManager2ndID` double DEFAULT NULL,
  `AssociateID` double DEFAULT NULL,
  `Associate2ndID` double DEFAULT NULL,
  `LastTreatmentPlan` datetime DEFAULT NULL,
  `LastHonos` datetime DEFAULT NULL,
  `NoUDS` tinyint(1) DEFAULT NULL,
  `SpecialNotes` text,
  PRIMARY KEY (`ID`),
  KEY `idx_associate_id` (`AssociateID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `People`
--

LOCK TABLES `People` WRITE;
/*!40000 ALTER TABLE `People` DISABLE KEYS */;
INSERT INTO `People` VALUES (1,'W1',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(2,'W2','BOB1234','Bob Brown',1,'2025-10-06 00:00:00','2025-10-06 00:00:00','2025-10-06 00:00:00',0,0,0,0,0,0,NULL,NULL,NULL,NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,''),(3,'W3',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(4,'W4',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(5,'W5',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(6,'W6',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(7,'W7','FPB1960','Johnny Cash',1,'2025-09-01 00:00:00','2025-09-01 00:00:00','2025-10-13 00:00:00',0,1,1,0,1,0,'Weekly','2025-10-06 00:00:00','Monday',NULL,1,1,52,41,29,NULL,NULL,'2025-06-01 00:00:00','2025-06-01 00:00:00',0,'Blob head'),(8,'E1',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(9,'E2',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(10,'E3','GGG1234','James O\'Reilly',1,'2026-01-06 00:00:00','2025-10-05 00:00:00','2025-11-06 00:00:00',0,0,0,0,0,0,'Monthly','2025-10-06 00:00:00',NULL,'2025-10-06 13:23:41',1,1,NULL,NULL,NULL,NULL,NULL,'2025-10-06 00:00:00',NULL,0,''),(11,'E4',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(12,'E5',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(13,'E6',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(14,'E7',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(15,'E8','TCB1935','Elvis Presley',2,'2026-01-03 00:00:00','2026-01-03 00:00:00','2025-10-10 00:00:00',1,1,1,1,1,0,'Monthly','2025-10-03 00:00:00','Tuesday',NULL,1,0,51,9,5,40,27,'2025-10-03 00:00:00','2025-10-03 00:00:00',0,'No Danny'),(16,'DEL',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(17,'S1',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(18,'S2',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(19,'S3',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `People` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Roles`
--

DROP TABLE IF EXISTS `Roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Roles` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Role` varchar(255) DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Roles`
--

LOCK TABLES `Roles` WRITE;
/*!40000 ALTER TABLE `Roles` DISABLE KEYS */;
INSERT INTO `Roles` VALUES (1,'RN','Registered Nurse'),(2,'HCA-AA','Health Care Assistant or Allied Assistant'),(3,'AR','Allied Registered Staff People'),(4,'AA','Allied Registred Assistant'),(5,'ACNM','Associate Charge Nurse Manager'),(6,'Charge Nurse','Charge Nurse Manager'),(7,'CNS','Clinical Nurse Specialist'),(8,'RC','Resposible Clinician'),(9,'EN','Enrolled Nurse');
/*!40000 ALTER TABLE `Roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RoomSortOrder`
--

DROP TABLE IF EXISTS `RoomSortOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RoomSortOrder` (
  `RoomName` varchar(255) NOT NULL,
  `SortValue` int DEFAULT NULL,
  PRIMARY KEY (`RoomName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RoomSortOrder`
--

LOCK TABLES `RoomSortOrder` WRITE;
/*!40000 ALTER TABLE `RoomSortOrder` DISABLE KEYS */;
INSERT INTO `RoomSortOrder` VALUES ('DEL',16),('E1',8),('E2',9),('E3',10),('E4',11),('E5',12),('E6',13),('E7',14),('E8',15),('S1',17),('S2',18),('S3',19),('W1',1),('W2',2),('W3',3),('W4',4),('W5',5),('W6',6),('W7',7);
/*!40000 ALTER TABLE `RoomSortOrder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Staff`
--

DROP TABLE IF EXISTS `Staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `StaffName` varchar(255) DEFAULT NULL,
  `RoleID` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_RoleID` (`RoleID`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
INSERT INTO `Staff` VALUES (1,'Elyse Falconer ',6),(2,'Bill McCulloch',7),(3,'Johannes Keppler',5),(4,'Hayley Brosnan',1),(5,'Gail Ackroyd',1),(6,'Sophie Rushworth',1),(7,'Angus Fraser ',1),(8,'Luke Greggory',1),(9,'Danny O\'Connor',1),(10,'Hanna Priest',1),(11,'Jaqueline Harvey',9),(12,'Steve Cumming',9),(13,'Krystal Dunham',9),(14,'Daniel Blair',2),(15,'Josh Clark',2),(16,'Andrew Davidson Black',2),(17,'Amara Caras',5),(18,'Jamil Escalera',1),(19,'Andrew McCormack',1),(20,'Therese Makasini',1),(21,'Manisha Kumar',1),(22,'Lee Ward',1),(23,'Theo Barnard',1),(24,'Irene Alex',1),(25,'Emma Ritchie',1),(26,'Stefan Sesante',1),(27,'Max Hill-Cattermole',9),(28,'Leo Aguirre',9),(29,'Ally Ealam',9),(30,'Kiri May Te Paea',2),(31,'Treena Matakai',2),(32,'Alex Hodgson',5),(33,'Mark Barrett',1),(34,'Jak Steels - Ewart',1),(35,'Matt Stiles',1),(36,'Zach Abraas',1),(37,'Rawinia Rhodes',1),(38,'Lisa Zandbergen ',1),(39,'Tanaya Bent',1),(40,'Manmeet Kaur',1),(41,'Ajo Savio',1),(42,'Sunita Tamang',1),(43,'Nicole Turner Robinson',9),(44,'Corrina Arrieta',9),(45,'Tom Coots',2),(46,'Diane Grant',1),(47,'Holly Wilson ',1),(48,'Sarah Bendle',1),(49,'Steven Mackenzie',1),(50,'Bindy Hall',1),(51,'Dr Paul Brown',8),(52,'Bob Geldoff',8);
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UIText`
--

DROP TABLE IF EXISTS `UIText`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UIText` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `FormContext` varchar(255) DEFAULT NULL,
  `ControlName` varchar(255) DEFAULT NULL,
  `CaptionText` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UIText`
--

LOCK TABLES `UIText` WRITE;
/*!40000 ALTER TABLE `UIText` DISABLE KEYS */;
INSERT INTO `UIText` VALUES (3,'Escorted','lblStatusMsg','Special Patients can only be escorted by regular Forensic Mental Health Staff'),(4,'Escorted','lblMSE','Please consider any change or deterioation to baseline mental state including mood, affect, thought process and perceptual disturbance.'),(5,'Escorted','lblLeaveCondition','Please consider approved locations of leave, number of leaves per day e.g. they are not going outside allowance, gender of escorting staff, skill mix e.g. does escort have to be registered health professional, ratios e.g. 2:1 or 1:1 requirement as per documentation.'),(6,'Escorted','lblAWOL','Ensure you are aware of AWOL plan which is documented under leaves in consumers relational security document. Please ensure you are confident in following patient at a distance, alerting ward on direct dial first and then contacting 111 to notify of AWOL and location.'),(7,'Escorted','lblRisk','PLease consider any change of risk to self or others, mention of AWOL or AOD use or increase in DASA in past 24hr period.'),(8,'Escorted','lbContactWard','If taking a ward phone you are aware of how to use same, that the pin is 153957 and how to access contacts to phone ward / shift lead.'),(9,'Escorted','lblContactOwn','If taking your own phone, you must have TWM direct dial (03) 3392867 and TWM ACNM 0212285378 and are able to contact ward'),(10,'Escorted','optWardOne','I am taking ward phone one: 0212298113'),(11,'Escorted','optWardTwo','I am taking ward phone two: 0276890289'),(12,'Escorted','optWardThree','I am taking ward phone three: 021814796'),(13,'Unescorted','lblStatusMsg','Special Patients can only be escorted by regular Forensic Mental Health Staff therefore Unescorted leaves must be complete by same.'),(14,'Unescorted','lblMSE','Please consider any change or deterioation to baseline mental state including mood, affect, thought process and perceptual disturbance'),(15,'Unescorted','lblLeaveCondition','Please consider approved locations of leave, number of leaves per day e.g. they are not going outside allowance'),(16,'Unescorted','lblAWOL','Ensure you are aware of AWOL plan which is documented under leaves in consumers relational security document. If patient does not return in allocated time frame; shift lead to be notified immediately and escalated to Responsible Clinician and CNM / CNS.'),(17,'Unescorted','lblRisk','Please consider any change of risk to self or others, mention of AWOL or AOD use or increase in DASA in past 24hr period.'),(18,'Escorted','chkLeaveCon','I am aware of specific leave conditions for special patient'),(19,'Escorted','optMSE_RN','Escorted by Registered Health Professional who has Completed MSE'),(20,'Escorted','optMSE_Other','Escorted by HCA and Buddy RN or EN has Completed MSE'),(21,'Escorted','chkAwol','I am aware of the AWOL procedure for patient'),(22,'Escorted','optRiskAssessmentRN','Escorted by Registered Health Professional who has Completed Risk Assessment'),(23,'Escorted','optRiskAssessment_Other','Escorted by HCA and Buddy RN or EN has Completed Risk Assessment'),(24,'Escorted','optOwnPhone',' I am taking my own phone and have both numbers saved. My phone number:'),(25,'Escorted','chkSeniorNotify',' I have notified shift lead or delegate prior to leave so they can ensure there are   enough resources left on the ward'),(26,'Escorted','lblMsg','Prior to leave please ensure you have ticked and signed six essential conditions:'),(27,'Escorted','lblNamePLace','Patient Name:'),(28,'Unescorted','lblMsg','Prior to leave please ensure you have ticked and signed six essential conditions:'),(29,'Unescorted','lblNamePLace','Patient Name:'),(30,'Unescorted','chkMSE','Registered Health Professional has completed MSE'),(31,'Unescorted','chkRisk','Registered Health Professional has completed risk assessment'),(32,'Unescorted','chkLeaveCon','I am aware of specific leave conditions for special patient'),(33,'Unescorted','chkAWOL','I am aware of AWOL procedure for patient'),(34,'Unescorted','chkPatientPhone','Check to Enter Patient Phone Number'),(35,'Unescorted','chkPatientAware','Patient knows how to make contact, has ward number and adequate credit to make the call'),(36,'Unescorted','chkSeniorNotify',' I have notified shift lead or delegate prior to leave so they can ensure there are   enough resources left on the ward');
/*!40000 ALTER TABLE `UIText` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_GetSortedPeople`
--

DROP TABLE IF EXISTS `vw_GetSortedPeople`;
/*!50001 DROP VIEW IF EXISTS `vw_GetSortedPeople`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_GetSortedPeople` AS SELECT 
 1 AS `ID`,
 1 AS `Room`,
 1 AS `NHI`,
 1 AS `PersonName`,
 1 AS `LegalStatusID`,
 1 AS `TreatmentPlans`,
 1 AS `HoNos`,
 1 AS `UDSDue`,
 1 AS `RelSecurity`,
 1 AS `Profile`,
 1 AS `Metobolic`,
 1 AS `Bloods`,
 1 AS `FlightRisk`,
 1 AS `Progress%`,
 1 AS `UDSFrequency`,
 1 AS `LastUDS`,
 1 AS `MDTDay`,
 1 AS `LeaveReturn`,
 1 AS `IsSpecialPatient`,
 1 AS `HasVNR`,
 1 AS `ClinicianID`,
 1 AS `CaseManagerID`,
 1 AS `CaseManager2ndID`,
 1 AS `AssociateID`,
 1 AS `Associate2ndID`,
 1 AS `LastTreatmentPlan`,
 1 AS `LastHonos`,
 1 AS `NoUDS`,
 1 AS `SpecialNotes`,
 1 AS `SortValue`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_GetSortedPeopleByName`
--

DROP TABLE IF EXISTS `vw_GetSortedPeopleByName`;
/*!50001 DROP VIEW IF EXISTS `vw_GetSortedPeopleByName`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_GetSortedPeopleByName` AS SELECT 
 1 AS `ID`,
 1 AS `Room`,
 1 AS `NHI`,
 1 AS `PersonName`,
 1 AS `LegalStatusID`,
 1 AS `TreatmentPlans`,
 1 AS `HoNos`,
 1 AS `UDSDue`,
 1 AS `RelSecurity`,
 1 AS `Profile`,
 1 AS `Metobolic`,
 1 AS `Bloods`,
 1 AS `FlightRisk`,
 1 AS `Progress%`,
 1 AS `UDSFrequency`,
 1 AS `LastUDS`,
 1 AS `MDTDay`,
 1 AS `LeaveReturn`,
 1 AS `IsSpecialPatient`,
 1 AS `HasVNR`,
 1 AS `ClinicianID`,
 1 AS `CaseManagerID`,
 1 AS `CaseManager2ndID`,
 1 AS `AssociateID`,
 1 AS `Associate2ndID`,
 1 AS `LastTreatmentPlan`,
 1 AS `LastHonos`,
 1 AS `NoUDS`,
 1 AS `SpecialNotes`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_StaffRoles`
--

DROP TABLE IF EXISTS `vw_StaffRoles`;
/*!50001 DROP VIEW IF EXISTS `vw_StaffRoles`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_StaffRoles` AS SELECT 
 1 AS `StaffName`,
 1 AS `Role`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_WhiteboardData`
--

DROP TABLE IF EXISTS `vw_WhiteboardData`;
/*!50001 DROP VIEW IF EXISTS `vw_WhiteboardData`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_WhiteboardData` AS SELECT 
 1 AS `ID`,
 1 AS `Room`,
 1 AS `NHI`,
 1 AS `PersonName`,
 1 AS `SpecialNotes`,
 1 AS `Progress%`,
 1 AS `IsSpecialPatient`,
 1 AS `LegalStatusID`,
 1 AS `ClinicianID`,
 1 AS `CaseManagerID`,
 1 AS `CaseManager2ndID`,
 1 AS `AssociateID`,
 1 AS `Associate2ndID`,
 1 AS `HasVNR`,
 1 AS `TreatmentPlans`,
 1 AS `HoNos`,
 1 AS `UDSDue`,
 1 AS `RelSecurity`,
 1 AS `Profile`,
 1 AS `Metobolic`,
 1 AS `Bloods`,
 1 AS `FlightRisk`,
 1 AS `UDSFrequency`,
 1 AS `MDTDay`,
 1 AS `LeaveReturn`,
 1 AS `LastTreatmentPlan`,
 1 AS `LastHonos`,
 1 AS `LastUDS`,
 1 AS `NoUDS`,
 1 AS `Legal`,
 1 AS `ClinicianName`,
 1 AS `CaseManagers`,
 1 AS `Associates`,
 1 AS `SortValue`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'PeopleAndLeaveDB'
--
/*!50003 DROP PROCEDURE IF EXISTS `SetLeaveReturnToNull` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `SetLeaveReturnToNull`()
BEGIN
    
SET SQL_SAFE_UPDATES = 0;

UPDATE People
SET LeaveReturn = NULL;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_AddLeave` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_AddLeave`(
    IN p_nhi VARCHAR(255),
    IN p_patient_name VARCHAR(255),
    IN p_leave_date DATE,
    IN p_leave_time DATETIME,
    IN p_expected_return_time DATETIME,
    IN p_leave_type VARCHAR(255),
    IN p_duration_minutes INT,
    IN p_is_escorted_leave BOOLEAN,
    IN p_is_special_patient BOOLEAN, -- NEW PARAMETER
    IN p_staff_responsible_id INT,
    IN p_staff_nurse_id INT,
    IN p_leave_description TEXT,
    IN p_mse_completed BOOLEAN,
    IN p_risk_assessment_completed BOOLEAN,
    IN p_leave_conditions_met BOOLEAN,
    IN p_awol_aware BOOLEAN,
    IN p_contact_aware BOOLEAN,
    IN p_senior_nurse_id INT,
    IN p_contact_phone_number VARCHAR(255),
    OUT p_new_id INT
)
BEGIN
    INSERT INTO LeaveLog (
        NHI, Name, LeaveDate, LeaveTime, ExpectedReturnTime, LeaveType, 
        DurationMinutes, `Is Escorted`, IsSpecialPatient, StaffResponsibleID, StaffNurseID, 
        LeaveDescription, MSE, Risk, LeaveCondition, AWOL, HasContactInfo, 
        SeniorNurseNotified, SeniorNurseID, ContactPhoneNumber
    )
    VALUES (
        p_nhi, p_patient_name, p_leave_date, p_leave_time, p_expected_return_time, p_leave_type, 
        p_duration_minutes, p_is_escorted_leave, p_is_special_patient, p_staff_responsible_id, p_staff_nurse_id, 
        p_leave_description, p_mse_completed, p_risk_assessment_completed,
        p_leave_conditions_met, p_awol_aware, p_contact_aware, 
        (p_senior_nurse_id IS NOT NULL), p_senior_nurse_id, p_contact_phone_number
    );

    SET p_new_id = LAST_INSERT_ID();
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_AssignPersonToRoom` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_AssignPersonToRoom`(
    -- Input parameters for the new person's details
    IN p_nhi VARCHAR(255),
    IN p_name VARCHAR(255),
    IN p_legal_id INT,
    IN p_has_vnr BOOLEAN,
    IN p_is_special BOOLEAN,
    IN p_notes TEXT,
    -- Input for the destination
    IN p_destination_room_name VARCHAR(255),
    -- Output parameter to return the record ID
    OUT p_record_id INT
)
BEGIN
    DECLARE occupied_nhi VARCHAR(255);
    DECLARE duplicate_nhi_exists INT;

    -- Start the transaction
    START TRANSACTION;

    -- 1. Validation: Check if the destination room is occupied.
    SELECT NHI, ID INTO occupied_nhi, p_record_id 
    FROM People 
    WHERE Room = p_destination_room_name 
    LIMIT 1;

    IF occupied_nhi IS NOT NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Destination room is already occupied.';
    -- 2. Validation: Check if the NHI is a duplicate.
    ELSE
        SELECT COUNT(*) INTO duplicate_nhi_exists FROM People WHERE NHI = p_nhi;
        IF duplicate_nhi_exists > 0 THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This NHI is already in use by another person.';
        ELSE
            -- 3. If validation passes, update the empty room's record.
            UPDATE People SET
                NHI = p_nhi,
                PersonName = p_name,
                LegalStatusID = p_legal_id,
                HasVNR = p_has_vnr,
                IsSpecialPatient = p_is_special,
                TreatmentPlans = CURDATE(),
                HoNos = CURDATE(),
                UDSDue = CURDATE(),
                `Progress%` = 0.0,
                SpecialNotes = p_notes
            WHERE ID = p_record_id;
            
            -- If all steps succeeded, commit the transaction.
            COMMIT;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetActiveNotices` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetActiveNotices`(IN p_today DATE)
BEGIN
    SELECT NoticeText FROM Notices WHERE ExpiryDate >= p_today;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetDelegatedStaff` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetDelegatedStaff`()
BEGIN
    SELECT 
        s.ID, 
        s.StaffName,
        r.Role
    FROM Staff AS s
    INNER JOIN DelegatedStaff AS ds ON s.ID = ds.StaffID
    LEFT JOIN Roles AS r ON s.RoleID = r.ID
    ORDER BY s.StaffName;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetLeaveByDateRange` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetLeaveByDateRange`(
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_nhi VARCHAR(255)
)
BEGIN
    SELECT *
    FROM LeaveLog
    WHERE
        LeaveDate BETWEEN p_start_date AND p_end_date
        AND (p_nhi IS NULL OR NHI = p_nhi)
    ORDER BY Name, LeaveDate, LeaveTime;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetLeaveForCurrentPeople` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetLeaveForCurrentPeople`()
BEGIN
    SELECT L.*
    FROM LeaveLog AS L
    INNER JOIN People AS P ON L.NHI = P.NHI
    WHERE P.NHI IS NOT NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetLeaveForPerson` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetLeaveForPerson`(
    IN p_nhi VARCHAR(255)
)
BEGIN
    SELECT *
    FROM LeaveLog
    WHERE NHI = p_nhi
    ORDER BY LeaveDate DESC, LeaveTime DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetPeopleOnLeave` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetPeopleOnLeave`()
BEGIN
    SELECT
        p.PersonName,
        l.LeaveType,
        l.LeaveDescription,
        s.StaffName,
        l.ContactPhoneNumber
    FROM LeaveLog AS l
    INNER JOIN People AS p ON l.NHI = p.NHI
    LEFT JOIN Staff AS s ON l.StaffNurseID = s.ID
    WHERE l.ReturnTime IS NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetSortedPeople` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_GetSortedPeople`()
BEGIN
    SELECT * FROM vw_WhiteboardData ORDER BY SortValue;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_IsPersonOnLeave` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_IsPersonOnLeave`(
    IN p_nhi VARCHAR(255),
    OUT p_is_on_leave BOOLEAN
)
BEGIN
    DECLARE leave_count INT;
    SELECT COUNT(ID) INTO leave_count
    FROM LeaveLog
    WHERE NHI = p_nhi AND ReturnTime IS NULL;

    IF leave_count > 0 THEN
        SET p_is_on_leave = TRUE;
    ELSE
        SET p_is_on_leave = FALSE;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_LogReturn` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_LogReturn`(
    IN p_record_id INT,
    IN p_return_time DATETIME,
    IN p_signed_in_by_id INT
)
BEGIN
    UPDATE LeaveLog
    SET ReturnTime = p_return_time, SignedInByID = p_signed_in_by_id
    WHERE ID = p_record_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_MovePerson` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_MovePerson`(
    IN p_current_id INT,
    IN p_destination_room VARCHAR(255)
)
BEGIN
    -- This procedure moves a person's data from their current room (identified by p_current_id)
    -- to an empty destination room (identified by p_destination_room).

    -- Step 1: Read all data from the source person's record into variables.
    SELECT
        NHI, PersonName, LegalStatusID, HasVNR, TreatmentPlans, HoNos, UDSDue,
        RelSecurity, `Profile`, Metobolic, Bloods, FlightRisk, UDSFrequency, MDTDay,
        ClinicianID, CaseManagerID, CaseManager2ndID, AssociateID, Associate2ndID,
        `Progress%`, SpecialNotes, IsSpecialPatient, LastTreatmentPlan, LastHonos, LastUDS, LeaveReturn
    INTO
        @v_nhi, @v_name, @v_legal_id, @v_has_vnr, @v_tp_due, @v_honos_due, @v_uds_due,
        @v_rel_sec, @v_profile, @v_metobolic, @v_bloods, @v_flight_risk, @v_uds_freq, @v_mdt_day,
        @v_clin_id, @v_cm_id, @v_cm_2nd_id, @v_assoc_id, @v_assoc_2nd_id,
        @v_progress, @v_notes, @v_is_special, @v_last_tp, @v_last_honos, @v_last_uds, @v_leave_return
    FROM People WHERE ID = p_current_id;

    -- Step 2: Update the destination room's record with the data from the variables.
    UPDATE People
    SET
        NHI = @v_nhi, PersonName = @v_name, LegalStatusID = @v_legal_id, HasVNR = @v_has_vnr,
        TreatmentPlans = @v_tp_due, HoNos = @v_honos_due, UDSDue = @v_uds_due,
        RelSecurity = @v_rel_sec, `Profile` = @v_profile, Metobolic = @v_metobolic, Bloods = @v_bloods,
        FlightRisk = @v_flight_risk, UDSFrequency = @v_uds_freq, MDTDay = @v_mdt_day,
        ClinicianID = @v_clin_id, CaseManagerID = @v_cm_id, CaseManager2ndID = @v_cm_2nd_id,
        AssociateID = @v_assoc_id, Associate2ndID = @v_assoc_2nd_id, `Progress%` = @v_progress,
        SpecialNotes = @v_notes, IsSpecialPatient = @v_is_special, LastTreatmentPlan = @v_last_tp,
        LastHonos = @v_last_honos, LastUDS = @v_last_uds, LeaveReturn = @v_leave_return
    WHERE Room = p_destination_room;

    -- Step 3: Clear all data from the source person's record, resetting it to an empty room.
    UPDATE People
    SET
        NHI = NULL, PersonName = NULL, LegalStatusID = NULL, HasVNR = 0,
        TreatmentPlans = NULL, HoNos = NULL, UDSDue = NULL, RelSecurity = 0,
        `Profile` = 0, Metobolic = 0, Bloods = 0, FlightRisk = 0,
        UDSFrequency = NULL, MDTDay = NULL, ClinicianID = NULL, CaseManagerID = NULL,
        CaseManager2ndID = NULL, AssociateID = NULL, Associate2ndID = NULL, `Progress%` = 0,
        SpecialNotes = NULL, IsSpecialPatient = 0, LastTreatmentPlan = NULL,
        LastHonos = NULL, LastUDS = NULL, LeaveReturn = NULL
    WHERE ID = p_current_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_RemovePerson` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_RemovePerson`(IN p_person_id INT)
BEGIN
    -- This procedure clears all data from a person's record,
    -- effectively making the room empty.
    UPDATE People
    SET
        NHI = NULL,
        PersonName = NULL,
        LegalStatusID = NULL,
        HasVNR = 0,
        TreatmentPlans = NULL,
        HoNos = NULL,
        UDSDue = NULL,
        RelSecurity = 0,
        `Profile` = 0,
        Metobolic = 0,
        Bloods = 0,
        FlightRisk = 0,
        UDSFrequency = NULL,
        MDTDay = NULL,
        ClinicianID = NULL,
        CaseManagerID = NULL,
        CaseManager2ndID = NULL,
        AssociateID = NULL,
        Associate2ndID = NULL,
        `Progress%` = 0,
        SpecialNotes = NULL,
        IsSpecialPatient = 0,
        -- This is the fix: ensuring these fields are also cleared
        LastTreatmentPlan = NULL,
        LastHonos = NULL,
        LastUDS = NULL,
        LeaveReturn = NULL
    WHERE ID = p_person_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdateLeaveFileName` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_UpdateLeaveFileName`(
    IN p_record_id INT,
    IN p_file_name VARCHAR(255)
)
BEGIN
    UPDATE LeaveLog
    SET FileName = p_file_name
    WHERE ID = p_record_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdatePerson` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_UpdatePerson`(
    IN p_id INT,
    IN p_nhi VARCHAR(255),
    IN p_name VARCHAR(255),
    IN p_legal_id INT,
    IN p_is_special BOOLEAN,
    IN p_has_vnr BOOLEAN,
    IN p_notes TEXT
)
BEGIN
    DECLARE existing_id INT;

    -- First, check if the new NHI is already in use by another person.
    SELECT ID INTO existing_id FROM People 
    WHERE NHI = p_nhi AND ID <> p_id 
    LIMIT 1;

    -- If we found a duplicate, raise an error and stop.
    IF existing_id IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'This NHI is already in use by another person.';
    ELSE
        -- If no duplicates, proceed with the update.
        UPDATE People SET
            NHI = p_nhi,
            PersonName = p_name,
            LegalStatusID = p_legal_id,
            IsSpecialPatient = p_is_special,
            HasVNR = p_has_vnr,
            SpecialNotes = p_notes
        WHERE ID = p_id;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdateStaffAssignments` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_UpdateStaffAssignments`(
    IN p_person_id INT,
    IN p_clinician_id INT,
    IN p_cm_id INT,
    IN p_cm_2nd_id INT,
    IN p_assoc_id INT,
    IN p_assoc_2nd_id INT
)
BEGIN
    UPDATE People SET
        ClinicianID = p_clinician_id,
        CaseManagerID = p_cm_id,
        CaseManager2ndID = p_cm_2nd_id,
        AssociateID = p_assoc_id,
        Associate2ndID = p_assoc_2nd_id
    WHERE ID = p_person_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `vw_GetSortedPeople`
--

/*!50001 DROP VIEW IF EXISTS `vw_GetSortedPeople`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_GetSortedPeople` AS select `p`.`ID` AS `ID`,`p`.`Room` AS `Room`,`p`.`NHI` AS `NHI`,`p`.`PersonName` AS `PersonName`,`p`.`LegalStatusID` AS `LegalStatusID`,`p`.`TreatmentPlans` AS `TreatmentPlans`,`p`.`HoNos` AS `HoNos`,`p`.`UDSDue` AS `UDSDue`,`p`.`RelSecurity` AS `RelSecurity`,`p`.`Profile` AS `Profile`,`p`.`Metobolic` AS `Metobolic`,`p`.`Bloods` AS `Bloods`,`p`.`FlightRisk` AS `FlightRisk`,`p`.`Progress%` AS `Progress%`,`p`.`UDSFrequency` AS `UDSFrequency`,`p`.`LastUDS` AS `LastUDS`,`p`.`MDTDay` AS `MDTDay`,`p`.`LeaveReturn` AS `LeaveReturn`,`p`.`IsSpecialPatient` AS `IsSpecialPatient`,`p`.`HasVNR` AS `HasVNR`,`p`.`ClinicianID` AS `ClinicianID`,`p`.`CaseManagerID` AS `CaseManagerID`,`p`.`CaseManager2ndID` AS `CaseManager2ndID`,`p`.`AssociateID` AS `AssociateID`,`p`.`Associate2ndID` AS `Associate2ndID`,`p`.`LastTreatmentPlan` AS `LastTreatmentPlan`,`p`.`LastHonos` AS `LastHonos`,`p`.`NoUDS` AS `NoUDS`,`p`.`SpecialNotes` AS `SpecialNotes`,`s`.`SortValue` AS `SortValue` from (`People` `p` left join `RoomSortOrder` `s` on((`p`.`Room` = `s`.`RoomName`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_GetSortedPeopleByName`
--

/*!50001 DROP VIEW IF EXISTS `vw_GetSortedPeopleByName`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_GetSortedPeopleByName` AS select `People`.`ID` AS `ID`,`People`.`Room` AS `Room`,`People`.`NHI` AS `NHI`,`People`.`PersonName` AS `PersonName`,`People`.`LegalStatusID` AS `LegalStatusID`,`People`.`TreatmentPlans` AS `TreatmentPlans`,`People`.`HoNos` AS `HoNos`,`People`.`UDSDue` AS `UDSDue`,`People`.`RelSecurity` AS `RelSecurity`,`People`.`Profile` AS `Profile`,`People`.`Metobolic` AS `Metobolic`,`People`.`Bloods` AS `Bloods`,`People`.`FlightRisk` AS `FlightRisk`,`People`.`Progress%` AS `Progress%`,`People`.`UDSFrequency` AS `UDSFrequency`,`People`.`LastUDS` AS `LastUDS`,`People`.`MDTDay` AS `MDTDay`,`People`.`LeaveReturn` AS `LeaveReturn`,`People`.`IsSpecialPatient` AS `IsSpecialPatient`,`People`.`HasVNR` AS `HasVNR`,`People`.`ClinicianID` AS `ClinicianID`,`People`.`CaseManagerID` AS `CaseManagerID`,`People`.`CaseManager2ndID` AS `CaseManager2ndID`,`People`.`AssociateID` AS `AssociateID`,`People`.`Associate2ndID` AS `Associate2ndID`,`People`.`LastTreatmentPlan` AS `LastTreatmentPlan`,`People`.`LastHonos` AS `LastHonos`,`People`.`NoUDS` AS `NoUDS`,`People`.`SpecialNotes` AS `SpecialNotes` from `People` where ((`People`.`NHI` is not null) and (`People`.`NHI` <> '')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_StaffRoles`
--

/*!50001 DROP VIEW IF EXISTS `vw_StaffRoles`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_StaffRoles` AS select `Staff`.`StaffName` AS `StaffName`,`Roles`.`Role` AS `Role` from (`Staff` join `Roles` on((`Staff`.`RoleID` = `Roles`.`ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_WhiteboardData`
--

/*!50001 DROP VIEW IF EXISTS `vw_WhiteboardData`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_WhiteboardData` AS select `p`.`ID` AS `ID`,`p`.`Room` AS `Room`,`p`.`NHI` AS `NHI`,`p`.`PersonName` AS `PersonName`,`p`.`SpecialNotes` AS `SpecialNotes`,`p`.`Progress%` AS `Progress%`,`p`.`IsSpecialPatient` AS `IsSpecialPatient`,`p`.`LegalStatusID` AS `LegalStatusID`,`p`.`ClinicianID` AS `ClinicianID`,`p`.`CaseManagerID` AS `CaseManagerID`,`p`.`CaseManager2ndID` AS `CaseManager2ndID`,`p`.`AssociateID` AS `AssociateID`,`p`.`Associate2ndID` AS `Associate2ndID`,`p`.`HasVNR` AS `HasVNR`,`p`.`TreatmentPlans` AS `TreatmentPlans`,`p`.`HoNos` AS `HoNos`,`p`.`UDSDue` AS `UDSDue`,`p`.`RelSecurity` AS `RelSecurity`,`p`.`Profile` AS `Profile`,`p`.`Metobolic` AS `Metobolic`,`p`.`Bloods` AS `Bloods`,`p`.`FlightRisk` AS `FlightRisk`,`p`.`UDSFrequency` AS `UDSFrequency`,`p`.`MDTDay` AS `MDTDay`,`p`.`LeaveReturn` AS `LeaveReturn`,`p`.`LastTreatmentPlan` AS `LastTreatmentPlan`,`p`.`LastHonos` AS `LastHonos`,`p`.`LastUDS` AS `LastUDS`,`p`.`NoUDS` AS `NoUDS`,`mha`.`LegalStatus` AS `Legal`,`rc`.`StaffName` AS `ClinicianName`,concat(if((`cm`.`StaffName` is null),'',left(`cm`.`StaffName`,(locate(' ',`cm`.`StaffName`) - 1))),if(((`cm`.`StaffName` is not null) and (`cm2`.`StaffName` is not null)),'/',''),if((`cm2`.`StaffName` is null),'',left(`cm2`.`StaffName`,(locate(' ',`cm2`.`StaffName`) - 1)))) AS `CaseManagers`,concat(if((`assoc`.`StaffName` is null),'',left(`assoc`.`StaffName`,(locate(' ',`assoc`.`StaffName`) - 1))),if(((`assoc`.`StaffName` is not null) and (`assoc2`.`StaffName` is not null)),'/ ',''),if((`assoc2`.`StaffName` is null),'',left(`assoc2`.`StaffName`,(locate(' ',`assoc2`.`StaffName`) - 1)))) AS `Associates`,`s`.`SortValue` AS `SortValue` from (((((((`People` `p` left join `MHA_Sections` `mha` on((`p`.`LegalStatusID` = `mha`.`ID`))) left join `Staff` `rc` on((`p`.`ClinicianID` = `rc`.`ID`))) left join `Staff` `cm` on((`p`.`CaseManagerID` = `cm`.`ID`))) left join `Staff` `cm2` on((`p`.`CaseManager2ndID` = `cm2`.`ID`))) left join `Staff` `assoc` on((`p`.`AssociateID` = `assoc`.`ID`))) left join `Staff` `assoc2` on((`p`.`Associate2ndID` = `assoc2`.`ID`))) left join `RoomSortOrder` `s` on((`p`.`Room` = `s`.`RoomName`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-06 13:14:12
