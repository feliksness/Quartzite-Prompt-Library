---
name: crypto-address-validator
description: Validate that a cryptocurrency address is correctly formatted and checksum-valid for its claimed chain (Bitcoin, Ethereum/EVM, Solana) before it's used anywhere — sending funds to a malformed or wrong-checksum address is often unrecoverable. Use whenever the user pastes a wallet address and wants it checked, or before including an address in any generated code, invoice, or documentation.
---

# Crypto Address Validator

## Purpose
A single mistyped character in a crypto address can send funds to an address nobody controls, with no way to reverse it. This skill runs the actual checksum/format validation for the address's claimed chain rather than just eyeballing the length and prefix.

## When to use
- User pastes an address and wants to confirm it's valid before using it.
- Before Claude itself outputs any address in generated code, a receipt, an invoice template, or documentation — validate it first, don't just pattern-match "looks like an address."
- Not for confirming an address belongs to a specific person/entity — format validity says nothing about ownership; never claim an address is "safe" or "legitimate" based on format checks alone.

## Workflow

1. Run the validator:
   ```bash
   python3 scripts/validate_address.py <address>
   ```
   It auto-detects likely chain family from the format and reports which specific check passed/failed:
   - **Bitcoin**: Base58Check checksum for legacy (`1...`)/P2SH (`3...`) addresses, and Bech32/Bech32m checksum for native SegWit (`bc1q...`)/Taproot (`bc1p...`)
   - **Ethereum/EVM**: hex format + length (0x + 40 hex chars), and EIP-55 mixed-case checksum validation if the address uses mixed case
   - **Solana**: Base58 format + 32-byte length check

2. Report the result plainly: valid + chain family, or invalid + the specific reason (bad checksum, wrong length, invalid character set).

3. If invalid, do not attempt to "fix" or guess the intended address — ask the user to re-copy it from the source, since a guessed correction could send funds to a different real address.

## Notes
- A format-valid address is not proof of ownership or that it's the intended recipient — for any real transfer, always recommend the user also do a small test transaction first and independently verify via a second channel for large amounts.
- EVM addresses without mixed case (all lowercase/uppercase) skip EIP-55 checksum by convention — that's valid, not an error, but mention that no checksum protection was present for that specific address.
