DROP TABLE IF EXISTS `recipes`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`
(
    `id`       INT          NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `role`     VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`username`)
);

CREATE TABLE `recipes`
(
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `category`    VARCHAR(255) NOT NULL,
    `name`        VARCHAR(255) NOT NULL,
    `description` TEXT         NOT NULL,
    `difficulty`  INT          NOT NULL,
    PRIMARY KEY (`id`)
);