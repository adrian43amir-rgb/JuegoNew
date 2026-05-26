# JuegoNew 🎮

**Descripción:** Creo mi propio juego

Este repositorio contiene el esquema y datos iniciales para un sistema de juego RPG con clases, jugadores e ítems.

## 📊 Estructura de la Base de Datos

### Tabla: BaseClasses
Contiene las clases base del juego con sus estadísticas iniciales.

| ClassID | ClassName | BaseHP | BaseATK | BaseDEF | BaseMAG |
|---------|-----------|--------|---------|---------|----------|
| 1 | Guerrero | 150 | 12 | 15 | 0 |
| 2 | Mago | 70 | 0 | 5 | 18 |
| 3 | Arquero | 100 | 15 | 8 | 0 |

### Tabla: Players
Almacena información de los jugadores.

- `PlayerID`: Identificador único del jugador
- `Username`: Nombre de usuario único
- `ClassID`: Clase seleccionada
- `CurrentLevel`: Nivel actual (por defecto 1)
- `CurrentXP`: Experiencia acumulada
- `GoldRyos`: Moneda del juego
- `AvailableAttributePoints`: Puntos disponibles para mejorar atributos
- `HasUsedInkPurification`: Control de habilidad especial

### Tabla: Items
Catálogo de ítems disponibles en el juego.

| ItemID | ItemName | ItemType | CostRyos | IsSoulbound |
|--------|----------|----------|----------|-------------|
| 100 | Poción de Supervivencia | Consumible | 25 | No |
| 200 | Hoja Espectral del Otoño | Material Forja | 0 | Sí |
| 201 | Acero Tamahagane Puro | Material Forja | 500 | No |

## 📁 Archivos

- **schema.sql** - Definición de las tablas
- **data.sql** - Datos iniciales
- **README.md** - Esta documentación

## 🚀 Cómo Usar

1. Ejecuta `schema.sql` para crear las tablas
2. Ejecuta `data.sql` para insertar los datos iniciales
3. ¡Comienza a desarrollar tu juego!

---

*Proyecto en desarrollo* 🎮