# Project Athenaeum

Project Athenaeum is my cybersecurity and information technology portfolio. This repository documents hands-on labs, security investigations, system administration exercises, Python security automation, and technical projects developed to demonstrate practical SOC and IT skills.

The project follows a structured progression from foundational system administration and isolated cybersecurity labs into endpoint monitoring, alert investigation, Python-based security tooling, software validation, and requirements-driven security-tool design.

## About This Project

The purpose of Project Athenaeum is to demonstrate practical technical ability through clearly documented, repeatable work.

Each lab documents relevant elements such as:

* Objective and scope
* Environment and tools
* Procedures performed
* Technical evidence
* Testing and validation
* Troubleshooting
* Findings
* Security relevance
* Lessons learned
* Sanitized portfolio evidence

Completed work is preserved as historical evidence. Later improvements extend validated work rather than rewriting earlier labs simply because a newer version becomes available.

## Focus Areas

* Security operations and alert investigation
* SIEM, endpoint telemetry, and log analysis
* Windows and Linux administration
* Networking and traffic analysis
* Vulnerability assessment
* Incident investigation and response
* Python security automation
* Python-based alert explanation
* AI-assisted security-tool design
* Security-data normalization and validation
* Software testing and error handling
* Human-in-the-loop security decision support
* IT troubleshooting and support
* Technical documentation
* Secure tool and dashboard development

## Repository Structure

This repository includes:

* Lab documentation
* Sanitized screenshots
* Security investigation exercises
* Network and architecture diagrams
* Command references
* Python scripts and technical exercises
* Testing and validation evidence
* Portfolio-safe design documentation
* Final portfolio writeups and summaries

Only sanitized, portfolio-appropriate material is published here.

## Completed Labs

### [Lab 01: Documentation Setup](lab-01-documentation-setup/README.md)

Established the folder structure, screenshot naming system, documentation templates, and portfolio workflow used throughout Project Athenaeum.

### [Lab 02: VirtualBox CyberLab](lab-02-virtualbox-cyberlab/README.md)

Built and validated an isolated VirtualBox cybersecurity lab using Kali Linux and Metasploitable 2. Both virtual machines use persistent static IP addresses on the private `CyberLab` internal network, with successful bidirectional connectivity testing and 0% packet loss.

### [Lab 03: Linux Fundamentals](lab-03-linux-fundamentals/README.md)

Practiced and documented essential Linux command-line skills, including navigation, file management, searching, permissions, process monitoring, background process control, file removal, and troubleshooting package updates on an isolated network.

### [Lab 04: Windows Fundamentals](lab-04-windows-fundamentals/README.md)

Reviewed core Windows 11 administration and security tools, including System Information, Task Manager, Event Viewer, Windows Security, PowerShell, network configuration, firewall settings, device health, and Windows Update. The lab includes 18 sanitized evidence screenshots.

### [Lab 05: DVWA Web Security](lab-05-dvwa-web-security/README.md)

Performed authorized web application security testing against DVWA inside the isolated `CyberLab` environment. The lab documents command injection and SQL injection testing, comparisons between Low and High security settings, defensive recommendations, and 12 sanitized evidence screenshots.

### [Lab 06: Nmap Networking Basics](lab-06-nmap-networking-basics/README.md)

Performed authorized Nmap scanning against Metasploitable 2 inside the isolated `CyberLab` environment. The lab documents basic scanning, service and version detection, targeted web, database, and remote-access port scans, operating-system detection, aggressive scanning, saved scan results, and 13 sanitized evidence screenshots.

### [Lab 07: BusinessGuardianLab Network Setup](lab-07-businessguardianlab-network-setup/README.md)

Created and validated an isolated Windows 11 small-business lab environment using the VirtualBox Internal Network `BusinessGuardianLab`. The workstation was isolated from the internet, assigned the persistent static address `192.168.70.10/24`, preserved with a clean recovery snapshot, and documented with 18 sanitized evidence screenshots.

### [Lab 08: Wazuh Monitoring Server Setup](lab-08-wazuh-monitoring-server-setup/README.md)

Deployed and configured a centralized Wazuh monitoring server for the isolated `BusinessGuardianLab` environment. The server uses separate NAT and internal-network adapters, the persistent internal address `192.168.70.20/24`, local dashboard access through VirtualBox port forwarding, validated Wazuh services, and 23 sanitized public evidence screenshots.

### [Lab 09: Wazuh Windows Agent Deployment](lab-09-wazuh-windows-agent-deployment/README.md)

Installed, configured, troubleshot, and validated the Wazuh Windows agent on the isolated Business Guardian workstation. The endpoint successfully registered with the Wazuh server at `192.168.70.20`, remained active after temporary NAT was removed, and was documented with 13 sanitized evidence screenshots.

### [Lab 10: Wazuh Alert Review and AI Data Collection](lab-10-wazuh-alert-review-ai-data-collection/README.md)

Generated safe Windows events, validated end-to-end Wazuh alert detection, reviewed alert details and structured JSON fields, and created a sanitized data sample for later Python-based alert processing. The lab includes 11 cropped evidence screenshots documenting the event-to-alert workflow.

