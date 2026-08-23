# Lab 13 — AI Alert Explainer v2: Requirements and Design

## Before Writing More Code, What Should the Next Version Actually Do?

Lab 11 produced the first working AI Alert Explainer MVP.

Lab 12 then tested it under normal and abnormal conditions and established a stable baseline.

The easy next move would have been to start adding features immediately.

Instead, Lab 13 stops and asks a more important question:

**What should version 2 look like before I write it?**

This lab turns the lessons from testing into a controlled technical design for the next processing architecture.

No v2 implementation code was written during Lab 13.

That was intentional.

The progression becomes:

```text
Lab 11
Working MVP
    ↓
Lab 12
Test and Validate
    ↓
Lab 13
Requirements and Design
    ↓
Lab 14
Controlled Implementation
```

The validated Labs 11 and 12 baseline remains untouched.

**Nothing gets built twice.**

---

# Why Design Before Coding?

Lab 12 showed that the original MVP worked.

It also exposed areas that would need to change if the project was going to grow beyond a single prepared alert.

Rather than modifying the stable version immediately, Lab 13 converted those observations into explicit requirements.

That helps prevent several common problems:

- Rewriting code without a clear target
- Expanding scope during implementation
- Breaking a working baseline
- Mixing source-specific logic with reusable processing
- Inventing behavior while testing
- Changing expected results after seeing what the code produces

The goal was to make Lab 14 testable before Lab 14 existed.

---

# What Version 2 Needed to Solve

The first MVP was intentionally small.

It processed one prepared alert at a time.

Version 2 needed to prepare for a much more realistic workflow.

The design focused on:

- Multiple-alert processing
- Cleaner input and output organization
- Vendor-neutral alert data
- Wazuh source translation
- Consistent severity handling
- Missing and malformed-data validation
- Independent alert processing
- Unique output reports
- Failure isolation
- Batch summaries
- Deterministic acceptance testing
- Human review before consequential conclusions

The goal was not to build the entire Business Guardian platform.

The goal was to define the next reliable layer.

---

# Preserve the Working Baseline

A major Lab 13 design rule was simple:

> **Do not improve a stable baseline by destroying the evidence that it worked.**

Labs 11 and 12 remain preserved exactly as the validated MVP stage.

Lab 13 creates the next design separately.

That means future implementation can be compared against the original behavior instead of retroactively changing history.

The design principles include:

- Preserve validated work
- Use testing results to justify changes
- Keep the first v2 implementation manageable
- Process alerts independently
- Separate source handling from reusable logic
- Identify incomplete data rather than invent values
- Preserve original alert evidence
- Protect generated reports from overwrite
- Keep analyst review visible throughout the workflow

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_05_design-principles-complete_GitHub.png"
    alt="Lab 13 completed design principles"
    width="820">
</p>

<p align="center">
  <em>The v2 design principles were documented before implementation began.</em>
</p>

---

# Stop Designing Around One Vendor

Wazuh is the first alert source used by Project Athenaeum because it is already deployed in the lab.

But Lab 13 deliberately avoids making Wazuh field names the permanent internal architecture.

Instead:

```text
Wazuh Alert
     ↓
Source-Specific Mapping
     ↓
Normalized Alert Model
     ↓
Shared Processing Logic
```

At a high level, the normalized model can represent:

- Source platform
- Timestamp
- Endpoint information
- Event information
- Detection rule
- Original severity
- Normalized severity
- Validation state
- Review state

The original source data remains available for analyst verification.

The benefit is that the core workflow can eventually support additional security platforms without rebuilding the entire explanation system around each vendor.

---

# Designing the Wazuh Mapping Layer

Lab 13 defines how selected Wazuh fields can be translated into the common model.

The mapping layer acts as the boundary between:

```text
Vendor-Specific Security Data
            ↓
Reusable Internal Structure
```

That separation becomes one of the most important architectural decisions in the later Business Guardian direction.

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_15_wazuh-mapping-part3_GitHub.png"
    alt="Lab 13 sanitized Wazuh-to-normalized mapping design"
    width="900">
</p>

<p align="center">
  <em>Selected Wazuh fields are mapped into a reusable normalized alert structure without changing the source evidence.</em>
</p>

---

# Severity Needs Its Own Design

Lab 12 proved that the MVP responded correctly when the Wazuh rule level changed.

