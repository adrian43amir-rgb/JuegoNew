using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== SIMULACIÓN DE MECÁNICAS EN TIEMPO REAL ===\n");

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

        // Mostrar stats en tiempo real
        Console.WriteLine("\n========== MECÁNICAS EN TIEMPO REAL ==========\n");
        MostrarStatsRealtime("GUERRERO - TANQUE", guerrero);
        MostrarStatsRealtime("MAGO - SOPORTE", mago);
        MostrarStatsRealtime("ARQUERO - TIRADOR", arquero);

        // Simulación de combate
        Console.WriteLine("\n========== SIMULACIÓN DE COMBATE ==========\n");
        SimularCombate(guerrero, arquero, 5f); // 5 segundos de simulación

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

    static void MostrarStatsRealtime(string nombre, PlayerCharacter personaje)
    {
        Console.WriteLine($"\n{nombre} (Tiempo Real):");
        Console.WriteLine($"  Velocidad de Movimiento: {personaje.MoveSpeed:F2} unidades/seg");
        Console.WriteLine($"  Velocidad de Ataque: {personaje.AttackSpeed:F2} ataques/seg");
        Console.WriteLine($"  Cadencia de Ataque: {1f / personaje.AttackSpeed:F2} segundos entre ataques");
    }

    static void SimularCombate(PlayerCharacter atacante, PlayerCharacter defensor, float duracionSimulacion)
    {
        Console.WriteLine($"\n--- Combate: {atacante.PlayerName} ({atacante.EvolutionName}) vs {defensor.PlayerName} ({defensor.EvolutionName}) ---");
        Console.WriteLine($"Duración simulada: {duracionSimulacion} segundos\n");

        float tiempoTranscurrido = 0f;
        float deltaTime = 0.1f; // 100ms por frame
        float lastAttackTime = 0f;
        int ataquesContador = 0;

        while (tiempoTranscurrido < duracionSimulacion)
        {
            // Verificar si es momento de atacar
            if (tiempoTranscurrido > lastAttackTime + (1f / atacante.AttackSpeed))
            {
                ataquesContador++;
                int daño = Math.Max(1, atacante.Attack - (defensor.Defense / 2));
                Console.WriteLine($"[{tiempoTranscurrido:F1}s] {atacante.PlayerName} ataca a {defensor.PlayerName}. Daño: {daño}");
                lastAttackTime = tiempoTranscurrido;
            }

            // Simular movimiento
            float distanciaRecorrida = atacante.MoveSpeed * deltaTime;
            if (ataquesContador % 5 == 0 && ataquesContador > 0)
            {
                Console.WriteLine($"[{tiempoTranscurrido:F1}s] {atacante.PlayerName} se mueve {distanciaRecorrida:F2} unidades");
            }

            tiempoTranscurrido += deltaTime;
        }

        Console.WriteLine($"\n--- Resumen del Combate ---");
        Console.WriteLine($"Total de ataques realizados: {ataquesContador}");
        Console.WriteLine($"Velocidad de ataque promedio: {ataquesContador / duracionSimulacion:F2} ataques/seg");
    }
}
