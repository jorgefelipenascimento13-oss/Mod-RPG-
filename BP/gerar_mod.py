"""
gerar_mod.py — Gera todos os itens e receitas do mod (armas + paxels + ferramentas de aço).
Executar na raiz do Behavior Pack. Cria:
  items/    → 61 arquivos
  recipes/  → 61 arquivos
"""
import os, json

NAMESPACE = "mod_rpg_rune"
MATERIAIS_DISPLAY = {
    "madeira": "Madeira", "pedra": "Pedra", "ouro": "Ouro",
    "cobre": "Cobre", "ferro": "Ferro", "aco": "Aço", "netherite": "Netherite",
}
MATERIAIS_ITEM = {
    "madeira":   "minecraft:oak_planks",
    "pedra":     "minecraft:cobblestone",
    "ouro":      "minecraft:gold_ingot",
    "cobre":     "minecraft:copper_ingot",
    "ferro":     "minecraft:iron_ingot",
    "aco":       "mod_rpg_rune:aco_ingot",   # ← criado depois
    "netherite": "minecraft:netherite_ingot",
}

os.makedirs("items", exist_ok=True)
os.makedirs("recipes", exist_ok=True)

# ═══════════════════════════════════════════════════════════
# 1. ARMAS (49 itens)
# ═══════════════════════════════════════════════════════════

ARMAS = {
    "katana": {
        "nome": "Katana", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dados": {
            "madeira":   {"dano": 3,  "durabilidade": 100,  "encantamento": 15},
            "pedra":     {"dano": 4,  "durabilidade": 200,  "encantamento": 15},
            "ouro":      {"dano": 5,  "durabilidade": 200,  "encantamento": 15},
            "cobre":     {"dano": 8,  "durabilidade": 400,  "encantamento": 15},
            "ferro":     {"dano": 6,  "durabilidade": 850,  "encantamento": 15},
            "aco":       {"dano": 9,  "durabilidade": 1400, "encantamento": 15},
            "netherite": {"dano": 11, "durabilidade": 2500, "encantamento": 15},
        },
    },
    "adaga": {
        "nome": "Adaga", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dados": {
            "madeira":   {"dano": 1, "durabilidade": 50,   "encantamento": 15},
            "pedra":     {"dano": 2, "durabilidade": 100,  "encantamento": 15},
            "ouro":      {"dano": 2, "durabilidade": 150,  "encantamento": 15},
            "cobre":     {"dano": 4, "durabilidade": 250,  "encantamento": 15},
            "ferro":     {"dano": 3, "durabilidade": 450,  "encantamento": 15},
            "aco":       {"dano": 5, "durabilidade": 800,  "encantamento": 15},
            "netherite": {"dano": 6, "durabilidade": 1800, "encantamento": 15},
        },
    },
    "espada_longa": {
        "nome": "Espada Longa", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dados": {
            "madeira":   {"dano": 5,  "durabilidade": 100,  "encantamento": 15},
            "pedra":     {"dano": 6,  "durabilidade": 200,  "encantamento": 15},
            "ouro":      {"dano": 6,  "durabilidade": 250,  "encantamento": 15},
            "cobre":     {"dano": 10, "durabilidade": 500,  "encantamento": 15},
            "ferro":     {"dano": 8,  "durabilidade": 1000, "encantamento": 15},
            "aco":       {"dano": 11, "durabilidade": 1800, "encantamento": 15},
            "netherite": {"dano": 13, "durabilidade": 3000, "encantamento": 15},
        },
    },
    "hari": {
        "nome": "Hari", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dados": {
            "madeira":   {"dano": 1, "durabilidade": 20,  "encantamento": 20},
            "pedra":     {"dano": 2, "durabilidade": 35,  "encantamento": 15},
            "ouro":      {"dano": 3, "durabilidade": 50,  "encantamento": 25},
            "cobre":     {"dano": 3, "durabilidade": 100, "encantamento": 10},
            "ferro":     {"dano": 4, "durabilidade": 150, "encantamento": 14},
            "aco":       {"dano": 5, "durabilidade": 200, "encantamento": 12},
            "netherite": {"dano": 6, "durabilidade": 300, "encantamento": 15},
        },
    },
    "machado_tatico": {
        "nome": "Machado Tático", "grupo": "itemGroup.name.axe", "slot": "axe",
        "digger": True,
        "dados": {
            "madeira":   {"dano": 4, "durabilidade": 40,  "encantamento": 20},
            "pedra":     {"dano": 5, "durabilidade": 70,  "encantamento": 15},
            "ouro":      {"dano": 5, "durabilidade": 80,  "encantamento": 25},
            "cobre":     {"dano": 6, "durabilidade": 160, "encantamento": 10},
            "ferro":     {"dano": 7, "durabilidade": 350, "encantamento": 14},
            "aco":       {"dano": 8, "durabilidade": 550, "encantamento": 12},
            "netherite": {"dano": 9, "durabilidade": 800, "encantamento": 10},
        },
    },
    "machado_de_batalha": {
        "nome": "Machado de Batalha", "grupo": "itemGroup.name.axe", "slot": "axe",
        "digger": True,
        "dados": {
            "madeira":   {"dano": 6,  "durabilidade": 46,  "encantamento": 20},
            "pedra":     {"dano": 7,  "durabilidade": 80,  "encantamento": 15},
            "ouro":      {"dano": 7,  "durabilidade": 92,  "encantamento": 25},
            "cobre":     {"dano": 8,  "durabilidade": 184, "encantamento": 10},
            "ferro":     {"dano": 9,  "durabilidade": 402, "encantamento": 14},
            "aco":       {"dano": 10, "durabilidade": 632, "encantamento": 12},
            "netherite": {"dano": 11, "durabilidade": 920, "encantamento": 10},
        },
    },
    "dragon_slayer": {
        "nome": "Dragon Slayer", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dados": {
            "madeira":   {"dano": 5,  "durabilidade": 100,  "encantamento": 15},
            "pedra":     {"dano": 6,  "durabilidade": 200,  "encantamento": 15},
            "ouro":      {"dano": 7,  "durabilidade": 240,  "encantamento": 22},
            "cobre":     {"dano": 10, "durabilidade": 480,  "encantamento": 12},
            "ferro":     {"dano": 8,  "durabilidade": 1020, "encantamento": 15},
            "aco":       {"dano": 11, "durabilidade": 1680, "encantamento": 12},
            "netherite": {"dano": 13, "durabilidade": 3000, "encantamento": 15},
        },
    },
}

