import sqlite3
import random
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
    
    c.execute("INSERT OR IGNORE INTO Classes VALUES (1, 'Guerrero', 120, 15, 10, 5)")
    c.execute("INSERT OR IGNORE INTO Classes VALUES (2, 'Mago', 80, 8, 5, 20)")
    c.execute("INSERT OR IGNORE INTO Classes VALUES (3, 'Arquero', 100, 12, 7, 8)")
    
    # Tabla de Players
    c.execute("""CREATE TABLE IF NOT EXISTS Players(
        PlayerID INTEGER PRIMARY KEY,
        PlayerName TEXT NOT NULL,
        ClassID INTEGER,
        CurrentHP INTEGER,
        MaxHP INTEGER,
        Ryos INTEGER DEFAULT 100,
        FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
    )""")
    
    # Tabla de Items
    c.execute("""CREATE TABLE IF NOT EXISTS Items(
        ItemID INTEGER PRIMARY KEY,
        ItemName TEXT NOT NULL,
        ItemType TEXT,
        CostRyos INTEGER
    )""")
    
    c.execute("INSERT OR IGNORE INTO Items VALUES (100, 'Poción de Supervivencia', 'Consumible', 25)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (200, 'Hoja Espectral del Otoño', 'Material Forja', 0)")
    c.execute("INSERT OR IGNORE INTO Items VALUES (201, 'Acero Tamahagane Puro', 'Material Forja', 500)")
    
    # Tabla de Inventario
    c.execute("""CREATE TABLE IF NOT EXISTS Inventory(
        PlayerID INTEGER,
        ItemID INTEGER,
        Quantity INTEGER DEFAULT 1,
        PRIMARY KEY (PlayerID, ItemID),
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
        PlayerID INTEGER PRIMARY KEY,
        CityID INTEGER,
        FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
        FOREIGN KEY (CityID) REFERENCES Cities(CityID)
    )""")
    
    c.execute("INSERT OR IGNORE INTO Cities VALUES (1, 'Villa Amanecer', 1)")
    
    conn.commit()
    conn.close()

def mostrar_clases():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT ClassID, ClassName, BaseHP, BaseATK, BaseDEF, BaseMAG FROM Classes")
    clases = c.fetchall()
    conn.close()
    
    print("\n=== Clases disponibles ===")
    for cid, nombre, hp, atk, df, mag in clases:
        print(f"{cid}. {nombre} - HP:{hp} ATK:{atk} DEF:{df} MAG:{mag}")
    sys.stdout.flush()
    return clases

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

    print(f"\n🎒 Inventario de {nombre} ===")
    if not items:
        print("Vacío")
    else:
        for nombre_item, cantidad, tipo in items:
            print(f"- {nombre_item} x{cantidad} ({tipo})")
    sys.stdout.flush()

def obtener_datos_jugador(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT p.PlayerName, p.CurrentHP, p.MaxHP, p.Ryos, cl.BaseATK, cl.BaseDEF, cl.BaseMAG
        FROM Players p
        JOIN Classes cl ON p.ClassID = cl.ClassID
        WHERE p.PlayerID = ?
    """, (player_id,))
    datos = c.fetchone()
    conn.close()
    return datos

def actualizar_hp_y_ryos(player_id, hp, ryos):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE Players SET CurrentHP = ?, Ryos = ? WHERE PlayerID = ?", (hp, ryos, player_id))
    conn.commit()
    conn.close()

def consultar_pociones(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT Quantity FROM Inventory WHERE PlayerID = ? AND ItemID = 100", (player_id,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

def usar_pocion_bd(player_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE Inventory SET Quantity = Quantity - 1 WHERE PlayerID = ? AND ItemID = 100", (player_id,))
    # Si la cantidad llega a cero, borramos el registro para limpiar la BD
    c.execute("DELETE FROM Inventory WHERE PlayerID = ? AND ItemID = 100 AND Quantity <= 0", (player_id,))
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

def tienda(player_id):
    while True:
        nombre, hp, max_hp, ryos, atk, df, mag = obtener_datos_jugador(player_id)
        print(f"\n--- 🏪 Tienda de Villa Amanecer (Tus Ryos: {ryos}) ---")
        print("1. Comprar Poción de Supervivencia (Recupera 50 HP) - Costo: 25 Ryos")
        print("2. Volver a la plaza")
        sys.stdout.flush()
        
        opcion = input("¿Qué deseas hacer?: ")
        if opcion == "1":
            if ryos >= 25:
                ryos -= 25
                conn = sqlite3.connect(DB)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO Inventory (PlayerID, ItemID, Quantity) 
                    VALUES (?, 100, 1)
                    ON CONFLICT(PlayerID, ItemID) DO UPDATE SET Quantity = Quantity + 1
                """, (player_id,))
                conn.commit()
                conn.close()
                actualizar_hp_y_ryos(player_id, hp, ryos)
                print("🛒 ¡Compraste 1 Poción de Supervivencia!")
            else:
                print("❌ No tienes suficientes Ryos.")
            sys.stdout.flush()
        elif opcion == "2":
            break

