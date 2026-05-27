-- ==========================================
-- TABLA DE MAPAS
-- ==========================================
CREATE TABLE Maps (
    MapID INT PRIMARY KEY,
    MapName VARCHAR(100) NOT NULL,
    Description VARCHAR(500),
    Width INT NOT NULL,
    Height INT NOT NULL,
    DifficultyLevel INT DEFAULT 1,  -- 1-5: Fácil a Muy Difícil
    RecommendedLevel INT DEFAULT 1,
    IsDiscovered BIT DEFAULT 0      -- 0 = Oculto, 1 = Descubierto
);

-- ==========================================
-- TABLA DE UBICACIONES EN MAPAS
-- ==========================================
CREATE TABLE MapLocations (
    LocationID INT PRIMARY KEY,
    MapID INT NOT NULL FOREIGN KEY REFERENCES Maps(MapID),
    LocationName VARCHAR(100) NOT NULL,
    CoordinateX INT NOT NULL,
    CoordinateY INT NOT NULL,
    Description VARCHAR(300),
    IsNPCLocation BIT DEFAULT 0,
    IsTreasureLocation BIT DEFAULT 0
);

-- ==========================================
-- TABLA DE TIPOS DE MONSTRUOS
-- ==========================================
CREATE TABLE MonsterTypes (
    MonsterTypeID INT PRIMARY KEY,
    MonsterTypeName VARCHAR(100) NOT NULL,
    Description VARCHAR(300),
    ImagePath VARCHAR(200),
    BaseMonsterRarity VARCHAR(50) DEFAULT 'Common'  -- Common, Uncommon, Rare, Epic, Legendary
);

-- ==========================================
-- TABLA DE MONSTRUOS (Instancias)
-- ==========================================
CREATE TABLE Monsters (
    MonsterID UNIQUEIDENTIFIER PRIMARY KEY,
    MonsterTypeID INT NOT NULL FOREIGN KEY REFERENCES MonsterTypes(MonsterTypeID),
    Level INT NOT NULL DEFAULT 1,
    CurrentHP INT NOT NULL,
    MaxHP INT NOT NULL,
    ATK INT NOT NULL,
    DEF INT NOT NULL,
    MAG INT NOT NULL,
    SPD INT NOT NULL,         -- Velocidad
    ExperienceReward INT NOT NULL,
    GoldReward INT NOT NULL,
    CanDrop BIT DEFAULT 1      -- 1 = Puede dropar items
);

-- ==========================================
-- TABLA DE ITEMS DROPEABLES POR MONSTRUOS
-- ==========================================
CREATE TABLE MonsterDrops (
    DropID INT PRIMARY KEY,
    MonsterTypeID INT NOT NULL FOREIGN KEY REFERENCES MonsterTypes(MonsterTypeID),
    ItemID INT NOT NULL FOREIGN KEY REFERENCES Items(ItemID),
    DropChance DECIMAL(5,2) NOT NULL,  -- Porcentaje de probabilidad (0-100)
    MinQuantity INT DEFAULT 1,
    MaxQuantity INT DEFAULT 1
);

-- ==========================================
-- TABLA DE MONSTRUOS EN MAPAS
-- ==========================================
CREATE TABLE MapMonsterSpawns (
    SpawnID INT PRIMARY KEY,
    MapID INT NOT NULL FOREIGN KEY REFERENCES Maps(MapID),
    MonsterTypeID INT NOT NULL FOREIGN KEY REFERENCES MonsterTypes(MonsterTypeID),
    SpawnLocationX INT NOT NULL,
    SpawnLocationY INT NOT NULL,
    SpawnRate DECIMAL(5,2) DEFAULT 50.0,  -- Porcentaje de spawn
    MaxMonsterCount INT DEFAULT 5,
    RespawnTimeSeconds INT DEFAULT 300   -- 5 minutos por defecto
);

-- ==========================================
-- TABLA DE ENCUENTROS ALEATORIOS
-- ==========================================
CREATE TABLE RandomEncounters (
    EncounterID INT PRIMARY KEY,
    MapID INT NOT NULL FOREIGN KEY REFERENCES Maps(MapID),
    MonsterTypeID INT NOT NULL FOREIGN KEY REFERENCES MonsterTypes(MonsterTypeID),
    EncounterChance DECIMAL(5,2) NOT NULL,  -- Porcentaje de probabilidad
    MinMonsterCount INT DEFAULT 1,
    MaxMonsterCount INT DEFAULT 3
);

-- ==========================================
-- TABLA DE EVENTOS EN MAPAS (Jefes, NPCs, etc)
-- ==========================================
CREATE TABLE MapEvents (
    EventID INT PRIMARY KEY,
    MapID INT NOT NULL FOREIGN KEY REFERENCES Maps(MapID),
    EventType VARCHAR(50) NOT NULL,  -- 'Boss', 'NPC', 'Treasure', 'Hazard'
    EventName VARCHAR(100) NOT NULL,
    Description VARCHAR(500),
    CoordinateX INT NOT NULL,
    CoordinateY INT NOT NULL,
    IsActive BIT DEFAULT 1,
    RequiredLevel INT DEFAULT 1
);

-- ==========================================
-- TABLA DE JEFES ESPECIALES
-- ==========================================
CREATE TABLE BossMonsters (
    BossID UNIQUEIDENTIFIER PRIMARY KEY,
    MonsterID UNIQUEIDENTIFIER NOT NULL FOREIGN KEY REFERENCES Monsters(MonsterID),
    BossName VARCHAR(100) NOT NULL,
    BossDescription VARCHAR(500),
    MapID INT NOT NULL FOREIGN KEY REFERENCES Maps(MapID),
    IsDefeated BIT DEFAULT 0,
    LastDefeatedDate DATETIME,
    ExperienceRewardMultiplier DECIMAL(3,2) DEFAULT 2.0,
    GoldRewardMultiplier DECIMAL(3,2) DEFAULT 2.0
);
