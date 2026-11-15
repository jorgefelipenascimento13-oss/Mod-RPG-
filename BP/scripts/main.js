import { world, system, ItemStack, EquipmentSlot } from "@minecraft/server";
import "./infestation.js";
import "./mesa_de_runas.js";

console.warn(">>> MOD RPG RUNE + MOTOR DE COMBATE CARREGADO <<<");

const NS = "mod_rpg_rune";

// ═══════════════════════════════════════════════════════════
// UTILITÁRIOS: LORE, COOLDOWN, KNOCKBACK
// ═══════════════════════════════════════════════════════════

function getRunaTier(item, runaId) {
  if (!item) return 0;
  for (const line of (item.getLore() || [])) {
    const clean = line.replace(/§./g, "");
    const m = clean.match(/Runa: (\w+) (\d)/);
    if (m && m[1] === runaId) return parseInt(m[2]);
  }
  return 0;
}

function getUpgradeTier(item, upId) {
  if (!item) return 0;
  for (const line of (item.getLore() || [])) {
    const clean = line.replace(/§./g, "");
    const m = clean.match(/Upgrade: (\w+) (\d)/);
    if (m && m[1] === upId) return parseInt(m[2]);
  }
  return 0;
}

function isOnCooldown(player, key, ticks) {
  const last = player.getDynamicProperty(`cd_${key}`) ?? 0;
  return (system.currentTick - last) < ticks;
}

function setCooldown(player, key) {
  player.setDynamicProperty(`cd_${key}`, system.currentTick);
}

function getMainhand(player) {
  const eq = player.getComponent("minecraft:equippable");
  return eq ? eq.getEquipment(EquipmentSlot.Mainhand) : null;
}

function knockback(entity, dirX, dirZ, strength, vertical = 0.4) {
  try { entity.applyKnockback(dirX, dirZ, strength, vertical); }
  catch (e) {
    try { entity.applyKnockback({ x: dirX * strength, z: dirZ * strength }, strength); }
    catch (e2) {}
  }
}

function healEntity(entity, amount) {
  try {
    const h = entity.getComponent("minecraft:health");
    if (!h) return;
    h.setCurrentValue(Math.min(h.effectiveMax, h.currentValue + amount));
  } catch (e) {}
}

const ecoActive = new Set();

// ═══════════════════════════════════════════════════════════
// MOTOR DE COMBATE — RUNAS DE ARMA (melee)
// ═══════════════════════════════════════════════════════════

world.afterEvents.entityHurt.subscribe((event) => {
  try {
    const { hurtEntity, damage, damageSource } = event;

    if (damageSource.cause === "override") return;
    if (damageSource.cause !== "entityAttack") return;

    const attacker = damageSource.damagingEntity;
    if (!attacker || attacker.typeId !== "minecraft:player") return;
    if (hurtEntity.id === attacker.id) return;

    const weapon = getMainhand(attacker);
    if (!weapon) return;

    const ecoKey = `${attacker.id}_${hurtEntity.id}`;
    if (ecoActive.has(ecoKey)) { ecoActive.delete(ecoKey); return; }

    // Vampirismo
    const vampTier = getRunaTier(weapon, "vampirism");
    if (vampTier > 0) {
      const pct = [0, 0.08, 0.15, 0.22][vampTier];
      healEntity(attacker, Math.min(6, damage * pct));
    }

    // Fogo das Almas
    const soulTier = getRunaTier(weapon, "soul_fire");
    if (soulTier > 0) {
      const sec = [0, 3, 5, 8][soulTier];
      hurtEntity.addEffect("wither", sec * 20, { amplifier: 0 });
      try { hurtEntity.setOnFire(sec, true); } catch (e) {}
    }

    // Decomposição
    const decompTier = getRunaTier(weapon, "decomposition");
    if (decompTier > 0) {
      const ticks = [0, 60, 80, 100][decompTier];
      const amp = [0, 0, 1, 2][decompTier];
      hurtEntity.addEffect("wither", ticks, { amplifier: amp });
    }

    // Veneno
    const poisonTier = getRunaTier(weapon, "poison");
    if (poisonTier > 0) {
      const ticks = [0, 80, 100, 120][poisonTier];
      const amp = [0, 0, 1, 2][poisonTier];
      hurtEntity.addEffect("poison", ticks, { amplifier: amp });
    }

    // Sangramento
    const bleedTier = getRunaTier(weapon, "bleeding");
    if (bleedTier > 0) {
      const total = [0, 3, 6, 9][bleedTier];
      const perTick = total / 3;
      let ticksLeft = 3;
      const bleedInterval = system.runInterval(() => {
        try {
          if (!hurtEntity.isValid()) { system.clearRun(bleedInterval); return; }
          hurtEntity.applyDamage(perTick, { cause: "override" });
          if (--ticksLeft <= 0) system.clearRun(bleedInterval);
        } catch (e) { system.clearRun(bleedInterval); }
      }, 20);
    }

    // Congelamento
    const freezeTier = getRunaTier(weapon, "freezing");
    if (freezeTier > 0) {
      hurtEntity.addEffect("slowness", 80, { amplifier: [0, 0, 1, 3][freezeTier] });
      hurtEntity.addEffect("weakness", 80, { amplifier: [0, 0, 0, 1][freezeTier] });
    }

    // Relampejante
    const lightTier = getRunaTier(weapon, "lightning");
    if (lightTier > 0 && !isOnCooldown(attacker, "lightning", 80)) {
      const dmg = [0, 3, 6, 10][lightTier];
      const stunTicks = [0, 5, 8, 12][lightTier];
      try { hurtEntity.applyDamage(dmg, { cause: "override" }); } catch (e) {}
      hurtEntity.addEffect("slowness", stunTicks, { amplifier: 7, showParticles: false });
      try {
        hurtEntity.dimension.spawnParticle("minecraft:electric_spark_particle", hurtEntity.location);
        hurtEntity.dimension.playSound("random.explode", hurtEntity.location, { volume: 0.5, pitch: 1.5 });
      } catch (e) {}
      setCooldown(attacker, "lightning");
    }

    // Fissura
    const fissureTier = getRunaTier(weapon, "fissure");
    if (fissureTier > 0) {
      const chance = [0, 0.15, 0.35, 1.0][fissureTier];
      const bonus = [0, 2, 5, 10][fissureTier];
      const cd = fissureTier === 3 ? 30 : 0;
      if (Math.random() < chance && !isOnCooldown(attacker, "fissure", cd)) {
        try { hurtEntity.applyDamage(bonus, { cause: "override" }); } catch (e) {}
        setCooldown(attacker, "fissure");
      }
    }

    // Eco
    const echoTier = getRunaTier(weapon, "echo");
    if (echoTier > 0 && !isOnCooldown(attacker, "echo", 20)) {
      const chance = [0, 0.15, 0.28, 0.40][echoTier];
      if (Math.random() < chance) {
        ecoActive.add(ecoKey);
        try { hurtEntity.applyDamage(damage * 0.75, { cause: "override" }); } catch (e) {}
        setCooldown(attacker, "echo");
        system.runTimeout(() => ecoActive.delete(ecoKey), 2);
      }
    }

    // Dano Permanente
    const permTier = getUpgradeTier(weapon, "permanent_damage");
    if (permTier > 0) {
      try { hurtEntity.applyDamage([0, 3, 6, 10][permTier], { cause: "override" }); } catch (e) {}
    }
  } catch (e) { console.warn("Melee err:", e); }
});