PADROES_ARMAS = {
    "katana":             ["X..", ".X.", "..S"],
    "adaga":              ["...", ".X.", "..S"],
    "espada_longa":       ["XX.", "XX.", "S.."],
    "hari":               ["XXS", "...", "..."],
    "dragon_slayer":      ["XXX", "XXX", "S.."],
    "machado_tatico":     ["XX.", "XS.", "..."],
    "machado_de_batalha": ["XXX", "XSX", ".S."],
}

AXE_DIGGER = {
    "use_efficiency": True,
    "destroy_speeds": [
        {"block": {"tags": "q.any_tag('wood')"}, "speed": 6},
    ],
}

# ═══════════════════════════════════════════════════════════
# 2. PAXELS (7 itens)
# ═══════════════════════════════════════════════════════════

PAXEL_TAGS = (
    "q.any_tag('stone', 'metal', 'wood', 'dirt', 'grass', 'sand', 'gravel', "
    "'snow', 'plant', 'leaves', 'crop', 'obsidian', 'glass', 'ice', 'wool', "
    "'door', 'trapdoor', 'anvil')"
)

PAXEL = {
    "madeira":   {"durabilidade": 200,  "dano": 1, "speed": 4,  "encantamento": 15},
    "pedra":     {"durabilidade": 400,  "dano": 1, "speed": 6,  "encantamento": 5},
    "ouro":      {"durabilidade": 300,  "dano": 1, "speed": 12, "encantamento": 22},
    "cobre":     {"durabilidade": 800,  "dano": 2, "speed": 8,  "encantamento": 12},
    "ferro":     {"durabilidade": 1500, "dano": 2, "speed": 10, "encantamento": 14},
    "aco":       {"durabilidade": 2200, "dano": 3, "speed": 13, "encantamento": 10},
    "netherite": {"durabilidade": 3000, "dano": 3, "speed": 16, "encantamento": 15},
}

