import os, json

NAMESPACE = "mod_rpg_rune"
MATERIAIS_DISPLAY = {
    "madeira": "Madeira", "pedra": "Pedra", "ouro": "Ouro",
    "cobre": "Cobre", "ferro": "Ferro", "aco": "Aço", "netherite": "Netherite",
}

AXE_DIGGER = {
    "use_efficiency": True,
    "destroy_speeds": [
        {"block": {"tags": "q.any_tag('wood')"}, "speed": 6},
    ],
}

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

os.makedirs("items", exist_ok=True)
total = 0

for arma_id, arma in ARMAS.items():
    for mat_id, stats in arma["dados"].items():
        item_id = f"{arma_id}_{mat_id}"
        display = f"{arma['nome']} de {MATERIAIS_DISPLAY[mat_id]}"

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
            "minecraft:display_name": {"value": display},
            "minecraft:tags": {"tags": [
                f"{NAMESPACE}:rune_compatible",
                f"weapon.{arma_id}",
                f"material.{mat_id}",
            ]},
        }

        if arma.get("digger"):
            components["minecraft:digger"] = AXE_DIGGER

        data = {
            "format_version": "1.21.30",
            "minecraft:item": {
                "description": {
                    "identifier": f"{NAMESPACE}:{item_id}",
                    "menu_category": {"category": "equipment", "group": arma["grupo"]},
                },
                "components": components,
            }
        }

        with open(f"items/{item_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        total += 1

print(f"✅ {total} itens gerados em items/")
