# Lab 21 — Controlled Live-Action Readiness Requirements and Design

## Problem

Lab 20 proved that Business Guardian could take a synthetic defensive action through a controlled lifecycle.

It could validate the request, enforce approval, prevent duplicate execution, perform the synthetic action, independently verify the result, trigger rollback when needed, and refuse to call something resolved unless verification actually proved it.

That was an important step.

But it still did not answer the next question:

> **What would Business Guardian need to prove before I would be comfortable letting it change a real test endpoint?**

Synthetic execution can test a lot of logic, but it cannot completely represent the risks that come with modifying an actual machine.

A real endpoint could have changed since the action was approved.

The wrong target could be selected.

An approval could be stale.

The action adapter could behave differently than expected.

Verification could become unavailable.

A partial change could occur.

Rollback could fail.

So Lab 21 stops before live remediation and focuses entirely on defining what must be true before a future live action is even considered ready.

No endpoint was modified in this lab.

---

## Importance

The move from synthetic action to real endpoint action is a major safety boundary.

A system should not be allowed to change something simply because an earlier workflow said the action was eligible.

Before Business Guardian is ever allowed to modify a real test endpoint, it should have to prove several things again at the point of execution.

It needs to know that:

- the target is really the endpoint we think it is,
- the target is actually authorized,
- the approval is still valid,
- the approval belongs to this exact action and target,
- the endpoint has not drifted into an unexpected state,
- the action adapter supports the requested operation,
- independent verification is available,
- rollback is ready when required,
- and a human has enough information to approve or stop the action.

The main rule for Lab 21 is:

> **Synthetic execution capability does not mean Business Guardian has permission to change a real endpoint.**

If one of the required readiness conditions cannot be proven, the system should stop or require human review.

---

## What I Designed

Lab 21 defines the readiness contract that must exist before Business Guardian can move from synthetic action orchestration toward a future live action.

The design checks readiness across:

- target identity,
- target authorization,
- approval validity,
- approval freshness,
- approval binding,
- current endpoint conditions,
- adapter support,
- independent verification readiness,
- rollback readiness,
- duplicate-action protection,
- human approval,
- audit preservation,
- and fail-closed handling.

This lab does not execute the action.

It defines what must be proven first.

---

## Where Lab 21 Fits

Project Athenaeum has now progressed through:

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
Controlled Live-Action Readiness
      ↓
Future Authorized Live Test
```

Lab 21 is the bridge between:

```text
"We can safely simulate this action."
```

and:

```text
"We have enough proof to consider testing this on a real authorized endpoint."
```

Those are not the same thing.

---

## Live Action Readiness Record

To represent that decision, Lab 21 introduces the conceptual:

```text
LAR — Live Action Readiness Record
```

The LAR is tied to an existing controlled action request and records whether the action is actually ready to move toward a live test.

The broader record progression becomes:

```text
AR → TR → PD → AP → AQR → LAR
```

The LAR does not replace any of the earlier records.

It adds another checkpoint.

A future live-action lab may eventually extend this chain further through execution and verification records.

---

## Readiness Outcomes

Lab 21 defines three possible outcomes:

```text
READY

NOT_READY

REQUIRES_HUMAN_REVIEW
```

### READY

All required readiness conditions have been demonstrated.

This does **not** mean the action is automatically authorized to execute.

It means the prerequisites have been satisfied.

### NOT_READY

At least one required safety condition failed.

The action must not move forward.

### REQUIRES_HUMAN_REVIEW

The system cannot safely determine readiness on its own.

Someone needs to review the situation before anything else happens.

Human review does not automatically turn the result into `READY`.

---

## Target Identity and Authorization

One of the first things I wanted to separate was identity from authorization.

Knowing which endpoint something is does not mean Business Guardian is allowed to modify it.

Before a future live action can be considered ready, both must be true:

```text
TARGET IDENTITY CONFIRMED
            +
TARGET AUTHORIZATION CONFIRMED
            ↓
