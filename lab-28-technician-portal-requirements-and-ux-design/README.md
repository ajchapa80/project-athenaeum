# Lab 28 — Technician Portal Requirements & UX Design

## Result

**PASS — TECHNICIAN PORTAL REQUIREMENTS AND UX DESIGN COMPLETED, FROZEN, AND VISUALLY VALIDATED**

Lab 28 defined the technician-facing experience for Business Guardian: a multi-customer operational workspace that helps an authorized technician understand incidents, review evidence, use structured AI assistance, prepare governed response actions, inspect audit history, and maintain customer context throughout consequential workflows.

The design follows two principles:

> **Instrument panel, not dashboard.**

> **Cybersecurity aesthetic without cybersecurity clutter.**

Lab 28 is a requirements and UX-design milestone. The design was frozen before implementation and its visual direction was later validated through Lab 29. This public lab does not publish Lab 29 implementation details.

## Objective

Design a clear, high-trust Technician Portal for authorized service-provider workflows while preserving organization isolation, least privilege, explicit human authority, evidence integrity, and the established separation between proposal, approval, execution, independent verification, rollback, resolution eligibility, and closure.

## Why the Technician Portal Is Separate

The customer Dashboard answers questions about one organization's security posture and incidents. The Technician Portal serves a different role: it must help an authorized technician work across assigned customers while continuously showing which customer is active and what authority applies.

Separating the experiences supports different information density, navigation, permissions, and operational responsibilities. It also prevents technician concepts from being presented as ordinary customer capabilities.

The Technician Portal is not a hidden administrative back door. Customer scope, technician authority, and consequential actions remain explicit and reviewable.

## Design Goals

- Keep the active customer visible throughout the workflow.
- Present evidence and human findings before advisory interpretation.
- Support focused technician work without turning the interface into a dense SIEM console.
- Keep AI assistance structured and advisory rather than chat-first or authoritative.
- Preserve human approval around consequential response actions.
- Make status, uncertainty, ownership, and next steps easy to distinguish.
- Repeat customer context near every consequential confirmation.
- Support keyboard use, visible focus, readable contrast, and clear semantic status.
- Reuse consistent components and tokens across desktop and narrower layouts.

## UX Architecture

The frozen architecture defined **19 major screen contracts**, **37 reusable components**, **50 deterministic UX and design acceptance cases**, **17 Lab 29 entry-gate conditions**, and **8 core technician journeys**.

The portal organizes work around persistent customer context and task-oriented areas rather than a single wall of security metrics. At a public-safe level, the architecture covers:

- technician overview and assigned-customer context,
- customer switching,
- customer and environment detail,
- incident queues and incident workspaces,
- structured evidence review,
- AI Copilot advisory content,
- governed response-action preparation,
- approvals and action progress,
- verification and rollback visibility,
- audit and lifecycle history,
- fleet and update concepts, and
- technician settings and accessibility behavior.

## Major Screen Concepts

The design treats each screen as an instrument for a specific decision:

- **Overview** highlights assigned work, urgent conditions, and customer context.
- **Customer workspace** presents the selected customer's incidents, Assets, sources, and operational state.
- **Incident queue** supports prioritization without collapsing severity, evidence quality, and workflow state into one signal.
- **Incident Workspace** combines authoritative evidence, human findings, advisory analysis, action history, and controlled next steps.
- **Response Action review** explains the exact target, scope, expected change, approval state, verification plan, and rollback readiness.
- **Audit History** preserves a readable sequence of security-relevant activity.
- **Fleet and update views** describe operational concepts at a high level without claiming unrestricted endpoint administration.

## Active-Customer Context

A persistent active-customer control anchors the technician experience. Customer identity is repeated in page headings, navigation context, incident views, and consequential confirmation surfaces.

Switching customers is an explicit context change. The interface must not carry a selection, approval, proposed action, or evidence interpretation silently from one customer to another.

Before a consequential action proceeds, the technician sees the customer context again alongside the exact target and proposed scope. This supports organization isolation and reduces wrong-customer errors.

## Incident Workspace

The central Incident Workspace uses an **evidence-left / AI-right** concept.

The evidence side presents authoritative and human-recorded information: source evidence, investigation history, findings, lifecycle state, approvals, execution records, independent verification, rollback, and closure context.

The AI side presents structured advisory assistance: summaries, relevant context, questions to consider, and recommended next steps. Advisory content remains visually and semantically distinct from authoritative evidence and deterministic decisions.

The workspace is designed to help a technician understand the complete incident without allowing narrative convenience to rewrite the underlying record.

## AI Copilot Advisory Design

The Copilot is structured, not chat-first. It organizes assistance around the current incident and offers bounded explanations and recommendations rather than an open command surface.

Violet is reserved for AI advisory content so technicians can distinguish it from evidence, system state, approvals, and action controls.

The Copilot has no **AI Execute** button. It cannot grant itself authority, approve an action, bypass policy, select an arbitrary command, independently verify an outcome, or close an incident.

## Response Action Presentation

The portal presents response work as a governed sequence:

```text
Evidence and Findings
        ↓
Proposed Response
        ↓
Prepare Action
        ↓
Send for Approval
        ↓
Human Approval
        ↓
Controlled Execution
        ↓
Independent Verification
        ↓
Rollback When Separately Authorized
        ↓
Resolution Eligibility
        ↓
Human Closure
```

The concepts **Prepare Action** and **Send for Approval** communicate that a technician proposal is not execution authority.

