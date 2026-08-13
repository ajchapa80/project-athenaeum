# Project Athenaeum

Project Athenaeum is my cybersecurity and information technology portfolio. This repository documents hands-on labs, security investigations, system administration exercises, and technical projects completed as I prepare for an entry-level SOC analyst or IT support position.

## About This Project

The purpose of Project Athenaeum is to demonstrate practical technical skills through clearly documented exercises. Each lab will include an objective, tools used, procedures performed, screenshots, findings, security relevance, and lessons learned.

## Focus Areas

- Security operations and alert investigation
- SIEM, endpoint telemetry, and log analysis
- Linux and Windows administration
- Networking and traffic analysis
- Vulnerability assessment
- Incident response
- Python security automation
- AI-assisted alert explanation and decision support
- Backup, business-continuity, and financial-risk monitoring
- IT troubleshooting and support
- Technical documentation
- Secure tool and dashboard development

## Lab Environment

My home lab currently includes:

- Kali Linux
- Ubuntu Linux
- Metasploitable 2
- Oracle VirtualBox
- Windows 11
- Internal and NAT virtual networking

All cybersecurity exercises are performed in an isolated lab environment using authorized systems.

## Repository Structure

As the project develops, this repository will include:

- Lab documentation
- Sanitized screenshots
- Security investigation case studies
- Network diagrams
- Command references
- Scripts and technical exercises
- Final portfolio writeups

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

Performed authorized web application security testing against DVWA inside the isolated CyberLab environment. The lab documents command injection and SQL injection testing, comparisons between Low and High security settings, defensive recommendations, and 12 sanitized evidence screenshots.

### [Lab 06: Nmap Networking Basics](lab-06-nmap-networking-basics/README.md)

Performed authorized Nmap scanning against Metasploitable 2 inside the isolated CyberLab environment. The lab documents basic scanning, service and version detection, targeted web, database, and remote-access port scans, operating-system detection, aggressive scanning, saved scan results, and 13 sanitized evidence screenshots.

### [Lab 07: BusinessGuardianLab Network Setup](lab-07-businessguardianlab-network-setup/README.md)

Created and validated an isolated Windows 11 small-business lab environment using the VirtualBox Internal Network `BusinessGuardianLab`. The workstation was installed, isolated from the internet, assigned the persistent static address `192.168.70.10/24`, preserved with a clean snapshot, and documented with 18 sanitized evidence screenshots.

### [Lab 08: Wazuh Monitoring Server Setup](lab-08-wazuh-monitoring-server-setup/README.md)

Deployed and configured a centralized Wazuh monitoring server for the isolated `BusinessGuardianLab` environment. The server uses separate NAT and internal-network adapters, the persistent internal address `192.168.70.20/24`, local dashboard access through VirtualBox port forwarding, validated Wazuh services, and 23 sanitized public evidence screenshots.

### [Lab 09: Wazuh Windows Agent Deployment](lab-09-wazuh-windows-agent-deployment/README.md)

Installed, configured, troubleshot, and validated the Wazuh Windows agent on the isolated Business Guardian workstation. The endpoint successfully registered with the Wazuh server at `192.168.70.20`, remained active after temporary NAT was removed, and was documented with 13 sanitized evidence screenshots.

### [Lab 10: Wazuh Alert Review and AI Data Collection](lab-10-wazuh-alert-review-ai-data-collection/README.md)

Generated safe Windows events, validated end-to-end Wazuh alert detection, reviewed alert details and structured JSON fields, and created a sanitized AI-ready data sample. The lab includes 11 cropped evidence screenshots documenting the complete event-to-alert workflow.

### [Lab 11: AI Alert Explainer MVP](lab-11-ai-alert-explainer-mvp/README.md)

Built a functional Python alert-explanation tool using the sanitized Wazuh data prepared during Lab 10. The MVP extracts selected endpoint, Windows event, and Wazuh rule fields; explains alert severity; generates analyst context and review steps; and preserves human verification before any security decision. The published lab includes the working Python script, sanitized input sample, generated output, and nine evidence screenshots.

### [Lab 12: AI Alert Explainer Testing and Validation](lab-12-ai-alert-explainer-testing-validation/README.md)

Tested and validated the Python-based AI Alert Explainer MVP created in Lab 11 while preserving the published MVP as a stable baseline. Validation covered normal execution, output-file creation, missing and empty input files, missing-field behavior, severity-logic changes, and final restoration to the original baseline. The published lab includes the copied working files and 17 sanitized evidence screenshots.

