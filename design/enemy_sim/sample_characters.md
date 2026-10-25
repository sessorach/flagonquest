# The sample characters

What each `sample_pcs.csv` row is and why it's built the way it is. The build itself (Stats, Skills, Techniques with their Features, items) is the Builder export in `builds/`, named in the row's `Build` column; a hand-made one says so in its own `simNotes`. These notes moved here from the CSV's Notes column on 2026-10-25 and are dated where they say so: older ones describe the sim on their day.

## Baseline Tier 1 Party Member

Build: `builds/baseline_tier_1_party_member.json`.

Validated on-level roster (win-rate grid) - the smoothed PC_SKILLS_COMBAT variant, see design/ENEMY_ENCOUNTER_DESIGN.md Analysis and this CSV's own header comment. Armor=Light for every Baseline row regardless of Tier (several would technically qualify for Medium on Might Skill Total alone) - a uniform 'typical adventurer' loadout, matching the enemy Roster's own uniform Light Armor choice, rather than gear scaling with Tier on its own axis

## Baseline Tier 2 Party Member

Build: `builds/baseline_tier_2_party_member.json`.

Validated on-level roster (win-rate grid) - the smoothed PC_SKILLS_COMBAT variant, see design/ENEMY_ENCOUNTER_DESIGN.md Analysis and this CSV's own header comment

## Baseline Tier 3 Party Member

Build: `builds/baseline_tier_3_party_member.json`.

Validated on-level roster (win-rate grid) - the smoothed PC_SKILLS_COMBAT variant, see design/ENEMY_ENCOUNTER_DESIGN.md Analysis and this CSV's own header comment

## Baseline Tier 4 Party Member

Build: `builds/baseline_tier_4_party_member.json`.

Validated on-level roster (win-rate grid) - the smoothed PC_SKILLS_COMBAT variant, see design/ENEMY_ENCOUNTER_DESIGN.md Analysis and this CSV's own header comment

## Baseline Tier 5 Party Member

Build: `builds/baseline_tier_5_party_member.json`.

Validated on-level roster (win-rate grid) - the smoothed PC_SKILLS_COMBAT variant, see design/ENEMY_ENCOUNTER_DESIGN.md Analysis and this CSV's own header comment

## Hilde

Build: `builds/hilde.json`.

