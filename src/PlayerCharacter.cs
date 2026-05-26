using System;

public enum AttributeType
{
    Fuerza,      // Sube Attack
    Agilidad,    // Sube Attack y un poco Defense/Evasion
    Vitalidad,   // Sube MaxHP
    Espíritu,    // Sube MAG y MP si lo agregas
    Destreza     // Sube Critico y Attack
}

public class PlayerCharacter
{
    public string PlayerName { get; private set; }
    public string ClassName { get; private set; }
    public int Level { get; private set; }
    public int GoldRyos { get; private set; }
    
    // Stats finales
    public int MaxHP { get; private set; }
    public int Attack { get; private set; }
    public int Defense { get; private set; }
    public int Magic { get; private set; }
    
    // Atributos distribuidos
    public int Fuerza { get; private set; }
    public int Agilidad { get; private set; }
    public int Vitalidad { get; private set; }
    public int Espíritu { get; private set; }
    public int Destreza { get; private set; }
    
    // Puntos y reset
    public int UnspentAttributePoints { get; private set; }
    public bool HasUsedInkPurification { get; private set; }
    
    // Evolución
    public int EvolutionID { get; private set; }
    public string EvolutionName { get; private set; }

    // Stats base de la clase
    private int baseHP, baseATK, baseDEF, baseMAG;
    private int bonusHP, bonusATK, bonusDEF, bonusMAG;
    private decimal vitMult, strMult, agiAtkMult, agiDefMult, sprMult;

    public PlayerCharacter(string name, string className, int baseHP, int baseATK, int baseDEF, int baseMAG)
    {
        PlayerName = name;
        ClassName = className;
        Level = 1;
        GoldRyos = 0;
        UnspentAttributePoints = 0;
        HasUsedInkPurification = false;
        EvolutionID = 0;
        EvolutionName = "Ninguna";
        
        this.baseHP = baseHP;
        this.baseATK = baseATK;
        this.baseDEF = baseDEF;
        this.baseMAG = baseMAG;
        
        // Multiplicadores por defecto (sin evolución)
        this.vitMult = 10m;
        this.strMult = 2m;
        this.agiAtkMult = 1m;
        this.agiDefMult = 0.5m;
        this.sprMult = 2m;
        
        RecalculateStats();
    }

    public void LevelUp()
    {
        if (Level >= 20) return;
        Level++;
        UnspentAttributePoints++;
        Console.WriteLine($"{PlayerName} subió a nivel {Level}. Punto de atributo ganado.");
    }

    public bool SpendAttributePoint(AttributeType stat)
    {
        if (UnspentAttributePoints <= 0)
        {
            Console.WriteLine("No tienes puntos sin gastar.");
            return false;
        }

        switch (stat)
        {
            case AttributeType.Fuerza: Fuerza++; break;
            case AttributeType.Agilidad: Agilidad++; break;
            case AttributeType.Vitalidad: Vitalidad++; break;
            case AttributeType.Espíritu: Espíritu++; break;
            case AttributeType.Destreza: Destreza++; break;
        }
        
        UnspentAttributePoints--;
        RecalculateStats();
        Console.WriteLine($"{stat} aumentado. Puntos restantes: {UnspentAttributePoints}");
        return true;
    }

    public void Evolve(int evolutionID, string evolutionName, 
                       int bonusHP, int bonusATK, int bonusDEF, int bonusMAG,
                       decimal vitMult, decimal strMult, decimal agiAtkMult, decimal agiDefMult, decimal sprMult)
    {
        if (Level < 20)
        {
            Console.WriteLine("Debes llegar a nivel 20 para evolucionar.");
            return;
        }
        if (EvolutionID != 0)
        {
            Console.WriteLine("Ya has evolucionado.");
            return;
        }

        EvolutionID = evolutionID;
        EvolutionName = evolutionName;
        this.bonusHP = bonusHP;
        this.bonusATK = bonusATK;
        this.bonusDEF = bonusDEF;
        this.bonusMAG = bonusMAG;
        this.vitMult = vitMult;
        this.strMult = strMult;
        this.agiAtkMult = agiAtkMult;
        this.agiDefMult = agiDefMult;
        this.sprMult = sprMult;

        RecalculateStats();
        Console.WriteLine($"{PlayerName} evolucionó a {EvolutionName}!");
    }

    private void RecalculateStats()
    {
        int hpFromVit = (int)(Vitalidad * vitMult);
        int atkFromStr = (int)(Fuerza * strMult);
        int atkFromAgi = (int)(Agilidad * agiAtkMult);
        int atkFromDex = Destreza * 1;
        int defFromAgi = (int)(Agilidad * agiDefMult);
        int magFromSpr = (int)(Espíritu * sprMult);

        MaxHP = baseHP + bonusHP + hpFromVit;
        Attack = baseATK + bonusATK + atkFromStr + atkFromAgi + atkFromDex;
        Defense = baseDEF + bonusDEF + defFromAgi;
        Magic = baseMAG + bonusMAG + magFromSpr;
    }

    public void AddRyos(int amount)
    {
        GoldRyos += amount;
        Console.WriteLine($"{PlayerName} obtuvo {amount} Ryos. Total: {GoldRyos}");
    }

    public bool TryPurifyInk()
    {
        int purificationCost = 1500;
        if (HasUsedInkPurification)
        {
            Console.WriteLine("Ya has utilizado la Purificación de Tinta.");
            return false;
        }
        if (GoldRyos < purificationCost)
        {
            Console.WriteLine($"Fondos insuficientes. Necesitas {purificationCost} Ryos.");
            return false;
        }

        GoldRyos -= purificationCost;
        HasUsedInkPurification = true;
        UnspentAttributePoints = Level - 1; // Devuelve 19 puntos en nivel 20
        
        // Reset atributos
        Fuerza = Agilidad = Vitalidad = Espíritu = Destreza = 0;
        RecalculateStats();
        
        Console.WriteLine($"Purificación exitosa. {UnspentAttributePoints} puntos restablecidos.");
        return true;
    }
}
