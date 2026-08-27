# Lab 17 — Policy Evaluation and Approval Logic

## Understanding a Security Problem Does Not Automatically Authorize a Response

Lab 16 gave Project Athenaeum the ability to classify a security condition and decide where it should go next.

That created the next question:

**If a response is recommended, is the system actually allowed to do it?**

Lab 17 introduces the authorization boundary.

It adds a deterministic policy-evaluation and approval-control layer after triage and before any future defensive execution.

The workflow now becomes:

```text
Alert Record (AR)
      ↓
Triage Decision (TR)
      ↓
Policy Evaluation
      ↓
Policy Decision (PD)
      ↓
Optional Approval Record (AP)
      ↓
Final Workflow State
```

The important distinction is simple:

> **Detection is not authorization. Triage is not authorization. Severity is not authorization. A recommendation is not authorization.**

Lab 17 decides whether a proposed response is permitted by policy and whether explicit human approval is required.

It does **not** execute the response.

---

# What Lab 17 Adds

The Lab 17 processor consumes sanitized Lab 16-style triage records and extends their history without replacing anything that came before.

It:

- Preserves the original `AR-...` Alert Record identity
- Preserves the original `TR-...` Triage Decision identity
- Creates a separate `PD-...` Policy Decision identity
- Creates an `AP-...` Approval Record only when approval is required
- Maintains complete `AR → TR → PD → AP` traceability
- Evaluates actions with deterministic policy rules
- Separates action risk from technical alert severity
- Supports explicit human approval states
- Fails closed when an action is unsupported
- Prevents unresolved investigation cases from entering an action workflow
- Produces structured JSON decision records
- Preserves chronological audit history
- Produces a human-readable batch summary
- Protects previous output from overwrite
- Executes no defensive action

This adds another distinct decision layer without rebuilding the alert-record or triage foundations from Labs 15 and 16.

**Nothing gets built twice.**

---

# The New Authorization Boundary

Before Lab 17, the public workflow could answer:

```text
What happened?
        ↓
How should it be classified?
        ↓
Where should it go next?
```

Lab 17 adds:

```text
Is the proposed response permitted?
        ↓
Does it require approval?
        ↓
What workflow state should follow?
```

That boundary matters because a system may understand a security condition perfectly and still have **no authority to act on it**.

---

# Four Final Workflow States

Lab 17 produces one of four public-safe workflow states:

```text
READY_FOR_ACTION
AWAITING_APPROVAL
INVESTIGATION
NO_ACTION_AUTHORIZED
```

## `READY_FOR_ACTION`

Policy requirements have been satisfied and the proposed response is eligible for a later action layer.

This does **not** mean the action was executed.

## `AWAITING_APPROVAL`

The proposed response requires explicit human approval and has not yet received it.

## `INVESTIGATION`

The security condition still requires investigation.

A requested action cannot bypass that state.

## `NO_ACTION_AUTHORIZED`

Policy does not permit the proposed action.

This can result from:

- Explicit denial
- A prohibited action
- An unsupported action
- A fail-closed fallback

---

# A Small Public Demonstration Policy

Lab 17 intentionally uses a limited sanitized action catalog.

It demonstrates policy behavior without exposing the production Business Guardian policy system.

## Low Risk — Pre-Authorized

```text
ADD_MONITORING_NOTE
Risk: LOW
Policy: PRE_AUTHORIZED
```

This can proceed to:

```text
READY_FOR_ACTION
```

No human approval record is required.

---

## Medium Risk — Approval Required

```text
TEMPORARY_BLOCK_SOURCE
Risk: MEDIUM
Policy: REQUIRES_APPROVAL
```

Its result depends on approval state:

```text
PENDING
   ↓
AWAITING_APPROVAL

APPROVED
   ↓
READY_FOR_ACTION

DENIED
   ↓
NO_ACTION_AUTHORIZED
```

---

## High Risk — Not Authorized

```text
DISABLE_USER_ACCOUNT
Risk: HIGH
Policy: NOT_AUTHORIZED
```

The public demonstration policy does not permit this action.

Result:

```text
NO_ACTION_AUTHORIZED
```

Any unrecognized action also fails closed as:

```text
NOT_AUTHORIZED
```

These are sanitized demonstration policies only.

They do not represent the production Business Guardian action or policy catalog.

---

# Missing Approval Never Means Approved

Approval-required actions use three explicit states:

```text
PENDING
APPROVED
DENIED
```

There is no implicit approval.

If approval is missing, the system defaults to:

```text
PENDING
```

not:

```text
APPROVED
```

That means an approval-required action cannot become `READY_FOR_ACTION` unless an explicit `APPROVED` state exists.

