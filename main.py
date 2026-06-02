import sqlite3
import random
import sys
import time

DB = "juego.db"

# === CONFIGURACIÓN DE HABILIDADES POR CLASE ===
# 1: Guerrero, 2: Mago, 3: Arquero
SKILLS_CONFIG = {
    1: {
        "1": {"nombre": "Espadazo Feroz", "coste_mana": 0, "cooldown": 0, "multiplicador": 1.0},
        "2": {"nombre": "Corte de Acero", "coste_mana": 10, "cooldown": 5, "multiplicador": 1.6},
        "3": {"nombre": "Furia del Dragón", "coste_mana": 30, "cooldown": 15, "multiplicador": 2.5}
    },
    2: {
        "1": {"nombre": "Chispa Mágica", "coste_mana": 0, "cooldown": 0, "multiplicador": 0.8},
        "2": {"nombre": "Orbe de Fuego", "coste_mana": 15, "cooldown": 4, "multiplicador": 1.9},
        "3": {"nombre": "Juicio del Trueno", "coste_mana": 45, "cooldown": 20, "multiplicador": 3.4}
    },
    3: {
        "1": {"nombre": "Tiro Rápido", "coste_mana": 0, "cooldown": 0, "multiplicador": 0.9},
        "2": {"nombre": "Flecha Perforante", "coste_mana": 12, "cooldown": 6, "multiplicador": 1.7},
        "3": {"nombre": "Lluvia Astral", "coste_mana": 35, "cooldown": 18, "multiplicador": 2.8}
    }
}

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    try:
        # === TABLAS BASE ===
        c.execute("""CREATE TABLE IF NOT EXISTS Players(
            PlayerID INTEGER PRIMARY KEY, 
            Name TEXT, 
            ClassID INTEGER,
            HP INTEGER, 
            MaxHP INTEGER,
            Mana INTEGER DEFAULT 30,
            MaxMana INTEGER DEFAULT 30,
            Ryos INTEGER, 
            ATK INTEGER, 
            DEF INTEGER, 
            MAG INTEGER, 
            Level INTEGER, 
            XP INTEGER,
            CurrentZone INTEGER DEFAULT 1, 
            MaxZone INTEGER DEFAULT 1,
            EquipWeapon INTEGER DEFAULT NULL,
            EquipArmor INTEGER DEFAULT NULL,
            CritRate INTEGER DEFAULT 5,
            CritDmg REAL DEFAULT 1.5,
            STR INTEGER DEFAULT 10,
            AGI INTEGER DEFAULT 10,
            DEX INTEGER DEFAULT 10,
            Accuracy INTEGER DEFAULT 80,
            Evasion INTEGER DEFAULT 5,
            FOREIGN KEY(ClassID) REFERENCES Classes(ClassID) ON DELETE RESTRICT
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS PlayerCooldowns(
            PlayerID INTEGER,
            SkillName TEXT,
            LastUsedAt REAL DEFAULT 0,
            PRIMARY KEY(PlayerID, SkillName),
            FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS Classes(
            ClassID INTEGER PRIMARY KEY, ClassName TEXT)""")

        c.execute("""CREATE TABLE IF NOT EXISTS Items(
            ItemID INTEGER PRIMARY KEY, ItemName TEXT, ItemType TEXT, Price INTEGER)""")

        c.execute("""CREATE TABLE IF NOT EXISTS Inventory(
            InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayerID INTEGER, ItemID INTEGER, Quantity INTEGER,
            FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
            FOREIGN KEY(ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
            UNIQUE(PlayerID, ItemID)
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS Cities(
            CityID INTEGER PRIMARY KEY, CityName TEXT)""")

        c.execute("""CREATE TABLE IF NOT EXISTS PlayerLocation(
            PlayerID PRIMARY KEY,
            CityID INTEGER,
            FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
            FOREIGN KEY(CityID) REFERENCES Cities(CityID) ON DELETE RESTRICT
        )""")

        # === TABLAS DE ZONAS Y MONSTRUOS ===
        c.execute("""CREATE TABLE IF NOT EXISTS Zones(
            ZoneID INTEGER PRIMARY KEY, ZoneName TEXT, ReqLevel INTEGER,
            RyosMin INTEGER, RyosMax INTEGER, XPMin INTEGER, XPMax INTEGER)""")

        c.execute("""CREATE TABLE IF NOT EXISTS Monsters (
                MonsterID INTEGER PRIMARY KEY,
                Name TEXT,
                ZoneID INTEGER,
                HP INTEGER,
                ATK INTEGER,
                DEF INTEGER,
                STR INTEGER,
                AGI INTEGER,
                DEX INTEGER,
                Accuracy INTEGER,
                Evasion INTEGER,
                CritRate INTEGER,
                CritDmg INTEGER,
                ExpReward INTEGER,
                IsBoss INTEGER
            )""")

        c.execute("""CREATE TABLE IF NOT EXISTS PlayerDrops(
            DropID INTEGER PRIMARY KEY AUTOINCREMENT,
            MonsterID INTEGER, ItemID INTEGER, DropRate INTEGER,
            FOREIGN KEY(MonsterID) REFERENCES Monsters(MonsterID) ON DELETE CASCADE,
            FOREIGN KEY(ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS CraftingRecipes(
            RecipeID INTEGER PRIMARY KEY AUTOINCREMENT,
            ResultItemID INTEGER, ClassID INTEGER,
            Material1ID INTEGER, Qty1 INTEGER,
            Material2ID INTEGER, Qty2 INTEGER,
            Material3ID INTEGER, Qty3 INTEGER,
            SuccessRate INTEGER,
            FOREIGN KEY(ResultItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
            FOREIGN KEY(ClassID) REFERENCES Classes(ClassID) ON DELETE CASCADE
        )""")

        c.execute("CREATE INDEX IF NOT EXISTS idx_inventory_player ON Inventory(PlayerID)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_monsters_zone ON Monsters(ZoneID)")

        # === DATOS BASE ===
        c.execute("INSERT OR IGNORE INTO Classes VALUES (1, 'Guerrero')")
        c.execute("INSERT OR IGNORE INTO Classes VALUES (2, 'Mago')")
        c.execute("INSERT OR IGNORE INTO Classes VALUES (3, 'Arquero')")
        c.execute("INSERT OR IGNORE INTO Cities VALUES (1, 'Villa Amanecer')")
        
        # ZONA 1: BOSQUE AMANECER
        c.execute("INSERT OR IGNORE INTO Zones VALUES (1, 'Bosque Amanecer', 1, 5, 10, 10, 20)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (300, 'Gel Viscoso', 'Material', 5)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (301, 'Colmillo de Lobo', 'Material', 8)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (302, 'Pelaje', 'Material', 6)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (303, 'Daga Oxidada', 'Material', 10)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (304, 'Colmillo del Alfa', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (305, 'Esencia Salvaje', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (400, 'Colmillada del Alfa', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (401, 'Báculo del Alfa', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (402, 'Arco del Alfa', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (31, 'Armadura del Alfa', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (1, 'Slime Verde', 1, 20, 5, 2, 3, 1, 1, 80, 0, 0, 100, 10, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (2, 'Lobo Salvaje', 1, 35, 8, 3, 6, 5, 4, 85, 5, 5, 120, 15, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (3, 'Goblin Ratero', 1, 40, 9, 4, 7, 6, 6, 90, 8, 5, 130, 18, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (4, 'Lobo Alfa', 1, 120, 18, 8, 15, 12, 10, 100, 10, 10, 150, 80, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 1, 300, 60)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 2, 301, 50)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 2, 302, 30)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 3, 303, 20)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 4, 304, 100)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 4, 305, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 400, 1, 304, 1, 305, 1, 300, 10, 80)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 401, 2, 304, 1, 305, 1, 300, 5, 80)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 402, 3, 304, 1, 305, 1, 302, 8, 80)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 31, 1, 304, 1, 305, 1, 302, 5, 80)")

        # ZONA 2: MINAS ABANDONADAS
        c.execute("INSERT OR IGNORE INTO Zones VALUES (2, 'Minas Abandonadas', 6, 15, 25, 30, 50)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (310, 'Fragmento de Hierro', 'Material', 10)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (311, 'Cola de Rata', 'Material', 8)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (312, 'Lingote de Hierro', 'Material', 15)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (313, 'Polvo de Piedra', 'Material', 12)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (314, 'Corona de Hierro', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (315, 'Esencia de Mando', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (420, 'Hacha del Rey Goblin', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (421, 'Báculo de Hierro', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (422, 'Ballesta de Minas', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (32, 'Armadura de Hierro', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (5, 'Rata Gigante', 2, 45, 10, 3, 8, 10, 8, 92, 10, 5, 130, 25, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (6, 'Murciélago Caverna', 2, 40, 11, 4, 7, 15, 12, 95, 15, 8, 140, 28, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (7, 'Goblin Minero', 2, 50, 12, 5, 10, 8, 8, 95, 8, 5, 140, 35, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (8, 'Rey Goblin', 2, 150, 22, 10, 20, 15, 18, 110, 12, 12, 160, 120, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 5, 311, 60)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 6, 310, 50)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 7, 312, 40)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 7, 313, 30)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 8, 314, 100)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 8, 315, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 420, 1, 314, 1, 315, 1, 310, 15, 75)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 421, 2, 314, 1, 315, 1, 313, 10, 75)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 422, 3, 314, 1, 315, 1, 312, 12, 75)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 32, 1, 314, 1, 315, 1, 312, 10, 75)")

        # ZONA 3
        c.execute("INSERT OR IGNORE INTO Zones VALUES (3, 'Pantano Sombrío', 11, 30, 45, 60, 90)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (320, 'Glándula Venenosa', 'Material', 15)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (321, 'Tela Empapada', 'Material', 12)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (322, 'Esencia Corrupta', 'Material', 20)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (323, 'Núcleo Venenoso', 'Material', 18)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (324, 'Raíz Ancestral', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (325, 'Esencia Corrupta Mayor', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (440, 'Lanza del Anciano', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (441, 'Báculo Tóxico', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (442, 'Arco del Pantano', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (33, 'Armadura del Pantano', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (9, 'Rana Venenosa', 3, 60, 13, 4, 11, 14, 12, 100, 12, 5, 140, 45, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (10, 'Zombi Ahogado', 3, 70, 15, 6, 14, 4, 6, 90, 0, 2, 120, 55, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (11, 'Espíritu Pantano', 3, 65, 16, 5, 12, 18, 15, 105, 20, 8, 150, 60, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (12, 'Anciano del Pantano', 3, 180, 25, 12, 22, 10, 20, 115, 15, 15, 170, 180, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 9, 320, 60)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 10, 321, 50)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 11, 322, 40)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 11, 323, 30)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 12, 324, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 12, 325, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 440, 1, 324, 1, 325, 1, 322, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 441, 2, 324, 1, 325, 1, 322, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 442, 3, 324, 1, 325, 1, 322, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 33, 1, 324, 1, 325, 1, 321, 10, 70)")

        # ZONA 4
        c.execute("INSERT OR IGNORE INTO Zones VALUES (4, 'Templo del Fuego', 16, 50, 70, 100, 140)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (330, 'Escama de Fuego', 'Material', 20)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (331, 'Carbón Puro', 'Material', 18)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (332, 'Núcleo de Fuego', 'Material', 25)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (333, 'Brasa Eterna', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (334, 'Esencia de Ifrit', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (450, 'Espadón Ígneo', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (451, 'Cetro de Ifrit', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (452, 'Arco de Llamas', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (34, 'Armadura Ígnea', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (13, 'Esqueleto Ígneo', 4, 80, 18, 6, 16, 12, 15, 105, 10, 10, 150, 80, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (14, 'Salamandra', 4, 75, 20, 7, 18, 20, 18, 110, 15, 12, 160, 85, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (15, 'Golem de Ceniza', 4, 100, 22, 10, 25, 5, 8, 95, 2, 5, 140, 100, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (16, 'Ifrit Menor', 4, 220, 30, 15, 32, 22, 25, 125, 15, 18, 180, 250, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 13, 330, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 14, 331, 60)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 15, 332, 40)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 16, 333, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 16, 334, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 450, 1, 333, 1, 334, 1, 332, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 451, 2, 333, 1, 334, 1, 332, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 452, 3, 333, 1, 334, 1, 332, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 34, 1, 333, 1, 334, 1, 332, 12, 70)")

        # ZONA 5
        c.execute("INSERT OR IGNORE INTO Zones VALUES (5, 'Bosque Helado', 21, 70, 100, 140, 200)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (340, 'Pelaje Polar', 'Material', 25)"); c.execute("INSERT OR IGNORE INTO Items VALUES (341, 'Cristal de Escarcha', 'Material', 22)"); c.execute("INSERT OR IGNORE INTO Items VALUES (342, 'Colmillo de Hielo', 'Material', 28)"); c.execute("INSERT OR IGNORE INTO Items VALUES (343, 'Garras de Yeti', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (344, 'Esencia Glacial', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (460, 'Hacha Glacial', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (461, 'Báculo de Escarcha', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (462, 'Arco Glacial', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (35, 'Armadura Glacial', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (17, 'Lobo de Hielo', 5, 100, 23, 8, 20, 25, 22, 115, 18, 12, 160, 110, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (18, 'Duende Polar', 5, 95, 25, 9, 22, 22, 20, 115, 15, 15, 165, 120, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (19, 'Yeti Joven', 5, 130, 28, 12, 28, 12, 15, 110, 8, 10, 150, 140, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (20, 'Yeti Anciano', 5, 280, 38, 18, 40, 18, 28, 135, 12, 20, 190, 350, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 17, 342, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 18, 340, 60)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 19, 341, 45)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 20, 343, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 20, 344, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 460, 1, 343, 1, 344, 1, 341, 18, 65)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 461, 2, 343, 1, 344, 1, 341, 18, 65)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 462, 3, 343, 1, 344, 1, 341, 18, 65)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 35, 1, 343, 1, 344, 1, 340, 12, 65)")

        # ZONA 6
        c.execute("INSERT OR IGNORE INTO Zones VALUES (6, 'Desierto Carmesí', 26, 100, 140, 200, 280)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (350, 'Aguijón de Escorpión', 'Material', 30)"); c.execute("INSERT OR IGNORE INTO Items VALUES (351, 'Sable Oxidado', 'Material', 28)"); c.execute("INSERT OR IGNORE INTO Items VALUES (352, 'Núcleo de Arena', 'Material', 35)"); c.execute("INSERT OR IGNORE INTO Items VALUES (353, 'Urna del Faraón', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (354, 'Esencia Carmesí', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (470, 'Cimitarra Carmesí', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (471, 'Báculo de Arena', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (472, 'Arco del Desierto', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (36, 'Armadura Carmesí', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (21, 'Escorpión de Arena', 6, 125, 28, 10, 25, 20, 24, 120, 15, 15, 170, 150, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (22, 'Bandido del Desierto', 6, 120, 30, 11, 28, 28, 26, 125, 20, 18, 180, 160, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (23, 'Momia Guardiana', 6, 160, 33, 14, 32, 10, 18, 115, 5, 10, 150, 180, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (24, 'Faraón Maldito', 6, 350, 45, 22, 45, 25, 35, 145, 18, 22, 200, 500, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 21, 350, 55)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 22, 351, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 23, 352, 40)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 24, 353, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 24, 354, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 470, 1, 353, 1, 354, 1, 352, 20, 60)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 471, 2, 353, 1, 354, 1, 352, 20, 60)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 472, 3, 353, 1, 354, 1, 352, 20, 60)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 36, 1, 353, 1, 354, 1, 350, 15, 60)")

        # ZONA 7
        c.execute("INSERT OR IGNORE INTO Zones VALUES (7, 'Montaña del Trueno', 31, 140, 190, 280, 380)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (360, 'Pluma de Arpía', 'Material', 35)"); c.execute("INSERT OR IGNORE INTO Items VALUES (361, 'Fragmento de Roca', 'Material', 32)"); c.execute("INSERT OR IGNORE INTO Items VALUES (362, 'Núcleo de Trueno', 'Material', 40)"); c.execute("INSERT OR IGNORE INTO Items VALUES (363, 'Garra de Wyvern', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (364, 'Esencia del Trueno', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (480, 'Mandoble del Trueno', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (481, 'Báculo del Rayo', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (482, 'Arco del Wyvern', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (37, 'Armadura del Trueno', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (25, 'Arpía', 7, 150, 33, 12, 28, 35, 32, 135, 25, 18, 180, 200, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (26, 'Gólem de Roca', 7, 190, 36, 16, 40, 8, 15, 120, 2, 8, 160, 220, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (27, 'Wyvern Joven', 7, 210, 40, 18, 38, 30, 28, 130, 15, 20, 190, 250, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (28, 'Rey Wyvern', 7, 420, 52, 25, 55, 40, 45, 160, 22, 25, 210, 700, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 25, 360, 55)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 26, 361, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 27, 362, 45)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 28, 363, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 28, 364, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 480, 1, 363, 1, 364, 1, 362, 25, 55)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 481, 2, 363, 1, 364, 1, 362, 25, 55)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 482, 3, 363, 1, 364, 1, 362, 25, 55)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 37, 1, 363, 1, 364, 1, 360, 15, 55)")

        # ZONA 8
        c.execute("INSERT OR IGNORE INTO Zones VALUES (8, 'Catedral Maldita', 36, 190, 250, 380, 500)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (370, 'Espada Rota', 'Material', 40)"); c.execute("INSERT OR IGNORE INTO Items VALUES (371, 'Símbolo Sagrado', 'Material', 38)"); c.execute("INSERT OR IGNORE INTO Items VALUES (372, 'Esencia Fantasmal', 'Material', 45)"); c.execute("INSERT OR IGNORE INTO Items VALUES (373, 'Cáliz Profano', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (374, 'Esencia Oscura', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (490, 'Espada Profana', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (491, 'Báculo Oscuro', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (492, 'Arco Sombrio', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (38, 'Armadura Profana', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (29, 'Caballero Caído', 8, 180, 38, 14, 35, 25, 30, 135, 12, 15, 175, 280, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (30, 'Sacerdote Oscuro', 8, 170, 42, 15, 28, 28, 35, 145, 18, 22, 190, 300, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (31, 'Gárgola Viviente', 8, 230, 45, 20, 45, 20, 25, 130, 10, 18, 185, 320, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (32, 'Sacerdote Caído', 8, 500, 60, 28, 60, 35, 50, 170, 20, 28, 220, 1000, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 29, 370, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 30, 371, 55)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 31, 372, 45)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 32, 373, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 32, 374, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 490, 1, 373, 1, 374, 1, 372, 30, 50)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 491, 2, 373, 1, 374, 1, 372, 30, 50)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 492, 3, 373, 1, 374, 1, 372, 30, 50)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 38, 1, 373, 1, 374, 1, 370, 20, 50)")

        # ZONA 9
        c.execute("INSERT OR IGNORE INTO Zones VALUES (9, 'Abismo Cristalino', 41, 250, 320, 500, 650)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (380, 'Seda de Cristal', 'Material', 45)"); c.execute("INSERT OR IGNORE INTO Items VALUES (381, 'Núcleo Prismático', 'Material', 42)"); c.execute("INSERT OR IGNORE INTO Items VALUES (382, 'Cristal Puro', 'Material', 50)"); c.execute("INSERT OR IGNORE INTO Items VALUES (383, 'Escama de Cristal', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (384, 'Esencia Prismática', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (500, 'Espada de Cristal', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (501, 'Báculo Prismático', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (502, 'Arco de Cristal', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (39, 'Armadura de Cristal', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (33, 'Araña de Cristal', 9, 210, 43, 16, 38, 42, 40, 150, 28, 22, 195, 400, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (34, 'Slime Prismático', 9, 200, 46, 18, 40, 30, 38, 145, 20, 20, 190, 420, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (35, 'Golem de Cristal', 9, 270, 50, 24, 55, 15, 25, 140, 5, 15, 180, 450, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (36, 'Dragón de Cristal', 9, 600, 68, 32, 75, 45, 60, 185, 25, 30, 240, 1500, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 33, 380, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 34, 381, 55)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 35, 382, 40)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 36, 383, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 36, 384, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 500, 1, 383, 1, 384, 1, 382, 35, 45)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 501, 2, 383, 1, 384, 1, 382, 35, 45)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 502, 3, 383, 1, 384, 1, 382, 35, 45)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 39, 1, 383, 1, 384, 1, 382, 20, 45)")

        # ZONA 10
        c.execute("INSERT OR IGNORE INTO Zones VALUES (10, 'Ciudadela del Caos', 46, 320, 400, 650, 800)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (390, 'Cuernos de Demonio', 'Material', 50)"); c.execute("INSERT OR IGNORE INTO Items VALUES (391, 'Placa del Caos', 'Material', 48)"); c.execute("INSERT OR IGNORE INTO Items VALUES (392, 'Corazón Demoníaco', 'Material', 60)"); c.execute("INSERT OR IGNORE INTO Items VALUES (393, 'Corona del Caos', 'Material Boss', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (394, 'Esencia del Caos', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (510, 'Espada del Caos', 'Arma Guerrero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (511, 'Báculo del Caos', 'Arma Mago', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (512, 'Arco del Abismo', 'Arma Arquero', 0)"); c.execute("INSERT OR IGNORE INTO Items VALUES (40, 'Armadura del Caos', 'Armadura', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (37, 'Demonio Menor', 10, 250, 48, 18, 45, 40, 45, 155, 22, 25, 200, 600, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (38, 'Caballero del Caos', 10, 280, 52, 22, 55, 35, 40, 160, 18, 22, 195, 650, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (39, 'Archidemonio', 10, 320, 56, 26, 65, 50, 55, 170, 25, 28, 220, 700, 0)"); c.execute("INSERT OR IGNORE INTO Monsters VALUES (40, 'Señor del Caos', 10, 800, 75, 35, 95, 65, 80, 210, 30, 35, 250, 3000, 1)")
        c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 37, 390, 50)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 38, 391, 55)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 39, 392, 40)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 40, 393, 100)"); c.execute("INSERT OR IGNORE INTO PlayerDrops VALUES (NULL, 40, 394, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 510, 1, 393, 1, 394, 1, 392, 40, 40)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 511, 2, 393, 1, 394, 1, 392, 40, 40)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 512, 3, 393, 1, 394, 1, 392, 40, 40)"); c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 40, 1, 393, 1, 394, 1, 391, 25, 40)")

        conn.commit()
        print("✅ Base de datos inicializada correctamente.")

    except sqlite3.Error as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