def combate(player_id):
    nombre, hp, max_hp, ryos, atk, df, mag = obtener_datos_jugador(player_id)
    
    if hp <= 0:
        print("\n💀 No puedes pelear sin vida. ¡Descansa en la ciudad primero!")
        sys.stdout.flush()
        return

    enemigo_nombre = random.choice(["Lobo Salvaje", "Duende Asaltante"])
    enemigo_hp = random.randint(40, 70)
    enemigo_atk = random.randint(8, 14)
    enemigo_def = random.randint(2, 6)
    recompensa_ryos = random.randint(15, 35)

    print(f"\n⚔️ ¡Un {enemigo_nombre} salvaje ha aparecido! (HP: {enemigo_hp} | ATK: {enemigo_atk})")
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
            # Turno del Jugador
            daño_jugador = max(1, atk - enemigo_def)
            enemigo_hp -= daño_jugador
            print(f"💥 Atacas al {enemigo_nombre} y le infliges {daño_jugador} de daño.")

            if enemigo_hp <= 0:
                break

            # Turno del Enemigo
            daño_enemigo = max(1, enemigo_atk - df)
            hp -= daño_enemigo
            print(f"⚠️ El {enemigo_nombre} te devuelve el golpe y te hace {daño_enemigo} de daño.")
        
        elif acc == "2":
            hp, exito = intentar_curacion(player_id, hp, max_hp)
            if exito:
                # El enemigo te ataca mientras te curás
                daño_enemigo = max(1, enemigo_atk - df)
                hp -= daño_enemigo
                print(f"⚠️ El {enemigo_nombre} aprovechó tu distracción y te hizo {daño_enemigo} de daño.")
        
        elif acc == "3":
            if random.random() > 0.3:
                print("💨 ¡Lograste escapar del combate!")
                sys.stdout.flush()
                actualizar_hp_y_ryos(player_id, hp, ryos)
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
        actualizar_hp_y_ryos(player_id, 1, ryos)
    else:
        ryos += recompensa_ryos
        print(f"\n🎉 ¡Victoria! Derrotaste al {enemigo_nombre}.")
        print(f"💰 Encontraste {recompensa_ryos} Ryos.")
        actualizar_hp_y_ryos(player_id, hp, ryos)
    sys.stdout.flush()


def visitar_ciudad(player_id):
    while True:
        nombre, hp, max_hp, ryos, atk, df, mag = obtener_datos_jugador(player_id)
        
        print(f"\n=== 🛡️ {nombre} | HP: {hp}/{max_hp} | Ryos: {ryos} ===")
        print("1. Descansar en la Posada (Recuperas HP gratis)")
        print("2. Ir a la Tienda de Objetos")
        print("3. Salir a las afueras (Buscar Combate ⚔️)")
        print("4. Usar una Poción de Supervivencia")
        print("5. Ver inventario")
        print("6. Salir del juego")
        sys.stdout.flush()
        
        opcion = input("Elige una opción: ")
        if opcion == "1":
            hp = max_hp
            actualizar_hp_y_ryos(player_id, hp, ryos)
            print("\n💤 Descansando... ¡Tu salud se ha restablecido por completo!")
        elif opcion == "2":
            tienda(player_id)
        elif opcion == "3":
            combate(player_id)
        elif opcion == "4":
            hp, exito = intentar_curacion(player_id, hp, max_hp)
            if exito:
                actualizar_hp_y_ryos(player_id, hp, ryos)
        elif opcion == "5":
            mostrar_inventario(player_id, nombre)
        elif opcion == "6":
            print("¡Gracias por jugar a JuegoNew! Guardando partida...")
            sys.stdout.flush()
            break
        else:
            print("Opción inválida.")
        sys.stdout.flush()

def crear_personaje():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    nombre = input("Ingresa el nombre de tu personaje: ")
    clases = mostrar_clases()
    clase_id = None
    ids_validos = [c[0] for c in clases]
    
    while clase_id not in ids_validos:
        try:
            clase_id = int(input("Elige el ID de tu clase: "))
            if clase_id not in ids_validos:
                print("ID no válido.")
        except ValueError:
            print("Ingresa un número válido.")
        sys.stdout.flush()
    
    c.execute("SELECT BaseHP FROM Classes WHERE ClassID = ?", (clase_id,))
    base_hp = c.fetchone()[0]
    
    c.execute("""
        INSERT INTO Players (PlayerName, ClassID, CurrentHP, MaxHP, Ryos) 
        VALUES (?, ?, ?, ?, 100)
    """, (nombre, clase_id, base_hp, base_hp))
    
    last_id = c.lastrowid

    c.execute("INSERT OR IGNORE INTO Inventory (PlayerID, ItemID, Quantity) VALUES (?, ?, ?)", (last_id, 100, 5))

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
