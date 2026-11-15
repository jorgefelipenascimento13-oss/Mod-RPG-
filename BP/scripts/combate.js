import { world, system, EquipmentSlot } from "@minecraft/server";
import { getRunaTier, getUpgradeTier, isOnCooldown, setCooldown, getMainhand, knockback, healEntity } from "./utils.js";

const ecoActive = new Set();

world.afterEvents.entityHurt.subscribe((event) => {
  try {
    const { hurtEntity, damage, damageSource } = event;
    if (damageSource.cause === "override" || damageSource.cause !== "entityAttack") return;
    const attacker = damageSource.damagingEntity;
    if (!attacker || attacker.typeId !== "minecraft:player" || hurtEntity.id === attacker.id) return;
    const weapon = getMainhand(attacker);
    if (!weapon) return;

    const ecoKey = `${attacker.id}_${hurtEntity.id}`;
    if (ecoActive.has(ecoKey)) { ecoActive.delete(ecoKey); return; }

    const vampTier = getRunaTier(weapon, "vampirism");
    if (vampTier > 0) healEntity(attacker, Math.min(6, damage * [0, 0.08, 0.15, 0.22][vampTier]));

    const soulTier = getRunaTier(weapon, "soul_fire");
    if (soulTier > 0) {
      hurtEntity.addEffect("wither", [0, 60, 100, 160][soulTier], { amplifier: 0 });
      try { hurtEntity.setOnFire([0, 3, 5, 8][soulTier], true); } catch (e) {}
    }

    const poisonTier = getRunaTier(weapon, "poison");
    if (poisonTier > 0) hurtEntity.addEffect("poison", [0, 80, 100, 120][poisonTier], { amplifier: [0, 0, 1, 2][poisonTier] });

    const lightTier = getRunaTier(weapon, "lightning");
    if (lightTier > 0 && !isOnCooldown(attacker, "lightning", 80)) {
      try { hurtEntity.applyDamage([0, 3, 6, 10][lightTier], { cause: "override" }); } catch (e) {}
      hurtEntity.addEffect("slowness", [0, 5, 8, 12][lightTier], { amplifier: 7, showParticles: false });
      try { hurtEntity.dimension.spawnParticle("minecraft:electric_spark_particle", hurtEntity.location); } catch (e) {}
      setCooldown(attacker, "lightning");
    }

    const echoTier = getRunaTier(weapon, "echo");
    if (echoTier > 0 && !isOnCooldown(attacker, "echo", 20) && Math.random() < [0, 0.15, 0.28, 0.40][echoTier]) {
      ecoActive.add(ecoKey);
      try { hurtEntity.applyDamage(damage * 0.75, { cause: "override" }); } catch (e) {}
      setCooldown(attacker, "echo");
      system.runTimeout(() => ecoActive.delete(ecoKey), 2);
    }
  } catch (e) {}
});
