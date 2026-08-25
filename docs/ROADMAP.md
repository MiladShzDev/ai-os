# AI OS — Execution Roadmap

## Team Ownership

### Milad — MacBook M4

Primary owner:

- Server and infrastructure
- FastAPI backend
- PostgreSQL / Redis / Docker
- Server Agent
- AI / LLM layer and model routing
- Agent Orchestrator
- Dynamic Agents
- Scheduler / Automation Engine
- Device Gateway and IoT protocols
- macOS client and agent
- iOS / iPadOS build, testing and release
- Next.js and production infrastructure

### Ashkan — Lenovo Windows

Primary owner:

- Windows client and agent
- Flutter cross-platform client foundations
- Windows OS integration
- Android client and agent
- Local runtime and tools
- Windows application discovery and control
- Browser integration
- Windows release and testing

### Shared

- Architecture contracts
- Client ↔ Server integration
- Cross-platform interfaces
- Integration and E2E testing
- Release validation

## Phase 0 — Architecture & Contracts

**Owners:** Milad + Ashkan

Define and review before large-scale implementation:

- System architecture
- Runtime boundaries
- Device model
- Application model
- Capability model
- Agent model
- Task model
- Tool model
- Permission model
- Automation model
- Event model
- Client ↔ Server protocol
- Repository structure and development standards

## Phase 1 — Repository & Development Infrastructure

**Milad:** Server infrastructure  
**Ashkan:** Client repository foundation

### Milad

- Docker / Docker Compose
- PostgreSQL
- Redis
- Environment configuration
- Development networking
- Server logging and configuration

### Ashkan

- Flutter repository structure
- Windows client skeleton
- Local storage foundation
- Client configuration
- Shared client contracts

## Phase 2 — Backend Foundation

**Owner:** Milad

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- API versioning
- REST foundation
- WebSocket foundation
- Logging
- Exceptions
- Health checks
- Configuration management

## Phase 3 — Identity, Device Registration & Security Foundation

**Owner:** Milad  
**Client implementation:** Ashkan / Milad by platform

- User identity
- Authentication
- Authorization
- Device identity
- Device registration
- Device sessions
- Device tokens
- Heartbeat / online state
- Secure communication
- Initial permission model

## Phase 4 — Core Domain & State

**Owner:** Milad

- Device Registry
- Application Registry
- Agent Registry
- Task Registry
- Capability Registry
- Tool Registry
- Event model
- Repositories
- Services
- Core APIs
- Persistent task state

## Phase 5 — Local Runtime & Local Agent

**Windows owner:** Ashkan  
**macOS owner:** Milad

Implement the local runtime as an independent execution environment capable of operating without the server for supported tasks.

### Local Runtime

- Local Agent lifecycle
- Local Tool Runtime
- Local storage
- Local event bus
- Local permissions
- Offline execution
- Local task state
- Server synchronization

### Platform adapters

- Windows Agent Adapter
- macOS Agent Adapter
- OS process integration
- Filesystem integration
- Application launch
- Notifications
- Platform permissions

## Phase 6 — Application Discovery & Control

**Windows:** Ashkan  
**macOS:** Milad  
**Server registry:** Milad

- Installed application scanning
- Application identity
- Application Registry
- Application Resolver
- Application metadata
- Application launch
- Application state
- Capability Discovery
- Platform-specific application control

Required execution path:

```text
User Command
  -> Application Resolver
  -> Installed?
  -> Capability Discovery
  -> Permission Check
  -> Execute
```

## Phase 7 — Application Installation

**Windows:** Ashkan  
**macOS:** Milad  
**Store Resolver / task model:** Milad

- Official Store detection
- Store Resolver
- Package metadata
- User confirmation
- Platform-supported installation
- Installation verification
- Installation state
- Audit events

AI OS must not bypass platform security or install untrusted application packages as part of normal application resolution.

## Phase 8 — AI / LLM Layer

**Owner:** Milad  
**Local runtime integrations:** Milad + Ashkan

- AI provider abstraction
- Local LLM abstraction
- Cloud LLM abstraction
- Model Router
- Context management
- Streaming
- Tool calling
- Memory foundation
- Embeddings / RAG foundation
- Hardware-aware local inference
- Offline inference

Routing considers task complexity, privacy, latency, hardware, network state, user policy and model capability.

## Phase 9 — Agent Orchestrator

**Owner:** Milad

- Planner
- Task engine
- Tool selection
- Agent selection
- Device selection
- Application selection
- Task state machine
- Retry
- Cancellation
- Verification
- Agent delegation
- Multi-agent task dependencies

## Phase 10 — Dynamic Agents

**Owner:** Milad  
**Local execution:** platform owners

Support agents created from natural-language instructions and persisted according to user policy.

- Dynamic Agent definition
- Agent lifecycle
- Persistent Agent state
- Agent memory
- Agent execution policy
- Agent recovery
- Agent logs
- Agent-to-agent delegation

Example:

```text
Every day at 08:00
  -> Check email
  -> Detect new attachment
  -> Extract text
  -> Summarize
  -> Notify user
```

## Phase 11 — Scheduler & Automation Engine

**Owner:** Milad

