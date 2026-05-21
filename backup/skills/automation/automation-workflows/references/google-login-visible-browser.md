# Google / Gmail login in a visible self-hosted browser

Use this note when a user wants you to drive a Google login or inspect Gmail inside a watchable browser session rather than through OAuth or IMAP tooling.

## When this reference applies

- The user wants a live browser they can watch and intervene in.
- The task is account login, inbox inspection, or retrieving one-time codes from Gmail in-session.
- Browser automation needs to pause for password entry, device approval, OTP, or recovery prompts.

## Practical workflow

1. **Prefer a mainstream installed browser for Google sign-in** if an automation-oriented build gets flagged as insecure.
   - Reuse the same visible desktop / VNC stack.
   - Keep a dedicated user-data-dir for session continuity.

2. **Drive the email/username step first.**
   - Do not ask for the password yet if the user said to provide it only when needed.

3. **Pause exactly when the password field or second-factor prompt is visible.**
   - Ask only for the secret needed at that moment.
   - For Google push approval, quote the exact on-screen number/device and let the user approve on their phone.

4. **After the user says they completed the manual step, verify state immediately.**
   - Capture a fresh screenshot.
   - Determine whether login succeeded, whether another factor is required, or whether the flow is blocked.

5. **For Gmail inbox work, use URL-driven search as a reliable fallback.**
   - `https://mail.google.com/mail/u/0/#search/<query>` is useful when synthetic keystrokes into the Gmail search box are flaky.
   - Then verify the page state with a screenshot because the UI may stay on inbox if the navigation did not take.

## Search hints for verification-email hunts

- Try product names and parent-brand names separately (for example `magnific`, `freepik`).
- If the brand search is noisy, search broader confirmation language such as `"verification code"`, then inspect sender/subject/date.
- Expect unrelated OTP traffic; confirm sender and recency before reporting a code.

## Pitfalls observed

- Multi-box OTP fields can miss the first digit under automation. Slow down and verify after entry rather than assuming success.
- Gmail/Google flows may open multiple tabs or leave a stale sign-in tab behind after success; inspect the active inbox tab before concluding login failed.
- URL-bar navigation can accidentally target the wrong tab if window focus is ambiguous; activate the intended inbox window first.
