#!/usr/bin/env python3
"""Validate cryptocurrency addresses (Bitcoin, Ethereum/EVM, Solana) using
real checksum algorithms, standard library only (hashlib for sha256/keccak
via a small pure-Python fallback isn't included for keccak, so ETH check
covers format + EIP-55 case-checksum only, not a full keccak recompute of
the address from a public key).

Usage:
    python3 validate_address.py <address>
"""
import argparse
import hashlib
import sys

B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def b58decode(s):
    num = 0
    for char in s:
        if char not in B58_ALPHABET:
            raise ValueError(f"invalid base58 character: {char!r}")
        num = num * 58 + B58_ALPHABET.index(char)
    combined = num.to_bytes((num.bit_length() + 7) // 8, "big") if num else b""
    n_pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * n_pad + combined


def check_bitcoin_legacy(addr):
    try:
        raw = b58decode(addr)
    except ValueError as e:
        return False, str(e)
    if len(raw) != 25:
        return False, f"decoded length {len(raw)} != 25 bytes"
    payload, checksum = raw[:-4], raw[-4:]
    computed = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    if computed != checksum:
        return False, "Base58Check checksum mismatch (likely a typo)"
    return True, "valid Base58Check checksum (legacy/P2SH Bitcoin address)"


def bech32_polymod(values):
    GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp):
    return [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]


def check_bech32(addr):
    if "1" not in addr:
        return False, "no separator '1' found"
    hrp, data_part = addr.rsplit("1", 1)
    if not data_part:
        return False, "empty data part"
    try:
        data = [BECH32_CHARSET.index(c) for c in data_part.lower()]
    except ValueError as e:
        return False, f"invalid bech32 character: {e}"
    const = bech32_polymod(bech32_hrp_expand(hrp.lower()) + data)
    # 1 = bech32 (SegWit v0), 0x2bc830a3 = bech32m (Taproot / SegWit v1+)
    if const == 1:
        return True, f"valid Bech32 checksum, hrp={hrp!r} (native SegWit)"
    if const == 0x2bc830a3:
        return True, f"valid Bech32m checksum, hrp={hrp!r} (Taproot)"
    return False, "bech32/bech32m checksum mismatch (likely a typo)"


def check_ethereum(addr):
    if not addr.startswith("0x") and not addr.startswith("0X"):
        return False, "missing 0x prefix"
    body = addr[2:]
    if len(body) != 40:
        return False, f"expected 40 hex chars after 0x, got {len(body)}"
    try:
        int(body, 16)
    except ValueError:
        return False, "contains non-hexadecimal characters"

    if body == body.lower() or body == body.upper():
        return True, "valid hex format (all lowercase/uppercase — no EIP-55 checksum encoded, which is allowed but offers no typo protection)"

    # EIP-55 checksum validation requires Keccak-256, not in hashlib.
    # We can still validate structurally; note the limitation explicitly.
    return True, "valid hex format with mixed-case (EIP-55-style) — full EIP-55 checksum verification requires Keccak-256, not available in the standard library here; structural format is valid"


def check_solana(addr):
    try:
        raw = b58decode(addr)
    except ValueError as e:
        return False, str(e)
    if len(raw) != 32:
        return False, f"decoded length {len(raw)} != 32 bytes (Solana pubkeys are 32 bytes)"
    if not (32 <= len(addr) <= 44):
        return False, f"address string length {len(addr)} outside typical 32-44 char range"
    return True, "valid Base58, decodes to 32 bytes (Solana-format public key)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("address")
    args = ap.parse_args()
    addr = args.address.strip()

    print(f"Address: {addr}\n")

    if addr.lower().startswith(("bc1", "tb1")):
        ok, msg = check_bech32(addr)
        chain = "Bitcoin (SegWit/Taproot)"
    elif addr.startswith(("1", "3")):
        ok, msg = check_bitcoin_legacy(addr)
        chain = "Bitcoin (legacy/P2SH)"
    elif addr.lower().startswith("0x"):
        ok, msg = check_ethereum(addr)
        chain = "Ethereum/EVM"
    else:
        ok, msg = check_solana(addr)
        chain = "Solana (best guess — no distinctive prefix)"

    status = "VALID" if ok else "INVALID"
    print(f"[{status}] {chain}")
    print(f"  {msg}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
