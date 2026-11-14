import os, json

NAMESPACE = "mod_rpg_rune"

MATERIAIS_ITEM = {
    "madeira":   "minecraft:oak_planks",
    "pedra":     "minecraft:cobblestone",
    "ouro":      "minecraft:gold_ingot",
    "cobre":     "minecraft:copper_ingot",
    "ferro":     "minecraft:iron_ingot",
    "aco":       "mod_rpg_rune:aco_ingot",   # ← será criado depois
}

PADROES = {
    "katana":             ["X..", ".X.", "..S"],
    "adaga":              ["...", ".X.", "..S"],
    "espada_longa":       ["XX.", "XX.", "S.."],
    "hari":               ["XXS", "...", "..."],
    "dragon_slayer":      ["XXX", "XXX", "S.."],
    "machado_tatico":     ["XX.", "XS.", "..."],
    "machado_de_batalha": ["XXX", "XSX", ".S."],
}

ARMAS = list(PADROES.keys())

os.makedirs("recipes", exist_ok=True)
crafting_count = 0
smithing_count = 0

# ─── 1. Receitas de crafting (6 materiais × 7 armas = 42) ───
for arma, pattern in PADROES.items():
    for mat, mat_item in MATERIAIS_ITEM.items():
        item_id = f"{arma}_{mat}"
        receita = {
            "format_version": "1.21.30",
            "minecraft:recipe_shaped": {
                "description": {"identifier": f"{NAMESPACE}:{item_id}"},
                "tags": ["crafting_table"],
                "pattern": pattern,
                "key": {
                    "X": {"item": mat_item},
                    "S": {"item": "minecraft:stick"},
                },
                "result": {"item": f"{NAMESPACE}:{item_id}"},
            }
        }
        with open(f"recipes/{item_id}.json", "w", encoding="utf-8") as f:
            json.dump(receita, f, indent=2, ensure_ascii=False)
        crafting_count += 1

# ─── 2. Receitas de smithing (netherite, 7 armas) ───
for arma in ARMAS:
    item_id = f"{arma}_netherite"
    receita = {
        "format_version": "1.21.30",
        "minecraft:recipe_smithing_transform": {
            "description": {"identifier": f"{NAMESPACE}:{item_id}"},
            "tags": ["smithing_table"],
            "template": {"item": "minecraft:netherite_upgrade_smithing_template"},
            "base":     {"item": f"{NAMESPACE}:{arma}_aco"},   # ← troque por _ferro se quiser testar antes
            "addition": {"item": "minecraft:netherite_ingot"},
            "result":   {"item": f"{NAMESPACE}:{item_id}"},
        }
    }
    with open(f"recipes/{item_id}.json", "w", encoding="utf-8") as f:
        json.dump(receita, f, indent=2, ensure_ascii=False)
    smithing_count += 1

print(f"✅ {crafting_count} receitas de crafting geradas")
print(f"✅ {smithing_count} receitas de smithing geradas")
print(f"✅ Total: {crafting_count + smithing_count} receitas em recipes/")
