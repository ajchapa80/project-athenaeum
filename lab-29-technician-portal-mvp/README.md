# Lab 29 — Technician Portal MVP

## Result

**PASS — TECHNICIAN PORTAL MVP IMPLEMENTED, INTEGRATED, AND VALIDATED**

Lab 29 implemented the high-fidelity Technician Portal designed in Lab 28 and connected it to bounded Business Guardian workflows.

The completed MVP supports authenticated technician access, server-authoritative organization context, tenant-aware incident work, structured AI advisory assistance, governed Response Action preparation and approval, one fixed defensive lab capability, independent verification, separately governed rollback, customer-safe audit history, and final safe-state restoration.

The core authority model is:

> **AI MAY PROPOSE.**
>
> **AUTHORIZED HUMAN/POLICY APPROVES.**
>
> **DETERMINISTIC BUSINESS GUARDIAN CONTROLS EXECUTE AND VERIFY.**

Generative AI remains advisory. It cannot independently approve, execute, verify, roll back, close incidents, or grant itself authority.

## Objective

Turn the frozen Lab 28 Technician Portal design into an integrated, validated MVP without weakening organization isolation, human approval, deterministic action governance, independent verification, rollback controls, or incident-closure boundaries.

## Starting Point from Lab 28

Lab 28 established the portal's information architecture, visual language, reusable component strategy, major screen contracts, core technician journeys, deterministic acceptance design, and human-authority boundaries.

Lab 29 implemented that approved direction rather than redesigning it during construction. The resulting portal preserves the principles:

> **Instrument panel, not dashboard.**

> **Cybersecurity aesthetic without cybersecurity clutter.**

## Architecture Boundary

The Technician Portal provides a bounded technician experience over existing Business Guardian security workflows. It does not expose arbitrary commands, unrestricted administration, raw private APIs, or a broad remediation catalog.

The server remains authoritative for technician identity, organization scope, customer switching, incident access, approval, action eligibility, execution state, verification, rollback, and audit projection.

Customer-facing information is projected through controlled views rather than exposing private records or internal implementation details directly.

## Technician Portal Purpose

The customer Dashboard focuses on one organization's security experience. The Technician Portal supports an authorized technician working across assigned organizations while continuously preserving the active customer context.

The MVP helps technicians:

- review assigned organization and incident context,
- investigate evidence and lifecycle history,
- view customer-safe incident and report projections,
- use structured AI advisory assistance,
- prepare a governed Response Action,
- submit or review explicit human approval,
- observe controlled execution and independent verification,
- manage separately governed rollback, and
- inspect customer-safe audit and system-health information.

## Phase 1 — High-Fidelity Prototype

Phase 1 translated the Lab 28 design into a high-fidelity interactive portal prototype.

The implementation established the dark technician visual system, persistent active-organization context, command-center layout, incident workspace, structured Copilot panel, governed action presentation, audit views, responsive behavior, and accessible interaction states.

## Phase 2 — Bounded Backend Integration

Phase 2 connected the portal to bounded backend workflows while keeping the server authoritative.

The integration added authenticated technician identity, tenant-aware incident retrieval, server-controlled organization switching, stale-context protection, cross-tenant access refusal, customer-safe report projection, lifecycle display, audit projection, and system-health information.

Changing the visible customer in the browser does not grant access. The server validates the technician's current authority and organization scope for each protected operation.

## Phase 3 — AI Copilot Advisory

Phase 3 added a structured AI Copilot advisory experience inside the Incident Workspace.

The advisory panel presents provenance, categorical confidence, supporting context, conflicting-evidence states, insufficient-evidence states, and bounded recommendations. It remains visually distinct from authoritative evidence and deterministic system decisions.

The Copilot is not a command surface. It cannot approve or execute an action, claim independent verification, declare resolution, or close an incident.

## Phase 4 — Governed Response Action

Phase 4 implemented the technician-facing proposal and approval flow for a governed Response Action.

The portal shows the active organization, exact intended target and scope, action status, approval boundary, execution readiness, verification state, rollback state, and audit history. Human approval remains explicit before a consequential action can proceed.

The interface presents a fixed supported capability. It does not turn advisory text or technician-entered prose into an arbitrary executable command.

## Phase 5 — Integrated Defensive Action

Phase 5 validated the first integrated Portal-controlled defensive action in an authorized isolated lab environment.

A pre-authorized Windows lab endpoint was used for one fixed defensive configuration change. The workflow demonstrated:

```text
Human Approval
      ↓
Controlled Dispatch
      ↓
Independent Verification
      ↓
Resolution Eligibility
      ↓
Separate Rollback Approval
      ↓
Controlled Restoration
      ↓
Independent Final-State Verification
```

Exactly one forward dispatch and exactly one rollback dispatch occurred. No duplicate endpoint mutation occurred, the incident was not automatically closed, and the final safe state was restored.

