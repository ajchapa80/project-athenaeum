# Lab 21 — Controlled Live-Action Readiness Requirements and Design

## Problem

Project Athenaeum has progressed from alert normalization and triage through investigation, policy evaluation, approval handling, execution-safety design, and synthetic controlled-action orchestration.

Lab 20 demonstrated that Business Guardian can safely process a synthetic action lifecycle with fail-closed validation, duplicate-execution protection, independent verification, rollback handling, and strict resolution gating.

That still does not establish readiness to modify a real endpoint.

A live action introduces additional risks that synthetic execution cannot fully represent, including target misidentification, stale approval, environmental drift, unsupported endpoint state, adapter failure, verification loss, partial real-world modification, and rollback failure.

Lab 21 asks the next question:

**What must Business Guardian prove before a synthetic controlled action may advance to a narrowly scoped, human-approved defensive action against an authorized test endpoint?**

Lab 21 addresses that question through requirements, readiness design, failure analysis, and tabletop validation only.

No live defensive action is executed.

---

## Importance

Changing real endpoint state introduces a higher level of operational risk than collecting evidence or modifying synthetic state.

A safe defensive platform cannot rely solely on an earlier approval, a hostname, an IP address, a successful command return, or the assumption that an endpoint has remained unchanged since it was last evaluated.

Before a future live action can even become ready for testing, Business Guardian must establish that the intended target is authoritative and authorized, the approval remains valid, the requested operation is supported, relevant endpoint conditions still match expectations, independent verification is available, rollback is ready when required, and a human has the information needed to approve or stop the action.

The central Lab 21 safety principle is:

**Synthetic execution capability does not imply authorization to change a real endpoint.**

When a required live-action readiness condition cannot be proven, the system must fail closed or route the condition for human review.

---

## Design Goal

Lab 21 defines the safety contract that must be satisfied before Business Guardian may progress from synthetic controlled actions toward a future live action against an authorized lab endpoint.

The design must prove readiness across the following areas:

- target identity,
- target authorization,
- approval validity and freshness,
- approval binding,
- environmental and precondition revalidation,
- supported adapter capability,
- independent verification readiness,
- rollback readiness,
- duplicate-action protection,
- human approval,
- audit preservation,
- and fail-closed handling.

Lab 21 does not authorize or execute the future action.

---

## Where Lab 21 Fits

The Project Athenaeum progression now includes:

```text
Alert Processing
      ↓
Triage
      ↓
Investigation
      ↓
Policy / Approval
      ↓
Action Eligibility
      ↓
Execution Safety Contract
      ↓
Synthetic Controlled Action
      ↓
Independent Synthetic Verification
      ↓
Controlled Live-Action Readiness Design
      ↓
Future Authorized Live Test
```

Lab 21 is the design bridge between synthetic action control and any future live endpoint modification.

---

## Live-Action Readiness Model

Lab 21 introduces the conceptual:

**LAR — Live Action Readiness Record**

The LAR represents a readiness evaluation associated with an existing controlled action request.

Conceptually:

```text
AR → TR → PD → AP → AQR → LAR
```

A future live-action lab may later extend the chain through execution and verification records.

The LAR does not replace or rewrite upstream records.

Lab 21 defines three readiness outcomes:

```text
READY
NOT_READY
REQUIRES_HUMAN_REVIEW
```

### READY

All mandatory readiness conditions have been demonstrated.

`READY` does **not** authorize execution by itself.

### NOT_READY

One or more required safety conditions failed.

Execution must not proceed.

### REQUIRES_HUMAN_REVIEW

The system cannot safely determine readiness without additional investigation or operator judgment.

Human review does not automatically convert the result to `READY`.

---

## Target Identity and Authorization

Target identity and target authorization are separate requirements.

Correctly identifying an endpoint does not automatically mean Business Guardian is permitted to modify it.

A future live-action path must establish:

```text
TARGET IDENTITY CONFIRMED
            +
TARGET AUTHORIZATION CONFIRMED
```

before readiness may become `READY`.

The design must not rely solely on weak identifiers such as:

- a display name,
- a free-text nickname,
- an IP address by itself,
- or an unverified user-supplied hostname.