### [Lab 11: AI Alert Explainer MVP](lab-11-ai-alert-explainer-mvp/README.md)

Built a functional Python-based alert explanation MVP using sanitized Wazuh data prepared during Lab 10. The tool extracts selected endpoint, Windows event, and Wazuh rule fields; interprets alert severity using deterministic logic; generates analyst context and review steps; and preserves human verification before any security decision.

The published lab includes the working Python script, sanitized input sample, generated output, and nine evidence screenshots.

### [Lab 12: AI Alert Explainer Testing and Validation](lab-12-ai-alert-explainer-testing-validation/README.md)

Tested and validated the Lab 11 AI Alert Explainer MVP while preserving the published version as a stable baseline.

Validation covered:

* Normal execution
* Output-file creation
* Missing input-file handling
* Empty input-file handling
* Missing-field behavior
* Severity-logic changes
* Final restoration to the original baseline

The published lab includes copied working files and 17 sanitized evidence screenshots.

### [Lab 13: AI Alert Explainer v2 Requirements and Design](lab-13-ai-alert-explainer-v2-requirements-design/README.md)

Designed the next version of the AI Alert Explainer before beginning implementation.

Lab 13 used the validated results from Labs 11 and 12 to define:

* A vendor-neutral normalized alert model
* Initial Wazuh-to-normalized field mapping
* Normalized severity
* Validation rules
* Missing-field and malformed-value handling
* Multiple-alert processing
* Per-alert failure isolation
* Individual alert reports
* Batch-summary reporting
* Five deterministic test cases
* The controlled Lab 14 implementation scope

Six sanitized design screenshots are published as portfolio evidence.

The complete internal design record and proprietary Business Guardian implementation details remain outside the public repository.

## Current Status

Project Athenaeum is current through **Lab 13**.

The following labs are completed and published:

* Lab 01: Documentation Setup
* Lab 02: VirtualBox CyberLab
* Lab 03: Linux Fundamentals
* Lab 04: Windows Fundamentals
* Lab 05: DVWA Web Security
* Lab 06: Nmap Networking Basics
* Lab 07: BusinessGuardianLab Network Setup
* Lab 08: Wazuh Monitoring Server Setup
* Lab 09: Wazuh Windows Agent Deployment
* Lab 10: Wazuh Alert Review and AI Data Collection
* Lab 11: AI Alert Explainer MVP
* Lab 12: AI Alert Explainer Testing and Validation
* Lab 13: AI Alert Explainer v2 Requirements and Design

Project Athenaeum now documents a progression from foundational system administration and isolated cybersecurity lab deployment through endpoint monitoring, controlled alert generation, structured security-data analysis, Python-based alert explanation, software validation, and requirements-driven security-tool design.

Labs 11 and 12 remain preserved as the validated MVP baseline.

Lab 13 used the results of that work to design the next version before additional code is introduced.

## Next Project Phase

### Lab 14: AI Alert Explainer v2 Multiple Alert Processing

Lab 14 will begin controlled implementation of the v2 design approved during Lab 13.

Initial implementation priorities include:

* Creating a separate v2 development workspace
* Separating input and output locations
* Discovering multiple supported alert files in one run
* Reusing validated Lab 11 parsing and file-handling concepts
* Building the normalized alert structure
* Creating the first Wazuh-to-normalized translation process
* Adding normalized severity handling
* Applying validation rules
* Improving missing-field reporting
* Producing validation notes
* Assigning processing outcomes
* Defaulting processed alerts to `Requires Review`
* Generating unique individual alert reports
* Preventing accidental report overwrites
* Preserving source files without modification
* Isolating failures so one invalid alert does not stop the batch
* Creating one batch summary per processing run
* Running the five deterministic test scenarios defined during Lab 13
* Comparing v2 behavior with the validated Lab 11 and Lab 12 baseline

Planned processing outcomes include:

* `Processed Normally`
* `Processed With Warnings`
* `Failed Validation`

### Lab 14 Validation Target

The first v2 implementation has a defined validation target:

* 5 alerts discovered
* 2 processed normally
* 2 processed with warnings
* 1 failed validation
* 4 individual alert reports
* 1 batch summary

These acceptance criteria were defined before implementation so the completed Lab 14 workflow can be evaluated against measurable expected results.

Dashboard development, advanced AI integration, automated response, and commercial product functionality remain outside the immediate Lab 14 scope.

## Development Principles

Project Athenaeum follows a **build, validate, document, and extend** approach.

* Validated work is preserved rather than rebuilt unnecessarily.
* Existing components are reused, improved, updated, or extended when practical.
* New capabilities are designed and tested before being added to stable versions.
* Testing is performed before portfolio publication.
* Stable baselines are preserved before new changes are introduced.
* Security-platform-specific data is translated into normalized internal structures where practical.
* Core parsing, validation, normalization, severity handling, and control logic remain deterministic and testable.
* Missing or malformed information is identified rather than replaced with fabricated values.
* Severity helps determine review priority but does not automatically determine whether activity is malicious.
* AI-assisted features support explanation, enrichment, and analysis rather than independently making consequential security decisions.
* Human review remains required for security actions and final incident decisions.
* Public repository content is sanitized and portfolio-focused.
* Proprietary Business Guardian product implementation remains private.