def inicializar_stats_forja():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS WeaponStats")
    c.execute("""
        CREATE TABLE IF NOT EXISTS WeaponStats (
            WeaponID INTEGER PRIMARY KEY,
            HP INTEGER DEFAULT 0,
            ATK INTEGER DEFAULT 0,
            DF INTEGER DEFAULT 0,
            MAG INTEGER DEFAULT 0,
            Accuracy INTEGER DEFAULT 0,
            Evasion INTEGER DEFAULT 0,
            CritRate INTEGER DEFAULT 0,
            CritDmg REAL DEFAULT 0.0,
            FOREIGN KEY(WeaponID) REFERENCES Items(ItemID)
        )
    """)
    armas_stats = [
        (400, 20, 15, 5, 0, 0, 0, 0, 0.0), (401, 15, 0, 3, 18, 0, 0, 0, 0.0), (402, 10, 16, 2, 0, 0, 0, 0, 0.0),
        (420, 40, 35, 12, 0, 0, 0, 0, 0.0), (421, 30, 0, 8, 40, 0, 0, 0, 0.0), (422, 25, 36, 6, 0, 0, 0, 0, 0.0),
        (440, 70, 55, 20, 0, 0, 0, 0, 0.0), (441, 55, 0, 15, 60, 0, 0, 0, 0.0), (442, 45, 56, 12, 0, 0, 0, 0, 0.0),
        (450, 110, 75, 30, 0, 5, 3, 0, 0.0), (451, 85, 0, 22, 85, 6, 4, 0, 0.0), (452, 70, 78, 18, 0, 8, 6, 0, 0.0),
        (460, 160, 100, 42, 0, 7, 4, 0, 0.0), (461, 125, 0, 32, 110, 9, 6, 0, 0.0), (462, 100, 104, 25, 0, 11, 9, 0, 0.0),
        (470, 220, 130, 55, 0, 10, 6, 0, 0.0), (471, 175, 0, 42, 145, 12, 8, 0, 0.0), (472, 140, 134, 35, 0, 15, 12, 0, 0.0),
        (480, 300, 165, 70, 0, 12, 8, 5, 0.0), (481, 240, 0, 55, 180, 14, 10, 6, 0.0), (482, 190, 170, 45, 0, 18, 16, 8, 0.0),
        (490, 400, 200, 90, 0, 15, 10, 8, 0.0), (491, 320, 0, 70, 220, 17, 13, 10, 0.0), (492, 250, 205, 58, 0, 22, 20, 12, 0.0),
        (500, 550, 245, 115, 0, 18, 13, 12, 0.0), (501, 440, 0, 90, 270, 20, 16, 14, 0.0), (502, 350, 250, 75, 0, 26, 25, 18, 0.0),
        (510, 750, 300, 150, 50, 22, 16, 15, 0.25), (511, 620, 30, 120, 330, 25, 20, 18, 0.30), (512, 500, 310, 100, 40, 32, 30, 22, 0.35)
    ]
    c.executemany("INSERT OR REPLACE INTO WeaponStats VALUES (?,?,?,?,?,?,?,?,?)", armas_stats)
    conn.commit()
    conn.close()
    print("📢 Base de datos: ¡Estadísticas de armas balanceadas e indexadas!")

