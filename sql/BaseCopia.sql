-- MySQL dump 10.13  Distrib 8.0.46, for macos15 (arm64)
--
-- Host: localhost    Database: tarea2
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actividad`
--

DROP TABLE IF EXISTS `actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `miembro_id` int NOT NULL,
  `dia` enum('lunes','martes','miércoles','jueves','viernes','sábado','domingo') NOT NULL,
  `hora_inicio` varchar(5) NOT NULL,
  `duracion` varchar(5) NOT NULL,
  `tipo` enum('arte','deporte','tecnología','social','recreación','otra') NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `descripcion` text,
  `dias` varchar(200) DEFAULT NULL,
  `hora_fin` varchar(20) DEFAULT NULL,
  `lugar` varchar(200) DEFAULT NULL,
  `acompanado` varchar(200) DEFAULT NULL,
  `entretencion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_actividad_miembro1_idx` (`miembro_id`),
  CONSTRAINT `fk_actividad_miembro1` FOREIGN KEY (`miembro_id`) REFERENCES `miembro` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividad`
--

LOCK TABLES `actividad` WRITE;
/*!40000 ALTER TABLE `actividad` DISABLE KEYS */;
INSERT INTO `actividad` VALUES (1,1,'lunes','15:00','01:00','deporte','Fútbol','Actividad deportiva en la cancha del DCC','lunes','16:00','Cancha DCC','Con amigos','Muy entretenida'),(2,2,'lunes','18:00','02:00','recreación','Ajedrez','Partidas de ajedrez con estudiantes','lunes miercoles','20:00','Sala de estudio DCC','Con amigos de la generación','Muy entretenida'),(3,3,'martes','17:00','02:00','deporte','Voleibol','Voleibol en cancha Beauchef','martes jueves','19:00','Cancha Beauchef','',''),(4,4,'sábado','10:00','02:00','deporte','Patinaje','Patinaje recreativo en el parque','sabado domingo','12:00','Parque O\'Higgins','','Entretenida'),(5,5,'lunes','19:00','02:00','deporte','Basquetbol','Basquetbol en el gimnasio','lunes viernes','21:00','Gimnasio Beauchef','Con compañeros del DCC',''),(6,6,'miércoles','16:00','02:00','recreación','Ajedrez','Ajedrez en biblioteca','miercoles','18:00','Biblioteca Central','',''),(7,7,'martes','18:30','01:30','deporte','Voleibol','Voleibol en multicancha DCC','martes sabado','20:00','Multicancha DCC','Con su familia','Muy entretenida'),(8,8,'lunes','18:30','02:30','otra','Hacer churrasquitos','Hacer churrasquitos','Lunes Jueves','21:00','Casino','Profe San Martín','Muy entretenida'),(9,8,'miércoles','00:00','14:00','otra','Patinaje','Patinaje','Miércoles','14:00','Parque Ohiggins','','');
/*!40000 ALTER TABLE `actividad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comuna`
--

DROP TABLE IF EXISTS `comuna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comuna` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `region_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comuna_region1_idx` (`region_id`),
  CONSTRAINT `fk_comuna_region1` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130607 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comuna`
--