// ═══════════════════════════════════════════════════════════
// MOTOR DE COMBATE — RUNAS DE ARMADURA
// ═══════════════════════════════════════════════════════════

world.afterEvents.entityHurt.subscribe((event) => {
  try {
    const { hurtEntity, damageSource } = event;
    if (hurtEntity.typeId !== "minecraft:player") return;
    if (damageSource.cause === "override") return;

    const player = hurtEntity;
    const attacker = damageSource.damagingEntity;
    if (!attacker || attacker.id === player.id) return;

    const eq = player.getComponent("minecraft:equippable");
    if (!eq) return;

    const armors = [
      eq.getEquipment(EquipmentSlot.Head),
      eq.getEquipment(EquipmentSlot.Chest),
      eq.getEquipment(EquipmentSlot.Legs),
      eq.getEquipment(EquipmentSlot.Feet)
    ].filter(a => a);

    let purifTier = 0, sylvanTier = 0, seismTier = 0;
    for (const a of armors) {
      purifTier = Math.max(purifTier, getRunaTier(a, "purification"));
      sylvanTier = Math.max(sylvanTier, getRunaTier(a, "sylvan"));
      seismTier = Math.max(seismTier, getRunaTier(a, "seismic"));
    }

    if (purifTier >= 1 && !isOnCooldown(player, "purif1", 80)) {
      try { player.removeEffect("poison"); } catch (e) {}
      setCooldown(player, "purif1");
    }
    if (purifTier >= 2 && !isOnCooldown(player, "purif2", 200)) {
      try { player.removeEffect("wither"); } catch (e) {}
      player.addEffect("regeneration", 60, { amplifier: 0 });
      setCooldown(player, "purif2");
    }

    if (sylvanTier >= 1 && !isOnCooldown(player, "sylvan", 30)) {
      try { attacker.applyDamage([0, 2, 4, 7][sylvanTier], { cause: "override" }); } catch (e) {}
      if (sylvanTier >= 2) {
        attacker.addEffect("poison", sylvanTier >= 3 ? 100 : 60, { amplifier: sylvanTier >= 3 ? 1 : 0 });
      }
      setCooldown(player, "sylvan");
    }

    if (seismTier >= 1 && !isOnCooldown(player, "seismic", 100)) {
      const kb = [0, 0.5, 0.8, 1.2][seismTier];
      const radius = [0, 3, 4, 5][seismTier];
      const targets = player.dimension.getEntities({
        location: player.location, maxDistance: radius,
        excludeTypes: ["minecraft:item", "minecraft:xp_orb"]
      });
      for (const t of targets) {
        if (t.id === player.id) continue;
        const dx = t.location.x - player.location.x;
        const dz = t.location.z - player.location.z;
        const len = Math.sqrt(dx*dx + dz*dz) || 1;
        knockback(t, dx/len, dz/len, kb, 0.3);
      }
      setCooldown(player, "seismic");
    }
  } catch (e) {}
});

