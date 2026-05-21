# War-documentary map infographic notes

Use this reference when the user wants a **detailed war documentary**, **current conflict explainer**, **map-first geopolitics video**, or **future-of-the-Gulf / UAE consequences** treatment.

## Trigger phrases
- "make it like a war documentary"
- "show it on the map"
- "what weapons are they using"
- "what is Strait of Hormuz"
- "future of UAE / Dubai"
- complaints that the first pass looked like weak slides or bad illustrations

## Preferred visual grammar
- real map assets first, not placeholder sketches
- documentary title cards with restrained palette
- one main idea per scene
- clear callout panels with short labels
- route lines, rings, arrows, and chokepoint boxes
- badge-like labels for categories: airstrikes, missiles, drones, naval pressure, insurance, shipping, aviation
- UAE/Dubai consequence scenes should feel analytical, not promotional

## Recommended source order for this task class
1. Authenticated Magnific vectors / illustrations / stock
2. Magnific search terms for this class:
   - `middle east map`
   - `strait of hormuz map`
   - `missile icon`
   - `drone icon`
   - `oil tanker vector`
   - `dubai skyline vector`
   - `container ship icon`
   - `airplane route`
3. Supplement only if needed with Storyset / unDraw / map base layers

## Verification pattern inside Magnific
- confirm logged-in access to `stock` and `illustrations`
- search directly inside Magnific rather than generic web requests, because direct HTTP/browser access may still hit 403s
- verify a detail page opens
- click Download once and confirm a new file appears under Playwright artifact directories
- inspect the downloaded file type:
  - JPG/PNG for rapid compositing
  - ZIP often contains EPS + preview JPG
- extract ZIP packages and keep both the preview image and source vector together in the project assets directory

## Durable production pattern learned here
- A strong conflict/UAE explainer structure is:
  1. opening title / why this matters
  2. strike geography
  3. weapons & methods categories
  4. Strait of Hormuz explanation
  5. immediate UAE exposure
  6. future scenarios / balance of downside and upside
  7. closing map takeaway
- Use **reported / pressure / risk / scenario** wording when facts are contested.
- For weapons, prefer **category framing** unless the reporting clearly supports exact model names.
- For Hormuz, explain the economic mechanism: risk, insurance, rerouting, energy reaction — not just a simplistic full-closure claim.
- For UAE, frame outcomes as a balance of short-term logistics/insurance pressure versus safe-haven, ports, and regional-HQ upside.

## Asset handling note
Downloaded Magnific files may land under `/tmp/playwright-artifacts-*` with UUID-like names and no extension. Inspect them with `file` and extract ZIPs before using them.
