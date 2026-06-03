-- MySQL dump for RFID Toll Gate System
-- Database: tollgate
-- -------------------------------------------------------

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

-- ---------------------------------------------------
-- Table structure for table `gate_entries`
-- ---------------------------------------------------

DROP TABLE IF EXISTS `gate_entries`;
CREATE TABLE `gate_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfid_tag` varchar(20) DEFAULT NULL,
  `entry_time` varchar(50) DEFAULT NULL,
  `access_granted` enum('Yes','No') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Sample data (replace RFID tags with your actual card UIDs)
-- INSERT INTO `gate_entries` VALUES (1,'XXXXXXXXXXXX','01-01-2025 10:00:00 AM','Yes');

-- ---------------------------------------------------
-- Table structure for table `toll_transactions`
-- ---------------------------------------------------

DROP TABLE IF EXISTS `toll_transactions`;
CREATE TABLE `toll_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfid_tag` varchar(20) DEFAULT NULL,
  `transaction_time` varchar(50) DEFAULT NULL,
  `amount_deducted` decimal(10,2) DEFAULT NULL,
  `balance_left` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Sample data (replace RFID tags with your actual card UIDs)
-- INSERT INTO `toll_transactions` VALUES (1,'XXXXXXXXXXXX','01-01-2025 10:00:00 AM',50.00,950.00);

-- ---------------------------------------------------
-- Table structure for table `users`
-- ---------------------------------------------------

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfid_tag` varchar(20) NOT NULL,
  `vehicle_number` varchar(20) DEFAULT NULL,
  `balance` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rfid_tag` (`rfid_tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Add your registered RFID cards here
-- Replace XXXXXXXXXXXX with your actual RFID card UID (scan using Arduino to find it)
-- Replace XX00XX0000 with the vehicle number
INSERT INTO `users` VALUES (1,'XXXXXXXXXXXX','XX00XX0000',1000.00);

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
