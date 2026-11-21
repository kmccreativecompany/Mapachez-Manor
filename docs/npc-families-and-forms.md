# NPC appearance diversity and family origins

Mapáchez Manor's NPC generator now combines existing small pixel-art character parts (eyes, hair, ears, horns, antlers, wings, tails, surfaces, facial hair and optional wheelchairs) without requiring a visible species category.

**Story rule:** Biological relatives have the same underlying species of origin. Their hairstyles, clothing, eye count, colors and other features can differ. Spouses, adopted children, step-relatives and pets do **not** automatically inherit that biological origin. A ghost or robot can share a spouse's underlying species while appearing ghostly or mechanical.

### Authoring an NPC family

The character drawing function remains `castLook(name, options)`. Give a stable `familyId` only when a story specifies a relationship. Do **not** infer a relationship from a surname, a wedding, a shared room or a guest's appearance.

```js
// The three biological relatives share a seeded, internal originKind.
const parent = castLook('Aster', {familyId: 'story:orchard-house', familyRole: 'biological'});
const child  = castLook('Sapling', {familyId: 'story:orchard-house', familyRole: 'biological'});

// Their adopted daughter is still family, but may have her own origin.
const adopted = castLook('Luma', {familyId: 'story:orchard-house', familyRole: 'adopted'});

// A spouse may be of any species. Same-origin robot or ghost partners
// explicitly reference the same heritageId:
const robotSpouse = castLook('Brass', {
  familyId: 'story:orchard-house', familyRole: 'spouse',
  heritageId: 'story:orchard-house', form: 'robot'
});
const ghostSpouse = castLook('Wisp', {
  familyId: 'story:orchard-house', familyRole: 'spouse',
  heritageId: 'story:orchard-house', form: 'ghost'
});
```

`familyId` groups members socially, while `familyRole: 'biological'` activates shared species inheritance. `heritageId` explicitly shares an origin with any character or group, including a spouse. An unrelated or adopted relative who is *coincidentally* the same species is permitted, but is not automatically forced to match. `form: 'living' | 'robot' | 'ghost'` controls visible body form. The internal `originKind` tracks species of origin and is not shown to the player. Use stable, unique string identifiers.

### Compatibility

- No change to player selection or the player's saved character.
- No change to pinned story character appearances, including Delores, the existing raccoon family, Mrs. Tanaka and the authored ghost cast.
- No need for local storage or external services: each name and family relationship always regenerates the same appearance.
- Existing unscripted NPCs have more visual variety; small game sprites stay deliberately simple.
- This adds the generation **infrastructure**, not invented family relationships or new story characters. A future story scene should attach relationship metadata to its NPC records explicitly.

### Verification

JavaScript parsed successfully. 400 named guest recipes produced 362 distinct combinations and all six supported visible character kinds. The pixel renderer drew 1,600 frames across four directions without throwing. Three biological family members matched on origin, robot and ghost spouses matched on origin when explicitly requested, and adoption and pets remained independently generated. New browser regression tests were added but not executed in Chromium in this environment.
