# Lab 16 — Alert Triage and Decision Logic

## Overview

Lab 16 adds a deterministic, vendor-neutral triage and decision-routing layer to the Project Athenaeum alert-processing workflow.

It builds directly from the validated Lab 15 alert-record baseline.

Public workflow demonstrated:

```text
Validated Alert Record
        ↓
Triage Classification
        ↓
Next-Stage Routing
```

This lab intentionally stops at decision routing.

It does **not** authorize remediation, execute defensive actions, verify fixes, or mark alerts resolved.

## Objectives

- Consume sanitized Lab 15-style JSON alert records.
- Preserve existing `AR-...` alert-record identity.
- Create a separate `TR-...` triage-decision identity.
- Preserve validation status, normalized severity, missing fields, and validation notes.
- Apply deterministic vendor-neutral triage rules.
- Keep technical severity separate from triage classification.
- Give evidence-quality problems priority over recognizable patterns.
- Preserve uncertainty instead of guessing.
- Record chronological triage history.
- Route alerts toward the appropriate next processing stage.
- Generate structured JSON triage-decision records.
- Generate an auditable batch summary.
- Preserve previous output through unique filenames.
- Perform no defensive action.

## Triage Classifications

Lab 16 uses four public-safe triage classifications:

### `KNOWN_COMMON`

A documented deterministic condition was recognized using the available evidence.

This classification does **not** mean:

- Benign
- Resolved
- Safe
- Automatically approved for remediation

It only means the alert matched a supported known condition strongly enough to continue to policy evaluation.

### `INSUFFICIENT_DATA`

Material evidence needed for a stronger decision is missing or unavailable.

Evidence-quality problems take priority over otherwise recognizable patterns.

### `UNUSUAL`

The alert contains a supported condition that warrants deeper investigation rather than immediate policy evaluation.

### `UNKNOWN`

The available evidence does not support a stronger deterministic classification.

The system preserves that uncertainty instead of guessing.

## Next-Stage Routing

Lab 16 supports four vendor-neutral routing states:

- `POLICY_EVALUATION`
- `INVESTIGATION`
- `HUMAN_REVIEW`
- `NO_ACTION_YET`

For the controlled validation set, alerts were routed only to:

- `POLICY_EVALUATION`
- `INVESTIGATION`

`POLICY_EVALUATION` is a routing state only. It is **not** authorization to perform a defensive action.

## Identity and Traceability

Lab 16 preserves the original alert-record identity created in Lab 15.

Example:

```text
AR-...  →  original alert-record identity
TR-...  →  new triage-decision identity
```

The `AR-...` identifier remains attached to the triage record so future stages can trace the decision back to the validated alert record.

Each triage execution generates a new `TR-...` identifier without replacing the original `AR-...` identity.

## Deterministic Decision Order

The public triage logic follows a controlled evaluation order.

Conceptually:

```text
1. Confirm alert-record structure
2. Review validation outcome
3. Check material missing evidence
4. Evaluate supported deterministic conditions
5. Preserve uncertainty when stronger classification is unsupported
6. Assign next-stage routing
7. Record decision history
```

This ordering prevents recognizable patterns from overriding serious evidence-quality problems.

## Severity Is Not a Verdict

Technical severity is preserved as an important signal, but it does not determine triage classification by itself.

Lab 16 specifically validates that:

- HIGH severity does not automatically mean malicious.
- LOW severity does not automatically mean safe.
- Missing evidence can override an otherwise recognizable known pattern.
- UNKNOWN remains explicit when evidence does not support a stronger conclusion.

Severity helps describe technical importance. Triage classification describes what the available evidence supports.

Those are separate decisions.

## Controlled Validation Set

Five sanitized Lab 15-style alert records were used:

1. Known Windows application error
2. Known repeated authentication failure
3. Insufficient-data condition
4. Controlled unusual configuration change
5. Unknown condition

## Frozen Expected Result

```text
Alert records discovered: 5

KNOWN_COMMON: 2
INSUFFICIENT_DATA: 1
UNUSUAL: 1
UNKNOWN: 1

POLICY_EVALUATION: 2
INVESTIGATION: 3
HUMAN_REVIEW: 0
NO_ACTION_YET: 0

Triage decision records created: 5
Failed: 0
```

## Observed First Run

```text
Alert records discovered: 5

KNOWN_COMMON: 2
INSUFFICIENT_DATA: 1
UNUSUAL: 1
UNKNOWN: 1

POLICY_EVALUATION: 2
INVESTIGATION: 3
HUMAN_REVIEW: 0
NO_ACTION_YET: 0

Triage decision records created: 5
Failed: 0
```

**Expected vs. observed: Exact match — PASS**

## Repeat-Processing Validation

A second complete run reproduced the exact same classification and routing totals with zero failures.

The second run also confirmed:

- Original `AR-...` identifiers remained unchanged.
- New `TR-...` identifiers were generated.
- First-run triage records remained intact.
- The first-run batch summary remained intact.
- Existing output was not overwritten.

## Important Safety Results

Lab 16 validated that:

- HIGH severity alone does not establish maliciousness.
- LOW severity alone does not establish safety.
- Missing material evidence has priority over known-pattern matching.
- Unsupported certainty is not fabricated.
- `UNKNOWN` remains explicit when stronger classification is unsupported.
- `POLICY_EVALUATION` does not authorize remediation.
- No alert was marked resolved.
- No defensive action was authorized.
- No defensive action was executed.
- Alert and log content remained untrusted data rather than executable instruction.

## Public / Private Boundary

This public Project Athenaeum lab demonstrates:

- Vendor-neutral triage architecture
- Sanitized deterministic sample rules
- `AR-...` to `TR-...` traceability
- Triage classifications
- Routing states
- Validation behavior
- Structured JSON decision records
- Batch processing
- Repeat-processing protection
- Controlled validation evidence

The following remain private Business Guardian implementation:

- Production triage heuristics
- Proprietary event and condition catalogs
- Cross-source correlation
- Investigation Lane workflows
- Evidence-collection orchestration
- Business-risk scoring
- Policy and approval logic
- Action selection
- Defensive execution
- Verification
- Audit mechanisms
- Customer or tenant-specific logic
- Sensitive configuration and data

Nothing gets built twice.

## Validation Status

**Lab 16 Technical Implementation:** Complete  
**Controlled Validation:** PASS  
**Repeat Processing Validation:** PASS  
**Identity Preservation:** PASS  
**Deterministic Routing:** PASS  
**Severity-Separation Validation:** PASS  
**Failure Count:** 0  
**Defensive Actions Executed:** 0

## Skills Demonstrated

- Python
- JSON processing
- Deterministic decision logic
- Security alert triage
- Vendor-neutral security design
- Evidence-quality handling
- Missing-data validation
- Uncertainty preservation
- Structured routing
- Traceability
- Batch processing
- Audit-oriented design
- Defensive programming
- Repeatable validation
