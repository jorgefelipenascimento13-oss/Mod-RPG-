import { world, system, EquipmentSlot } from "@minecraft/server";
const NS = "mod_rpg_rune";
const enchanted = new Set();

system.runInterval(() => {
  for (const p of world.getAllPlayers()) {
    const eq = p.getComponent("minecraft:equippable"); if (!eq) continue;
    const m = eq.getEquipment(EquipmentSlot.Mainhand); if (!m || !m.typeId.startsWith(`${NS}:paxel_`)) continue;
    try { const d = m.getComponent("minecraft:durability"); if (d && d.damage > 0) { d.damage = 0; eq.setEquipment(EquipmentSlot.Mainhand, m); } } catch (e) {}
    if (!enchanted.has(`${p.id}:${m.typeId}`)) { p.runCommandAsync("enchant @s sharpness 5"); p.runCommandAsync("enchant @s efficiency 5"); p.runCommandAsync("enchant @s unbreaking 3"); enchanted.add(`${p.id}:${m.typeId}`); }
  }
}, 20);

world.afterEvents.playerBreakBlock.subscribe((e) => {
  const { player, brokenBlockPermutation, block, dimension } = e;
  const m = player.getComponent("minecraft:equippable")?.getEquipment(EquipmentSlot.Mainhand);
  if (!m || !m.typeId.startsWith(`${NS}:paxel_`) || !player.isSneaking) return;
  const type = brokenBlockPermutation.type.id, start = block.location, q = [start], visited = new Set(); let c = 0;
  system.run(() => {
    while (q.length && c < 128) {
      const l = q.shift(), k = `${l.x},${l.y},${l.z}`; if (visited.has(k)) continue; visited.add(k);
      const t = dimension.getBlock(l); if (!t) continue;
      if ((l.x === start.x && l.y === start.y && l.z === start.z) || t.typeId === type) {
        if (l !== start) try { dimension.runCommandAsync(`setblock ${l.x} ${l.y} ${l.z} air destroy`); } catch (er) {}
        c++; for (const n of [{ x: l.x+1, y: l.y, z: l.z }, { x: l.x-1, y: l.y, z: l.z }, { x: l.x, y: l.y+1, z: l.z }, { x: l.x, y: l.y-1, z: l.z }, { x: l.x, y: l.y, z: l.z+1 }, { x: l.x, y: l.y, z: l.z-1 }]) q.push(n);
      }
    }
  });
});

const STRIPPED = { "minecraft:oak_log":"minecraft:stripped_oak_log", "minecraft:spruce_log":"minecraft:stripped_spruce_log", "minecraft:birch_log":"minecraft:stripped_birch_log", "minecraft:jungle_log":"minecraft:stripped_jungle_log", "minecraft:acacia_log":"minecraft:stripped_acacia_log", "minecraft:dark_oak_log":"minecraft:stripped_dark_oak_log" };
const SOILS = new Set(["minecraft:grass_block","minecraft:dirt","minecraft:dirt_with_roots","minecraft:coarse_dirt"]);

world.beforeEvents.itemUseOn.subscribe(e => {
  if (!e.itemStack?.typeId.startsWith(`${NS}:paxel_`) || !e.block) return;
  const dim = e.block.dimension, type = e.block.typeId;
  if (STRIPPED[type]) { system.run(() => { const b = dim.getBlock(e.block.location); if (b?.typeId === type) b.setType(STRIPPED[type]); }); return; }
  if (SOILS.has(type)) { const c = e.block.location; system.run(() => { for (let x = -1; x <= 1; x++) for (let z = -1; z <= 1; z++) { const b = dim.getBlock({ x: c.x+x, y: c.y, z: c.z+z }); if (b && SOILS.has(b.typeId) && ["minecraft:air"].includes(dim.getBlock({ x: b.x, y: b.y+1, z: b.z })?.typeId)) b.setType("minecraft:farmland"); } }); }
});