## Public Repository Boundary

Project Athenaeum serves as the public, sanitized portfolio record of the work.

Public material may include:

* Completed lab summaries
* Sanitized screenshots
* Portfolio-safe scripts and demonstrations
* High-level architectural concepts
* Testing methodology
* Validation results
* Technical lessons learned
* Professional-development progress

More advanced Business Guardian product development remains outside this public repository.

Private product-level material may include:

* Proprietary application code
* Advanced backend and dashboard logic
* Security-platform adapters and connectors
* Investigation workflows
* Policy and approval mechanisms
* Audit mechanisms
* Sensitive security or business logging
* Tenant or customer logic
* Secrets-related configuration
* Sensitive test data
* Proprietary architecture and workflows
* Commercial material

The goal is to demonstrate technical progress publicly without publishing enough proprietary implementation detail to reproduce the commercial product.

## Future Roadmap

Project Athenaeum will continue to expand through controlled, documented projects rather than adding features without testing.

Future portfolio-safe development may include:

* Additional controlled Wazuh alert scenarios
* Broader alert-type testing
* Complete JSON alert parsing
* Improved alert normalization and validation
* Multiple-alert correlation
* Reusable severity mappings
* Additional deterministic and automated testing
* Structured processing records
* Modular alert-report components
* Structured incident-summary generation
* Analyst feedback and correction workflows
* Accuracy and consistency testing
* Additional Windows and Linux administration exercises
* Networking and troubleshooting projects
* Security monitoring and incident-investigation labs
* IT support automation
* Additional Python security automation
* A polished browser-based security monitoring interface
* Security+ certification preparation and supporting technical practice

A future Project Athenaeum lab will also build a Windows Network Troubleshooting Toolkit using a manually created batch-file workflow, administrator elevation, safety confirmations, authorized testing, documentation, and sanitized publication.

Dashboard, investigation, approval, and advanced AI capabilities will be added only after the underlying processing and validation layers are proven reliable.

## Home Lab

My current lab infrastructure includes:

* Windows 11 host computer
* Oracle VirtualBox
* Kali Linux security workstation
* Ubuntu Linux practice virtual machine
* Metasploitable 2 vulnerable target
* Windows 11 administration lab
* VirtualBox Internal Network: `CyberLab`
* CyberLab subnet: `192.168.56.0/24`
* BusinessGuardian-Win11-Workstation: `192.168.70.10/24`
* Wazuh Monitoring Server: `192.168.70.20/24`
* Active Wazuh Windows endpoint agent
* VirtualBox Internal Network: `BusinessGuardianLab`
* BusinessGuardianLab subnet: `192.168.70.0/24`
* NAT and isolated internal-network segmentation
* Local Wazuh dashboard access through VirtualBox port forwarding
* Clean recovery snapshots for major deployment stages

### Validated Lab Capabilities

* Isolated virtual-network deployment
* Static IPv4 configuration
* Windows and Linux administration
* Authorized vulnerability testing
* Nmap service and network scanning
* End-to-end Windows-to-Wazuh monitoring
* Controlled Windows event generation
* Wazuh alert generation and review
* Wazuh alert-detail, rule-field, and JSON analysis
* Sanitized security-data preparation
* Functional Python AI Alert Explainer MVP
* Plain-language alert report generation
* Missing-file and empty-file testing
* Missing alert-field behavior testing
* Wazuh severity-logic validation
* Stable baseline restoration and verification
* Vendor-neutral alert-model design
* Wazuh-to-normalized field-mapping design
* Normalized severity design
* Multiple-alert processing workflow design
* Deterministic validation-test planning
* Human-reviewed investigation recommendations

All cybersecurity exercises are performed using personally owned or authorized systems in isolated lab environments.

## Education and Development

* Bachelor of Science in Cybersecurity with a concentration in Project Management Fundamentals — expected September 2026
* InfoSec Labs Pre-Security Fundamentals Certificate
* InfoSec Labs Alert Investigation Specialist training
* CompTIA Security+ preparation
* Ongoing SOC, SIEM, endpoint-monitoring, Python, networking, Windows, Linux, and IT support practice
* Continued Project Athenaeum development focused on practical technical skills, testing, validation, documentation, and portfolio evidence

## Professional Goals

My immediate goal is to begin in an IT support, SOC analyst, cybersecurity support, or public-sector IT role where I can apply practical troubleshooting, documentation, endpoint monitoring, and security-analysis skills while continuing to build technical experience.

I am developing a foundation that combines IT support, cybersecurity operations, system administration, networking, Python automation, security monitoring, structured testing, and clear technical communication.

My longer-term goal is to grow into more advanced security and systems responsibilities while continuing to use Project Athenaeum to demonstrate measurable hands-on progress.

I also want to continue developing security tools that make technical information easier to understand and investigate while preserving evidence, deterministic controls, and human judgment for consequential security decisions.