FERRAMENTAS_PAXEL = {
    "madeira": {
        "picareta": "minecraft:wooden_pickaxe", "machado": "minecraft:wooden_axe",
        "pa": "minecraft:wooden_shovel", "enxada": "minecraft:wooden_hoe", "espada": "minecraft:wooden_sword",
    },
    "pedra": {
        "picareta": "minecraft:stone_pickaxe", "machado": "minecraft:stone_axe",
        "pa": "minecraft:stone_shovel", "enxada": "minecraft:stone_hoe", "espada": "minecraft:stone_sword",
    },
    "ouro": {
        "picareta": "minecraft:golden_pickaxe", "machado": "minecraft:golden_axe",
        "pa": "minecraft:golden_shovel", "enxada": "minecraft:golden_hoe", "espada": "minecraft:golden_sword",
    },
    "cobre": {
        "picareta": "minecraft:copper_pickaxe", "machado": "minecraft:copper_axe",
        "pa": "minecraft:copper_shovel", "enxada": "minecraft:copper_hoe", "espada": "minecraft:copper_sword",
    },
    "ferro": {
        "picareta": "minecraft:iron_pickaxe", "machado": "minecraft:iron_axe",
        "pa": "minecraft:iron_shovel", "enxada": "minecraft:iron_hoe", "espada": "minecraft:iron_sword",
    },
    "aco": {
        "picareta": f"{NAMESPACE}:aco_pickaxe", "machado": f"{NAMESPACE}:aco_axe",
        "pa": f"{NAMESPACE}:aco_shovel", "enxada": f"{NAMESPACE}:aco_hoe", "espada": f"{NAMESPACE}:aco_sword",
    },
}

# ═══════════════════════════════════════════════════════════
# 3. FERRAMENTAS DE AÇO (5 itens)
# ═══════════════════════════════════════════════════════════

FERRAMENTAS_ACO = {
    "aco_pickaxe": {
        "nome": "Picareta de Aço", "grupo": "itemGroup.name.pickaxe", "slot": "pickaxe",
        "dano": 3, "durabilidade": 1600, "encantamento": 14,
        "digger": [{"block": {"tags": "q.any_tag('stone', 'metal')"}, "speed": 8}],
    },
    "aco_axe": {
        "nome": "Machado de Aço", "grupo": "itemGroup.name.axe", "slot": "axe",
        "dano": 7, "durabilidade": 1600, "encantamento": 14,
        "digger": [{"block": {"tags": "q.any_tag('wood', 'plant')"}, "speed": 8}],
    },
    "aco_shovel": {
        "nome": "Pá de Aço", "grupo": "itemGroup.name.shovel", "slot": "shovel",
        "dano": 2, "durabilidade": 1600, "encantamento": 14,
        "digger": [{"block": {"tags": "q.any_tag('dirt', 'sand', 'gravel', 'snow')"}, "speed": 8}],
    },
    "aco_hoe": {
        "nome": "Enxada de Aço", "grupo": "itemGroup.name.hoe", "slot": "hoe",
        "dano": 1, "durabilidade": 1600, "encantamento": 14,
        "digger": [{"block": {"tags": "q.any_tag('plant', 'leaves', 'crop')"}, "speed": 8}],
    },
    "aco_sword": {
        "nome": "Espada de Aço", "grupo": "itemGroup.name.sword", "slot": "sword",
        "dano": 7, "durabilidade": 1600, "encantamento": 14,
        "digger": None,
    },
}

PADROES_ACO = {
    "aco_pickaxe": ["XXX", ".S.", ".S."],
    "aco_axe":     ["XX.", "XS.", ".S."],
    "aco_shovel":  ["X..", "S..", "S.."],
    "aco_hoe":     ["XX.", ".S.", ".S."],
    "aco_sword":   ["X..", "X..", "S.."],
}

