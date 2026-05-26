using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== EJEMPLO COMPLETO: EVOLUCIONES DE CLASES ===\n");

        // Crear personajes de las tres clases base
        var guerrero = new PlayerCharacter("Kaito", "Guerrero", 150, 12, 15, 0);
        var mago = new PlayerCharacter("Yuki", "Mago", 70, 0, 5, 18);
        var arquero = new PlayerCharacter("Takeshi", "Arquero", 100, 15, 8, 0);

        // Subir todos a nivel 20
        Console.WriteLine("--- Subiendo personajes a nivel 20 ---\n");
        for (int i = 0; i < 19; i++)
        {
            guerrero.LevelUp();
            mago.LevelUp();
            arquero.LevelUp();
        }

        // Distribuir atributos para cada personaje
        Console.WriteLine("\n--- Distribuyendo atributos ---\n");

        // Guerrero (enfocado en Vitalidad y Fuerza)
        for (int i = 0; i < 10; i++) guerrero.SpendAttributePoint(AttributeType.Vitalidad);
        for (int i = 0; i < 5; i++) guerrero.SpendAttributePoint(AttributeType.Fuerza);
        for (int i = 0; i < 4; i++) guerrero.SpendAttributePoint(AttributeType.Agilidad);

        // Mago (enfocado en Espíritu)
        for (int i = 0; i < 12; i++) mago.SpendAttributePoint(AttributeType.Espíritu);
        for (int i = 0; i < 5; i++) mago.SpendAttributePoint(AttributeType.Vitalidad);
        for (int i = 0; i < 2; i++) mago.SpendAttributePoint(AttributeType.Agilidad);

        // Arquero (enfocado en Agilidad y Destreza)
        for (int i = 0; i < 8; i++) arquero.SpendAttributePoint(AttributeType.Agilidad);
        for (int i = 0; i < 7; i++) arquero.SpendAttributePoint(AttributeType.Destreza);
        for (int i = 0; i < 4; i++) arquero.SpendAttributePoint(AttributeType.Fuerza);

        // Mostrar stats antes de evolución
        Console.WriteLine("\n========== ANTES DE EVOLUCIONAR ==========\n");
        MostrarStats("GUERRERO", guerrero);
        MostrarStats("MAGO", mago);
        MostrarStats("ARQUERO", arquero);

        // Aplicar evoluciones
        Console.WriteLine("\n========== EVOLUCIONES ==========\n");

        // Tanque
        Console.WriteLine("--- Guerrero evoluciona a TANQUE ---");
        guerrero.Evolve(1, "Tanque", 750, 0, 105, 0, 10.0m, 2.0m, 1.0m, 0.5m, 2.0m);

        // Tirador
        Console.WriteLine("\n--- Arquero evoluciona a TIRADOR ---");
        arquero.Evolve(6, "Tirador", 0, 115, 0, 0, 10.0m, 2.0m, 1.0m, 0.5m, 2.0m);

        // Soporte
        Console.WriteLine("\n--- Mago evoluciona a SOPORTE ---");
        mago.Evolve(4, "Soporte", 380, 0, 0, 72, 10.0m, 2.0m, 1.0m, 0.5m, 2.0m);

        // Mostrar stats después de evolución
        Console.WriteLine("\n========== DESPUÉS DE EVOLUCIONAR ==========\n");
        MostrarStats("GUERRERO - TANQUE", guerrero);
        MostrarStats("MAGO - SOPORTE", mago);
        MostrarStats("ARQUERO - TIRADOR", arquero);

        // Intentar evolucionar de nuevo (debe fallar)
        Console.WriteLine("\n--- Intento de doble evolución (debe fallar) ---");
        guerrero.Evolve(2, "DPS", 0, 73, 0, 0, 10.0m, 2.0m, 1.0m, 0.5m, 2.0m);
    }

    static void MostrarStats(string nombre, PlayerCharacter personaje)
    {
        Console.WriteLine($"\n{nombre}:");
        Console.WriteLine($"  Nivel: {personaje.Level}");
        Console.WriteLine($"  Evolución: {personaje.EvolutionName}");
        Console.WriteLine($"  HP: {personaje.MaxHP}");
        Console.WriteLine($"  ATK: {personaje.Attack}");
        Console.WriteLine($"  DEF: {personaje.Defense}");
        Console.WriteLine($"  MAG: {personaje.Magic}");
        Console.WriteLine($"  Atributos - FUE:{personaje.Fuerza} AGI:{personaje.Agilidad} VIT:{personaje.Vitalidad} ESP:{personaje.Espíritu} DES:{personaje.Destreza}");
    }
}
