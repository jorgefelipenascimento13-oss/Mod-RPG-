import { system, EquipmentSlot } from "@minecraft/server";

function readTier(item, prefix, id) {
  if (!item) return 0;
  let lore;
  try { lore = item.getLore(); } catch (e) { return 0; }
  const re = new RegExp(`${prefix}: (\\w+) (\\d)`);
  for (const line of lore ?? []) {
    const m = line.replace(/§./g, "").match(re);
    if (m && m[1] === id) return parseInt(m[2]);
  }
  return 0;
}

export function getRunaTier(item, runaId) { return readTier(item, "Runa", runaId); }
export function getUpgradeTier(item, upId) { return readTier(item, "Upgrade", upId); }

// Cooldown em MEMÓRIA. Antes era dynamic property, mas system.currentTick volta
// a 0 quando o mundo é recarregado, e o cooldown salvo ficava "preso" por muito tempo.
const cooldowns = new Map();
export function isOnCooldown(player, key, ticks) {
  const last = cooldowns.get(`${player.id}:${key}`);
  return last !== undefined && system.currentTick - last < ticks;
}
export function setCooldown(player, key) {
  cooldowns.set(`${player.id}:${key}`, system.currentTick);
}

export function getMainhand(player) {
  try {
    const eq = player.getComponent("minecraft:equippable");
    return eq ? eq.getEquipment(EquipmentSlot.Mainhand) : undefined;
  } catch (e) { return undefined; }
}

// isValid é propriedade na API 2.x e método na 1.x
export function isValid(entity) {
  try { return typeof entity.isValid === "function" ? entity.isValid() : !!entity.isValid; }
  catch (e) { return false; }
}

export function knockback(entity, dirX, dirZ, strength, vertical = 0.4) {
  try { entity.applyKnockback({ x: dirX * strength, z: dirZ * strength }, vertical); } // API 2.x
  catch (e) {
    try { entity.applyKnockback(dirX, dirZ, strength, vertical); } catch (e2) {}      // API 1.x
  }
}

export function healEntity(entity, amount) {
  try {
    const h = entity.getComponent("minecraft:health");
    if (!h) return;
    h.setCurrentValue(Math.min(h.effectiveMax, h.currentValue + amount));
  } catch (e) {}
}