READINESS MAY CONTINUE
```

The design should not rely only on weak identifiers like:

- a display name,
- a nickname,
- an IP address by itself,
- or a free-text hostname.

A future implementation will need authoritative endpoint information that makes sense for the platform being controlled.

I intentionally did not lock this public lab into one production target-authority mechanism.

That belongs in the private implementation when the time comes.

---

## Approval Freshness

Approval cannot last forever.

An approval that made sense earlier may no longer be appropriate if enough time has passed or the endpoint has changed.

Lab 21 therefore requires approval to be checked again during live-action readiness.

The public design does not define an exact production expiration window.

What matters here is the rule.

When approval is required, it must still match the intended:

- action,
- target,
- request,
- scope,
- and authorized environment.

Approval for one action cannot quietly authorize another.

Approval for one endpoint cannot quietly move to a different endpoint.

Missing, stale, denied, pending, or mismatched approval blocks readiness.

---

## Pre-Execution Revalidation

Another problem is environmental drift.

Even if the target was correct when the action was requested, something may have changed before execution.

So the system cannot rely completely on earlier evidence.

The future readiness process needs a checkpoint that compares what Business Guardian expects to see with what is actually true immediately before execution.

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

Newer evidence wins over older assumptions.

If the environment has changed in a meaningful way, readiness should either fail or require human review.

An earlier valid observation should never override newer contradictory evidence.

---

## Action Adapter Contract

A future live-action adapter cannot just accept arbitrary commands.

Each supported action needs a defined contract.

That contract should describe things such as:

- which action is supported,
- which platform or target it supports,
- what authorization is required,
- what conditions must be true before execution,
- what state is expected to change,
- what known failure conditions exist,
- whether partial changes are possible,
- how verification works,
- whether rollback is supported,
- what rollback cannot do,
- timeout behavior,
- and what audit information should be preserved.

The intended model is:

```text
CONTROLLED ACTION ID
        ↓
AUTHORIZED ADAPTER
        ↓
DEFINED OPERATION
```

Not:

```text
FREE TEXT
   ↓
ARBITRARY SHELL COMMAND
```

That boundary is important.

Security data or user-provided text should never become a shortcut to arbitrary execution.

---

## Independent Verification

Lab 20 already proved this idea synthetically, and Lab 21 keeps the same rule for future live actions:

> **The component performing the action cannot verify its own work.**

This is not enough:

```text
Executor:
"Command succeeded"

Verifier:
"The executor says it succeeded"
```

The verifier needs its own meaningful evidence.

A future live verifier must be able to produce outcomes such as:

- positive confirmation,
- negative confirmation,
- evidence unavailable,
- conflicting evidence,
- or inconclusive evidence.

Only positive independent verification should ever support eventual resolution eligibility.

If verification cannot prove the expected result, Business Guardian should not pretend the condition is resolved.

---

## Rollback Readiness

Rollback also needs to be planned before execution.

If a future action requires rollback capability, Business Guardian should already know:

- what rollback is expected to do,
- whether rollback is actually available,
- what conditions rollback requires,
- how rollback will be independently verified,
- and what happens if rollback fails.

A clean failure with no state change does not need unnecessary rollback.

A partial or harmful change may.

The rule established earlier still holds:

```text
ROLLBACK_VERIFIED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

A successful rollback only proves that the attempted change was reversed.

It does not prove that the original security problem was fixed.

---

## Human Approval Boundary

For the first future live endpoint action, I want explicit human approval.

Even if Business Guardian eventually supports low-risk preauthorized actions, the first live action should not begin as autonomous remediation.

Before approving the action, the operator should be able to understand:

- what Business Guardian wants to do,
- which endpoint it wants to change,
- why the action is being requested,
- what state should change,
- how the result will be independently verified,
- whether rollback is available,
- and what happens if verification fails.

Conceptually, a future approval step could look something like:

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

Lab 21 defines the information that should be available.

It does not build the interface yet.

---

## Auditability

I also wanted readiness decisions to leave a history.

A future Live Action Readiness Record should preserve information such as:

- readiness-record identity,
- action-request reference,
- target reference,
- action type,
- target-identity result,
- target-authorization result,
- approval status,
- approval-freshness result,
- precondition result,
- environmental drift result,
- adapter-readiness result,
- verifier-readiness result,
- rollback-readiness result,
- human-control result,
- readiness outcome,
- reason information,
- and evaluation time.

If readiness fails and later passes after something changes, both records should remain.

For example:

```text
LAR-001 → NOT_READY
LAR-002 → READY
```

The second result does not erase the first.

That makes it possible to see how the system reached the final decision instead of only seeing the latest state.

---

## Tabletop Validation

Because Lab 21 is design-only, I validated the readiness contract with a frozen tabletop matrix instead of executing anything.

The 24 cases covered:

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

