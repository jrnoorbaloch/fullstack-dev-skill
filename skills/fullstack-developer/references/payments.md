# Payments

Golden rules for every gateway:
1. **Never trust the client** — calculate the amount on the server from the order in the database.
2. **Confirm on the server** — mark an order paid only after a verified webhook/callback or a server-side status check, never from the browser redirect alone.
3. **Verify signatures / hashes** on every callback. Reject anything that does not verify.
4. **Idempotency** — store the gateway transaction ID and ignore duplicates.
5. **Secrets** stay in env vars on the server. Use sandbox credentials until go-live.
6. Never store card numbers. Let the gateway's hosted page or SDK handle card entry.

Recommended order model:
```
orders(id, user_id, status: pending|paid|failed|refunded|cancelled, amount, currency,
       gateway, gateway_ref, created_at, paid_at)
order_items(order_id, product_id, qty, unit_price)
payment_events(id, order_id, gateway, raw_payload jsonb, verified bool, created_at)
```

---

## Stripe (international cards, subscriptions)
- Use **Stripe Checkout** (hosted page) for one-off payments and subscriptions; **Customer Portal** for managing subscriptions.
- Flow: server creates a Checkout Session with `line_items` from the DB and `metadata.order_id` → redirect user to `session.url` → handle `checkout.session.completed` webhook → mark order paid.
- Webhook: read the **raw body**, verify with `stripe.webhooks.constructEvent(rawBody, sig, STRIPE_WEBHOOK_SECRET)`.
- Subscriptions: also handle `customer.subscription.updated` / `deleted` and `invoice.payment_failed`.
- Local testing: `stripe listen --forward-to localhost:3000/api/stripe/webhook`; test card `4242 4242 4242 4242`.
- Env: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`.

## PayPal
- Use the **Orders v2 API**: server creates the order → client approves with PayPal JS SDK buttons → server **captures** the order → store capture ID.
- Verify webhooks with PayPal's verify-webhook-signature endpoint.
- Env: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID`, `PAYPAL_ENV=sandbox|live`.

## JazzCash (Pakistan)
- Merchant account gives **Merchant ID, Password, Integrity Salt**. Use the sandbox portal first.
- Hosted Checkout / Page Redirection: build the `pp_*` request fields on the server (amount in **paisa**, i.e. PKR × 100, `pp_TxnRefNo` unique, `pp_TxnDateTime` and expiry in `yyyyMMddHHmmss`).
- Compute `pp_SecureHash` = HMAC-SHA256 with the Integrity Salt over the sorted non-empty `pp_` values as documented by JazzCash; post the form to the JazzCash endpoint.
- On the return/IPN callback, **recompute the hash** and check `pp_ResponseCode == "000"` before marking paid; optionally call the status inquiry API.
- Env: `JAZZCASH_MERCHANT_ID`, `JAZZCASH_PASSWORD`, `JAZZCASH_INTEGRITY_SALT`, `JAZZCASH_RETURN_URL`, `JAZZCASH_ENV`.
- Always follow the latest official integration guide from the merchant portal; field names and endpoints differ between versions.

## Easypaisa (Pakistan)
- Merchant account gives **Store ID** and **Hash Key**. Options: hosted checkout (redirect) or mobile-account (MA) API.
- Build the request on the server, generate the hash/encrypted value with the Hash Key as described in Easypaisa's merchant documentation, redirect or call the API.
- On the callback, verify the response and confirm with the transaction inquiry API before marking paid.
- Env: `EASYPAISA_STORE_ID`, `EASYPAISA_HASH_KEY`, `EASYPAISA_RETURN_URL`, `EASYPAISA_ENV`.

## Other regional gateways
| Region | Gateway | Notes |
|---|---|---|
| Pakistan | Safepay, PayFast (PK), bank IPGs | Safepay has a modern REST API + webhooks |
| India | Razorpay, Cashfree, PhonePe PG | Verify `razorpay_signature` (HMAC-SHA256 of `order_id|payment_id`) |
| Middle East | Tap, PayTabs, Checkout.com | Hosted pages + webhooks |
| Africa | Paystack, Flutterwave | Verify webhook hash; confirm with verify-transaction API |
| Bangladesh | bKash, SSLCommerz | Validate via IPN + validation API |

## Cash on Delivery (COD)
- Create order with `status = pending`, `gateway = "cod"`. Show "Pay on delivery".
- Admin/rider marks **delivered + collected** → `paid`. Add optional phone OTP to reduce fake orders.
- Track COD cash per rider for reconciliation.

## Bank transfer / manual
- Show account details, let the customer upload a receipt image; admin approves → `paid`.

## Checklist
- [ ] Amount computed server-side from DB
- [ ] Webhook/callback signature verified
- [ ] Idempotent (duplicate events ignored)
- [ ] Order states and emails/WhatsApp notifications for paid/failed
- [ ] Refund path documented
- [ ] Sandbox tested end-to-end, then switched to live keys
