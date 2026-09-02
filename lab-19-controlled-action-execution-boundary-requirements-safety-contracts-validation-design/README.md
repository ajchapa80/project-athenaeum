# Lab 19 — Controlled Action Execution Boundary: Requirements, Safety Contracts, and Validation Design

Lab 19 defines the safety contract that must exist between an eligible security response and any future action execution. It deliberately stops before implementation.

## The Question

> What must be proven before an eligible, approved security response may execute, and what evidence is required before any condition may be marked resolved?

Labs 15–18 already established traceable alert records, deterministic triage, policy and approval boundaries, live evidence collection, and conservative investigation routing. Lab 19 preserves those validated baselines and designs the missing boundary after `READY_FOR_ACTION`.

## Why Design Before Execution?

`READY_FOR_ACTION` means that a response is eligible for further validation. It is not an instruction to execute.

Lab 19 conceptually consumes the existing Lab 17 `READY_FOR_ACTION` boundary. It does not implement a consumer, executor, or action adapter.

Without a frozen execution contract, a system could incorrectly treat approval as permanent, target the wrong asset, execute a duplicate request, confuse command submission with success, or mark a condition resolved without independent verification.

Lab 19 prevents those unsafe assumptions from becoming implementation behavior.

## Vendor-Neutral Execution Boundary

```text
READY_FOR_ACTION
        ↓
Validated Action Request
        ↓
Authorization and Approval-Freshness Validation
        ↓
Target Validation
        ↓
Duplicate and Idempotency Protection
        ↓
Controlled Execution
        ↓
Independent Verification
        ↓
Rollback When Required
        ↓
Rollback Verification
        ↓
Verified Outcome
        ↓
Resolution Eligibility
```

Every transition is conditional. Missing, stale, mismatched, denied, unsupported, ambiguous, or unverifiable information fails closed.

## Frozen Architectural Rules

- `READY_FOR_ACTION` is eligibility only.
- The executor does not decide authorization.
- Approval must be present, affirmative, current, and bound to the intended action and target.
- The target must be explicit and validated before execution.
- Unsupported actions fail closed.
- Duplicate requests must not produce duplicate execution.
- Command submission is not execution success.
- Execution success is not verification success.
- Verification should be independent of the executor response wherever technically practical.
- Failed, unavailable, or inconclusive verification prohibits resolution.
- Reversible actions require a defined rollback contract.
- Rollback completion must be independently verified.
- No condition becomes resolved solely because an action returned success.

## Record Responsibilities

Lab 19 defines public-safe responsibilities rather than proprietary product schemas:

- **Action Request Record (AQR):** binds the proposed action to the existing alert, triage, policy, and approval chain; identifies the intended target, requested action, approval context, expiry, and verification and rollback expectations.
- **Execution Record (EXR):** records executor receipt, validation result, idempotency decision, attempt identity, timestamps, and execution status without deciding authorization.
- **Verification Record (VR):** records the independent observation used to determine whether the intended post-action condition exists.
- **Rollback Record (RBR):** records why rollback was required, the rollback attempt, and the independently observed restoration result.
- **Outcome/Audit Record (OAR):** preserves the complete chronological execution history and determines resolution eligibility from verified evidence rather than command success. It may not overwrite or hide earlier requests, attempts, failures, verification results, rollback activity, or prior decisions.

These records preserve the existing identities:

```text
AR → TR → PD → AP → AQR → EXR → VR → optional RBR → OAR
```

No future record replaces or rewrites a prior decision record.

## State Design

The design separates eligibility, execution, verification, rollback, and resolution:

```text
READY_FOR_ACTION
  → EXECUTION_VALIDATION_PENDING
  → EXECUTING
  → EXECUTION_FAILED
     or EXECUTION_COMPLETED_UNVERIFIED
          → VERIFICATION_SUCCEEDED
             → RESOLUTION_ELIGIBLE
          → VERIFICATION_FAILED
             → ROLLBACK_REQUIRED or NOT_RESOLUTION_ELIGIBLE
          → VERIFICATION_INCONCLUSIVE
             → NOT_RESOLUTION_ELIGIBLE

ROLLBACK_REQUIRED
  → ROLLBACK_EXECUTING
  → ROLLBACK_VERIFIED
     → NOT_RESOLUTION_ELIGIBLE
     → reassessment or human review as appropriate
     or ROLLBACK_FAILED
```

Only positive independent verification can permit `RESOLUTION_ELIGIBLE`. Eligibility still does not itself mark a condition resolved.

Successful rollback proves that the attempted change was reversed. It does not prove that the original security condition was resolved. Separate evidence would be required to establish that the underlying condition no longer exists.

The OAR must show events in chronological order. For example, an execution failure followed by verified rollback remains an execution failure followed by rollback; it cannot collapse into a generic successful or completed outcome.

## Tabletop Validation

The design was reviewed against cases covering:

- valid, missing, stale, denied, and mismatched approval;
- wrong-action and wrong-target approval;
- ambiguous or nonexistent targets;
- unsupported actions;
- duplicate requests and repeated attempts;
- execution success, failure, and partial execution;
- verification success, failure, and unavailability;
- rollback requirements, success, verification failure, and failure;
- attempted resolution without positive verification.

Unsafe transitions consistently terminate in a blocked, failed, rollback-required, or not-resolution-eligible state.

## Design Validation Result

**PASS — DESIGN CONTRACT ONLY**

The frozen contracts consistently prevent unsafe transitions across the defined tabletop cases.

This PASS explicitly means:

- no action was executed;
- no endpoint was modified;
- no remediation occurred;
- no live executor or action adapter was created;
- no condition was marked resolved.

It does not validate action execution or production readiness.

## Public / Private Boundary

Public Project Athenaeum material may describe vendor-neutral architecture, record responsibilities, state transitions, fail-closed behavior, acceptance cases, and sanitized validation results.

Private Business Guardian material remains private, including execution source code, action adapters, proprietary action selection, production policy catalogs, customer permissions, credentials, rollback and verification implementations, and commercial orchestration logic.

## What Lab 19 Proves

Lab 19 proves that the execution boundary can be specified before implementation and evaluated against adverse conditions without changing an endpoint.

The lab establishes a measurable contract for future development:

> An action may execute only after its request, approval, target, support status, and duplicate protections pass. A condition may approach resolution only after independently verified evidence supports the intended outcome.

## Scope Boundary

Lab 19 created documentation only. It did not:

- start any virtual machine;
- execute a command against an endpoint;
- implement an execution subsystem;
- build an action adapter;
- modify Business Guardian;
- perform remediation;
- mark any condition resolved;
- begin Lab 20.

The validated Project Athenaeum baseline through Lab 18 remains preserved.
