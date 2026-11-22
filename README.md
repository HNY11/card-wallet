# My Card Wallet

A mobile-friendly static credit-card offers dashboard for 11 cards.

## Live site

https://hny11.github.io/card-wallet/

## Update your dashboard

The website reads `data.json` whenever it loads. To change offers, update that file on the `main` branch and commit the change.

Each offer should include:
- Card and category
- Title and full terms (minimum spend, cap, eligibility, exclusions)
- Validity / expiry information
- Date last checked
- Official source URL
- Status (`verified` or `needs-review`)

Only label an entry `verified` after checking the official issuer or merchant terms. A source link does not guarantee that an offer will be accepted at checkout.

## Scheduled source monitoring

The GitHub Actions workflow at `.github/workflows/offer-source-monitor.yml` checks the official source URLs referenced in `data.json` daily at 07:00 India time. It can also be run manually from **Actions → Monitor card offer sources → Run workflow**.

The monitor stores source fingerprints in `source_checks.json`. If an issuer page changes or cannot be reached, it creates or comments on a GitHub issue titled **[Offer Monitor] Review changed issuer pages**.

**Important:** The monitor detects source changes; it does not automatically rewrite cashback rates, offer caps or expiry dates. A changed page is not proof that an offer changed. Review the issuer's current terms and update `data.json` manually after validating the details.

GitHub Pages is static hosting and does not have access to private bank systems or targeted offers behind login. Do not add card numbers, CVVs, OTPs or banking credentials to this repository.

## Cards tracked

SBI Cashback; SBI PhonePe SELECT BLACK; Axis My Zone; Axis Neo RuPay; Axis Privilege Amex; ICICI Amazon Pay; RBL Play BookMyShow; BOB HPCL RuPay; HDFC Millennia; HDFC Swiggy; YES Bank Kiwi NEON.

Merchant recommendations are starting points, not guaranteed "best" results. Confirm live terms, eligibility and remaining caps before payment.
