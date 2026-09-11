# Lab 20 — Synthetic Controlled Action Orchestration and Independent Verification

## The Next Question

By the end of Lab 19, Business Guardian could determine whether an action was eligible and Lab 19 had defined the safety rules that would have to exist before anything was ever allowed to execute.

But that left an obvious problem.

Knowing that an action **may** be allowed is not the same thing as actually performing it safely.

So Lab 20 focused on the next question:

> **Can Business Guardian take an eligible action through execution, verification, rollback, and final outcome handling without ever confusing “the action ran” with “the problem is resolved”?**

I wanted to answer that question before letting the system touch a real endpoint.

For that reason, every action in this lab was synthetic and every state change happened in memory.

No Windows machine was modified.

No Linux machine was modified.

No Wazuh Active Response was triggered.

No real remediation occurred.

The goal was to prove the safety logic first.

---

## Why This Lab is Important

Read-only investigation is relatively safe.

Once software is allowed to change a system, the consequences become much more serious.

A security platform cannot safely receive an action request and simply assume:

```text
Request Exists
      ↓
Run Action
      ↓
Success
```

There are too many things that can go wrong.

The request may not be authorized.

The approval may be missing or stale.

The target may be wrong.

The action may not be supported.

The same request may arrive twice.

The action may report success while producing the wrong result.

It may partially change the system and then fail.

It may need to be reversed.

And even after rollback succeeds, the original security condition may still exist.

So the rule for Lab 20 became simple:

> **If Business Guardian cannot prove that the required safety conditions were satisfied, it does not get to call the result successful.**

That is the boundary this lab was built to test.

---

## What I Built

Lab 20 added a private synthetic controlled-action subsystem to Business Guardian.

The subsystem can take an already eligible action request and move it through a controlled lifecycle.

It now handles:

- action-request validation,
- approval enforcement,
- authorization checks,
- target validation,
- unsupported actions,
- duplicate delivery,
- controlled synthetic execution,
- independent verification,
- execution failure,
- partial execution,
- rollback when required,
- independent rollback verification,
- chronological audit history,
- and final resolution-eligibility decisions.

The important word here is **synthetic**.

The system is exercising real orchestration logic, but it is operating against injected in-memory state instead of a real endpoint.

That gave me a way to test the decision and safety boundaries without introducing live remediation risk.

---

## The Controlled Action Lifecycle

The high-level workflow now looks like this:

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

One of the most important design decisions in this lab is that the component performing the action does **not** get to verify its own work.

Execution and verification are separate responsibilities.

That means:

```text
"I ran the action successfully."
```

is not enough.

A separate verifier has to examine the resulting state and prove that the expected outcome actually occurred.

---

## Safety Rules I Wanted to Prove

Before running the full validation matrix, I froze the safety rules I expected the system to follow.

Lab 20 had to prove that:

- `READY_FOR_ACTION` means eligible for controlled processing, not already executed.
- Missing approval never means approval.
- Authorization must actually belong to the request being processed.
- Invalid, ambiguous, missing, or unauthorized targets fail closed.
- Unsupported actions fail closed.
- The same request cannot silently execute twice.
- Execution completion does not prove the intended result occurred.
- The executor cannot verify its own work.
- Positive independent verification is required before resolution eligibility.
- Failed, unavailable, conflicting, or inconclusive verification blocks resolution.
- A clean failure before any state change should not trigger unnecessary rollback.
- A partial change may require rollback.
- Rollback has to be verified separately.
- Successful rollback does not mean the original security problem was resolved.
- Failed and partial attempts remain part of the audit history.
- Instruction-like text inside security data cannot choose or authorize an action.

I did not want these to be assumptions.

I wanted them tested.

---

## When Is Something Actually Resolution-Eligible?

Lab 20 keeps execution and resolution deliberately separate.

The successful path is:

```text
VALID + AUTHORIZED
        ↓
EXECUTION SUCCEEDED
        ↓
INDEPENDENT VERIFICATION SUCCEEDED
        ↓
RESOLUTION_ELIGIBLE
```

That means even a technically successful action remains unverified until a separate component proves that the expected state exists.

If verification fails:

```text
EXECUTION_COMPLETED_UNVERIFIED
        ↓
VERIFICATION_FAILED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

If verification is unavailable:

```text
EXECUTION_COMPLETED_UNVERIFIED
        ↓
UNABLE_TO_VERIFY
        ↓
NOT_RESOLUTION_ELIGIBLE
```

If the evidence conflicts, the result still does not become resolved.

And rollback follows the same conservative rule.

```text
ROLLBACK_VERIFIED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

Rollback proves that the attempted change was reversed.

