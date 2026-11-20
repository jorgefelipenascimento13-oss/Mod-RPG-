import { world, system } from "@minecraft/server";
import { getRunaTier, isOnCooldown, setCooldown, getMainhand, healEntity, isValid } from "./utils.js";

function safe(fn) { try { fn(); } catch (e) {} }

world.afterEvents.entityHurt.subscribe((event) => {
  try {
    const { hurtEntity, damage, damageSource } = event;
    // Só ataque corpo a corpo. Dano "override" é o do próprio mod (Relampejante/Eco), então não gera loop.
    if (damageSource.cause !== "entityAttack") return;
    const attacker = damageSource.damagingEntity;
    if (!attacker || attacker.typeId !== "minecraft:player" || hurtEntity.id === attacker.id) return;

    const weapon = getMainhand(attacker);
    if (!weapon) return;

    const vampTier = getRunaTier(weapon, "vampirism");
    if (vampTier > 0) healEntity(attacker, Math.min(6, damage * [0, 0.08, 0.15, 0.22][vampTier]));

    // Se o alvo morreu no golpe, não dá para aplicar efeitos nele
    if (!isValid(hurtEntity)) return;

    const soulTier = getRunaTier(weapon, "soul_fire");
    if (soulTier > 0) {
      safe(() => hurtEntity.addEffect("wither", [0, 60, 100, 160][soulTier], { amplifier: 0 }));
      safe(() => hurtEntity.setOnFire([0, 3, 5, 8][soulTier], true));
    }

    const poisonTier = getRunaTier(weapon, "poison");
    if (poisonTier > 0) {
      safe(() => hurtEntity.addEffect("poison", [0, 80, 100, 120][poisonTier], { amplifier: [0, 0, 1, 2][poisonTier] }));
    }

    const lightTier = getRunaTier(weapon, "lightning");
    if (lightTier > 0 && !isOnCooldown(attacker, "lightning", 80)) {
      safe(() => hurtEntity.applyDamage([0, 3, 6, 10][lightTier], { cause: "override" }));
      if (isValid(hurtEntity)) {
        safe(() => hurtEntity.addEffect("slowness", [0, 5, 8, 12][lightTier], { amplifier: 7, showParticles: false }));
        safe(() => hurtEntity.dimension.spawnParticle("minecraft:electric_spark_particle", hurtEntity.location));
      }
      setCooldown(attacker, "lightning");
    }

    const echoTier = getRunaTier(weapon, "echo");
    if (echoTier > 0 && !isOnCooldown(attacker, "echo", 20) && Math.random() < [0, 0.15, 0.28, 0.40][echoTier]) {
      if (isValid(hurtEntity)) safe(() => hurtEntity.applyDamage(damage * 0.75, { cause: "override" }));
      setCooldown(attacker, "echo");
    }
  } catch (e) {
    console.warn("combate.js erro:", e);
  }
});
