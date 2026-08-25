# AI OS — Protocols

This document defines the logical contracts between AI OS components. Concrete wire formats may evolve, but these entities and boundaries must remain explicit.

## 1. Device Contract

A Device/Node must expose:

```text
node_id
node_type
platform
version
status
capabilities
agent_id
last_seen
```

Node types include desktop, mobile, browser, TV, IoT and cloud service.

## 2. Application Contract

```text
application_id
node_id
package_id
name
version
install_state
launch_info
capabilities
store_metadata
```

The Application Resolver must use verified registry information rather than guessing package identifiers.

## 3. Agent Contract

```text
agent_id
agent_type
node_id
status
capabilities
tools
permissions
state
```

Agent types include local, server, dynamic, browser and device agents.

## 4. Task Contract

```text
task_id
parent_task_id
request
intent
target_nodes
selected_agents
required_capabilities
state
priority
created_at
updated_at
result
error
```

Task states:

```text
created
planned
waiting_permission
queued
running
waiting_external
completed
failed
cancelled
```

## 5. Capability Contract

Capabilities are normalized identifiers with platform-specific implementations.

Examples:

```text
application.open
application.install
file.read
file.write
process.start
browser.navigate
browser.click
email.read
email.send
tv.power_on
tv.set_channel
iot.device_control
bank.transfer
```

A capability must declare its permission sensitivity.

## 6. Tool Contract

Tools expose executable operations to agents.

```text
tool_id
name
input_schema
output_schema
required_capabilities
risk_level
execution_scope
```

Tools must validate input and return structured results.

## 7. Permission Contract

Permission decisions must be explicit.

```text
permission_id
subject
capability
scope
policy
decision
confirmation_required
expires_at
```

Possible policy decisions:

```text
allow
deny
ask
allow_once
allow_with_conditions
```

## 8. Event Contract

Events are used for device changes, application changes, schedules and agent triggers.

```text
event_id
type
source
node_id
payload
timestamp
correlation_id
```

Examples:

```text
node.connected
node.disconnected
application.installed
application.uninstalled
file.created
email.received
schedule.triggered
task.completed
permission.requested
```

## 9. Task Execution Protocol

```text
Client / User
    |
    v
Create Task
    |
    v
Server or Local Router
    |
    v
Resolve Node
    |
    v
Resolve Application / Capability
    |
    v
Permission Decision
    |
    v
Select Agent + Tool
    |
    v
Execute
    |
    v
Return Structured Result
    |
    v
Verify / Complete
```

## 10. Local / Cloud Synchronization

The Local Runtime must be able to queue eligible work while offline.

When connectivity returns:

```text
Local State
   |
   v
Sync Queue
   |
   v
Server
   |
   v
Reconciliation
```

Tasks must use stable identifiers and idempotency rules where retries can repeat an operation.

## 11. Dynamic Agent Contract

A persistent Dynamic Agent contains:

```text
agent_definition
triggers
conditions
target_nodes
tools
capabilities
llm_policy
permission_policy
notification_policy
state
schedule
```

Dynamic Agents must be recoverable after process or server restart.
