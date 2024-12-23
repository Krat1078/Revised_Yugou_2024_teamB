-- MySQL Script generated by MySQL Workbench
-- Wed Nov 20 10:29:27 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sample_django_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sample_django_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sample_django_db` DEFAULT CHARACTER SET utf8 ;
USE `sample_django_db` ;

-- -----------------------------------------------------
-- Table `sample_django_db`.`items_name_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sample_django_db`.`items_name_tag` (
  `item_name_id` INT NOT NULL AUTO_INCREMENT,
  `item_name` VARCHAR(100) NOT NULL COMMENT 'Name tags for items (Stationery, clothing, electronic equipment ...etc)',
  `description` TEXT NULL,
  PRIMARY KEY (`item_name_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sample_django_db`.`picked_or_dropped_locations_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sample_django_db`.`picked_or_dropped_locations_tag` (
  `PorD_location_id` INT NOT NULL AUTO_INCREMENT,
  `picked_or_dropped_location_name` VARCHAR(100) NOT NULL COMMENT 'Name of the place where it was found or dropped (Each faculty building, Student Center and on campus ...etc)\nFor more information, see the university map.',
  `description` TEXT NULL,
  PRIMARY KEY (`PorD_location_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sample_django_db`.`storage_locations_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sample_django_db`.`storage_locations_tag` (
  `storage_location_id` INT NOT NULL AUTO_INCREMENT,
  `storage_location_name` VARCHAR(100) NOT NULL COMMENT 'Name of the place to store lost items (Administrative offices of each faculty, gym, library, Student Center Building A)',
  `description` TEXT NULL,
  PRIMARY KEY (`storage_location_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sample_django_db`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sample_django_db`.`item` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `item_name_id` INT NOT NULL COMMENT 'Foreign key referencing id in the items_name_tags table (Name tags for items)',
  `PorD_location_id` INT NOT NULL COMMENT 'Foreign key referencing id in the picked_or_dropped_locations table (picked or dropped locations)',
  `storage_location_id` INT NOT NULL COMMENT 'Foreign key referencing id in the storage_locations_tags table (storage_locations)',
  `item_type` INT NOT NULL COMMENT 'Integer code indicating if it\'s a lost or found item (e.g., 0: found, 1: lost)',
  `status` TINYINT NOT NULL COMMENT 'Integer code for processing status (e.g., 0: pending, 1: in progress, 2: resolved)',
  `created_at` DATETIME NOT NULL COMMENT 'Date and time when the item was added',
  `updated_at` DATETIME NULL COMMENT 'Date and time when the item was last updated',
  `contact_email` VARCHAR(100) NULL,
  `contact_phone` VARCHAR(20) NULL,
  PRIMARY KEY (`item_id`),
  INDEX `item_name_tag_idx` (`item_name_id` ASC) VISIBLE,
  INDEX `fk_items_picked_or_dropped_locations_tags1_idx` (`PorD_location_id` ASC) VISIBLE,
  INDEX `fk_items_storage_location_tag1_idx` (`storage_location_id` ASC) VISIBLE,
  CONSTRAINT `item_name_tag`
    FOREIGN KEY (`item_name_id`)
    REFERENCES `sample_django_db`.`items_name_tag` (`item_name_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_items_picked_or_dropped_locations_tags1`
    FOREIGN KEY (`PorD_location_id`)
    REFERENCES `sample_django_db`.`picked_or_dropped_locations_tag` (`PorD_location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_items_storage_location_tag1`
    FOREIGN KEY (`storage_location_id`)
    REFERENCES `sample_django_db`.`storage_locations_tag` (`storage_location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sample_django_db`.`item_image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sample_django_db`.`item_image` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL,
  `image_path` VARCHAR(225) NOT NULL,
  `uploaded_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `items_id_idx` (`item_id` ASC) VISIBLE,
  CONSTRAINT `items_id`
    FOREIGN KEY (`item_id`)
    REFERENCES `sample_django_db`.`item` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