def inicializar_stats_armaduras():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS ArmorStats")
    c.execute("""
        CREATE TABLE IF NOT EXISTS ArmorStats (
            ArmorID INTEGER PRIMARY KEY,
            HP INTEGER DEFAULT 0,
            ATK INTEGER DEFAULT 0,
            DF INTEGER DEFAULT 0,
            MAG INTEGER DEFAULT 0,
            Accuracy INTEGER DEFAULT 0,
            Evasion INTEGER DEFAULT 0,
            CritRate INTEGER DEFAULT 0,
            CritDmg REAL DEFAULT 0.0,
            FOREIGN KEY(ArmorID) REFERENCES Items(ItemID)
        )
    """)
    armaduras_stats = [
        (31, 30, 0, 5, 0, 0, 2, 0, 0.0),
        (32, 60, 0, 12, 0, 0, 4, 0, 0.0),
        (33, 100, 0, 22, 0, 0, 6, 0, 0.0),
        (34, 150, 5, 35, 5, 0, 8, 0, 0.0),
        (35, 210, 0, 50, 0, 0, 10, 0, 0.0),
        (36, 280, 8, 68, 0, 5, 12, 2, 0.0),
        (37, 360, 0, 88, 10, 0, 15, 0, 0.0),
        (38, 450, 12, 110, 12, 5, 18, 4, 0.0),
        (39, 560, 0, 135, 0, 8, 22, 0, 0.0),
        (40, 700, 25, 170, 25, 12, 28, 5, 0.20)
    ]
    c.executemany("INSERT OR REPLACE INTO ArmorStats VALUES (?,?,?,?,?,?,?,?,?)", armaduras_stats)
    conn.commit()
    conn.close()
    print("📢 Base de datos: ¡Estadísticas de armaduras añaduras!")

