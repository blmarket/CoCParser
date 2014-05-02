CREATE TABLE `src` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DATA` mediumblob,
  `category` varchar(128) DEFAULT NULL,
  `PNG` mediumblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8;


CREATE TABLE `samples` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `src_id` int(11) NOT NULL,
  `attack` tinyint(4) DEFAULT NULL,
  `predict_attack` tinyint(4) DEFAULT NULL,
  `atkstars` tinyint(4) DEFAULT NULL,
  `predict_atkstars` tinyint(4) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `src_id` (`src_id`),
  CONSTRAINT `samples_ibfk_1` FOREIGN KEY (`src_id`) REFERENCES `src` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=450 DEFAULT CHARSET=utf8;