// ═══════════════════════════════════════════════════════════
// MOTOR DE COMBATE — RUNAS DE ARCO
// ═══════════════════════════════════════════════════════════

world.afterEvents.projectileHitEntity.subscribe((event) => {
  try {
    const hitInfo = event.getEntityHit();
    if (!hitInfo) return;
    const target = hitInfo.entity;
    if (!target) return;

    const player = event.source;
    if (!player || player.typeId !== "minecraft:player") return;

    const weapon = getMainhand(player);
    if (!weapon) return;
    const isCrossbow = weapon.typeId === "minecraft:crossbow";
    const cd = isCrossbow ? 1.5 : 1.0;
    const baseDmg = event.damage || 5;

    // Tempestade
    const tempTier = getRunaTier(weapon, "tempest");
    if (tempTier > 0 && !isOnCooldown(player, "tempest", Math.floor(120 * cd))) {
      try { target.applyDamage([0, 2, 4, 6][tempTier], { cause: "override" }); } catch (e) {}
      if (tempTier >= 2) target.addEffect("slowness", 40, { amplifier: 0 });
      if (tempTier >= 3) {
        target.addEffect("slowness", 60, { amplifier: 1 });
        target.addEffect("slowness", 5, { amplifier: 7, showParticles: false });
      }
      try { target.dimension.spawnParticle("minecraft:electric_spark_particle", target.location); } catch (e) {}
      setCooldown(player, "tempest");
    }

    // Chamas Raio
    const flameTier = getRunaTier(weapon, "flame_lightning");
    if (flameTier > 0 && !isOnCooldown(player, "flame", Math.floor(100 * cd))) {
      const dmg = [0, 2, 4, 6][flameTier];
      const sec = [0, 2, 3, 5][flameTier];
      try { target.applyDamage(dmg, { cause: "override" }); } catch (e) {}
      try { target.setOnFire(sec, true); } catch (e) {}
      setCooldown(player, "flame");
    }

    // Glacial
    const glacialTier = getRunaTier(weapon, "glacial");
    if (glacialTier > 0 && !isOnCooldown(player, "glacial", Math.floor(120 * cd))) {
      target.addEffect("slowness", [0, 20, 40, 60][glacialTier], { amplifier: [0, 0, 1, 3][glacialTier] });
      setCooldown(player, "glacial");
    }

    // Carmesim
    const crimTier = getRunaTier(weapon, "crimson");
    if (crimTier > 0) {
      healEntity(player, Math.min(4, baseDmg * [0, 0.10, 0.20, 0.30][crimTier]));
    }

    // Pútrida
    const putridTier = getRunaTier(weapon, "putrid");
    if (putridTier > 0 && !isOnCooldown(player, "putrid", Math.floor(160 * cd))) {
      const radius = [0, 1.5, 2.5, 3][putridTier];
      const sec = [0, 3, 5, 7][putridTier];
      const amp = [0, 0, 1, 1][putridTier];
      const victims = target.dimension.getEntities({
        location: target.location, maxDistance: radius,
        excludeTypes: ["minecraft:item", "minecraft:xp_orb"]
      });
      for (const v of victims) v.addEffect("poison", sec * 20, { amplifier: amp });
      if (putridTier >= 3) target.addEffect("nausea", 60, { amplifier: 0 });
      setCooldown(player, "putrid");
    }

    // Zéfiro
    const zephTier = getRunaTier(weapon, "zephyr");
    if (zephTier > 0 && !isOnCooldown(player, "zephyr", Math.floor(100 * cd))) {
      const kb = [0, 0.8, 1.2, 1.8][zephTier];
      const dx = target.location.x - player.location.x;
      const dz = target.location.z - player.location.z;
      const len = Math.sqrt(dx*dx + dz*dz) || 1;
      knockback(target, dx/len, dz/len, kb, 0.5);
      if (zephTier >= 3) target.addEffect("levitation", 10, { amplifier: 0 });
      setCooldown(player, "zephyr");
    }

    // Alvorada
    const dawnTier = getRunaTier(weapon, "dawn");
    if (dawnTier > 0 && !isOnCooldown(player, "dawn", Math.floor(240 * cd))) {
      const isUndead = target.matches({ families: ["undead"] });
      if (isUndead) {
        try { target.applyDamage([0, 3, 6, 10][dawnTier], { cause: "override" }); } catch (e) {}
      } else {
        healEntity(player, [0, 2, 4, 6][dawnTier]);
      }
      if (dawnTier >= 3) player.addEffect("regeneration", 60, { amplifier: 0 });
      setCooldown(player, "dawn");
    }

    // Dano Projétil
    const projTier = getUpgradeTier(weapon, "projectile_damage");
    if (projTier > 0) {
      try { target.applyDamage([0, 2, 4, 6][projTier], { cause: "override" }); } catch (e) {}
    }
  } catch (e) {}
});

