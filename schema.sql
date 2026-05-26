-- Tabla de Clases Base y Estadísticas Iniciales
CREATE TABLE BaseClasses (
    ClassID INT PRIMARY KEY,
    ClassName VARCHAR(50) NOT NULL,
    BaseHP INT NOT NULL,
    BaseMP INT DEFAULT 0,
    BaseATK INT NOT NULL,
    BaseDEF INT NOT NULL,
    BaseMAG INT NOT NULL
);

-- Tabla de Jugadores
CREATE TABLE Players (
    PlayerID UNIQUEIDENTIFIER PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    ClassID INT FOREIGN KEY REFERENCES BaseClasses(ClassID),
    CurrentLevel INT DEFAULT 1,
    CurrentXP INT DEFAULT 0,
    GoldRyos INT DEFAULT 0,
    AvailableAttributePoints INT DEFAULT 0,
    HasUsedInkPurification BIT DEFAULT 0 -- 0 = Falso, 1 = Verdadero
);

-- Tabla de Economía e Inventario Básico
CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    ItemType VARCHAR(50) NOT NULL,
    CostRyos INT NOT NULL,
    IsSoulbound BIT DEFAULT 0
);

-- Tabla de Evoluciones de Clases
CREATE TABLE ClassEvolutions (
    EvolutionID INT PRIMARY KEY,
    BaseClassID INT NOT NULL FOREIGN KEY REFERENCES BaseClasses(ClassID),
    EvolutionName VARCHAR(50) NOT NULL,
    BonusHP INT DEFAULT 0,
    BonusATK INT DEFAULT 0,
    BonusDEF INT DEFAULT 0,
    BonusMAG INT DEFAULT 0,
    HP_MultPerVit DECIMAL(3,2) DEFAULT 10.00,
    ATK_MultPerStr DECIMAL(3,2) DEFAULT 2.00,
    ATK_MultPerAgi DECIMAL(3,2) DEFAULT 1.00,
    DEF_MultPerAgi DECIMAL(3,2) DEFAULT 0.50,
    MAG_MultPerSpr DECIMAL(3,2) DEFAULT 2.00
);