### [Lab 13: AI Alert Explainer v2 Requirements and Design](lab-13-ai-alert-explainer-v2-requirements-design/README.md)

Designed the next version of the AI Alert Explainer before beginning implementation. Lab 13 used the validated results from Labs 11 and 12 to define a vendor-neutral normalized alert model, Wazuh-to-normalized field mapping, normalized severity, validation rules, multiple-alert processing, individual alert reports, batch-summary reporting, five deterministic test cases, and the controlled Lab 14 implementation scope.

Six sanitized design screenshots are published as portfolio evidence. The complete internal design record and proprietary Business Guardian implementation details remain outside the public repository.

## Current Status

Project Athenaeum is current through Lab 13. The following labs are completed, documented, supported by sanitized evidence, and published in this repository:

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

Labs 11 and 12 remain preserved as the validated MVP baseline. Lab 13 used the results of that work to design the next version before new code is introduced.

## Next Project Phase

### Lab 14: AI Alert Explainer v2 Multiple Alert Processing

Lab 14 will begin controlled implementation of the v2 design approved during Lab 13.

Initial implementation priorities include:

* Creating a separate v2 development workspace
* Supporting multiple sanitized alert samples
* Separating input and output handling
* Building the normalized alert structure
* Creating the first Wazuh-to-normalized mapping process
* Applying validation rules
* Adding normalized severity handling
* Improving missing-field reporting
* Generating unique individual alert reports
* Preventing accidental report overwrites
* Isolating failures so one invalid alert does not stop the batch
* Creating a batch-summary report
* Running the five deterministic test scenarios defined during Lab 13
* Comparing v2 behavior with the validated Lab 11 and Lab 12 baseline

Dashboard development, advanced AI integration, automated response, and commercial product functionality remain outside the immediate Lab 14 scope.

## Development Principles

Project Athenaeum follows a build, validate, document, and extend approach.

- Validated work is preserved rather than rebuilt unnecessarily.
- New capabilities are designed and tested before being added to stable versions.
- Security-platform-specific data is translated into normalized internal structures where practical.
- Core parsing, validation, severity handling, and control logic remain deterministic and testable.
- AI-assisted features support explanation and analysis rather than independently making consequential security decisions.
- Human review remains required for security actions and final incident decisions.
- Public repository content is sanitized and portfolio-focused; proprietary Business Guardian product implementation remains private.

## Future Roadmap

Project Athenaeum will continue to expand through controlled, documented projects rather than adding features without testing.

Future portfolio-safe development may include:

* Additional Wazuh alert types and controlled security events
* Complete JSON alert parsing
* Improved alert normalization and validation
* Multiple-alert correlation
* Reusable severity mappings
* Additional automated and deterministic testing
* Structured incident-summary generation
* Analyst feedback and correction workflows
* Accuracy and consistency testing
* Windows and Linux administration exercises
* Networking and troubleshooting projects
* Security monitoring and incident-investigation labs
* IT support automation
* A polished browser-based security monitoring interface
* Additional Python security automation
* Security+ certification preparation and supporting technical practice

More advanced Business Guardian product development, proprietary workflows, sensitive configuration, connectors, approval mechanisms, tenant logic, commercial material, and product-level architecture remain outside the public Project Athenaeum repository.

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

* End-to-end Windows-to-Wazuh monitoring
* Controlled Windows event and Wazuh alert generation
* Wazuh alert-detail, rule-field, and JSON review
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

All security exercises are performed using personally owned or authorized systems in isolated lab environments.

## Education and Development

* Bachelor of Science in Cybersecurity, Project Management Fundamentals concentration — expected September 2026
* InfoSec Labs Pre-Security Fundamentals Certificate
* InfoSec Labs Alert Investigation Specialist training
* CompTIA Security+ preparation
* Ongoing SOC, SIEM, endpoint monitoring, Python, networking, Windows, Linux, and IT support practice
* Continued Project Athenaeum development focused on practical technical skills, testing, documentation, and portfolio evidence

## Professional Goals

My immediate goal is to begin in an IT support, SOC analyst, cybersecurity support, or public-sector IT role where I can apply practical troubleshooting, documentation, endpoint monitoring, and security-analysis skills while continuing to build experience.

I am developing a foundation that combines IT support, cybersecurity operations, system administration, networking, Python automation, and clear technical communication. My longer-term goal is to continue growing into more advanced security and systems responsibilities while using Project Athenaeum to demonstrate measurable hands-on progress.

I also want to continue learning how security tools can make technical information easier for people to understand without removing human judgment from important security decisions.
