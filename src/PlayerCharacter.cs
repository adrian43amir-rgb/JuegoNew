using System;

public class PlayerCharacter
{
    public string PlayerName { get; private set; }
    public int Level { get; private set; }
    public int GoldRyos { get; private set; }
    
    // Estadísticas
    public int MaxHP { get; private set; }
    public int Attack { get; private set; }
    public int Defense { get; private set; }
    
    // Puntos de estatus y mecánica de reinicio
    public int UnspentAttributePoints { get; private set; }
    public bool HasUsedInkPurification { get; private set; } // Solo se puede usar una vez

    public PlayerCharacter(string name, int baseHP, int baseATK, int baseDEF)
    {
        PlayerName = name;
        Level = 1;
        GoldRyos = 0;
        MaxHP = baseHP;
        Attack = baseATK;
        Defense = baseDEF;
        UnspentAttributePoints = 0;
        HasUsedInkPurification = false;
    }

    // Método para ganar botín (Ej: derrotar a Kuroshiko da 500-1000 Ryos)
    public void AddRyos(int amount)
    {
        GoldRyos += amount;
        Console.WriteLine($"{PlayerName} obtuvo {amount} Ryos de Oro. Total: {GoldRyos}");
    }

    // Mecánica: Purificación de Tinta
    public bool TryPurifyInk()
    {
        int purificationCost = 1500; // Costo de 1,500 Ryos

        if (HasUsedInkPurification)
        {
            Console.WriteLine("El destino solo se reescribe una vez con la misma tinta... Ya has utilizado este servicio.");
            return false;
        }

        if (GoldRyos >= purificationCost)
        {
            GoldRyos -= purificationCost;
            HasUsedInkPurification = true;
            
            // Lógica de reinicio: Devolver 19 puntos (Nivel 20) al jugador
            UnspentAttributePoints = (Level - 1); 
            
            Console.WriteLine($"Purificación exitosa. Se han deducido {purificationCost} Ryos. Puntos restablecidos.");
            return true;
        }
        else
        {
            Console.WriteLine($"Fondos insuficientes. Necesitas {purificationCost} Ryos de Oro.");
            return false;
        }
    }
}
