// wp_rtt_probe - WhatsApp RTT Probe using whatsmeow
// Measures Round-Trip Time using "Stealthy Reaction" messages
// (reactions to old messages do NOT generate pop-up notifications)
//
// Usage: ./wp_rtt_probe <target_phone_number_with_country_code>
// Example: ./wp_rtt_probe 919876543210
//
// The probe sends a reaction to a dummy/placeholder message ID on the target JID.
// WhatsApp delivers a receipt (double tick) for reactions just like normal messages.
// Since we react to a non-existent/old message, the target sees NO notification,
// making this a "stealthy" RTT measurement.

package main

import (
	"context"
	"fmt"
	"math/rand"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	_ "github.com/mattn/go-sqlite3"
	qrterm "github.com/mdp/qrterminal/v3"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/proto/waCommon"
	"go.mau.fi/whatsmeow/proto/waE2E"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
)

// ─────────────────────────────────────────────
//  Probe constants / config
// ─────────────────────────────────────────────

const (
	sessionDB = "session.db" // SQLite file that persists WhatsApp session

	minIntervalSec = 2  // minimum sleep between pings  (seconds)
	maxIntervalSec = 20 // maximum sleep between pings  (seconds)

	// A reaction is sent *to* this placeholder message-ID on the target JID.
	// Because this message-ID very likely does not exist in the target's chat,
	// WhatsApp silently delivers the reaction packet without a pop-up notification.
	stealthyReactionMsgID = "3EB0_PROBE_PLACEHOLDER"

	// The emoji we send as the reaction (single emoji, UTF-8).
	reactionEmoji = "👍"
)

// ─────────────────────────────────────────────
//  pendingPing – tracks in-flight send timestamps
// ─────────────────────────────────────────────

type pendingPing struct {
	sentAt    time.Time
	messageID types.MessageID
}

var (
	mu      sync.Mutex
	pending = make(map[types.MessageID]*pendingPing)
)

