CREATE DATABASE IF NOT EXISTS sample_db;
CREATE TABLE IF NOT EXISTS sample_db.sample (
    id INT(11) AUTO_INCREMENT NOT NULL, 
    name VARCHAR(30) NOT NULL COLLATE utf8mb4_unicode_ci, 
    age INT(3) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO sample_db.sample (name, age)
        VALUES ('1st', '25'),
        ('2nd', '23'),
        ('3rd', '21');