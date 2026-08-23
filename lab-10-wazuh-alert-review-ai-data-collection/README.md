# Lab 10 — Wazuh Alert Review and Security Data Collection

## Can I Follow One Security Event From the Endpoint All the Way to the Alert?

By the end of Lab 09, the Windows workstation was connected to Wazuh and reporting telemetry successfully.

But an active agent does not prove that the entire monitoring workflow is useful.

Lab 10 asks a more practical question:

**Can I create a controlled Windows event, watch Wazuh detect it, inspect the resulting alert, and extract the evidence needed for later automation?**

This lab validates the first complete event-to-alert workflow in the Project Athenaeum Business Guardian environment.

The progression becomes:

```text
Windows Test Event
        ↓
Windows Event Log
        ↓
Wazuh Agent
        ↓
Wazuh Manager
        ↓
Detection Rule
        ↓
Wazuh Alert
        ↓
Alert Review
        ↓
Structured JSON Evidence
        ↓
Sanitized Security Data Sample
```

This is where the monitoring environment begins producing data that can be used by custom security tooling.

---

# What Lab 10 Proves

A monitored endpoint is only useful if its activity can be detected and understood.

Lab 10 validates that:

- A controlled Windows event can be generated
- Windows records the event
- The Wazuh agent collects it
- The Wazuh server processes it
- A corresponding alert appears in the dashboard
- The alert contains useful investigation fields
- The underlying JSON can be examined
- Useful fields can be separated from unnecessary data
- A sanitized dataset can be prepared for later Python processing

The important transition is:

```text
Monitoring
    ↓
Detection
    ↓
Evidence
    ↓
Usable Security Data
```

---

# Lab Environment

The workflow uses the isolated `BusinessGuardianLab` environment.

## Windows Workstation

```text
BusinessGuardian-Win11-Workstation
192.168.70.10/24
```

## Wazuh Monitoring Server

```text
192.168.70.20/24
```

## Internal Network

```text
BusinessGuardianLab
192.168.70.0/24
```

The workstation and monitoring server communicate through the isolated VirtualBox internal network.

No production environment is involved.

---

# Starting From a Known-Good Monitoring State

Before creating the test event, the Wazuh environment was checked to confirm that the Windows endpoint agent was active.

That matters because if an alert fails to appear later, the troubleshooting process needs to distinguish between:

```text
Event Generation Problem
        vs.
Agent Communication Problem
        vs.
Detection Problem
```

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_02_agent-active-starting-state.png"
    alt="Wazuh Windows agent active before Lab 10 event generation"
    width="900">
</p>

<p align="center">
  <em>The Windows endpoint agent was confirmed active before controlled event generation began.</em>
</p>

---

# Creating a Controlled Windows Event

A safe Windows event was created on the authorized Business Guardian workstation.

The purpose was not to simulate a destructive attack.

The goal was to create known activity that could be followed through the complete monitoring pipeline.

The test needed to confirm:

- Windows recorded the event
- The Wazuh agent collected it
- The Wazuh manager processed it
- A detection rule matched
- The alert became visible
- The alert contained usable investigation data

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_03_safe-windows-events-created.png"
    alt="Controlled Windows events generated during Lab 10"
    width="900">
</p>

<p align="center">
  <em>Controlled Windows activity provided a known event that could be traced through the monitoring pipeline.</em>
</p>

---

# The Alert Appears in Wazuh

After the event was generated, the Wazuh dashboard was reviewed for new activity from the monitored workstation.

The simulated Windows error appeared successfully.

That confirmed the complete path:

```text
Windows Endpoint
      ↓
Wazuh Agent
      ↓
Wazuh Manager
      ↓
Detection Rule
      ↓
Dashboard Alert
```

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_04_wazuh-simulated-windows-error-alert-visible.png"
    alt="Simulated Windows error alert visible in Wazuh"
    width="900">
</p>

<p align="center">
  <em>The controlled Windows event successfully reached Wazuh and produced a visible security alert.</em>
</p>

This was the first validated end-to-end alert workflow in the Business Guardian lab.

---

# Reviewing the Alert Like an Analyst

Finding the alert is only the beginning.

