"""
gerar_texturas.py — Gera TODAS as texturas 16×16 do mod (armas, paxels, ferramentas, aço, runas, upgrades).
Rodar na raiz do Resource Pack (RP/).
Requer: pip install Pillow
"""
from PIL import Image
import os, json

SIZE = 16

# ═══════════════════════════════════════════════════════════
# PALETAS
# ═══════════════════════════════════════════════════════════

PALETAS_MATERIAL = {
    "madeira":   {"base": (139, 90, 43),  "dark": (75, 50, 25),   "light": (185, 135, 85)},
    "pedra":     {"base": (130, 130, 130),"dark": (75, 75, 75),   "light": (175, 175, 175)},
    "ouro":      {"base": (252, 217, 40), "dark": (180, 145, 20), "light": (255, 245, 130)},
    "cobre":     {"base": (216, 127, 51), "dark": (150, 80, 25),  "light": (255, 180, 130)},
    "ferro":     {"base": (216, 216, 216),"dark": (140, 140, 140),"light": (245, 245, 245)},
    "aco":       {"base": (140, 155, 175),"dark": (75, 90, 110),  "light": (190, 205, 225)},
    "netherite": {"base": (80, 65, 75),   "dark": (45, 35, 45),   "light": (120, 100, 115)},
}
HANDLE      = (110, 75, 45)
HANDLE_DARK = (65, 40, 20)

PALETAS_CATEGORIA = {
    "weapon":  {"base": (170, 50, 50),  "light": (255, 220, 100)},
    "armor":   {"base": (90, 170, 90),  "light": (255, 255, 220)},
    "bow":     {"base": (210, 170, 40), "light": (150, 220, 255)},
    "shield":  {"base": (140, 85, 85),  "light": (255, 180, 180)},
    "upgrade": {"base": (70, 150, 200), "light": (200, 240, 255)},
}

# ═══════════════════════════════════════════════════════════
# PADRÕES DAS ARMAS (16x16)
# Legendas: X=base  x=dark  L=light  H=cabo  h=cabo escuro  .=vazio
# ═══════════════════════════════════════════════════════════