Barbarian, Body-primary melee duelist (player-drafted build, replacing the earlier reference version of this character) - Weapon=2H Heavy Melee (I120, weapon_categories.csv WC004: Damage 5 + [Body], Skill Melee) - Armor=Medium (I129 'Heavy Armor' in her export, but per the designer this is the main branch's naming and should read as Medium here; Might Skill Total 6 clears both Medium's real Might Requirement of 5 and 2H Heavy Melee's own Might Requirement of 6) - Card Techniques: Second Wind (T012, 0 AP self-heal when Wounded - tactics.try_second_wind), budget card_uses_left = hand_size // 3 = 4 // 3 = 1 use this fight. Furious Rage (T130) and both Battle Maneuver copies (T072: one Lunging 3, one Half Guard 3, used in that order) are modeled since 2026-10-24. Her Second Wind is a point short of its prereq (Resilience or Composure 3); per the designer that's fine to leave, since these rows are benchmarks. 75 XP verified (28 Stats + 29 Skills + 18 Techniques).

## Browndog

Build: `builds/browndog.json`.

Fighter, Agility-primary melee disruptor (player-drafted build, replacing the earlier reference version) - Weapon left blank (I118 Heavy One-Handed Melee Weapon, weapon_categories.csv WC002, is an exact match for the sim's own blank-Weapon default: Damage 4 + [Body], Skill Melee) - also carries a Shield (I126, WC010: +2 to a chosen Defense) and Parries with it (Parry Weapons: its +2 Weapon Defense) - Armor=Medium (I129 'Heavy Armor' read as Medium per the designer's main-branch note; Might Skill Total 5 exactly clears Medium's real Might Requirement of 5). Since 2026-10-24: both Challenge copies, Brace (T001, 3 Protected) and both Battle Maneuver copies (Lunging 3, then Half Guard 3) are modeled; Follower (T059) isn't, being out of combat. 75 XP verified (28 Stats + 29 Skills + 18 Techniques). Challenge (T058) is modeled via Encounter Techniques: she Taunts the enemy closest to the party's most fragile member.

## Carrick

Build: `builds/carrick.json`.

Rogue, a versatile Acrobatics/Stealth/Streetwise build (player-drafted, replacing the earlier alchemist-concept version of this character - that concept moved to Jackal, see her own Notes) - Weapon=Light Thrown (I121, weapon_categories.csv WC005: Damage 2 + [Cunning], Skill Acrobatics - same weapon/Skill pairing as Rook's existing build) - Armor=Light (Might Skill Total 3 exactly clears Light's real Might Requirement of 3) - Card Techniques: Perfect Strike (T078, 0 AP - +2 Good Luck on an attack where she Gambles - tactics.perfect_strike_bonus), budget card_uses_left = hand_size // 3 = 8 // 3 = 2 uses this fight. Legerdemain (T034) and Rumormonger (T065) are both non-combat and not modeled. 75 XP verified (30 Stats + 27 Skills + 18 Techniques). Light Thrown is 2 + [Cunning] since 2026-10-24 (items.csv's I121; the sim had kept the pre-cut 3).

## Jackal

Build: `builds/jackal.json`.

Alchemist, a Mixology/Acrobatics build entirely reliant on Bottomless Bottles for anything beyond her baseline weapon (player-drafted, replacing the earlier scout-concept version of this character - that concept isn't currently represented in this roster) - Weapon=Light Thrown (I121, same WC005 pairing as Carrick/Rook) - Armor=Light (Might Skill Total 3 exactly clears Light's real Might Requirement of 3) - Card Techniques: Bottomless Bottles (T053, tactics.bottomless_bottles_choice) - substitutes Bottled Fire (I030, a [Grenade] - Acrobatics Skill Total, no accuracy bonus, flat 8 Fire damage, opposed by Dodge alone) for one of her normal attacks; Healing Potion dropped per the designer's own call (balancing two items off one budget was 'a bit tricky,' not worth it for one PC). bottled_fire_uses_left is a dedicated per-fight count, not the generic card_uses_left // 3 budget the other Card Techniques share, since Bottomless Bottles' own resource is Gold, not just 'a card': hand_size=10, spend 2/3 of a day's cards on it (10 x 2 // 3 = 6) for a Gold budget of 4 x 6 = 24 (T053's own Effects text), Bottled Fire costs 4 Gold (items.csv - the designer's own general rule for alchemy items without a specific price, 2 x Level, applied sitewide to every blank-Cost Grenade/Potion row), giving 24 // 4 = 6 Bottled Fire a day, and a single fight gets half of that (3) per the designer's own framing. 75 XP verified (36 Stats + 27 Skills + 12 Techniques - she spent more on Stats/less on Techniques than the usual 57/18 split, still totals 75).

## Felix

Build: `builds/felix.json`.

Monk, a cat Wildfolk: the designer's own Level 1 build (Builder export 2026-10-08, archive/player_builds/Felix-the-Mystic-2026-10-08.json), replacing the earlier stand-in. Player note: "Plays carefully but tries to tactically remove targets and is capable of fighting in the front lines." Weapon=Unarmed (Brawl 6 + 2 = attack +8, Damage 2 + Body = 4, Parry 15), Armor=Light. Modeled: Battle Maneuver (T072 Level 1, Encounter: Bare-Handed, then Bare-Handed's 2 extra points split per the designer 2026-10-09 into Lunging x2 and Half Guard x3 - two free 2 m Shifts and 3 + [Spades] Protected on a hit), used as his opening move; Firefly Leaves the Hand (T080, Meditation vs Mental, 4 Brilliant) and Thief Empties the Vessel (T159, Meditation vs Vital, 4 Shadow, discarding a card to heal 3 when he's missing 3 or more) as Encounter attacks; Great Old Oak School - Boughs Unbroken (T175, his Style: no Harried from Parrying with Unarmed; an Unarmed hit clears Bleeding, else Crippled, else another debuff). 75 XP: 32 Stats + 25 Skills + 18 Techniques.

## Enith

Build: `builds/enith.json`.

Duelist, the designer's Warlock stand-in, a Settler: the designer's own Level 1 build (Builder export 2026-10-08, archive/player_builds/Enith-the-Shade-2026-10-08.json). Her blade is the bread-and-butter offense, paired with non-damaging Sorcery hexes; per the designer (2026-10-09) she's a tactical skirmisher, almost a disabler, using the hexes to split enemies up so the party can divide and conquer. Weapon=Soulblade as a Light One-Handed Melee Weapon (Melee 4 + 1 = attack +5, Damage 3 + Cunning = 5, Parry 13), Armor=Light. Modeled: Hand of Chaos (T131, Sift 1 into each attack's suit pool); two War Magic hexes (T120 Level 1, Tormenting Curse's 3 extra points, Sorcery 5), each Lance (range 5) plus the rest on its one effect: Hex of Sloth, Frigid x3 (Slowed 6 + [Spades]) against Dodge, and Hex of Rebuking, Kinetic x3 (Pushed 12 + [Spades] meters) against Vital; Temper Soulblade as Fatestealer Level 1 (a kill banks 1 charge; 3 charges draw a card). 75 XP: 26 Stats + 31 Skills + 18 Techniques.

## Ashleigh

Build: `builds/ashleigh.json`.

Leader, a bard and cat Wildfolk: the designer's own Level 1 build (Builder export 2026-10-08, archive/player_builds/Ashleigh-the-Bard-2026-10-08.json). Weapon=Light Thrown (Acrobatics 4 + 1 = attack +5, Damage 2 + Cunning = 3, Range 3 x Body = 6), Armor=Light. Modeled: Raise Spirits (T069 Level 4: for 1 AP as an Interrupt, an ally within [Performance Skill Total = 6] meters gets Good Luck on an attack they declare). Per the designer (2026-10-09) she boosts anyone, holds an AP for a big attack (an Encounter Technique, like Beornhard's War Magic), stays within range of the party, and throws a knife with whatever AP is left on her own turn. Favorite Face (T063) is social only. 75 XP: 28 Stats + 29 Skills + 18 Techniques.

## Sable

Build: `builds/sable.json`.

Deadeye, an Agility/Archery build (player-drafted, replacing the earlier reference-build version of this character) - Weapon=Light Bow (I123, the actual craftable item - Accuracy +1, Damage 3 + [Cunning], Skill Archery, Range 19m; this sim's own tunables.WEAPON entry used to read 15m off weapon_categories.csv's more abstract category instead - corrected to match the real item) - Armor=Light (Might Skill Total 3 exactly clears Light's real Might Requirement of 3). All three of her Techniques are modeled: Perfect Strike (T078, tactics.perfect_strike_bonus - +2 Good Luck on any weapon attack) and Hand of Chaos (T131, tactics.sift_bonus - a flat 1-in-4 chance of +1 damage on a hit, the designer's own explicit stand-in for real suit-pool tracking, which this sim doesn't have) both share her card_uses_left/passives budget as usual. One Eye Behind You (T011) is Passives=One Eye Behind You: Good Luck on her Reflex flip specifically (combat_sim._roll_initiative/_resolve_group_order check for it), so she tends to go early in turn order - verified over 500 fights, her average initiative position is ~1.4th of 8 vs. ~3.5th for a random unit. The technique's other half (discard a card to manually reorder turn order mid-fight) isn't modeled - an of-the-moment tactical choice this sim has no basis to make for a player. 75 XP verified (24 Stats + 33 Skills + 18 Techniques).

## Rook

Build: `builds/rook.json`.

Skirmisher/knife-thrower, Body-primary - Weapon=Light Thrown (weapon_categories.csv WC005: Accuracy +1, Damage 2 + [Cunning], Range Close or 3 x Body, Skill Acrobatics or Melee - Acrobatics chosen here), so this build's own Range scales directly off Body rather than being fixed like a bow - built specifically to test combat_sim's movement=True mode from the PC side, see combat_sim.py's own note on the result - Armor=Light (Might Skill Total 5 clears Medium too, but Light was picked on purpose to keep a skirmisher's Dodge/Speed unpenalized) - built to rulebook.md's own Quick Creation Reference shape (2 Skills@3, 5@2, 2@1; 1 Stat@3, 2@2, 2@1), 57 XP in Skills+Stats + 18 XP (6 Levels) of Techniques (not modeled here) = 75 total, matching chargen exactly

## Wren

Build: `builds/wren.json`.

Mage, Essence-primary - Weapon=War Magic (Lance) (T120's own Sorcery-spell attack, plus its Lance feature - features.csv F064 - which sets Range = Sorcery Skill Total meters; Damage 2 + [Mind] Fire straight from T120's own Effects text, opposed by Dodge alone per T120's own 'Dodge or Vital, chosen when you learn this' rule, no Accuracy bonus since it's a Spell attack, not a weapon-category one) - built specifically to test combat_sim's movement=True mode from the PC side, see combat_sim.py's own note on the result - Armor=Unarmored (Might Skill Total 1, and it wouldn't help her Fire attacks' own elemres anyway) - built to rulebook.md's own Quick Creation Reference shape (2 Skills@3, 5@2, 2@1; 1 Stat@3, 2@2, 2@1), 57 XP in Skills+Stats + 18 XP (6 Levels) of Techniques (not modeled here) = 75 total, matching chargen exactly

## Beornhard

Build: `builds/beornhard.json`.

Arcanist, a damage-mage build entirely reliant on War Magic (player-drafted, replacing the earlier melee-support-healer version of this character - that support/healer concept isn't currently represented in this roster) - Weapon=War Magic (Lance) (T120 x3 + its own Lance feature - Sorcery Skill Total 6, Damage 2 + [Mind] = 5 Fire, Range = Sorcery Skill Total = 6m via Lance, opposed by Dodge - Dodge picked to match Wren's existing build, since the JSON export doesn't capture this one-time chargen choice) - carries a Light Two-Handed Melee Weapon (I119) too, but his Melee Skill is 0, so it's not used - War Magic is his only real attack, same 'no fallback' situation as Felix. Weapon Uses=3 (his 3 known copies of War Magic, an Encounter Technique - techniques.csv/Warmage's Reserves both call it that) + Warmage's Reserves (T124, 0 AP interrupt, discard X cards) adds ceil(hand_size / 3) = ceil(8/3) = 3 more, so 6 total War Magic casts this fight (party.py's own Weapon Uses paragraph) - once exhausted he simply doesn't attack that turn, no melee fallback. Shadow Jaunt (T097, a 1 AP Teleport up to his Sorcery Skill Total) is an Encounter Technique: he Teleports clear when an enemy reaches him (combat_sim._try_shadow_jaunt, 2026-10-25). Armor=Light (Might Skill Total 3 exactly clears Light's real Might Requirement of 3). 75 XP verified (38 Stats + 19 Skills + 18 Techniques).

## Hanforth

Build: `builds/hanforth.json`.

Of Epione, a dedicated Theurgy healer (new addition, not a replacement) - Weapon=Unarmed (weapon_categories.csv WC009: Accuracy +2, Damage 2 + [Body or Cunning], Skill Brawl - his own Cunning is higher than Body, so that's what's used; carries a Light Two-Handed Melee Weapon, I119, but his Melee Skill is 0, same 'not used' situation as Beornhard/Felix, so Unarmed/Brawl is his real attack instead) - Armor=Light (Might Skill Total 3 exactly clears Light's real Might Requirement of 3) - Support=TRUE, Healing Magic (T105) at Level 2 with Vitality x2 (features.csv F057, +1 healing per copy): Heal Cards=2 (T105's own Cost is 'Discard [Level] cards', so a Level 2 casting discards 2, each assumed a Heart per the existing guaranteed-favorable-discard convention), Heal Bonus=2 (Vitality x2's own flat total), Heal Range=4 (only enforced under movement=True - tactics.strategy_support_healer won't reach for an ally farther than that) - his own heal comes out to 1 + 2 (Hearts) + 2 (Vitality) = 5 Shallow Health per use. heal_uses_left = hand_size // 4 = 12 // 4 = 3 uses this fight. Battle Tactic=Straggler Hunter (tactics.target_straggler) - he still attacks when he can (Support doesn't stop him fighting between heals), but goes after whichever enemy is most isolated from its own pack rather than the nearest/first, so closing to his own melee range doesn't also put him in the middle of the main clump. Placeholder's Lengthy Ley-weaving (T133, +3m Range on Spells) is in Passives: Heal Range 4 is Healing Magic's adjacent reach plus its 3, and it adds 3 to his other Spells' ranges. Gust of Wind (T107, 1 AP, Encounter) is in Encounter Techniques: once an enemy reaches him he blows it back [twice Mind] + [Spades] meters, aimed so no ally is in the 3-meter cone (combat_sim._try_gust_of_wind, 2026-10-25). The cone's length is a shape, not a Range, so Ley-weaving doesn't stretch it. 75 XP verified (42 Stats + 18 Skills + 15 Techniques - he spent more on Stats/less on Techniques than the usual 57/18 split, still totals 75).

## Hilde (L2)

Build: `builds/hilde_l2.json`.

The designer's own 125 XP build of Hilde (archive/player_builds/Hilde-the-Barbarian-125XP-2026-10-24.json, 2026-10-24), replacing the extrapolated Level 2 row. New since Level 1: Strength from the Slain (T018, eaten after a kill: Hasted and Protected three times each, Good Luck on the next attack) and Toughened Body (T014, Deep Health +3, so Health 13). Armor=Medium (I127 in the export; Might Skill Total 7 clears it). Furious Rage and both Battle Maneuver copies as Level 1.

## Hilde (L3)

Build: `builds/hilde_l3.json`.

The designer's own 175 XP build of Hilde (archive/player_builds/Hilde-the-Barbarian-175XP-2026-10-24.json, 2026-10-24). New since Level 2: a Level 3 Battle Maneuver (Whirlwind, Victorious, Ascended Blade) and a third Lunging 3 copy, used Lunging, then the Level 3 copy, then Half Guard, then Lunging. Ascended Blade's prereq (Composure, Meditation or Theurgy 3) is a point short; left as built, per the designer. Bound Across Mountains (T007) isn't modeled, being out of combat.

## Browndog (L2)

Build: `builds/browndog_l2.json`.

The designer's own 125 XP build of Browndog (archive/player_builds/Browndog-the-Fighter-125XP-2026-10-24.json, 2026-10-24), replacing the extrapolated Level 2 row. New since Level 1: Inexhaustible Guardian (T139, a Style), a third Battle Maneuver (Lunging 3) and Second Wind (T012). No Toughened Body, so Health 10. Armor=Heavy (I129, as in every export; Might Skill Total 7 clears it now). Acrobatics drops from 1 to 0 between the exports; left as built.

## Browndog (L3)

Build: `builds/browndog_l3.json`.

The designer's own 175 XP build of Browndog (archive/player_builds/Browndog-the-Fighter-175XP-2026-10-24.json, 2026-10-24). New since Level 2: Exert Pressure (T067, Taunts everyone within 2 meters) and Toughened Resolve (T019, Shallow and Deep Health +2 each, so Health 14 and Wounded only after 7 Shallow). Armor=Heavy.

## Carrick (L2)

Build: `builds/carrick_l2.json`.

The designer's own 125 XP build of Carrick (archive/player_builds/Carrick-the-Rogue-125XP-2026-10-24.json, 2026-10-24), replacing the extrapolated Level 2 row. New since Level 1: Lawman's Hand (T128, a Style: Slowed on a damaging hit), Distraction (T144) and Patch Up (T036); the last two work out of combat and aren't modeled. Light Thrown at 2 + [Cunning].

## Carrick (L3)

Build: `builds/carrick_l3.json`.

The designer's own 175 XP build of Carrick (archive/player_builds/Carrick-the-Rogue-175XP-2026-10-24.json, 2026-10-24). New since Level 2: Cloak and Dagger (T079). It needs a close-range weapon, so it never fires for Carrick throwing from range in the sim; it'd matter only if he fought in melee.

## Jackal (L2)

Build: `builds/jackal_l2.json`.

The designer's own 125 XP build of Jackal (archive/player_builds/Jackal-the-Alchemist-125XP-2026-10-24.json, 2026-10-24), replacing the extrapolated Level 2 row. New since Level 1: Mighty Mixologist (T035, +1 damage on her Bottled Fire) and Eagle Eyes (T137, a Style: an extra 1 AP for Good Luck twice on a thrown attack, taken when the AP left only covers one attack). No Toughened Body, so Health 10.

## Jackal (L3)

Build: `builds/jackal_l3.json`.

The designer's own 175 XP build of Jackal (archive/player_builds/Jackal-the-Alchemist-175XP-2026-10-24.json, 2026-10-24). New since Level 2: two Battle Maneuvers with Wind Slash 3 (+6 range on the attack) and Grim Resolve (T010: one card at the start of each fight for 1 Health committed until a full rest).

## Sable (L2)

Build: `builds/sable_l2.json`.

Level 2 version of Sable (+50 XP, 125 total, the Tier schedule the Baseline Tier 2 row uses; split ~+15 Stats/+15 Skills/+20 Techniques). New Techniques: Battle Maneuver (L2), Blinkstep, Shadow's Path, Parting Shot. Toughened Body shows up as Health 13. see the Sable row's own Notes for the Level 1 build. 2026-10-25: Battle Maneuver at Level 2 is extrapolated as Calculated and Wing Clip 3 (6 points: Good Luck, then Crippled 3 + [Clubs] on a hit), her opening shot. Blinkstep (T077) carries her first planned move or her back-off after shooting. Parting Shot (T076) needs a close-range weapon; she has only the bow, so it's her Unarmed one. Shadow's Path is out of combat.

## Rook (L2)

Build: `builds/rook_l2.json`.

Level 2 version of Rook (+50 XP, 125 total, the Tier schedule the Baseline Tier 2 row uses; split ~+15 Stats/+15 Skills/+20 Techniques). New Techniques: Perfect Strike, Blinkstep, Quick Draw, Parting Shot. Toughened Body shows up as Health 13. see the Rook row's own Notes for the Level 1 build. 2026-10-25: Blinkstep (T077) and Parting Shot (T076, with the thrown knife up close) are modeled. Quick Draw is out of combat.

## Wren (L2)

Build: `builds/wren_l2.json`.

Level 2 version of Wren (+50 XP, 125 total, the Tier schedule the Baseline Tier 2 row uses; split ~+15 Stats/+15 Skills/+20 Techniques). New Techniques: Overchanneling, Warmage's Reserves, War Magic (L2). Toughened Body shows up as Health 13. Only Techniques this sim models change anything beyond Stats/Skills - see the Wren row's own Notes for the Level 1 build.

## Beornhard (L2)

Build: `builds/beornhard_l2.json`.

The designer's own 125 XP build of Beornhard (archive/player_builds/Arcanist-Beornhard-125XP-2026-10-24.json, 2026-10-24), replacing the extrapolated Level 2 row. War Magic: two Level 2 copies with Lance and Destructive x2 (the Destructive War Magic technique attack) and one Level 1 copy with Lance (Weapon Uses 1); Warmage's Reserves takes back a Destructive copy (tunables.RESERVES_REGAIN_BEST). Overchanneling (T140, a Style) adds +1 to every one. All learned against Dodge, as at Level 1. Shadow Jaunt (T097) Teleports him clear when an enemy reaches him. Health 10.

## Beornhard (L3)

Build: `builds/beornhard_l3.json`.

The designer's own 175 XP build of Beornhard (archive/player_builds/Arcanist-Beornhard-175XP-2026-10-24.json, 2026-10-24). War Magic: the two Level 2 Destructive copies and a Level 4 one with Destructive x2, Draw Power and Furrow (Shape), a line half his Sorcery Skill Total long with no Lance (Furrow War Magic); no plain copy left, so Weapon Uses 0. Shadow Jaunt (T097) Teleports him clear of melee; Gainsay (T122) casts a War Magic copy at a melee attacker (or one that could Down him) from his Interrupt AP; Wall of Shadows (T123) goes across the line to the enemies' shooters when it blocks more of their shots than the party's (all 2026-10-25). Health 10.

## Felix (L2)

Build: `builds/felix_l2.json`.

Level 2 version of Felix (+50 XP, 125 total; ~+15 Stats/+15 Skills/+20 Techniques, same schedule as the extrapolated (L2) rows). New Techniques: Hand Rings the Bell x2 (T154, Unarmed vs Mental, Brilliant, Slowed 2 + [Spades]) and Toughened Body (Health 13). See the Felix row for the build.

## Hanforth (L2)

Build: `builds/hanforth_l2.json`.

Level 2 version of Hanforth (+50 XP, 125 total, the Tier schedule the Baseline Tier 2 row uses; split ~+15 Stats/+15 Skills/+20 Techniques). New Techniques: Lifeline, Spirit Blessing, Toughened Body, Brace. Toughened Body shows up as Health 13. Only Techniques this sim models change anything beyond Stats/Skills - see the Hanforth row's own Notes for the Level 1 build. 2026-09-30: Reckoning (T111, Theurgy vs Mental, Crippled 5 + [Clubs]) swapped in for Brace, per the designer, so the party's healer has a debuff on an enemy's Mental Defense. 2026-10-25: everything on the sheet is modeled now. Reckoning is a ranged cast at the start of his turn (Theurgy Skill Total + 3 meters, on the biggest threat not yet Crippled), not a stand-in for his Unarmed attack. Gust of Wind and Ley-weaving as at Level 1. Lifeline (T110) links an ally whose hit would Down them, from his Interrupt AP, and he takes their Health loss while he can stand it. Spirit Blessing (T104) at Level 2 is extrapolated like the rest of this row: Shielding 2, Quickened and Reach (4 points), so 1 AP for Protected three times on whoever has the most enemies on them.

## HOLE (90 XP)

Build: `builds/hole_90_xp.json`.

Real player build from the designer's current campaign (~90 XP), shared 2026-10-08 - see archive/player_builds/HOLE_2026-10-08.md for the share link and full breakdown. Stats/Skills/Techniques are exact. Per the designer: Light armor; Soulblade makes a Heavy Thrown weapon (Acrobatics 5 + 0 to hit, Damage 3 + Body = 6, Range 3 x Body = 9); Temper Soulblade is Level 2 with Fatestealer (I092: a kill gains 3 charges, spent to Sift or draw cards) - not on this row; the sim's Fatestealer is Enith's Level 1 version. That makes 81 XP spent (Temper Soulblade at Level 2). Spacious Gut, Gorger and Vow of Poverty are non-combat. Health 10 (no Toughened Body). Play Style Skirmisher: a light-armored thrower. Thrown weapons can't Parry, so Parry falls back to Unarmed.

## Hilde (Bleed)

Build: `builds/hilde_bleed.json`.

Bleeding test variant of Hilde (2026-10-09): her own export already has Furious Rage (T130), which the base row didn't model then; here it's on. Since 2026-10-24 base Hilde has it too, plus her Battle Maneuvers; this row stays as the Bleeding work ran it, without them. Everything else as Hilde.

## Felix (Bleed)

Build: `builds/felix_bleed.json`.

Bleeding test variant of Felix (2026-10-09): Battle Maneuver's Half Guard x3 swapped for Battering x3 (F005: on a hit or Parry, the target gains 3 + [Clubs] stacks of Bleeding). Everything else as Felix.

## Jackal (Bleed)

Build: `builds/jackal_bleed.json`.

Bleeding test variant of Jackal (2026-10-09): Bottomless Bottles makes Acidic Flasks (I028, Level 1, 2 Gold: on a hit, 5 + [Clubs] stacks of Bleeding, no damage) instead of Bottled Fire, twice as many for the same Gold. Everything else as Jackal.

## Beornhard (Bleed)

Build: `builds/beornhard_bleed.json`.

Bleeding test variant of Beornhard (2026-10-09): two of his three Level 1 War Magic copies (3 XP each) swapped for one Level 2 copy (6 XP) with Lance, Sanguine and Destructive x1 (F067: +3 damage, and Health it would lose becomes that many Bleeding stacks + [Clubs]). One plain War Magic left. Everything else as Beornhard.

## Beornhard (Cash)

Build: `builds/beornhard_cash.json`.

Bleeding cash-out test (2026-10-16): as Beornhard (Bleed), but the Level 2 War Magic copy has Lance and Reign of Blood x2 (F073: on a hit, remove up to 4 + [Clubs] stacks of Bleeding from the target, and it loses that much Health) on top of its 2 + [Mind] Fire. Held until the target has 2 or more stacks. Same XP as the Sanguine copy.

## Beornhard (Destr)

Build: `builds/beornhard_destr.json`.

Yardstick for Beornhard (Cash) (2026-10-16): the same Level 2 War Magic copy with Lance and Destructive x2 (+2 damage) instead of Reign of Blood x2. Same XP.

## Felix (Cash)

Build: `builds/felix_cash.json`.

Bleeding cash-out test (2026-10-16): Felix's Battle Maneuver with a draft Feature, Open the Wound x3 (Reign of Blood's text for Battle Maneuver: on a hit, remove up to 6 + [Clubs] stacks of Bleeding from the target, and it loses that much Health) in place of Half Guard x3. Held until the target has 2 or more stacks, or round 3. Everything else as Felix.

## Variants (2026-10-25)

Alternate builds of the sample characters, for "what if they'd picked this instead?" Each is a file in `builds/` that names its base export and lists only what changes (README, `builds/`), so when the base export is updated, the variant follows. Its own `sample_pcs.csv` row copies the base row's Weapon, Play Style and Choices. Every swap stays inside the copy's Feature Budget. They're drafts: reasonable picks a player might make, not tuned.

Each was run with `compare_builds.py` against its base party, 300 fights a mix over the four standard mixes, same seeds both ways. Two enemy toughnesses: ×1.75 (the effect check's) and a tougher one that gives fights of about five rounds, THE TABEL's length (×2.75 for Party B at Level 2, ×2.25 for Party B at Level 3 and Party A at Level 2). Parties D and S already go 4.5 to 7 rounds at ×1.75. Change in the party's Health left at the end (losses count 0), with its 95% margin, and in win rate:

| Variant | Party | Swap | ×1.75 | ~5 rounds |
|---|---|---|---|---|
| Beornhard (L2, Frost) | B, L2 | both Level 2 copies Lance + Frigid 2 (was Destructive 2) | -1.3 ±0.4, wins -0.8 | -4.8 ±1.0, wins -5.8 |
| Beornhard (L2, Kinetic) | B, L2 | Lance + Kinetic 1 + Destructive 1 | -0.9 ±0.3, wins -0.2 | -3.4 ±0.8, wins -3.6 |
| Beornhard (L2, Corrupting) | B, L2 | Lance + Corrupting 1 + Destructive 1, all against Vital | -1.0 ±0.3, wins -0.2 | -1.8 ±0.8, wins -0.2 |
| Beornhard (L2, Vital) | B, L2 | as built, all three copies against Vital | -0.7 ±0.3, wins -0.3 | +0.4 ±0.7, wins +1.7 |
| Beornhard (L3, Frost) | B, L3 | the Frost build, Level 4 copy Furrow + Frigid 2 + Destructive | -3.0 ±0.7, wins -2.9 | -2.3 ±0.8, wins -2.6 |
| Beornhard (L3, Piercing) | B, L3 | Level 4 copy Lance + Destructive 3 + Piercing Elements + Draw Power, no Furrow | +0.6 ±0.2, wins +0.9 | +1.8 ±0.4, wins +2.8 |
| Hilde (L2, Wing Clip) | B, L2 | Half Guard 3 copy as Wing Clip 3 | -0.9 ±0.2, wins 0 | -2.8 ±0.5, wins -3.2 |
| Hilde (L2, Battering) | B, L2 | Half Guard 3 copy as Battering 3 | -1.4 ±0.2, wins -0.2 | -3.4 ±0.5, wins -3.8 |
| Hilde (L3, Flurry) | B, L3 | Level 3 copy as Flurry + Calculated | +1.4 ±0.5, wins +0.3 | +1.4 ±0.7, wins +1.6 |
| Hilde (L3, Viper) | B, L3 | opening Lunging 3 copy as Viper's Sting | -0.6 ±0.3, wins -0.3 | -0.3 ±0.3, wins -0.2 |
| Browndog (L2, Distracting) | B, L2 | second Lunging 3 copy as Distracting 3 | 0.0 ±0.1 | -0.3 ±0.2, wins -0.4 |
| Browndog (L2, Lodestone) | B, L2 | second Lunging 3 copy as Lodestone 3 | -0.1 ±0.1 | -0.8 ±0.3, wins -0.9 |
| Jackal (L3, Hamstring) | B, L3 | second Wind Slash 3 copy as Hamstring 3 | +0.2 ±0.1 | +0.3 ±0.3, wins +0.3 |
| Sable (L2, Viper) | A, L2 | Level 2 Maneuver as Viper's Sting + Wing Clip 3 (was Calculated) | +0.1 ±0.7 | -0.1 ±0.9, wins -0.3 |
| Felix (Viper) | D, L1 | Viper's Sting + Lunging 2 (was Lunging 2 + Half Guard 3) | -0.5 ±1.2, wins -0.8 | |
| Enith (Corrupting) | S, L1 | Kinetic hex as Corrupting 3 | -5.4 ±1.5, wins -7.1 | |
| Hanforth (L2, Triage) | D, L2 | Healing Magic Triage + Reach (was Vitality 2) | +0.9 ±0.3, wins +0.1 | |
| Hanforth (L2, Guardian Angel) | D, L2 | Guardian Angel 2 + Vitality 1 | -0.6 ±0.2, wins +0.1 | |
| Hanforth (L2, Rejuvenate) | D, L2 | Rejuvenate + Vitality 1 + Reach | -2.9 ±0.5, wins -0.8 | |
| Hanforth (L2, Retribution) | D, L2 | Spirit Blessing Retribution 2 + Shielding 1 + Reach | -0.5 ±0.4, wins -0.7 | |
| Hanforth (L2, River's Might) | D, L2 | River's Might 2 + Quickened + Reach | -2.2 ±0.6, wins -0.8 | |
| Hanforth (L2, Touch of Chaos) | D, L2 | Touch of Chaos 2 + Quickened + Reach | -1.5 ±0.6, wins -0.4 | |

What it says, roughly:

- **Damage beats control.** Beornhard's Frost and Kinetic copies give up damage for Slowed or a Push, and the longer the fight, the more the lost damage shows. I guessed it was because Party B's Hilde and Browndog are already on whatever he'd slow, but in Party D at Level 2 (Browndog the only one up front) the swap still costs 1.9 Health (Frost) and 2.1 (Kinetic) a fight, ±0.6. So the trade itself looks short, at least at 2 damage for Slowed 4 + [Spades]. Enith's Kinetic hex is the exception: Party S has nobody holding the line, and her Kinetic hex beats a Corrupting one by 5 Health a fight.
- **Kinetic is "up to", so the sim now chooses.** Pushing every time dragged enemies off Hilde and Browndog and cost 5.7 Health a fight. Now Beornhard pushes only a target that's next to a ranged ally or next to nobody, and the cost is 3.4. Lodestone and River's Might say "Pushed", no "up to", so they push every time, and it shows: River's Might is the worst of Hanforth's blessings.
- **Dodge or Vital for Beornhard's War Magic is a wash**: Vital is a hair worse in short fights and a hair better in long ones. Piercing Elements (Good Luck on the cast) over Furrow is a clear win at Level 3.
- **Flurry is the one Maneuver swap that helps.** Calculated's Good Luck plus a free Repeat beats the Level 3 copy Hilde built. Viper's Sting saves 1 AP, but most turns have nothing to spend it on: Sable is usually already in range, and Hilde's Viper copy gives up Lunging's free Shifts.
- **Hanforth's heal as built is about right.** Triage edges out Vitality 2, and Rejuvenate's heal-over-time is too slow to keep up at Level 2.
