---
name: camofox-browser
description: Anti-detection browser server for AI agents to browse the real web using Camoufox (Firefox fork with fingerprint spoofing)
category: browser
version: 1.0.0
---

# Camofox Browser

Anti-detection browser server for AI agents. Uses **Camoufox** (a Firefox fork with C++-level fingerprint spoofing) to bypass bot detection (Google, Cloudflare, etc.) by spoofing browser fingerprints before JavaScript sees them. Exposes a REST API on `localhost:9377` for agent workflows.

## When to Use

- **Bot detection bypass needed**: When websites detect and block automated browsers
- **Real web browsing**: Accessing production websites that require legitimate browser fingerprints
- **Accessibility snapshots**: Getting structured, accessible DOM trees with stable element references
- **Cookie-based sessions**: Maintaining authenticated sessions across requests
- **YouTube transcript extraction**: Getting video transcripts without API keys

## Server Status Check

The server is running on `localhost:9377`. Check health with:

```bash
curl http://localhost:9377/health
```

Expected response:
```json
{
  "ok": true,
  "engine": "camoufox",
  "browserConnected": true,
  "browserRunning": true,
  "activeTabs": 0,
  "activeSessions": 0,
  "consecutiveFailures": 0
}
```

## Quick Start

### 1. Create a Tab (New Browser Session)

```bash
curl -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "agent1",
    "sessionKey": "task1",
    "url": "https://example.com"
  }'
```

Response:
```json
{
  "tabId": "c6c9e4b2-0469-4f71-8273-28cd56b32fa4",
  "url": "https://example.com/"
}
```

### 2. Get Accessibility Snapshot

```bash
curl "http://localhost:9377/tabs/TAB_ID/snapshot?userId=agent1"
```

Response includes structured DOM with element references:
```json
{
  "url": "https://example.com/",
  "snapshot": "- heading \"Example Domain\" [level=1]\n- paragraph: ...\n- link \"Learn more\" [e1]: ...",
  "refsCount": 1,
  "truncated": false,
  "totalChars": 237
}
```

### 3. Click Element by Reference

```bash
curl -X POST http://localhost:9377/tabs/TAB_ID/click \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "agent1",
    "ref": "e1"
  }'
```

### 4. Type Text into Input

```bash
curl -X POST http://localhost:9377/tabs/TAB_ID/type \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "agent1",
    "ref": "e2",
    "text": "hello"
  }'
```

### 5. Close Tab (Cleanup)

```bash
curl -X DELETE http://localhost:9377/tabs/TAB_ID \
  -H 'Content-Type: application/json' \
  -d '{"userId": "agent1"}'
```

## Common Workflows

### Web Scraping with Bot Detection Bypass

1. Create tab with target URL
2. Get accessibility snapshot to understand page structure
3. Extract element references for interaction
4. Click, type, or navigate as needed
5. Repeat snapshot to verify state changes

### Authentication via Cookies

**Prerequisite**: Set `CAMOFOX_API_KEY` environment variable before starting server.

1. Export Netscape-format cookies from browser (e.g., `linkedin.txt`)
2. Save to `~/.camofox/cookies/` directory
3. Import via API:

```bash
curl -X POST http://localhost:9377/sessions/agent1/cookies \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "cookies": [
      {
        "name": "session_id",
        "value": "abc123",
        "domain": ".linkedin.com",
        "path": "/",
        "expires": 1234567890
      }
    ]
  }'
```

### YouTube Transcript Extraction

```bash
curl -X POST http://localhost:9377/youtube/transcript \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://youtube.com/watch?v=VIDEO_ID",
    "languages": ["en", "fr"]
  }'
```

### Search Macro (Google Search)

```bash
curl -X POST http://localhost:9377/tabs/TAB_ID/navigate \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "agent1",
    "macro": "@google_search",
    "query": "your search query"
  }'
```

## Available Endpoints

### Tab Lifecycle
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tabs` | Create new tab |
| GET | `/tabs` | List all tabs |
| DELETE | `/tabs/:id` | Close tab |

### Page Interaction
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tabs/:id/snapshot` | Accessibility snapshot (with optional `screenshot=true`) |
| POST | `/tabs/:id/click` | Click element by ref |
| POST | `/tabs/:id/type` | Type text into element |
| POST | `/tabs/:id/navigate` | Navigate to URL or use macro |
| POST | `/tabs/:id/scroll` | Scroll page |
| POST | `/tabs/:id/press` | Press keyboard key |
| GET | `/tabs/:id/links` | Get all links |
| GET | `/tabs/:id/images` | Get all images |
| GET | `/tabs/:id/downloads` | Get download status |
| GET | `/tabs/:id/screenshot` | Get screenshot (base64) |

