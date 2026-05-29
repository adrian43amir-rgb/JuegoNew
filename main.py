import sqlite3
import sys

DB = "juego.db"

def mostrar_clases():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT ClassID, ClassName, BaseHP, BaseATK, BaseDEF, BaseMAG FROM ClassClasses")
    clases = c.fetchall()
    conn.close()

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

def crear_personaje():
    nombre = input("\nIngresa el nombre de tu personaje: ").strip()

    clases = mostrar_clases()
    ids_validos = [c[0] for c in clases]

    while True:
        try:
            cid = int(input("Elige el ID de tu clase: "))
            if cid in ids_validos:
                break
            print("ID inválido, intenta de nuevo.")
        except ValueError:
            print("Pon un número.")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO Players (PlayerName, ClassID) VALUES (?,?)", (nombre, cid))
    conn.commit()
    conn.close()

    print(f"\nPersonaje '{nombre}' creado con éxito!")

if __name__ == "__main__":
    print("=== JuegoNew RPG ===")
    crear_personaje()
    mostrar_items()
