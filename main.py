import sqlite3
import sys

DB = "juego.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Tabla de Clases
    c.execute("""CREATE TABLE IF NOT EXISTS Classes(
        ClassID INTEGER PRIMARY KEY,
        ClassName TEXT NOT NULL,
        BaseHP INTEGER,
        BaseATK INTEGER,
        BaseDEF INTEGER,
        BaseMAG INTEGER
    )""")
    
    # Meter las 3 clases por defecto si no existen
    c.execute("INSERT OR IGNORE INTO Classes VALUES (1, 'Guerrero', 120, 15, 10, 5)")
    c.execute("INSERT OR IGNORE INTO Classes VALUES (2, 'Mago', 80, 8, 5, 20)")
    c.execute("INSERT OR IGNORE INTO Classes VALUES (3, 'Arquero', 100, 12, 7, 8)")
    
    # Tabla de Players
    c.execute("""CREATE TABLE IF NOT EXISTS Players(
        PlayerID INTEGER PRIMARY KEY,
        PlayerName TEXT NOT NULL,
        ClassID INTEGER,
        FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
    )""")
    
    # Tabla de Items
    c.execute("""CREATE TABLE IF NOT EXISTS Items(
        ItemID INTEGER PRIMARY KEY,
        ItemName TEXT NOT NULL,
        ItemType TEXT,
        CostRyos INTEGER
    )""")
    
    # Meter items por defecto
    c.execute("INSERT OR IGNORE INTO Items VALUES (100, 'Poción de Supervivencia', 'Consumible', 25)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (200, 'Hoja Espectral del Otoño', 'Material Forja', 0)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (201, 'Acero Tamahagane Puro', 'Material Forja', 500)")
    
    # Tabla de Inventario
    c.execute("""CREATE TABLE IF NOT EXISTS Inventory(
        PlayerID INTEGER,
        ItemID INTEGER,
        Quantity INTEGER DEFAULT 1,
        FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
        FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
    )""")
    
    # Tablas de Ciudad
    c.execute("""CREATE TABLE IF NOT EXISTS Cities(
        CityID INTEGER PRIMARY KEY,
        CityName TEXT NOT NULL,
        IsSafeZone INTEGER DEFAULT 1
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS PlayerLocation(
        PlayerID INTEGER,
        CityID INTEGER,
        FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
        FOREIGN KEY (CityID) REFERENCES Cities(CityID)
    )""")
    
    # Meter Villa Amanecer
    c.execute("INSERT OR IGNORE INTO Cities VALUES (1, 'Villa Amanecer', 1)")
    
    conn.commit()
    conn.close()

def mostrar_clases():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT ClassID, ClassName, BaseHP, BaseATK, BaseDEF, BaseMAG FROM Classes")
    clases = c.fetchall()
    conn.close()

    if not clases:
        print("\n=== No hay clases en la BD. Usando clases por defecto ===")
        clases = [
            (1, "Guerrero", 120, 15, 10, 5),
            (2, "Mago", 80, 8, 5, 20),
            (3, "Arquero", 100, 12, 7, 8)
        ]

    print("\n=== Clases disponibles ===")
    for cid, nombre, hp, atk, df, mag in clases:
        print(f"{cid}. {nombre} - HP:{hp} ATK:{atk} DEF:{df} MAG:{mag}")
        sys.stdout.flush()
    return clases

def mostrar_items():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT ItemID, ItemName, ItemType, CostRyos FROM Items")
    items = c.fetchall()
    conn.close()

    print("\n=== Items disponibles ===")
    for iid, nombre, tipo, costo in items:
        print(f"{iid}. {nombre} - {tipo} - {costo} Ryos")

def mostrar_inventario(player_id, nombre):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT i.ItemName, inv.Quantity, i.ItemType 
        FROM Inventory inv
        JOIN Items i ON inv.ItemID = i.ItemID
        WHERE inv.PlayerID = ?
    """, (player_id,))
    items = c.fetchall()
    conn.close()

    print(f"\n=== Inventario de {nombre} ===")
    if not items:
        print("Vacío")
    else:
        for nombre_item, cantidad, tipo in items:
            print(f"{nombre_item} x{cantidad} - {tipo}")

def visitar_ciudad(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT c.CityName, c.IsSafeZone 
        FROM PlayerLocation pl
        JOIN Cities c ON pl.CityID = c.CityID
        WHERE pl.PlayerID = ?
    """, (player_id,))
    ciudad = c.fetchone()
    conn.close()

    if ciudad:
        nombre, segura = ciudad
        print(f"\n=== {nombre} ===")
        if segura:
            print("Zona segura. Aquí puedes descansar y curarte.")
        print("1. Descansar - Recuperas HP gratis")
        print("2. Ver inventario")
        print("3. Salir de la ciudad")
    else:
        print("No estás en ninguna ciudad")

def crear_personaje():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    nombre = input("Ingresa el nombre de tu personaje: ")
    clases = mostrar_clases()
    clase_id = int(input("Elige el ID de tu clase: "))
    
    c.execute("INSERT INTO Players (PlayerName, ClassID) VALUES (?, ?)", (nombre, clase_id))
    last_id = c.lastrowid

    # Dar 5 Pociones de HP al crear el personaje
    c.execute("INSERT INTO Inventory (PlayerID, ItemID, Quantity) VALUES (?, ?, ?)", 
              (last_id, 100, 5))

    # Meter al jugador en Villa Amanecer
    c.execute("INSERT INTO PlayerLocation (PlayerID, CityID) VALUES (?, ?)", 
              (last_id, 1))

    print(f"Personaje '{nombre}' creado con éxito!")
    print("Recibiste 5 Pociones de Supervivencia")
    
    conn.commit()
    conn.close()
    
    mostrar_inventario(last_id, nombre)
    visitar_ciudad(last_id)


if __name__ == "__main__":
    init_db()  # Crea las tablas y mete Villa Amanecer
    print("=== JuegoNew RPG ===")
    crear_personaje()
    mostrar_items()
