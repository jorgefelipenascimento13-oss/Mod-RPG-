import { world, system } from "@minecraft/server";

const ZONES_KEY = "mod_rpg_rune:zones";
const SPAWN_INTERVAL = 40;     // 2s entre spawns
const MAX_MOBS_IN_ZONE = 15;   // cap por zona
const ZONE_RADIUS = 4;         // 8x8 → raio 4

// Mobs por dimensão (slime excluído conforme pedido)
const MOBS = {
  "minecraft:overworld": [
    "minecraft:zombie", "minecraft:skeleton", "minecraft:creeper",
    "minecraft:spider", "minecraft:cave_spider", "minecraft:enderman",
    "minecraft:witch", "minecraft:drowned", "minecraft:husk",
    "minecraft:stray", "minecraft:silverfish"
  ],
  "minecraft:nether": [
    "minecraft:zombie_pigman", "minecraft:blaze", "minecraft:magma_cube",
    "minecraft:wither_skeleton", "minecraft:hoglin", "minecraft:piglin",
    "minecraft:zoglin"
  ],
  "minecraft:the_end": [
    "minecraft:enderman", "minecraft:endermite"
  ]
};

// ─── Persistência ────────────────────────────────────────
function getZones() {
  try {
    const raw = world.getDynamicProperty(ZONES_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) { return []; }
}

function saveZones(zones) {
  world.setDynamicProperty(ZONES_KEY, JSON.stringify(zones));
}

// ─── Criação da zona ────────────────────────────────────
function createZone(dimension, block) {
  const zones = getZones();
  zones.push({
    id: `${Date.now()}_${Math.floor(Math.random() * 99999)}`,
    dim: dimension.id,
    x: block.location.x,
    y: block.location.y,
    z: block.location.z,
    signature: block.typeId,
    lastSpawn: system.currentTick
  });
  saveZones(zones);

  dimension.spawnParticle("minecraft:heart_particle", {
    x: block.location.x + 0.5,
    y: block.location.y + 1.5,
    z: block.location.z + 0.5
  });
  dimension.playSound("random.explode", block.location, { volume: 0.5, pitch: 0.8 });
}

world.afterEvents.projectileHitBlock.subscribe((event) => {
  if (event.projectile?.typeId !== "mod_rpg_rune:infestation_projectile") return;
  const hit = event.getBlockHit();
  if (!hit || !hit.block) return;
  createZone(event.dimension, hit.block);
  try { event.projectile.remove(); } catch (e) {}
});

// ─── Loop de spawn ──────────────────────────────────────
function pickMob(dimId) {
  const list = MOBS[dimId] || MOBS["minecraft:overworld"];
  return list[Math.floor(Math.random() * list.length)];
}

function pickSpawnPos(dimension, zone) {
  for (let attempt = 0; attempt < 8; attempt++) {
    const angle = Math.random() * Math.PI * 2;
    const dist = Math.random() * ZONE_RADIUS;
    const bx = Math.floor(zone.x + Math.cos(angle) * dist);
    const bz = Math.floor(zone.z + Math.sin(angle) * dist);

    for (let y = zone.y + 5; y >= zone.y - 5; y--) {
      const b = dimension.getBlock({ x: bx, y, z: bz });
      const above = dimension.getBlock({ x: bx, y: y + 1, z: bz });
      if (b && b.typeId !== "minecraft:air" && above?.typeId === "minecraft:air") {
        return { x: bx + 0.5, y: y + 1.05, z: bz + 0.5 };
      }
    }
  }
  return { x: zone.x + 0.5, y: zone.y + 1.05, z: zone.z + 0.5 };
}

system.runInterval(() => {
  const zones = getZones();
  if (zones.length === 0) return;

  const now = system.currentTick;
  const alive = [];
  let changed = false;

  for (const zone of zones) {
    const dim = world.getDimension(zone.dim);
    const center = dim.getBlock({ x: zone.x, y: zone.y, z: zone.z });

    // Se o bloco-âncora sumiu/foi trocado, zona morre
    if (!center || center.typeId !== zone.signature) {
      changed = true;
      continue;
    }

    // Cap de mobs vivos na área
    const nearby = dim.getEntities({
      location: { x: zone.x + 0.5, y: zone.y + 1, z: zone.z + 0.5 },
      maxDistance: ZONE_RADIUS + 2,
      families: ["monster"]
    });

    if (nearby.length < MAX_MOBS_IN_ZONE && now - zone.lastSpawn >= SPAWN_INTERVAL) {
      const mob = pickMob(zone.dim);
      const pos = pickSpawnPos(dim, zone);
      try { dim.spawnEntity(mob, pos); } catch (e) {}
      zone.lastSpawn = now;
      changed = true;
    }

    alive.push(zone);
  }

  if (changed) saveZones(alive);
}, 20);