This is one of the most important safety controls in the lab.

---

# Investigation Cannot Be Bypassed

A proposed response does not automatically become eligible simply because the action itself exists in the policy catalog.

If the Lab 16 triage decision says the condition belongs in:

```text
INVESTIGATION
```

Lab 17 keeps it there.

Conceptually:

```text
Unresolved Investigation
        +
Requested Action
        ↓
Still INVESTIGATION
```

The request cannot pull an unresolved security condition into an action workflow prematurely.

---

# Policy Evaluation Order

The public policy rules are evaluated in a controlled priority order.

Conceptually:

```text
INVESTIGATION
    ↓
Remain in INVESTIGATION

Unsupported Action
    ↓
NOT_AUTHORIZED
    ↓
NO_ACTION_AUTHORIZED

Prohibited Action
    ↓
NOT_AUTHORIZED
    ↓
NO_ACTION_AUTHORIZED

Pre-Authorized Low-Risk Action
    ↓
READY_FOR_ACTION

Approval-Required Action
    ├── PENDING
    │      ↓
    │  AWAITING_APPROVAL
    │
    ├── APPROVED
    │      ↓
    │  READY_FOR_ACTION
    │
    └── DENIED
           ↓
       NO_ACTION_AUTHORIZED

No Safe Rule Match
    ↓
FAIL CLOSED
    ↓
NO_ACTION_AUTHORIZED
```

The fallback behavior is deliberately conservative.

If a safe authorization rule cannot be established, the system does not invent permission.

---

# Identity and Traceability Continue Forward

Lab 15 introduced persistent Alert Record identities:

```text
AR-...
```

Lab 16 added separate Triage Decision identities:

```text
TR-...
```

Lab 17 now adds:

```text
PD-...  Policy Decision
AP-...  Approval Record
```

The complete relationship can become:

```text
AR-...
  ↓
TR-...
  ↓
PD-...
  ↓
AP-...
```

An Approval Record is only created when approval is actually part of the policy path.

This keeps the original alert, the triage decision, the policy decision, and the approval decision as separate records.

That matters because:

> **The evidence, the classification, the policy decision, and the human approval are four different things.**

---

# Controlled Validation

Seven sanitized policy inputs were created before implementation.

They test:

1. Pre-authorized low-risk action
2. Approval required — pending
3. Approval required — approved
4. Approval required — denied
5. Investigation-lane protection
6. Prohibited high-risk action
7. Unsupported action

Expected results were frozen before coding began.

---

# Frozen Expected Result

```text
Policy inputs discovered: 7

AUTHORIZED: 1
REQUIRES_APPROVAL: 3
DEFERRED_TO_INVESTIGATION: 1
NOT_AUTHORIZED: 2

Approval records created: 3

PENDING: 1
APPROVED: 1
DENIED: 1

READY_FOR_ACTION: 2
AWAITING_APPROVAL: 1
INVESTIGATION: 1
NO_ACTION_AUTHORIZED: 3

Policy Decision records created: 7
Failed: 0
```

---

# First Controlled Run

The first complete execution produced the exact frozen result.

```text
7 policy inputs
1 AUTHORIZED
3 REQUIRES_APPROVAL
1 DEFERRED_TO_INVESTIGATION
2 NOT_AUTHORIZED

3 approval records

1 PENDING
1 APPROVED
1 DENIED

2 READY_FOR_ACTION
1 AWAITING_APPROVAL
1 INVESTIGATION
3 NO_ACTION_AUTHORIZED

7 Policy Decision records
0 failures
```

**Expected vs. observed: Exact match — PASS**

---

# Repeat-Processing Validation

A second complete execution reproduced the same policy, approval, and workflow results.

After both runs, the local validated output contained:

```text
14 Policy Decision JSON records
 6 Approval JSON records
 2 batch summaries
------------------------------
22 total files
```

Repeat processing confirmed that:

- Original `AR-...` identities remained unchanged
- Original `TR-...` identities remained unchanged
- Each execution created new `PD-...` identities
- Approval-required cases created new `AP-...` identities
- First-run output remained intact
- First-run batch summary remained intact
- No output was overwritten
- Both runs produced identical decision totals

**Repeat-processing validation: PASS**

---

# Safety Validation

Lab 17 deliberately stops before remediation.

Validation confirmed that:

- No defensive action was executed
- No PowerShell remediation command was generated or run
- No firewall rule was changed
- No account was disabled
- No service was modified
- No endpoint was isolated
- No file was quarantined
- Investigation state could not be bypassed
- Unsupported actions could not become `READY_FOR_ACTION`
- Prohibited actions could not become `READY_FOR_ACTION`
- Approval-required actions required explicit `APPROVED`
- Missing approval never became approval
- HIGH severity did not grant authorization
- LOW severity did not imply safety
- AI output did not grant authorization
- Alert or log content was never converted into executable instruction
- Policy evaluation did not mark a condition resolved