world.afterEvents.projectileHitBlock.subscribe((event) => {
  try {
    const hit = event.getBlockHit();
    if (!hit) return;
    const player = event.source;
    if (!player || player.typeId !== "minecraft:player") return;

    const weapon = getMainhand(player);
    if (!weapon) return;

    const eqTier = getRunaTier(weapon, "earthquake");
    if (eqTier > 0 && !isOnCooldown(player, "earthquake", 120)) {
      const radius = [0, 3, 5, 7][eqTier];
      const kb = [0, 0.4, 0.6, 0.8][eqTier];
      const loc = hit.block.location;
      const victims = player.dimension.getEntities({
        location: { x: loc.x+0.5, y: loc.y+0.5, z: loc.z+0.5 },
        maxDistance: radius,
        excludeTypes: ["minecraft:item", "minecraft:xp_orb"]
      });
      for (const v of victims) {
        if (v.id === player.id) continue;
        const dx = v.location.x - loc.x;
        const dz = v.location.z - loc.z;
        const len = Math.sqrt(dx*dx + dz*dz) || 1;
        knockback(v, dx/len, dz/len, kb, 0.3);
        if (eqTier >= 3) v.addEffect("slowness", 5, { amplifier: 7, showParticles: false });
      }
      setCooldown(player, "earthquake");
    }
  } catch (e) {}
});

// ═══════════════════════════════════════════════════════════
// UPGRADES PASSIVOS
// ═══════════════════════════════════════════════════════════

system.runInterval(() => {
  try {
    for (const player of world.getAllPlayers()) {
      const eq = player.getComponent("minecraft:equippable");
      if (!eq) continue;

      const armors = [
        eq.getEquipment(EquipmentSlot.Head),
        eq.getEquipment(EquipmentSlot.Chest),
        eq.getEquipment(EquipmentSlot.Legs),
        eq.getEquipment(EquipmentSlot.Feet)
      ].filter(a => a);

      let totalVit = 0, maxRes = 0, t3Pieces = 0;
      for (const a of armors) {
        const v = getUpgradeTier(a, "vitality");
        if (v > 0) {
          totalVit += [0, 2, 6, 10][v];
          if (v === 3) t3Pieces++;
        }
        maxRes = Math.max(maxRes, getUpgradeTier(a, "resistance"));
      }
      if (t3Pieces === 4) totalVit += 10;

      if (totalVit > 0) {
        const amp = Math.max(0, Math.floor(totalVit / 4) - 1);
        player.addEffect("health_boost", 60, { amplifier: amp, showParticles: false });
      }
      if (maxRes > 0) {
        player.addEffect("resistance", 60, {
          amplifier: [0, 0, 1, 3][maxRes], showParticles: false
        });
      }

      const main = eq.getEquipment(EquipmentSlot.Mainhand);
      if (!main) continue;

      const effTier = getUpgradeTier(main, "efficiency");
      if (effTier > 0) {
        player.addEffect("haste", 60, {
          amplifier: [0, 0, 1, 2][effTier], showParticles: false
        });
      }

      const unbTier = getUpgradeTier(main, "unbreaking");
      if (unbTier > 0) {
        try {
          const dur = main.getComponent("minecraft:durability");
          if (dur && dur.damage > 0) {
            if (Math.random() < [0, 0.5, 0.85, 1.0][unbTier]) {
              dur.damage = Math.max(0, dur.damage - 1);
              eq.setEquipment(EquipmentSlot.Mainhand, main);
            }
          }
        } catch (e) {}
      }
    }
  } catch (e) {}
}, 40);

// ═══════════════════════════════════════════════════════════
// TORRES INDUSTRIAIS
// ═══════════════════════════════════════════════════════════

const TOWER_TYPES = {
  PLANTER:    `${NS}:industrial_planter`,
  FERTILIZER: `${NS}:industrial_fertilizer`,
  HARVESTER:  `${NS}:industrial_harvester`
};
const TOWER_IDS = new Set(Object.values(TOWER_TYPES));
const AREA_RADIUS = 10;
const activeTowers = new Map();

function buildScanPattern(radius) {
  const pos = [{ dx: 0, dz: 0 }];
  for (let r = 1; r <= radius; r++) {
    const circ = Math.max(8, Math.ceil(2 * Math.PI * r));
    for (let i = 0; i < circ; i++) {
      const a = (i / circ) * Math.PI * 2;
      pos.push({ dx: Math.round(Math.cos(a) * r), dz: Math.round(Math.sin(a) * r) });
    }
  }
  return pos;
}
const SCAN_PATTERN = buildScanPattern(AREA_RADIUS);

