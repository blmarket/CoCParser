CREATE TABLE `src` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DATA` mediumblob,
  `category` varchar(128) DEFAULT NULL,
  `PNG` mediumblob,
  `data_url` varchar(512) DEFAULT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=607 DEFAULT CHARSET=utf8;

CREATE TABLE `samples` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `src_id` int(11) NOT NULL,
  `clan_place` tinyint(4) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `attack1` tinyint(4) DEFAULT NULL,
  `attack2` tinyint(4) DEFAULT NULL,
  `total_stars` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `src_id` (`src_id`),
  CONSTRAINT `samples_ibfk_1` FOREIGN KEY (`src_id`) REFERENCES `src` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=utf8;

CREATE TABLE `predictions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `field_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

CREATE TABLE `predict_result` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