The next step is understanding what evidence the alert actually contains.

The alert details were reviewed for information such as:

- Timestamp
- Agent name
- Agent address
- Rule ID
- Rule description
- Alert severity
- Windows event information
- Event source
- Host information
- Supporting event data

These fields help answer basic investigation questions:

```text
What happened?
Where did it happen?
When did it happen?
Why did the platform alert?
How important might it be?
What should be reviewed next?
```

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_05a_windows-error-alert-details-top.png"
    alt="Lab 10 Wazuh alert overview"
    width="900">
</p>

<p align="center">
  <em>The alert overview provides timestamp, endpoint, severity, description, and supporting event context.</em>
</p>

---

# Looking at the Detection Rule

The Wazuh rule fields were also inspected.

These fields help explain why Wazuh considered the event important enough to generate an alert.

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_05b_windows-error-alert-details-rule-fields.png"
    alt="Lab 10 Wazuh alert rule fields"
    width="900">
</p>

<p align="center">
  <em>Rule details provide structured detection context that can later support triage and automation.</em>
</p>

---

# Moving From Dashboard Views to Structured Data

The dashboard is useful for human review.

Software needs something more structured.

The full JSON alert view was examined to understand how Wazuh represents the same event internally.

JSON security data can later be:

- Searched
- Filtered
- Parsed with Python
- Compared with other alerts
- Added to incident records
- Used in dashboards
- Fed into controlled analysis workflows
- Used by AI-assisted tooling

This makes the JSON view an important bridge between manual SOC-style review and later automation.

---

# Reviewing the Event Fields

The event portion of the JSON was inspected for useful information such as:

- Endpoint identity
- Timestamp
- Event source
- Windows event fields
- Supporting event context

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_06a_windows-error-alert-json-event-fields.png"
    alt="Lab 10 Wazuh JSON event fields"
    width="900">
</p>

<p align="center">
  <em>Structured event fields provide machine-readable context that later Python tools can process.</em>
</p>

---

# Reviewing the Rule Fields in JSON

The structured rule information was also examined.

These fields are especially useful because they can help later processing understand:

- Which detection matched
- How Wazuh categorized the activity
- The source severity
- The rule description
- Other detection metadata

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_06b_windows-error-alert-json-rule-fields.png"
    alt="Lab 10 Wazuh JSON rule fields"
    width="900">
</p>

<p align="center">
  <em>Structured rule fields become useful inputs for later normalization, severity handling, and analyst explanation.</em>
</p>

---

# Not Every Field Needs to Be Kept

A raw security alert can contain far more information than a small analysis tool needs.

Instead of copying the entire Wazuh alert into the next project, Lab 10 identifies a smaller set of useful fields.

The goal is to preserve enough evidence to answer questions such as:

- Which endpoint produced the event?
- Which Windows event occurred?
- Which Wazuh rule matched?
- What severity did the source provide?
- What message describes the activity?
- What evidence should an analyst examine?

Unnecessary, repetitive, or sensitive information was excluded before publication.

---

# Creating the Sanitized Security Data Sample

Selected fields from the Wazuh alert were converted into a smaller sanitized data sample.

That file becomes the input for later Python development.

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_07_ai-data-sample-file-created.png"
    alt="Lab 10 sanitized alert data sample"
    width="850">
</p>

<p align="center">
  <em>Selected alert evidence was reduced to a sanitized dataset suitable for later security-tool development.</em>
</p>

The progression is now:

```text
Raw Wazuh Alert
       ↓
Review Relevant Evidence
       ↓
Remove Unnecessary or Sensitive Data
       ↓
Sanitized Alert Sample
       ↓
Python Processing
```

At this stage, the sample is only a building block.

No claim is made that it is a complete automated security product.

---

# Why Clean Security Data Matters

Security tools often produce a large amount of information.

More data is not automatically better.

An analyst still needs to determine:

1. What happened?
2. Which system was involved?
3. Which evidence is important?
4. Which information is noise?
5. How serious might the activity be?
6. What should be reviewed next?

This lab reinforced an important design principle for later Business Guardian development:

> **Automation should begin with understandable, validated security data—not blindly consume everything available.**

