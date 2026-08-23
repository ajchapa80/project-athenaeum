# Project Athenaeum

## Building Cybersecurity Skills Into a Working Security Platform

Project Athenaeum started as a place to document hands-on cybersecurity and IT labs.

It has grown into something much more interesting.

What began with VirtualBox, Linux, Windows administration, networking, and basic security testing has progressed into endpoint monitoring, Wazuh alert collection, Python-based security tooling, structured alert records, traceability, and deterministic cybersecurity triage.

The project now follows a clear technical progression:

```text
Build the Environment
        ↓
Monitor the Endpoint
        ↓
Generate Security Events
        ↓
Collect and Normalize Alerts
        ↓
Validate the Data
        ↓
Preserve Identity and Traceability
        ↓
Triage the Condition
        ↓
Decide What Should Happen Next
```

Every major step is built, tested, documented, and preserved before the next layer is added.

**Nothing gets built twice.**

---

## What This Project Demonstrates

Project Athenaeum is my hands-on cybersecurity and information technology portfolio.

The goal is not simply to complete labs. The goal is to demonstrate how I approach technical problems:

- Build controlled environments
- Understand what the systems are actually doing
- Troubleshoot failures
- Work with real security data
- Write tools to process that data
- Define expected behavior before trusting the result
- Test normal and failure conditions
- Preserve evidence and traceability
- Document what worked, what failed, and what changed
- Extend validated work instead of constantly starting over

The repository includes working scripts, sanitized security data, screenshots, validation evidence, design documentation, technical writeups, and the history of the project as it has become more advanced.

Only sanitized, portfolio-appropriate material is published here.

---

## Current Focus

The project currently sits at the intersection of security operations, software development, and practical defensive cybersecurity.

Current areas include:

- Security operations and alert investigation
- SIEM and endpoint telemetry
- Wazuh monitoring
- Windows and Linux administration
- Networking and vulnerability assessment
- Python security automation
- Vendor-neutral security-data processing
- Missing and malformed-data handling
- Multiple-alert processing
- Structured alert records
- Source-to-record traceability
- Deterministic cybersecurity triage
- Evidence-quality-first decision logic
- Investigation and policy-evaluation routing
- Testing, repeatability, and failure isolation
- Human-controlled consequential security decisions

---

# Completed Labs

## Foundation

### [Lab 01: Documentation Setup](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-01-documentation-setup/README.md)

Before building technical labs, I created the documentation system that would support everything afterward.

Lab 01 established the folder structure, screenshot naming system, documentation templates, and portfolio workflow used throughout Project Athenaeum.

---

### [Lab 02: VirtualBox CyberLab](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-02-virtualbox-cyberlab/README.md)

Built the first isolated cybersecurity environment using Kali Linux and Metasploitable 2.

Both systems were configured with persistent addresses on the private `CyberLab` network and validated with successful bidirectional connectivity.

This became the safe environment for later networking and security testing.

---

### [Lab 03: Linux Fundamentals](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-03-linux-fundamentals/README.md)

Worked through practical Linux administration from the command line.

The lab covered navigation, file management, permissions, searching, process monitoring, background processes, file removal, and troubleshooting package updates inside the isolated environment.

---

### [Lab 04: Windows Fundamentals](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-04-windows-fundamentals/README.md)

Moved the project into Windows administration and troubleshooting.

The lab explored System Information, Task Manager, Event Viewer, Windows Security, PowerShell, networking, firewall configuration, device health, and Windows Update.

---

## Security Testing and Networking

### [Lab 05: DVWA Web Security](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-05-dvwa-web-security/README.md)

Used DVWA inside the isolated lab to perform authorized web-security testing.

The lab explored command injection and SQL injection, compared different application security levels, and documented both offensive observations and defensive recommendations.

---

### [Lab 06: Nmap Networking Basics](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-06-nmap-networking-basics/README.md)

Used Nmap to answer a basic but important security question:

**What is actually reachable on the network?**

The lab covered host discovery, service and version detection, targeted port scanning, operating-system detection, aggressive scanning, and saved scan results against an authorized vulnerable target.

---

# Building the Business Guardian Lab

### [Lab 07: BusinessGuardianLab Network Setup](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-07-businessguardianlab-network-setup/README.md)