The future implementation must use authoritative endpoint information appropriate to the platform and environment.

Lab 21 intentionally does not expose or freeze a production target-authority mechanism.

---

## Approval Freshness and Binding

Approval that was valid earlier may no longer be valid when a live action is about to occur.

Lab 21 therefore requires approval freshness to be evaluated during live-action readiness.

The exact production freshness interval is intentionally not defined in this public design.

When approval is required, it must remain appropriately bound to the intended:

- action,
- target,
- request,
- scope,
- and authorized environment.

Approval for one action or endpoint must not silently authorize a materially different request.

Missing, stale, denied, pending, or mismatched approval prevents readiness.

---

## Pre-Execution Revalidation

Readiness cannot depend entirely on earlier observations.

A target may change after initial validation or approval.

Lab 21 therefore requires a future pre-execution revalidation checkpoint.

Conceptually:

```text
EXPECTED PRECONDITION
        ↓
CURRENT OBSERVATION
        ↓
      MATCH?
     /     \
   YES      NO
    ↓        ↓
continue   stop/review
```

Relevant state drift must either block readiness or require human review.

An earlier valid observation does not override newer contradictory evidence.

---

## Adapter Contract

A future live-action adapter must have a defined safety contract.

At minimum, the adapter contract must identify:

- supported controlled action,
- supported target or platform,
- required authorization,
- required preconditions,
- expected state change,
- known failure behavior,
- partial-change behavior,
- verification requirements,
- rollback capability,
- rollback limitations,
- timeout behavior,
- and sanitized audit outputs.

A live adapter must not accept arbitrary free-text commands as authorization to act.

The intended model is:

```text
CONTROLLED ACTION ID
        ↓
AUTHORIZED ADAPTER
        ↓
DEFINED OPERATION
```

not:

```text
FREE TEXT
   ↓
ARBITRARY SHELL COMMAND
```

---

## Independent Verification

Execution success is not proof that the intended endpoint state was achieved.

A future live verifier must independently observe endpoint state.

The action adapter cannot verify itself merely by returning success.

This is insufficient:

```text
Adapter:
"Execution succeeded"

Verifier:
"Adapter reported success"
```

The verifier must obtain independently meaningful evidence.

Lab 21 requires future verification to support:

- positive confirmation,
- negative confirmation,
- unavailable evidence,
- and conflicting or inconclusive evidence.

Only positive independent verification may support eventual resolution eligibility.

---

## Rollback Readiness

If a future action requires rollback capability, rollback readiness must be established before execution.

The future system must know:

- what rollback is expected to do,
- whether rollback is available,
- what prerequisites rollback requires,
- how rollback will be independently verified,
- and what happens if rollback fails.

A clean failure that produces no state change does not require unnecessary rollback.

Partial or adverse changes may require rollback according to the action contract.

The previously established invariant remains unchanged:

```text
ROLLBACK_VERIFIED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

Verified reversal does not prove that the original security condition was resolved.

---

## Human Approval Boundary

For the first future live endpoint action, explicit human approval is mandatory.

Even if Business Guardian eventually supports preauthorized low-risk activity, the first live-action milestone will not begin with autonomous remediation.

Before approval, the operator should be able to understand:

- what action will occur,
- what endpoint will change,
- why the action is being requested,
- what state is expected to change,
- how success will be independently verified,
- whether rollback is available,
- and what happens if verification fails.

A future approval interaction should conceptually resemble:

```text
Target: Authorized test endpoint
Action: Controlled low-risk action
Risk: Low
Reversible: Yes
Independent verification: Ready
Rollback: Ready
Approval: Current
Environment: Authorized isolated lab

