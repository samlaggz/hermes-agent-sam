# Magnific premium stock sourcing for luxury real-estate edits

Use this reference when building a premium property / developer-style video from Magnific stock.

## When to use
- The user asks for a more premium, cinematic, luxury real-estate film
- The first-pass edit felt generic, repetitive, or too explainer-like
- You need better lifestyle / amenity / architectural coverage than general stock searches produced

## High-yield Magnific search queries
Start with `type=video` and search directly for the specific amenity or mood:

- `luxury residence`
- `modern luxury building`
- `luxury lobby`
- `concierge hotel lobby`
- `rooftop lounge`
- `luxury swimming pool`
- `spa amenities`
- `gym amenities`
- `architectural details luxury`
- `family walking luxury community`
- `women luxury interior`

## What each query was good for
- `luxury residence` → exterior hero mansions / residences
- `modern luxury building` → illuminated tower / premium architecture hero clips
- `luxury lobby` → grand stair / arrival / polished interior scale
- `concierge hotel lobby` → hospitality-style reception / serviced-living feel
- `rooftop lounge` → terrace seating / skyline-adjacent amenity mood
- `luxury swimming pool` → resort-style amenity / clubhouse water shots
- `architectural details luxury` → staircase / materials / transition details
- `family walking luxury community` → landscaped community / emotional lifestyle coverage
- `women luxury interior` → elegant female lifestyle moments inside refined interiors
- `gym amenities` → usable but often visually weaker than pool / lobby / concierge / rooftop

## Selection heuristics
Prefer clips that visibly communicate one of these premium signals:
- clear architectural intent (hero exterior, tower, branded-looking residence)
- arrival and service (lobby, concierge, reception)
- lifestyle warmth (woman by window, family walking, people using amenities)
- hospitality-adjacent amenities (pool, rooftop, spa, wellness)
- elegant detail inserts (stairs, materials, fixtures, lighting)

Reject or shorten clips that are:
- repetitive variants of the same angle
- generic empty spaces with no obvious premium cues
- visually premium but off-brand for property marketing (too abstract, too fashion-only, too unrelated)
- noticeably weaker than the surrounding shots

## Magnific download behavior observed
- Downloaded stock files may land in a temporary Playwright artifacts directory rather than a normal Downloads folder.
- In this session they appeared under paths like:
  - `/tmp/playwright-artifacts-*/<uuid>`
  - sometimes first as `.crdownload`, then finalizing to an extensionless media file
- The downloaded files were still valid video containers even without an extension.
- Practical recovery pattern:
  1. download from the visible browser
  2. watch `/tmp/playwright-artifacts-*` for newly created files
  3. wait for `.crdownload` to disappear if present
  4. identify the newest completed file
  5. inspect with `file` / `ffprobe`
  6. rename or copy to a stable `.mp4` working filename

## Edit guidance learned from this session
For premium real-estate videos, the stronger order is usually:
1. architectural hero
2. lobby / arrival
3. concierge / service
4. elegant lifestyle interior
5. rooftop / pool / wellness
6. family / community living
7. architectural detail transitions
8. skyline / tower / closing residence hero

## Typography / pacing notes
- Avoid generic center-stacked promo text on every shot
- Use fewer text moments with stronger hierarchy
- Serif headline + modern sans support text reads more premium than default UI-style captions
- Music-only edits often fit this category better than voiceover-heavy explainer edits
- Black-frame or flash-cut accents should be rare and tied only to stronger beats