def interfaz_forja_categoria(player_id, tipo_item):
    COLOR_VERDE = "\033[92m"
    COLOR_ROJO = "\033[91m"
    COLOR_RESET = "\033[0m"

    while True:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        c.execute("SELECT ClassID FROM Players WHERE PlayerID = ?", (player_id,))
        clase_jugador = c.fetchone()[0]
        
        # === CORRECCIÓN AQUÍ ===
        filtro_tipo = "Arma %" if tipo_item == "Arma" else "Armadura%"
        
        c.execute("""
            SELECT r.RecipeID, i_res.ItemName, r.ResultItemID, r.SuccessRate,
                   i_m1.ItemName, r.Material1ID, r.Qty1,
                   i_m2.ItemName, r.Material2ID, r.Qty2,
                   i_m3.ItemName, r.Material3ID, r.Qty3
            FROM CraftingRecipes r
            JOIN Items i_res ON r.ResultItemID = i_res.ItemID
            LEFT JOIN Items i_m1 ON r.Material1ID = i_m1.ItemID
            LEFT JOIN Items i_m2 ON r.Material2ID = i_m2.ItemID
            LEFT JOIN Items i_m3 ON r.Material3ID = i_m3.ItemID
            WHERE i_res.ItemType LIKE ? AND r.ClassID = ?
        """, (filtro_tipo, clase_jugador))
        recetas = c.fetchall()
        
        c.execute("SELECT ItemID, Quantity FROM Inventory WHERE PlayerID = ?", (player_id,))
        inv_jugador = dict(c.fetchall())
        conn.close()

        print(f"\n🔨 === SECCIÓN: FORJA DE {tipo_item.upper()}S ===")
        if not recetas:
            print(f"No hay recetas de {tipo_item.lower()}s disponibles para tu clase.")
            break
            
        for i, r in enumerate(recetas):
            _, name_res, _, _, _, m1_id, q1, _, m2_id, q2, _, m3_id, q3 = r
            
            tengo_m1 = inv_jugador.get(m1_id, 0) >= q1 if m1_id else True
            tengo_m2 = inv_jugador.get(m2_id, 0) >= q2 if m2_id else True
            tengo_m3 = inv_jugador.get(m3_id, 0) >= q3 if m3_id else True
            
            color_item = COLOR_VERDE if (tengo_m1 and tengo_m2 and tengo_m3) else COLOR_ROJO
            icono = "⚔️" if tipo_item == "Arma" else "🛡️"
            print(f"{i+1}. {color_item}{icono} {name_res}{COLOR_RESET}")
        
        print("0. Volver")
        sys.stdout.flush()
        
        opc = input(f"\nSelecciona una opción para inspeccionar materiales: ")
        if opc == "0":
            break
            
        if opc.isdigit() and 0 < int(opc) <= len(recetas):
            idx = int(opc) - 1
            r_elegida = recetas[idx]
            rec_id, name_res, id_res, rate, m1_name, m1_id, q1, m2_name, m2_id, q2, m3_name, m3_id, q3 = r_elegida
            
            print(f"\n📋 --- DETALLES DE PRODUCCIÓN: {name_res} ---")
            print(f"Probabilidad de éxito elemental: {rate}%")
            print("Materiales requeridos:")
            
            cant1 = inv_jugador.get(m1_id, 0) if m1_id else 0
            cant2 = inv_jugador.get(m2_id, 0) if m2_id else 0
            cant3 = inv_jugador.get(m3_id, 0) if m3_id else 0
            
            tengo_m1_det = cant1 >= q1 if m1_id else True
            tengo_m2_det = cant2 >= q2 if m2_id else True
            tengo_m3_det = cant3 >= q3 if m3_id else True
            
            if m1_id:
                col = COLOR_VERDE if tengo_m1_det else COLOR_ROJO
                print(f" - {col}{m1_name}: {cant1}/{q1}{COLOR_RESET}")
            if m2_id:
                col = COLOR_VERDE if tengo_m2_det else COLOR_ROJO
                print(f" - {col}{m2_name}: {cant2}/{q2}{COLOR_RESET}")
            if m3_id:
                col = COLOR_VERDE if tengo_m3_det else COLOR_ROJO
                print(f" - {col}{m3_name}: {cant3}/{q3}{COLOR_RESET}")
                
            print("\n1. Intentar fabricar pieza")
            print("0. Volver al listado")
            sys.stdout.flush()
            
            accion = input("¿Qué deseas hacer?: ")
            if accion == "1":
                if tengo_m1_det and tengo_m2_det and tengo_m3_det:
                    conn = sqlite3.connect(DB)
                    c = conn.cursor()
                    
                    if m1_id: c.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE PlayerID = ? AND ItemID = ?", (q1, player_id, m1_id))
                    if m2_id: c.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE PlayerID = ? AND ItemID = ?", (q2, player_id, m2_id))
                    if m3_id: c.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE PlayerID = ? AND ItemID = ?", (q3, player_id, m3_id))
                    c.execute("DELETE FROM Inventory WHERE Quantity <= 0")
                    
                    print(f"\n🔥 Trabajando los elementos en el yunque para {name_res}...")
                    if random.randint(1, 100) <= rate:
                        c.execute("""
                            INSERT INTO Inventory (PlayerID, ItemID, Quantity)
                            VALUES (?, ?, 1)
                            ON CONFLICT(PlayerID, ItemID) DO UPDATE SET Quantity = Quantity + 1
                        """, (player_id, id_res))
                        print(f"✨ ¡ÉXITO! Has obtenido tu recompensa: ¡{name_res}! ✨")
                    else:
                        print("💥 ¡FALLO! Los materiales se destruyeron por un desbalance de temperatura.")
                    
                    conn.commit()
                    conn.close()
                else:
                    print("❌ Recursos insuficientes en tu bolsa de viaje.")
        else:
            print("❌ Selección fuera de rango.")
        sys.stdout.flush()