Created a second isolated environment designed around a small-business security scenario.

The Windows 11 workstation was placed on the private `BusinessGuardianLab` network, isolated from the internet, given a persistent address, tested, and preserved with a recovery snapshot.

This became the foundation for the Wazuh monitoring environment.

---

### [Lab 08: Wazuh Monitoring Server Setup](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-08-wazuh-monitoring-server-setup/README.md)

Deployed a centralized Wazuh monitoring server.

The server was configured with separate NAT and isolated-network interfaces, persistent addressing, validated Wazuh services, and local dashboard access through VirtualBox port forwarding.

At this point, Project Athenaeum moved from individual system exercises into an actual monitored security environment.

---

### [Lab 09: Wazuh Windows Agent Deployment](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-09-wazuh-windows-agent-deployment/README.md)

Connected the Windows workstation to Wazuh.

The agent was installed, configured, troubleshot, registered with the monitoring server, and validated after temporary internet access was removed.

The result was a fully isolated Windows endpoint reporting security telemetry to a centralized monitoring server.

---

### [Lab 10: Wazuh Alert Review and AI Data Collection](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-10-wazuh-alert-review-ai-data-collection/README.md)

The monitoring environment was working. The next question was:

**What can I do with the security data it produces?**

Lab 10 generated controlled Windows events, confirmed end-to-end Wazuh detection, examined alert details and structured JSON fields, and created sanitized security data for later Python processing.

That data became the bridge between the monitoring labs and the software-development phase of Project Athenaeum.

---

# From Alerts to Security Tooling

### [Lab 11: AI Alert Explainer MVP](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-11-ai-alert-explainer-mvp/README.md)

Built the first working Python security tool in Project Athenaeum.

The MVP reads sanitized Wazuh alert data, extracts important endpoint and rule information, interprets severity using deterministic logic, and produces analyst-oriented context and review steps.

The design deliberately keeps human verification between an alert and a security conclusion.

---

### [Lab 12: AI Alert Explainer Testing and Validation](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-12-ai-alert-explainer-testing-validation/README.md)

A tool working once was not enough.

Lab 12 tested the Lab 11 MVP against:

- Normal execution
- Output-file creation
- Missing files
- Empty files
- Missing fields
- Severity changes
- Restoration to the validated baseline

This lab established a rule that continues through the project:

**A feature is not treated as stable until its failure behavior is understood too.**

---

### [Lab 13: AI Alert Explainer v2 Requirements and Design](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-13-ai-alert-explainer-v2-requirements-design/README.md)

Instead of immediately writing more code, Lab 13 stopped and designed the next version first.

The design introduced:

- A vendor-neutral alert model
- Wazuh-to-normalized field mapping
- Platform-neutral severity
- Missing and malformed-data handling
- Multiple-alert processing
- Per-alert failure isolation
- Individual reports
- Batch summaries
- Five deterministic acceptance cases

The implementation target for Lab 14 was frozen before coding began.

---

### [Lab 14: AI Alert Explainer v2 Multiple Alert Processing](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-14-ai-alert-explainer-v2-multiple-alert-processing/README.md)

Security tools do not get to assume that every input will be clean.

Lab 14 moved from processing a single alert to handling a batch containing good data, incomplete data, malformed data, and unsupported content.

The processor:

- Discovered multiple alert files
- Normalized vendor-specific data
- Preserved source information
- Identified missing and malformed fields
- Isolated failures
- Generated individual reports
- Produced a batch summary
- Protected previous output from overwrite

The predetermined validation target was:

```text
5 discovered
2 processed normally
2 processed with warnings
1 failed validation
4 reports created
1 batch summary
```

The implementation matched that target exactly.

A second run reproduced the result without overwriting the first.

**Validation: PASS**

---

# Private Business Guardian Milestone

## Live Wazuh Evidence Validation

At this stage, some Business Guardian development moved into a separate private repository.

The goal was no longer just to process sanitized examples. I wanted to know whether the architecture could retrieve evidence from the actual lab.

A private read-only Wazuh evidence connector was tested against both the Wazuh Server API and the indexed alert data.

Results:

