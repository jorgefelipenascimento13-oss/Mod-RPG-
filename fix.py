import os, json

print("Iniciando correções...")

# 1. Corrigir Receitas (adicionar unlock)
recipes_dirs = ["recipes", "BP/recipes"]
rec_dir = next((d for d in recipes_dirs if os.path.exists(d)), None)
if rec_dir:
    count = 0
    for f in os.listdir(rec_dir):
        if f.endswith(".json"):
            p = os.path.join(rec_dir, f)
            with open(p, "r", encoding="utf-8") as file:
                data = json.load(file)
            unlock = [{"item": "minecraft:stick"}]
            mudou = False
            for key in ["minecraft:recipe_shaped", "minecraft:recipe_shapeless", "minecraft:recipe_furnace", "minecraft:recipe_smithing_transform"]:
                if key in data and "unlock" not in data[key]:
                    data[key]["unlock"] = unlock
                    mudou = True
            if mudou:
                with open(p, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
                count += 1
    print(f"✅ {count} receitas corrigidas.")
else:
    print("❌ Pasta de receitas não encontrada.")

# 2. Corrigir Texturas (item_texture.json)
items_dirs = ["RP/textures/items", "textures/items"]
it_dir = next((d for d in items_dirs if os.path.exists(d)), None)
if it_dir:
    rp_textures = os.path.dirname(it_dir)
    tex_path = os.path.join(rp_textures, "item_texture.json")
    tex_data = {}
    for f in os.listdir(it_dir):
        if f.endswith(".png"):
            key = f[:-4]
            tex_data[key] = {"textures": f"textures/items/{key}"}
    json_final = {
        "resource_pack_name": "mod_rpg_rune",
        "texture_name": "atlas.items",
        "texture_data": tex_data
    }
    with open(tex_path, "w", encoding="utf-8") as file:
        json.dump(json_final, file, indent=2, ensure_ascii=False)
    print(f"✅ item_texture.json refeito com {len(tex_data)} texturas.")
else:
    print("❌ Pasta de texturas não encontrada.")