Customer context, target, action scope, expected change, risk, verification plan, rollback implications, and approval state remain visible around consequential steps.

## Audit-History Design

Audit History emphasizes who acted, which customer and incident were involved, what lifecycle stage changed, and whether an operation was proposed, approved, executed, verified, rolled back, corrected, reopened, or closed.

The design favors chronological, append-oriented history. Later success does not erase earlier uncertainty or failure, and correction does not rewrite the original record.

## Fleet and Update Concepts

Fleet and update concepts support a future technician view of assigned customer environments and software readiness. They are presented at a high level and do not imply remote shell access, unrestricted administration, automatic remediation, or completed production deployment controls.

## Visual System

The Technician Portal is darker than the customer Dashboard. Deep Chapa navy and near-black surfaces form the operational canvas; teal and cyan carry Chapa Technology Solutions identity; signal blue marks technician interaction; violet identifies AI advisory content; and semantic colors communicate status.

Public-safe design tokens include:

| Role | Token | Value | Meaning |
|---|---|---:|---|
| Canvas | `portal-canvas` | `#040D18` | Deep workspace background |
| Surface | `portal-950` | `#06172C` | Primary dark surface |
| Surface | `portal-900` | `#0A1930` | Raised content surface |
| Surface | `portal-800` | `#12304F` | Interactive or grouped surface |
| Border | `portal-border` | `#24425F` | Standard separation |
| Strong border | `portal-border-strong` | `#647D98` | Emphasized boundaries |
| Primary text | `text-primary` | `#E8EDF4` | Main readable content |
| Muted text | `text-muted` | `#93A2B8` | Supporting information |
| Brand | `chapa-teal` | `#0B8F7D` | Primary Chapa identity |
| Brand depth | `chapa-teal-deep` | `#017666` | Strong brand surface |
| Highlight | `cyan-highlight` | `#2FD9C5` | Active identity accent |
| Interaction | `signal-500` | `#3D8BFF` | Primary technician action |
| Interaction | `signal-300` | `#8FC1FF` | Secondary interaction state |
| Success | `success` | `#3FB950` | Positive confirmed state |
| Warning | `warning` | `#D9A93B` | Attention or caution |
| Danger | `danger` | `#E5534B` | Failure or destructive risk |
| Unknown | `unknown` | `#8993A6` | Unavailable or unresolved state |
| Advisory | `advisory` | `#9A8FE8` | AI-generated advisory content |
| Focus | `focus` | `#F2C465` | Keyboard focus visibility |

Color is never the only carrier of meaning. Labels, icons, state text, and layout reinforce every semantic status.

## Accessibility and Readability

The design uses high-contrast text, visible keyboard focus, predictable navigation, descriptive labels, sufficient target sizes, and redundant status cues.

Progressive disclosure keeps primary decisions readable while allowing technical evidence to remain available. Dense information is grouped by task and hierarchy instead of compressed into undifferentiated tables.

Confirmation language states what will happen, which customer and target are affected, and what authority is required. Destructive or consequential actions do not rely on color alone.

## Safety and Human Authority

- AI advice remains visually and functionally separate from authoritative evidence.
- AI cannot execute, approve, verify, roll back, or close an incident.
- Technician proposals do not equal approval.
- Approval does not equal execution.
- Execution does not equal independent verification.
- Verification does not automatically equal resolution eligibility or closure.
- Rollback remains a separately governed consequential operation.
- Customer context is repeated around consequential actions.
- No arbitrary command surface is included.
- Human authority remains explicit at approval and closure boundaries.

## Validation Outcome

The frozen design produced:

- 19/19 major screen contracts completed,
- 37/37 reusable component definitions completed,
- 50/50 deterministic UX and design acceptance cases passed,
- 17/17 Lab 29 entry-gate conditions satisfied, and
- 8/8 core technician journeys defined.

The Technician Portal design was later visually validated through Lab 29. Lab 28 publication records the approved design baseline and does not publish Lab 29 as part of this task.

## Transition to Lab 29

Lab 28 supplied the frozen requirements, visual system, component strategy, safety boundaries, and entry gate for Lab 29's Technician Portal implementation and visual validation.

This transition preserved the rule that implementation follows an approved design rather than redefining safety and authority boundaries during construction.

## Lessons Learned

- Multi-customer security work requires persistent, repeated customer context.
- Technician efficiency improves when evidence and advisory help are adjacent but visibly distinct.
- Structured advisory assistance is safer and clearer than a command-oriented chat surface.
- Consequential operations need exact customer, target, scope, approval, and verification context at the decision point.
- A darker technical interface still needs restraint, hierarchy, and accessible semantic cues.
- Freezing components and acceptance cases before implementation reduces ambiguity during visual validation.

## Skills Demonstrated

- Security-product UX architecture
- Multi-customer information architecture
- Human-in-the-loop workflow design
- Least-privilege interaction design
- AI advisory-boundary design
- Incident-workspace design
- Governed response-action presentation
- Audit and history visualization
- Accessibility and semantic color design
- Design-system and token strategy
- Responsive component planning
- Deterministic UX acceptance design

## Public / Private Boundary

This public lab documents portfolio-safe goals, UX structure, visual language, quantitative design evidence, and human-authority boundaries.

It contains no proprietary source code, private APIs, exact backend contracts, credentials, secrets, private repository paths, live tenant data, sensitive identifiers, production infrastructure details, or exploitable implementation controls.