- Both evidence paths successfully returned live lab security data
- 257 automated tests passed
- A real Wazuh compatibility issue was discovered during live testing
- The issue was corrected and regression-tested
- GitHub Actions passed after the correction
- Final live validation returned `PASS`

The proprietary connector implementation, investigation system, and other product-level Business Guardian components remain private.

Project Athenaeum records only the sanitized milestone.

---

# Creating Persistent Security Records

### [Lab 15 — Alert Records, Validation, and Traceability](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-15-alert-records-validation-traceability/README.md)

Alerts are temporary events. A security workflow needs something more durable.

Lab 15 introduced structured vendor-neutral alert records that can preserve an alert's identity as it moves through later security decisions.

Each processable alert receives a non-sensitive `AR-...` identity while preserving:

- Original source alert ID
- Source event timestamp
- Separate ingestion timestamp
- Normalized severity
- Validation outcome
- Missing fields
- Validation notes
- Processing history
- Source traceability

The same controlled five-alert validation set was used.

Results:

```text
5 discovered
2 processed normally
2 processed with warnings
1 failed validation
4 alert records created
```

Missing data remained missing rather than being invented.

Malformed severity remained preserved while normalized severity safely became `UNKNOWN`.

Unsupported content failed without stopping the other alerts.

A second run reproduced the same results while preserving the first-run output.

**Final validation: PASS**

---

# Deciding What Happens Next

### [Lab 16 — Alert Triage and Decision Logic](https://github.com/ajchapa80/project-athenaeum/blob/main/lab-16-alert-triage-decision-logic/README.md)

Security alerts rarely arrive with perfect information.

Some match conditions we understand. Some are missing evidence. Some look unusual. Others simply do not support a confident conclusion yet.

Lab 16 asked:

**How should a security system decide what happens next without guessing?**

The lab adds a deterministic triage layer after the Lab 15 alert-record stage.

It preserves the original `AR-...` alert identity and creates a separate `TR-...` triage-decision identity.

Supported classifications are:

- `KNOWN_COMMON`
- `INSUFFICIENT_DATA`
- `UNUSUAL`
- `UNKNOWN`

Supported next-stage routing includes:

- `POLICY_EVALUATION`
- `INVESTIGATION`
- `HUMAN_REVIEW`
- `NO_ACTION_YET`

The controlled validation produced:

```text
5 records processed
2 KNOWN_COMMON
1 INSUFFICIENT_DATA
1 UNUSUAL
1 UNKNOWN

2 POLICY_EVALUATION
3 INVESTIGATION
0 failures
```

A second complete execution reproduced the same classification and routing totals while preserving the original alert identities and generating new triage-decision identities.

**Final validation: PASS**

One of the most important results from this lab is simple:

> A HIGH-severity alert is not automatically malicious, and a LOW-severity alert is not automatically safe.

Severity is evidence. It is not a verdict.

Lab 16 intentionally stops at decision routing. It does not authorize remediation, execute defensive actions, verify fixes, or mark an alert resolved.

---

# Where Project Athenaeum Stands Today

Project Athenaeum is complete through **Lab 16 — Alert Triage and Decision Logic**.

The technical progression now looks like this:

```text
Security Event
      ↓
Collect Alert Data
      ↓
Normalize and Validate
      ↓
Create Persistent Alert Record
      ↓
Preserve Traceability
      ↓
Triage the Condition
      ↓
Route to the Next Security Stage
```

Labs 11–12 established and validated the first alert-processing MVP.

Lab 13 designed the next architecture.

Lab 14 proved deterministic multiple-alert processing.

Lab 15 added persistent alert identity and traceability.

Lab 16 added deterministic triage and decision routing.

Each layer extends the previous validated baseline instead of replacing it.

---

# Next Project Phase

Lab 16 answers:

**What should happen next?**

The next phase will move deeper into the remaining security lifecycle.

Potential areas include:

- Investigation and evidence handling
- Policy and approval records
- Business-risk and impact representation
- Audit-oriented workflow records
- Controlled defensive-action planning
- Verification and outcome tracking
- Customer-facing incident and resolution reporting

The exact next lab will be selected only after comparing the public roadmap with work already completed in the private Business Guardian repository.

