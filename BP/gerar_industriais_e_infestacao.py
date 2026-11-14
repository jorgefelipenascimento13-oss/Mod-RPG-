"""
gerar_industriais_e_infestacao.py
Gera: 3 blocos industriais + flecha da Alvorada + Poção de Infestação (item + entidade).
Inclui receitas, texturas 16x16, terrain_texture.json, item_texture.json e lang.
"""
from PIL import Image
import os, json

NS = "mod_rpg_rune"

# ─── Pastas ───────────────────────────────────────────────
os.makedirs("blocks",   exist_ok=True)
os.makedirs("items",    exist_ok=True)
os.makedirs("entities", exist_ok=True)
os.makedirs("recipes",  exist_ok=True)

RP_BLOCKS = "../RP/textures/blocks"
RP_ITEMS  = "../RP/textures/items"
os.makedirs(RP_BLOCKS, exist_ok=True)
os.makedirs(RP_ITEMS,  exist_ok=True)

def gravar(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════
# 1. BLOCOS INDUSTRIAIS (3)
# ═══════════════════════════════════════════════════════════

BLOCOS = {
    "industrial_planter": {
        "nome_pt": "Plantador Industrial", "nome_en": "Industrial Planter",
        "cor_detalhe": (74, 124, 58),  # verde
        "receita": {
            "pattern": ["IHI", "DPS", "ICI"],
            "key": {
                "I": {"item": "minecraft:iron_ingot"},
                "H": {"item": "minecraft:iron_hoe"},
                "D": {"item": "minecraft:dirt"},
                "P": {"item": "minecraft:piston"},
                "S": {"item": "minecraft:oak_sapling"},
                "C": {"item": "minecraft:chest"},
            },
        },
    },
    "industrial_fertilizer": {
        "nome_pt": "Fertilizador Industrial", "nome_en": "Industrial Fertilizer",
        "cor_detalhe": (200, 184, 90),  # amarelo
        "receita": {
            "pattern": ["IBI", "MPM", "ICI"],
            "key": {
                "I": {"item": "minecraft:iron_ingot"},
                "B": {"item": "minecraft:bone_block"},
                "M": {"item": "minecraft:bone_meal"},
                "P": {"item": "minecraft:piston"},
                "C": {"item": "minecraft:chest"},
            },
        },
    },
    "industrial_harvester": {
        "nome_pt": "Colhedor Industrial", "nome_en": "Industrial Harvester",
        "cor_detalhe": (139, 58, 58),  # vermelho
        "receita": {
            "pattern": ["IAI", "SPS", "ICI"],
            "key": {
                "I": {"item": "minecraft:iron_ingot"},
                "A": {"item": "minecraft:iron_axe"},
                "S": {"item": "minecraft:shears"},
                "P": {"item": "minecraft:piston"},
                "C": {"item": "minecraft:chest"},
            },
        },
    },
}

for block_id, b in BLOCOS.items():
    # Bloco
    gravar(f"blocks/{block_id}.json", {
        "format_version": "1.21.30",
        "minecraft:block": {
            "description": {
                "identifier": f"{NS}:{block_id}",
                "menu_category": {"category": "construction"},
            },
            "components": {
                "minecraft:geometry": "minecraft:geometry.full_block",
                "minecraft:material_instances": {
                    "*": {"texture": block_id, "render_method": "opaque"}
                },
                "minecraft:destructible_by_mining": {"seconds_to_destroy": 2.5},
                "minecraft:destructible_by_explosion": {"explosion_resistance": 15},
                "minecraft:map_color": "#5A5A5A",
                "minecraft:collision_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
                "minecraft:selection_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            },
        },
    })

    # Item placeable
    gravar(f"items/{block_id}.json", {
        "format_version": "1.21.30",
        "minecraft:item": {
            "description": {
                "identifier": f"{NS}:{block_id}",
                "menu_category": {"category": "construction"},
            },
            "components": {
                "minecraft:icon": {"texture": block_id},
                "minecraft:display_name": {"value": b["nome_pt"]},
                "minecraft:max_stack_size": 64,
                "minecraft:block_placer": {"block": f"{NS}:{block_id}"},
            },
        },
    })

    # Receita
    gravar(f"recipes/{block_id}.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shaped": {
            "description": {"identifier": f"{NS}:{block_id}"},
            "tags": ["crafting_table"],
            "pattern": b["receita"]["pattern"],
            "key": b["receita"]["key"],
            "result": {"item": f"{NS}:{block_id}", "count": 1},
        },
    })

print("✅ 3 blocos industriais (block + item + recipe)")

# ═══════════════════════════════════════════════════════════
# 2. FLECHA DA ALVORADA
# ═══════════════════════════════════════════════════════════

gravar("items/flecha_alvorada.json", {
    "format_version": "1.21.30",
    "minecraft:item": {
        "description": {
            "identifier": f"{NS}:flecha_alvorada",
            "menu_category": {"category": "equipment"},
        },
        "components": {
            "minecraft:icon": {"texture": "flecha_alvorada"},
            "minecraft:display_name": {"value": "Flecha da Alvorada"},
            "minecraft:max_stack_size": 64,
        },
    },
})

# Receita espelhada ao spectral arrow vanilla: 4 glowstone + 1 arrow → 2 flechas
gravar("recipes/flecha_alvorada.json", {
    "format_version": "1.21.30",
    "minecraft:recipe_shaped": {
        "description": {"identifier": f"{NS}:flecha_alvorada"},
        "tags": ["crafting_table"],
        "pattern": [".G.", "GAG", ".G."],
        "key": {
            "G": {"item": "minecraft:glowstone_dust"},
            "A": {"item": "minecraft:arrow"},
        },
        "result": {"item": f"{NS}:flecha_alvorada", "count": 2},
    },
})

print("✅ Flecha da Alvorada (item + recipe)")

# ═══════════════════════════════════════════════════════════
# 3. POÇÃO DE INFESTAÇÃO (item + entidade)
# ═══════════════════════════════════════════════════════════

gravar("items/pocao_infestacao.json", {
    "format_version": "1.21.30",
    "minecraft:item": {
        "description": {
            "identifier": f"{NS}:pocao_infestacao",
            "menu_category": {"category": "equipment"},
        },
        "components": {
            "minecraft:icon": {"texture": "pocao_infestacao"},
            "minecraft:display_name": {"value": "Poção de Infestação"},
            "minecraft:max_stack_size": 16,
            "minecraft:throwable": {"do_swing_animation": True},
            "minecraft:projectile": {
                "projectile_entity": f"{NS}:infestation_projectile"
            },
        },
    },
})

gravar("entities/infestation_projectile.json", {
    "format_version": "1.21.30",
    "minecraft:entity": {
        "description": {
            "identifier": f"{NS}:infestation_projectile",
            "is_spawnable": False,
            "is_summonable": True,
        },
        "components": {
            "minecraft:collision_box": {"width": 0.25, "height": 0.25},
            "minecraft:physics": {"has_gravity": True, "has_collision": False},
            "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
            "minecraft:projectile": {
                "on_hit": {
                    "impact_damage": {"damage": 0},
                    "remove_on_hit": {}
                },
                "power": 1.2,
                "gravity": 0.03,
            },
            "minecraft:type_family": {"family": ["projectile", "inanimate"]},
        },
    },
})

# Receita: bottle + rotten flesh + spider eye + gunpowder
gravar("recipes/pocao_infestacao.json", {
    "format_version": "1.21.30",
    "minecraft:recipe_shaped": {
        "description": {"identifier": f"{NS}:pocao_infestacao"},
        "tags": ["crafting_table"],
        "pattern": [".F.", "SBS", ".G."],
        "key": {
            "F": {"item": "minecraft:rotten_flesh"},
            "S": {"item": "minecraft:spider_eye"},
            "B": {"item": "minecraft:glass_bottle"},
            "G": {"item": "minecraft:gunpowder"},
        },
        "result": {"item": f"{NS}:pocao_infestacao", "count": 1},
    },
})

print("✅ Poção de Infestação (item + entidade + recipe)")

# ═══════════════════════════════════════════════════════════
# 4. TEXTURAS (16x16 procedurais)
# ═══════════════════════════════════════════════════════════

def bloco_texture(accent):
    base = (90, 90, 90)
    dark = tuple(max(0, c - 40) for c in base)
    light = tuple(min(255, c + 40) for c in base)
    img = Image.new("RGBA", (16, 16), base + (255,))
    px = img.load()
    # Bordas escuras
    for i in range(16):
        px[i, 0] = dark + (255,); px[i, 15] = dark + (255,)
        px[0, i] = dark + (255,); px[15, i] = dark + (255,)
    # Parafusos nos cantos
    for cx, cy in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        px[cx, cy] = light + (255,)
    # Detalhe central 6x6
    for y in range(5, 11):
        for x in range(5, 11):
            px[x, y] = accent + (255,)
    return img

for block_id, b in BLOCOS.items():
    img = bloco_texture(b["cor_detalhe"])
    img.save(f"{RP_BLOCKS}/{block_id}.png")
    img.save(f"{RP_ITEMS}/{block_id}.png")

# Flecha da Alvorada: haste diagonal + ponta dourada + penas
def flecha_texture():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for i in range(4, 12):
        px[i, 15 - i] = (200, 200, 200, 255)  # haste
    px[12, 3] = (255, 220, 100, 255)          # ponta
    px[13, 2] = (255, 240, 130, 255)
    px[11, 4] = (255, 200, 80, 255)
    px[12, 2] = (255, 255, 200, 255)          # brilho
    px[4, 12] = (240, 240, 240, 255)          # penas
    px[5, 11] = (240, 240, 240, 255)
    px[3, 13] = (240, 240, 240, 255)
    px[4, 13] = (220, 220, 220, 255)
    return img
flecha_texture().save(f"{RP_ITEMS}/flecha_alvorada.png")

# Poção: frasco verde brilhante
def pocao_texture():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    cork      = (140, 100, 60, 255)
    glass     = (210, 210, 220, 200)
    liquid    = (120, 200, 90, 255)
    liquid_hi = (190, 250, 140, 255)

    # Rolha
    for x in [7, 8]:
        for y in [2, 3]:
            px[x, y] = cork
    # Pescoço
    for x in [7, 8]:
        for y in [4, 5, 6]:
            px[x, y] = glass
    # Corpo (alarga e afina)
    widths = {7: 2, 8: 4, 9: 6, 10: 6, 11: 6, 12: 4, 13: 2}
    for y, w in widths.items():
        for x in range(8 - w // 2, 8 + w // 2):
            px[x, y] = glass
    # Líquido nas linhas 8..12
    for y in [8, 9, 10, 11, 12]:
        w = widths[y]
        for x in range(8 - w // 2, 8 + w // 2):
            px[x, y] = liquid
    # Highlight
    px[6, 8] = liquid_hi
    px[6, 9] = liquid_hi
    return img
pocao_texture().save(f"{RP_ITEMS}/pocao_infestacao.png")

print("✅ Texturas: 3 blocos (×2) + flecha + poção")

# ═══════════════════════════════════════════════════════════
# 5. REGISTRO EM terrain_texture.json
# ═══════════════════════════════════════════════════════════

TT = "../RP/textures/terrain_texture.json"
if os.path.exists(TT):
    with open(TT, "r", encoding="utf-8") as f:
        tt = json.load(f)
else:
    tt = {"resource_pack_name": NS, "texture_name": "atlas.terrain",
          "padding": 8, "num_mip_levels": 4, "texture_data": {}}

for block_id in BLOCOS.keys():
    tt["texture_data"][block_id] = {"textures": f"textures/blocks/{block_id}"}

with open(TT, "w", encoding="utf-8") as f:
    json.dump(tt, f, indent=2, ensure_ascii=False)
print("✅ terrain_texture.json atualizado")

# ═══════════════════════════════════════════════════════════
# 6. REGISTRO EM item_texture.json
# ═══════════════════════════════════════════════════════════

IT = "../RP/textures/item_texture.json"
if os.path.exists(IT):
    with open(IT, "r", encoding="utf-8") as f:
        it = json.load(f)
else:
    it = {"resource_pack_name": NS, "texture_name": "atlas.items", "texture_data": {}}

for block_id in BLOCOS.keys():
    it["texture_data"][block_id] = {"textures": f"textures/items/{block_id}"}
it["texture_data"]["flecha_alvorada"]   = {"textures": "textures/items/flecha_alvorada"}
it["texture_data"]["pocao_infestacao"]  = {"textures": "textures/items/pocao_infestacao"}

with open(IT, "w", encoding="utf-8") as f:
    json.dump(it, f, indent=2, ensure_ascii=False)
print("✅ item_texture.json atualizado")

# ═══════════════════════════════════════════════════════════
# 7. LANG (pt_BR + en_US) com marker para evitar duplicar
# ═══════════════════════════════════════════════════════════

MARKER = "# === MOD INDUSTRIAL + INFESTACAO ==="

TRADUCOES = {
    "industrial_planter":    ("Plantador Industrial",   "Industrial Planter"),
    "industrial_fertilizer": ("Fertilizador Industrial","Industrial Fertilizer"),
    "industrial_harvester":  ("Colhedor Industrial",    "Industrial Harvester"),
    "flecha_alvorada":       ("Flecha da Alvorada",     "Dawn Arrow"),
    "pocao_infestacao":      ("Poção de Infestação",    "Potion of Infestation"),
}

def atualizar_lang(path, idx):
    if not os.path.exists(path):
        print(f"⚠️  {path} não encontrado — pulando")
        return
    with open(path, "r", encoding="utf-8") as f:
        conteudo = f.read()
    if MARKER in conteudo:
        print(f"⏭️  {path} já contém as entradas — pulando")
        return

    bloco = f"\n{MARKER}\n"
    for item_id, nomes in TRADUCOES.items():
        # Bloco placeable → tile + item
        if item_id in BLOCOS:
            bloco += f"tile.{NS}:{item_id}.name={nomes[idx]}\n"
            bloco += f"item.{NS}:{item_id}={nomes[idx]}\n"
        else:
            bloco += f"item.{NS}:{item_id}={nomes[idx]}\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(bloco)
    print(f"✅ {path} atualizado")

atualizar_lang("../RP/texts/pt_BR.lang", 0)
atualizar_lang("../RP/texts/en_US.lang", 1)

# ═══════════════════════════════════════════════════════════
# SUMÁRIO
# ═══════════════════════════════════════════════════════════

print("\n🎉 Geração concluída.")
print("\nArquivos criados/atualizados:")
print("  BP/blocks/    → 3 blocos industriais")
print("  BP/items/     → 3 placeable + 1 flecha + 1 poção = 5 itens")
print("  BP/entities/  → 1 projétil (infestation_projectile)")
print("  BP/recipes/   → 5 receitas (3 blocos + flecha + poção)")
print("  RP/textures/blocks/ → 3 PNGs")
print("  RP/textures/items/  → 5 PNGs (3 blocos + flecha + poção)")
print("  terrain_texture.json + item_texture.json atualizados")
print("  pt_BR.lang + en_US.lang atualizados")
print("\n⚠️  Ainda falta:")
print("  • Anexar o código da infestação (infestation.js) — ver resposta anterior")
print("  • Corrigir namespace no main.js (meu_addon: → mod_rpg_rune:)")
print("  • Corrigir detecção de baú + remover enchant spam no main.js")
print("  • Testar em mundo novo (recipes podem precisar de /reload)")
