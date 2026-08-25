# AI OS — Security Model

## 1. Security Principles

AI OS is an agent system capable of controlling devices and external services. Security is therefore capability-based and enforced at every execution boundary.

Principles:

1. Least privilege.
2. Explicit capability grants.
3. User confirmation for sensitive operations.
4. Native OS and application authentication remains authoritative.
5. Agents cannot infer permission from natural-language intent alone.
6. Every sensitive operation is auditable.
7. Local and cloud credentials are isolated.

## 2. Trust Boundaries

```text
User
 |
 v
AI OS UI
 |
 +--> Local Runtime --> OS / Apps / Devices
 |
 +--> Cloud Runtime --> Server / Database / AI Providers
 |
 +--> External Services / APIs
```

Each boundary requires authenticated communication and explicit authorization.

## 3. Capability-Based Permissions

Every executable operation maps to a capability.

Examples:

```text
file.read
file.write
application.open
application.install
browser.navigate
email.send
bank.transfer
device.control
```

Capabilities have a risk level and execution scope.

## 4. Confirmation Policy

Examples of policy classes:

| Operation | Default policy |
|---|---|
| Open application | Allow |
| Read local file | Ask / policy dependent |
| Send email | Ask / policy dependent |
| Install application | Ask |
| Delete important data | Always ask |
| Financial transfer | Always ask |
| Purchase | Always ask |
| Change credentials | Always ask |

A policy may be stricter than the platform default.

## 5. Financial and Sensitive Actions

For a command such as:

```text
Transfer 100,000 Toman through the bank application.
```

AI OS may resolve the application, navigate the workflow and prepare the operation, but the final sensitive action must remain subject to user policy, application authentication and any required confirmation or native authorization.

AI OS must never bypass OTP, biometric authentication, PINs, transaction confirmation screens or other security controls.

## 6. Application Installation

Application installation must use official and platform-supported mechanisms whenever available.

The normal flow is:

```text
Application not found
        |
        v
Official Store Resolver
        |
        v
User Confirmation
        |
        v
Platform Installation
        |
        v
Verify Installed Application
```

AI OS must not silently download and execute untrusted packages as a fallback for normal application discovery.

## 7. Device Security

Each Node must have a unique device identity and authenticated session.

Required controls include:

- Device registration
- Device authentication
- Token rotation
- Secure credential storage
- Revocation
- Device status monitoring
- Audit events

## 8. Agent Security

Agents receive only the capabilities required for their current task or policy.

Dynamic Agents must have:

- Explicit tool list
- Capability scope
- Target node scope
- Permission policy
- Resource limits where applicable
- Persistent audit trail

## 9. Local Security

Local agents must use platform security mechanisms:

- Windows permissions and security boundaries
- macOS entitlements and permissions
- Android permissions and sandboxing
- iOS/iPadOS sandboxing and entitlements
- Linux user and process permissions

The agent must not attempt to bypass OS security boundaries.

## 10. Cloud Security

Server components must use:

- TLS
- Authenticated APIs
- Secure secret management
- Database access controls
- Rate limiting
- Input validation
- Audit logging
- Secure session handling
- Token rotation

## 11. Auditability

Sensitive actions must generate structured audit events containing at least:

```text
event_id
user_id
node_id
agent_id
task_id
capability
action
decision
timestamp
result
```

Secrets, passwords, tokens and private authentication material must not be written to ordinary logs.

## 12. Recovery

Long-running agents and tasks must have persistent state and recovery semantics so a process restart does not silently convert an unknown operation into a successful one.

Operations that are not safely retryable must use idempotency or explicit reconciliation before retry.
