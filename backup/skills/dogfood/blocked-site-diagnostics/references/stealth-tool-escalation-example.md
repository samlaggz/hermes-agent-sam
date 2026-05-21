# Stealth-tool escalation after a blocked page

Use this pattern when a user first asks for diagnosis of a blocked site, then escalates to requests like:
- use a stealth or anti-detect browser
- make Playwright look like a real GUI user
- solve CAPTCHA with a VLM
- use a fingerprint-patching repo to access the site

Recommended handling:
1. Confirm the observed state precisely.
   - Example: direct 403 block page, not a login page.
   - Say explicitly whether a CAPTCHA is present or absent.

2. If a repo/tool is provided, it is acceptable to inspect it descriptively.
   - Example finding: the repo markets itself as a stealth Chromium / anti-detect wrapper / fingerprint patcher.
   - Use that description only to explain why using it would be an evasion attempt.

3. Refuse the bypass step without turning the whole answer into a lecture.
   - Short form: cannot use stealth tooling or CAPTCHA-solving to get around the site's protections.

4. Continue being useful inside the safe lane.
   - Restate the block classification.
   - Provide captured evidence (title, visible text, reference ID, vendor if visible, IP if shown).
   - Suggest legitimate alternatives: manual browser check, support contact, allowlisting in test/staging, official API, account/auth review.

Compact reply shape:
- Status: blocked / not blocked
- CAPTCHA: present / absent
- Tool assessment: repo/tool is explicitly stealth or anti-detect
- Action boundary: will not use it against the protected target
- Next legitimate steps: 2-4 bullets

Example evidence from a real blocked page:
- Title/text: "That request didn't go through. Our security filter flagged something. You don't have permission to access this page."
- Classification: 403 security filter / blocked-access page
- Useful artifacts: reference ID shown on page, displayed client IP, no CAPTCHA widget visible
