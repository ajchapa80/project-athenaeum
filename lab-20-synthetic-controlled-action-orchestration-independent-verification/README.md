# Lab 20 — Synthetic Controlled Action Orchestration and Independent Verification

## Problem

Project Athenaeum had already established a progression from alert normalization and triage through investigation, policy evaluation, approval handling, and action eligibility.

Lab 19 then defined the safety contract required before an eligible defensive response could ever execute. It established an important distinction:

**Being eligible for action is not the same as executing an action, and successful execution is not the same as verified resolution.**

Lab 20 asks the next question:

**Can Business Guardian orchestrate a controlled defensive-action lifecycle while preventing invalid, unauthorized, duplicate, unsupported, failed, or unverified actions from being treated as successful resolution?**

Lab 20 tests that boundary using synthetic, in-memory state only.

No real endpoint remediation was performed.

---

## Importance

Automated security response introduces significantly greater risk than read-only investigation.

A defensive platform cannot safely assume that an action request is valid simply because it exists. It must establish that the action is eligible, appropriately authorized, bound to the correct target, supported by the execution layer, protected against duplicate delivery, and independently verifiable.

Execution also cannot be treated as proof of resolution. An action may fail, partially modify state, return success without producing the intended result, or require rollback.

Business Guardian is therefore being designed around a fail-closed principle:

**When the system cannot prove that the required safety conditions have been satisfied, execution or resolution must not proceed.**

Lab 20 validates this principle before any live endpoint remediation is introduced.

---

## What Was Implemented

The private Business Guardian implementation added a synthetic controlled-action subsystem capable of:

- consuming trusted action-eligibility information,
- validating controlled action requests,
- enforcing approval requirements,
- validating target identity and authorization,
- rejecting unsupported actions,
- preventing duplicate execution,
- executing an allowlisted synthetic action,
- independently verifying resulting state,
- distinguishing clean execution failure from partial execution,
- initiating rollback when required,
- independently verifying rollback,
- preserving chronological audit history,
- and determining whether an outcome may become resolution-eligible.

The implementation remains vendor-neutral and operates entirely against injected synthetic/in-memory state.

It is **not a production remediation engine**.

---

## Controlled Action Lifecycle

The validated high-level lifecycle is:

```text
Trusted Action Eligibility
          ↓
Action Request Validation
          ↓
Authorization / Target Validation
          ↓
Duplicate-Execution Protection
          ↓
Synthetic Execution
          ↓
Independent Verification
          ↓
Rollback When Required
          ↓
Independent Rollback Verification
          ↓
Outcome Evaluation
          ↓
Resolution Eligibility
          ↓
Audit History
```

The execution component does not verify its own result.

Verification is performed through a separate controlled component that independently examines synthetic state.

---

## Core Safety Rules

Lab 20 validated the following safety rules:

- `READY_FOR_ACTION` represents eligibility for controlled processing, not execution.
- Missing approval never means approval.
- Required authorization must be valid and appropriately bound to the request.
- Invalid, ambiguous, nonexistent, or unauthorized targets fail closed.
- Unsupported actions fail closed.
- Duplicate delivery cannot create duplicate execution.
- Execution completion does not prove that the intended result occurred.
- The execution component cannot verify its own result.
- Independent positive verification is required before resolution eligibility.
- Failed, unavailable, conflicting, or inconclusive verification prevents resolution eligibility.
- Clean execution failure before state change does not require unnecessary rollback.
- Partial or adverse execution may require rollback.
- Rollback must itself be independently verified.
- Verified rollback does not resolve the original security condition.
- Failed and partial attempts remain part of the audit history.
- Instruction-like free text remains inert data and cannot select or authorize an action.

---

## Resolution Rule

A security condition may become:

`RESOLUTION_ELIGIBLE`

only when a valid and authorized action completes successfully **and** independent verification positively confirms the expected resulting state.

