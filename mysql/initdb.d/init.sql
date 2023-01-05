CREATE DATABASE IF NOT EXISTS sample_db;

CREATE TABLE IF NOT EXISTS sample_db.to_dos (
    `id` varchar(191) NOT NULL,
    `title` longtext,
    `memo` longtext,
    `deadline` datetime(3) DEFAULT NULL,
    `created_at` datetime(3) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ;

INSERT IGNORE INTO sample_db.to_dos (id, title, memo, deadline)
    VALUES ('1st', 'title1', 'memomemo', '2022-12-12 12:12:12'),
    ('2nd', 'title2', 'memomemomemo', '2023-01-01 01:01:01');


CREATE TABLE IF NOT EXISTS sample_db.images (
    `id` varchar(191) NOT NULL,
    `title` longtext,
    `memo` longtext,
    `image_path` longtext,
    `created_at` datetime(3) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ;

INSERT IGNORE INTO sample_db.images (id, title, memo)
    VALUES ('1st', 'title1', 'memomemo'),
    ('2nd', 'title2', 'memomemomemo');
