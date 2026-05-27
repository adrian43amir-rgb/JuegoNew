-- ==========================================
-- TABLA DE SISTEMA DE COMBATE
-- ==========================================

-- Tabla de Habilidades de Combate
CREATE TABLE CombatAbilities (
    AbilityID INT PRIMARY KEY,
    AbilityName VARCHAR(100) NOT NULL,
    Description VARCHAR(300),
    AbilityType VARCHAR(50),          -- 'Attack', 'Magic', 'Defense', 'Heal', 'Support'
    BaseClassID INT FOREIGN KEY REFERENCES BaseClasses(ClassID),
    RequiredLevel INT DEFAULT 1,
    ManaCost INT DEFAULT 0,
    CooldownSeconds INT DEFAULT 0,
    DamageMultiplier DECIMAL(3,2) DEFAULT 1.0,
    AccuracyRate DECIMAL(5,2) DEFAULT 100.0,  -- Porcentaje de precisión
    CriticalChance DECIMAL(5,2) DEFAULT 0.0   -- Porcentaje de crítico
);

-- Tabla de Batallas/Encuentros
CREATE TABLE Battles (
    BattleID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    MonsterID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Monsters(MonsterID),
    MapID INT FOREIGN KEY REFERENCES Maps(MapID),
    BattleStartTime DATETIME DEFAULT GETDATE(),
    BattleEndTime DATETIME,
    BattleResult VARCHAR(20),         -- 'Victory', 'Defeat', 'Fled'
    PlayerDamageTaken INT DEFAULT 0,
    MonsterDamageTaken INT DEFAULT 0,
    ExperienceGained INT DEFAULT 0,
    GoldGained INT DEFAULT 0
);

-- Tabla de Turnos de Combate
CREATE TABLE BattleTurns (
    TurnID UNIQUEIDENTIFIER PRIMARY KEY,
    BattleID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Battles(BattleID),
    TurnNumber INT NOT NULL,
    ActorType VARCHAR(20),            -- 'Player' or 'Monster'
    ActionType VARCHAR(50),           -- 'Attack', 'UseAbility', 'UseItem', 'Defend', 'Flee'
    ActionValue INT,                  -- ID de habilidad o item
    DamageDealt INT,
    HealingApplied INT,
    TurnResult VARCHAR(100),
    TurnTimestamp DATETIME DEFAULT GETDATE()
);

-- Tabla de Historial de Combates del Jugador
CREATE TABLE PlayerBattleHistory (
    HistoryID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    TotalBattles INT DEFAULT 0,
    TotalVictories INT DEFAULT 0,
    TotalDefeats INT DEFAULT 0,
    TotalFlees INT DEFAULT 0,
    WinRate DECIMAL(5,2) DEFAULT 0.0,
    LastBattleDate DATETIME,
    ConsecutiveVictories INT DEFAULT 0
);

-- Tabla de Estados de Combate (buffs/debuffs)
CREATE TABLE CombatStatuses (
    StatusID INT PRIMARY KEY,
    StatusName VARCHAR(100) NOT NULL,
    Description VARCHAR(300),
    StatusType VARCHAR(50),           -- 'Buff', 'Debuff', 'Condition'
    DurationTurns INT DEFAULT 1,
    EffectATK INT DEFAULT 0,
    EffectDEF INT DEFAULT 0,
    EffectMAG INT DEFAULT 0,
    EffectSPD INT DEFAULT 0,
    DamagePerTurn INT DEFAULT 0,      -- Para estados de daño continuado
    IsRemovable BIT DEFAULT 1
);

-- Tabla de Aplicación de Estados en Combate
CREATE TABLE ActiveCombatStatuses (
    ActiveStatusID UNIQUEIDENTIFIER PRIMARY KEY,
    BattleID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Battles(BattleID),
    StatusID INT FOREIGN KEY REFERENCES CombatStatuses(StatusID),
    AffectedType VARCHAR(20),         -- 'Player' or 'Monster'
    TurnsRemaining INT,
    AppliedTurn INT,
    IsActive BIT DEFAULT 1
);

-- ==========================================
-- TABLA DE INVENTARIO Y EQUIPO
-- ==========================================

-- Tabla de Inventario del Jugador
CREATE TABLE PlayerInventory (
    InventoryID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    ItemID INT FOREIGN KEY REFERENCES Items(ItemID),
    Quantity INT DEFAULT 1,
    IsEquipped BIT DEFAULT 0,
    EquipSlot VARCHAR(50),            -- 'Head', 'Chest', 'Legs', 'Feet', 'MainHand', 'OffHand', 'Accessory'
    AcquiredDate DATETIME DEFAULT GETDATE()
);

-- Tabla de Equipos
CREATE TABLE Equipment (
    EquipmentID INT PRIMARY KEY,
    EquipmentName VARCHAR(100) NOT NULL,
    EquipmentType VARCHAR(50),        -- 'Weapon', 'Armor', 'Accessory'
    EquipSlot VARCHAR(50) NOT NULL,
    BaseItemID INT FOREIGN KEY REFERENCES Items(ItemID),
    BonusATK INT DEFAULT 0,
    BonusDEF INT DEFAULT 0,
    BonusMAG INT DEFAULT 0,
    BonusSPD INT DEFAULT 0,
    RequiredLevel INT DEFAULT 1,
    RequiredClass INT FOREIGN KEY REFERENCES BaseClasses(ClassID),
    Rarity VARCHAR(50),               -- 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'
    SellValue INT
);

