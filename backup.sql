-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: PeopleAndLeaveDB
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DelegatedStaff`
--

LOCK TABLES `DelegatedStaff` WRITE;
/*!40000 ALTER TABLE `DelegatedStaff` DISABLE KEYS */;
INSERT INTO `DelegatedStaff` VALUES (10,3),(11,1),(12,9);
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
  `Is Special` tinyint(1) DEFAULT NULL,
  `Is Escorted` tinyint(1) DEFAULT NULL,
  `FileName` varchar(255) DEFAULT NULL,
  `LeaveDescription` text,
  PRIMARY KEY (`ID`),
  KEY `idx_nhi` (`NHI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LeaveLog`
--

LOCK TABLES `LeaveLog` WRITE;
/*!40000 ALTER TABLE `LeaveLog` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notices`
--

LOCK TABLES `Notices` WRITE;
/*!40000 ALTER TABLE `Notices` DISABLE KEYS */;
INSERT INTO `Notices` VALUES (1,'New Admission expected this Thursday 18/9','2025-09-30 00:00:00'),(2,'BBQ Next Thursday 25/9','2025-09-26 00:00:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `People`
--

LOCK TABLES `People` WRITE;
/*!40000 ALTER TABLE `People` DISABLE KEYS */;
INSERT INTO `People` VALUES (1,'W1',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(2,'W2','CBA4321','Johnny Cash',2,'2025-09-25 00:00:00','2025-09-25 00:00:00','2025-09-25 00:00:00',1,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,1,2,3,4,5,NULL,NULL,0,NULL),(3,'W3','TCB1935','Elvis Presley',1,'2025-11-07 00:00:00','2025-11-07 00:00:00','2025-08-14 00:00:00',0,1,1,1,1,0.75,'Weekly',NULL,'Monday',NULL,1,1,51,9,19,47,5,NULL,NULL,0,'Test update at 00:44:03'),(4,'W4',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(5,'W5',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-08-07 00:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-08-07 00:00:00','2025-08-07 00:00:00',0,NULL),(6,'W6',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(7,'W7',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(8,'E1',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(9,'E2',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(10,'E3',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(11,'E4','TAM1964','Bob Dylan',1,'2024-04-29 00:00:00','2025-11-07 00:00:00','2025-09-07 00:00:00',0,1,1,1,1,0.62,'Monthly','2025-08-07 00:00:00','Monday',NULL,1,1,51,23,9,22,29,'2024-01-29 00:00:00','2025-08-07 00:00:00',0,NULL),(12,'E5',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(13,'E6',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(14,'E7',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(15,'E8',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(16,'DEL',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(17,'S1',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(18,'S2','RIP2025','Ozzy Osbourne',5,'2025-08-07 00:00:00','2025-08-07 00:00:00','2025-09-07 00:00:00',0,1,1,1,1,0.62,'Monthly','2025-08-07 00:00:00','Monday',NULL,0,0,51,22,0,24,23,'2025-08-07 00:00:00','2025-08-07 00:00:00',0,NULL),(19,'S3',NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL);
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
INSERT INTO `Roles` VALUES (1,'RN','Registered Nurse'),(2,'HCA','Health Care Assistant'),(3,'AR','Allied Resgistred Staff'),(4,'AA','Allied Registred Assistant'),(5,'ACNM','Associate Charge Nurse Manager'),(6,'Charge Nurse','Charge Nurse Manager'),(7,'CNS','Clinical Nurse Specialist'),(8,'RC','Resposible Clinician'),(9,'EN','Enrolled Nurse');
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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
INSERT INTO `Staff` VALUES (1,'Elyse Falconer ',6),(2,'Bill McCulloch',7),(3,'Johannes Keppler',5),(4,'Hayley Brosnan',1),(5,'Gail Ackroyd',1),(6,'Sophie Rushworth',1),(7,'Angus Fraser ',1),(8,'Luke Greggory',1),(9,'Danny O\'Connor',1),(10,'Hanna Priest',1),(11,'Jaqueline Harvey',9),(12,'Steve Cumming',9),(13,'Krystal Dunham',9),(14,'Daniel Blair',2),(15,'Josh Clark',2),(16,'Andrew Davidson Black',2),(17,'Amara Caras',5),(18,'Jamil Escalera',1),(19,'Andrew McCormack',1),(20,'Therese Makasini',1),(21,'Manisha Kumar',1),(22,'Lee Ward',1),(23,'Theo Barnard',1),(24,'Irene Alex',1),(25,'Emma Ritchie',1),(26,'Stefan Sesante',1),(27,'Max Hill-Cattermole',9),(28,'Leo Aguirre',9),(29,'Ally Ealam',9),(30,'Kiri May Te Paea',2),(31,'Treena Matakai',2),(32,'Alex Hodgson',5),(33,'Mark Barrett',1),(34,'Jak Steels - Ewart',1),(35,'Matt Stiles',1),(36,'Zach Abraas',1),(37,'Rawinia Rhodes',1),(38,'Lisa Zandbergen ',1),(39,'Tanaya Bent',1),(40,'Manmeet Kaur',1),(41,'Ajo Savio',1),(42,'Sunita Tamang',1),(43,'Nicole Turner Robinson',9),(44,'Corrina Arrieta',9),(45,'Tom Coots',2),(46,'Diane Grant',1),(47,'Holly Wilson ',1),(48,'Sarah Bendle',1),(49,'Steven Mackenzie',1),(50,'Bindy Hall',1),(51,'Dr Paul Brown',8);
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
-- Temporary view structure for view `vw_LoadLeaveForCurrentPeople`
--

DROP TABLE IF EXISTS `vw_LoadLeaveForCurrentPeople`;
/*!50001 DROP VIEW IF EXISTS `vw_LoadLeaveForCurrentPeople`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_LoadLeaveForCurrentPeople` AS SELECT 
 1 AS `ID`,
 1 AS `NHI`,
 1 AS `Name`,
 1 AS `LeaveDate`,
 1 AS `LeaveType`,
 1 AS `LeaveTime`,
 1 AS `ReturnTime`,
 1 AS `ExpectedReturnTime`,
 1 AS `MSE`,
 1 AS `Risk`,
 1 AS `LeaveCondition`,
 1 AS `AWOL`,
 1 AS `OwnPhone`,
 1 AS `ContactPhoneNumber`,
 1 AS `HasContactInfo`,
 1 AS `SeniorNurseNotified`,
 1 AS `SeniorNurseID`,
 1 AS `StaffNurseID`,
 1 AS `StaffResponsibleID`,
 1 AS `SignedInByID`,
 1 AS `Is Special`,
 1 AS `Is Escorted`,
 1 AS `FileName`,
 1 AS `LeaveDescription`*/;
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
 1 AS `Room`,
 1 AS `NHI`,
 1 AS `PersonName`,
 1 AS `Legal`,
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
 1 AS `ClinicianName`,
 1 AS `CaseManagers`,
 1 AS `Associates`,
 1 AS `Progress%`,
 1 AS `SpecialNotes`,
 1 AS `IsSpecialPatient`,
 1 AS `SortValue`*/;
SET character_set_client = @saved_cs_client;

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
-- Final view structure for view `vw_LoadLeaveForCurrentPeople`
--

/*!50001 DROP VIEW IF EXISTS `vw_LoadLeaveForCurrentPeople`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_LoadLeaveForCurrentPeople` AS select `L`.`ID` AS `ID`,`L`.`NHI` AS `NHI`,`L`.`Name` AS `Name`,`L`.`LeaveDate` AS `LeaveDate`,`L`.`LeaveType` AS `LeaveType`,`L`.`LeaveTime` AS `LeaveTime`,`L`.`ReturnTime` AS `ReturnTime`,`L`.`ExpectedReturnTime` AS `ExpectedReturnTime`,`L`.`MSE` AS `MSE`,`L`.`Risk` AS `Risk`,`L`.`LeaveCondition` AS `LeaveCondition`,`L`.`AWOL` AS `AWOL`,`L`.`OwnPhone` AS `OwnPhone`,`L`.`ContactPhoneNumber` AS `ContactPhoneNumber`,`L`.`HasContactInfo` AS `HasContactInfo`,`L`.`SeniorNurseNotified` AS `SeniorNurseNotified`,`L`.`SeniorNurseID` AS `SeniorNurseID`,`L`.`StaffNurseID` AS `StaffNurseID`,`L`.`StaffResponsibleID` AS `StaffResponsibleID`,`L`.`SignedInByID` AS `SignedInByID`,`L`.`Is Special` AS `Is Special`,`L`.`Is Escorted` AS `Is Escorted`,`L`.`FileName` AS `FileName`,`L`.`LeaveDescription` AS `LeaveDescription` from (`LeaveLog` `L` join `People` `P` on((`L`.`NHI` = `P`.`NHI`))) where (`P`.`NHI` is not null) */;
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
/*!50001 VIEW `vw_WhiteboardData` AS select `p`.`Room` AS `Room`,`p`.`NHI` AS `NHI`,`p`.`PersonName` AS `PersonName`,`mha`.`LegalStatus` AS `Legal`,`p`.`HasVNR` AS `HasVNR`,`p`.`TreatmentPlans` AS `TreatmentPlans`,`p`.`HoNos` AS `HoNos`,`p`.`UDSDue` AS `UDSDue`,`p`.`RelSecurity` AS `RelSecurity`,`p`.`Profile` AS `Profile`,`p`.`Metobolic` AS `Metobolic`,`p`.`Bloods` AS `Bloods`,`p`.`FlightRisk` AS `FlightRisk`,`p`.`UDSFrequency` AS `UDSFrequency`,`p`.`MDTDay` AS `MDTDay`,`p`.`LeaveReturn` AS `LeaveReturn`,`rc`.`StaffName` AS `ClinicianName`,concat(if((`cm`.`StaffName` is null),'',if((locate(' ',`cm`.`StaffName`) > 0),left(`cm`.`StaffName`,(locate(' ',`cm`.`StaffName`) - 1)),`cm`.`StaffName`)),if(((`cm`.`StaffName` is not null) and (`cm2`.`StaffName` is not null)),'/',''),if((`cm2`.`StaffName` is null),'',if((locate(' ',`cm2`.`StaffName`) > 0),left(`cm2`.`StaffName`,(locate(' ',`cm2`.`StaffName`) - 1)),`cm2`.`StaffName`))) AS `CaseManagers`,concat(if((`assoc`.`StaffName` is null),'',if((locate(' ',`assoc`.`StaffName`) > 0),left(`assoc`.`StaffName`,(locate(' ',`assoc`.`StaffName`) - 1)),`assoc`.`StaffName`)),if(((`assoc`.`StaffName` is not null) and (`assoc2`.`StaffName` is not null)),'/ ',''),if((`assoc2`.`StaffName` is null),'',if((locate(' ',`assoc2`.`StaffName`) > 0),left(`assoc2`.`StaffName`,(locate(' ',`assoc2`.`StaffName`) - 1)),`assoc2`.`StaffName`))) AS `Associates`,`p`.`Progress%` AS `Progress%`,`p`.`SpecialNotes` AS `SpecialNotes`,`p`.`IsSpecialPatient` AS `IsSpecialPatient`,`s`.`SortValue` AS `SortValue` from (((((((`People` `p` left join `MHA_Sections` `mha` on((`p`.`LegalStatusID` = `mha`.`ID`))) left join `Staff` `rc` on((`p`.`ClinicianID` = `rc`.`ID`))) left join `Staff` `cm` on((`p`.`CaseManagerID` = `cm`.`ID`))) left join `Staff` `cm2` on((`p`.`CaseManager2ndID` = `cm2`.`ID`))) left join `Staff` `assoc` on((`p`.`AssociateID` = `assoc`.`ID`))) left join `Staff` `assoc2` on((`p`.`Associate2ndID` = `assoc2`.`ID`))) left join `RoomSortOrder` `s` on((`p`.`Room` = `s`.`RoomName`))) */;
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

-- Dump completed on 2025-09-24 14:32:36
