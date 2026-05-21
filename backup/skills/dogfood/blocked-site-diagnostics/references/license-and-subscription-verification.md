# License and Subscription Verification Under Blocked Access

Use this pattern when a user asks whether their paid plan permits a use case, but the service blocks automated access to the logged-in account UI.

## Principle
Separate three layers of certainty:

1. **Public legal terms** — what the provider says generally about ownership, outputs, restrictions, or user responsibility.
2. **Plan-specific subscription details** — what the user's actual billing/account page says about tier, entitlements, and downloads.
3. **Asset-specific rights** — badges or notices on the exact stock asset page such as commercial use, editorial-only, resale limits, or attribution requirements.

Do not collapse these into one answer.

## Safe response shape
- State what was verified directly.
- State what could not be verified due to blocked account access.
- Give a practical provisional answer if warranted, labeled as likely/not fully verified.
- Offer the fastest path to full verification: visible local browser session, screenshot from the user, or checking the exact asset page.

## Example boundary statement
- "Public terms confirm ownership of AI-generated/transformed assets."
- "I could not verify your exact subscription tier from the account page because the site returned a 403 from this machine."
- "For stock assets, final confirmation requires the logged-in plan page or the exact asset license details."

## Why this matters
Users often ask a yes/no legal-use question. Under blocked access, the failure mode is false confidence: answering from generic terms while implying the account plan was checked. Preserve trust by being precise about the evidence boundary.
