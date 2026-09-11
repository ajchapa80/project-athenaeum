# Lab 23 — Business Guardian Operator Dashboard Requirements and UX Design

## Problem

Up to this point, most of Business Guardian had been focused on the security logic behind the scenes.

The system could process alerts, investigate evidence, evaluate policy, handle approval, control execution, verify results, and preserve audit history.

But none of that answers a very important product question:

> **What should Business Guardian actually look like to the person using it?**

I did not want to build another security dashboard that expects the operator to understand raw logs, event IDs, severity scores, or dozens of technical widgets.

Business Guardian is meant to help small businesses.

That means the interface needs to answer simpler questions first:

```text
Am I okay?

What needs my attention?

What did Business Guardian find?

What do I need to approve?

What action was taken?

Did the action actually work?
```

Lab 23 was built around designing that experience.

No production dashboard was built in this lab.

The goal was to create the design baseline first.

---

## Importance

A strong backend is only useful if the person using it can understand what the system is telling them.

Small businesses may not have a dedicated cybersecurity analyst sitting behind the screen.

The operator may be an owner, manager, office administrator, or technical employee who needs clear answers without digging through security telemetry.

That means Business Guardian should show the most important conclusion first and let the operator go deeper only when they need more detail.

The design follows that idea:

```text
Plain-English Summary
        ↓
Recommended Next Step
        ↓
Supporting Evidence
        ↓
Technical Detail
```

The interface should help the operator make a safe decision without hiding the evidence behind that decision.

---

## What I Designed

Lab 23 produced the first complete Business Guardian operator UX baseline.

The design contains 18 desktop and tablet or narrow-laptop artboards covering nine main areas:

1. Overview
2. Alert Detail
3. Investigation
4. Recommended Action / Human Approval
5. Action Progress / Independent Verification
6. Reports
7. Audit History
8. System Health
9. Settings

Together, these screens define how the main Business Guardian workflow should feel from the operator side.

The design covers:

- information architecture,
- visual hierarchy,
- navigation,
- alert review,
- investigation results,
- recommended actions,
- human approval,
- action progress,
- independent verification,
- reporting,
- audit history,
- system health,
- settings,
- responsive layouts,
- and Chapa Technology Solutions branding.

This gives future implementation a clear target instead of designing the interface while writing production code.

---

## Operator Workflow

The interface follows the same safety model that Business Guardian has been building through the previous labs:

```text
Alert
  ↓
Investigation
  ↓
Recommendation
  ↓
Human Approval
  ↓
Controlled Execution
  ↓
Independent Verification
  ↓
Final Outcome
```

I wanted those stages to remain visually separate because they mean different things.

The dashboard should never make it look like:

```text
Recommendation = Approval
```

or:

```text
Execution = Verification
```

The interface preserves these boundaries:

```text
Recommendation ≠ Authorization

Authorization ≠ Execution

Execution ≠ Verification

Verification ≠ Automatic Resolution
```

That separation is just as important in the interface as it is in the backend.

---

## Designing for a Small-Business Operator

I wanted the main experience to feel understandable without making it simplistic.

The operator should see the answer to the immediate question first.

For example:

```text
What happened?

What does it mean?

Do I need to do anything?

What does Business Guardian recommend?
```

Technical evidence should still be available, but it does not need to dominate the screen.

This is where progressive disclosure becomes useful.

A normal operator may only need:

```text
Suspicious login detected

Business Guardian investigated the activity

Additional review is recommended
```

A technical user may choose to expand the evidence and see:

```text
Source platform
Event information
Endpoint
User
Evidence collected
Rule details
Investigation notes
```

Both users can work from the same product without forcing the less technical operator to read a SIEM console.

---

## Overview

The Overview is meant to answer the first question someone would probably ask when opening Business Guardian:

> **Is everything okay?**

The screen is designed around:

- current security status,
- items needing attention,
- active investigations,
- actions waiting for approval,
- recently verified outcomes,
- system health,
- and important activity.

I wanted the Overview to act more like a security briefing than a wall of charts.

Charts can still be useful, but they should support the story instead of becoming the story.

---

## Alert Detail

The Alert Detail screen gives the operator a focused view of one security event.

The goal is to explain:

```text
What happened?

How serious is it?

What system or account is involved?

What does Business Guardian currently know?

What happens next?
```

The design keeps the plain-English explanation near the top while still allowing deeper technical evidence to be reviewed when needed.

Alert severity, business impact, workflow status, and evidence quality are kept separate.

Those values may influence one another, but they are not the same thing.

---

## Investigation

The Investigation screen shows what Business Guardian has done to better understand the alert.

It can present things such as:

- evidence collected,
- evidence still missing,
- investigation steps,
- endpoint or account context,
- related activity,
- investigation result,
- and the recommended next step.

One of the things I wanted to avoid was making incomplete evidence look like certainty.