// ─────────────────────────────────────────────
//  main
// ─────────────────────────────────────────────

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: wp_rtt_probe <phone_number_with_country_code>")
		fmt.Fprintln(os.Stderr, "Example: wp_rtt_probe 919876543210")
		os.Exit(1)
	}

	targetPhone := os.Args[1]

	// Build the target JID (user@s.whatsapp.net)
	targetJID, err := types.ParseJID(targetPhone + "@s.whatsapp.net")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid phone number %q: %v\n", targetPhone, err)
		os.Exit(1)
	}

	// ── 1. Open / create the SQLite session store ──────────────────────────
	dbLog := waLog.Stdout("DB", "WARN", true)
	container, err := sqlstore.New(context.Background(), "sqlite3", "file:"+sessionDB+"?_foreign_keys=on", dbLog)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to open session DB: %v\n", err)
		os.Exit(1)
	}

	// Load existing device or create a new one
	deviceStore, err := container.GetFirstDevice(context.Background())
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get device: %v\n", err)
		os.Exit(1)
	}

	// ── 2. Create whatsmeow client ──────────────────────────────────────────
	clientLog := waLog.Stdout("Client", "WARN", true)
	client := whatsmeow.NewClient(deviceStore, clientLog)

	// ── 3. Register event handler for receipts ──────────────────────────────
	client.AddEventHandler(func(evt interface{}) {
		handleEvent(evt)
	})

	// ── 4. Connect / QR login ───────────────────────────────────────────────
	if client.Store.ID == nil {
		// No session yet → QR code login
		qrChan, _ := client.GetQRChannel(context.Background())
		if err := client.Connect(); err != nil {
			fmt.Fprintf(os.Stderr, "Connect error: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("Scan the QR code below with WhatsApp (Linked Devices → Link a Device):")
		for evt := range qrChan {
			if evt.Event == "code" {
				qrterm.GenerateHalfBlock(evt.Code, qrterm.L, os.Stdout)
			} else {
				fmt.Println("QR event:", evt.Event)
				if evt.Event == "success" {
					break
				}
			}
		}
	} else {
		// Existing session – just reconnect
		if err := client.Connect(); err != nil {
			fmt.Fprintf(os.Stderr, "Reconnect error: %v\n", err)
			os.Exit(1)
		}
	}

	fmt.Println("Connected to WhatsApp. Starting RTT probe loop …")
	fmt.Printf("Target : %s\n", targetJID)
	fmt.Printf("Interval: %d–%d seconds (random)\n\n", minIntervalSec, maxIntervalSec)
	fmt.Println("─────────────────────────────────────────────────────────────")
	fmt.Printf("%-5s  %-30s  %-26s  %-26s  RTT (ns)\n",
		"Seq", "MessageID", "Sent (UTC)", "Acked (UTC)")
	fmt.Println("─────────────────────────────────────────────────────────────")

	// ── 5. Graceful-shutdown on SIGINT / SIGTERM ────────────────────────────
	ctx, cancel := context.WithCancel(context.Background())
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigCh
		fmt.Println("\nShutting down …")
		cancel()
		client.Disconnect()
	}()

	// ── 6. Probe loop ────────────────────────────────────────────────────────
	seq := 0
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))

	for {
		select {
		case <-ctx.Done():
			return
		default:
		}

		seq++
		msgID := whatsmeow.GenerateMessageID()

		// Build the Reaction message proto
		// We react to stealthyReactionMsgID which is a placeholder –
		// the target receives the reaction silently (no notification).
		reactionMsg := &waE2E.Message{
			ReactionMessage: &waE2E.ReactionMessage{
				Key: &waCommon.MessageKey{
					RemoteJID: proto.String(targetJID.String()),
					FromMe:    proto.Bool(false),
					ID:        proto.String(stealthyReactionMsgID),
				},
				Text:              proto.String(reactionEmoji),
				SenderTimestampMS: proto.Int64(time.Now().UnixMilli()),
			},
		}

		// Record send time in nanoseconds BEFORE the network call
		sentNs := time.Now().UnixNano()
		sentTime := time.Now().UTC()

		// Register the pending ping BEFORE sending so the receipt handler
		// cannot beat us to it.
		mu.Lock()
		pending[msgID] = &pendingPing{
			sentAt:    sentTime,
			messageID: msgID,
		}
		mu.Unlock()

		// Send the reaction message with simple retry/reconnect logic to
		// handle transient websocket/usync failures that can leave the
		// store without device JIDs (observed as EOF / disconnected errors).
	var resp whatsmeow.SendResponse
	var sendErr error
		const maxAttempts = 3
		for attempt := 1; attempt <= maxAttempts; attempt++ {
			resp, sendErr = client.SendMessage(ctx, targetJID, reactionMsg,
				whatsmeow.SendRequestExtra{ID: msgID})
			if sendErr == nil {
				break
			}
			// Log the transient error and try to recover by reconnecting.
			fmt.Fprintf(os.Stderr, "[seq=%d] SendMessage error (attempt %d/%d): %v\n", seq, attempt, maxAttempts, sendErr)

			// Try a graceful disconnect then reconnect. Ignore connect errors
			// for now — we'll retry the send in the next loop iteration.
			client.Disconnect()
			time.Sleep(500 * time.Millisecond)
			if err := client.Connect(); err != nil {
				fmt.Fprintf(os.Stderr, "[seq=%d] Reconnect error: %v\n", seq, err)
			} else {
				// Allow a short moment for usync/device info to populate.
				time.Sleep(500 * time.Millisecond)
			}
		}

		if sendErr != nil {
			fmt.Fprintf(os.Stderr, "[seq=%d] SendMessage failed after %d attempts: %v\n", seq, maxAttempts, sendErr)
			mu.Lock()
			delete(pending, msgID)
			mu.Unlock()
		} else {
			// resp.Timestamp is when the server accepted the message.
			// We use our local high-res clock for maximum precision.
			_ = resp
			_ = sentNs // kept for reference; we use the struct's sentAt field in handler

			// The actual RTT is printed by the event handler when the
			// delivery receipt arrives. Print a "sent" confirmation now.
			fmt.Printf("[seq=%d] ✉  Sent  MsgID=%-30s  at %s\n",
				seq, msgID, sentTime.Format("15:04:05.000000000"))
		}

		// Wait for a random interval before next probe
		interval := time.Duration(minIntervalSec+rng.Intn(maxIntervalSec-minIntervalSec+1)) * time.Second
		select {
		case <-ctx.Done():
			return
		case <-time.After(interval):
		}
	}
}

// ─────────────────────────────────────────────
//  handleEvent – processes incoming WhatsApp events
// ─────────────────────────────────────────────

func handleEvent(rawEvt interface{}) {
	switch evt := rawEvt.(type) {

	// Receipt event: server / device delivery ticks
	case *events.Receipt:
		ackedAt := time.Now() // capture immediately – maximum precision
		ackedNs := ackedAt.UnixNano()

		// We only care about "delivered" (double-tick) receipts.
		// types.ReceiptTypeDelivered == server delivery confirmation.
		if evt.Type != types.ReceiptTypeDelivered && evt.Type != types.ReceiptTypeRead {
			return
		}

		mu.Lock()
		for _, msgID := range evt.MessageIDs {
			pp, ok := pending[msgID]
			if !ok {
				continue
			}
			delete(pending, msgID)
			mu.Unlock()

			sentNs := pp.sentAt.UnixNano()
			rttNs := ackedNs - sentNs

			// ── STDOUT output (machine-readable + human-readable) ──────────
			fmt.Printf("RTT  MsgID=%-30s  Sent=%d ns  Acked=%d ns  RTT=%d ns  (%.3f ms)\n",
				msgID,
				sentNs,
				ackedNs,
				rttNs,
				float64(rttNs)/1e6,
			)

			mu.Lock()
		}
		mu.Unlock()
	}
}
