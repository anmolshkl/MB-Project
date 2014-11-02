-- phpMyAdmin SQL Dump
-- version 4.1.6
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Oct 27, 2014 at 06:43 PM
-- Server version: 5.6.16
-- PHP Version: 5.5.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mb_db2`
--

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp`
--

CREATE TABLE IF NOT EXISTS `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(100) NOT NULL,
  `secret` varchar(100) NOT NULL,
  `key` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `socialaccount_socialapp`
--

INSERT INTO `socialaccount_socialapp` (`id`, `provider`, `name`, `client_id`, `secret`, `key`) VALUES
(1, 'linkedin', 'LinkedIn', '75v6ppasybk7zd', 'WJjgPEsGW7NSCVCD', ''),
(2, 'facebook', 'Facebook', '713549365387916', '5fd7cd3b9958b979647df997b5b27c8e', ''),
(3, 'google', 'Google', '745226397307-sktc3grus53u160q3icthf5s51ukijke.apps.googleusercontent.com', 'Qg4q0dAsipUqAuYa2TOVnMGF', ''),
(4, 'twitter', 'Twitter', 'R4LNGeDnrA6xUfuZHn6rcs9qY', 'UBQL0dlSeODOXHMWltGqX0vxtk4rPZBVC599yWkZMHM7KTi3yD', ''),
(5, 'github', 'Github', '6794ac2dc9ec74a13392', '40d82fc51a9f2ad4595642cc30c6bb8568eb39f1', '');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
