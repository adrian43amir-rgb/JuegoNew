import sqlite3
import random
import sys

DB = "juego.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    try:
        # === TABLAS BASE ===
        c.execute("""CREATE TABLE IF NOT EXISTS Players(
            PlayerID INTEGER PRIMARY KEY, Name TEXT, HP INTEGER, MaxHP INTEGER,
            Ryos INTEGER, ATK INTEGER, DEF INTEGER, MAG INTEGER, Level INTEGER, XP INTEGER)""")

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
            PlayerID INTEGER PRIMARY KEY,
            CityID INTEGER,
            FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
            FOREIGN KEY(CityID) REFERENCES Cities(CityID) ON DELETE RESTRICT
        )""")

        # === TABLAS DE ZONAS ===
        c.execute("""CREATE TABLE IF NOT EXISTS Zones(
            ZoneID INTEGER PRIMARY KEY, ZoneName TEXT, ReqLevel INTEGER,
            RyosMin INTEGER, RyosMax INTEGER, XPMin INTEGER, XPMax INTEGER)""")

        c.execute("""CREATE TABLE IF NOT EXISTS Monsters(
            MonsterID INTEGER PRIMARY KEY, MonsterName TEXT, ZoneID INTEGER,
            HP INTEGER, ATK INTEGER, DEF INTEGER, XP INTEGER, IsBoss INTEGER DEFAULT 0,
            FOREIGN KEY(ZoneID) REFERENCES Zones(ZoneID) ON DELETE SET NULL
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS MonsterDrops(
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
        c.execute("INSERT OR IGNORE INTO Items VALUES (100, 'Poción de Supervivencia', 'Consumible', 25)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (200, 'Hoja Espectral del Otoño', 'Material Forja', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (201, 'Acero Tamahagane', 'Material', 15)")

        # ==================== ZONA 1: BOSQUE AMANECER | NV 1-5 ====================
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
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (1, 'Slime Verde', 1, 20, 5, 2, 10, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (2, 'Lobo Salvaje', 1, 35, 8, 3, 15, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (3, 'Goblin Ratero', 1, 40, 9, 4, 18, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (4, 'Lobo Alfa', 1, 120, 18, 8, 80, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 1, 300, 60)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 2, 301, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 2, 302, 30)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 3, 200, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 3, 303, 20)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 4, 304, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 4, 305, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 400, 1, 304, 1, 305, 1, 201, 10, 80)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 401, 2, 304, 1, 305, 1, 200, 5, 80)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 402, 3, 304, 1, 305, 1, 302, 8, 80)")

        # ==================== ZONA 2: MINAS ABANDONADAS | NV 6-10 ====================
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
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (5, 'Rata Gigante', 2, 45, 10, 3, 25, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (6, 'Murciélago Caverna', 2, 40, 11, 4, 28, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (7, 'Goblin Minero', 2, 50, 12, 5, 35, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (8, 'Rey Goblin', 2, 150, 22, 10, 120, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 5, 311, 60)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 6, 310, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 7, 312, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 7, 313, 30)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 8, 314, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 8, 315, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 420, 1, 314, 1, 315, 1, 310, 15, 75)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 421, 2, 314, 1, 315, 1, 313, 10, 75)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 422, 3, 314, 1, 315, 1, 312, 12, 75)")

        # ==================== ZONA 3: PANTANO SOMBRÍO | NV 11-15 ====================
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
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (9, 'Rana Venenosa', 3, 60, 13, 4, 45, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (10, 'Zombi Ahogado', 3, 70, 15, 6, 55, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (11, 'Espíritu Pantano', 3, 65, 16, 5, 60, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (12, 'Anciano del Pantano', 3, 180, 25, 12, 180, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 9, 320, 60)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 10, 321, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 11, 322, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 11, 323, 30)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 12, 324, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 12, 325, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 440, 1, 324, 1, 325, 1, 322, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 441, 2, 324, 1, 325, 1, 322, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 442, 3, 324, 1, 325, 1, 322, 15, 70)")

        # ==================== ZONA 4: TEMPLO DEL FUEGO | NV 16-20 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (4, 'Templo del Fuego', 16, 50, 70, 100, 140)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (330, 'Escama de Fuego', 'Material', 20)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (331, 'Carbón Puro', 'Material', 18)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (332, 'Núcleo de Fuego', 'Material', 25)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (333, 'Brasa Eterna', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (334, 'Esencia de Ifrit', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (450, 'Espadón Ígneo', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (451, 'Cetro de Ifrit', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (452, 'Arco de Llamas', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (13, 'Esqueleto Ígneo', 4, 80, 18, 6, 80, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (14, 'Salamandra', 4, 75, 20, 7, 85, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (15, 'Golem de Ceniza', 4, 100, 22, 10, 100, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (16, 'Ifrit Menor', 4, 220, 30, 15, 250, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 13, 330, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 14, 331, 60)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 15, 332, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 16, 333, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 16, 334, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 450, 1, 333, 1, 334, 1, 332, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 451, 2, 333, 1, 334, 1, 332, 15, 70)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 452, 3, 333, 1, 334, 1, 332, 15, 70)")

        # ==================== ZONA 5: BOSQUE HELADO | NV 21-25 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (5, 'Bosque Helado', 21, 70, 100, 140, 200)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (340, 'Pelaje Polar', 'Material', 25)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (341, 'Cristal de Escarcha', 'Material', 22)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (342, 'Colmillo de Hielo', 'Material', 28)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (343, 'Garras de Yeti', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (344, 'Esencia Glacial', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (460, 'Hacha Glacial', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (461, 'Báculo de Escarcha', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (462, 'Arco Glacial', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (17, 'Lobo de Hielo', 5, 100, 23, 8, 110, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (18, 'Duende Polar', 5, 95, 25, 9, 120, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (19, 'Yeti Joven', 5, 130, 28, 12, 140, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (20, 'Yeti Anciano', 5, 280, 38, 18, 350, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 17, 342, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 18, 340, 60)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 19, 341, 45)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 20, 343, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 20, 344, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 460, 1, 343, 1, 344, 1, 341, 18, 65)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 461, 2, 343, 1, 344, 1, 341, 18, 65)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 462, 3, 343, 1, 344, 1, 341, 18, 65)")

        # ==================== ZONA 6: DESIERTO CARMESÍ | NV 26-30 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (6, 'Desierto Carmesí', 26, 100, 140, 200, 280)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (350, 'Aguijón de Escorpión', 'Material', 30)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (351, 'Sable Oxidado', 'Material', 28)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (352, 'Núcleo de Arena', 'Material', 35)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (353, 'Urna del Faraón', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (354, 'Esencia Carmesí', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (470, 'Cimitarra Carmesí', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (471, 'Báculo de Arena', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (472, 'Arco del Desierto', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (21, 'Escorpión de Arena', 6, 125, 28, 10, 150, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (22, 'Bandido del Desierto', 6, 120, 30, 11, 160, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (23, 'Momia Guardiana', 6, 160, 33, 14, 180, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (24, 'Faraón Maldito', 6, 350, 45, 22, 500, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 21, 350, 55)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 22, 351, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 23, 352, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 24, 353, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 24, 354, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 470, 1, 353, 1, 354, 1, 352, 20, 60)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 471, 2, 353, 1, 354, 1, 352, 20, 60)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 472, 3, 353, 1, 354, 1, 352, 20, 60)")

        # ==================== ZONA 7: MONTAÑA DEL TRUENO | NV 31-35 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (7, 'Montaña del Trueno', 31, 140, 190, 280, 380)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (360, 'Pluma de Arpía', 'Material', 35)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (361, 'Fragmento de Roca', 'Material', 32)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (362, 'Núcleo de Trueno', 'Material', 40)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (363, 'Garra de Wyvern', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (364, 'Esencia del Trueno', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (480, 'Mandoble del Trueno', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (481, 'Báculo del Rayo', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (482, 'Arco del Wyvern', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (25, 'Arpía', 7, 150, 33, 12, 200, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (26, 'Gólem de Roca', 7, 190, 36, 16, 220, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (27, 'Wyvern Joven', 7, 210, 40, 18, 250, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (28, 'Rey Wyvern', 7, 420, 52, 25, 700, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 25, 360, 55)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 26, 361, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 27, 362, 45)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 28, 363, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 28, 364, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 480, 1, 363, 1, 364, 1, 362, 25, 55)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 481, 2, 363, 1, 364, 1, 362, 25, 55)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 482, 3, 363, 1, 364, 1, 362, 25, 55)")

        # ==================== ZONA 8: CATEDRAL MALDITA | NV 36-40 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (8, 'Catedral Maldita', 36, 190, 250, 380, 500)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (370, 'Espada Rota', 'Material', 40)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (371, 'Símbolo Sagrado', 'Material', 38)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (372, 'Esencia Fantasmal', 'Material', 45)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (373, 'Cáliz Profano', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (374, 'Esencia Oscura', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (490, 'Espada Profana', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (491, 'Báculo Oscuro', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (492, 'Arco Sombrio', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (29, 'Caballero Caído', 8, 180, 38, 14, 280, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (30, 'Sacerdote Oscuro', 8, 170, 42, 15, 300, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (31, 'Gárgola Viviente', 8, 230, 45, 20, 320, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (32, 'Sacerdote Caído', 8, 500, 60, 28, 1000, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 29, 370, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 30, 371, 55)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 31, 372, 45)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 32, 373, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 32, 374, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 490, 1, 373, 1, 374, 1, 372, 30, 50)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 491, 2, 373, 1, 374, 1, 372, 30, 50)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 492, 3, 373, 1, 374, 1, 372, 30, 50)")

        # ==================== ZONA 9: ABISMO CRISTALINO | NV 41-45 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (9, 'Abismo Cristalino', 41, 250, 320, 500, 650)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (380, 'Seda de Cristal', 'Material', 45)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (381, 'Núcleo Prismático', 'Material', 42)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (382, 'Cristal Puro', 'Material', 50)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (383, 'Escama de Cristal', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (384, 'Esencia Prismática', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (500, 'Espada de Cristal', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (501, 'Báculo Prismático', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (502, 'Arco de Cristal', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (33, 'Araña de Cristal', 9, 210, 43, 16, 400, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (34, 'Slime Prismático', 9, 200, 46, 18, 420, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (35, 'Golem de Cristal', 9, 270, 50, 24, 450, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (36, 'Dragón de Cristal', 9, 600, 68, 32, 1500, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 33, 380, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 34, 381, 55)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 35, 382, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 36, 383, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 36, 384, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 500, 1, 383, 1, 384, 1, 382, 35, 45)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 501, 2, 383, 1, 384, 1, 382, 35, 45)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 502, 3, 383, 1, 384, 1, 382, 35, 45)")

        # ==================== ZONA 10: CIUDADELA DEL CAOS | NV 46-50 ====================
        c.execute("INSERT OR IGNORE INTO Zones VALUES (10, 'Ciudadela del Caos', 46, 320, 400, 650, 800)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (390, 'Cuernos de Demonio', 'Material', 50)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (391, 'Placa del Caos', 'Material', 48)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (392, 'Corazón Demoníaco', 'Material', 60)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (393, 'Corona del Caos', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (394, 'Esencia del Caos', 'Material Boss', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (510, 'Espada del Caos', 'Arma Guerrero', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (511, 'Báculo del Caos', 'Arma Mago', 0)")
        c.execute("INSERT OR IGNORE INTO Items VALUES (512, 'Arco del Abismo', 'Arma Arquero', 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (37, 'Demonio Menor', 10, 250, 48, 18, 600, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (38, 'Caballero del Caos', 10, 280, 52, 22, 650, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (39, 'Archidemonio', 10, 320, 56, 26, 700, 0)")
        c.execute("INSERT OR IGNORE INTO Monsters VALUES (40, 'Señor del Caos', 10, 800, 75, 35, 3000, 1)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 37, 390, 50)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 38, 391, 55)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 39, 392, 40)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 40, 393, 100)")
        c.execute("INSERT OR IGNORE INTO MonsterDrops VALUES (NULL, 40, 394, 100)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 510, 1, 393, 1, 394, 1, 392, 40, 40)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 511, 2, 393, 1, 394, 1, 392, 40, 40)")
        c.execute("INSERT OR IGNORE INTO CraftingRecipes VALUES (NULL, 512, 3, 393, 1, 394, 1, 392, 40, 40)")

        conn.commit()
        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

def obtener_datos_jugador(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT p.Name, p.HP, p.MaxHP, p.Ryos, p.ATK, p.DEF, p.MAG, p.Level, p.XP, pl.CityID
        FROM Players p
        JOIN PlayerLocation pl ON p.PlayerID = pl.PlayerID
        WHERE p.PlayerID =?
    """, (player_id,))
    datos = c.fetchone()
    conn.close()
    return datos

def actualizar_hp_ryos_xp(player_id, hp, ryos, xp):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE Players SET HP =?, Ryos =?, XP =? WHERE PlayerID =?", (hp, ryos, xp, player_id))
    conn.commit()
    conn.close()

def subir_nivel_si_aplica(player_id, xp_actual, level_actual):
    # XP necesaria para subir: 100 * nivel actual
    xp_necesaria = 100 * level_actual
    
    if xp_actual >= xp_necesaria:
        nuevo_level = level_actual + 1
        xp_restante = xp_actual - xp_necesaria
        
        # Sube stats base al subir nivel
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT ATK, DEF, MAG, MaxHP FROM Players WHERE PlayerID =?", (player_id,))
        atk, df, mag, max_hp = c.fetchone()
        
        # Stats que gana por nivel
        atk += 2
        df += 1
        mag += 1
        max_hp += 10
        
        c.execute("""
            UPDATE Players 
            SET Level =?, XP =?, ATK =?, DEF =?, MAG =?, MaxHP =?, HP =?
            WHERE PlayerID =?
        """, (nuevo_level, xp_restante, atk, df, mag, max_hp, max_hp, player_id))
        conn.commit()
        conn.close()
        
        print(f"\n🎊 ¡SUBISTE A NIVEL {nuevo_level}!")
        print(f"💪 ATK +2 | DEF +1 | MAG +1 | HP +10")
        sys.stdout.flush()
        return True
    return False

def obtener_monstruos_zona(zone_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT MonsterID, MonsterName, HP, ATK, DEF, XP, IsBoss FROM Monsters WHERE ZoneID =?", (zone_id,))
    mobs = c.fetchall()
    conn.close()
    return random.choice(mobs)

def mostrar_drops_monstruo(monster_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT i.ItemName, d.DropRate FROM MonsterDrops d
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
    c.execute("SELECT ItemID, DropRate FROM MonsterDrops WHERE MonsterID =?", (monster_id,))
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
    nombre, hp, max_hp, ryos, atk, df, mag, level, xp, zone_id = datos

    if hp <= 0:
        print("\n💀 No puedes pelear sin vida. ¡Descansa en la ciudad primero!")
        sys.stdout.flush()
        return

    mob = obtener_monstruos_zona(zone_id)
    monster_id, enemigo_nombre, enemigo_hp, enemigo_atk, enemigo_def, enemigo_xp, is_boss = mob

    print(f"\n⚔️ ¡Un {enemigo_nombre} salvaje ha aparecido! (HP: {enemigo_hp} | ATK: {enemigo_atk})")
    mostrar_drops_monstruo(monster_id)
    sys.stdout.flush()

    while hp > 0 and enemigo_hp > 0:
        pociones_actuales = consultar_pociones(player_id)
        print(f"\nTu HP: {hp}/{max_hp} | HP del {enemigo_nombre}: {enemigo_hp}")
        print(f"1. Atacar con tu arma")
        print(f"2. Usar Poción ({pociones_actuales} restantes)")
        print("3. Huir")
        sys.stdout.flush()
        acc = input("Elige tu acción: ")

        if acc == "1":
            daño_jugador = max(1, atk - enemigo_def)
            enemigo_hp -= daño_jugador
            print(f"💥 Atacas al {enemigo_nombre} y le infliges {daño_jugador} de daño.")
            if enemigo_hp <= 0: break
            daño_enemigo = max(1, enemigo_atk - df)
            hp -= daño_enemigo
            print(f"⚠️ El {enemigo_nombre} te devuelve el golpe y te hace {daño_enemigo} de daño.")

        elif acc == "2":
            hp, exito = intentar_curacion(player_id, hp, max_hp)
            if exito:
                daño_enemigo = max(1, enemigo_atk - df)
                hp -= daño_enemigo
                print(f"⚠️ El {enemigo_nombre} aprovechó tu distracción y te hizo {daño_enemigo} de daño.")

        elif acc == "3":
            if random.random() > 0.3:
                print("💨 ¡Lograste escapar del combate!")
                sys.stdout.flush()
                actualizar_hp_ryos_xp(player_id, hp, ryos, xp)
                return
            else:
                print("❌ ¡Intentaste huir pero el enemigo te bloqueó el paso!")
                daño_enemigo = max(1, enemigo_atk - df)
                hp -= daño_enemigo
                print(f"⚠️ El {enemigo_nombre} te golpea por la espalda haciendo {daño_enemigo} de daño.")
        else:
            print("Acción inválida. Pierdes el turno.")
        sys.stdout.flush()

    if hp <= 0:
        print(f"\n💀 Has sido derrotado por el {enemigo_nombre}... Reapareces en la ciudad con 1 HP.")
        actualizar_hp_ryos_xp(player_id, 1, ryos, xp)
    else:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT RyosMin, RyosMax, XPMin, XPMax FROM Zones WHERE ZoneID =?", (zone_id,))
        ryos_min, ryos_max, xp_min, xp_max = c.fetchone()
        conn.close()
        recompensa_ryos = random.randint(ryos_min, ryos_max)
        recompensa_xp = random.randint(xp_min, xp_max)
        ryos += recompensa_ryos
        xp += recompensa_xp
        print(f"\n🎉 ¡Victoria! Derrotaste al {enemigo_nombre}.")
        print(f"💰 Encontraste {recompensa_ryos} Ryos.")
        print(f"⭐ Ganaste {recompensa_xp} XP.")

        # Checa si sube de nivel
        subir_nivel_si_aplica(player_id, xp, level)
        tirar_drop(monster_id, player_id)
        actualizar_hp_ryos_xp(player_id, hp, ryos, xp)
        sys.stdout.flush()

def visitar_ciudad(player_id):
    while True:
        datos = obtener_datos_jugador(player_id)
        nombre, hp, max_hp, ryos, atk, df, mag, level, xp, zone_id = datos

        print(f"\n=== 🛡️ {nombre} | HP: {hp}/{max_hp} | Ryos: {ryos} | NV: {level} ===")
        print("1. Descansar en la Posada (Recuperas HP gratis)")
        print("2. Salir a las afueras (Buscar Combate ⚔️)")
        print("3. Usar una Poción de Supervivencia")
        print("4. Salir del juego")
        sys.stdout.flush()

        opcion = input("Elige una opción: ")
        if opcion == "1":
            hp = max_hp
            actualizar_hp_ryos_xp(player_id, hp, ryos, xp)
            print("\n💤 Descansando... ¡Tu salud se ha restablecido por completo!")
        elif opcion == "2":
            combate(player_id)
        elif opcion == "3":
            hp, exito = intentar_curacion(player_id, hp, max_hp)
            if exito:
                actualizar_hp_ryos_xp(player_id, hp, ryos, xp)
        elif opcion == "4":
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
    print("1. Guerrero - HP:120 ATK:15 DEF:10 MAG:5")
    print("2. Mago - HP:80 ATK:8 DEF:5 MAG:20")
    print("3. Arquero - HP:100 ATK:12 DEF:7 MAG:8")
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

    base_stats = {1: [120, 15, 10, 5], 2: [80, 8, 5, 20], 3: [100, 12, 7, 8]}
    hp, atk, df, mag = base_stats[clase_id]

    c.execute("""
        INSERT INTO Players (Name, HP, MaxHP, Ryos, ATK, DEF, MAG, Level, XP)
        VALUES (?,?,?,?,?,?,?, 1, 0)
    """, (nombre, hp, hp, 100, atk, df, mag))

    last_id = c.lastrowid
    c.execute("INSERT INTO PlayerLocation VALUES (?, 1)", (last_id,))
    c.execute("INSERT INTO Inventory (PlayerID, ItemID, Quantity) VALUES (?,?,?)", (last_id, 100, 5))

    print(f"\n¡Personaje '{nombre}' creado! Recibiste 5 Pociones y 100 Ryos.")
    sys.stdout.flush()
    conn.commit()
    conn.close()
    visitar_ciudad(last_id)

if __name__ == "__main__":
    init_db()
    print("=== ¡Bienvenido a JuegoNew RPG! ===")
    sys.stdout.flush()
    crear_personaje()