LOCK TABLES `comuna` WRITE;
/*!40000 ALTER TABLE `comuna` DISABLE KEYS */;
INSERT INTO `comuna` VALUES (10101,'Gral. Lagos',15),(10102,'Putre',15),(10201,'Arica',15),(10202,'Camarones',15),(10301,'Camiña',1),(10302,'Huara',1),(10303,'Pozo Almonte',1),(10304,'Iquique',1),(10305,'Pica',1),(10306,'Colchane',1),(10307,'Alto Hospicio',1),(20101,'Tocopilla',2),(20102,'Maria Elena',2),(20201,'Ollague',2),(20202,'Calama',2),(20203,'San Pedro Atacama',2),(20301,'Sierra Gorda',2),(20302,'Mejillones',2),(20303,'Antofagasta',2),(20304,'Taltal',2),(30101,'Diego de Almagro',3),(30102,'Chañaral',3),(30201,'Caldera',3),(30202,'Copiapo',3),(30203,'Tierra Amarilla',3),(30301,'Huasco',3),(30302,'Freirina',3),(30303,'Vallenar',3),(30304,'Alto del Carmen',3),(40101,'La Higuera',4),(40102,'La Serena',4),(40103,'Vicuña',4),(40104,'Paihuano',4),(40105,'Coquimbo',4),(40106,'Andacollo',4),(40201,'Rio Hurtado',4),(40202,'Ovalle',4),(40203,'Monte Patria',4),(40204,'Punitaqui',4),(40205,'Combarbala',4),(40301,'Mincha',4),(40302,'Illapel',4),(40303,'Salamanca',4),(40304,'Los Vilos',4),(50101,'Petorca',5),(50102,'Cabildo',5),(50103,'Papudo',5),(50104,'La Ligua',5),(50105,'Zapallar',5),(50201,'Putaendo',5),(50202,'Santa Maria',5),(50203,'San Felipe',5),(50204,'Pencahue',5),(50205,'Catemu',5),(50206,'Llay Llay',5),(50301,'Nogales',5),(50302,'La Calera',5),(50303,'Hijuelas',5),(50304,'La Cruz',5),(50305,'Quillota',5),(50306,'Olmue',5),(50307,'Limache',5),(50401,'Los Andes',5),(50402,'Rinconada',5),(50403,'Calle Larga',5),(50404,'San Esteban',5),(50501,'Puchuncavi',5),(50502,'Quintero',5),(50503,'Viña del Mar',5),(50504,'Villa Alemana',5),(50505,'Quilpue',5),(50506,'Valparaiso',5),(50507,'Juan Fernandez',5),(50508,'Casablanca',5),(50509,'Concon',5),(50601,'Isla de Pascua',5),(50701,'Algarrobo',5),(50702,'El Quisco',5),(50703,'El Tabo',5),(50704,'Cartagena',5),(50705,'San Antonio',5),(50706,'Santo Domingo',5),(60101,'Mostazal',6),(60102,'Codegua',6),(60103,'Graneros',6),(60104,'Machali',6),(60105,'Rancagua',6),(60106,'Olivar',6),(60107,'Doñihue',6),(60108,'Requinoa',6),(60109,'Coinco',6),(60110,'Coltauco',6),(60111,'Quinta Tilcoco',6),(60112,'Las Cabras',6),(60113,'Rengo',6),(60114,'Peumo',6),(60115,'Pichidegua',6),(60116,'Malloa',6),(60117,'San Vicente',6),(60201,'Navidad',6),(60202,'La Estrella',6),(60203,'Marchigue',6),(60204,'Pichilemu',6),(60205,'Litueche',6),(60206,'Paredones',6),(60301,'San Fernando',6),(60302,'Peralillo',6),(60303,'Placilla',6),(60304,'Chimbarongo',6),(60305,'Palmilla',6),(60306,'Nancagua',6),(60307,'Santa Cruz',6),(60308,'Pumanque',6),(60309,'Chepica',6),(60310,'Lolol',6),(70101,'Teno',7),(70102,'Romeral',7),(70103,'Rauco',7),(70104,'Curico',7),(70105,'Sagrada Familia',7),(70106,'Hualañe',7),(70107,'Vichuquen',7),(70108,'Molina',7),(70109,'Licanten',7),(70201,'Rio Claro',7),(70202,'Curepto',7),(70203,'Pelarco',7),(70204,'Talca',7),(70205,'Pencahue',7),(70206,'San Clemente',7),(70207,'Constitucion',7),(70208,'Maule',7),(70209,'Empedrado',7),(70210,'San Rafael',7),(70301,'San Javier',7),(70302,'Colbun',7),(70303,'Villa Alegre',7),(70304,'Yerbas Buenas',7),(70305,'Linares',7),(70306,'Longavi',7),(70307,'Retiro',7),(70308,'Parral',7),(70401,'Chanco',7),(70402,'Pelluhue',7),(70403,'Cauquenes',7),(80101,'Cobquecura',16),(80102,'Ñiquen',16),(80103,'San Fabian',16),(80104,'San Carlos',16),(80105,'Quirihue',16),(80106,'Ninhue',16),(80107,'Trehuaco',16),(80108,'San Nicolas',16),(80109,'Coihueco',16),(80110,'Chillan',16),(80111,'Portezuelo',16),(80112,'Pinto',16),(80113,'Coelemu',16),(80114,'Bulnes',16),(80115,'San Ignacio',16),(80116,'Ranquil',16),(80117,'Quillon',16),(80118,'El Carmen',16),(80119,'Pemuco',16),(80120,'Yungay',16),(80121,'Chillan Viejo',16),(80201,'Tome',8),(80202,'Florida',8),(80203,'Penco',8),(80204,'Talcahuano',8),(80205,'Concepcion',8),(80206,'Hualqui',8),(80207,'Coronel',8),(80208,'Lota',8),(80209,'Santa Juana',8),(80210,'Chiguayante',8),(80211,'San Pedro de la Paz',8),(80212,'Hualpen',8),(80301,'Cabrero',8),(80302,'Yumbel',8),(80303,'Tucapel',8),(80304,'Antuco',8),(80305,'San Rosendo',8),(80306,'Laja',8),(80307,'Quilleco',8),(80308,'Los Angeles',8),(80309,'Nacimiento',8),(80310,'Negrete',8),(80311,'Santa Barbara',8),(80312,'Quilaco',8),(80313,'Mulchen',8),(80314,'Alto Bio Bio',8),(80401,'Arauco',8),(80402,'Curanilahue',8),(80403,'Los Alamos',8),(80404,'Lebu',8),(80405,'Cañete',8),(80406,'Contulmo',8),(80407,'Tirua',8),(90101,'Renaico',9),(90102,'Angol',9),(90103,'Collipulli',9),(90104,'Los Sauces',9),(90105,'Puren',9),(90106,'Ercilla',9),(90107,'Lumaco',9),(90108,'Victoria',9),(90109,'Traiguen',9),(90110,'Curacautin',9),(90111,'Lonquimay',9),(90201,'Perquenco',9),(90202,'Galvarino',9),(90203,'Lautaro',9),(90204,'Vilcun',9),(90205,'Temuco',9),(90206,'Carahue',9),(90207,'Melipeuco',9),(90208,'Nueva Imperial',9),(90209,'Puerto Saavedra',9),(90210,'Cunco',9),(90211,'Freire',9),(90212,'Pitrufquen',9),(90213,'Teodoro Schmidt',9),(90214,'Gorbea',9),(90215,'Pucon',9),(90216,'Villarrica',9),(90217,'Tolten',9),(90218,'Curarrehue',9),(90219,'Loncoche',9),(90220,'Padre Las Casas',9),(90221,'Cholchol',9),(100101,'Lanco',14),(100102,'Mariquina',14),(100103,'Panguipulli',14),(100104,'Mafil',14),(100105,'Valdivia',14),(100106,'Los Lagos',14),(100107,'Corral',14),(100108,'Paillaco',14),(100109,'Futrono',14),(100110,'Lago Ranco',14),(100111,'La Union',14),(100112,'Rio Bueno',14),(100201,'San Pablo',10),(100202,'San Juan',10),(100203,'Osorno',10),(100204,'Puyehue',10),(100205,'Rio Negro',10),(100206,'Purranque',10),(100207,'Puerto Octay',10),(100301,'Frutillar',10),(100302,'Fresia',10),(100303,'Llanquihue',10),(100304,'Puerto Varas',10),(100305,'Los Muermos',10),(100306,'Puerto Montt',10),(100307,'Maullin',10),(100308,'Calbuco',10),(100309,'Cochamo',10),(100401,'Ancud',10),(100402,'Quemchi',10),(100403,'Dalcahue',10),(100404,'Curaco de Velez',10),(100405,'Castro',10),(100406,'Chonchi',10),(100407,'Queilen',10),(100408,'Quellon',10),(100409,'Quinchao',10),(100410,'Puqueldon',10),(100501,'Chaiten',10),(100502,'Futaleufu',10),(100503,'Palena',10),(100504,'Hualaihue',10),(110101,'Guaitecas',11),(110102,'Cisnes',11),(110103,'Aysen',11),(110201,'Coyhaique',11),(110202,'Lago Verde',11),(110301,'Rio Ibañez',11),(110302,'Chile Chico',11),(110401,'Cochrane',11),(110402,'Tortel',11),(110403,'O\'Higgins',11),(120101,'Torres del Paine',12),(120102,'Puerto Natales',12),(120201,'Laguna Blanca',12),(120202,'San Gregorio',12),(120203,'Rio Verde',12),(120204,'Punta Arenas',12),(120301,'Porvenir',12),(120302,'Primavera',12),(120303,'Timaukel',12),(120401,'Antartica',12),(130101,'Tiltil',13),(130102,'Colina',13),(130103,'Lampa',13),(130201,'Conchali',13),(130202,'Quilicura',13),(130203,'Renca',13),(130204,'Las Condes',13),(130205,'Pudahuel',13),(130206,'Quinta Normal',13),(130207,'Providencia',13),(130208,'Santiago',13),(130209,'La Reina',13),(130210,'Ñuñoa',13),(130211,'San Miguel',13),(130212,'Maipú',13),(130213,'La Cisterna',13),(130214,'La Florida',13),(130215,'La Granja',13),(130216,'Independencia',13),(130217,'Huechuraba',13),(130218,'Recoleta',13),(130219,'Vitacura',13),(130220,'Lo Barrenechea',13),(130221,'Macul',13),(130222,'Peñalolén',13),(130223,'San Joaquín',13),(130224,'La Pintana',13),(130225,'San Ramon',13),(130226,'El Bosque',13),(130227,'Pedro Aguirre Cerda',13),(130228,'Lo Espejo',13),(130229,'Estacion Central',13),(130230,'Cerrillos',13),(130231,'Lo Prado',13),(130232,'Cerro Navia',13),(130301,'San José de Maipo',13),(130302,'Puente Alto',13),(130303,'Pirque',13),(130401,'San Bernardo',13),(130402,'Calera de Tango',13),(130403,'Buin',13),(130404,'Paine',13),(130501,'Peñaflor',13),(130502,'Talagante',13),(130503,'El Monte',13),(130504,'Isla de Maipo',13),(130601,'Curacavi',13),(130602,'María Pinto',13),(130603,'Melipilla',13),(130604,'San Pedro',13),(130605,'Alhué',13),(130606,'Padre Hurtado',13);
/*!40000 ALTER TABLE `comuna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foto`
--

DROP TABLE IF EXISTS `foto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ruta_archivo` varchar(300) NOT NULL,
  `nombre_archivo` varchar(300) NOT NULL,
  `actividad_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_foto_actividad1_idx` (`actividad_id`),
  CONSTRAINT `fk_foto_actividad1` FOREIGN KEY (`actividad_id`) REFERENCES `actividad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foto`
--

LOCK TABLES `foto` WRITE;
/*!40000 ALTER TABLE `foto` DISABLE KEYS */;
INSERT INTO `foto` VALUES (1,'static/archivos/DccActividades.png','DccActividades.png',8),(2,'static/archivos/patinaje.png','patinaje.png',9);
/*!40000 ALTER TABLE `foto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `miembro`
--

DROP TABLE IF EXISTS `miembro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `miembro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(80) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `comuna_id` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `comuna` varchar(100) NOT NULL,
  `correo` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_miembro_comuna1_idx` (`comuna_id`),
  CONSTRAINT `fk_miembro_comuna1` FOREIGN KEY (`comuna_id`) REFERENCES `comuna` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `miembro`
--

LOCK TABLES `miembro` WRITE;
/*!40000 ALTER TABLE `miembro` DISABLE KEYS */;
INSERT INTO `miembro` VALUES (1,'Usuario','usua@rio.com','+56900000000','2026-05-02 00:00:00',130208,'estudiante','Prueba','Usuario123','Metropolitana','Santiago',NULL),(2,'Ana','ana@uchile.cl','+56911111111','2026-05-03 00:00:00',130207,'estudiante','Soto','Ana123','Metropolitana','Providencia',NULL),(3,'Carlos','carlos@uchile.cl','+56922222222','2026-05-04 00:00:00',50503,'profesor','Pérez','Carlos123','Valparaíso','Viña del Mar',NULL),(4,'María','maria@uchile.cl','+56933333333','2026-05-05 00:00:00',80205,'estudiante','Díaz','Maria123','Biobío','Concepcion',NULL),(5,'Javier','javier@uchile.cl','+56944444444','2026-05-06 00:00:00',130204,'estudiante','Muñoz','Javier123','Metropolitana','Las Condes',NULL),(6,'Laura','laura@uchile.cl','+56955555555','2026-05-07 00:00:00',130210,'profesor','Gómez','Laura123','Metropolitana','Ñuñoa',NULL),(7,'Diego','diego@uchile.cl','+56966666666','2026-05-08 00:00:00',130212,'funcionario','Salas','Diego123','Metropolitana','Maipú',NULL),(8,'Benjas','benjas@uchile.cl','+56971313131','2026-05-10 19:31:31',130214,'estudiante','Sepúlveda','Benjas1234','Región Metropolitana de Santiago ','La Florida',NULL);
/*!40000 ALTER TABLE `miembro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Región de Tarapacá'),(2,'Región de Antofagasta'),(3,'Región de Atacama'),(4,'Región de Coquimbo '),(5,'Región de Valparaíso'),(6,'Región del Libertador Bernardo O\'Higgins'),(7,'Región del Maule'),(8,'Región del Biobío'),(9,'Región de La Araucanía'),(10,'Región de Los Lagos'),(11,'Región Aisén del General Carlos Ibáñez del Campo'),(12,'Región de Magallanes y la Antártica Chilena'),(13,'Región Metropolitana de Santiago '),(14,'Región de Los Ríos'),(15,'Región Arica y Parinacota'),(16,'Región del Ñuble');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-10 22:09:57
