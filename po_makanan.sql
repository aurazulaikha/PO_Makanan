-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 12, 2025 at 11:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `po_makanan`
--

-- --------------------------------------------------------

--
-- Table structure for table `keranjang`
--

CREATE TABLE `keranjang` (
  `idKeranjang` bigint(20) UNSIGNED NOT NULL,
  `jumlah` double NOT NULL,
  `subtotal` double NOT NULL,
  `tanggalDitambahkan` date NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `menu_id` bigint(20) UNSIGNED NOT NULL,
  `statusKeranjang` varchar(50) NOT NULL DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `keranjang`
--

INSERT INTO `keranjang` (`idKeranjang`, `jumlah`, `subtotal`, `tanggalDitambahkan`, `user_id`, `menu_id`, `statusKeranjang`) VALUES
(2, 2, 6000, '2025-07-03', 2, 4, 'ordered'),
(3, 5, 80000, '2025-07-04', 3, 1, 'active'),
(4, 1, 16000, '2025-07-05', 3, 1, 'active'),
(5, 1, 3000, '2025-07-05', 3, 4, 'active'),
(6, 1, 16000, '2025-07-12', 2, 1, 'ordered'),
(7, 1, 6000, '2025-07-12', 2, 8, 'ordered'),
(8, 1, 16000, '2025-07-12', 2, 1, 'ordered'),
(11, 1, 16000, '2025-07-12', 87, 1, 'ordered'),
(12, 1, 3000, '2025-07-12', 87, 5, 'ordered'),
(13, 1, 16000, '2025-07-12', 88, 1, 'ordered');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `idMenu` bigint(20) UNSIGNED NOT NULL,
  `namaMenu` varchar(100) NOT NULL,
  `harga` double NOT NULL,
  `stok` int(11) DEFAULT 0,
  `kategori` enum('makanan','minuman','') NOT NULL,
  `gambar` varchar(255) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`idMenu`, `namaMenu`, `harga`, `stok`, `kategori`, `gambar`, `isActive`) VALUES
(1, 'Mie Ayam', 16000, 16, 'makanan', 'bakso.jpeg', 1),
(2, 'Lontong Sayur', 7000, 30, 'makanan', 'lontong.jpg', 1),
(3, 'Ayam Geprek', 15000, 50, 'makanan', 'geprek.png', 1),
(4, 'Teh Es', 3000, 198, 'minuman', 'teh.jpg', 1),
(5, 'Air Mineral', 3000, 299, 'minuman', 'air.jpg', 1),
(6, 'Nasi Goreng', 10000, 50, 'makanan', 'nasgor.jpg', 1),
(7, 'Es Jeruk', 10000, 30, 'minuman', 'esjeruk.jpg', 1),
(8, 'Teh Susu', 6000, 29, 'minuman', 'tehsusu.jpg', 1),
(9, 'Ayam bakar', 15000, 30, 'makanan', 'geprek.png', 1);

-- --------------------------------------------------------

--
-- Table structure for table `pesanan`
--

