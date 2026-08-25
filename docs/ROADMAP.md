# AI OS — Execution Roadmap

## Team

### Milad — MacBook M4
- Development Server
- Docker / infrastructure
- FastAPI backend
- Server Agent
- AI / LLM layer
- macOS and iOS build environment

### Ashkan — Lenovo Windows
- Web application
- Flutter application shell
- Windows Client
- Client Agent

### Shared
- Client ↔ Server integration
- Cross-platform testing
- Release and distribution

## Phases

### Phase 0 — Repository & Development Standards
**Owner:** Ashkan

Git conventions, repository structure, branch strategy, documentation and CI foundation.

### Phase 1 — Server Infrastructure
**Owner:** Milad

Docker, Docker Compose, PostgreSQL, Redis, environment configuration and networking.

### Phase 2 — Backend Foundation
**Owner:** Milad

FastAPI, SQLAlchemy, Alembic, Pydantic, API architecture, logging, exceptions and health checks.

### Phase 3 — Authentication & Security Foundation
**Owner:** Milad

Users, authentication, authorization, JWT, refresh tokens, roles and permissions.

### Phase 4 — Core Backend
**Owner:** Milad

Domain models, database schema, repositories, services, core APIs, tasks and events.

### Phase 5 — Cross-Platform Client Core
**Owner:** Milad

Agent Core, communication, authentication, task engine, tool system, permissions and OS adapter interfaces.

### Phase 6 — Desktop & Mobile Framework
**Owner:** Ashkan

Flutter application shell targeting Windows, macOS, Linux, Android and iOS/iPadOS.

### Phase 7 — Windows Client
**Owner:** Ashkan

Windows Agent Adapter, filesystem/process integration, notifications, permissions, installer and testing.

### Phase 8 — macOS Client
**Owner:** Milad

macOS Agent Adapter, filesystem/process integration, notifications, permissions and Apple Silicon testing.

### Phase 9 — Linux Client
**Owner:** Milad + Ashkan

Linux Agent Adapter, x64/ARM64 support, packaging, permissions and desktop integration.

### Phase 10 — Server Agent
**Owner:** Milad

Agent runtime, task manager, tool manager, client manager, permission manager and LLM interface.

### Phase 11 — LLM / AI Layer
**Owner:** Milad

Cloud LLM, Local LLM, model abstraction, context, memory, tool calling and agent orchestration.

### Phase 12 — Client ↔ Server Integration
**Owner:** Milad + Ashkan

Authentication, device registration, secure communication, task synchronization, real-time events and recovery.

### Phase 13 — Web Application
**Owner:** Ashkan

Next.js + TypeScript dashboard, authentication, devices, agents, tasks, logs and settings.

### Phase 14 — Mobile
**Owner:** Milad + Ashkan

Flutter Android/iOS/iPadOS UI, authentication, device management, agent communication, notifications and mobile permissions.

### Phase 15 — Cross-Platform Security
**Owner:** Milad

Device identity, secure credential storage, permission isolation, encryption, TLS, token security, sandboxing and audit logs.

### Phase 16 — Testing
**Owner:** Milad + Ashkan

Unit, integration, API, agent, E2E, performance, security and compatibility testing across supported platforms.

### Phase 17 — Production
**Owner:** Milad

Linux production server, reverse proxy, Next.js, FastAPI, Server Agent, PostgreSQL and Redis deployment.

### Phase 18 — Release & Distribution
**Owner:** Milad + Ashkan

Windows installer, macOS application, Linux packages, Android package, iOS/iPadOS release and Web deployment.

## Platform Matrix

| Platform | Client | Primary Owner | Build/Test Environment |
|---|---|---|---|
| Windows | Flutter + Client Agent | Ashkan | Lenovo Windows |
| macOS | Flutter + Client Agent | Milad | MacBook M4 |
| Linux | Flutter + Client Agent | Milad + Ashkan | Linux CI/test environment |
| Android | Flutter | Milad + Ashkan | Android build/test environment |
| iOS/iPadOS | Flutter | Milad + Ashkan | MacBook M4 + Xcode |
| Web | Next.js | Ashkan | Lenovo Windows / CI |
| Server | Dockerized services | Milad | MacBook M4 → Linux Production |