No exact rule name, VM identifier, action identifier, approval identifier, attempt identifier, credential, command text, or private runtime artifact is published.

## Live Validation Summary

The sanitized live demonstration confirmed:

- a pre-authorized Windows test endpoint in an isolated environment,
- authoritative target verification,
- server-authoritative organization context,
- explicit human approval,
- deterministic permission before execution,
- durable execution coordination,
- exactly one forward dispatch,
- independent confirmation of the intended change,
- resolution eligibility without automatic closure,
- separate approval for rollback,
- exactly one rollback dispatch,
- independent confirmation of restoration,
- no automatic retry or redispatch, and
- restoration of the final safe state.

The demonstration proved one tightly controlled capability. It does not imply broad remediation coverage for arbitrary SIEM alerts.

## Independent Verification

The executor's return value did not determine the final result. Independent observation confirmed whether the intended state change occurred.

Only the independently verified outcome supported resolution eligibility. The incident remained open until a separately authorized human closure decision; Lab 29 did not convert verification into automatic closure.

## Rollback Validation

Rollback remained a separate consequential operation. It required its own governed approval and controlled dispatch.

After one rollback dispatch, independent observation confirmed that the original safe state was restored. Rollback did not erase the forward action or its evidence; both operations remained visible in lifecycle and audit history.

## Audit-History Improvement

During validation, the underlying action lifecycle was correct, but some customer-safe audit labels were too generic.

The projection was refined so new activity distinguishes concepts such as:

- proposed,
- approved,
- execution requested,
- execution completed,
- independently verified,
- rollback approved,
- rollback requested,
- rollback completed, and
- rollback independently verified.

This was a presentation and audit-clarity correction, not an execution-safety defect. The authoritative action lifecycle did not change.

## CI Regression Lesson

A historical regression test from an earlier portal phase assumed that the Technician Portal had no rollback surface. Later approved phases intentionally introduced governed rollback.

The stale test was updated to preserve the enduring invariant:

> **No arbitrary or ungoverned consequential action.**

The correction aligned the historical expectation with the approved architecture without weakening action governance. The final CI run then passed.

## Security Boundaries

- Technician access requires authenticated identity.
- Organization context is enforced by the server.
- Stale tenant context is rejected.
- Cross-tenant access fails closed.
- AI content remains advisory and carries provenance.
- Conflicting and insufficient evidence remain explicit states.
- Actions require governed preparation and human approval.
- Only a fixed supported capability was demonstrated.
- Arbitrary command execution is not exposed.
- Execution and independent verification remain separate.
- Resolution eligibility does not automatically close an incident.
- Rollback is separately approved and governed.
- No automatic retry or duplicate mutation is permitted.
- Audit history preserves the meaningful action lifecycle.

## Testing and Validation

Public-safe validation confirms:

- focused Lab 29 validation passed,
- earlier Lab 26 and Lab 27 behavior remained intact,
- tenant-isolation tests passed,
- action-idempotency tests passed,
- rollback-governance tests passed,
- audit-projection tests passed,
- customer-safe filtering passed, and
- final CI completed successfully.

The final private CI checkpoint recorded:

- **1,014/1,014 discovered Business Guardian tests passed**, and
- **the Lab 27 workflow pytest step passed**.

These accepted results were recorded for portfolio publication. Private tests were not rerun from this public repository.

## Lessons Learned

- Multi-customer technician workflows need persistent, server-authoritative organization context.
- Advisory AI is most useful when provenance, confidence, and uncertainty remain visible.
- Fixed capabilities and governed transitions are safer than command-oriented controls.
- Independent verification must remain separate from executor success.
- Rollback needs the same explicit governance as the forward operation.
- Customer-safe audit language matters even when the underlying lifecycle is correct.
- Historical tests should preserve enduring safety invariants rather than obsolete interface assumptions.

## Skills Demonstrated

- Security-product frontend implementation
- Bounded backend integration
- Multi-tenant authorization design
- Stale-context and cross-tenant protection
- Human-in-the-loop action governance
- AI advisory-boundary implementation
- Independent-verification workflows
- Governed rollback design
- Idempotency and duplicate-action prevention
- Customer-safe audit projection
- CI diagnosis and regression maintenance
- Accessible, responsive interface implementation

## Public / Private Boundary

This public lab documents portfolio-safe capabilities, architecture boundaries, validation outcomes, and engineering lessons.

It includes no proprietary source code, private repository paths, exploitable API detail, exact internal schemas, credentials, secrets, local paths, live identifiers, raw action or approval IDs, proof-gate internals, command implementation, capability digests, production infrastructure details, customer information, or private acceptance matrices.

## Outcome and Next Step

Lab 29 completed and validated the Technician Portal MVP designed in Lab 28.

The next lab has not started and is not published by this task. Any future work should continue to preserve server-authoritative organization scope, human approval, fixed capabilities, deterministic execution controls, independent verification, separately governed rollback, and explicit incident closure.