function getRingPositions(radius) {
  if (radius === 0) return [{ dx: 0, dz: 0 }];
  const pos = [];
  const circ = Math.max(8, Math.ceil(2 * Math.PI * radius));
  for (let i = 0; i < circ; i++) {
    const a = (i / circ) * Math.PI * 2;
    pos.push({ dx: Math.round(Math.cos(a) * radius), dz: Math.round(Math.sin(a) * radius) });
  }
  return pos;
}

const PLANTABLE = {
  "minecraft:wheat_seeds":       { crop: "minecraft:wheat",            soil: ["farmland","dirt","grass_block"] },
  "minecraft:carrot":            { crop: "minecraft:carrots",          soil: ["farmland","dirt","grass_block"] },
  "minecraft:potato":            { crop: "minecraft:potatoes",         soil: ["farmland","dirt","grass_block"] },
  "minecraft:beetroot_seeds":    { crop: "minecraft:beetroot",         soil: ["farmland","dirt","grass_block"] },
  "minecraft:melon_seeds":       { crop: "minecraft:melon_stem",       soil: ["farmland","dirt","grass_block"] },
  "minecraft:pumpkin_seeds":     { crop: "minecraft:pumpkin_stem",     soil: ["farmland","dirt","grass_block"] },
  "minecraft:torchflower_seeds": { crop: "minecraft:torchflower_crop", soil: ["farmland","dirt","grass_block"] },
  "minecraft:pitcher_pod":       { crop: "minecraft:pitcher_crop",     soil: ["farmland","dirt","grass_block"] },
  "minecraft:nether_wart":       { crop: "minecraft:nether_wart",      soil: ["soul_sand"] },
  "minecraft:crimson_fungus":    { crop: "minecraft:crimson_fungus",   soil: ["crimson_nylium"] },
  "minecraft:warped_fungus":     { crop: "minecraft:warped_fungus",    soil: ["warped_nylium"] },
  "minecraft:sugar_cane":        { crop: "minecraft:reeds",            soil: ["sand","dirt","grass_block"] },
  "minecraft:reeds":             { crop: "minecraft:reeds",            soil: ["sand","dirt","grass_block"] },
  "minecraft:bamboo":            { crop: "minecraft:bamboo",           soil: ["sand","dirt","grass_block"] },
  "minecraft:cactus":            { crop: "minecraft:cactus",           soil: ["sand"] },
  "minecraft:sweet_berries":     { crop: "minecraft:sweet_berry_bush", soil: ["dirt","grass_block","podzol"] },
  "minecraft:oak_sapling":       { crop: "minecraft:oak_sapling",      soil: ["dirt","grass_block","podzol"] },
  "minecraft:spruce_sapling":    { crop: "minecraft:spruce_sapling",   soil: ["dirt","grass_block","podzol"] },
  "minecraft:birch_sapling":     { crop: "minecraft:birch_sapling",    soil: ["dirt","grass_block","podzol"] },
  "minecraft:jungle_sapling":    { crop: "minecraft:jungle_sapling",   soil: ["dirt","grass_block","podzol"] },
  "minecraft:acacia_sapling":    { crop: "minecraft:acacia_sapling",   soil: ["dirt","grass_block","podzol"] },
  "minecraft:dark_oak_sapling":  { crop: "minecraft:dark_oak_sapling", soil: ["dirt","grass_block","podzol"] },
  "minecraft:cherry_sapling":    { crop: "minecraft:cherry_sapling",   soil: ["dirt","grass_block","podzol"] },
  "minecraft:mangrove_propagule":{ crop: "minecraft:mangrove_propagule", soil: ["dirt","grass_block","podzol"] }
};

const HARVESTABLE = {
  "minecraft:wheat":            { drop: "minecraft:wheat",           extra: ["minecraft:wheat_seeds"],   growth: true },
  "minecraft:carrots":          { drop: "minecraft:carrot",          extra: [],                          growth: true },
  "minecraft:potatoes":         { drop: "minecraft:potato",          extra: [],                          growth: true },
  "minecraft:beetroot":         { drop: "minecraft:beetroot",        extra: ["minecraft:beetroot_seeds"], growth: true },
  "minecraft:nether_wart":      { drop: "minecraft:nether_wart",     extra: [],                          growth: true },
  "minecraft:sweet_berry_bush": { drop: "minecraft:sweet_berries",   extra: [],                          growth: true },
  "minecraft:torchflower_crop": { drop: "minecraft:torchflower",     extra: [],                          growth: true },
  "minecraft:pitcher_crop":     { drop: "minecraft:pitcher_plant",   extra: [],                          growth: true },
  "minecraft:melon":            { drop: "minecraft:melon",           extra: [],                          growth: false },
  "minecraft:pumpkin":          { drop: "minecraft:pumpkin",         extra: [],                          growth: false }
};

