import { world, system, ItemStack } from "@minecraft/server";

const NS = "mod_rpg_rune";
const TOWER_TYPES = { PLANTER: `${NS}:industrial_planter`, FERTILIZER: `${NS}:industrial_fertilizer`, HARVESTER: `${NS}:industrial_harvester` };
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
  "minecraft:wheat_seeds": { crop: "minecraft:wheat", soil: ["farmland","dirt","grass_block"] },
  "minecraft:carrot": { crop: "minecraft:carrots", soil: ["farmland","dirt","grass_block"] },
  "minecraft:potato": { crop: "minecraft:potatoes", soil: ["farmland","dirt","grass_block"] },
  "minecraft:beetroot_seeds": { crop: "minecraft:beetroot", soil: ["farmland","dirt","grass_block"] },
  "minecraft:melon_seeds": { crop: "minecraft:melon_stem", soil: ["farmland","dirt","grass_block"] },
  "minecraft:pumpkin_seeds": { crop: "minecraft:pumpkin_stem", soil: ["farmland","dirt","grass_block"] },
  "minecraft:nether_wart": { crop: "minecraft:nether_wart", soil: ["soul_sand"] },
  "minecraft:sugar_cane": { crop: "minecraft:reeds", soil: ["sand","dirt","grass_block"] },
  "minecraft:cactus": { crop: "minecraft:cactus", soil: ["sand"] },
  "minecraft:oak_sapling": { crop: "minecraft:oak_sapling", soil: ["dirt","grass_block","podzol"] }
};

const HARVESTABLE = {
  "minecraft:wheat": { drop: "minecraft:wheat", extra: ["minecraft:wheat_seeds"], growth: true },
  "minecraft:carrots": { drop: "minecraft:carrot", extra: [], growth: true },
  "minecraft:potatoes": { drop: "minecraft:potato", extra: [], growth: true },
  "minecraft:beetroot": { drop: "minecraft:beetroot", extra: ["minecraft:beetroot_seeds"], growth: true },
  "minecraft:nether_wart": { drop: "minecraft:nether_wart", extra: [], growth: true },
  "minecraft:melon": { drop: "minecraft:melon", extra: [], growth: false },
  "minecraft:pumpkin": { drop: "minecraft:pumpkin", extra: [], growth: false }
};

const STACKABLE = new Set(["minecraft:cactus", "minecraft:bamboo", "minecraft:reeds"]);
const TREE_LOGS = new Set(["minecraft:oak_log","minecraft:spruce_log","minecraft:birch_log","minecraft:jungle_log","minecraft:acacia_log","minecraft:dark_oak_log"]);

function getGrowth(b) { try { const s = b.permutation.getAllStates(); return s["growth"] ?? s["growth_stage"] ?? s["age"] ?? null; } catch (e) { return null; } }
function isMature(b) { const g = getGrowth(b); return g !== null && (g >= 7 || (b.typeId.includes("wart") && g >= 3)); }
function forceMature(b) { try { if (b.typeId.includes("wart")) { b.setPermutation(b.permutation.withState("age", 3)); return true; } b.setPermutation(b.permutation.withState("growth", 7)); return true; } catch (e) { return false; } }

function getChest(dim, loc) {
  try {
    for (const d of [{x:1,y:0,z:0},{x:-1,y:0,z:0},{x:0,y:0,z:1},{x:0,y:0,z:-1},{x:0,y:1,z:0},{x:0,y:-1,z:0}]) {
      const b = dim.getBlock({ x: loc.x+d.x, y: loc.y+d.y, z: loc.z+d.z });
      if (b && (b.typeId === "minecraft:chest" || b.typeId === "minecraft:barrel")) return b.getComponent("inventory")?.container;
    }
  } catch (e) {}
  return null;
}
function take(c, id, amt = 1) { for (let i = 0; i < c.size; i++) { const it = c.getItem(i); if (it?.typeId === id) { if (it.amount > amt) { it.amount -= amt; c.setItem(i, it); } else c.setItem(i, undefined); return true; } } return false; }
function put(c, id, amt = 1) { let r = amt; for (let i = 0; i < c.size && r > 0; i++) { const it = c.getItem(i); if (!it) { c.setItem(i, new ItemStack(id, r)); r = 0; } else if (it.typeId === id && it.amount < 64) { const a = Math.min(64 - it.amount, r); it.amount += a; c.setItem(i, it); r -= a; } } return r === 0; }