# ═══════════════════════════════════════════════════════════
# 4. GERAÇÃO — ITENS
# ═══════════════════════════════════════════════════════════

def gravar(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 4.1 Armas
for arma_id, arma in ARMAS.items():
    for mat_id, stats in arma["dados"].items():
        item_id = f"{arma_id}_{mat_id}"
        components = {
            "minecraft:max_stack_size": 1,
            "minecraft:hand_equipped": True,
            "minecraft:damage": stats["dano"],
            "minecraft:durability": {"max_durability": stats["durabilidade"]},
            "minecraft:enchantable": {"value": stats["encantamento"], "slot": arma["slot"]},
            "minecraft:weapon": {
                "on_hit_block":  {"affect_item_durability": True},
                "on_hit_entity": {"affect_item_durability": True},
            },
            "minecraft:icon": {"texture": item_id},
            "minecraft:display_name": {"value": f"{arma['nome']} de {MATERIAIS_DISPLAY[mat_id]}"},
            "minecraft:tags": {"tags": [
                f"{NAMESPACE}:rune_compatible",
                f"weapon.{arma_id}",
                f"material.{mat_id}",
            ]},
        }
        if arma.get("digger"):
            components["minecraft:digger"] = AXE_DIGGER

        gravar(f"items/{item_id}.json", {
            "format_version": "1.21.30",
            "minecraft:item": {
                "description": {
                    "identifier": f"{NAMESPACE}:{item_id}",
                    "menu_category": {"category": "equipment", "group": arma["grupo"]},
                },
                "components": components,
            }
        })

# 4.2 Paxels
for mat, s in PAXEL.items():
    item_id = f"paxel_{mat}"
    gravar(f"items/{item_id}.json", {
        "format_version": "1.21.30",
        "minecraft:item": {
            "description": {
                "identifier": f"{NAMESPACE}:{item_id}",
                "menu_category": {"category": "equipment", "group": "itemGroup.name.equipment"},
            },
            "components": {
                "minecraft:icon": {"texture": item_id},
                "minecraft:display_name": {"value": f"Paxel de {MATERIAIS_DISPLAY[mat]}"},
                "minecraft:max_stack_size": 1,
                "minecraft:hand_equipped": True,
                "minecraft:durability": {"max_durability": s["durabilidade"]},
                "minecraft:damage": s["dano"],
                "minecraft:digger": {
                    "use_efficiency": True,
                    "destroy_speeds": [{"block": {"tags": PAXEL_TAGS}, "speed": s["speed"]}],
                },
                "minecraft:enchantable": {"value": s["encantamento"], "slot": "pickaxe"},
                "minecraft:tags": {"tags": [f"{NAMESPACE}:paxel", f"material.{mat}"]},
            }
        }
    })

# 4.3 Ferramentas de aço
for item_id, f in FERRAMENTAS_ACO.items():
    components = {
        "minecraft:icon": {"texture": item_id},
        "minecraft:display_name": {"value": f["nome"]},
        "minecraft:max_stack_size": 1,
        "minecraft:hand_equipped": True,
        "minecraft:damage": f["dano"],
        "minecraft:durability": {"max_durability": f["durabilidade"]},
        "minecraft:enchantable": {"value": f["encantamento"], "slot": f["slot"]},
        "minecraft:tags": {"tags": [
            f"{NAMESPACE}:rune_compatible",
            f"material.aco",
        ]},
    }
    if f["digger"]:
        components["minecraft:digger"] = {
            "use_efficiency": True,
            "destroy_speeds": f["digger"],
        }
    gravar(f"items/{item_id}.json", {
        "format_version": "1.21.30",
        "minecraft:item": {
            "description": {
                "identifier": f"{NAMESPACE}:{item_id}",
                "menu_category": {"category": "equipment", "group": f["grupo"]},
            },
            "components": components,
        }
    })

# ═══════════════════════════════════════════════════════════
# 5. GERAÇÃO — RECEITAS
# ═══════════════════════════════════════════════════════════

# 5.1 Receitas de armas (6 materiais cada, exceto netherite)
for arma, pattern in PADROES_ARMAS.items():
    for mat in ["madeira", "pedra", "ouro", "cobre", "ferro", "aco"]:
        item_id = f"{arma}_{mat}"
        gravar(f"recipes/{item_id}.json", {
            "format_version": "1.21.30",
            "minecraft:recipe_shaped": {
                "description": {"identifier": f"{NAMESPACE}:{item_id}"},
                "tags": ["crafting_table"],
                "pattern": pattern,
                "key": {
                    "X": {"item": MATERIAIS_ITEM[mat]},
                    "S": {"item": "minecraft:stick"},
                },
                "result": {"item": f"{NAMESPACE}:{item_id}"},
            }
        })

# 5.2 Receitas smithing de armas netherite
for arma in ARMAS.keys():
    item_id = f"{arma}_netherite"
    gravar(f"recipes/{item_id}.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_smithing_transform": {
            "description": {"identifier": f"{NAMESPACE}:{item_id}"},
            "tags": ["smithing_table"],
            "template": {"item": "minecraft:netherite_upgrade_smithing_template"},
            "base":     {"item": f"{NAMESPACE}:{arma}_aco"},
            "addition": {"item": "minecraft:netherite_ingot"},
            "result":   {"item": f"{NAMESPACE}:{item_id}"},
        }
    })