const STACKABLE = new Set(["minecraft:cactus", "minecraft:bamboo", "minecraft:reeds"]);
const TREE_LOGS = new Set([
  "minecraft:oak_log","minecraft:spruce_log","minecraft:birch_log","minecraft:jungle_log",
  "minecraft:acacia_log","minecraft:dark_oak_log","minecraft:cherry_log","minecraft:mangrove_log"
]);

function getGrowth(block) {
  try {
    const s = block.permutation.getAllStates();
    return s["growth"] ?? s["growth_stage"] ?? s["age"] ?? null;
  } catch (e) { return null; }
}
function isMature(block) {
  const g = getGrowth(block);
  if (g === null) return false;
  return g >= 7 || (block.typeId.includes("nether_wart") && g >= 3);
}
function forceMature(block) {
  try {
    if (block.typeId.includes("nether_wart")) {
      block.setPermutation(block.permutation.withState("age", 3));
      return true;
    }
    block.setPermutation(block.permutation.withState("growth", 7));
    return true;
  } catch (e) { return false; }
}

function getAdjacentChest(dim, loc) {
  try {
    for (const d of [
      {x:1,y:0,z:0},{x:-1,y:0,z:0},{x:0,y:0,z:1},
      {x:0,y:0,z:-1},{x:0,y:1,z:0},{x:0,y:-1,z:0}
    ]) {
      const b = dim.getBlock({ x: loc.x+d.x, y: loc.y+d.y, z: loc.z+d.z });
      if (b && (b.typeId === "minecraft:chest" || b.typeId === "minecraft:barrel")) {
        const inv = b.getComponent("inventory");
        if (inv?.container) return inv.container;
      }
    }
  } catch (e) {}
  return null;
}
function takeFromChest(c, typeId, amount = 1) {
  try {
    for (let i = 0; i < c.size; i++) {
      const it = c.getItem(i);
      if (it && it.typeId === typeId) {
        if (it.amount > amount) { it.amount -= amount; c.setItem(i, it); }
        else c.setItem(i, undefined);
        return true;
      }
    }
  } catch (e) {}
  return false;
}
function putInChest(c, typeId, amount = 1) {
  try {
    let rem = amount;
    for (let i = 0; i < c.size && rem > 0; i++) {
      const it = c.getItem(i);
      if (!it) {
        const a = Math.min(rem, 64);
        c.setItem(i, new ItemStack(typeId, a));
        rem -= a;
      } else if (it.typeId === typeId && it.amount < 64) {
        const a = Math.min(64 - it.amount, rem);
        it.amount += a;
        c.setItem(i, it);
        rem -= a;
      }
    }
    return rem === 0;
  } catch (e) { return false; }
}

function getTowerKey(dim, loc) { return `${loc.x},${loc.y},${loc.z},${dim.id}`; }
function registerTower(dim, loc, type) {
  const key = getTowerKey(dim, loc);
  if (!activeTowers.has(key)) {
    activeTowers.set(key, {
      type, location: { x: loc.x, y: loc.y, z: loc.z }, dimension: dim,
      cursor: 0, waveRing: 0, lastAction: 0
    });
  }
}
function scanNearby(player) {
  try {
    const dim = player.dimension;
    const p = player.location;
    for (let x = -12; x <= 12; x++)
      for (let y = -3; y <= 3; y++)
        for (let z = -12; z <= 12; z++) {
          const loc = { x: Math.floor(p.x)+x, y: Math.floor(p.y)+y, z: Math.floor(p.z)+z };
          const b = dim.getBlock(loc);
          if (b && TOWER_IDS.has(b.typeId)) registerTower(dim, loc, b.typeId);
        }
  } catch (e) {}
}

world.afterEvents.playerSpawn.subscribe(e => { if (e.initialSpawn) scanNearby(e.player); });
world.afterEvents.playerPlaceBlock.subscribe(e => {
  if (TOWER_IDS.has(e.block.typeId)) registerTower(e.dimension, e.block.location, e.block.typeId);
});
world.afterEvents.playerBreakBlock.subscribe(e => {
  if (TOWER_IDS.has(e.brokenBlockPermutation.type.id)) {
    activeTowers.delete(getTowerKey(e.dimension, e.block.location));
  }
});

