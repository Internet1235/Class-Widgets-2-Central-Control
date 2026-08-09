# Central Control Protocol

Protocol version: `1`

The terminal uses JSON over HTTP. A terminal pairs once, then sends one authenticated sync request every 10 seconds. Delivery is at-least-once: clients deduplicate commands by `command_id` and persist acknowledgements until accepted by the server.

## Security boundaries

- Device tokens are returned once and stored as hashes by the service.
- Production deployments require HTTPS.
- Commands are a fixed allowlist; arbitrary shell execution and arbitrary file access are not part of this protocol.
- Schedules use Class Widgets schedule schema version `1`.
- Policies contain typed, allowlisted keys only.

The authoritative OpenAPI document is served by FastAPI at `/openapi.json`.
