import { world, system, EquipmentSlot } from "@minecraft/server";
import { ModalFormData } from "@minecraft/server-ui";

const NS = "mod_rpg_rune";
const TABLE_ID = `${NS}:mesa_de_runas`;

// ═══════════════════════════════════════════════════════
// LISTAS DE RUNAS E UPGRADES POR CATEGORIA
// ═══════════════════════════════════════════════════════

const RUNAS_ARMA   = ["vampirism","soul_fire","decomposition","poison","bleeding","freezing","lightning","fissure","echo"];
const RUNAS_ARMADURA = ["purification","sylvan","seismic"];
const RUNAS_ARCO   = ["tempest","flame_lightning","glacial","void","crimson","putrid","zephyr","dawn","earthquake"];
const RUNAS_ESCUDO = ["bastion","counter","mirror"];

const NOMES_RUNAS = {
    vampirism: "Vampirismo", soul_fire: "Fogo das Almas", decomposition: "Decomposição",
    poison: "Veneno", bleeding: "Sangramento", freezing: "Congelamento",
    lightning: "Relampejante", fissure: "Fissura", echo: "Eco",
    purification: "Purificação", sylvan: "Silvestre", seismic: "Sísmica",
    tempest: "Tempestade", flame_lightning: "Chamas Raio", glacial: "Glacial",
    void: "Vazio", crimson: "Carmesim", putrid: "Pútrida", zephyr: "Zéfiro",
    dawn: "Alvorada", earthquake: "Terremoto",
    bastion: "Bastião", counter: "Contragolpe", mirror: "Espelho"
};
const NOMES_UPGRADES = {
    vitality: "Vitalidade", resistance: "Resistência", permanent_damage: "Dano Permanente",
    unbreaking: "Inquebrável", efficiency: "Eficiência", projectile_damage: "Dano Projétil",
    reload_speed: "Vel. Recarga", projectile_speed: "Vel. Projétil",
    block_absorption: "Absorção de Bloqueio", steady_guard: "Guarda Firme",
    guard_recovery: "Recuperação de Guarda"
};

// ═══════════════════════════════════════════════════════
// CLASSIFICAÇÃO DO ITEM
// ═══════════════════════════════════════════════════════

function getConfig(item) {
    const id = item.typeId;

    // Paxel (7 variantes) — só ferramenta, sem runas
    if (id.includes("paxel_")) {
        return { runas: [], upgrades: ["unbreaking","efficiency"], maxRunas: 0 };
    }

    // Machados do mod (arma + ferramenta)
    if (id.includes("machado_")) {
        return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","efficiency","unbreaking"], maxRunas: 3 };
    }

    // Demais armas do mod
    const armasMod = ["katana","adaga","espada_longa","hari","dragon_slayer"];
    for (const a of armasMod) {
        if (id.includes(a)) {
            return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","unbreaking"], maxRunas: 3 };
        }
    }

    // Ferramentas de aço
    if (id === `${NS}:aco_sword`) return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","unbreaking"], maxRunas: 3 };
    if (id === `${NS}:aco_axe`)   return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","efficiency","unbreaking"], maxRunas: 3 };
    if (id.startsWith(`${NS}:aco_`)) return { runas: [], upgrades: ["unbreaking","efficiency"], maxRunas: 0 };

    // Vanilla
    if (id === "minecraft:shield") {
        return { runas: RUNAS_ESCUDO, upgrades: ["block_absorption","steady_guard","guard_recovery","unbreaking"], maxRunas: 3 };
    }
    if (id === "minecraft:bow" || id === "minecraft:crossbow") {
        return { runas: RUNAS_ARCO, upgrades: ["projectile_damage","reload_speed","projectile_speed","unbreaking"], maxRunas: 1 };
    }
    if (id.endsWith("_sword")) {
        return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","unbreaking"], maxRunas: 3 };
    }
    if (id.endsWith("_axe")) {
        return { runas: RUNAS_ARMA, upgrades: ["permanent_damage","efficiency","unbreaking"], maxRunas: 3 };
    }
    if (id.endsWith("_helmet") || id.endsWith("_chestplate") ||
        id.endsWith("_leggings") || id.endsWith("_boots")) {
        return { runas: RUNAS_ARMADURA, upgrades: ["vitality","resistance","unbreaking"], maxRunas: 3 };
    }

    return null;
}

// ═══════════════════════════════════════════════════════
// LORE (leitura/escrita)
// ═══════════════════════════════════════════════════════

function parseLore(item) {
    const lore = item.getLore() || [];
    const runas = [], upgrades = [];
    for (const line of lore) {
        const clean = line.replace(/§./g, "");
        let m = clean.match(/Runa: (\w+) (\d)/);
        if (m) { runas.push({ id: m[1], tier: parseInt(m[2]) }); continue; }
        m = clean.match(/Upgrade: (\w+) (\d)/);
        if (m) upgrades.push({ id: m[1], tier: parseInt(m[2]) });
    }
    return { runas, upgrades };
}

