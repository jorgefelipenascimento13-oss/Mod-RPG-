import os
import json

# Lista de (nome_base, nome_exibicao)
itens = [
    # Runas de Arma
    ("runa_vampirism_1", "Runa de Vampirismo I"), ("runa_vampirism_2", "Runa de Vampirismo II"), ("runa_vampirism_3", "Runa de Vampirismo III"),
    ("runa_soul_fire_1", "Runa de Fogo das Almas I"), ("runa_soul_fire_2", "Runa de Fogo das Almas II"), ("runa_soul_fire_3", "Runa de Fogo das Almas III"),
    ("runa_decomposition_1", "Runa de Decomposição I"), ("runa_decomposition_2", "Runa de Decomposição II"), ("runa_decomposition_3", "Runa de Decomposição III"),
    ("runa_poison_1", "Runa de Veneno I"), ("runa_poison_2", "Runa de Veneno II"), ("runa_poison_3", "Runa de Veneno III"),
    ("runa_bleeding_1", "Runa de Sangramento I"), ("runa_bleeding_2", "Runa de Sangramento II"), ("runa_bleeding_3", "Runa de Sangramento III"),
    ("runa_freezing_1", "Runa de Congelamento I"), ("runa_freezing_2", "Runa de Congelamento II"), ("runa_freezing_3", "Runa de Congelamento III"),
    ("runa_lightning_1", "Runa Relampejante I"), ("runa_lightning_2", "Runa Relampejante II"), ("runa_lightning_3", "Runa Relampejante III"),
    ("runa_fissure_1", "Runa de Fissura I"), ("runa_fissure_2", "Runa de Fissura II"), ("runa_fissure_3", "Runa de Fissura III"),
    ("runa_echo_1", "Runa de Eco I"), ("runa_echo_2", "Runa de Eco II"), ("runa_echo_3", "Runa de Eco III"),
    # Runas de Armadura
    ("runa_purification_1", "Runa de Purificação I"), ("runa_purification_2", "Runa de Purificação II"), ("runa_purification_3", "Runa de Purificação III"),
    ("runa_sylvan_1", "Runa Silvestre I"), ("runa_sylvan_2", "Runa Silvestre II"), ("runa_sylvan_3", "Runa Silvestre III"),
    ("runa_seismic_1", "Runa Sísmica I"), ("runa_seismic_2", "Runa Sísmica II"), ("runa_seismic_3", "Runa Sísmica III"),
    # Runas de Arco
    ("runa_tempest_1", "Runa de Tempestade I"), ("runa_tempest_2", "Runa de Tempestade II"), ("runa_tempest_3", "Runa de Tempestade III"),
    ("runa_flame_lightning_1", "Runa de Chamas Raio I"), ("runa_flame_lightning_2", "Runa de Chamas Raio II"), ("runa_flame_lightning_3", "Runa de Chamas Raio III"),
    ("runa_glacial_1", "Runa Glacial I"), ("runa_glacial_2", "Runa Glacial II"), ("runa_glacial_3", "Runa Glacial III"),
    ("runa_void_1", "Runa do Vazio I"), ("runa_void_2", "Runa do Vazio II"), ("runa_void_3", "Runa do Vazio III"),
    ("runa_crimson_1", "Runa Carmesim I"), ("runa_crimson_2", "Runa Carmesim II"), ("runa_crimson_3", "Runa Carmesim III"),
    ("runa_putrid_1", "Runa Pútrida I"), ("runa_putrid_2", "Runa Pútrida II"), ("runa_putrid_3", "Runa Pútrida III"),
    ("runa_zephyr_1", "Runa do Zéfiro I"), ("runa_zephyr_2", "Runa do Zéfiro II"), ("runa_zephyr_3", "Runa do Zéfiro III"),
    ("runa_dawn_1", "Runa da Alvorada I"), ("runa_dawn_2", "Runa da Alvorada II"), ("runa_dawn_3", "Runa da Alvorada III"),
    ("runa_earthquake_1", "Runa de Terremoto I"), ("runa_earthquake_2", "Runa de Terremoto II"), ("runa_earthquake_3", "Runa de Terremoto III"),
    # Runas de Escudo
    ("runa_bastion_1", "Runa de Bastião I"), ("runa_bastion_2", "Runa de Bastião II"), ("runa_bastion_3", "Runa de Bastião III"),
    ("runa_counter_1", "Runa de Contragolpe I"), ("runa_counter_2", "Runa de Contragolpe II"), ("runa_counter_3", "Runa de Contragolpe III"),
    ("runa_mirror_1", "Runa de Espelho I"), ("runa_mirror_2", "Runa de Espelho II"), ("runa_mirror_3", "Runa de Espelho III"),
    # Upgrades
    ("upgrade_vitality_1", "Upgrade de Vitalidade I"), ("upgrade_vitality_2", "Upgrade de Vitalidade II"), ("upgrade_vitality_3", "Upgrade de Vitalidade III"),
    ("upgrade_resistance_1", "Upgrade de Resistência I"), ("upgrade_resistance_2", "Upgrade de Resistência II"), ("upgrade_resistance_3", "Upgrade de Resistência III"),
    ("upgrade_permanent_damage_1", "Upgrade de Dano Permanente I"), ("upgrade_permanent_damage_2", "Upgrade de Dano Permanente II"), ("upgrade_permanent_damage_3", "Upgrade de Dano Permanente III"),
    ("upgrade_unbreaking_1", "Upgrade Inquebrável I"), ("upgrade_unbreaking_2", "Upgrade Inquebrável II"), ("upgrade_unbreaking_3", "Upgrade Inquebrável III"),
    ("upgrade_efficiency_1", "Upgrade de Eficiência I"), ("upgrade_efficiency_2", "Upgrade de Eficiência II"), ("upgrade_efficiency_3", "Upgrade de Eficiência III"),
    ("upgrade_projectile_damage_1", "Upgrade de Dano Projétil I"), ("upgrade_projectile_damage_2", "Upgrade de Dano Projétil II"), ("upgrade_projectile_damage_3", "Upgrade de Dano Projétil III"),
    ("upgrade_reload_speed_1", "Upgrade de Vel. Recarga I"), ("upgrade_reload_speed_2", "Upgrade de Vel. Recarga II"), ("upgrade_reload_speed_3", "Upgrade de Vel. Recarga III"),
    ("upgrade_projectile_speed_1", "Upgrade de Vel. Projétil I"), ("upgrade_projectile_speed_2", "Upgrade de Vel. Projétil II"), ("upgrade_projectile_speed_3", "Upgrade de Vel. Projétil III"),
    ("upgrade_block_absorption_1", "Upgrade de Absorção de Bloqueio I"), ("upgrade_block_absorption_2", "Upgrade de Absorção de Bloqueio II"), ("upgrade_block_absorption_3", "Upgrade de Absorção de Bloqueio III"),
    ("upgrade_steady_guard_1", "Upgrade de Guarda Firme I"), ("upgrade_steady_guard_2", "Upgrade de Guarda Firme II"), ("upgrade_steady_guard_3", "Upgrade de Guarda Firme III"),
    ("upgrade_guard_recovery_1", "Upgrade de Recuperação de Guarda I"), ("upgrade_guard_recovery_2", "Upgrade de Recuperação de Guarda II"), ("upgrade_guard_recovery_3", "Upgrade de Recuperação de Guarda III"),
]

os.makedirs("items", exist_ok=True)

for nome_base, nome_exibicao in itens:
    item_json = {
        "format_version": "1.21.30",
        "minecraft:item": {
            "description": {
                "identifier": f"mod_rpg_rune:{nome_base}",
                "menu_category": {"category": "items"}
            },
            "components": {
                "minecraft:icon": {"texture": nome_base},
                "minecraft:display_name": {"value": nome_exibicao},
                "minecraft:max_stack_size": 1
            }
        }
    }
    with open(f"items/{nome_base}.json", "w", encoding="utf-8") as f:
        json.dump(item_json, f, indent=2, ensure_ascii=False)

print(f"{len(itens)} arquivos de itens criados com sucesso na pasta 'items/'.")