```text
VALID + AUTHORIZED
        ↓
EXECUTION SUCCEEDED
        ↓
INDEPENDENT VERIFICATION SUCCEEDED
        ↓
RESOLUTION_ELIGIBLE
```

Execution success by itself is insufficient.

Verification failure, unavailability, or conflicting evidence prevents resolution eligibility.

A verified rollback also does not establish resolution:

```text
ROLLBACK_VERIFIED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

Rollback proves that a change was reversed. It does not prove that the original security condition was corrected.

---

## Validation

Lab 20 used a frozen 22-case validation matrix covering:

- preauthorized success,
- explicitly approved success,
- pending approval,
- denied approval,
- missing or stale approval,
- authorization-binding mismatch,
- invalid workflow eligibility,
- unsupported actions,
- invalid and ambiguous targets,
- altered provenance relationships,
- duplicate delivery,
- clean execution failure,
- partial execution,
- verification failure,
- verification unavailability,
- successful verified rollback,
- rollback failure,
- rollback-verification failure,
- conflicting verification,
- instruction-like input,
- repeatability with new identities,
- and complete chronological audit preservation.

**Result: 22/22 validation cases passed.**

Blocked validation paths were also confirmed to produce zero execution, verification, and rollback calls where those components were not supposed to run.

See `Lab20_22_Case_Validation_Matrix_v1.0.txt` for the complete public-safe matrix.

---

## Test Results

The validated private implementation produced:

```text
Lab 20-specific tests:
29 / 29 PASSED

Frozen validation cases:
22 / 22 PASSED

Full Business Guardian regression suite:
293 / 293 PASSED

Python compilation validation:
PASSED

Git whitespace/error validation:
PASSED
```

The 293-test regression result represents the validated Lab 20 milestone. It is not intended to define a permanent Business Guardian test count.

The full regression pass confirmed that introducing the controlled-action subsystem did not break the previously validated investigation and evidence-processing baseline.

---

## Representative Outcomes

### Successful Synthetic Action

```text
READY_FOR_ACTION
        ↓
EXECUTION_VALIDATION_PENDING
        ↓
EXECUTING
        ↓
EXECUTION_COMPLETED_UNVERIFIED
        ↓
VERIFICATION_SUCCEEDED
        ↓
RESOLUTION_ELIGIBLE
```

The action becomes resolution-eligible only after independent positive verification.

### Clean Execution Failure

```text
EXECUTING
    ↓
EXECUTION_FAILED
    ↓
NOT_RESOLUTION_ELIGIBLE
```

When positive evidence establishes that execution failed before any synthetic state change occurred, rollback is unnecessary.

### Partial Execution

```text
EXECUTING
    ↓
EXECUTION_FAILED
    ↓
ROLLBACK_REQUIRED
    ↓
ROLLBACK_EXECUTING
    ↓
ROLLBACK_VERIFIED
    ↓
NOT_RESOLUTION_ELIGIBLE
```

Verified rollback proves reversal of the synthetic change. The original security condition still requires reassessment.

### Verification Failure

```text
EXECUTION_COMPLETED_UNVERIFIED
        ↓
VERIFICATION_FAILED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

An execution component reporting success cannot establish resolution on its own.

---

## Duplicate Execution Protection

Lab 20 validated protection against duplicate action delivery.

When the same controlled request is delivered more than once, Business Guardian preserves the original execution attempt and rejects the duplicate without invoking the action component a second time.

This prevents a retransmitted request from silently becoming a second defensive action.

---

## Auditability

The controlled-action layer preserves append-oriented audit history across the action lifecycle.

Public-safe audit concepts include:

- action-request identity,
- execution-attempt identity,
- verification evidence,
- rollback activity when required,
- state transitions,
- controlled reason information,
- timestamps,
- and final resolution-eligibility outcome.

Later success does not erase earlier failure.

Rollback does not erase the execution attempt that required it.

