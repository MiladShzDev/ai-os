# AI OS — Architecture

## 1. Purpose

AI OS is an offline-first, cross-platform agent platform for controlling and automating user devices, applications, browsers, TVs, IoT devices and connected services.

The architecture separates local execution from cloud coordination while allowing both to participate in the same agent system.

## 2. High-Level Architecture

```text
                              USER
                                |
                                v
                    +------------------------+
                    | AI OS User Applications |
                    | Flutter / Next.js       |
                    +-----------+------------+
                                |
                         Local AI Runtime
                                |
             +------------------+------------------+
             |                  |                  |
        Local Agent         Local LLM        Local Tools
             |                  |                  |
             +------------------+------------------+
                                |
                        Agent Orchestrator
                                |
          +---------------------+---------------------+
          |                     |                     |
   Dynamic Agents        Automation Engine      Device/App Layer
          |                 + Scheduler                |
          |                                             |
          +---------------------+-----------------------+
                                |
                         Cloud Runtime
                                |
                +---------------+---------------+
                |               |               |
             FastAPI       Server Agent      AI Gateway
                |               |               |
          PostgreSQL          Redis          Cloud LLMs
```

## 3. Local Runtime

The Local Runtime exists on supported user devices.

Responsibilities:

- Local Agent lifecycle
- Local LLM inference
- Local tools
- Application discovery
- Application control
- Device discovery
- Local capability discovery
- OS permissions
- Local events
- Offline task execution
- Local task state
- Synchronization with the cloud runtime

The Local Runtime must remain useful when the server is unavailable for tasks that do not require remote services.

## 4. Cloud Runtime

The Cloud Runtime provides services that benefit from persistent availability or centralized coordination:

- FastAPI API
- Server Agent
- Agent Orchestrator
- Dynamic Agent persistence
- Scheduler
- Automation Engine
- Multi-device coordination
- Shared state
- Cloud AI access
- Task queue
- Device registry
- Application metadata
- Audit and operational logs

The production Cloud Runtime runs on Linux. Development uses Docker Compose on Milad's MacBook M4.

## 5. Node Model

Every controllable endpoint is modeled as a Node.

```text
Node
├── Windows
├── macOS
├── Linux
├── Android
├── iOS / iPadOS
├── Browser
├── Smart TV
├── IoT device
└── Cloud service / API
```

A Node exposes normalized capabilities through an adapter or connector.

## 6. Agent Model

### Local Agent

Executes device-local tasks and uses local tools and OS integrations.

### Server Agent

Executes server-side work and coordinates tasks across devices and agents.

### Dynamic Agent

Created from a user instruction and persisted according to user policy. Dynamic Agents can have triggers, conditions, tools, memory, permissions and target nodes.

### Browser Agent

Controls supported browser environments. Official APIs are preferred over browser automation when they provide the required capability.

### Device Agent / Adapter

Maps device-specific protocols into the normalized capability model.

### Service Connector

Connects AI OS to official APIs and supported cloud services.

## 7. Application Model

Applications are first-class entities on a Node.

```text
Application
├── Identity
├── Package ID
├── Version
├── Install State
├── Launch Information
├── Capabilities
└── Source / Store Metadata
```

Before execution, the Application Resolver determines whether the requested application exists on the selected Node.

If it is not installed, AI OS may resolve an official store and request user confirmation before installation, subject to platform rules.

## 8. Capability Model

Agents do not assume that an application or device supports an action merely because of its name.

```text
Application / Device
        |
        v
Capability Discovery
        |
        v
Normalized Capabilities
        |
        v
Planner / Agent
```

Examples:

- `application.open`
- `browser.navigate`
- `file.read`
- `device.power_on`
- `tv.set_channel`
- `email.read`
- `email.send`
- `bank.transfer`

Sensitive capabilities require stronger permission policies.

## 9. Task Execution

```text
User Request
    |
    v
Intent / Task Router
    |
    v
Target Node Resolver
    |
    v
Application / Capability Resolver
    |
    v
Permission Engine
    |
    v
Planner
    |
    v
Selected Agent + Tools
    |
    v
Execution
    |
    v
Verification / Result
```

The system must verify execution results rather than treating tool invocation alone as proof of success.

## 10. Local / Cloud AI Routing

The AI Router selects local, cloud, or hybrid execution.

Factors include:

- Task complexity
- Privacy requirements
- Network availability
- Latency
- Device CPU/GPU/RAM
- Model capability
- Cost policy
- User policy

Online availability does not force every task to the cloud. Lightweight and private tasks can remain local.

## 11. Dynamic Automation

A user can convert natural-language instructions into persistent automation.

```text
User
 |
 v
Dynamic Agent Definition
 |
 +-- Trigger
 +-- Conditions
 +-- Target Nodes
 +-- Tools / Capabilities
 +-- LLM Policy
 +-- Permission Policy
 +-- Notification Policy
 |
 v
Scheduler / Event Engine
 |
 v
Agent Execution
```

Triggers can include time, files, applications, devices, network events, webhooks and other supported events.

## 12. Multi-Agent / Multi-Device

Tasks can span multiple Nodes and Agents.

```text
Phone
  |
  v
Orchestrator
  |
  +--> Gmail Connector
  |
  +--> Document Agent
  |
  +--> Local / Cloud LLM
  |
  +--> Phone Notification Agent
  |
  +--> TV Adapter
```

The orchestrator maintains task dependencies and shared execution state.

## 13. Security Boundary

Security is enforced at multiple levels:

- User identity
- Device identity
- Agent identity
- Capability permissions
- Tool permissions
- OS permissions
- Application permissions
- User confirmation
- Authentication required by external services

Financial transfers, purchases, credential changes and other high-risk actions require explicit policy-controlled confirmation and/or native authentication where applicable.

## 14. Platform Strategy

### Windows

Owner: Ashkan. Development and testing on Lenovo Windows.

### macOS

Owner: Milad. Development and testing on MacBook M4.

### Android

Owner: Ashkan. Android build/test environment.

### iOS / iPadOS

Owner: Milad. MacBook M4 + Xcode.

### Linux

Shared ownership and Linux CI/test environment.

### Web

Next.js application. Milad is primary owner; Ashkan supports UI and integration.

## 15. Architectural Principles

1. Local execution first for eligible tasks.
2. Cloud is an extension, not a mandatory dependency for every local task.
3. Agents operate through capabilities and tools.
4. Devices and applications are discoverable entities.
5. Sensitive actions require explicit permission policies.
6. Dynamic agents are persistent system entities, not temporary chat prompts.
7. Protocols are platform-neutral; platform adapters contain OS-specific behavior.
8. Official APIs and OS integrations are preferred over fragile UI automation.
9. Execution results must be verifiable.
10. All long-running or distributed tasks must have persistent state and recovery semantics.