-- Tabla de Equipamiento Actual del Jugador
CREATE TABLE PlayerEquipment (
    EquipmentSlotID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    EquipmentID INT FOREIGN KEY REFERENCES Equipment(EquipmentID),
    EquipSlot VARCHAR(50) NOT NULL,
    EquippedDate DATETIME DEFAULT GETDATE()
);

-- Tabla de Banca/Almacén
CREATE TABLE PlayerBank (
    BankID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    ItemID INT FOREIGN KEY REFERENCES Items(ItemID),
    Quantity INT DEFAULT 1,
    StoredDate DATETIME DEFAULT GETDATE()
);

-- ==========================================
-- TABLA DE SISTEMA DE PROGRESIÓN
-- ==========================================

-- Tabla de Habilidades del Jugador
CREATE TABLE PlayerSkills (
    SkillID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    AbilityID INT FOREIGN KEY REFERENCES CombatAbilities(AbilityID),
    SkillLevel INT DEFAULT 1,
    SkillExperience INT DEFAULT 0,
    LastUsedDate DATETIME,
    TimesUsed INT DEFAULT 0
);

-- Tabla de Atributos del Jugador
CREATE TABLE PlayerAttributes (
    AttributeID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    Vitality INT DEFAULT 10,          -- Aumenta HP
    Strength INT DEFAULT 10,          -- Aumenta ATK
    Agility INT DEFAULT 10,           -- Aumenta SPD y Evasión
    Spirit INT DEFAULT 10,            -- Aumenta MAG y Defensa Mágica
    LastUpdated DATETIME DEFAULT GETDATE()
);

-- Tabla de Logros/Achievements
CREATE TABLE Achievements (
    AchievementID INT PRIMARY KEY,
    AchievementName VARCHAR(100) NOT NULL,
    Description VARCHAR(300),
    AchievementType VARCHAR(50),      -- 'Combat', 'Exploration', 'Collection', 'Social'
    RewardXP INT DEFAULT 0,
    RewardGold INT DEFAULT 0,
    IconPath VARCHAR(200)
);

-- Tabla de Logros Desbloqueados del Jugador
CREATE TABLE PlayerAchievements (
    PlayerAchievementID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    AchievementID INT FOREIGN KEY REFERENCES Achievements(AchievementID),
    UnlockedDate DATETIME DEFAULT GETDATE(),
    Progress INT DEFAULT 0            -- Para logros con progreso
);

-- Tabla de Misiones
CREATE TABLE Quests (
    QuestID INT PRIMARY KEY,
    QuestName VARCHAR(100) NOT NULL,
    Description VARCHAR(500),
    QuestType VARCHAR(50),            -- 'Main', 'Side', 'Daily', 'Weekly'
    RecommendedLevel INT DEFAULT 1,
    RewardXP INT DEFAULT 0,
    RewardGold INT DEFAULT 0,
    RequiredLevel INT DEFAULT 1
);

-- Tabla de Misiones Activas del Jugador
CREATE TABLE PlayerQuests (
    PlayerQuestID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    QuestID INT FOREIGN KEY REFERENCES Quests(QuestID),
    AcceptedDate DATETIME DEFAULT GETDATE(),
    CompletedDate DATETIME,
    QuestStatus VARCHAR(50),          -- 'Accepted', 'InProgress', 'Completed', 'Failed'
    ProgressValue INT DEFAULT 0
);

-- ==========================================
-- TABLA DE NPCs Y DIÁLOGOS
-- ==========================================

-- Tabla de NPCs
CREATE TABLE NPCs (
    NPCID UNIQUEIDENTIFIER PRIMARY KEY,
    NPCName VARCHAR(100) NOT NULL,
    Description VARCHAR(300),
    MapID INT FOREIGN KEY REFERENCES Maps(MapID),
    LocationID INT FOREIGN KEY REFERENCES MapLocations(LocationID),
    NPCType VARCHAR(50),              -- 'Merchant', 'Quest Giver', 'Trainer', 'Healer', 'Guard'
    Level INT DEFAULT 1,
    CoordinateX INT,
    CoordinateY INT
);

-- Tabla de Diálogos
CREATE TABLE Dialogues (
    DialogueID UNIQUEIDENTIFIER PRIMARY KEY,
    NPCID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES NPCs(NPCID),
    DialogueText VARCHAR(500) NOT NULL,
    DialogueType VARCHAR(50),         -- 'greeting', 'quest', 'trade', 'story'
    NextDialogueID UNIQUEIDENTIFIER,
    RequiredQuestID INT FOREIGN KEY REFERENCES Quests(QuestID),
    RequiredLevel INT DEFAULT 1
);

