using System;

class Program
{
    static void Main()
    {
        // Crear un Guerrero nivel 1
        var guerrero = new PlayerCharacter("Kaito", "Guerrero", 150, 12, 15, 0);

        Console.WriteLine("=== EJEMPLO DE USO: PlayerCharacter ===\n");
        Console.WriteLine($"Personaje: {guerrero.PlayerName} ({guerrero.ClassName})");
        Console.WriteLine($"Nivel: {guerrero.Level} | HP: {guerrero.MaxHP} | ATK: {guerrero.Attack} | DEF: {guerrero.Defense}\n");

        // Subir a nivel 20 (gana 19 puntos de atributo)
        Console.WriteLine("--- Subiendo de nivel ---");
        for (int i = 0; i < 19; i++) 
        {
            guerrero.LevelUp();
        }

        Console.WriteLine($"\nPuntos disponibles: {guerrero.UnspentAttributePoints}\n");

        // Gastar puntos de atributo
        Console.WriteLine("--- Gastando puntos de atributo ---");
        guerrero.SpendAttributePoint(AttributeType.Vitalidad);
        guerrero.SpendAttributePoint(AttributeType.Fuerza);
        guerrero.SpendAttributePoint(AttributeType.Fuerza);
        guerrero.SpendAttributePoint(AttributeType.Agilidad);
        guerrero.SpendAttributePoint(AttributeType.Destreza);

        Console.WriteLine($"\n--- Stats Finales ---");
        Console.WriteLine($"Nivel: {guerrero.Level}");
        Console.WriteLine($"HP: {guerrero.MaxHP}");
        Console.WriteLine($"ATK: {guerrero.Attack}");
        Console.WriteLine($"DEF: {guerrero.Defense}");
        Console.WriteLine($"MAG: {guerrero.Magic}");
        Console.WriteLine($"Puntos disponibles: {guerrero.UnspentAttributePoints}\n");

        // Ganar dinero y probar Purificación de Tinta
        Console.WriteLine("--- Mecánica: Purificación de Tinta ---");
        guerrero.AddRyos(1500);
        guerrero.TryPurifyInk();
        
        Console.WriteLine($"\nDespués de Purificación:");
        Console.WriteLine($"HP: {guerrero.MaxHP}");
        Console.WriteLine($"ATK: {guerrero.Attack}");
        Console.WriteLine($"DEF: {guerrero.Defense}");
        Console.WriteLine($"Puntos disponibles: {guerrero.UnspentAttributePoints}");
    }
}