# 5.3 Receitas de paxel (crafting + smithing netherite)
for mat in ["madeira", "pedra", "ouro", "cobre", "ferro", "aco"]:
    ferr = FERRAMENTAS_PAXEL[mat]
    item_id = f"paxel_{mat}"
    gravar(f"recipes/{item_id}.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shaped": {
            "description": {"identifier": f"{NAMESPACE}:{item_id}"},
            "tags": ["crafting_table"],
            "pattern": ["ABC", "DE.", "..."],
            "key": {
                "A": {"item": ferr["picareta"]},
                "B": {"item": ferr["machado"]},
                "C": {"item": ferr["pa"]},
                "D": {"item": ferr["enxada"]},
                "E": {"item": ferr["espada"]},
            },
            "result": {"item": f"{NAMESPACE}:{item_id}"},
        }
    })

gravar("recipes/paxel_netherite.json", {
    "format_version": "1.21.30",
    "minecraft:recipe_smithing_transform": {
        "description": {"identifier": f"{NAMESPACE}:paxel_netherite"},
        "tags": ["smithing_table"],
        "template": {"item": "minecraft:netherite_upgrade_smithing_template"},
        "base":     {"item": f"{NAMESPACE}:paxel_aco"},
        "addition": {"item": "minecraft:netherite_ingot"},
        "result":   {"item": f"{NAMESPACE}:paxel_netherite"},
    }
})

# 5.4 Receitas das ferramentas de aço
for item_id, pattern in PADROES_ACO.items():
    gravar(f"recipes/{item_id}.json", {
        "format_version": "1.21.30",
        "minecraft:recipe_shaped": {
            "description": {"identifier": f"{NAMESPACE}:{item_id}"},
            "tags": ["crafting_table"],
            "pattern": pattern,
            "key": {
                "X": {"item": f"{NAMESPACE}:aco_ingot"},
                "S": {"item": "minecraft:stick"},
            },
            "result": {"item": f"{NAMESPACE}:{item_id}"},
        }
    })

# ═══════════════════════════════════════════════════════════
# 6. SUMÁRIO
# ═══════════════════════════════════════════════════════════

print("✅ Geração concluída:")
print(f"   items/  → 49 armas + 7 paxels + 5 ferramentas de aço = 61 arquivos")
print(f"   recipes/ → 42 (armas crafting) + 7 (armas smithing)")
print(f"            + 6 (paxels crafting) + 1 (paxel smithing)")
print(f"            + 5 (ferramentas de aço) = 61 arquivos")
print(f"   ⚠️  Lembre-se: o item 'mod_rpg_rune:aco_ingot' ainda precisa ser criado.")
