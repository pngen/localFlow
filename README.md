# LocalFlow

A fully deterministic, Temporal-inspired local workflow engine with event sourcing and replay capabilities.

## Overview

LocalFlow is a distributed systems architecture designed for deterministic workflow execution. It provides a DSL for defining workflows, ensures complete event sourcing, supports timer scheduling, and enables safe activity execution with retries and cancellation.

## Architecture Diagram
```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│     CLI     │    │  Workflow    │    │  Timer       │
│             │    │  Engine      │    │  Scheduler   │
└──────┬──────┘    └──────┬───────┘    └──────┬───────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
               ┌──────────▼──────────┐
               │   Activity Runner   │
               └──────────┬──────────┘
                          │
               ┌──────────▼──────────┐
               │   State Persistence │
               └─────────────────────┘
```

## Core Components

1. **Workflow Engine** - Manages workflow lifecycle and state transitions
2. **DSL Parser** - Parses workflow definitions into executable steps
3. **Activity Runner** - Executes external activities with timeouts and retries
4. **Timer Scheduler** - Handles deterministic timer scheduling and firing
5. **State Persistence** - Stores workflows and events durably
6. **CLI Interface** - Command-line interface for workflow management

## Usage

Start a new workflow:
```bash
lf start PurchaseFlow
List all workflows:

lf list
Inspect a workflow:

lf inspect <workflow_id>
View workflow history:

lf history <workflow_id>
```

## Design Principles
- Deterministic: All execution paths are predictable and replayable
- Auditable: Complete event log for all state transitions
- Replayable: Workflows can be replayed exactly from any point
- Resilient: Built-in retry mechanisms and error handling
- Minimal: Focused on core workflow functionality only
- Composable: Modular components that can be extended independently

## Requirements
- Python 3.8+
- No external dependencies beyond standard library
- POSIX-compliant system for subprocess execution

## License

MIT License

## Author

Paul Ngen
