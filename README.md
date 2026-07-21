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

## Current Status

Project Athenaeum is current through Lab 07. The following labs are completed, documented, supported by sanitized evidence, and published in this repository:

- Lab 01: Documentation Setup
- Lab 02: VirtualBox CyberLab
- Lab 03: Linux Fundamentals
- Lab 04: Windows Fundamentals
- Lab 05: DVWA Web Security
- Lab 06: Nmap Networking Basics
- Lab 07: BusinessGuardianLab Network Setup

The isolated Windows 11 foundation for the Athenaeum Business Guardian MVP is complete. The next phase will expand the environment with centralized monitoring, endpoint telemetry, simulated business activity, Python-based detection, and AI-assisted alert explanations.

## Next Project Phase

### Athenaeum Business Guardian MVP — Monitoring Foundation

With the isolated Windows 11 workstation and `BusinessGuardianLab` network foundation complete, the next phase will introduce centralized security monitoring.

Planned work includes:

- Deploying a Wazuh security-monitoring server
- Connecting the server to the isolated `BusinessGuardianLab` network
- Installing the Wazuh agent on `BusinessGuardian-Win11-Workstation`
- Confirming that the workstation reports successfully to the Wazuh dashboard
- Reviewing Windows endpoint and security telemetry
- Generating controlled test events
- Documenting alerts, findings, and troubleshooting steps
- Creating sanitized screenshots and portfolio evidence
- Preserving clean snapshots before major configuration changes

Later Business Guardian phases will add:

- Synthetic QuickBooks-style activity
- Python-based detection and event correlation
- AI-assisted alert explanations
- Backup and recovery monitoring
- Financial-risk indicators
- Human approval controls
- A simple monitoring dashboard
- Incident reports and response documentation

The next lab number and final title will be assigned when this phase begins.

## Future Roadmap

Later Project Athenaeum work may include:

- Wireshark traffic-analysis fundamentals
- SOC alert triage and investigation
- PowerShell administration and automation
- AI-assisted cybersecurity and IT support tools
- A Windows Network Troubleshooting Toolkit built manually as a batch file
- Administrator elevation, menu controls, and safety confirmations for the troubleshooting toolkit
- A simulated incident-response and business-continuity environment
- A lean Pueblo-based IT services business test
- Website, booking, remote-support, and mobile IT-service development

Lab numbers for later projects will be assigned as the roadmap develops. This prevents completed work from having to be renumbered when priorities change.

## Professional Goal

My immediate goal is to begin in an entry-level IT support, service desk, technical support, or cybersecurity support role where I can apply my customer service, troubleshooting, documentation, and security knowledge while gaining practical experience.

As I continue developing my technical skills, I plan to advance into security operations, incident investigation, and cybersecurity analysis.

My long-term goal is to build a practical IT services business and eventually expand into responsible cybersecurity services as my experience, certifications, and capabilities grow.