Most importantly:

```text
Lab 17 evaluated policy and approval state only.
No defensive action was executed.
```

---

# `READY_FOR_ACTION` Does Not Mean Executed

This distinction is critical.

```text
READY_FOR_ACTION
```

means:

> The policy and approval requirements demonstrated in this lab have been satisfied and a future controlled-action layer may evaluate the action for execution.

It does **not** mean:

- The firewall was changed
- An account was disabled
- A process was terminated
- A file was quarantined
- An endpoint was isolated
- Remediation occurred
- The incident was resolved

Lab 17 establishes eligibility.

Execution belongs to a later layer.

---

# Validation Status

| Validation Area | Result |
| --- | --- |
| Technical implementation | **COMPLETE** |
| Controlled validation | **PASS** |
| Repeat-processing validation | **PASS** |
| Policy inputs processed | 7 |
| Policy Decision records created | 7 |
| Approval Records created | 3 |
| Failures | 0 |
| Investigation-gate protection | **PASS** |
| Explicit approval requirement | **PASS** |
| Fail-closed behavior | **PASS** |
| AR / TR identity preservation | **PASS** |
| PD / AP traceability | **PASS** |
| Output overwrite protection | **PASS** |
| Defensive actions executed | **0** |

---

# What Lab 17 Proves

Lab 17 demonstrates that understanding a security condition and recommending a response are not enough to authorize that response.

The lab successfully shows that:

- Policy decisions can have their own identities
- Human approvals can have separate identities
- Alert and triage history can remain preserved
- Low-risk actions can be represented as pre-authorized
- Higher-risk actions can require explicit approval
- Denied approval can prevent action eligibility
- Missing approval cannot silently become approval
- Prohibited actions remain unauthorized
- Unsupported actions fail closed
- Investigation cannot be bypassed
- Technical severity cannot grant authority
- AI output cannot grant authority
- Repeat execution can preserve previous decisions
- Authorization can be evaluated without performing remediation

The most important principle is:

> **A security system should know not only what it wants to do, but whether it is allowed to do it.**

---

# Public / Private Boundary

Project Athenaeum publishes the sanitized architecture and controlled validation evidence.

Public Lab 17 may demonstrate:

- Vendor-neutral policy architecture
- Sanitized deterministic policy rules
- Public-safe action-risk categories
- Approval-state handling
- `PD-...` Policy Decision records
- `AP-...` Approval Records
- `AR → TR → PD → AP` traceability
- Fail-closed behavior
- Repeat-processing protection
- Public-safe audit history
- Controlled validation results

The private Business Guardian repository retains product-level implementation including:

- Production customer policy catalogs
- Customer and tenant permissions
- Proprietary business-risk scoring
- Production action-selection logic
- Production approval workflows
- Identity-provider integrations
- Privileged credentials
- Real defensive-action adapters
- Remediation implementation
- Rollback logic
- Production verification logic
- Proprietary orchestration
- Customer security configuration
- Commercial product behavior

The public lab demonstrates the security-control architecture without exposing the production policy engine.

---

# Skills Demonstrated

- Python
- JSON processing
- Deterministic policy evaluation
- Authorization-boundary design
- Human approval workflows
- Action-risk classification
- Fail-closed security design
- Security workflow state management
- Record identity design
- `AR → TR → PD → AP` traceability
- Approval-state validation
- Investigation-gate enforcement
- Batch processing
- Audit-oriented history
- Repeat-processing validation
- Output overwrite protection
- Defensive programming
- Security architecture
- Technical documentation

---

# Where the Project Goes From Here

Lab 15 answered:

**How do I preserve a security alert as a durable, traceable record?**

Lab 16 answered:

**What kind of condition is it, and where should it go next?**

Lab 17 answers:

**If a response is proposed, is the system actually authorized to do it?**

The progression is now:

```text
Alert
  ↓
Normalize / Validate
  ↓
Alert Record
  ↓
Triage
  ↓
Policy Evaluation
  ↓
Approval When Required
  ↓
READY_FOR_ACTION
```

And then Lab 17 stops.

The next major technical boundary is intentionally separate:

```text
READY_FOR_ACTION
       ↓
Future Controlled Execution
       ↓
Verification
       ↓
Audit / Outcome
```

Lab 17 does not cross that boundary.

It establishes the control that must exist **before** defensive execution becomes possible.
