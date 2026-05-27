-- ==========================================
-- INSERTAR MAPAS
-- ==========================================
INSERT INTO Maps (MapID, MapName, Description, Width, Height, DifficultyLevel, RecommendedLevel, IsDiscovered)
VALUES 
(1, 'Bosque Inicial', 'Un bosque tranquilo donde comienzan los aventureros. Lleno de pequeños monstruos y naturaleza.', 100, 100, 1, 1, 1),
(2, 'Caverna Oscura', 'Una caverna profunda y peligrosa. Hogar de criaturas subterráneas y minerales valiosos.', 80, 120, 2, 5, 0),
(3, 'Torre Antigua', 'Una torre en ruinas que flota en el cielo. Se dice que contiene magia antigua y tesoros.', 60, 150, 3, 10, 0),
(4, 'Volcán Dormido', 'Un volcán que despierta. El calor extremo y los monstruos de fuego habitan este lugar.', 100, 100, 4, 15, 0),
(5, 'Castillo del Rey Mago', 'El castillo más poderoso del reino. Solo los más valientes se atreven a entrar.', 150, 150, 5, 20, 0);

-- ==========================================
-- INSERTAR UBICACIONES EN MAPAS
-- ==========================================
INSERT INTO MapLocations (LocationID, MapID, LocationName, CoordinateX, CoordinateY, Description, IsNPCLocation, IsTreasureLocation)
VALUES 
(1, 1, 'Entrada del Bosque', 10, 10, 'La entrada principal al Bosque Inicial', 1, 0),
(2, 1, 'Árbol Antiguo', 50, 50, 'Un árbol gigante en el centro del bosque', 0, 1),
(3, 1, 'Arroyo Cristalino', 30, 70, 'Un arroyo con agua pura', 0, 0),
(4, 2, 'Entrada Caverna', 5, 5, 'La entrada a la Caverna Oscura', 1, 0),
(5, 2, 'Mina de Cristales', 40, 60, 'Una mina brillante con cristales raros', 0, 1);

-- ==========================================
-- INSERTAR TIPOS DE MONSTRUOS
-- ==========================================
INSERT INTO MonsterTypes (MonsterTypeID, MonsterTypeName, Description, BaseMonsterRarity)
VALUES 
(1, 'Slime Verde', 'Una criatura gelatinosa y débil. Perfecta para principiantes.', 'Common'),
(2, 'Lobo Salvaje', 'Un lobo feroz con colmillos afilados. Más fuerte que los Slimes.', 'Common'),
(3, 'Goblin', 'Una criatura pequeña pero astuta. Usa armas simples.', 'Uncommon'),
(4, 'Esqueleto Guerrero', 'Un antiguo guerrero resucitado. Tiene defensa moderada.', 'Uncommon'),
(5, 'Dragón Joven', 'Un dragón pequeño pero poderoso. Domina el fuego.', 'Rare'),
(6, 'Gigante de Hielo', 'Un coloso de hielo que congela todo a su paso.', 'Rare'),
(7, 'Demonio Oscuro', 'Una criatura de la oscuridad. Muy poderosa y resistente.', 'Epic'),
(8, 'Rey Dragón', 'El dragón más poderoso. Un jefe legendario.', 'Legendary');

-- ==========================================
-- INSERTAR MONSTRUOS INICIALES
-- ==========================================
INSERT INTO Monsters (MonsterID, MonsterTypeID, Level, CurrentHP, MaxHP, ATK, DEF, MAG, SPD, ExperienceReward, GoldReward, CanDrop)
VALUES 
(NEWID(), 1, 1, 10, 10, 2, 0, 1, 1, 10, 5, 1),
(NEWID(), 2, 2, 25, 25, 5, 2, 0, 3, 30, 20, 1),
(NEWID(), 3, 3, 20, 20, 6, 1, 1, 2, 40, 25, 1),
(NEWID(), 4, 5, 40, 40, 8, 5, 2, 2, 80, 50, 1),
(NEWID(), 5, 10, 100, 100, 15, 8, 12, 8, 300, 150, 1),
(NEWID(), 6, 12, 120, 120, 14, 10, 16, 6, 350, 200, 1),
(NEWID(), 7, 18, 200, 200, 25, 15, 20, 7, 600, 400, 1),
(NEWID(), 8, 25, 400, 400, 40, 20, 35, 10, 1000, 1000, 1);