system.runInterval(() => {
  try {
    const now = system.currentTick;
    for (const [key, tower] of activeTowers.entries()) {
      const { type, location, dimension } = tower;
      const self = dimension.getBlock(location);
      if (!self || self.typeId !== type) { activeTowers.delete(key); continue; }

      const chest = getAdjacentChest(dimension, location);
      if (!chest) continue;
      const groundY = location.y - 1;

      if (type === TOWER_TYPES.PLANTER) {
        if (now - tower.lastAction < 4) continue;
        const pos = SCAN_PATTERN[tower.cursor % SCAN_PATTERN.length];
        tower.cursor = (tower.cursor + 1) % SCAN_PATTERN.length;
        tower.lastAction = now;

        const soilLoc = { x: location.x+pos.dx, y: groundY, z: location.z+pos.dz };
        const cropLoc = { x: soilLoc.x, y: groundY+1, z: soilLoc.z };
        const soil = dimension.getBlock(soilLoc);
        const above = dimension.getBlock(cropLoc);
        if (!soil || !above || above.typeId !== "minecraft:air") continue;

        let seedType = null, info = null;
        for (let i = 0; i < chest.size; i++) {
          const it = chest.getItem(i);
          if (it && PLANTABLE[it.typeId]) { seedType = it.typeId; info = PLANTABLE[it.typeId]; break; }
        }
        if (!seedType) continue;
        if (!info.soil.some(s => soil.typeId === `minecraft:${s}`)) continue;

        if (takeFromChest(chest, seedType, 1)) {
          try {
            above.setType(info.crop);
            dimension.spawnParticle("minecraft:crop_growth_emitter",
              { x: cropLoc.x+0.5, y: cropLoc.y+0.3, z: cropLoc.z+0.5 });
          } catch (e) {}
        }
      }

      if (type === TOWER_TYPES.FERTILIZER) {
        if (now - tower.lastAction < 30) continue;
        tower.lastAction = now;

        const ring = getRingPositions(tower.waveRing || 0);
        let grown = 0;
        const maxGrow = 3;

        for (const pos of ring) {
          if (grown >= maxGrow) break;
          const cropLoc = { x: location.x+pos.dx, y: groundY+1, z: location.z+pos.dz };
          const crop = dimension.getBlock(cropLoc);
          if (!crop || crop.typeId === "minecraft:air") continue;
          if (isMature(crop)) continue;
          const isKnown = Object.values(PLANTABLE).some(p => p.crop === crop.typeId);
          if (!isKnown) continue;

          if (takeFromChest(chest, "minecraft:bone_meal", 1)) {
            forceMature(crop);
            grown++;
            try {
              dimension.spawnParticle("minecraft:villager_happy",
                { x: cropLoc.x+0.5, y: cropLoc.y+0.5, z: cropLoc.z+0.5 });
            } catch (e) {}
          } else break;
        }

        for (const pos of ring.slice(0, 6)) {
          try {
            dimension.spawnParticle("minecraft:crop_growth_emitter",
              { x: location.x+pos.dx+0.5, y: groundY+1.2, z: location.z+pos.dz+0.5 });
          } catch (e) {}
        }

        tower.waveRing = ((tower.waveRing || 0) + 1) % (AREA_RADIUS + 1);
      }

      if (type === TOWER_TYPES.HARVESTER) {
        if (now - tower.lastAction < 4) continue;
        const pos = SCAN_PATTERN[tower.cursor % SCAN_PATTERN.length];
        tower.cursor = (tower.cursor + 1) % SCAN_PATTERN.length;
        tower.lastAction = now;

        const cropLoc = { x: location.x+pos.dx, y: groundY+1, z: location.z+pos.dz };
        const above = dimension.getBlock(cropLoc);
        if (!above || above.typeId === "minecraft:air") continue;
        const cropId = above.typeId;

        if (TREE_LOGS.has(cropId)) {
          let y = cropLoc.y;
          for (let i = 0; i < 12; i++) {
            const b = dimension.getBlock({ x: cropLoc.x, y, z: cropLoc.z });
            if (!b || !TREE_LOGS.has(b.typeId)) break;
            putInChest(chest, b.typeId, 1);
            b.setType("minecraft:air");
            y++;
          }
          continue;
        }

        if (STACKABLE.has(cropId)) {
          let h = 0;
          for (let k = 0; k < 8; k++) {
            const b = dimension.getBlock({ x: cropLoc.x, y: cropLoc.y+k, z: cropLoc.z });
            if (b && b.typeId === cropId) h++; else break;
          }
          if (h >= 2) {
            for (let k = h-1; k >= 1; k--) {
              const b = dimension.getBlock({ x: cropLoc.x, y: cropLoc.y+k, z: cropLoc.z });
              if (b) { putInChest(chest, cropId, 1); b.setType("minecraft:air"); }
            }
          }
          continue;
        }

        const info = HARVESTABLE[cropId];
        if (!info) continue;
        if (info.growth && !isMature(above)) continue;
        try {
          above.setType("minecraft:air");
          putInChest(chest, info.drop, 1);
          for (const e of info.extra) putInChest(chest, e, 1);
        } catch (e) {}
      }
    }
  } catch (e) {}
}, 1);

// ═══════════════════════════════════════════════════════════
// PAXEL — DURABILIDADE INFINITA + ENCANTAMENTOS
// ═══════════════════════════════════════════════════════════

const paxelEnchanted = new Set();
system.runInterval(() => {
  try {
    for (const player of world.getAllPlayers()) {
      const eq = player.getComponent("minecraft:equippable");
      if (!eq) continue;
      const main = eq.getEquipment(EquipmentSlot.Mainhand);
      if (!main || !main.typeId.startsWith(`${NS}:paxel_`)) continue;

      try {
        const dur = main.getComponent("minecraft:durability");
        if (dur && dur.damage > 0) {
          dur.damage = 0;
          eq.setEquipment(EquipmentSlot.Mainhand, main);
        }
      } catch (e) {}

      const sig = `${player.id}:${main.typeId}`;
      if (!paxelEnchanted.has(sig)) {
        player.runCommandAsync("enchant @s sharpness 5");
        player.runCommandAsync("enchant @s efficiency 5");
        player.runCommandAsync("enchant @s unbreaking 3");
        player.runCommandAsync("enchant @s mending 1");
        paxelEnchanted.add(sig);
      }
    }
  } catch (e) {}
}, 20);

