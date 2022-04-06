
-- FOR MYSQL

-- Dumping database structure for gestion
CREATE DATABASE IF NOT EXISTS `gestion` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `gestion`;

-- Dumping structure for table gestion.client
CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dateOfBirth` date DEFAULT NULL,
  `age` int(11) DEFAULT '0',
  `uuid` binary(16) DEFAULT NULL,
  `height` decimal(19,5) DEFAULT '0.00000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

