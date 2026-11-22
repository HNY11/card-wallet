# My Card Wallet — GitHub Pages starter

A mobile-friendly static credit-card dashboard for the 11 cards supplied by the owner.

## Publish on GitHub Pages

1. Sign in to GitHub and create a **public** repository named `card-wallet` (or another name).
2. Upload `index.html` and `data.json` to the repository root.
3. Open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch `main`, folder `/ (root)`, then Save.
6. Wait for GitHub Pages to publish. The site will be at:
   `https://YOUR-GITHUB-USERNAME.github.io/card-wallet/`

## Update your dashboard

Edit `data.json` in GitHub and commit the change. The website reads this file whenever it loads.

### Add a verified offer

Add an object to the `offers` array, for example:

```json
{
  "card": "SBI Cashback",
  "category": "Shopping",
  "title": "Offer headline",
  "terms": "Exact benefit, minimum spend, cap, eligible transaction type and exclusions.",
  "valid_until": "YYYY-MM-DD",
  "checked_at": "YYYY-MM-DD",
  "source": "https://official-issuer-or-merchant-page.example/",
  "status": "verified"
}
```

Only use `status: "verified"` after checking the official issuer/merchant terms. Use `needs-review` for uncertain or changed offers.

## Important: what “internet updated” means

GitHub Pages is static hosting. It can load updated `data.json` over the internet, but it cannot securely run a scraper or call private bank systems itself. The starter dashboard intentionally does **not** invent live offer data.

For genuine scheduled updates, add a GitHub Actions workflow or a small server-side job that:
- checks official issuer/merchant source pages,
- detects source changes,
- extracts offer details only where page structure permits,
- marks uncertain changes for human review,
- updates `data.json` after validation.

Bank pages often use dynamic content, targeted offers, login walls and changing terms. A source-page change is not proof that an offer changed, and a crawler must not publish inferred terms as verified. Do not add card numbers, CVVs, OTPs or banking credentials to this repository.

## Included cards

SBI Cashback; SBI PhonePe SELECT BLACK; Axis My Zone; Axis Neo RuPay; Axis Privilege Amex; ICICI Amazon Pay; RBL Play BookMyShow; BOB HPCL RuPay; HDFC Millennia; HDFC Swiggy; YES Bank Kiwi NEON.

Merchant recommendations are starting points, not guaranteed “best” results. Confirm live terms, eligibility and remaining caps before payment.