If Business Guardian does not have enough information, the interface should say so.

For example:

```text
INSUFFICIENT EVIDENCE
```

should remain different from:

```text
SAFE
```

If the system does not know, the dashboard should not pretend that it does.

---

## Recommended Action and Human Approval

The approval screen is one of the most important parts of the design.

I did not want a large generic:

```text
FIX NOW
```

button.

If the action can change a real system, the operator should understand exactly what they are approving.

The design keeps information such as this visible:

```text
What Will Change

What Will NOT Change

Target

Action

Reason

Risk

Expected Result

Verification Method

Rollback Availability
```

The operator should know the scope before approving anything.

Approval should be deliberate without becoming confusing.

---

## Action Progress and Independent Verification

Once an action begins, the interface needs to show more than a loading spinner.

The operator should be able to tell which stage the workflow is actually in.

For example:

```text
Approved
    ↓
Preparing Action
    ↓
Executing
    ↓
Execution Completed
    ↓
Independent Verification
    ↓
Verified Outcome
```

The interface keeps execution and verification separate.

A successful execution should not immediately become a green resolved message.

Instead, the operator should be able to see that the action completed but is still waiting for verification.

That makes the product behavior visible instead of hiding the safety model behind the scenes.

---

## Reports

The Reports area gives the operator a cleaner way to review security activity over time.

Reports may eventually include things such as:

- alert summaries,
- investigation results,
- verified actions,
- unresolved issues,
- security trends,
- and Business Guardian activity.

Lab 23 defines how that experience should look.

It does not implement production report generation or PDF creation yet.

---

## Audit History

The Audit History screen is designed to answer:

> **What happened, and when?**

The operator should be able to review the sequence of important events without digging through application logs.

That can include:

```text
Alert Created

Investigation Started

Evidence Collected

Recommendation Created

Human Approval

Action Started

Action Completed

Verification Completed

Final Outcome Recorded
```

The history should preserve previous failures or blocked states rather than rewriting the past when something later succeeds.

The design shows recorded workflow history without claiming that production-grade immutable audit storage has already been implemented.

---

## System Health

Business Guardian also needs to tell the operator when **Business Guardian itself** may have a problem.

System Health is kept separate from alert severity.

For example:

```text
Evidence Connector Offline
```

does not automatically mean:

```text
Security Incident
```

It means the system may have reduced visibility.

The design keeps those concepts separate so a product-health problem is not accidentally presented as evidence of malicious activity.

---

## Settings

The Settings area establishes the future location for product configuration.

Examples may include:

- notification preferences,
- connected security sources,
- operator preferences,
- approval behavior,
- reporting options,
- and product configuration.

These are design concepts only.

Persistent production settings were not implemented in Lab 23.

---

## Safety and Trust Model

The UX follows the same safety boundaries already established in Business Guardian.

Important design rules include:

- consequential actions require explicit human approval,
- no arbitrary endpoint shell is exposed,
- no general-purpose command interface is exposed,
- action risk is separate from alert severity,
- evidence quality is separate from workflow status,
- business impact is separate from technical severity,
- blocked execution is separate from failed execution,
- verification failure stays visible,
- insufficient evidence routes to review instead of becoming a guessed answer,
- and degraded system health is not treated as proof of malicious activity.

Automatic remediation and automatic rollback are not presented as implemented capabilities.

The interface should never make the product look more capable than the backend actually is.

---

## Responsive Design

The baseline includes both desktop and tablet or narrow-laptop concepts.

The goal was not to build two completely different products.

The goal was to see whether the same information hierarchy could adapt to less screen space.

The narrow layouts demonstrate:

- responsive navigation,
- stacked information,
- preserved action visibility,
- readable status presentation,
- and simplified layouts without removing important safety information.

These artboards show responsive design direction.

They do not represent a finished production tablet application.

---

## Branding

Lab 23 also establishes the first complete branded Business Guardian product experience under Chapa Technology Solutions.

The design uses the company branding while keeping security-state colors separate from brand colors.

That distinction matters.

A blue company color should not automatically mean:

```text
SAFE
```

and a red brand element should never accidentally imply:

```text
CRITICAL
```

Branding and security meaning need to remain separate.

---

## Validation and Review

After the UX baseline was completed, I reviewed the design for consistency and safety.

The review covered:

- screen architecture,
- desktop behavior,
- narrow-layout behavior,
- terminology,
- workflow boundaries,
- button hierarchy,
- badges and states,
- progressive disclosure,
- accessibility consistency,
- capability overclaims,
- security controls,
- commercial coherence,
- and branding.

Several corrections were made during that review.

These included:

- changing **Recently Resolved** to **Recently Verified**,
- normalizing approval terminology,
- normalizing evidence-review terminology,
- clarifying that automatic rollback is not implemented,
- separating evidence-quality styling from workflow status,
- and keeping brand colors separate from security-state colors.