It does **not** prove that the original security condition was fixed.

That distinction ended up being one of the most important lessons in this lab.

---

## Validation Plan

I used a frozen 22-case validation matrix.

The goal was not just to prove the happy path.

I wanted to see what happened when approvals were wrong, targets were invalid, actions failed, verification disagreed, rollback broke, or the same request arrived twice.

The matrix covered:

- preauthorized success,
- explicitly approved success,
- pending approval,
- denied approval,
- missing approval,
- stale approval,
- authorization-binding mismatch,
- invalid workflow eligibility,
- unsupported actions,
- invalid targets,
- ambiguous targets,
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
- repeat execution with new identities,
- and preservation of complete chronological audit history.

### Result

```text
22 / 22 VALIDATION CASES PASSED
```

Blocked cases were also checked to make sure they really stopped where they were supposed to stop.

If execution was not allowed, the execution component was not called.

If verification was not appropriate, the verification component was not called.

If rollback was not required, rollback was not called.

That mattered because a system that eventually reaches the right answer after doing something it should never have done is still unsafe.

The complete public-safe matrix is available here:

[`Lab20_22_Case_Validation_Matrix_v1.0.txt`](Lab20_22_Case_Validation_Matrix_v1.0.txt)

---

## Test Results

After the controlled validation passed, I ran the Lab 20 tests and then the full private Business Guardian regression suite.

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

The **293 / 293** result represents the validated Business Guardian baseline at the time Lab 20 was completed.

That number is expected to grow as the product grows.

What mattered here was that adding the controlled-action subsystem did not break the investigation and evidence-processing capabilities that were already working.

---

## What the Main Outcomes Looked Like

### Successful Synthetic Action

The clean successful path looked like this:

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

The key step is:

```text
EXECUTION_COMPLETED_UNVERIFIED
```

The action has run, but Business Guardian still refuses to call it resolved.

Only independent verification can move it forward.

---

### Clean Execution Failure

Not every failed action needs rollback.

If the system can prove that execution failed before any synthetic state was changed, the result is:

```text
EXECUTING
    ↓
EXECUTION_FAILED
    ↓
NOT_RESOLUTION_ELIGIBLE
```

Nothing changed, so there is nothing to undo.

That keeps rollback from becoming an automatic reflex when it is unnecessary.

---

### Partial Execution

A more dangerous case is when an action changes something and then fails.

That path looked like:

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

Even after rollback succeeds, Business Guardian does not pretend the original security condition has been resolved.

It only knows that the attempted change was successfully reversed.

The original condition still needs to be evaluated.

---

### Verification Failure

Another case I wanted to prove was an executor reporting success while the verifier disagreed.

```text
EXECUTION_COMPLETED_UNVERIFIED
        ↓
VERIFICATION_FAILED
        ↓
NOT_RESOLUTION_ELIGIBLE
```

The execution result does not win simply because it happened first.

The verifier gets an independent say.

---

## Duplicate Execution Protection

One of the cases I especially wanted to test was duplicate delivery.

In a real system, the same request could be submitted twice because of a retry, communication problem, or some other failure upstream.

If that happened, I did not want Business Guardian to simply execute the action again.

Lab 20 confirmed that it does not.

When the same controlled request is delivered a second time, the original execution attempt is preserved and the duplicate is rejected before another action can run.

That gives the system an important guarantee:

> **One approved request should not quietly become two defensive actions.**

---

## Auditability

Another goal for Lab 20 was making sure the system could explain what happened after the fact.

A security workflow should not only know where it ended.

It should preserve how it got there.

The controlled-action layer keeps a chronological history that can include:

- the original action request,
- the execution attempt,
- verification evidence,
- rollback activity when needed,
- state changes,
- timestamps,
- controlled reason information,
- and the final resolution-eligibility decision.

That history is intentionally not erased when something later succeeds.

If an execution attempt fails and rollback is required, the failure remains part of the record.

If rollback succeeds, the execution attempt that caused it remains part of the record.

If the same request is delivered twice, the duplicate does not replace the original attempt.

The result is a much clearer picture of what the system considered, what it actually tried, what it verified, and what it ultimately allowed or refused.

---

## Evidence

I did not want to publish the private Business Guardian implementation just to prove Lab 20 worked.

Instead, I created a small set of sanitized evidence records showing the most important outcomes from the controlled validation.

### Successful Controlled Action

[`sanitized-successful-action-audit.json`](evidence/sanitized-successful-action-audit.json)

Shows a synthetic action completing successfully and then passing independent verification before becoming `RESOLUTION_ELIGIBLE`.

### Clean Execution Failure

[`sanitized-clean-failure-audit.json`](evidence/sanitized-clean-failure-audit.json)