function buildLore(runas, upgrades) {
    const out = [];
    for (const r of runas) out.push(`§r§7Runa: ${r.id} ${r.tier}`);
    for (const u of upgrades) out.push(`§r§bUpgrade: ${u.id} ${u.tier}`);
    return out;
}

// ═══════════════════════════════════════════════════════
// UI
// ═══════════════════════════════════════════════════════

export async function openRuneTableUI(player, item) {
    const config = getConfig(item);
    if (!config) {
        player.sendMessage("§cEste item não aceita runas ou upgrades.");
        return;
    }

    const existing = parseLore(item);
    const { runas, upgrades } = existing;

    const form = new ModalFormData().title("§5Mesa de Runas");

    // Labels informativos (contam como formValues? NÃO — label não ocupa slot)
    if (runas.length) {
        form.label(`§eRunas: §f${runas.map(r => `${NOMES_RUNAS[r.id]} ${r.tier}`).join(", ")}`);
    }
    if (upgrades.length) {
        form.label(`§eUpgrades: §f${upgrades.map(u => `${NOMES_UPGRADES[u.id]} ${u.tier}`).join(", ")}`);
    }
    if (config.maxRunas > 0) {
        const livres = config.maxRunas - runas.length;
        form.label(`§aSlots de runa: ${livres}/${config.maxRunas}`);
    }

    // Runa (só se o item suporta)
    const runaOptions = ["§7Nenhuma", ...config.runas.map(r => NOMES_RUNAS[r] || r)];
    if (config.maxRunas > 0) {
        form.dropdown("§6Adicionar Runa", runaOptions, 0);
        form.slider("Tier da Runa (1–3)", 1, 3, 1, 1);
    }

    // Upgrade
    const upOptions = ["§7Nenhum", ...config.upgrades.map(u => NOMES_UPGRADES[u] || u)];
    form.dropdown("§bAdicionar Upgrade", upOptions, 0);
    form.slider("Tier do Upgrade (1–3)", 1, 3, 1, 1);

    // Limpar tudo
    form.toggle("§cRemover todas as runas/upgrades", false);

    const result = await form.show(player);
    if (result.canceled) return;

    // Labels não contam como formValues — só dropdown/slider/toggle contam
    const vals = result.formValues;
    let idx = 0;

    let runaToAdd = null;
    if (config.maxRunas > 0) {
        const runaIdx = vals[idx++];
        const runaTier = vals[idx++];
        if (runaIdx > 0) runaToAdd = { id: config.runas[runaIdx - 1], tier: runaTier };
    }

    const upIdx = vals[idx++];
    const upTier = vals[idx++];
    let upgradeToAdd = null;
    if (upIdx > 0) upgradeToAdd = { id: config.upgrades[upIdx - 1], tier: upTier };

    const clearAll = vals[idx++];

    // Aplicar
    let finalRunas    = clearAll ? [] : [...runas];
    let finalUpgrades = clearAll ? [] : [...upgrades];

    if (runaToAdd) {
        if (finalRunas.some(r => r.id === runaToAdd.id)) {
            player.sendMessage(`§cJá possui a runa ${NOMES_RUNAS[runaToAdd.id]}.`);
            return;
        }
        if (finalRunas.length >= config.maxRunas) {
            player.sendMessage(`§cLimite de ${config.maxRunas} runas atingido.`);
            return;
        }
        finalRunas.push(runaToAdd);
    }

    if (upgradeToAdd) {
        if (finalUpgrades.some(u => u.id === upgradeToAdd.id)) {
            player.sendMessage(`§cJá possui o upgrade ${NOMES_UPGRADES[upgradeToAdd.id]}.`);
            return;
        }
        finalUpgrades.push(upgradeToAdd);
    }

    item.setLore(buildLore(finalRunas, finalUpgrades));
    const eq = player.getComponent("equippable");
    if (eq) eq.setEquipment(EquipmentSlot.Mainhand, item);

    player.sendMessage("§aRunas/upgrades aplicados!");
    player.playSound("random.orb", { volume: 0.6, pitch: 1.5 });
}

// ═══════════════════════════════════════════════════════
// INTERAÇÃO COM A MESA
// ═══════════════════════════════════════════════════════

world.afterEvents.playerInteractWithBlock.subscribe((e) => {
    try {
        if (!e.block || e.block.typeId !== TABLE_ID) return;
        const item = e.itemStack;
        if (!item || item.typeId === TABLE_ID) return;
        system.run(() => openRuneTableUI(e.player, item));
    } catch (err) {
        console.warn("Mesa de Runas erro:", err);
    }
});

console.warn(">>> MESA DE RUNAS CARREGADA <<<");