def visitar_forja(player_id):
    while True:
        print("\n🔨 === EL YUNQUE DE VILLA AMANECER ===")
        print("1. Forjar Armas ⚔️")
        print("2. Forjar Armaduras 🛡️")
        print("0. Volver a la Zona Segura ↩️")
        sys.stdout.flush()
        
        opc = input("¿Qué sección deseas visitar?: ")
        if opc == "1":
            interfaz_forja_categoria(player_id, "Arma")
        elif opc == "2":
            interfaz_forja_categoria(player_id, "Armadura")
        elif opc == "0":
            break
        else:
            print("❌ Opción inválida.")
        sys.stdout.flush()

def obtener_datos_jugador(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT Name, HP, MaxHP, Ryos, ATK, DEF, MAG, Level, XP, CurrentZone, MaxZone, CritRate, CritDmg, Accuracy, Evasion, ClassID, Mana, MaxMana
        FROM Players WHERE PlayerID = ?
    """, (player_id,))
    datos = c.fetchone()
    conn.close()
    return datos

def actualizar_hp_mana_ryos_xp(player_id, hp, mana, ryos, xp):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE Players SET HP =?, Mana =?, Ryos =?, XP =? WHERE PlayerID =?", (hp, mana, ryos, xp, player_id))
    conn.commit()
    conn.close()

def subir_nivel_si_aplica(player_id, xp_actual, level_actual):
    xp_necesaria = 100 * level_actual
    if xp_actual >= xp_necesaria:
        nuevo_level = level_actual + 1
        xp_restante = xp_actual - xp_necesaria
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT ATK, DEF, MAG, MaxHP, MaxMana FROM Players WHERE PlayerID =?", (player_id,))
        atk, df, mag, max_hp, max_mana = c.fetchone()
        
        atk += 2; df += 1; mag += 1; max_hp += 10; max_mana += 5
        
        c.execute("""
            UPDATE Players 
            SET Level =?, XP =?, ATK =?, DEF =?, MAG =?, MaxHP =?, HP =?, MaxMana =?, Mana =?
            WHERE PlayerID =?
        """, (nuevo_level, xp_restante, atk, df, mag, max_hp, max_hp, max_mana, max_mana, player_id))
        conn.commit()
        conn.close()
        
        print(f"\n🎊 ¡SUBISTE A NIVEL {nuevo_level}!")
        print(f"💪 ATK +2 | DEF +1 | MAG +1 | HP +10 | MANÁ +5")
        sys.stdout.flush()
        return True
    return False

def comprobar_cooldown(player_id, skill_name, cooldown_duration):
    if cooldown_duration == 0:
        return True, 0
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT LastUsedAt FROM PlayerCooldowns WHERE PlayerID = ? AND SkillName = ?", (player_id, skill_name))
    res = c.fetchone()
    conn.close()
    if res:
        tiempo_restante = cooldown_duration - (time.time() - res[0])
        if tiempo_restante > 0:
            return False, int(tiempo_restante)
    return True, 0

def registrar_cooldown(player_id, skill_name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO PlayerCooldowns (PlayerID, SkillName, LastUsedAt)
        VALUES (?, ?, ?)
        ON CONFLICT(PlayerID, SkillName) DO UPDATE SET LastUsedAt = EXCLUDED.LastUsedAt
    """, (player_id, skill_name, time.time()))
    conn.commit()
    conn.close()

def obtener_monstruos_zona(zone_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT MonsterID, Name, HP, ATK, DEF, ExpReward, IsBoss, CritRate, CritDmg, Accuracy, Evasion 
        FROM Monsters WHERE ZoneID = ?
    """, (zone_id,))
    mobs = c.fetchall()
    conn.close()
    return random.choice(mobs) if mobs else None

def mostrar_drops_monstruo(monster_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT i.ItemName, d.DropRate FROM PlayerDrops d
        JOIN Items i ON d.ItemID = i.ItemID WHERE d.MonsterID =?
    """, (monster_id,))
    drops = c.fetchall()
    conn.close()
    if drops:
        print("Drops posibles:")
        for nombre, prob in drops:
            print(f" - {nombre}: {prob}%")
    sys.stdout.flush()