Proceed?
[Approve] [Cancel]
```

Lab 21 defines this contract but does not build the user interface.

---

## Auditability

Readiness history must remain chronological and append-oriented.

A future LAR should preserve public-safe evidence concepts such as:

- readiness-record identity,
- action-request reference,
- target reference,
- action type,
- target-identity result,
- target-authorization result,
- approval status,
- approval-freshness result,
- precondition result,
- drift result,
- adapter-readiness result,
- verifier-readiness result,
- rollback-readiness result,
- human-control result,
- readiness outcome,
- reason information,
- and evaluation timestamp.

If readiness fails and is later reevaluated successfully, the later result must not erase the earlier failure.

For example:

```text
LAR-001 → NOT_READY
LAR-002 → READY
```

Both records must remain part of the history.

---

## Tabletop Validation

Lab 21 uses a frozen 24-case tabletop validation matrix.

The cases cover:

- fully ready conditions,
- ambiguous target identity,
- unauthorized targets,
- target mismatch,
- missing approval,
- denied approval,
- pending approval,
- stale approval,
- action-binding mismatch,
- target-binding mismatch,
- unsupported actions,
- unavailable adapters,
- incomplete adapter contracts,
- unavailable verification,
- non-independent verification,
- unavailable rollback,
- unavailable rollback verification,
- environment drift,
- failed preconditions,
- duplicate live-action requests,
- instruction-like input,
- non-reversible first actions,
- repeated readiness evaluation,
- and complete audit-history preservation.

The tabletop exercise validates the design contract only.

No live action is invoked.

---

## Validation Result

The frozen design validation result is:

```text
Tabletop cases:
24 / 24 PASSED

Live endpoint actions:
0

VMs accessed:
0

Production adapters created:
0

Real rollback actions:
0
```

Overall result:

**PASS — LIVE-ACTION READINESS CONTRACT VALIDATED BY DESIGN**

This result means the readiness requirements and failure-handling expectations produced the intended deterministic outcomes across the frozen tabletop scenarios.

It does not mean that live endpoint remediation has been validated.

---

## Safety Boundary

Lab 21 is design-only.

The lab does **not**:

- start or access a virtual machine,
- connect to a managed endpoint,
- modify an endpoint file,
- modify a user account,
- modify a firewall,
- modify a service,
- change network configuration,
- invoke Wazuh Active Response,
- execute PowerShell remediation,
- execute shell remediation,
- perform live rollback,
- create a production remediation adapter,
- target a production or customer system,
- authorize automatic retry,
- perform irreversible actions,
- allow generative AI to authorize execution,
- or allow generative AI to verify execution.

No live endpoint state is changed.

---

## Public / Private Boundary

The public Project Athenaeum lab documents:

- the live-action readiness concept,
- LAR record purpose,
- high-level readiness outcomes,
- target-identity and authorization requirements,
- approval-freshness requirements,
- pre-execution revalidation,
- adapter-contract requirements,
- verifier-independence requirements,
- rollback-readiness requirements,
- human-control requirements,
- the 24-case tabletop matrix,
- validation results,
- and safety boundaries.

The public lab intentionally excludes:

- production target-authority implementation,
- private approval-freshness thresholds,
- internal adapter capability registries,
- production verifier-source logic,
- private rollback-readiness logic,
- customer authorization rules,
- tenant scope,
- credential handling,
- production secrets,
- proprietary execution integrations,
- and future live-remediation implementation details.

No public Python implementation is created for this design-only lab.

---

## What This Proves

Lab 21 demonstrates that Project Athenaeum has defined the safety conditions required before Business Guardian may progress from synthetic action control toward a future authorized live endpoint test.

The design accounts for:

- authoritative target identity,
- separate target authorization,
- current and correctly bound approval,
- endpoint-state drift,
- pre-execution revalidation,
- controlled adapter capabilities,
- independent verification readiness,
- rollback readiness,
- duplicate-action protection,
- human approval,
- irreversible-action restrictions,
- and append-oriented audit preservation.

A result of `READY` means only that the prerequisites for a future controlled test have been demonstrated.

It does not authorize execution.

---

## What Comes Next

Lab 21 deliberately stops before a live endpoint action.

A future lab may validate one narrowly scoped action against one user-owned, authorized, isolated test endpoint under explicit human approval.

The first live action must remain:

- low-risk,
- reversible,
- narrowly scoped,
- independently observable,
- and harmless to normal lab operation.

The future test must also preserve:

- target revalidation immediately before execution,
- explicit human authorization,
- duplicate-execution protection,
- independent verification,
- rollback readiness,
- independent rollback verification,
- complete audit evidence,
- and fail-closed behavior.

No production system or customer environment will be used.