// ═══════════════════════════════════════════════════════════
// VEIN MINE
// ═══════════════════════════════════════════════════════════

world.afterEvents.playerBreakBlock.subscribe((e) => {
  try {
    const { player, brokenBlockPermutation, block, dimension } = e;
    const eq = player.getComponent("minecraft:equippable");
    if (!eq) return;
    const main = eq.getEquipment(EquipmentSlot.Mainhand);
    if (!main || !main.typeId.startsWith(`${NS}:paxel_`)) return;
    if (!player.isSneaking) return;

    const blockTypeId = brokenBlockPermutation.type.id;
    const initialLoc = block.location;
    const queue = [initialLoc];
    const visited = new Set();
    let count = 0;
    const maxBlocks = 128;

    system.run(() => {
      try {
        while (queue.length && count < maxBlocks) {
          const loc = queue.shift();
          const k = `${loc.x},${loc.y},${loc.z}`;
          if (visited.has(k)) continue;
          visited.add(k);
          const target = dimension.getBlock(loc);
          if (!target) continue;

          const isStart = (loc.x === initialLoc.x && loc.y === initialLoc.y && loc.z === initialLoc.z);
          if (isStart || target.typeId === blockTypeId) {
            if (!isStart) {
              try { dimension.runCommandAsync(`setblock ${loc.x} ${loc.y} ${loc.z} air destroy`); } catch (er) {}
            }
            count++;
            for (const n of [
              { x: loc.x+1, y: loc.y, z: loc.z },
              { x: loc.x-1, y: loc.y, z: loc.z },
              { x: loc.x, y: loc.y+1, z: loc.z },
              { x: loc.x, y: loc.y-1, z: loc.z },
              { x: loc.x, y: loc.y, z: loc.z+1 },
              { x: loc.x, y: loc.y, z: loc.z-1 }
            ]) queue.push(n);
          }
        }
      } catch (er) {}
    });
  } catch (e) {}
});

// ═══════════════════════════════════════════════════════════
// AÇÕES FARM DO PAXEL
// ═══════════════════════════════════════════════════════════

const STRIPPED_LOGS = {
  "minecraft:oak_log":"minecraft:stripped_oak_log",
  "minecraft:spruce_log":"minecraft:stripped_spruce_log",
  "minecraft:birch_log":"minecraft:stripped_birch_log",
  "minecraft:jungle_log":"minecraft:stripped_jungle_log",
  "minecraft:acacia_log":"minecraft:stripped_acacia_log",
  "minecraft:dark_oak_log":"minecraft:stripped_dark_oak_log",
  "minecraft:mangrove_log":"minecraft:stripped_mangrove_log",
  "minecraft:cherry_log":"minecraft:stripped_cherry_log",
  "minecraft:crimson_stem":"minecraft:stripped_crimson_stem",
  "minecraft:warped_stem":"minecraft:stripped_warped_stem"
};
const VALID_SOILS = new Set([
  "minecraft:grass_block","minecraft:dirt","minecraft:dirt_with_roots","minecraft:coarse_dirt"
]);

world.beforeEvents.itemUseOn.subscribe(e => {
  try {
    const { itemStack, block } = e;
    if (!itemStack || !itemStack.typeId.startsWith(`${NS}:paxel_`)) return;
    if (!block) return;
    const dim = block.dimension;
    const typeId = block.typeId;

    if (STRIPPED_LOGS[typeId]) {
      const stripped = STRIPPED_LOGS[typeId];
      system.run(() => {
        try {
          const b = dim.getBlock(block.location);
          if (b && b.typeId === typeId) b.setType(stripped);
        } catch (er) {}
      });
      return;
    }

    if (VALID_SOILS.has(typeId)) {
      const c = block.location;
      system.run(() => {
        try {
          for (let x = -1; x <= 1; x++)
            for (let z = -1; z <= 1; z++) {
              const loc = { x: c.x+x, y: c.y, z: c.z+z };
              const b = dim.getBlock(loc);
              if (b && VALID_SOILS.has(b.typeId)) {
                const above = dim.getBlock({ x: loc.x, y: loc.y+1, z: loc.z });
                if (above && (above.typeId === "minecraft:air" || above.typeId.includes("grass")))
                  b.setType("minecraft:farmland");
              }
            }
        } catch (er) {}
      });
    }
  } catch (e) {}
});

console.warn(">>> TODOS OS MÓDULOS CARREGADOS: COMBATE + INDÚSTRIA + PAXEL + VEIN MINE <<<");