Shows an action failing before synthetic state changed. Because nothing changed, the system correctly avoided an unnecessary rollback.

### Partial Execution and Rollback

[`sanitized-rollback-audit.json`](evidence/sanitized-rollback-audit.json)

Shows a partial synthetic change, the rollback process, independent rollback verification, and the final `NOT_RESOLUTION_ELIGIBLE` outcome.

### Duplicate Delivery

[`sanitized-duplicate-delivery-audit.json`](evidence/sanitized-duplicate-delivery-audit.json)

Shows the same controlled request being delivered twice while producing only one execution attempt.

These records use demonstration identities and sanitized synthetic values.

They do not contain production or customer information.

---

## Safety Boundary

Lab 20 was intentionally kept synthetic.

That was important.

The goal of this lab was to prove the orchestration and safety logic **before** giving it the ability to change a real system.

Lab 20 did not:

- start or access a virtual machine,
- modify a Windows or Linux endpoint,
- change endpoint files,
- disable or modify an account,
- change firewall rules,
- modify a service,
- change network controls,
- invoke Wazuh Active Response,
- run remediation through PowerShell,
- run remediation through a shell,
- perform a live rollback,
- target a production or customer system,
- allow generative AI to authorize an action,
- or allow generative AI to verify an action.

Execution, verification, and rollback all happened against controlled in-memory state.

That gave me a way to test the dangerous part of the workflow without introducing the danger of real remediation.

---

## Public / Private Boundary

The working controlled-action subsystem remains in the private Business Guardian repository.

Project Athenaeum documents the parts that are useful for showing the engineering process:

- the high-level architecture,
- the safety rules,
- the workflow,
- the validation approach,
- the results,
- and sanitized evidence showing representative outcomes.

The public lab does not include:

- private orchestration source code,
- proprietary validation implementation,
- internal action adapters,
- internal verification implementation,
- private attempt-ledger behavior,
- exact internal validation sequencing,
- customer policy logic,
- tenant authorization,
- credentials,
- sensitive configuration,
- or future live-remediation implementation.

That separation is intentional.

I wanted Lab 20 to prove that the capability exists without rebuilding the private product in public just for the sake of having another lab.

> **Nothing gets built twice.**

---

## What This Proves

Lab 20 is the first point in Project Athenaeum where Business Guardian moves beyond a completely read-only investigation architecture.

But it does that carefully.

The system can now take an eligible synthetic action through a controlled lifecycle while still refusing to assume that execution means success.

The validation showed that it can:

- stop invalid actions before execution,
- enforce authorization and approval requirements,
- reject bad or ambiguous targets,
- prevent duplicate execution,
- preserve the relationship between the request and its source,
- tell the difference between a clean failure and a partial change,
- require independent verification,
- trigger rollback when the situation requires it,
- verify rollback separately,
- preserve the full history of what happened,
- and refuse resolution when positive verification is missing.

The part that matters most to me is that the system remained conservative even when things went wrong.

It did not turn uncertainty into success.

It did not turn rollback into resolution.

And it did not let the component performing the action declare its own work verified.

That is exactly the behavior I wanted to establish before considering anything live.

---

## What I Learned

The biggest lesson from Lab 20 was that execution is actually a small part of the problem.

Running a command is easy.

Proving that it was the right command, against the right target, with the right authorization, exactly once, and then proving that it produced the intended result is much harder.

Rollback adds another layer.

A rollback can succeed perfectly and still leave the original security problem unresolved.

That means a safe response system has to think about more than actions.

It has to think about:

```text
Intent
   ↓
Authorization
   ↓
Execution
   ↓
Evidence
   ↓
Verification
   ↓
Outcome
```

Each one is a separate question.

That is the architecture I want Business Guardian to keep following.

---

## What Comes Next

Lab 20 deliberately stops here.

The next step is **not** to immediately point this at a real endpoint.

Before Business Guardian is allowed to move from synthetic action orchestration into carefully scoped remediation against an authorized test machine, there are still some important problems to solve.

Those include:

- proving exactly which target an action is allowed to affect,
- defining safe production-style action-adapter contracts,
- making sure the verifier remains independent from the executor,
- deciding how long approvals remain valid,
- controlling when a failed action may be retried,
- handling actions that cannot be safely reversed,
- defining live rollback procedures,
- and strengthening human approval around higher-risk actions.

Lab 19 defined the safety contract.

Lab 20 proved that the contract can be enforced in a synthetic controlled-action workflow.

The next challenge will be deciding when that design is strong enough to take one carefully controlled step closer to a real authorized endpoint.

And the rule remains the same:

> **Nothing is resolved until the result is independently verified.**