Those may sound like small wording changes, but they help keep the interface aligned with the actual Business Guardian safety model.

---

## Evidence

The six images below are sanitized prototype artboards.

Names, organizations, endpoints, and events shown in them are fictional demonstration data.

The public repository does not include the full interactive prototype archive or the complete 18-artboard design package.

### Overview

<p align="center">
  <img src="evidence/Lab23_Overview_Desktop_Final.png" alt="Business Guardian Overview" width="760">
</p>

### Alert Detail

<p align="center">
  <img src="evidence/Lab23_Alert_Detail_Desktop_Final.png" alt="Business Guardian Alert Detail" width="760">
</p>

### Investigation

<p align="center">
  <img src="evidence/Lab23_Investigation_Desktop_Final.png" alt="Business Guardian Investigation" width="760">
</p>

### Recommended Action and Human Approval

<p align="center">
  <img src="evidence/Lab23_Recommended_Action_Desktop_Final.png" alt="Business Guardian Recommended Action and Human Approval" width="760">
</p>

### Action Progress and Independent Verification

<p align="center">
  <img src="evidence/Lab23_Action_Progress_Desktop_Final.png" alt="Business Guardian Action Progress and Independent Verification" width="760">
</p>

### Reports

<p align="center">
  <img src="evidence/Lab23_Reports_Desktop_Final.png" alt="Business Guardian Reports" width="760">
</p>

See:

[`Lab23_Validation_Results_v1.0.txt`](Lab23_Validation_Results_v1.0.txt)

for the public-safe validation summary.

---

## Capability Boundary

Lab 23 is a UX requirements and design lab.

It does **not** claim that the production dashboard already exists.

### Designed

The completed baseline includes:

- operator-facing information architecture,
- visual hierarchy,
- desktop layouts,
- narrow-layout concepts,
- alert review,
- investigation,
- approval,
- action progress,
- verification,
- reports,
- audit history,
- system health,
- settings,
- and Chapa Technology Solutions branding.

### Not Implemented

Lab 23 did not implement:

- a production dashboard,
- backend dashboard integration,
- production authentication,
- production role-based access control,
- persistent settings,
- production report generation,
- production PDF generation,
- external sharing,
- automatic remediation,
- automatic rollback,
- arbitrary endpoint shell access,
- customer administration,
- tenant administration,
- or production action and verification orchestration.

The prototype shows how the product should behave.

It is not proof that every control shown in the design is already connected to a production backend.

---

## What This Proves

Lab 23 proves that the Business Guardian safety model can be translated into an interface that a small-business operator can actually understand.

The product does not have to become a traditional SIEM console just because it works with cybersecurity data.

The operator can see:

```text
What happened

What Business Guardian found

What needs attention

What requires approval

What action occurred

Whether the result was verified
```

without removing access to the technical evidence behind those answers.

Just as importantly, the design keeps the safety boundaries visible.

The interface does not make recommendation, approval, execution, verification, and resolution look like the same thing.

That gives the future dashboard implementation a much stronger starting point.

---

## What I Learned

The biggest lesson from Lab 23 is that designing the operator experience forces you to look at the security workflow differently.

A backend can contain dozens of states and records.

The operator should not have to understand all of them just to answer:

```text
Do I need to do something?
```

The challenge is deciding what information needs to be visible immediately and what should stay one level deeper.

I also found that small wording choices matter.

Terms like:

```text
Resolved

Verified

Approved

Recommended

Failed

Blocked
```

can completely change what the operator thinks happened.

If those words are used carelessly, the interface can weaken the safety model even if the backend logic is correct.

That is why I wanted the UX designed and reviewed before building the actual dashboard.

---

## Final Lab Result

> **PASS — COMPLETE BUSINESS GUARDIAN OPERATOR UX BASELINE DESIGNED, REVIEWED FOR SAFETY AND CONSISTENCY, BRANDED, AND PRESERVED FOR IMPLEMENTATION**

Lab 23 gives Business Guardian something it did not have before:

A complete picture of what the product should feel like from the operator side.

---

## What Comes Next

The next planned lab is:

> **Lab 24 — Business Guardian Dashboard MVP**

Lab 24 should begin turning this frozen UX baseline into a working browser-based interface.

The goal should be to reuse the Business Guardian capabilities that already exist rather than inventing fake backend behavior just to make buttons appear functional.

The implementation should preserve the same workflow:

```text
UNDERSTAND
    ↓
INVESTIGATE
    ↓
RECOMMEND
    ↓
AUTHORIZE
    ↓
ACT
    ↓
INDEPENDENTLY VERIFY
    ↓
SHOW THE OUTCOME CLEARLY
```

The design work is done.

The next challenge is turning it into a real operator experience without losing the safety boundaries that were built into it.
