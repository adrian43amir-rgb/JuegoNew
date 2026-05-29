CREATE TABLE ClassClasses (
    ClassID INT PRIMARY KEY,
    ClassName VARCHAR(50) UNIQUE NOT NULL,
    BaseHP INT NOT NULL,
    BaseATK INT NOT NULL,
    BaseDEF INT NOT NULL,
    BaseMAG INT NOT NULL
);

CREATE TABLE Players (
    PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlayerName VARCHAR(50) NOT NULL,
    ClassID INT NOT NULL,
    FOREIGN KEY (ClassID) REFERENCES ClassClasses(ClassID)
);

CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    ItemType VARCHAR(20) NOT NULL,
    CostRyos INT NOT NULL,
    IsSoulbound INT DEFAULT 0,
    BaseClassID INT,
    EvolutionID INT,
    FOREIGN KEY (BaseClassID) REFERENCES ClassClasses(ClassID),
    FOREIGN KEY (EvolutionID) REFERENCES Items(ItemID)
);
