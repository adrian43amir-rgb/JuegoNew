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