CREATE TABLE `pesanan` (
  `idPesanan` bigint(20) UNSIGNED NOT NULL,
  `keranjang_id` bigint(20) UNSIGNED NOT NULL,
  `pembayaran` varchar(255) DEFAULT NULL,
  `totalHarga` double NOT NULL,
  `statusPemesanan` enum('Diproses','Selesai','') NOT NULL,
  `tanggalPesanan` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pesanan`
--

INSERT INTO `pesanan` (`idPesanan`, `keranjang_id`, `pembayaran`, `totalHarga`, `statusPemesanan`, `tanggalPesanan`) VALUES
(1, 2, '6.jpeg', 6000, 'Diproses', '2025-07-04'),
(2, 6, 'lontong.jpg', 16000, 'Selesai', '2025-07-12'),
(3, 7, 'transaksi.jpg', 6000, 'Diproses', '2025-07-12'),
(4, 8, 'transaksi.jpg', 16000, 'Diproses', '2025-07-12'),
(5, 11, 'transaksi.jpg', 16000, 'Diproses', '2025-07-12'),
(6, 12, 'transaksi.jpg', 3000, 'Diproses', '2025-07-12'),
(7, 13, 'transaksi.jpg', 16000, 'Selesai', '2025-07-12');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` bigint(25) UNSIGNED NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_telp` varchar(20) NOT NULL,
  `role` enum('admin','pembeli') NOT NULL DEFAULT 'pembeli'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `nama`, `email`, `password`, `no_telp`, `role`) VALUES
(1, 'vinaa', 'vina@gmail.com', '$2y$10$hrFtWFPiyLZSYVhKEd0j1.3evbWHOrCdwtTtIfDFLk2QxR6gwIxp6', '088899997777', 'admin'),
(2, 'Aura', 'aura@gmail.com', '$2y$10$4BDabNEG0sJLecQRqk0Gtu4jHS809DP2eFUB/YcSxeEGXsNpc3Ww.', '081234567876', 'pembeli'),
(3, 'Obake', 'obake@gmail.com', '$2y$10$P.DEsdwl5TVgSaKKOyN4FurNDgCfgdxnhm4/i97TYsXgqahP247qC', '081123456789', 'pembeli'),
(74, 'T. Reza Susanti, S.Sos', 'user1@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(75, 'Tgk. Karen Salahudin, M.Ak', 'user2@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(76, 'Jarwi Uwais', 'user3@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(77, 'KH. Nasab Prasetya, M.Ak', 'user4@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(78, 'R.M. Capa Rahayu, S.Pd', 'user5@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(79, 'Ibrahim Budiyanto', 'user6@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(80, 'Kasiran Habibi', 'user7@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(81, 'Cahyo Marbun', 'user8@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(82, 'Puti Elma Budiyanto', 'user9@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(83, 'Maya Prastuti', 'user10@example.com', '$2b$12$PTMOa9g7msV33AZCWw7mEe5suST.4o1vTJMLTQUlhqBjiza6AVSym', '', 'pembeli'),
(84, 'vina', 'vinaa@gmail.com', '$2b$12$tx6BSeW1wWULIKJFeJvn4.VJ9L8B05rfSgoLKUJmsE2XfgeaUFOUu', '088899997777', 'pembeli'),
(86, 'admin', 'admin@gmail.com', '$2y$10$P.DEsdwl5TVgSaKKOyN4FurNDgCfgdxnhm4/i97TYsXgqahP247qC', '087722334455', 'admin'),
(87, 'Lalaa', 'lala@gmail.com', '$2b$12$2in64oxsi2LmdB1tRpJTaOcokmGu0GLPYCUHHQ4SjhHSV2mD.tkgi', '08123456789099', 'pembeli'),
(88, 'Citraa', 'citra@gmail.com', '$2b$12$KH3amEwJEsSAPQUdQdsFB.zTiZyvgAjU7GpWExBNd8QI9A8rk1wvy', '0812435678', 'pembeli');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD PRIMARY KEY (`idKeranjang`),
  ADD KEY `keranjang_menu_id` (`menu_id`),
  ADD KEY `keranjang_user_id` (`user_id`) USING BTREE;

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`idMenu`);

--
-- Indexes for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD PRIMARY KEY (`idPesanan`),
  ADD KEY `pesanan_keranjang_id` (`keranjang_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UC_Email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `keranjang`
--
ALTER TABLE `keranjang`
  MODIFY `idKeranjang` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `idMenu` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `pesanan`
--
ALTER TABLE `pesanan`
  MODIFY `idPesanan` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` bigint(25) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD CONSTRAINT `keranjang_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`idMenu`),
  ADD CONSTRAINT `keranjang_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD CONSTRAINT `pesanan_keranjang_id` FOREIGN KEY (`keranjang_id`) REFERENCES `keranjang` (`idKeranjang`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
