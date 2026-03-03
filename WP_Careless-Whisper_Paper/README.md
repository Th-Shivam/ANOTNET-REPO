# wp_rtt_probe — WhatsApp RTT Probe

Measures **Round-Trip Time (RTT)** to a WhatsApp contact using **Stealthy Reaction messages** (reactions to placeholder/old message IDs that generate **zero pop-up notifications** on the target's device).

---

## How it works

```
You  ──── Reaction(emoji) ────►  WA Server  ──── deliver ───►  Target device
                                                              (no notification)
You  ◄─── Receipt (double tick) ─  WA Server  ◄──  ack  ──── Target device
         ▲ RTT measured here ▲
```

1. The script sends a `ReactionMessage` proto to the target JID.
2. The reaction points to a placeholder message-ID (`3EB0_PROBE_PLACEHOLDER`) that does not exist → target's WhatsApp silently processes it, triggering **no notification**.
3. WhatsApp still generates a **delivery receipt** (double-tick) for the reaction packet.
4. The script records `sent_ns` (nanoseconds since epoch) before the network call and `acked_ns` when the receipt arrives.
5. `RTT = acked_ns − sent_ns` is printed to **STDOUT**.
6. The loop sleeps a **random interval between 2–20 seconds** before the next probe.

---

## Build

```bash
go build -o wp_rtt_probe .
```

Requires:
- Go 1.25+
- CGO enabled (for `go-sqlite3`)
- `gcc` installed (`apt install build-essential`)

---

## Usage

```bash
./wp_rtt_probe <phone_number_with_country_code>
```

### Example

```bash
./wp_rtt_probe 919876543210
```

**First run** — QR code appears in terminal. Scan it with WhatsApp:  
`Settings → Linked Devices → Link a Device`

**Subsequent runs** — Session is loaded from `session.db` automatically.

---

## Sample Output

```
Connected to WhatsApp. Starting RTT probe loop …
Target : 919876543210@s.whatsapp.net
Interval: 2–20 seconds (random)

─────────────────────────────────────────────────────────────
Seq   MessageID                        Sent (UTC)                  Acked (UTC)                 RTT (ns)
─────────────────────────────────────────────────────────────
[seq=1] ✉  Sent  MsgID=3EB0C1A2B3D4E5F6  at 10:22:01.123456789
RTT  MsgID=3EB0C1A2B3D4E5F6  Sent=1709288521123456789 ns  Acked=1709288521456789012 ns  RTT=333332223 ns  (333.332 ms)
```

---

## Files

| File | Description |
|------|-------------|
| `main.go` | Main probe script |
| `session.db` | SQLite session store (auto-created on first login) |
| `go.mod` / `go.sum` | Go module dependencies |
| `wp_rtt_probe` | Compiled binary |

---

## Stop

Press `Ctrl+C` for a clean shutdown.

---

## ⚠️ Disclaimer

This tool is for **research and educational purposes only**. Use responsibly and only on accounts/contacts you have permission to test.
