--
-- Table structure for table `films_allo`
--

DROP TABLE IF EXISTS `films_allo`;
CREATE TABLE `films_allo` (
  `id` varchar(255) NOT NULL,
  `id_jp` varchar(255) NOT NULL,
  `url_allo` varchar(255) NOT NULL,
  `director_allo` json DEFAULT NULL,
  `year_allo` int DEFAULT NULL,
  `synopsis` text,
  `distributor` varchar(100) DEFAULT NULL,
  `casting` json DEFAULT NULL,
  `rating_press` float DEFAULT NULL,
  `rating_public` float DEFAULT NULL,
  `award` int DEFAULT NULL,
  `budget` bigint DEFAULT NULL,
  `lang` json DEFAULT NULL,
  `visa` int DEFAULT NULL,
  `time_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_films_allo_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `films_imdb`
--

DROP TABLE IF EXISTS `films_imdb`;
CREATE TABLE `films_imdb` (
  `id` varchar(255) NOT NULL,
  `id_jp` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `original_title` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `synopsis` text,
  `distributor` json DEFAULT NULL,
  `casting` json DEFAULT NULL,
  `rating_press` float DEFAULT NULL,
  `rating_public` float DEFAULT NULL,
  `award` int DEFAULT NULL,
  `budget` bigint DEFAULT NULL,
  `lang` json DEFAULT NULL,
  `time_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `films_jp`
--

DROP TABLE IF EXISTS `films_jp`;
CREATE TABLE `films_jp` (
  `id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  `original_title` varchar(255) DEFAULT NULL,
  `director` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `raw_title` varchar(255) NOT NULL,
  `raw_director` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `url_jp` varchar(255) NOT NULL,
  `year` int DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `first_day` int DEFAULT NULL,
  `first_weekend` int DEFAULT NULL,
  `first_week` int DEFAULT NULL,
  `hebdo_rank` int DEFAULT NULL,
  `total_spectator` int DEFAULT NULL,
  `copies` int DEFAULT NULL,
  `scraped` tinyint DEFAULT '0',
  `time_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_films_jp_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `functionalities_filmscrap`
--

DROP TABLE IF EXISTS `functionalities_filmscrap`;
CREATE TABLE `functionalities_filmscrap` (
  `id` varchar(255) NOT NULL,
  `url_allo` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `synopsis` text,
  `year_allo` int DEFAULT NULL,
  `director_allo` json DEFAULT NULL,
  `director_raw` json DEFAULT NULL,
  `genre` json DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `rating_press` float DEFAULT NULL,
  `rating_public` float DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `casting` json DEFAULT NULL,
  `distributor` varchar(255) DEFAULT NULL,
  `budget` bigint DEFAULT NULL,
  `lang` json DEFAULT NULL,
  `visa` int DEFAULT NULL,
  `award` int DEFAULT NULL,
  `thumbnail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_functionalities_filmscrap_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
