-- Insertando los datos de Nivel 1 del Manual Maestro
INSERT INTO BaseClasses (ClassID, ClassName, BaseHP, BaseATK, BaseDEF, BaseMAG)
VALUES 
(1, 'Guerrero', 150, 12, 15, 0),
(2, 'Mago', 70, 0, 5, 18),
(3, 'Arquero', 100, 15, 8, 0);

-- Insertando ítems clave de la economía
INSERT INTO Items (ItemID, ItemName, ItemType, CostRyos, IsSoulbound)
VALUES
(100, 'Poción de Supervivencia', 'Consumible', 25, 0),
(200, 'Hoja Espectral del Otoño', 'Material Forja', 0, 1),
(201, 'Acero Tamahagane Puro', 'Material Forja', 500, 0);