PATTERNS_ARMAS = {
    "espada_longa": [
        "..............LL",
        ".............LXX",
        "............XX..",
        "...........XX...",
        "..........XX....",
        ".........XX.....",
        "........XX......",
        ".......XX.......",
        "......XX........",
        ".....XX.........",
        "....xXXx........",
        "...hHHHh........",
        "....HhH.........",
        "....H.H.........",
        "...h..h.........",
        "................",
    ],
    "katana": [
        "...............L",
        "..............LL",
        ".............XX.",
        "............XX..",
        "...........XX...",
        "..........XX....",
        ".........XX.....",
        "........XX......",
        ".......XX.......",
        "......XX........",
        ".....XX.........",
        "....xXx.........",
        "...hHHh.........",
        "....Hh..........",
        "...h.h..........",
        "................",
    ],
    "adaga": [
        "................",
        "................",
        "................",
        "................",
        "..............L.",
        ".............LX.",
        "............XX..",
        "...........XX...",
        "..........XX....",
        ".........XX.....",
        "........xXx.....",
        ".......hHHh.....",
        "........Hh......",
        ".......h........",
        "................",
        "................",
    ],
    "hari": [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "....LLLLLHHh....",
        "....XXXXXHhh....",
        "....xxxxx.......",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
    ],
    "dragon_slayer": [
        "..............LL",
        ".............LXX",
        "............XXX.",
        "...........XXX..",
        "..........XXX...",
        ".........XXX....",
        "........XXX.....",
        ".......XXX......",
        "......XXX.......",
        ".....XXX........",
        "....xXXx........",
        "...hHHHh........",
        "..h.HhH.h.......",
        "....H.H.........",
        "...h...h........",
        "................",
    ],
    "machado_tatico": [
        "................",
        "................",
        "................",
        ".....xxxxx......",
        "....xLLXXXx.....",
        "....xLXXXXx.....",
        "....xXXXXXx.....",
        ".....xXXXx......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "machado_de_batalha": [
        "................",
        "..xxx...xxx.....",
        ".xLLXx.xLLXx....",
        ".xLXXXxLXXXXx...",
        ".xXXXXXXXXXXXx..",
        ".xXXXXxXXXXXXx..",
        ".xxxxx.xxxxxx...",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "paxel": [
        ".....xxxx.......",
        "....xLLXXx..xxx.",
        "....xLXXXx.xLLx.",
        "....xXXXXx.xxxx.",
        ".....xXXx.xXXXx.",
        "......hHh.xXXXx.",
        "......hHh.xxxx..",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "aco_pickaxe": [
        "................",
        "...xxxxxxxx.....",
        "..xLLXXLLXXx....",
        "..xLXXXXXXXx....",
        "...xXXXXXXx.....",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "aco_axe": [
        "................",
        "................",
        "................",
        "................",
        "......hHh.......",
        "..xxxxhHh.......",
        ".xLLXXhHh.......",
        ".xLXXXhHh.......",
        ".xXXXXhHh.......",
        "..xXXXhHh.......",
        "...xxxhHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "aco_shovel": [
        "................",
        "................",
        "................",
        "................",
        "................",
        ".....xxxxx......",
        "....xLLXXXx.....",
        "....xXXXXXx.....",
        "....xXXXXXx.....",
        ".....xXXXx......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        "......hHh.......",
        ".....h.h.h......",
        "................",
    ],
    "aco_hoe": [
        "................",
        "................",
        "................",
        "................",
        "..xxxx..........",
        ".xLLXXx.........",
        ".xLXXXXx........",
        ".xXXXXXx........",
        "..xXXXx.hHh.....",
        "...xxx..hHh.....",
        "........hHh.....",
        "........hHh.....",
        "........hHh.....",
        "........hHh.....",
        ".......h.h.h....",
        "................",
    ],
    "aco_sword": [
        "..............LL",
        ".............LXX",
        "............XX..",
        "...........XX...",
        "..........XX....",
        ".........XX.....",
        "........XX......",
        ".......XX.......",
        "......XX........",
        ".....XX.........",
        "....xXXx........",
        "...hHHHh........",
        "....HhH.........",
        "....H.H.........",
        "...h..h.........",
        "................",
    ],
}

# ═══════════════════════════════════════════════════════════
# SÍMBOLOS DAS RUNAS/UPGRADES (7x7)
# ═══════════════════════════════════════════════════════════

SIMBOLOS = {
    # ── Weapon runas ──
    "vampirism":         ["...X...", "..XXX..", ".XXXXX.", ".XXXXX.", "..XXX..", "...X...", "......."],
    "soul_fire":         ["...X...", "..XXX..", "..XXX..", ".XXXXX.", ".XXXXX.", "..XXX..", "......."],
    "decomposition":     ["X..X..X", ".X..X..", "..X..X.", "X..X..X", ".X..X..", "..X..X.", "X..X..X"],
    "poison":            ["..X..X.", ".X..X..", "..X..X.", "X..X..X", ".X..X..", "..X..X.", "......."],
    "bleeding":          ["...X...", "..X.X..", "...X...", "..X.X..", "...X...", "..X.X..", "......."],
    "freezing":          ["X..X..X", ".X.X.X.", "..XXX..", "XXXXXXX", "..XXX..", ".X.X.X.", "X..X..X"],
    "lightning":         ["...XX..", "..XX...", ".XXXX..", "...XX..", "..XX...", ".XX....", "......."],
    "fissure":           ["...X...", "..X.X..", ".X.X.X.", "..X.X..", ".X.X.X.", "..X.X..", "...X..."],
    "echo":              ["XXXXXXX", "X.....X", "X.XXX.X", "X.X.X.X", "X.XXX.X", "X.....X", "XXXXXXX"],
    # ── Armor runas ──
    "purification":      ["...X...", "...X...", ".XXXXX.", "...X...", "...X...", "...X...", "......."],
    "sylvan":            ["...XX..", "..XXXX.", ".XXXXX.", ".XXXXX.", "..XXX..", "...X...", "......."],
    "seismic":           [".......", "XXX....", "...XXX.", "XXXXXXX", "...XXX.", "XXX....", "......."],
    # ── Bow runas ──
    "tempest":           [".XXXX..", "XXXXX..", ".XXXX..", "...XX..", "..XX...", ".XX....", "......."],
    "flame_lightning":   ["...X.X.", "..XX.X.", ".XX.X..", ".XXXX..", "...X...", "..XX...", "......."],
    "glacial":           ["...X...", "..XXX..", ".XXXXX.", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."],
    "void":              ["XXXXXXX", "X.....X", "X.....X", "X.....X", "X.....X", "X.....X", "XXXXXXX"],
    "crimson":           ["...X...", "..XXX..", ".XXXXX.", ".XXXXX.", ".XXXXX.", "..XXX..", "...X..."],
    "putrid":            [".XXXXX.", "XXXXXXX", "X.XXX.X", "XXXXXXX", "X.X.X.X", "XXXXXXX", ".XXXXX."],
    "zephyr":            ["XX.....", "X.XX...", "..X.X..", "...X.X.", "..X.X..", ".XX....", "......."],
    "dawn":              ["...X...", ".X.X.X.", "..XXX..", "XXXXXXX", "..XXX..", ".X.X.X.", "...X..."],
    "earthquake":        ["...X...", "..X.X..", "...X...", "XXXXXXX", "X.X.X.X", "XXXXXXX", "......."],
    # ── Shield runas ──
    "bastion":           ["XXXXXXX", "XXXXXXX", ".XXXXX.", ".XXXXX.", "..XXX..", "..XXX..", "...X..."],
    "counter":           ["...X...", "..XXX..", ".X.X.X.", "...X...", "..X.X..", "...X...", "......."],
    "mirror":            ["X..X..X", "XX.X.XX", "XXX.XXX", ".....X.", "XXX.XXX", "XX.X.XX", "X..X..X"],
    # ── Upgrades ──
    "vitality":          [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X...", "......."],
    "resistance":        ["XXXXXXX", "XXXXXXX", ".XXXXX.", ".XXXXX.", "..XXX..", "..XXX..", "...X..."],
    "permanent_damage":  ["...X...", "..XXX..", ".XX.XX.", "...X...", "...X...", "...X...", "......."],
    "unbreaking":        [".......", "XXXXXXX", "XXXXXXX", ".XXXXX.", ".XXXXX.", "XXXXXXX", "......."],
    "efficiency":        ["....X..", "...X...", "..X....", ".X...X.", "X...X..", "...X...", "......."],
    "projectile_damage": ["...X...", "..XXX..", ".XXXXX.", "X..X..X", "...X...", "...X...", "......."],
    "reload_speed":      ["X...X..", "XX.X...", ".XXX...", "..X....", ".XXX...", "XX.X...", "X...X.."],
    "projectile_speed":  ["X....X.", ".XX.XX.", "..X..X.", ".XX.XX.", "X....X.", ".......", "......."],
    "block_absorption":  ["XXXXXXX", "XXXXXXX", "XXXXXXX", ".XXXXX.", ".XXXXX.", "..XXX..", "...X..."],
    "steady_guard":      ["...X...", "...X...", ".XXXXX.", "...X...", "...X...", "..XXX..", "......."],
    "guard_recovery":    ["..XXX..", ".X...X.", "X..X..X", "X..X..X", "X..X..X", ".X...X.", "..XXX.."],
}

# Mapeamento: nome → categoria (para cor da gema)
CATEGORIA = {
    # Weapon
    "vampirism": "weapon", "soul_fire": "weapon", "decomposition": "weapon",
    "poison": "weapon", "bleeding": "weapon", "freezing": "weapon",
    "lightning": "weapon", "fissure": "weapon", "echo": "weapon",
    # Armor
    "purification": "armor", "sylvan": "armor", "seismic": "armor",
    # Bow
    "tempest": "bow", "flame_lightning": "bow", "glacial": "bow",
    "void": "bow", "crimson": "bow", "putrid": "bow", "zephyr": "bow",
    "dawn": "bow", "earthquake": "bow",
    # Shield
    "bastion": "shield", "counter": "shield", "mirror": "shield",
    # Upgrades
    "vitality": "upgrade", "resistance": "upgrade", "permanent_damage": "upgrade",
    "unbreaking": "upgrade", "efficiency": "upgrade", "projectile_damage": "upgrade",
    "reload_speed": "upgrade", "projectile_speed": "upgrade",
    "block_absorption": "upgrade", "steady_guard": "upgrade", "guard_recovery": "upgrade",
}

# Nomes que são upgrades (vão usar prefixo "upgrade_" no arquivo)
UPGRADES = {
    "vitality", "resistance", "permanent_damage", "unbreaking", "efficiency",
    "projectile_damage", "reload_speed", "projectile_speed",
    "block_absorption", "steady_guard", "guard_recovery",
}

# ═══════════════════════════════════════════════════════════
# FUNÇÕES DE DESENHO
# ═══════════════════════════════════════════════════════════

def draw_pattern(pattern, paleta):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            if ch == ".": continue
            if   ch == "X": c = paleta["base"]  + (255,)
            elif ch == "x": c = paleta["dark"]  + (255,)
            elif ch == "L": c = paleta["light"] + (255,)
            elif ch == "H": c = HANDLE          + (255,)
            elif ch == "h": c = HANDLE_DARK     + (255,)
            else: continue
            px[x, y] = c
    return img

def draw_runa(simbolo, categoria, tier):
    """Gema colorida + símbolo central + indicador de tier."""
    paleta = PALETAS_CATEGORIA[categoria]
    # Tiers mais brilhantes
    factor = 1.0 + 0.1 * (tier - 1)
    base  = tuple(min(255, int(c * factor)) for c in paleta["base"])
    light = paleta["light"]
    dark  = tuple(max(0, int(c * 0.55)) for c in paleta["base"])

    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()

    # Fundo gema (quadrado com cantos chanfrados)
    for y in range(2, 14):
        for x in range(2, 14):
            if x in (2, 13) and y in (2, 13): continue
            px[x, y] = base + (255,)

    # Borda escura
    for x in range(3, 13):
        px[x, 2]  = dark + (255,)
        px[x, 13] = dark + (255,)
    for y in range(3, 13):
        px[2, y]  = dark + (255,)
        px[13, y] = dark + (255,)

    # Símbolo 7x7 centralizado (offset 4,4)
    for sy, row in enumerate(simbolo):
        for sx, ch in enumerate(row):
            if ch == "X":
                px[4 + sx, 4 + sy] = light + (255,)

    # Indicador de tier (pontinhos no topo esquerdo)
    for i in range(tier):
        px[3 + i * 2, 3] = (255, 255, 255, 255)

    return img

def draw_ingot(paleta):
    """Lingote (usado para aco_ingot)."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()
    base, dark, light = paleta["base"], paleta["dark"], paleta["light"]
    for y in range(6, 12):
        for x in range(3, 13):
            px[x, y] = base + (255,)
    for x in range(3, 13):
        px[x, 6]  = dark + (255,)
        px[x, 11] = dark + (255,)
    for y in range(6, 12):
        px[3, y]  = dark + (255,)
        px[12, y] = dark + (255,)
    for x in range(5, 10):
        px[x, 7] = light + (255,)
    return img

# ═══════════════════════════════════════════════════════════
# GERAÇÃO
# ═══════════════════════════════════════════════════════════

os.makedirs("textures/items", exist_ok=True)

# 1. Armas (7 tipos × 7 materiais = 49)
for arma in ["katana", "adaga", "espada_longa", "hari",
             "machado_tatico", "machado_de_batalha", "dragon_slayer"]:
    for mat, pal in PALETAS_MATERIAL.items():
        img = draw_pattern(PATTERNS_ARMAS[arma], pal)
        img.save(f"textures/items/{arma}_{mat}.png")

# 2. Paxels (7)
for mat, pal in PALETAS_MATERIAL.items():
    img = draw_pattern(PATTERNS_ARMAS["paxel"], pal)
    img.save(f"textures/items/paxel_{mat}.png")

# 3. Ferramentas de aço (5)
for ferr in ["aco_pickaxe", "aco_axe", "aco_shovel", "aco_hoe", "aco_sword"]:
    img = draw_pattern(PATTERNS_ARMAS[ferr], PALETAS_MATERIAL["aco"])
    img.save(f"textures/items/{ferr}.png")

# 4. Barra de aço (1)
img = draw_ingot(PALETAS_MATERIAL["aco"])
img.save("textures/items/aco_ingot.png")

# 5. Runas + Upgrades (35 tipos × 3 tiers = 105)
for tipo, simbolo in SIMBOLOS.items():
    categoria = CATEGORIA[tipo]
    prefixo = "upgrade" if tipo in UPGRADES else "runa"
    for tier in (1, 2, 3):
        img = draw_runa(simbolo, categoria, tier)
        img.save(f"textures/items/{prefixo}_{tipo}_{tier}.png")

# ═══════════════════════════════════════════════════════════
# ATUALIZA item_texture.json
# ═══════════════════════════════════════════════════════════

ITEM_TEX = "textures/item_texture.json"
if os.path.exists(ITEM_TEX):
    with open(ITEM_TEX, "r", encoding="utf-8") as f:
        it = json.load(f)
else:
    it = {"resource_pack_name": "mod_rpg_rune", "texture_name": "atlas.items", "texture_data": {}}

for fname in sorted(os.listdir("textures/items")):
    if fname.endswith(".png"):
        key = fname[:-4]
        it["texture_data"][key] = {"textures": f"textures/items/{key}"}

with open(ITEM_TEX, "w", encoding="utf-8") as f:
    json.dump(it, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════
# SUMÁRIO
# ═══════════════════════════════════════════════════════════

total = len([f for f in os.listdir("textures/items") if f.endswith(".png")])
print(f"✅ {total} texturas geradas em textures/items/")
print(f"   • 49 armas (7 tipos × 7 materiais)")
print(f"   • 7 paxels")
print(f"   • 5 ferramentas de aço")
print(f"   • 1 barra de aço")
print(f"   • 72 runas (24 × 3 tiers)")
print(f"   • 33 upgrades (11 × 3 tiers)")
print(f"✅ item_texture.json atualizado ({total} entradas)")
print("")
print("⚠️  Próximos passos opcionais:")
print("   • Mesa de Runas (bloco + item) ainda sem textura")
print("   • Substitua PNGs individuais para refinar — o item_texture.json já está pronto")
