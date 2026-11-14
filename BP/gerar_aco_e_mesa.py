"""
gerar_aco_e_mesa.py — Gera aco_ingot (item + receita) + Mesa de Runas (bloco + item + receita + texturas).
Rodar na raiz do BP.
"""
from PIL import Image
import os, json

NS = "mod_rpg_rune"
os.makedirs("blocks",  exist_ok=True)
os.makedirs("items",   exist_ok=True)
os.makedirs("recipes", exist_ok=True)

RP_BLOCKS = "../RP/textures/blocks"
RP_ITEMS  = "../RP/textures/items"
os.makedirs(RP_BLOCKS, exist_ok=True)
os.makedirs(RP_ITEMS,  exist_ok=True)

def gravar(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════
# 1. AÇO INGOT
# ═══════════════════════════════════════════════════════

gravar("items/aco_ingot.json", {
    "format_version": "1.21.30",
    "minecraft:item": {
        "description": {
            "identifier": f"{NS}:aco_ingot",
            "menu_category": {"category": "items"}
        },
        "components": {
            "minecraft:icon": {"texture": "aco_ingot"},
            "minecraft:display_name": {"value": "Barra de Aço"},
            "minecraft:max_stack_size": 64
        }
    }
})

# Ferro → Aço na fornalha (10s) e alto-forno (5s)
gravar("recipes/aco_ingot.json", {
    "format_version": "1.21.30",
    "minecraft:recipe_furnace": {
        "description": {"identifier": f"{NS}:aco_ingot"},
        "tags": ["furnace", "blast_furnace"],
        "input": "minecraft:iron_ingot",
        "output": f"{NS}:aco_ingot"
    }
})

print("✅ aco_ingot (item + recipe)")

# ═══════════════════════════════════════════════════════
# 2. MESA DE RUNAS
# ═══════════════════════════════════════════════════════

gravar("blocks/mesa_de_runas.json", {
    "format_version": "1.21.30",
    "minecraft:block": {
        "description": {
            "identifier": f"{NS}:mesa_de_runas",
            "menu_category": {"category": "construction"}
        },
        "components": {
            "minecraft:geometry": "minecraft:geometry.full_block",
            "minecraft:material_instances": {
                "*": {"texture": "mesa_de_runas", "render_method": "opaque"}
            },
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 3.0},
            "minecraft:destructible_by_explosion": {"explosion_resistance": 20},
            "minecraft:map_color": "#4A2A6B",
            "minecraft:light_emission": 7,
            "minecraft:collision_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            "minecraft:selection_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]}
        }
    }
})

gravar("items/mesa_de_runas.json", {
    "format_version": "1.21.30",
    "minecraft:item": {
        "description": {
            "identifier": f"{NS}:mesa_de_runas",
            "menu_category": {"category": "construction"}
        },
        "components": {
            "minecraft:icon": {"texture": "mesa_de_runas"},
            "minecraft:display_name": {"value": "Mesa de Runas"},
            "minecraft:max_stack_size": 64,
            "minecraft:block_placer": {"block": f"{NS}:mesa_de_runas"}
        }
    }
})

# Craft: 4 ouro + 4 esmeralda + 1 obsidiana (padrão GEG/EOE/GEG)
gravar("recipes/mesa_de_runas.json", {
    "format_version": "1.21.30",
    "minecraft:recipe_shaped": {
        "description": {"identifier": f"{NS}:mesa_de_runas"},
        "tags": ["crafting_table"],
        "pattern": ["GEG", "EOE", "GEG"],
        "key": {
            "G": {"item": "minecraft:gold_ingot"},
            "E": {"item": "minecraft:emerald"},
            "O": {"item": "minecraft:obsidian"}
        },
        "result": {"item": f"{NS}:mesa_de_runas", "count": 1}
    }
})

print("✅ mesa_de_runas (block + item + recipe)")

# ═══════════════════════════════════════════════════════
# 3. TEXTURAS
# ═══════════════════════════════════════════════════════

# Barra de aço (recria se não existir)
def aco_texture():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    base, dark, light = (140, 155, 175, 255), (75, 90, 110, 255), (190, 205, 225, 255)
    for y in range(6, 11):
        for x in range(3, 13):
            px[x, y] = base
    for x in range(3, 13):
        px[x, 6] = dark
        px[x, 10] = dark
    for y in range(6, 11):
        px[3, y] = dark
        px[12, y] = dark
    for x in range(5, 10):
        px[x, 7] = light
    return img