That principle becomes increasingly important once Python, normalization, triage, and later investigation logic are introduced.

---

# Preserving the Validated Environment

After the monitoring and data-collection workflow was successfully validated, recovery snapshots were created.

## Wazuh Server Snapshot

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_08a_wazuh-server-alert-data-snapshot.png"
    alt="Lab 10 Wazuh server recovery snapshot"
    width="850">
</p>

## Windows Workstation Snapshot

<p align="center">
  <img
    src="screenshots/2026-07-24_Lab10_WazuhAI_08b_windows-events-created-snapshot.png"
    alt="Lab 10 Windows workstation recovery snapshot"
    width="850">
</p>

These snapshots preserve the environment after successful event generation, collection, review, and data preparation.

---

# Complete Workflow Validation

Lab 10 successfully demonstrated:

```text
Controlled Windows Event
        ↓
Event Recorded Locally
        ↓
Collected by Wazuh Agent
        ↓
Processed by Wazuh Manager
        ↓
Detection Rule Matched
        ↓
Alert Displayed
        ↓
Alert Evidence Reviewed
        ↓
JSON Examined
        ↓
Useful Fields Identified
        ↓
Sanitized Dataset Created
```

## Validation Status

| Validation Area | Result |
| --- | --- |
| Windows event generation | **PASS** |
| Endpoint event recording | **PASS** |
| Wazuh agent collection | **PASS** |
| Wazuh server processing | **PASS** |
| Alert detection | **PASS** |
| Dashboard alert review | **PASS** |
| JSON field review | **PASS** |
| Relevant-field identification | **PASS** |
| Sanitized data preparation | **PASS** |
| Recovery snapshots created | **PASS** |

---

# Security and Privacy

All work was completed using personally owned and authorized virtual systems.

The lab followed several safeguards:

- Systems remained on the isolated `BusinessGuardianLab` network
- No Bridged Adapter was used
- No production systems were tested
- No employer systems were tested
- No school systems were tested
- No customer systems were tested
- No real financial data was used
- The Windows event was controlled and non-destructive
- Alert information was reviewed before publication
- Passwords and credentials were excluded
- Personal information was excluded
- Unnecessary system information was removed
- The sanitized data sample was reviewed before publication

---

# What Lab 10 Proves

Lab 10 demonstrates that the Business Guardian lab can do more than show an active Wazuh agent.

It can follow a known event through the complete monitoring path and inspect the evidence produced at every stage.

The lab connects:

- Windows event generation
- Endpoint telemetry
- Wazuh collection
- SIEM detection
- Alert review
- JSON analysis
- Evidence selection
- Data sanitization
- Future automation

Most importantly:

> **The project now has verified security data that custom software can begin working with.**

That changes the direction of Project Athenaeum.

Up to this point, the primary focus was building and validating infrastructure.

After Lab 10, the project begins building software on top of the security data that infrastructure produces.

---

# Skills Demonstrated

- Windows event generation
- Wazuh endpoint monitoring
- SIEM alert review
- Security-event validation
- Windows telemetry analysis
- JSON review
- Detection-rule analysis
- Security-field identification
- Evidence collection
- Data sanitization
- Dataset preparation
- SOC-style investigation
- Technical troubleshooting
- Snapshot and recovery management
- Technical documentation

---

# Where the Project Goes From Here

Lab 09 answered:

**Can the Windows endpoint reliably report telemetry to Wazuh inside the isolated environment?**

Lab 10 answered:

**Can I generate a controlled event, follow it through Wazuh, inspect the evidence, and prepare that evidence for automation?**

The answer was yes.

That creates the next question:

**Can I write software that takes this security data and explains it more clearly?**

[Lab 11 — AI Alert Explainer MVP](../lab-11-ai-alert-explainer-mvp/README.md) uses the sanitized alert sample created here as input for the first custom Python security-analysis tool in Project Athenaeum.

The progression becomes:

```text
Endpoint Monitoring
       ↓
Alert Detection
       ↓
Evidence Review
       ↓
Sanitized Security Data
       ↓
Python Processing
       ↓
Analyst-Oriented Explanation
```

Lab 10 is the bridge between **monitoring security events** and **building software that can work with them**.
