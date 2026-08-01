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

## Current Status

Project Athenaeum is current through Lab 12. The following labs are completed, documented, supported by sanitized evidence, and published in this repository:

- Lab 01: Documentation Setup
- Lab 02: VirtualBox CyberLab
- Lab 03: Linux Fundamentals
- Lab 04: Windows Fundamentals
- Lab 05: DVWA Web Security
- Lab 06: Nmap Networking Basics
- Lab 07: BusinessGuardianLab Network Setup
- Lab 08: Wazuh Monitoring Server Setup
- Lab 09: Wazuh Windows Agent Deployment
- Lab 10: Wazuh Alert Review and AI Data Collection
- Lab 11: AI Alert Explainer MVP
- Lab 12: AI Alert Explainer Testing and Validation

Project Athenaeum now includes a complete progression from isolated lab deployment and endpoint monitoring to alert generation, Python-based alert explanation, and structured validation testing.

Lab 12 preserved the published Lab 11 MVP as a stable baseline and tested copied files in a separate workspace. All planned tests passed, including baseline execution, missing-file handling, empty-file handling, missing-field behavior, severity-logic validation, and final restoration to the original working state.

## Next Project Phase

### AI Alert Explainer Expansion Planning

Lab 12 established documented evidence about how the current MVP behaves under normal and abnormal input conditions. Future improvements will be based on those validation results rather than being rushed into the stable Lab 11 version.

Potential next steps include:

- Testing additional sanitized Wazuh alert samples
- Comparing different rule levels and alert categories
- Creating repeatable automated test cases
- Improving missing-field handling
- Parsing complete JSON alert records
- Supporting multiple alert files
- Creating reusable severity mappings
- Exporting reports in text and structured formats
- Comparing generated explanations with original alert evidence
- Recording analyst corrections and feedback
- Measuring explanation consistency and accuracy

Later Business Guardian development may include:

- Alert correlation
- A simplified graphical interface
- Dashboard integration
- Business-focused incident summaries
- Synthetic financial and QuickBooks-style activity
- Backup and recovery monitoring
- Approved local or external AI-model integration
- Human-approved investigation and response actions

The next lab number and final scope will be assigned inside Project Athenaeum after the next technical phase is planned.

## Professional Goal

My immediate goal is to begin in an entry-level IT support, service desk, technical support, or cybersecurity support role where I can apply my customer service, troubleshooting, documentation, and security knowledge while gaining practical experience.

As I continue developing my technical skills, I plan to advance into security operations, incident investigation, and cybersecurity analysis.

My long-term goal is to build a practical IT services business and eventually expand into responsible cybersecurity services as my experience, certifications, and capabilities grow.