The purpose was to make sure the readiness rules produced the expected outcome before any live implementation was attempted.

---

## Validation Result

The frozen tabletop validation produced:

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

> **PASS — LIVE-ACTION READINESS CONTRACT VALIDATED BY DESIGN**

The important part of this result is what it does **not** mean.

It does not mean Business Guardian has performed live remediation.

It does not mean a production adapter exists.

It does not mean a real endpoint has been proven safe to modify.

It means the readiness requirements behaved correctly across the frozen design scenarios.

---

## Safety Boundary

Lab 21 is intentionally design-only.

No endpoint state was changed.

The lab did not:

- start or access a virtual machine,
- connect to a managed endpoint,
- modify a file,
- modify a user account,
- change firewall rules,
- modify a service,
- change network configuration,
- invoke Wazuh Active Response,
- run PowerShell remediation,
- run shell remediation,
- perform live rollback,
- create a production remediation adapter,
- target a production or customer system,
- authorize automatic retries,
- perform irreversible actions,
- allow generative AI to authorize execution,
- or allow generative AI to verify execution.

That restriction is part of the design process.

I want the rules established before the live capability exists.

---

## Public / Private Boundary

Project Athenaeum documents the parts of the design that are useful for showing the engineering process.

The public Lab 21 material includes:

- the live-action readiness concept,
- the purpose of the LAR,
- the readiness outcomes,
- target identity and authorization requirements,
- approval freshness,
- pre-execution revalidation,
- adapter-contract requirements,
- independent verification requirements,
- rollback readiness,
- human approval,
- the frozen tabletop matrix,
- validation results,
- and the safety boundary.

The public lab does not expose:

- production target-authority implementation,
- private approval-expiration thresholds,
- internal adapter registries,
- private verifier-source logic,
- private rollback-readiness logic,
- customer authorization rules,
- tenant scope,
- credentials,
- production secrets,
- proprietary execution integrations,
- or future live-remediation implementation details.

No public Python implementation was created for this lab because there was nothing useful to gain by rebuilding private product logic simply to make the public repository look more complete.

> **Nothing gets built twice.**

---

## What This Proves

Lab 21 proves that Business Guardian now has a defined safety contract for deciding whether a synthetic controlled action is ready to move toward a future live endpoint test.

The design accounts for:

- authoritative target identity,
- separate target authorization,
- current and correctly bound approval,
- environmental drift,
- pre-execution revalidation,
- controlled adapter capability,
- independent verification readiness,
- rollback readiness,
- duplicate-action protection,
- human approval,
- restrictions around non-reversible actions,
- and preserved readiness history.

The most important distinction is:

```text
READY
```

does not mean:

```text
EXECUTE
```

It means the prerequisites have been demonstrated.

Execution still requires its own controlled decision.

That keeps readiness, authorization, and execution from collapsing into one step.

---

## What I Learned

The biggest lesson from Lab 21 is that the closer Business Guardian gets to changing a real system, the less it can rely on assumptions made earlier in the workflow.

An alert may have been valid.

The investigation may have been correct.

The policy decision may have been correct.

The approval may have been valid.

The synthetic action may have worked perfectly.

And none of that guarantees that a real endpoint is still safe to modify later.

Before live execution, the system has to ask again:

```text
Is this still the right target?

Are we still allowed to act?

Is the approval still valid?

Is the environment still what we expect?

Can we verify the result independently?

Can we recover safely if something goes wrong?
```

That extra layer may feel repetitive, but for a defensive system that can change real infrastructure, repetition at the right safety boundaries is a strength.

---

## What Comes Next

Lab 21 stops before the first live endpoint action.

A future lab may test one narrowly scoped defensive action against one user-owned, authorized, isolated test endpoint.

The first live action should be:

- low risk,
- reversible,
- narrowly scoped,
- independently observable,
- easy to verify,
- and harmless to normal lab operation.

Before anything executes, the future test should still require:

- target revalidation immediately before execution,
- explicit human approval,
- duplicate-execution protection,
- independent verification,
- rollback readiness,
- independent rollback verification,
- complete audit evidence,
- and fail-closed behavior.

No production system or customer environment should be involved.

Lab 20 proved that Business Guardian could safely orchestrate a synthetic action.

Lab 21 defined what has to be true before I would allow that process to move one step closer to a real endpoint.

The next milestone should only happen when those readiness requirements can be proven in the lab, not assumed.