### Sessions & Server
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/:userId/cookies` | Import cookies (requires API key) |
| POST | `/youtube/transcript` | Get YouTube transcript |
| GET | `/health` | Server health check |
| POST | `/start` | Start browser (if stopped) |
| POST | `/stop` | Stop browser (requires admin key) |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CAMOFOX_PORT` / `PORT` | Server port | `9377` |
| `CAMOFOX_API_KEY` | Enables cookie import | - |
| `CAMOFOX_ADMIN_KEY` | Required for `/stop` | - |
| `CAMOFOX_COOKIES_DIR` | Cookie files directory | `~/.camofox/cookies` |
| `PROXY_STRATEGY` | `backconnect` or blank | - |
| `PROXY_HOST`/`PORT`/`USERNAME`/`PASSWORD` | Simple proxy config | - |
| `PROXY_BACKCONNECT_HOST`/`PORT` | Backconnect proxy config | `7000` |
| `MAX_SESSIONS` | Max concurrent sessions | `50` |
| `SESSION_TIMEOUT_MS` | Session inactivity timeout | `1800000` (30 min) |
| `BROWSER_IDLE_TIMEOUT_MS` | Browser idle timeout | `300000` (5 min) |

## Installation

### Standalone (npm)
```bash
git clone https://github.com/jo-inc/camofox-browser && cd camofox-browser
npm install && npm start
```

### Docker
```bash
make up
# Or with explicit version:
make up ARCH=x86_64 VERSION=135.0.1 RELEASE=beta.24
```

### OpenClaw Plugin
```bash
openclaw plugins install @askjo/camofox-browser
```

## Tips & Best Practices

1. **Always check health first**: Before starting a workflow, verify `GET /health` returns `browserConnected: true`

2. **Use stable element references**: The `[e1]`, `[e2]` references in snapshots are stable across page reloads - use these for reliable interactions

3. **Clean up tabs**: Delete tabs when done to free resources:
   ```bash
   curl -X DELETE http://localhost:9377/tabs/TAB_ID
   ```

4. **Session isolation**: Use unique `userId` and `sessionKey` combinations to keep sessions separate

5. **Screenshot for debugging**: Add `screenshot=true` to snapshot requests for visual verification

6. **YouTube transcripts**: Requires `yt-dlp` - install with `pip install yt-dlp`

7. **Cookie import requires auth**: Set `CAMOFOX_API_KEY` before starting server to enable cookie import functionality

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not responding on port 9377 | Start server: `npm start` or `make up` |
| `browserConnected: false` | Wait for browser to initialize (first run downloads ~300MB Camoufox) |
| Element reference not found | Get fresh snapshot - DOM may have changed |
| Cookie import fails | Ensure `CAMOFOX_API_KEY` is set and `Authorization` header included |
| YouTube transcript fails | Install `yt-dlp` with `pip install yt-dlp` |

## Examples

### Complete Web Search Workflow

```bash
# 1. Create tab with Google
TAB_ID=$(curl -s -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","sessionKey":"search1","url":"https://google.com"}' | jq -r .tabId)

# 2. Get snapshot to find search input
curl -s "http://localhost:9377/tabs/${TAB_ID}/snapshot?userId=agent1"

# 3. Type search query (find the input element ref from snapshot)
curl -s -X POST http://localhost:9377/tabs/${TAB_ID}/type \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","ref":"e1","text":"camofox browser"}'

# 4. Submit search (find search button ref)
curl -s -X POST http://localhost:9377/tabs/${TAB_ID}/click \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","ref":"e2"}'

# 5. Get results snapshot
curl -s "http://localhost:9377/tabs/${TAB_ID}/snapshot?userId=agent1"

# 6. Clean up
curl -X DELETE http://localhost:9377/tabs/${TAB_ID}
```

### Extract Job Offer Details

```bash
# 1. Navigate to job offer
TAB_ID=$(curl -s -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","sessionKey":"job1","url":"https://company.com/jobs/123"}' | jq -r .tabId)

# 2. Get accessibility snapshot
SNAPSHOT=$(curl -s "http://localhost:9377/tabs/${TAB_ID}/snapshot?userId=agent1")

# 3. Parse snapshot to extract job title, description, requirements
# (Use your preferred JSON parser or LLM to extract structured data)

# 4. Close tab
curl -X DELETE http://localhost:9377/tabs/${TAB_ID}
```

## Related Skills

- `cv-job-application-workflow` - Uses camofox for job offer extraction
- `web-research-with-tavily` - Alternative web search method
- `ocr-and-documents` - Document parsing when browser extraction not possible