-- ==========================================
-- INSERTAR DROPS DE MONSTRUOS
-- ==========================================
INSERT INTO MonsterDrops (DropID, MonsterTypeID, ItemID, DropChance, MinQuantity, MaxQuantity)
VALUES 
(1, 1, 100, 30.0, 1, 2),      -- Slime Verde dropea Poción de Supervivencia (30%)
(2, 2, 200, 50.0, 1, 1),      -- Lobo Salvaje dropea Hoja Espectral (50%)
(3, 3, 100, 40.0, 1, 3),      -- Goblin dropea Poción (40%)
(4, 4, 201, 70.0, 1, 2),      -- Esqueleto dropea Acero Puro (70%)
(5, 5, 201, 80.0, 2, 3),      -- Dragón Joven dropea Acero Puro (80%)
(6, 6, 200, 90.0, 1, 2),      -- Gigante de Hielo dropea Hoja Espectral (90%)
(7, 7, 100, 60.0, 3, 5),      -- Demonio Oscuro dropea Pociones (60%)
(8, 8, 201, 100.0, 5, 10);    -- Rey Dragón dropea Acero Puro (100%)

-- ==========================================
-- INSERTAR SPAWNS DE MONSTRUOS EN MAPAS
-- ==========================================
INSERT INTO MapMonsterSpawns (SpawnID, MapID, MonsterTypeID, SpawnLocationX, SpawnLocationY, SpawnRate, MaxMonsterCount, RespawnTimeSeconds)
VALUES 
(1, 1, 1, 20, 20, 70.0, 5, 300),      -- Slimes verdes en Bosque Inicial
(2, 1, 2, 50, 50, 50.0, 3, 400),      -- Lobos salvajes en Bosque Inicial
(3, 1, 3, 75, 75, 40.0, 2, 500),      -- Goblins en Bosque Inicial
(4, 2, 4, 30, 30, 60.0, 4, 350),      -- Esqueletos en Caverna Oscura
(5, 2, 5, 60, 60, 30.0, 1, 600),      -- Dragones Jóvenes en Caverna Oscura
(6, 3, 6, 40, 40, 50.0, 2, 450),      -- Gigantes de Hielo en Torre Antigua
(7, 4, 7, 50, 50, 70.0, 3, 380),      -- Demonios Oscuros en Volcán
(8, 5, 8, 75, 75, 100.0, 1, 1000);    -- Rey Dragón en Castillo

-- ==========================================
-- INSERTAR ENCUENTROS ALEATORIOS
-- ==========================================
INSERT INTO RandomEncounters (EncounterID, MapID, MonsterTypeID, EncounterChance, MinMonsterCount, MaxMonsterCount)
VALUES 
(1, 1, 1, 40.0, 1, 3),         -- Encuentro con Slimes en Bosque
(2, 1, 2, 25.0, 1, 2),         -- Encuentro con Lobos en Bosque
(3, 2, 4, 50.0, 2, 4),         -- Encuentro con Esqueletos en Caverna
(4, 2, 5, 20.0, 1, 1),         -- Encuentro con Dragón Joven en Caverna
(5, 3, 6, 60.0, 1, 3),         -- Encuentro con Gigantes de Hielo en Torre
(6, 4, 7, 70.0, 2, 3),         -- Encuentro con Demonios en Volcán
(7, 5, 8, 100.0, 1, 1);        -- Encuentro con Rey Dragón en Castillo

-- ==========================================
-- INSERTAR EVENTOS EN MAPAS
-- ==========================================
INSERT INTO MapEvents (EventID, MapID, EventType, EventName, Description, CoordinateX, CoordinateY, IsActive, RequiredLevel)
VALUES 
(1, 1, 'NPC', 'Guardabosque', 'Un guardabosque amable que te enseña sobre el combate', 10, 10, 1, 1),
(2, 1, 'Treasure', 'Cofre Escondido', 'Un cofre con tesoros del bosque antiguo', 50, 50, 1, 3),
(3, 2, 'Boss', 'Jefe Caverna', 'El guardián de la Caverna Oscura', 40, 40, 1, 5),
(4, 3, 'Hazard', 'Tormenta Mágica', 'Una tormenta mágica que causa daño constante', 75, 75, 1, 8),
(5, 4, 'Boss', 'Señor del Volcán', 'Un poderoso elemental del fuego', 50, 50, 1, 15),
(6, 5, 'Boss', 'Rey Mago Supremo', 'El gobernante del castillo y el enemigo final', 75, 75, 0, 20);