if not os.path.exists(f"{RP_ITEMS}/aco_ingot.png"):
    aco_texture().save(f"{RP_ITEMS}/aco_ingot.png")
    print("✅ aco_ingot.png criada")
else:
    print("⏭️  aco_ingot.png já existia — mantida")

# Mesa de Runas: pedra escura com runas brilhantes
def mesa_texture():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    base  = (58, 34, 82, 255)   # roxo escuro
    dark  = (30, 18, 45, 255)
    light = (140, 100, 200, 255)
    glow  = (210, 160, 255, 255)

    # Fundo
    for y in range(16):
        for x in range(16):
            px[x, y] = base
    # Borda
    for i in range(16):
        px[i, 0] = dark; px[i, 15] = dark
        px[0, i] = dark; px[15, i] = dark
    # Runas nos cantos
    for rx, ry in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        px[rx, ry] = glow
        px[rx + 1, ry] = light
        px[rx, ry + 1] = light
    # Símbolo central (estrela de 8 pontas)
    for dx, dy in [(0,-3),(0,3),(-3,0),(3,0),(-1,-1),(1,-1),(-1,1),(1,1),(0,0)]:
        px[8 + dx, 8 + dy] = glow
    for dx, dy in [(-2,-2),(2,-2),(-2,2),(2,2)]:
        px[8 + dx, 8 + dy] = light
    return img

img = mesa_texture()
img.save(f"{RP_BLOCKS}/mesa_de_runas.png")
img.save(f"{RP_ITEMS}/mesa_de_runas.png")
print("✅ Texturas da mesa criadas (bloco + ícone)")

# ═══════════════════════════════════════════════════════
# 4. ATLAS
# ═══════════════════════════════════════════════════════

TT = "../RP/textures/terrain_texture.json"
if os.path.exists(TT):
    with open(TT, encoding="utf-8") as f: tt = json.load(f)
else:
    tt = {"resource_pack_name": NS, "texture_name": "atlas.terrain",
          "padding": 8, "num_mip_levels": 4, "texture_data": {}}
tt["texture_data"]["mesa_de_runas"] = {"textures": "textures/blocks/mesa_de_runas"}
with open(TT, "w", encoding="utf-8") as f: json.dump(tt, f, indent=2, ensure_ascii=False)

IT = "../RP/textures/item_texture.json"
if os.path.exists(IT):
    with open(IT, encoding="utf-8") as f: it = json.load(f)
else:
    it = {"resource_pack_name": NS, "texture_name": "atlas.items", "texture_data": {}}
it["texture_data"]["mesa_de_runas"] = {"textures": "textures/items/mesa_de_runas"}
it["texture_data"]["aco_ingot"]     = {"textures": "textures/items/aco_ingot"}
with open(IT, "w", encoding="utf-8") as f: json.dump(it, f, indent=2, ensure_ascii=False)
print("✅ terrain_texture.json + item_texture.json atualizados")

# ═══════════════════════════════════════════════════════
# 5. LANG (com marker anti-duplicação)
# ═══════════════════════════════════════════════════════

MARKER = "# === ACO + MESA DE RUNAS ==="
def update_lang(path, entries):
    if not os.path.exists(path):
        print(f"⚠️  {path} não encontrado — pulando")
        return
    with open(path, encoding="utf-8") as f: c = f.read()
    if MARKER in c:
        print(f"⏭️  {path} já tem entradas — pulando")
        return
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n{MARKER}\n")
        for k, v in entries:
            f.write(f"{k}={v}\n")
    print(f"✅ {path} atualizado")

update_lang("../RP/texts/pt_BR.lang", [
    (f"item.{NS}:aco_ingot",          "Barra de Aço"),
    (f"tile.{NS}:mesa_de_runas.name", "Mesa de Runas"),
    (f"item.{NS}:mesa_de_runas",      "Mesa de Runas"),
])
update_lang("../RP/texts/en_US.lang", [
    (f"item.{NS}:aco_ingot",          "Steel Ingot"),
    (f"tile.{NS}:mesa_de_runas.name", "Rune Table"),
    (f"item.{NS}:mesa_de_runas",      "Rune Table"),
])

print("\n🎉 Concluído!")
print("\nResumo:")
print("  items/aco_ingot.json")
print("  recipes/aco_ingot.json")
print("  blocks/mesa_de_runas.json")
print("  items/mesa_de_runas.json")
print("  recipes/mesa_de_runas.json")
print("  RP/textures/blocks/mesa_de_runas.png")
print("  RP/textures/items/mesa_de_runas.png")
print("  RP/textures/items/aco_ingot.png (se não existir)")
print("  Atlas + lang atualizados")
