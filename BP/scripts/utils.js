import { system, EquipmentSlot } from "@minecraft/server";

export function getRunaTier(item, runaId) {
  if (!item) return 0;
  for (const line of (item.getLore() || [])) {
    const clean = line.replace(/§./g, "");
    const m = clean.match(/Runa: (\w+) (\d)/);
    if (m && m[1] === runaId) return parseInt(m[2]);
  }
  return 0;
}

export function getUpgradeTier(item, upId) {
  if (!item) return 0;
  for (const line of (item.getLore() || [])) {
    const clean = line.replace(/§./g, "");
    const m = clean.match(/Upgrade: (\w+) (\d)/);
    if (m && m[1] === upId) return parseInt(m[2]);
  }
  return 0;
}

export function isOnCooldown(player, key, ticks) {
  const last = player.getDynamicProperty(`cd_${key}`) ?? 0;
  return (system.currentTick - last) < ticks;
}

export function setCooldown(player, key) {
  player.setDynamicProperty(`cd_${key}`, system.currentTick);
}

export function getMainhand(player) {
  const eq = player.getComponent("minecraft:equippable");
  return eq ? eq.getEquipment(EquipmentSlot.Mainhand) : null;
}

export function knockback(entity, dirX, dirZ, strength, vertical = 0.4) {
  try { entity.applyKnockback(dirX, dirZ, strength, vertical); }
  catch (e) {
    try { entity.applyKnockback({ x: dirX * strength, z: dirZ * strength }, strength); }
    catch (e2) {}
  }
}

export function healEntity(entity, amount) {
  try {
    const h = entity.getComponent("minecraft:health");
    if (!h) return;
    h.setCurrentValue(Math.min(h.effectiveMax, h.currentValue + amount));
  } catch (e) {}
}