def tirar_drop(monster_id, player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT ItemID, DropRate FROM PlayerDrops WHERE MonsterID =?", (monster_id,))
    drops = c.fetchall()
    for item_id, rate in drops:
        if random.randint(1, 100) <= rate:
            c.execute("""
                INSERT INTO Inventory (PlayerID, ItemID, Quantity)
                VALUES (?,?, 1)
                ON CONFLICT(PlayerID, ItemID) DO UPDATE SET Quantity = Quantity + 1
            """, (player_id, item_id))
    conn.commit()
    conn.close()

def ver_inventario(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT i.ItemName, i.ItemType, inv.Quantity, i.Price
        FROM Inventory inv
        JOIN Items i ON inv.ItemID = i.ItemID
        WHERE inv.PlayerID = ? AND inv.Quantity > 0
    """, (player_id,))
    items = c.fetchall()
    conn.close()

    print("\n🎒 === TU INVENTARIO ===")
    if not items:
        print("Tu inventario está vacío.")
    else:
        for nombre, tipo, cant, precio in items:
            print(f"- {nombre} x{cant} ({tipo}) | Valor de venta: {precio} Ryos")
    sys.stdout.flush()

def actualizar_tienda_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    c.execute("INSERT OR IGNORE INTO Items VALUES (100, 'Poción de Supervivencia', 'Consumible', 10)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (101, 'Poción de Maná', 'Consumible', 25)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (110, 'Espada Larga', 'Arma Guerrero', 100)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (111, 'Báculo de Aprendiz', 'Arma Mago', 100)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (112, 'Arco de Caza', 'Arma Arquero', 100)")
    
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (110, 8, 0)")
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (111, 0, 10)")
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (112, 9, 0)")
    
    c.execute("INSERT OR IGNORE INTO Items VALUES (120, 'Espadón de Acero (Nv 10)', 'Arma Guerrero', 500)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (121, 'Báculo de Rubí (Nv 10)', 'Arma Mago', 500)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (122, 'Arco Compuesto (Nv 10)', 'Arma Arquero', 500)")
    
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (120, 25, 0)")
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (121, 0, 30)")
    c.execute("INSERT OR IGNORE INTO WeaponStats (WeaponID, ATK, MAG) VALUES (122, 28, 0)")
    
    conn.commit()
    conn.close()

def visitar_tienda(player_id):
    while True:
        datos = obtener_datos_jugador(player_id)
        nivel, ryos = datos[7], datos[3]

        print(f"\n🏪 === TIENDA DE VILLA AMANECER === (Tus Ryos: {ryos})")
        print("1. Comprar Objetos y Armas")
        print("2. Vender Materiales (Drops)")
        print("0. Salir de la Tienda")
        sys.stdout.flush()
        
        opc = input("Elige una opción: ")
        if opc == "1":
            comprar_tienda(player_id, nivel, ryos)
        elif opc == "2":
            vender_tienda(player_id)
        elif opc == "0":
            break
        else:
            print("❌ Opción inválida.")

def comprar_tienda(player_id, nivel, ryos):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    ids_tienda = [100, 101, 110, 111, 112, 120, 121, 122]
    placeholders = ','.join('?' for _ in ids_tienda)
    c.execute(f"SELECT ItemID, ItemName, Price FROM Items WHERE ItemID IN ({placeholders})", ids_tienda)
    productos = c.fetchall()

    print("\n🛒 --- SECCIÓN DE COMPRA ---")
    for i, (id_item, nombre, precio) in enumerate(productos):
        print(f"{i+1}. {nombre} - {precio} Ryos")
    print("0. Volver")
    sys.stdout.flush()

    opc = input("¿Qué deseas comprar?: ")
    if opc.isdigit() and 0 < int(opc) <= len(productos):
        idx = int(opc) - 1
        item_id, item_nombre, precio = productos[idx]

        if "(Nv 10)" in item_nombre and nivel < 10:
            print(f"❌ Nivel insuficiente. Eres nivel {nivel} y esta arma requiere Nivel 10.")
        elif ryos >= precio:
            c.execute("UPDATE Players SET Ryos = Ryos - ? WHERE PlayerID =?", (precio, player_id))
            c.execute("""
                INSERT INTO Inventory (PlayerID, ItemID, Quantity)
                VALUES (?,?,1)
                ON CONFLICT(PlayerID, ItemID) DO UPDATE SET Quantity = Quantity + 1
            """, (player_id, item_id))
            conn.commit()
            print(f"✅ Compraste {item_nombre}.")
        else:
            print("❌ No tienes suficientes Ryos.")
    conn.close()

def vender_tienda(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT inv.ItemID, i.ItemName, inv.Quantity, i.Price
        FROM Inventory inv
        JOIN Items i ON inv.ItemID = i.ItemID
        WHERE inv.PlayerID = ? AND inv.Quantity > 0 AND i.ItemType LIKE 'Material%' AND i.Price > 0
    """, (player_id,))
    inventario = c.fetchall()

    if not inventario:
        print("\n❌ No tienes materiales valiosos para vender.")
        conn.close()
        return

    print("\n⚖️ --- SECCIÓN DE VENTA ---")
    for i, (item_id, nombre, cant, precio) in enumerate(inventario):
        print(f"{i+1}. {nombre} x{cant} (Te dan {precio} Ryos por cada uno)")
    print("0. Volver")
    sys.stdout.flush()

    opc = input("Elige qué quieres vender: ")
    if opc.isdigit() and 0 < int(opc) <= len(inventario):
        idx = int(opc) - 1
        item_id, item_nombre, cant_actual, precio_unidad = inventario[idx]

        cant_vender = input(f"¿Cuántos '{item_nombre}' quieres vender? (Max {cant_actual}): ")
        if cant_vender.isdigit():
            cant_vender = int(cant_vender)
            if 0 < cant_vender <= cant_actual:
                ganancia = cant_vender * precio_unidad
                c.execute("UPDATE Players SET Ryos = Ryos + ? WHERE PlayerID =?", (ganancia, player_id))
                c.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE PlayerID =? AND ItemID =?", (cant_vender, player_id, item_id))
                c.execute("DELETE FROM Inventory WHERE Quantity <= 0")
                conn.commit()
                print(f"✅ Vendiste {cant_vender}x {item_nombre} por {ganancia} Ryos.")
            else:
                print("❌ Cantidad inválida.")
    conn.close()

def gestionar_equipo(player_id):
    while True:
        print("\n🎒 === GESTIÓN DE EQUIPO ===")
        print("1. Equipar Arma ⚔️")
        print("2. Equipar Armadura 🛡️")
        print("0. Volver")
        sys.stdout.flush()
        
        opc = input("¿Qué deseas gestionar?: ")
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        if opc == "1":
            c.execute("""
                SELECT i.ItemID, i.ItemName FROM Inventory inv
                JOIN Items i ON inv.ItemID = i.ItemID
                WHERE inv.PlayerID = ? AND i.ItemType LIKE 'Arma %' AND inv.Quantity > 0
            """, (player_id,))
            armas = c.fetchall()
            if not armas:
                print("No tienes armas en tu inventario.")
            else:
                for i, (id_item, nombre) in enumerate(armas):
                    print(f"{i+1}. {nombre}")
                sel = input("Selecciona el arma a equipar (0 para cancelar): ")
                if sel.isdigit() and 0 < int(sel) <= len(armas):
                    item_id = armas[int(sel)-1][0]
                    c.execute("UPDATE Players SET EquipWeapon = ? WHERE PlayerID = ?", (item_id, player_id))
                    conn.commit()
                    print("⚔️ Arma equipada con éxito.")
                    
        elif opc == "2":
            c.execute("""
                SELECT i.ItemID, i.ItemName FROM Inventory inv
                JOIN Items i ON inv.ItemID = i.ItemID
                WHERE inv.PlayerID = ? AND i.ItemType LIKE 'Armadura%' AND inv.Quantity > 0
            """, (player_id,))
            armaduras = c.fetchall()
            if not armaduras:
                print("No tienes armaduras en tu inventario.")
            else:
                for i, (id_item, nombre) in enumerate(armaduras):
                    print(f"{i+1}. {nombre}")
                sel = input("Selecciona la armadura a equipar (0 para cancelar): ")
                if sel.isdigit() and 0 < int(sel) <= len(armaduras):
                    item_id = armaduras[int(sel)-1][0]
                    c.execute("UPDATE Players SET EquipArmor = ? WHERE PlayerID = ?", (item_id, player_id))
                    conn.commit()
                    print("🛡️ Armadura equipada con éxito.")
                    
        elif opc == "0":
            conn.close()
            break
        else:
            print("❌ Opción inválida.")
        conn.close()

def obtener_stats_completas(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT HP, MaxHP, ATK, DEF, MAG, CritRate, CritDmg, Accuracy, Evasion, EquipWeapon, EquipArmor 
        FROM Players WHERE PlayerID = ?
    """, (player_id,))
    res = c.fetchone()
    if not res:
        conn.close()
        return None
    hp, max_hp, atk, df, mag, crit_rate, crit_dmg, acc, eva, eq_weapon, eq_armor = res
    
    if eq_weapon:
        c.execute("SELECT HP, ATK, DF, MAG, Accuracy, Evasion, CritRate, CritDmg FROM WeaponStats WHERE WeaponID = ?", (eq_weapon,))
        w = c.fetchone()
        if w:
            max_hp += w[0]; atk += w[1]; df += w[2]; mag += w[3]; acc += w[4]; eva += w[5]; crit_rate += w[6]; crit_dmg += w[7]
            
    if eq_armor:
        c.execute("SELECT HP, ATK, DF, MAG, Accuracy, Evasion, CritRate, CritDmg FROM ArmorStats WHERE ArmorID = ?", (eq_armor,))
        a = c.fetchone()
        if a:
            max_hp += a[0]; atk += a[1]; df += a[2]; mag += a[3]; acc += a[4]; eva += a[5]; crit_rate += a[6]; crit_dmg += a[7]
            
    conn.close()
    return {
        "hp": hp, "max_hp": max_hp, "atk": atk, "def": df, "mag": mag,
        "crit_rate": crit_rate, "crit_dmg": crit_dmg, "accuracy": acc, "evasion": eva
    }

def calcular_daño(atk_atacante, def_defensor, crit_rate, crit_dmg, acc_atacante, eva_defensor):
    chance_acierto = acc_atacante - eva_defensor
    if random.randint(1, 100) > chance_acierto:
        return 0, False, True 
    
    daño = max(1, atk_atacante - def_defensor)
    es_critico = random.randint(1, 100) <= crit_rate
    if es_critico:
        daño = int(daño * crit_dmg)
    return daño, es_critico, False

def consultar_pociones(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT Quantity FROM Inventory WHERE PlayerID =? AND ItemID = 100", (player_id,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

def usar_pocion_bd(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE Inventory SET Quantity = Quantity - 1 WHERE PlayerID =? AND ItemID = 100", (player_id,))
    c.execute("DELETE FROM Inventory WHERE PlayerID =? AND ItemID = 100 AND Quantity <= 0", (player_id,))
    conn.commit()
    conn.close()

def intentar_curacion(player_id, hp, max_hp):
    cant_pociones = consultar_pociones(player_id)
    if cant_pociones <= 0:
        print("❌ No te quedan Pociones de Supervivencia.")
        sys.stdout.flush()
        return hp, False
    if hp >= max_hp:
        print("💚 Tu salud ya está al máximo.")
        sys.stdout.flush()
        return hp, False
    usar_pocion_bd(player_id)
    hp = min(max_hp, hp + 50)
    print(f"🧪 Usaste una poción. ¡Recuperaste 50 HP! (Vida actual: {hp}/{max_hp})")
    sys.stdout.flush()
    return hp, True

def combate(player_id):
    datos = obtener_datos_jugador(player_id)
    nombre, hp, _, ryos, _, _, _, level, xp, current_zone, max_zone, _, _, _, _, class_id, mana, max_mana = datos

    if hp <= 0:
        print("\n💀 No puedes pelear sin vida. ¡Descansa en la ciudad primero!")
        sys.stdout.flush()
        return

    mob = obtener_monstruos_zona(current_zone)
    if not mob:
        print("\n❌ No hay monstruos configurados para esta zona.")
        sys.stdout.flush()
        return

    monster_id, enemigo_nombre, enemigo_hp, enemigo_atk, enemigo_def, exp_reward, is_boss, enemigo_crit_rate, enemigo_crit_dmg, enemigo_acc, enemigo_eva = mob
    
    stats_p = obtener_stats_completas(player_id)
    max_hp_t = stats_p["max_hp"]
    atk_t = stats_p["atk"]
    def_t = stats_p["def"]
    crit_rate_t = stats_p["crit_rate"]
    crit_dmg_t = stats_p["crit_dmg"]
    acc_t = stats_p["accuracy"]
    eva_t = stats_p["evasion"]

    print(f"\n⚔️ ¡Un {enemigo_nombre} salvaje ha aparecido! (HP: {enemigo_hp} | ATK: {enemigo_atk})")
    mostrar_drops_monstruo(monster_id)
    sys.stdout.flush()

    skills = SKILLS_CONFIG[class_id]

    while hp > 0 and enemigo_hp > 0:
        pociones_actuales = consultar_pociones(player_id)
        print(f"\nTu HP: {hp}/{max_hp_t} | Maná: {mana}/{max_mana} | HP del {enemigo_nombre}: {enemigo_hp}")
        print(f"1. [Atk] {skills['1']['nombre']} (0 MP)")
        print(f"2. [Skill] {skills['2']['nombre']} ({skills['2']['coste_mana']} MP) [CD: {skills['2']['cooldown']}s]")
        print(f"3. [Potente] {skills['3']['nombre']} ({skills['3']['coste_mana']} MP) [CD: {skills['3']['cooldown']}s]")
        print(f"4. 🧪 Usar Poción ({pociones_actuales} restantes)")
        print("5. 💨 Huir")
        sys.stdout.flush()
        acc = input("Elige tu acción: ")

        if acc in ["1", "2", "3"]:
            chosen_skill = skills[acc]
            
            if mana < chosen_skill["coste_mana"]:
                print(f"❌ No tienes suficiente Maná. Requiere {chosen_skill['coste_mana']} MP.")
                sys.stdout.flush()
                continue
                
            disponible, cd_restante = comprobar_cooldown(player_id, chosen_skill["nombre"], chosen_skill["cooldown"])
            if not disponible:
                print(f"⏳ Habilidad en enfriamiento. Espera {cd_restante}s.")
                sys.stdout.flush()
                continue
                
            mana -= chosen_skill["coste_mana"]
            registrar_cooldown(player_id, chosen_skill["nombre"])
            
            atk_efectivo = int(atk_t * chosen_skill["multiplicador"])
            daño_final, crit, esquivado = calcular_daño(atk_efectivo, enemigo_def, crit_rate_t, crit_dmg_t, acc_t, enemigo_eva)
            
            print(f"\n✨ ¡Lanzas {chosen_skill['nombre']}!")
            if esquivado:
                print(f"💨 ¡MISS! El {enemigo_nombre} ha esquivado tu golpe.")
            else:
                enemigo_hp -= daño_final
                if crit:
                    print(f"🔥 ¡CRÍTICO! Infliges {daño_final} de daño.")
                else:
                    print(f"⚔️ Infliges {daño_final} de daño al objetivo.")
            
            if enemigo_hp <= 0: 
                break
                
            daño_recibido, crit_enemigo, esquivado_player = calcular_daño(enemigo_atk, def_t, enemigo_crit_rate, enemigo_crit_dmg, enemigo_acc, eva_t)
            if esquivado_player:
                print(f"🛡️ ¡MISS! Has esquivado el ataque del {enemigo_nombre}.")
            else:
                hp -= daño_recibido
                if crit_enemigo:
                    print(f"💀 ¡GOLPE CRÍTICO DEL ENEMIGO! Te hace {daño_recibido} de daño.")
                else:
                    print(f"⚠️ El {enemigo_nombre} te devuelve el golpe y te hace {daño_recibido} de daño.")

        elif acc == "4":  
            hp, exito = intentar_curacion(player_id, hp, max_hp_t)
            if exito:
                daño_enemigo, crit_enemigo, esquivado_player = calcular_daño(enemigo_atk, def_t, enemigo_crit_rate, enemigo_crit_dmg, enemigo_acc, eva_t)
                if esquivado_player:
                    print(f"🛡️ El {enemigo_nombre} intentó atacarte mientras te curabas, ¡pero lo esquivaste!")
                else:
                    hp -= daño_enemigo
                    print(f"⚠️ El {enemigo_nombre} aprovechó tu distracción y te hizo {daño_enemigo} de daño.")

        elif acc == "5":  
            if is_boss == 1:
                print("❌ ¡No puedes huir de la batalla contra un Jefe!")
            elif random.random() > 0.3:
                print("💨 ¡Lograste escapar del combate!")
                sys.stdout.flush()
                actualizar_hp_mana_ryos_xp(player_id, hp, mana, ryos, xp)
                return
            else:
                print("❌ ¡Intentaste huir pero el enemigo te bloqueó el paso!")
                daño_enemigo, crit_enemigo, esquivado_player = calcular_daño(enemigo_atk, def_t, enemigo_crit_rate, enemigo_crit_dmg, enemigo_acc, eva_t)
                if esquivado_player:
                    print(f"🛡️ El {enemigo_nombre} intentó golpearte por la espalda, ¡pero lo esquivaste justo a tiempo!")
                else:
                    hp -= daño_enemigo
                    print(f"⚠️ El {enemigo_nombre} te golpea por la espalda haciendo {daño_enemigo} de daño.")
        else:  
            print("Acción inválida. Pierdes el turno.")
        sys.stdout.flush()

    if hp <= 0:
        print(f"\n💀 Has sido derrotado por el {enemigo_nombre}... Reapareces en la ciudad con 1 HP.")
        actualizar_hp_mana_ryos_xp(player_id, 1, max_mana, ryos, xp)
    else:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT RyosMin, RyosMax, XPMin, XPMax FROM Zones WHERE ZoneID =?", (current_zone,))
        ryos_min, ryos_max, xp_min, xp_max = c.fetchone()
        conn.close()
        
        recompensa_ryos = random.randint(ryos_min, ryos_max)
        recompensa_xp = random.randint(xp_min, xp_max)
        ryos += recompensa_ryos
        xp += recompensa_xp
        
        print(f"\n🎉 ¡Victoria! Derrotaste al {enemigo_nombre}.")
        print(f"💰 Encontraste {recompensa_ryos} Ryos.")
        print(f"⭐ Ganaste {recompensa_xp} XP.")

        subir_nivel_si_aplica(player_id, xp, level)
        tirar_drop(monster_id, player_id)
        actualizar_hp_mana_ryos_xp(player_id, hp, mana, ryos, xp)
        
        if is_boss == 1:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            if current_zone == max_zone and current_zone < 10:
                max_zone += 1
                c.execute("UPDATE Players SET MaxZone = ? WHERE PlayerID = ?", (max_zone, player_id))
                conn.commit()
                print(f"\n🏆 ¡Felicidades! Has derrotado al jefe de la zona.")
                print(f"🔓 ¡HAS DESBLOQUEADO LA ZONA {max_zone}!")
            conn.close()

            if current_zone < 10:
                avanzar = input(f"\n¿Quieres avanzar a la Zona {current_zone + 1} ahora? (s/n): ").strip().lower()
                if avanzar == 's':
                    current_zone += 1
                    conn = sqlite3.connect(DB)
                    c = conn.cursor()
                    c.execute("UPDATE Players SET CurrentZone = ? WHERE PlayerID = ?", (current_zone, player_id))
                    conn.commit()
                    conn.close()
                    print(f"\n🚶‍♂️ Viajaste a la Zona {current_zone}.")
        sys.stdout.flush()

# =====================================================================
# MODIFICADO AQUÍ: Se agregó '(Lv. {level})' al string del menú principal.
# =====================================================================
def visitar_ciudad(player_id):
    while True:
        datos = obtener_datos_jugador(player_id)
        nombre, hp, max_hp, ryos, atk, df, mag, level, xp, current_zone, max_zone, _, _, _, _, _, mana, max_mana = datos

        print(f"\n=== MENÚ PRINCIPAL | {nombre} (Lv. {level}) | HP: {hp}/{max_hp} | MP: {mana}/{max_mana} | ZONA: {current_zone} ===")
        print("1. Entrar a la Zona Segura 🛡️")
        print("2. Buscar Combate (Salir a las afueras) ⚔️")
        print("3. Cambiar de Zona de Caza (Viaje Rápido) 🗺️")
        print("4. Gestionar Equipo 🎒")
        print("5. Ver inventario 📦")
        print("6. Salir del juego 🚪")
        sys.stdout.flush()

        opcion = input("Elige una opción: ")
        if opcion == "1":
            while True:
                print(f"\n--- 🏡 ZONA SEGURA (Villa Amanecer) | Ryos: {ryos} ---")
                print("1. Descansar en la Posada (Recuperar HP y MP gratis 💤)")
                print("2. Visitar Tienda 💰")
                print("3. Forjar y Craftear 🔨")
                print("4. Volver al menú principal ↩️")
                sys.stdout.flush()
                
                sub_opc = input("¿Qué deseas hacer en la zona segura?: ")
                if sub_opc == "1":
                    hp = max_hp
                    mana = max_mana
                    actualizar_hp_mana_ryos_xp(player_id, hp, mana, ryos, xp)
                    print("\n💤 Descansando... ¡Tu salud y energía se han restablecido por completo!")
                elif sub_opc == "2":
                    visitar_tienda(player_id)
                    datos_act = obtener_datos_jugador(player_id)
                    ryos = datos_act[3] 
                elif sub_opc == "3":
                    visitar_forja(player_id)
                elif sub_opc == "4":
                    print("\nVolviendo al exterior de la zona segura...")
                    break
                else:
                    print("❌ Opción inválida en la Zona Segura.")
                sys.stdout.flush()

        elif opcion == "2":
            print(f"\n🚪 Cruzas las murallas hacia las afueras (Zona de peligro activa: {current_zone})...")
            sys.stdout.flush()
            combate(player_id)
        elif opcion == "3":
            print(f"\n=== 🗺️ Viaje Rápido (Zonas Desbloqueadas: {max_zone}) ===")
            for i in range(1, max_zone + 1):
                print(f"{i}. Configurar Zona {i}")
            print("0. Cancelar")
            sys.stdout.flush()
            try:
                z_elegida = int(input("Elige el número de zona al que quieres apuntar tus viajes: "))
                if 1 <= z_elegida <= max_zone:
                    conn = sqlite3.connect(DB)
                    c = conn.cursor()
                    c.execute("UPDATE Players SET CurrentZone = ? WHERE PlayerID = ?", (z_elegida, player_id))
                    conn.commit()
                    conn.close()
                    print(f"✈️ Has configurado tus salidas para la Zona {z_elegida}.")
                elif z_elegida != 0:
                    print("❌ Zona no válida o aún bloqueada.")
            except ValueError:
                print("❌ Ingresa un número válido.")
        elif opcion == "4":
            gestionar_equipo(player_id)
        elif opcion == "5":
            ver_inventario(player_id)
        elif opcion == "6":
            print("¡Gracias por jugar! Guardando partida...")
            sys.stdout.flush()
            break
        else:
            print("Opción inválida.")
        sys.stdout.flush()

def crear_personaje():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    nombre = input("Ingresa el nombre de tu personaje: ")
    print("\n=== Clases disponibles ===")
    print("1. Guerrero - HP:120 MP:20 ATK:15 DEF:10 MAG:5")
    print("2. Mago     - HP:80  MP:60 ATK:8  DEF:5  MAG:20")
    print("3. Arquero  - HP:100 MP:35 ATK:12 DEF:7  MAG:8")
    sys.stdout.flush()

    clase_id = None
    while clase_id not in [1, 2, 3]:
        try:
            clase_id = int(input("Elige el ID de tu clase: "))
            if clase_id not in [1, 2, 3]:
                print("ID no válido.")
        except ValueError:
            print("Ingresa un número válido.")
        sys.stdout.flush()

    base_stats = {1: [120, 20, 15, 10, 5], 2: [80, 60, 8, 5, 20], 3: [100, 35, 12, 7, 8]}
    hp, mp, atk, df, mag = base_stats[clase_id]

    c.execute("""
    INSERT INTO Players (Name, ClassID, HP, MaxHP, Mana, MaxMana, Ryos, ATK, DEF, MAG, Level, XP, CurrentZone, MaxZone, CritRate, CritDmg, STR, AGI, DEX, Accuracy, Evasion)
    VALUES (?,?,?,?,?,?, ?,?,?,?, 1, 0, 1, 1, 5, 1.5, 10, 10, 10, 80, 5)
    """, (nombre, clase_id, hp, hp, mp, mp, 100, atk, df, mag))

    last_id = c.lastrowid
    c.execute("INSERT OR IGNORE INTO PlayerLocation VALUES (?, 1)", (last_id,))
    c.execute("INSERT OR IGNORE INTO Inventory (PlayerID, ItemID, Quantity) VALUES (?, 100, 5)", (last_id,))

    print(f"\n¡Personaje '{nombre}' creado! Recibiste 5 Pociones, Maná base de clase y 100 Ryos.")
    sys.stdout.flush()
    conn.commit()
    conn.close()
    visitar_ciudad(last_id)

if __name__ == "__main__":
    init_db()
    inicializar_stats_forja()     
    inicializar_stats_armaduras() 
    actualizar_tienda_db()        
    print("=== ¡Bienvenido a JuegoNew RPG! ===")
    sys.stdout.flush()
    crear_personaje()