- Time triggers
- Event triggers
- Conditions
- Workflow execution
- Persistent jobs
- Task queue
- Retry policies
- Job recovery
- Automation history

Supported trigger classes include time, application events, files, devices, network events, webhooks and other supported events.

## Phase 12 — Client ↔ Server Integration

**Owners:** Milad + Ashkan

- Device pairing
- Secure communication
- Task synchronization
- Real-time events
- Local/cloud state synchronization
- Offline queue
- Reconnection
- Conflict handling
- Remote task execution

## Phase 13 — Browser Agent

**Ashkan:** local browser integration  
**Milad:** browser protocol / server runtime

- Browser Agent protocol
- Browser session management
- Browser extension / local integration
- Navigation
- Page interaction
- DOM interaction
- Browser permissions
- Browser security
- Official API connectors where available

Priority:

```text
Official API
  -> Native integration
  -> Browser automation
```

## Phase 14 — Android

**Owner:** Ashkan  
**Server / push integration:** Milad

- Android Flutter application
- Android Agent
- Application Discovery
- Application Resolver
- Deep Links
- OS permissions
- Notifications
- Background execution where platform policy permits
- Android device registration
- Android task execution

## Phase 15 — iOS / iPadOS

**Owner:** Milad

- Flutter iOS / iPadOS application
- iOS Agent integration
- Application Discovery where platform APIs permit
- Deep Links
- Notifications
- Background execution where platform policy permits
- OS permissions
- Xcode builds
- Signing
- TestFlight
- App Store release

## Phase 16 — Linux

**Owners:** Milad + Ashkan

- Linux Agent Adapter
- x64 / ARM64 support
- Application Discovery
- Packaging
- Permissions
- Desktop integration
- CI/test environment

## Phase 17 — Device Gateway / TV / IoT

**Milad:** gateway and protocols  
**Ashkan:** local adapters and testing

- Universal Device / Node model
- Device Discovery
- Capability Discovery
- Device Gateway
- MQTT
- Matter
- Local network discovery
- Smart TV integration
- IoT adapters
- Device control

## Phase 18 — Multi-Device / Multi-Agent Orchestration

**Owner:** Milad  
**Execution:** platform owners

- Multi-device tasks
- Agent delegation
- Task dependencies
- Cross-device context
- Distributed task state
- Device-to-device execution
- File transfer where permitted
- Result aggregation

## Phase 19 — Web Application

**Owner:** Milad  
**UI support:** Ashkan

- Next.js + TypeScript
- Authentication
- Device management
- Agent management
- Task management
- Automation management
- Logs
- Settings
- Real-time task state

## Phase 20 — Security Hardening

**Owner:** Milad  
**Platform security:** Ashkan + Milad

- Authentication hardening
- Authorization
- Capability-based permissions
- Confirmation policies
- Device identity
- Credential storage
- Encryption
- TLS
- Token rotation
- Sandboxing / OS permissions
- Audit logs
- Rate limiting
- Sensitive-action controls

## Phase 21 — Testing

**Owners:** Milad + Ashkan

- Unit tests
- Integration tests
- API tests
- Agent tests
- Local/offline tests
- E2E tests
- Multi-device tests
- Performance tests
- Security tests
- Compatibility tests
- Cross-platform release validation

## Phase 22 — Production

**Owner:** Milad

- Linux production server
- Docker deployment
- Reverse proxy
- FastAPI
- Server Agent
- Next.js
- PostgreSQL
- Redis
- Monitoring
- Metrics
- Logging
- Backup
- Recovery
- CI/CD
- Server scaling foundation

## Phase 23 — Release & Distribution

**Windows / Android:** Ashkan  
**macOS / iOS / server:** Milad  
**Shared:** release validation

- Windows installer
- Windows auto-update
- macOS application
- macOS distribution
- iOS / iPadOS release
- Android package / distribution
- Linux packages
- Web deployment
- Production documentation

## MVP Boundary

The first end-to-end MVP must prove this path before expanding into IoT and advanced multi-device automation:

```text
Windows / macOS
      |
      v
Local Runtime + Local Agent
      |
      +---- offline local task
      |
      v
FastAPI Server
      |
      v
Server Agent + AI Router
      |
      v
Application Discovery
      |
      v
Capability Discovery
      |
      v
Permission Check
      |
      v
Execute Task
```

After this path is stable, Dynamic Agents, Scheduler, Browser, Mobile, TV/IoT and advanced multi-device orchestration are expanded incrementally.

## Platform Matrix

| Platform | Client | Primary Owner | Build/Test Environment |
|---|---|---|---|
| Windows | Flutter + Windows Agent | Ashkan | Lenovo Windows |
| macOS | Flutter + macOS Agent | Milad | MacBook M4 |
| Linux | Flutter + Linux Agent | Milad + Ashkan | Linux CI/test environment |
| Android | Flutter + Android Agent | Ashkan | Android build/test environment |
| iOS/iPadOS | Flutter + iOS integration | Milad | MacBook M4 + Xcode |
| Web | Next.js | Milad | MacBook M4 / CI |
| Server | Dockerized services | Milad | MacBook M4 -> Linux Production |
| TV / IoT | Device adapters | Milad + Ashkan | Local network / test devices |