Version 2 takes the next step.

Instead of treating Wazuh's numeric rule level as the permanent internal severity system, Lab 13 defines platform-neutral categories:

```text
INFORMATIONAL
LOW
MEDIUM
HIGH
CRITICAL
UNKNOWN
```

The original source severity remains preserved.

Conceptually:

```text
Original Wazuh Severity
          +
Normalized Severity
```

The normalized value improves consistency across reports.

It does not erase the original evidence.

It also does not decide whether activity is malicious.

> **Severity helps describe importance. It is not a security verdict.**

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_18_severity-design-part3_GitHub.png"
    alt="Lab 13 normalized severity design"
    width="900">
</p>

<p align="center">
  <em>The severity design preserves the source value while introducing a consistent platform-neutral representation.</em>
</p>

---

# Moving Beyond One Alert at a Time

The Lab 11 MVP handled one prepared alert per execution.

Lab 13 designs a workflow capable of processing several alerts during one run.

The planned sequence is:

```text
1. Discover input files
2. Process each alert independently
3. Normalize supported data
4. Validate available fields
5. Generate an explanation
6. Create a unique report
7. Record the processing result
8. Continue to the next alert
9. Produce a batch summary
```

The key reliability requirement is:

> **One invalid alert should not automatically stop the rest of the batch.**

That idea becomes failure isolation in Lab 14.

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_21_processing-flow-diagram_GitHub.png"
    alt="Lab 13 AI Alert Explainer v2 processing flow"
    width="900">
</p>

<p align="center">
  <em>The planned processing flow defines the sequence later implemented in Lab 14.</em>
</p>

---

# Validation Becomes Part of the Architecture

In the original MVP, validation was mainly something encountered when input went wrong.

Version 2 treats validation as an explicit processing stage.

The design distinguishes between:

- Valid input
- Incomplete input
- Missing optional information
- Unsupported input
- Processing errors

Missing values must be identified.

They must not be invented.

That gives the system room to say:

```text
I can process this, but some information is missing.
```

rather than choosing between only:

```text
Success
```

or:

```text
Failure
```

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_34_validation-design-part5_GitHub.png"
    alt="Lab 13 validation design"
    width="900">
</p>

<p align="center">
  <em>The validation design separates incomplete, unsupported, and valid security data before output is generated.</em>
</p>

---

# Designing the Output Before Generating It

Version 2 is designed to create one report for each processable alert.

Planned report content includes:

- Alert identification
- Endpoint context
- Event context
- Source rule information
- Original severity
- Normalized severity
- Missing-field warnings
- Plain-language explanation
- Recommended review steps
- Human-review status

Every report must use a unique filename.

That prevents a later execution from silently replacing earlier evidence.

---

# The Batch Summary

Processing multiple alerts creates another problem:

**How does an analyst understand the entire run without opening every report first?**

Lab 13 introduces the batch-summary concept.

A batch summary may include:

- Files discovered
- Alerts successfully processed
- Alerts containing incomplete data
- Alerts that failed validation
- Reports generated
- Processing errors
- Items requiring human review

The batch summary becomes the high-level record of one complete processing execution.

---

# Designing the Test Before Building the Feature

One of the most important outcomes from Lab 13 is the controlled validation plan for Lab 14.

The design defines five deterministic test scenarios.

They cover:

1. A normal baseline alert
2. A different severity condition
3. A higher-severity alert
4. An alert with missing information
5. Invalid or unsupported input

The purpose is not simply to see whether the program runs.

The purpose is to define what correct behavior looks like before implementation begins.

That changes the development process from:

```text
Write Code
    ↓
See What Happens
```

to:

```text
Define Expected Behavior
        ↓
Write Code
        ↓
Compare Actual Result
        ↓
PASS or FIX
```

That model becomes increasingly important in Labs 14, 15, and 16.

---

# Freezing the Lab 14 Scope

Lab 13 ends by defining exactly what the next implementation is allowed to include.

Lab 14 will focus on:

- Creating the v2 workspace
- Supporting multiple sanitized alert samples
- Separating input and output
- Building the normalized alert structure
- Creating the first Wazuh mapping process
- Applying validation rules
- Adding normalized severity
- Generating unique reports
- Isolating individual alert failures
- Creating a batch summary
- Running the planned deterministic tests