-- Tabla de Tiendas NPC
CREATE TABLE NPCShops (
    ShopID UNIQUEIDENTIFIER PRIMARY KEY,
    NPCID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES NPCs(NPCID),
    ShopName VARCHAR(100),
    ShopDescription VARCHAR(300),
    ShopType VARCHAR(50)              -- 'General', 'Weapons', 'Armor', 'Potions'
);

-- Tabla de Inventario de Tienda
CREATE TABLE ShopInventory (
    ShopInventoryID UNIQUEIDENTIFIER PRIMARY KEY,
    ShopID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES NPCShops(ShopID),
    ItemID INT FOREIGN KEY REFERENCES Items(ItemID),
    Quantity INT DEFAULT 999,
    PriceMultiplier DECIMAL(3,2) DEFAULT 1.0
);

-- Tabla de Historial de Compras
CREATE TABLE PurchaseHistory (
    PurchaseID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    NPCID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES NPCs(NPCID),
    ItemID INT FOREIGN KEY REFERENCES Items(ItemID),
    Quantity INT,
    TotalPrice INT,
    PurchaseDate DATETIME DEFAULT GETDATE(),
    TransactionType VARCHAR(20)       -- 'Buy', 'Sell'
);

-- ==========================================
-- TABLA DE GUARDADO DE PROGRESO
-- ==========================================

-- Tabla de Puntos de Guardado
CREATE TABLE SavePoints (
    SavePointID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    SaveName VARCHAR(100),
    MapID INT FOREIGN KEY REFERENCES Maps(MapID),
    LocationID INT FOREIGN KEY REFERENCES MapLocations(LocationID),
    CoordinateX INT,
    CoordinateY INT,
    CurrentHP INT,
    CurrentMP INT,
    SaveDate DATETIME DEFAULT GETDATE(),
    PlayTimeSeconds INT DEFAULT 0,
    IsAutosave BIT DEFAULT 0
);

-- Tabla de Estadísticas de Sesión
CREATE TABLE SessionStatistics (
    SessionID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    SessionStartTime DATETIME DEFAULT GETDATE(),
    SessionEndTime DATETIME,
    TotalPlayTimeSeconds INT DEFAULT 0,
    MonstersDefeated INT DEFAULT 0,
    ExperienceGained INT DEFAULT 0,
    GoldEarned INT DEFAULT 0,
    ItemsCollected INT DEFAULT 0,
    QuestsCompleted INT DEFAULT 0
);

-- Tabla de Progreso General del Juego
CREATE TABLE GameProgress (
    ProgressID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    LastSaveDate DATETIME DEFAULT GETDATE(),
    TotalPlayTime INT DEFAULT 0,      -- En segundos
    MapExplorationPercentage DECIMAL(5,2) DEFAULT 0.0,
    CompletionPercentage DECIMAL(5,2) DEFAULT 0.0,
    AchievementPercentage DECIMAL(5,2) DEFAULT 0.0
);

-- ==========================================
-- TABLA DE INTERFAZ DE USUARIO (HUD)
-- ==========================================

-- Tabla de Configuración de Interfaz
CREATE TABLE UISettings (
    UISettingID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    UIScale DECIMAL(3,2) DEFAULT 1.0,
    BrightnessSetting DECIMAL(3,2) DEFAULT 1.0,
    VolumeSetting DECIMAL(3,2) DEFAULT 0.8,
    ShowFPS BIT DEFAULT 0,
    ShowMinimap BIT DEFAULT 1,
    ShowDamageNumbers BIT DEFAULT 1,
    ScreenMode VARCHAR(50),           -- 'Fullscreen', 'Windowed', 'Borderless'
    ResolutionWidth INT DEFAULT 1920,
    ResolutionHeight INT DEFAULT 1080
);

-- Tabla de Hotkeys/Atajos de Teclado
CREATE TABLE KeyBindings (
    KeyBindingID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    ActionName VARCHAR(100) NOT NULL,
    KeyCode VARCHAR(50),              -- 'W', 'A', 'S', 'D', etc.
    IsCustom BIT DEFAULT 0
);

-- Tabla de Notificaciones del HUD
CREATE TABLE HUDNotifications (
    NotificationID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    NotificationType VARCHAR(50),     -- 'Quest', 'Achievement', 'Item', 'Level Up', 'Warning'
    NotificationText VARCHAR(300),
    CreatedDate DATETIME DEFAULT GETDATE(),
    IsRead BIT DEFAULT 0,
    ExpiryDate DATETIME
);

-- Tabla de Mapas Descubiertos (para el mapa del mundo)
CREATE TABLE DiscoveredMaps (
    DiscoveredMapID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    MapID INT FOREIGN KEY REFERENCES Maps(MapID),
    DiscoveryDate DATETIME DEFAULT GETDATE(),
    ExplorationPercentage DECIMAL(5,2) DEFAULT 0.0
);

-- Tabla de Puntos de Interés Descubiertos
CREATE TABLE DiscoveredLocations (
    DiscoveredLocationID UNIQUEIDENTIFIER PRIMARY KEY,
    PlayerID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES Players(PlayerID),
    LocationID INT FOREIGN KEY REFERENCES MapLocations(LocationID),
    DiscoveryDate DATETIME DEFAULT GETDATE()
);