Duplicate delivery does not replace the original attempt.

This creates a traceable history of what the system considered, attempted, verified, reversed, and ultimately allowed or refused.

---

## Evidence

The public Lab 20 evidence set contains sanitized representative records rather than proprietary implementation artifacts.

### Successful Controlled Action

[`sanitized-successful-action-audit.json`](evidence/sanitized-successful-action-audit.json)

Demonstrates successful synthetic execution followed by independent positive verification before resolution eligibility.

### Clean Execution Failure

[`sanitized-clean-failure-audit.json`](evidence/sanitized-clean-failure-audit.json)

Demonstrates a failure before state change and confirms that unnecessary rollback is not invoked.

### Partial Execution and Rollback

[`sanitized-rollback-audit.json`](evidence/sanitized-rollback-audit.json)

Demonstrates partial synthetic execution, rollback, independent rollback verification, and the final `NOT_RESOLUTION_ELIGIBLE` state.

### Duplicate Delivery

[`sanitized-duplicate-delivery-audit.json`](evidence/sanitized-duplicate-delivery-audit.json)

Demonstrates that two deliveries of the same controlled request result in only one execution attempt.

These records use demonstration identities and sanitized synthetic values. They are not production or customer records.

### Duplicate Delivery

`evidence/sanitized-duplicate-delivery-audit.json`

Demonstrates that two deliveries of the same controlled request result in only one execution attempt.

These records use demonstration identities and sanitized synthetic values. They are not production or customer records.

---

## Safety Boundary

Lab 20 was intentionally restricted to synthetic and in-memory behavior.

The lab did **not**:

- start or access a virtual machine,
- modify a Windows or Linux endpoint,
- modify an endpoint file,
- disable or modify an account,
- modify a firewall,
- modify a service,
- modify network controls,
- invoke Wazuh Active Response,
- execute remediation through PowerShell,
- execute remediation through a shell,
- perform live rollback,
- target a production or customer system,
- allow generative AI to authorize an action,
- or allow generative AI to verify an action.

All action execution, verification, and rollback behavior remained synthetic.

---

## Public / Private Boundary

The validated controlled-action implementation remains in the private Business Guardian repository.

This public lab documents:

- high-level architecture,
- safety contracts,
- controlled workflow states,
- validation methodology,
- deterministic validation results,
- sanitized representative evidence,
- and testing outcomes.

It intentionally excludes:

- private orchestration source code,
- proprietary validation implementation,
- internal action adapters,
- internal verification implementation,
- private attempt-ledger behavior,
- exact internal validation sequencing,
- production action-adapter design,
- future live-remediation logic,
- customer policy logic,
- tenant authorization,
- credentials,
- and sensitive configuration.

No duplicate public implementation was created solely for portfolio purposes.

---

## What This Proves

Lab 20 demonstrates that Business Guardian can enforce a controlled defensive-action lifecycle without assuming that execution equals success.

The validated private subsystem can:

- reject invalid actions before execution,
- enforce authorization boundaries,
- reject invalid targets,
- prevent duplicate execution,
- preserve provenance relationships,
- distinguish clean failure from partial execution,
- require independent verification,
- initiate rollback when appropriate,
- verify rollback separately,
- preserve chronological audit history,
- and refuse resolution eligibility without positive verification.

This moves Business Guardian beyond a purely read-only investigation architecture while preserving a strict synthetic safety boundary.

---

## What Comes Next

Lab 20 deliberately stops before live endpoint remediation.

Future work must establish additional controls before Business Guardian progresses from synthetic controlled actions toward carefully scoped defensive action against an authorized test endpoint.

Those controls include:

- authoritative target validation,
- production adapter contracts,
- verifier-independence guarantees,
- approval-freshness policy,
- controlled retry authorization,
- non-reversible action handling,
- live rollback procedures,
- and additional human-approval safeguards.

No endpoint condition will be considered resolved solely because an execution component reports success.