It will not attempt to build:

- A full dashboard
- Autonomous remediation
- Advanced investigation
- Commercial Business Guardian functionality
- The entire future security lifecycle

Scope is intentionally limited so the processing foundation can be proven first.

<p align="center">
  <img
    src="screenshots/2026-08-13_Lab13_AIAlertExplainerV2_42_final-baseline-part2_GitHub.png"
    alt="Lab 13 final baseline and Lab 14 implementation scope"
    width="900">
</p>

<p align="center">
  <em>The final design review preserves the validated MVP and freezes the implementation scope for Lab 14.</em>
</p>

---

# What Was Completed

Lab 13 produced an implementation-ready design without changing the working MVP.

Completed work includes:

- Reviewed the validated Lab 11 MVP
- Reviewed Lab 12 testing results
- Preserved Labs 11 and 12 as the stable baseline
- Defined v2 design principles
- Designed the normalized alert model
- Designed the initial Wazuh mapping
- Designed normalized severity handling
- Defined multiple-alert processing
- Defined validation behavior
- Defined missing-field behavior
- Planned failure isolation
- Designed individual report requirements
- Designed batch-summary requirements
- Defined the Lab 14 workspace
- Created deterministic validation scenarios
- Frozen the initial Lab 14 implementation scope
- Completed technical design documentation
- Completed the lab notes and screenshot record
- Selected sanitized evidence for public publication

No v2 production implementation was written during this lab.

That distinction is important.

**Lab 13 is the design. Lab 14 is the implementation.**

---

# What Lab 13 Changed About the Development Process

The project progression now becomes:

```text
Build
  ↓
Test
  ↓
Validate
  ↓
Design the Next Version
  ↓
Implement
  ↓
Test Again
```

Lab 13 demonstrates that development is not just about adding more code.

Sometimes the correct next technical step is to stop coding long enough to decide what the code should actually do.

---

# Public / Private Boundary

Lab 13 publishes the portfolio-safe design progression.

Public material includes:

- High-level requirements
- Sanitized architectural concepts
- Vendor-neutral design principles
- Testing strategy
- Implementation scope
- Selected design evidence
- Lessons learned

The complete internal requirements record and full screenshot history are intentionally not published.

Business Guardian product-level development remains private, including areas such as:

- Proprietary connector logic
- Production investigation workflows
- Policy and approval systems
- Tenant architecture
- Sensitive logging
- Product-specific automation
- Commercial workflows
- Other proprietary implementation details

Project Athenaeum shows the engineering decisions without exposing the commercial product architecture.

---

# Skills Demonstrated

- Requirements analysis
- Technical design
- Security architecture planning
- Vendor-neutral data modeling
- Wazuh data mapping
- Severity normalization design
- Validation design
- Missing-data handling
- Failure-isolation planning
- Batch-processing design
- Report architecture
- Deterministic test planning
- Scope control
- Human-in-the-loop security design
- Technical documentation

---

# What Lab 13 Proves

Lab 13 demonstrates that a validated MVP can be extended without immediately rewriting it.

The lab successfully established:

- A vendor-neutral direction
- A normalized alert model
- A Wazuh translation boundary
- Platform-neutral severity
- Multiple-alert processing requirements
- Explicit validation behavior
- Missing-data rules
- Failure isolation
- Unique output requirements
- Batch-level reporting
- Deterministic acceptance criteria
- A frozen implementation scope

Most importantly:

> **The next version had a measurable definition of success before the first new line of v2 implementation code was written.**

---

# Where the Project Goes From Here

Lab 12 answered:

**Does the original MVP behave reliably under normal and abnormal conditions?**

Lab 13 answered:

**What should the next version look like based on what those tests taught me?**

The next question is:

**Can I actually build it and make the observed behavior match the design?**

[Lab 14 — AI Alert Explainer v2: Multiple Alert Processing](../lab-14-ai-alert-explainer-v2-multiple-alert-processing/README.md) answers that question.

The progression becomes:

```text
Single-Alert MVP
      ↓
Validated MVP
      ↓
Requirements and Design
      ↓
Multiple-Alert Implementation
      ↓
Controlled Validation
```

Lab 13 is the point where Project Athenaeum stops adding features reactively and starts treating the security tooling like a designed software system.