world.afterEvents.playerSpawn.subscribe(e => { if (e.initialSpawn) { for (let x = -12; x <= 12; x++) for (let y = -3; y <= 3; y++) for (let z = -12; z <= 12; z++) { const l = { x: Math.floor(e.player.location.x)+x, y: Math.floor(e.player.location.y)+y, z: Math.floor(e.player.location.z)+z }; const b = e.player.dimension.getBlock(l); if (b && TOWER_IDS.has(b.typeId)) activeTowers.set(`${l.x},${l.y},${l.z},${e.player.dimension.id}`, { type: b.typeId, location: l, dimension: e.player.dimension, cursor: 0, waveRing: 0, last: 0 }); } } });
world.afterEvents.playerPlaceBlock.subscribe(e => { if (TOWER_IDS.has(e.block.typeId)) activeTowers.set(`${e.block.location.x},${e.block.location.y},${e.block.location.z},${e.dimension.id}`, { type: e.block.typeId, location: e.block.location, dimension: e.dimension, cursor: 0, waveRing: 0, last: 0 }); });
world.afterEvents.playerBreakBlock.subscribe(e => { if (TOWER_IDS.has(e.brokenBlockPermutation.type.id)) activeTowers.delete(`${e.block.location.x},${e.block.location.y},${e.block.location.z},${e.dimension.id}`); });

system.runInterval(() => {
  const now = system.currentTick;
  for (const [key, t] of activeTowers) {
    const dim = t.dimension; if (!dim.getBlock(t.location)) { activeTowers.delete(key); continue; }
    const chest = getChest(dim, t.location); if (!chest) continue;
    const gY = t.location.y - 1;

    if (t.type === TOWER_TYPES.PLANTER && now - t.last >= 4) {
      const p = SCAN_PATTERN[t.cursor++ % SCAN_PATTERN.length]; t.last = now;
      const s = dim.getBlock({ x: t.location.x+p.dx, y: gY, z: t.location.z+p.dz }), a = dim.getBlock({ x: s.x, y: gY+1, z: s.z });
      if (!s || !a || a.typeId !== "minecraft:air") continue;
      let seed = null, info = null;
      for (let i = 0; i < chest.size; i++) { const it = chest.getItem(i); if (it && PLANTABLE[it.typeId]) { seed = it.typeId; info = PLANTABLE[it.typeId]; break; } }
      if (seed && info.soil.some(x => s.typeId === `minecraft:${x}`) && take(chest, seed)) a.setType(info.crop);
    }

    if (t.type === TOWER_TYPES.FERTILIZER && now - t.last >= 30) {
      t.last = now; const ring = getRingPositions(t.waveRing || 0); let g = 0;
      for (const p of ring) {
        if (g >= 3) break;
        const c = dim.getBlock({ x: t.location.x+p.dx, y: gY+1, z: t.location.z+p.dz });
        if (c && c.typeId !== "minecraft:air" && !isMature(c) && Object.values(PLANTABLE).some(x => x.crop === c.typeId) && take(chest, "minecraft:bone_meal")) { forceMature(c); g++; }
      }
      t.waveRing = ((t.waveRing || 0) + 1) % (AREA_RADIUS + 1);
    }

    if (t.type === TOWER_TYPES.HARVESTER && now - t.last >= 4) {
      const p = SCAN_PATTERN[t.cursor++ % SCAN_PATTERN.length]; t.last = now;
      const a = dim.getBlock({ x: t.location.x+p.dx, y: gY+1, z: t.location.z+p.dz });
      if (!a || a.typeId === "minecraft:air") continue;
      if (TREE_LOGS.has(a.typeId)) { let y = a.y; for (let i = 0; i < 12; i++) { const b = dim.getBlock({ x: a.x, y, z: a.z }); if (!b || !TREE_LOGS.has(b.typeId)) break; put(chest, b.typeId); b.setType("minecraft:air"); y++; } continue; }
      if (STACKABLE.has(a.typeId)) { let h = 0; for (let k = 0; k < 8; k++) { if (dim.getBlock({ x: a.x, y: a.y+k, z: a.z })?.typeId === a.typeId) h++; else break; } if (h >= 2) for (let k = h-1; k >= 1; k--) { dim.getBlock({ x: a.x, y: a.y+k, z: a.z }).setType("minecraft:air"); put(chest, a.typeId); } continue; }
      const info = HARVESTABLE[a.typeId]; if (info && (!info.growth || isMature(a))) { a.setType("minecraft:air"); put(chest, info.drop); for (const e of info.extra) put(chest, e); }
    }
  }
}, 1);
