"""
gerar_receitas_runas.py — Gera 105 receitas de runas/upgrades + arquivos lang.
Rodar na raiz do BP. Requer apenas Python padrão (sem Pillow).
"""
import os, json

NS = "mod_rpg_rune"

# ═══════════════════════════════════════════════════════
# MATERIAIS TEMÁTICOS POR TIPO
# ═══════════════════════════════════════════════════════

MATERIAIS = {
    # Runas de arma
    "vampirism":       "minecraft:redstone",
    "soul_fire":       "minecraft:blaze_powder",
    "decomposition":   "minecraft:rotten_flesh",
    "poison":          "minecraft:spider_eye",
    "bleeding":        "minecraft:flint",
    "freezing":        "minecraft:packed_ice",
    "lightning":       "minecraft:copper_ingot",
    "fissure":         "minecraft:cobblestone",
    "echo":            "minecraft:ender_pearl",
    # Runas de armadura
    "purification":    "minecraft:sugar",
    "sylvan":          "minecraft:oak_sapling",
    "seismic":         "minecraft:gunpowder",
    # Runas de arco
    "tempest":         "minecraft:feather",
    "flame_lightning": "minecraft:blaze_powder",
    "glacial":         "minecraft:packed_ice",
    "void":            "minecraft:ender_pearl",
    "crimson":         "minecraft:redstone",
    "putrid":          "minecraft:spider_eye",
    "zephyr":          "minecraft:phantom_membrane",
    "dawn":            "minecraft:glowstone_dust",
    "earthquake":      "minecraft:gunpowder",
    # Runas de escudo
    "bastion":         "minecraft:iron_block",
    "counter":         "minecraft:flint",
    "mirror":          "minecraft:glass",
    # Upgrades
    "vitality":        "minecraft:golden_apple",
    "resistance":      "minecraft:turtle_scute",
    "permanent_damage":"minecraft:diamond",
    "unbreaking":      "minecraft:obsidian",
    "efficiency":      "minecraft:redstone_block",
    "projectile_damage":"minecraft:arrow",
    "reload_speed":    "minecraft:sugar",
    "projectile_speed":"minecraft:feather",
    "block_absorption":"minecraft:iron_block",
    "steady_guard":    "minecraft:slime_ball",
    "guard_recovery":  "minecraft:string",
}

# Núcleo comum por categoria
NUCLEO = {
    "weapon":  "minecraft:iron_ingot",
    "armor":   "minecraft:iron_ingot",
    "bow":     "minecraft:string",
    "shield":  "minecraft:iron_ingot",
    "upgrade": "minecraft:iron_ingot",
}

# Tipo → categoria
CATEGORIA = {
    "vampirism":"weapon","soul_fire":"weapon","decomposition":"weapon","poison":"weapon",
    "bleeding":"weapon","freezing":"weapon","lightning":"weapon","fissure":"weapon","echo":"weapon",
    "purification":"armor","sylvan":"armor","seismic":"armor",
    "tempest":"bow","flame_lightning":"bow","glacial":"bow","void":"bow","crimson":"bow",
    "putrid":"bow","zephyr":"bow","dawn":"bow","earthquake":"bow",
    "bastion":"shield","counter":"shield","mirror":"shield",
    "vitality":"upgrade","resistance":"upgrade","permanent_damage":"upgrade","unbreaking":"upgrade",
    "efficiency":"upgrade","projectile_damage":"upgrade","reload_speed":"upgrade",
    "projectile_speed":"upgrade","block_absorption":"upgrade","steady_guard":"upgrade",
    "guard_recovery":"upgrade",
}

# Upgrades usam prefixo "upgrade_", o resto "runa_"
UPGRADES = {"vitality","resistance","permanent_damage","unbreaking","efficiency",
            "projectile_damage","reload_speed","projectile_speed",
            "block_absorption","steady_guard","guard_recovery"}

def prefixo(tipo):
    return "upgrade" if tipo in UPGRADES else "runa"

# Nomes PT
NOMES_PT = {
    "vampirism": "Runa de Vampirismo",
    "soul_fire": "Runa de Fogo das Almas",
    "decomposition": "Runa de Decomposição",
    "poison": "Runa de Veneno",
    "bleeding": "Runa de Sangramento",
    "freezing": "Runa de Congelamento",
    "lightning": "Runa Relampejante",
    "fissure": "Runa de Fissura",
    "echo": "Runa de Eco",
    "purification": "Runa de Purificação",
    "sylvan": "Runa Silvestre",
    "seismic": "Runa Sísmica",
    "tempest": "Runa de Tempestade",
    "flame_lightning": "Runa de Chamas Raio",
    "glacial": "Runa Glacial",
    "void": "Runa do Vazio",
    "crimson": "Runa Carmesim",
    "putrid": "Runa Pútrida",
    "zephyr": "Runa do Zéfiro",
    "dawn": "Runa da Alvorada",
    "earthquake": "Runa de Terremoto",
    "bastion": "Runa de Bastião",
    "counter": "Runa de Contragolpe",
    "mirror": "Runa de Espelho",
    "vitality": "Upgrade de Vitalidade",
    "resistance": "Upgrade de Resistência",
    "permanent_damage": "Upgrade de Dano Permanente",
    "unbreaking": "Upgrade Inquebrável",
    "efficiency": "Upgrade de Eficiência",
    "projectile_damage": "Upgrade de Dano Projétil",
    "reload_speed": "Upgrade de Vel. Recarga",
    "projectile_speed": "Upgrade de Vel. Projétil",
    "block_absorption": "Upgrade de Absorção de Bloqueio",
    "steady_guard": "Upgrade de Guarda Firme",
    "guard_recovery": "Upgrade de Recuperação de Guarda",
}