That prevents duplicate implementation and keeps the public portfolio aligned with the larger product architecture.

```text
Alert
  ↓
Normalize / Validate
  ↓
Record / Trace
  ↓
Triage
  ↓
Investigate when needed
  ↓
Policy / Approval
  ↓
Authorized Defensive Action
  ↓
Verify
  ↓
Audit
```

**Nothing gets built twice.**

---

# How I Build

Project Athenaeum follows a simple development cycle:

## Build → Test → Validate → Document → Preserve → Extend

That means:

- Validated work is preserved rather than rebuilt unnecessarily.
- Expected behavior is defined before implementation when practical.
- Failure conditions are tested along with successful ones.
- Stable baselines are preserved before adding new capabilities.
- Security-platform-specific data is separated from reusable processing logic.
- Missing information is identified rather than fabricated.
- Alerts, logs, and external security data are treated as untrusted input.
- Technical severity does not automatically determine maliciousness.
- Core security decisions use deterministic, testable logic.
- Consequential security actions remain appropriately human-controlled.
- Nothing is treated as resolved until the result has been verified.

---

# Public vs. Private Development

Project Athenaeum is the public proof-of-work repository.

It may contain:

- Sanitized portfolio labs
- Selected screenshots
- Portfolio-safe Python
- Controlled test data
- High-level architecture
- Testing methodology
- Validation results
- Technical lessons
- Professional-development progress

The private Business Guardian repository contains product-level development such as:

- Security-platform connectors
- Production triage logic
- Evidence orchestration
- Investigation workflows
- Policy and approval systems
- Business-risk logic
- Defensive-action selection and execution
- Verification mechanisms
- Audit systems
- Tenant/customer logic
- Sensitive configuration
- Proprietary architecture
- Commercial material

The goal is to show meaningful technical progress publicly without publishing enough proprietary implementation detail to reproduce the commercial product.

---

# Home Lab

My current lab infrastructure includes:

- Windows 11 host computer
- Oracle VirtualBox
- Kali Linux security workstation
- Ubuntu Linux practice virtual machine
- Metasploitable 2 vulnerable target
- Windows 11 administration workstation
- Wazuh monitoring server
- Active Wazuh Windows endpoint agent
- Isolated `CyberLab` network
- Isolated `BusinessGuardianLab` network
- NAT and internal-network segmentation
- Local Wazuh dashboard access
- Clean recovery snapshots for major deployment stages

All cybersecurity exercises are performed using personally owned or authorized systems inside controlled lab environments.

---

# Skills Demonstrated Across the Project

- Windows and Linux administration
- Virtual network deployment
- Nmap network and service discovery
- Authorized vulnerability testing
- Wazuh endpoint monitoring
- Windows event generation and analysis
- Security alert review
- JSON security-data processing
- Python automation
- Vendor-neutral data normalization
- Multiple-alert processing
- Missing and malformed-data validation
- Failure isolation
- Persistent alert records
- Source traceability
- Deterministic cybersecurity triage
- Evidence-quality-first decision logic
- Severity-independent classification
- Investigation and policy routing
- Automated testing
- Repeatability testing
- Non-destructive processing
- Technical documentation
- Security architecture planning

---

# Education and Development

- Bachelor of Science in Cybersecurity with a concentration in Project Management Fundamentals — degree conferral expected September 2026
- InfoSec Labs Pre-Security Fundamentals Certificate
- InfoSec Labs Alert Investigation Specialist training
- CompTIA Security+ preparation
- Continued SOC, SIEM, endpoint-monitoring, Python, networking, Windows, Linux, and IT support practice

---

# Professional Direction

My immediate goal is to move into an IT support, SOC analyst, cybersecurity support, or public-sector IT role where I can apply practical troubleshooting, documentation, endpoint-monitoring, and security-analysis skills while continuing to grow technically.

Longer term, I want to take on deeper security and systems responsibilities while continuing to build practical cybersecurity tooling and automation.

Project Athenaeum is also helping me explore a larger goal: building cybersecurity technology that can help smaller organizations understand what is happening in their environment, investigate security conditions, and eventually perform supported defensive actions when policy and authorization permit.

The system should not simply say that something was fixed.

It should be able to prove it.
