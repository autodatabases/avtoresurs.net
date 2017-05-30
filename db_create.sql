CREATE TABLE `all_articles` (
  `supplierid`                BIGINT(20)   NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128) NOT NULL,
  KEY `all_articles_idx01` (`supplierid`),
  KEY `all_articles_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `all_articles_csv` (
  `id`                        BIGINT(20) NOT NULL AUTO_INCREMENT,
  `supplierid`                BIGINT(20) NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128)        DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `all_articles_csv_idx01` (`supplierid`),
  KEY `all_articles_csv_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 4336603
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_acc` (
  `supplierId`                   BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber`    VARCHAR(128) NOT NULL,
  `Description`                  VARCHAR(128) NOT NULL,
  `AccSupplierId`                BIGINT(20)   NOT NULL,
  `AccDataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  KEY `article_acc_idx01` (`supplierId`),
  KEY `article_acc_idx02` (`DataSupplierArticleNumber`),
  KEY `article_acc_idx03` (`AccSupplierId`),
  KEY `article_acc_idx04` (`AccDataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_attributes` (
  `supplierid`                BIGINT(20)    NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128)  NOT NULL,
  `id`                        BIGINT(20)    NOT NULL,
  `attributeinformationtype`  VARCHAR(512)  NOT NULL,
  `description`               VARCHAR(512) DEFAULT NULL,
  `displaytitle`              VARCHAR(512) DEFAULT NULL,
  `displayvalue`              VARCHAR(4096) NOT NULL,
  KEY `article_attributes_idx01` (`supplierid`),
  KEY `article_attributes_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_cross` (
  `manufacturerId`                 BIGINT(20)   NOT NULL,
  `OENbr`                          VARCHAR(128) NOT NULL,
  `SupplierId`                     BIGINT(20)   NOT NULL,
  `PartsDataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  KEY `article_cross_idx01` (`manufacturerId`),
  KEY `article_cross_idx02` (`OENbr`),
  KEY `article_cross_idx03` (`SupplierId`),
  KEY `article_cross_idx04` (`PartsDataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_images` (
  `supplierId`                BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  `AdditionalDescription`     VARCHAR(128) NOT NULL,
  `Description`               VARCHAR(128) NOT NULL,
  `DocumentName`              VARCHAR(128) NOT NULL,
  `DocumentType`              VARCHAR(128) NOT NULL,
  `NormedDescriptionID`       VARCHAR(128) NOT NULL,
  `PictureName`               VARCHAR(128) NOT NULL,
  `ShowImmediately`           VARCHAR(128) NOT NULL,
  KEY `article_images_idx01` (`supplierId`),
  KEY `article_images_idx02` (`DataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_inf` (
  `supplierId`                BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  `InformationText`           TEXT         NOT NULL,
  `InformationType`           VARCHAR(128) NOT NULL,
  `InformationTypeKey`        VARCHAR(128) NOT NULL,
  KEY `article_inf_idx01` (`supplierId`),
  KEY `article_inf_idx02` (`DataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_li` (
  `supplierId`                BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  `linkageTypeId`             VARCHAR(128) NOT NULL,
  `linkageId`                 BIGINT(20)   NOT NULL,
  KEY `article_li_idx01` (`supplierId`),
  KEY `article_li_idx02` (`DataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_links` (
  `supplierid`                BIGINT(20) NOT NULL,
  `productid`                 BIGINT(20) NOT NULL,
  `linkagetypeid`             BIGINT(20) NOT NULL,
  `linkageid`                 BIGINT(20) NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128) DEFAULT NULL,
  KEY `article_links_idx01` (`supplierid`),
  KEY `article_links_idx02` (`productid`),
  KEY `article_links_idx03` (`linkagetypeid`),
  KEY `article_links_idx04` (`linkageid`),
  KEY `article_links_idx05` (`datasupplierarticlenumber`),
  KEY `article_links_idx06` (`linkageid`, `linkagetypeid`, `productid`, `supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_nn` (
  `supplierid`                   BIGINT(20)   NOT NULL,
  `datasupplierarticlenumber`    VARCHAR(128) NOT NULL,
  `newnbr`                       VARCHAR(128) NOT NULL,
  `newsupplierid`                BIGINT(20)   NOT NULL,
  `newdatasupplierarticlenumber` VARCHAR(128) NOT NULL,
  KEY `article_nn_idx01` (`supplierid`),
  KEY `article_nn_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_oe` (
  `supplierid`                BIGINT(20)   NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128) NOT NULL,
  `IsAdditive`                VARCHAR(128) NOT NULL,
  `OENbr`                     VARCHAR(128) NOT NULL,
  `manufacturerId`            BIGINT(20)   NOT NULL,
  KEY `article_oe_idx01` (`supplierid`),
  KEY `article_oe_idx02` (`datasupplierarticlenumber`),
  KEY `article_oe_idx03` (`manufacturerId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_parts` (
  `supplierId`                     BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber`      VARCHAR(128) NOT NULL,
  `Quantity`                       VARCHAR(128) NOT NULL,
  `PartsSupplierId`                BIGINT(20)   NOT NULL,
  `PartsDataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  KEY `article_parts_idx01` (`supplierId`),
  KEY `article_parts_idx02` (`DataSupplierArticleNumber`),
  KEY `article_parts_idx03` (`PartsSupplierId`),
  KEY `article_parts_idx04` (`PartsDataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_rn` (
  `supplierid`                       BIGINT(20)   NOT NULL,
  `datasupplierarticlenumber`        VARCHAR(128) NOT NULL,
  `replacenbr`                       VARCHAR(128) NOT NULL,
  `replacedupplierid`                BIGINT(20)   NOT NULL,
  `replacedatasupplierarticlenumber` VARCHAR(128) NOT NULL,
  KEY `article_rn_idx01` (`supplierid`),
  KEY `article_rn_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `article_un` (
  `supplierid`                BIGINT(20)   NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128) NOT NULL,
  `utilityno`                 VARCHAR(128) NOT NULL,
  KEY `article_un_idx01` (`supplierid`),
  KEY `article_un_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `articles` (
  `supplierId`                BIGINT(20)   NOT NULL,
  `DataSupplierArticleNumber` VARCHAR(128) NOT NULL,
  `ArticleStateDisplayTitle`  VARCHAR(128) NOT NULL,
  `ArticleStateDisplayValue`  VARCHAR(128) NOT NULL,
  `Description`               VARCHAR(128) NOT NULL,
  `FlagAccessory`             VARCHAR(128) NOT NULL,
  `FlagMaterialCertification` VARCHAR(128) NOT NULL,
  `FlagRemanufactured`        VARCHAR(128) NOT NULL,
  `FlagSelfServicePacking`    VARCHAR(128) NOT NULL,
  `FoundBy`                   VARCHAR(128) NOT NULL,
  `FoundString`               VARCHAR(128) NOT NULL,
  `HasAxle`                   VARCHAR(128) NOT NULL,
  `HasCommercialVehicle`      VARCHAR(128) NOT NULL,
  `HasCVManuID`               VARCHAR(128) NOT NULL,
  `HasEngine`                 VARCHAR(128) NOT NULL,
  `HasLinkitems`              VARCHAR(128) NOT NULL,
  `HasMotorbike`              VARCHAR(128) NOT NULL,
  `HasPassengerCar`           VARCHAR(128) NOT NULL,
  `IsValid`                   VARCHAR(128) NOT NULL,
  `LotSize1`                  VARCHAR(128) NOT NULL,
  `LotSize2`                  VARCHAR(128) NOT NULL,
  `NormalizedDescription`     VARCHAR(128) NOT NULL,
  `PackingUnit`               VARCHAR(128) NOT NULL,
  `QuantityPerPackingUnit`    VARCHAR(128) NOT NULL,
  KEY `articles_idx01` (`supplierId`),
  KEY `articles_idx02` (`DataSupplierArticleNumber`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `articles_csv` (
  `id`                        BIGINT(20) NOT NULL AUTO_INCREMENT,
  `supplierid`                BIGINT(20) NOT NULL,
  `datasupplierarticlenumber` VARCHAR(128)        DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `articles_csv_idx01` (`supplierid`),
  KEY `articles_csv_idx02` (`datasupplierarticlenumber`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 3668292
  DEFAULT CHARSET = utf8;
CREATE TABLE `axle_attributes` (
  `axleid`         BIGINT(20) NOT NULL,
  `attributegroup` VARCHAR(512)  DEFAULT NULL,
  `attributetype`  VARCHAR(512)  DEFAULT NULL,
  `displaytitle`   VARCHAR(512)  DEFAULT NULL,
  `displayvalue`   VARCHAR(2048) DEFAULT NULL,
  KEY `axle_attributes_idx01` (`axleid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `axle_pds` (
  `axleid`     BIGINT(20) NOT NULL,
  `nodeid`     BIGINT(20) NOT NULL,
  `productid`  BIGINT(20) NOT NULL,
  `supplierid` BIGINT(20) NOT NULL,
  KEY `axle_pds_idx01` (`axleid`),
  KEY `axle_pds_idx02` (`nodeid`),
  KEY `axle_pds_idx03` (`productid`),
  KEY `axle_pds_idx04` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `axle_prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `axle_prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `axle_qsi` (
  `axleid`         BIGINT(20) NOT NULL,
  `description`    VARCHAR(512) DEFAULT NULL,
  `quickstarttype` VARCHAR(512) DEFAULT NULL,
  `validstate`     VARCHAR(512) DEFAULT NULL,
  KEY `axle_qsi_idx01` (`axleid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `axle_trees` (
  `axleid`       BIGINT(20) NOT NULL,
  `searchtreeid` BIGINT(20) NOT NULL,
  `id`           BIGINT(20) NOT NULL,
  `parentid`     BIGINT(20)   DEFAULT NULL,
  `description`  VARCHAR(512) DEFAULT NULL,
  KEY `axle_trees_idx01` (`axleid`),
  KEY `axle_trees_idx02` (`id`),
  KEY `axle_trees_idx03` (`parentid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `axles` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `modelid`                  BIGINT(20)   DEFAULT NULL,
  KEY `axles_idx01` (`id`),
  KEY `axles_idx02` (`modelid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_driver_cabs` (
  `id`          BIGINT(20) NOT NULL,
  `drivercabid` BIGINT(20) NOT NULL,
  KEY `commercial_driver_cabs_idx01` (`id`),
  KEY `commercial_driver_cabs_idx02` (`drivercabid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_attributes` (
  `commercialvehicleid` BIGINT(20) NOT NULL,
  `attributegroup`      VARCHAR(512)  DEFAULT NULL,
  `attributetype`       VARCHAR(512)  DEFAULT NULL,
  `displaytitle`        VARCHAR(512)  DEFAULT NULL,
  `displayvalue`        VARCHAR(2048) DEFAULT NULL,
  KEY `commercial_vehicle_attributes_idx01` (`commercialvehicleid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_axles` (
  `id`     BIGINT(20) NOT NULL,
  `axleid` BIGINT(20) NOT NULL,
  KEY `commercial_vehicle_axles_idx01` (`id`),
  KEY `commercial_vehicle_axles_idx02` (`axleid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_engines` (
  `id`       BIGINT(20) NOT NULL,
  `engineid` BIGINT(20) NOT NULL,
  KEY `commercial_vehicle_engines_idx01` (`id`),
  KEY `commercial_vehicle_engines_idx02` (`engineid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_pds` (
  `commertialvehicleid` BIGINT(20) NOT NULL,
  `nodeid`              BIGINT(20) NOT NULL,
  `productid`           BIGINT(20) NOT NULL,
  `supplierid`          BIGINT(20) NOT NULL,
  KEY `commercial_vehicle_pds_idx01` (`commertialvehicleid`),
  KEY `commercial_vehicle_pds_idx02` (`nodeid`),
  KEY `commercial_vehicle_pds_idx03` (`productid`),
  KEY `commercial_vehicle_pds_idx04` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `commercial_vehicle_prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_qsi` (
  `commercialvehicleid` BIGINT(20) NOT NULL,
  `description`         VARCHAR(512) DEFAULT NULL,
  `quickstarttype`      VARCHAR(512) DEFAULT NULL,
  `validstate`          VARCHAR(512) DEFAULT NULL,
  KEY `commercial_vehicle_qsi_idx01` (`commercialvehicleid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_sub_types` (
  `id`        BIGINT(20) NOT NULL,
  `subtypeid` BIGINT(20) NOT NULL,
  KEY `commercial_vehicle_sub_types_idx01` (`id`),
  KEY `commercial_vehicle_sub_types_idx02` (`subtypeid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicle_trees` (
  `commercialvehicleid` BIGINT(20) NOT NULL,
  `searchtreeid`        BIGINT(20) NOT NULL,
  `id`                  BIGINT(20) NOT NULL,
  `parentid`            BIGINT(20)   DEFAULT NULL,
  `description`         VARCHAR(512) DEFAULT NULL,
  KEY `commercial_vehicle_trees_idx01` (`commercialvehicleid`),
  KEY `commercial_vehicle_trees_idx02` (`id`),
  KEY `commercial_vehicle_trees_idx03` (`parentid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `commercial_vehicles` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `modelid`                  BIGINT(20)   DEFAULT NULL,
  KEY `commercial_vehicles_idx01` (`id`),
  KEY `commercial_vehicles_idx02` (`modelid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `countries` (
  `countrycode`  VARCHAR(512) DEFAULT NULL,
  `currencycode` VARCHAR(512) DEFAULT NULL,
  `description`  VARCHAR(512) DEFAULT NULL,
  `isgroup`      VARCHAR(512) DEFAULT NULL,
  `isocode2`     VARCHAR(512) DEFAULT NULL,
  `isocode3`     VARCHAR(512) DEFAULT NULL,
  `isocodeno`    VARCHAR(512) DEFAULT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `country_groups` (
  `countrycode`  VARCHAR(512) DEFAULT NULL,
  `currencycode` VARCHAR(512) DEFAULT NULL,
  `description`  VARCHAR(512) DEFAULT NULL,
  `isgroup`      VARCHAR(512) DEFAULT NULL,
  `isocode2`     VARCHAR(512) DEFAULT NULL,
  `isocode3`     VARCHAR(512) DEFAULT NULL,
  `isocodeno`    VARCHAR(512) DEFAULT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engine_attributes` (
  `engineid`       BIGINT(20) NOT NULL,
  `attributegroup` VARCHAR(512)  DEFAULT NULL,
  `attributetype`  VARCHAR(512)  DEFAULT NULL,
  `displaytitle`   VARCHAR(512)  DEFAULT NULL,
  `displayvalue`   VARCHAR(2048) DEFAULT NULL,
  KEY `engine_attributes_idx01` (`engineid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engine_pds` (
  `engineid`   BIGINT(20) NOT NULL,
  `nodeid`     BIGINT(20) NOT NULL,
  `productid`  BIGINT(20) NOT NULL,
  `supplierid` BIGINT(20) NOT NULL,
  KEY `engine_pds_idx01` (`engineid`),
  KEY `engine_pds_idx02` (`nodeid`),
  KEY `engine_pds_idx03` (`productid`),
  KEY `engine_pds_idx04` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engine_prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `engine_prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engine_qsi` (
  `engineid`       BIGINT(20) NOT NULL,
  `description`    VARCHAR(512) DEFAULT NULL,
  `quickstarttype` VARCHAR(512) DEFAULT NULL,
  `validstate`     VARCHAR(512) DEFAULT NULL,
  KEY `engine_qsi_idx01` (`engineid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engine_trees` (
  `engineid`     BIGINT(20) NOT NULL,
  `searchtreeid` BIGINT(20) NOT NULL,
  `id`           BIGINT(20) NOT NULL,
  `parentid`     BIGINT(20)   DEFAULT NULL,
  `description`  VARCHAR(512) DEFAULT NULL,
  KEY `engine_trees_idx01` (`engineid`),
  KEY `engine_trees_idx02` (`id`),
  KEY `engine_trees_idx03` (`parentid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `engines` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `haslinkitem`              VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `manufacturerid`           BIGINT(20)   DEFAULT NULL,
  `salesdescription`         VARCHAR(512) DEFAULT NULL,
  KEY `engines_idx01` (`id`),
  KEY `engines_idx02` (`manufacturerid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `languages` (
  `id`          BIGINT(20) NOT NULL,
  `codepage`    VARCHAR(512) DEFAULT NULL,
  `description` VARCHAR(512) DEFAULT NULL,
  `isocode2`    VARCHAR(512) DEFAULT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `manufacturers` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `isvgl`                    VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `matchcode`                VARCHAR(512) DEFAULT NULL,
  KEY `manufacturers_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `models` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `manufacturerid`           BIGINT(20)   DEFAULT NULL,
  KEY `models_idx01` (`id`),
  KEY `models_idx02` (`manufacturerid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbike_attributes` (
  `motorbikeid`    BIGINT(20) NOT NULL,
  `attributegroup` VARCHAR(512)  DEFAULT NULL,
  `attributetype`  VARCHAR(512)  DEFAULT NULL,
  `displaytitle`   VARCHAR(512)  DEFAULT NULL,
  `displayvalue`   VARCHAR(2048) DEFAULT NULL,
  KEY `motorbike_attributes_idx01` (`motorbikeid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbike_pds` (
  `motorbikeid` BIGINT(20) NOT NULL,
  `nodeid`      BIGINT(20) NOT NULL,
  `productid`   BIGINT(20) NOT NULL,
  `supplierid`  BIGINT(20) NOT NULL,
  KEY `motorbike_pds_idx01` (`motorbikeid`),
  KEY `motorbike_pds_idx02` (`nodeid`),
  KEY `motorbike_pds_idx03` (`productid`),
  KEY `motorbike_pds_idx04` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbike_prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `motorbike_prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbike_qsi` (
  `motorbikeid`    BIGINT(20) NOT NULL,
  `description`    VARCHAR(512) DEFAULT NULL,
  `quickstarttype` VARCHAR(512) DEFAULT NULL,
  `validstate`     VARCHAR(512) DEFAULT NULL,
  KEY `motorbike_qsi_idx01` (`motorbikeid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbike_trees` (
  `motorbikeid`  BIGINT(20) NOT NULL,
  `searchtreeid` BIGINT(20) NOT NULL,
  `id`           BIGINT(20) NOT NULL,
  `parentid`     BIGINT(20)   DEFAULT NULL,
  `description`  VARCHAR(512) DEFAULT NULL,
  KEY `motorbike_trees_idx01` (`motorbikeid`),
  KEY `motorbike_trees_idx02` (`id`),
  KEY `motorbike_trees_idx03` (`parentid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `motorbikes` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `modelid`                  BIGINT(20)   DEFAULT NULL,
  KEY `motorbikes_idx01` (`id`),
  KEY `motorbikes_idx02` (`modelid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_attributes` (
  `passangercarid` BIGINT(20) NOT NULL,
  `attributegroup` VARCHAR(512)  DEFAULT NULL,
  `attributetype`  VARCHAR(512)  DEFAULT NULL,
  `displaytitle`   VARCHAR(512)  DEFAULT NULL,
  `displayvalue`   VARCHAR(2048) DEFAULT NULL,
  KEY `passanger_car_attributes_idx01` (`passangercarid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_engines` (
  `id`       BIGINT(20) NOT NULL,
  `engineid` BIGINT(20) NOT NULL,
  KEY `passanger_car_engines_idx01` (`id`),
  KEY `passanger_car_engines_idx02` (`engineid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_pds` (
  `passangercarid` BIGINT(20) NOT NULL,
  `nodeid`         BIGINT(20) NOT NULL,
  `productid`      BIGINT(20) NOT NULL,
  `supplierid`     BIGINT(20) NOT NULL,
  KEY `passanger_car_pds_idx01` (`passangercarid`),
  KEY `passanger_car_pds_idx02` (`nodeid`),
  KEY `passanger_car_pds_idx03` (`productid`),
  KEY `passanger_car_pds_idx04` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `passanger_car_prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_qsi` (
  `passangercarid` BIGINT(20) NOT NULL,
  `description`    VARCHAR(512) DEFAULT NULL,
  `quickstarttype` VARCHAR(512) DEFAULT NULL,
  `validstate`     VARCHAR(512) DEFAULT NULL,
  KEY `passanger_car_qsi_idx01` (`passangercarid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_car_trees` (
  `passangercarid` BIGINT(20) NOT NULL,
  `searchtreeid`   BIGINT(20) NOT NULL,
  `id`             BIGINT(20) NOT NULL,
  `parentid`       BIGINT(20)   DEFAULT NULL,
  `description`    VARCHAR(512) DEFAULT NULL,
  KEY `passanger_car_trees_idx01` (`passangercarid`),
  KEY `passanger_car_trees_idx02` (`id`),
  KEY `passanger_car_trees_idx03` (`parentid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `passanger_cars` (
  `id`                       BIGINT(20) NOT NULL,
  `canbedisplayed`           VARCHAR(512) DEFAULT NULL,
  `constructioninterval`     VARCHAR(512) DEFAULT NULL,
  `description`              VARCHAR(512) DEFAULT NULL,
  `fulldescription`          VARCHAR(512) DEFAULT NULL,
  `haslink`                  VARCHAR(512) DEFAULT NULL,
  `isaxle`                   VARCHAR(512) DEFAULT NULL,
  `iscommercialvehicle`      VARCHAR(512) DEFAULT NULL,
  `iscvmanufacturerid`       VARCHAR(512) DEFAULT NULL,
  `isengine`                 VARCHAR(512) DEFAULT NULL,
  `ismotorbike`              VARCHAR(512) DEFAULT NULL,
  `ispassengercar`           VARCHAR(512) DEFAULT NULL,
  `istransporter`            VARCHAR(512) DEFAULT NULL,
  `isvalidforcurrentcountry` VARCHAR(512) DEFAULT NULL,
  `linkitemtype`             VARCHAR(512) DEFAULT NULL,
  `modelid`                  BIGINT(20)   DEFAULT NULL,
  KEY `passanger_cars_idx01` (`id`),
  KEY `passanger_cars_idx02` (`modelid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `prd` (
  `id`                       BIGINT(20)   NOT NULL,
  `assemblygroupdescription` VARCHAR(256) NOT NULL,
  `description`              VARCHAR(256) NOT NULL,
  `normalizeddescription`    VARCHAR(256) NOT NULL,
  `usagedescription`         VARCHAR(256) NOT NULL,
  KEY `prd_idx01` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `supplier_details` (
  `supplierid`           BIGINT(20) NOT NULL,
  `addresstype`          VARCHAR(512) DEFAULT NULL,
  `addresstypeid`        VARCHAR(512) DEFAULT NULL,
  `city1`                VARCHAR(512) DEFAULT NULL,
  `city2`                VARCHAR(512) DEFAULT NULL,
  `countrycode`          VARCHAR(512) DEFAULT NULL,
  `email`                VARCHAR(512) DEFAULT NULL,
  `fax`                  VARCHAR(512) DEFAULT NULL,
  `homepage`             VARCHAR(512) DEFAULT NULL,
  `name1`                VARCHAR(512) DEFAULT NULL,
  `name2`                VARCHAR(512) DEFAULT NULL,
  `postalcodecity`       VARCHAR(512) DEFAULT NULL,
  `postalcodepob`        VARCHAR(512) DEFAULT NULL,
  `postalcodewholesaler` VARCHAR(512) DEFAULT NULL,
  `postalcountrycode`    VARCHAR(512) DEFAULT NULL,
  `postofficebox`        VARCHAR(512) DEFAULT NULL,
  `street1`              VARCHAR(512) DEFAULT NULL,
  `street2`              VARCHAR(512) DEFAULT NULL,
  `telephone`            VARCHAR(512) DEFAULT NULL,
  KEY `supplier_details_idx01` (`supplierid`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `suppliers` (
  `id`                    BIGINT(20) NOT NULL,
  `dataversion`           VARCHAR(512) DEFAULT NULL,
  `description`           VARCHAR(512) DEFAULT NULL,
  `matchcode`             VARCHAR(512) DEFAULT NULL,
  `nbrofarticles`         VARCHAR(512) DEFAULT NULL,
  `hasnewversionarticles` VARCHAR(512) DEFAULT NULL,
  KEY `suppliers_idx01` (`id`),
  KEY `suppliers_idx02` (`description`(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `suppliers_with_nv_articles` (
  `id`                    BIGINT(20) NOT NULL,
  `dataversion`           VARCHAR(512) DEFAULT NULL,
  `description`           VARCHAR(512) DEFAULT NULL,
  `matchcode`             VARCHAR(512) DEFAULT NULL,
  `nbrofarticles`         VARCHAR(512) DEFAULT NULL,
  `hasnewversionarticles` VARCHAR(512) DEFAULT NULL,
  KEY `suppliers_with_nv_articles_idx01` (`id`),
  KEY `suppliers_with_nv_articles_idx02` (`description`(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
CREATE TABLE `suppliers_with_nv_linkages` (
  `id`                    BIGINT(20) NOT NULL,
  `dataversion`           VARCHAR(512) DEFAULT NULL,
  `description`           VARCHAR(512) DEFAULT NULL,
  `matchcode`             VARCHAR(512) DEFAULT NULL,
  `nbrofarticles`         VARCHAR(512) DEFAULT NULL,
  `hasnewversionarticles` VARCHAR(512) DEFAULT NULL,
  KEY `suppliers_with_nv_linkages_idx01` (`id`),
  KEY `suppliers_with_nv_linkages_idx02` (`description`(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