# Nomes EN
NOMES_EN = {
    "vampirism": "Vampirism Rune",
    "soul_fire": "Soul Fire Rune",
    "decomposition": "Decomposition Rune",
    "poison": "Poison Rune",
    "bleeding": "Bleeding Rune",
    "freezing": "Freezing Rune",
    "lightning": "Lightning Rune",
    "fissure": "Fissure Rune",
    "echo": "Echo Rune",
    "purification": "Purification Rune",
    "sylvan": "Sylvan Rune",
    "seismic": "Seismic Rune",
    "tempest": "Tempest Rune",
    "flame_lightning": "Flame Lightning Rune",
    "glacial": "Glacial Rune",
    "void": "Void Rune",
    "crimson": "Crimson Rune",
    "putrid": "Putrid Rune",
    "zephyr": "Zephyr Rune",
    "dawn": "Dawn Rune",
    "earthquake": "Earthquake Rune",
    "bastion": "Bastion Rune",
    "counter": "Counter Rune",
    "mirror": "Mirror Rune",
    "vitality": "Vitality Upgrade",
    "resistance": "Resistance Upgrade",
    "permanent_damage": "Permanent Damage Upgrade",
    "unbreaking": "Unbreaking Upgrade",
    "efficiency": "Efficiency Upgrade",
    "projectile_damage": "Projectile Damage Upgrade",
    "reload_speed": "Reload Speed Upgrade",
    "projectile_speed": "Projectile Speed Upgrade",
    "block_absorption": "Block Absorption Upgrade",
    "steady_guard": "Steady Guard Upgrade",
    "guard_recovery": "Guard Recovery Upgrade",
}

ROMANOS = {1: "I", 2: "II", 3: "III"}

# ═══════════════════════════════════════════════════════
# GERAÇÃO DAS RECEITAS
# ═══════════════════════════════════════════════════════

os.makedirs("recipes", exist_ok=True)

def gravar(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

total_receitas = 0

for tipo, material in MATERIAIS.items():
    cat = CATEGORIA[tipo]
    nucleo = NUCLEO[cat]
    pref = prefixo(tipo)
    base = f"{pref}_{tipo}"

    # ─── T1: shaped (cruz) ───
    gravar(f"recipes/{base}_1.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shaped": {
            "description": {"identifier": f"{NS}:{base}_1"},
            "tags": ["crafting_table"],
            "pattern": [
                " A ",
                "ABA",
                " A "
            ],
            "key": {
                "A": {"item": material},
                "B": {"item": nucleo}
            },
            "result": {"item": f"{NS}:{base}_1", "count": 1}
        }
    })
    total_receitas += 1

    # ─── T2: shapeless (2× T1) ───
    gravar(f"recipes/{base}_2.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shapeless": {
            "description": {"identifier": f"{NS}:{base}_2"},
            "tags": ["crafting_table"],
            "ingredients": [
                {"item": f"{NS}:{base}_1"},
                {"item": f"{NS}:{base}_1"}
            ],
            "result": {"item": f"{NS}:{base}_2", "count": 1}
        }
    })
    total_receitas += 1

    # ─── T3: shapeless (2× T2) ───
    gravar(f"recipes/{base}_3.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shapeless": {
            "description": {"identifier": f"{NS}:{base}_3"},
            "tags": ["crafting_table"],
            "ingredients": [
                {"item": f"{NS}:{base}_2"},
                {"item": f"{NS}:{base}_2"}
            ],
            "result": {"item": f"{NS}:{base}_3", "count": 1}
        }
    })
    total_receitas += 1

print(f"✅ {total_receitas} receitas geradas em recipes/")

# ═══════════════════════════════════════════════════════
# LANG (pt_BR + en_US)
# ═══════════════════════════════════════════════════════

os.makedirs("../RP/texts", exist_ok=True)

MARKER_PT = "# === RUNAS E UPGRADES ==="
MARKER_EN = "# === RUNES AND UPGRADES ==="

lines_pt = [f"\n{MARKER_PT}\n"]
lines_en = [f"\n{MARKER_EN}\n"]

for tipo in MATERIAIS.keys():
    pref = prefixo(tipo)
    for tier in [1, 2, 3]:
        item_id = f"{pref}_{tipo}_{tier}"
        nome_pt = f"{NOMES_PT[tipo]} {ROMANOS[tier]}"
        nome_en = f"{NOMES_EN[tipo]} {ROMANOS[tier]}"
        lines_pt.append(f"item.{NS}:{item_id}={nome_pt}\n")
        lines_en.append(f"item.{NS}:{item_id}={nome_en}\n")

def anexar_lang(path, marker, lines):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        if marker in conteudo:
            print(f"⏭️  {path} já contém as entradas — pulando")
            return
        with open(path, "a", encoding="utf-8") as f:
            f.writelines(lines)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    print(f"✅ {path} atualizado")

anexar_lang("../RP/texts/pt_BR.lang", MARKER_PT, lines_pt)
anexar_lang("../RP/texts/en_US.lang", MARKER_EN, lines_en)

# ═══════════════════════════════════════════════════════
# SUMÁRIO
# ═══════════════════════════════════════════════════════

print("\n🎉 Concluído!")
print(f"\n📁 Arquivos criados/atualizados:")
print(f"   BP/recipes/          → {total_receitas} arquivos (.json)")
print(f"   RP/texts/pt_BR.lang  → 105 entradas")
print(f"   RP/texts/en_US.lang  → 105 entradas")
print(f"\n⚠️  Não se esqueça de rodar /reload no jogo")
print(f"⚠️  Se as receitas não aparecerem no creative, use /reload uma segunda vez")
