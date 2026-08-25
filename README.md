# AI OS

AI OS is a cross-platform, offline-first agent platform that lets users control and automate devices, applications, browsers, IoT devices, TVs, and connected services through natural-language commands.

## Product Vision

AI OS provides one user-facing system across desktop, mobile, and web while distributing execution between local runtimes and cloud services.

The system is designed around:

- Offline-first local execution
- Local and cloud LLMs with intelligent routing
- Persistent and dynamic agents
- Scheduled and event-driven automation
- Multi-device and multi-agent orchestration
- Application discovery, resolution, capability discovery, and installation
- Device discovery and capability-based control
- Browser automation and API connectors
- IoT and smart-device integration
- Explicit permission and confirmation policies for sensitive actions

## Target Platforms

### User Applications

- Windows
- macOS
- Linux
- Android
- iOS / iPadOS
- Web

### Connected Nodes

- Windows PCs
- macOS devices
- Linux devices
- Android devices
- iOS / iPadOS devices
- Smart TVs
- IoT devices
- Browsers
- Cloud services and APIs

## Core Architecture

```text
                              AI OS
                                |
              +-----------------+-----------------+
              |                                   |
       User Applications                    Web Application
              |                                   |
       Local AI Runtime                         Next.js
              |
      +-------+----------------+
      |       |        |       |
   Local    Local    Tool   Permission
   Agent    LLM      Runtime  Engine
      |
      +------------------+
                         |
                  Agent Orchestrator
                         |
        +----------------+----------------+
        |                |                |
   Dynamic Agents   Automation       Device/App Layer
                    Scheduler              |
                                      +----+----+
                                      |         |
                                  Applications Devices
                                      |         |
                                  Browser   IoT / TV
                         |
                    Cloud Runtime
                         |
              +----------+----------+
              |                     |
           FastAPI              Server Agent
              |
       PostgreSQL / Redis
              |
          AI Gateway
```

## Runtime Model

### Local Runtime

Runs on the user's device and is responsible for offline-capable execution, local tools, local application and device discovery, local permissions, local events, and local LLM inference when available.

### Cloud Runtime

Runs on the server and provides persistent agents, orchestration, scheduling, multi-device coordination, shared state, cloud AI access, synchronization, and server-side services.

### Hybrid Execution

The Model Router chooses between local and cloud models according to task complexity, privacy, latency, available hardware, network state, user policy, and model capability.

```text
User Request
     |
     v
Task / Intent Router
     |
     +---- Simple / Private / Offline ----> Local LLM + Local Agent
     |
     +---- Complex / Cloud-capable -------> Cloud LLM / Server Agent
     |
     +---- Hybrid ------------------------> Local + Cloud
```

## Agent Model

AI OS supports multiple agent types:

- Local Agents — execute tasks on a user's device
- Server Agents — execute server-side tasks and coordinate distributed work
- Dynamic Agents — created from user instructions and persisted according to policy
- Browser Agents — operate supported browser environments
- Device Agents / Adapters — expose capabilities of TVs, IoT devices, and other connected nodes
- Service Connectors — integrate with cloud services and official APIs

Agents operate through capabilities and tools rather than hard-coded assumptions about a device or application.

## Application & Device Discovery

Before executing an application command, AI OS can resolve the requested application against the target device's application registry.

```text
User Command
    |
    v
Application Resolver
    |
    +-- Installed --> Capability Discovery --> Permission Check --> Execute
    |
    +-- Not Installed --> Official Store Resolver --> User Confirmation
                              |
                              v
                         Install / Verify
                              |
                              v
                       Capability Discovery
```

Application installation must use official and platform-supported installation mechanisms and must respect OS security restrictions.

Devices expose normalized capabilities through adapters so agents can operate across different hardware and protocols without embedding device-specific logic in the planner.

## Automation

Users can create persistent automations such as:

```text
Every day at 08:00
    -> Check email
    -> Detect new attachment
    -> Extract document text
    -> Summarize with local or cloud LLM
    -> Notify the user
```

Supported trigger categories include time, application events, files, devices, network events, webhooks, and other supported system events.

## Security Model

AI OS uses capability-based permissions and explicit confirmation for sensitive operations.

Examples of high-risk operations include:

- Financial transfers
- Purchases
- Account or credential changes
- Destructive file operations
- Application installation when confirmation is required

The agent may prepare and navigate a task, but sensitive operations remain subject to the applicable device, application, authentication, and user-confirmation controls.

## Technology Stack

| Layer | Technology |
|---|---|
| Desktop / Mobile UI | Flutter / Dart |
| Web | Next.js + TypeScript |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Cache / Queue | Redis |
| Containers | Docker / Docker Compose |
| Server Agent | Python |
| Local Agent | Platform runtime + shared contracts |
| AI | Local LLM + Cloud LLM abstraction |
| Realtime | WebSocket |
| API | REST / WebSocket |

## Development Machines

### Milad — MacBook M4

Primary owner for:

- Server and infrastructure
- FastAPI backend
- Server Agent
- AI / LLM layer
- Agent orchestration
- Dynamic agents and scheduler
- Device gateway
- macOS client and agent
- iOS / iPadOS build and release
- Next.js and production infrastructure

### Ashkan — Lenovo Windows

Primary owner for:

- Windows client and agent
- Flutter cross-platform client foundations
- Windows OS integration
- Android client and agent
- Application discovery and control on Windows
- Browser integration
- Local runtime and tools
- Windows release and testing

## Development Strategy

Platform ownership follows the actual build and test environments:

- Windows development and release: Ashkan's Lenovo Windows
- macOS and iOS/iPadOS development and release: Milad's MacBook M4 + Xcode
- Server development: Milad's MacBook M4 using Docker Compose
- Production server: Linux environment
- Shared contracts and cross-platform interfaces are maintained jointly

## Repository Documentation

- `docs/ARCHITECTURE.md` — system architecture and runtime boundaries
- `docs/ROADMAP.md` — phased execution plan and ownership
- `docs/PROTOCOLS.md` — agent, device, task, capability, and event contracts
- `docs/SECURITY.md` — security and permission model

## Status

The repository is in the architecture and foundation stage. Implementation must follow the contracts and phased roadmap before expanding platform-specific integrations.
