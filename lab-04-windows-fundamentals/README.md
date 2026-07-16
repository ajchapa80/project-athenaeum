# Lab 04: Windows Fundamentals

## Overview

This lab documents the review of core Windows 11 administration, security, networking, system monitoring, and troubleshooting features.

The exercises focused on identifying system information, reviewing active processes, examining Windows event logs, evaluating built-in security protections, checking network configuration, reviewing firewall settings, and verifying operating system health and update status.

## Objective

Develop practical familiarity with Windows administration and security tools commonly used in IT support, system administration, and entry-level cybersecurity roles.

## Skills Demonstrated

- Windows system administration
- Operating system identification
- Hardware and system-information review
- Process and performance monitoring
- Windows Event Viewer navigation
- Windows Security review
- Microsoft Defender awareness
- Firewall configuration review
- Network configuration analysis
- PowerShell navigation
- Windows Update verification
- Device security review
- Technical documentation
- Privacy-conscious evidence collection

## Environment and Tools

- Windows 11
- Windows Settings
- System Information
- Task Manager
- Event Viewer
- Windows Security
- Microsoft Defender Firewall
- PowerShell
- Command-line networking utilities
- Windows Update

## Work Completed

During this lab, I:

- Verified the installed Windows edition and version using `winver`
- Reviewed detailed operating system and hardware information using `msinfo32`
- Examined running applications, background processes, performance, and system resources in Task Manager
- Opened and reviewed Windows Event Viewer
- Examined system and security-related event categories
- Reviewed the Windows Security dashboard
- Verified virus and threat protection status
- Reviewed firewall and network protection settings
- Examined device security features
- Reviewed device performance and health information
- Used PowerShell to examine Windows system information
- Reviewed network adapter and IP configuration information
- Verified Windows Update status
- Reviewed Windows Update history
- Sanitized screenshots to remove the computer name and local network details
- Documented the exercises in the Lab 04 notes and screenshot log

## System Information Review

Windows provides several built-in tools for identifying the operating system, hardware, and system configuration.

The `winver` utility was used to verify the Windows version and edition. System Information was then reviewed to examine additional details about the operating system, processor, memory, system type, and hardware environment.

## Task Manager and Performance Monitoring

Task Manager was used to review:

- Running applications
- Background processes
- CPU utilization
- Memory utilization
- Disk activity
- Network activity
- Startup applications
- System uptime

This information can help identify resource shortages, unresponsive applications, excessive background activity, and unusual processes.

## Event Viewer

Windows Event Viewer provides centralized access to operating system and application logs.

The following primary log categories were reviewed:

- Application
- Security
- Setup
- System
- Forwarded Events

Event Viewer is an important troubleshooting and cybersecurity tool because it records system activity, errors, warnings, authentication events, application failures, and other operational information.

## Windows Security

The Windows Security application was reviewed to examine built-in endpoint protection and operating system security features.

Areas reviewed included:

- Virus and threat protection
- Account protection
- Firewall and network protection
- App and browser control
- Device security
- Device performance and health
- Protection history

These tools provide visibility into security settings, endpoint protection status, firewall profiles, hardware-backed protections, and system health.

## Network Configuration

Windows networking information was reviewed using built-in command-line tools.

The review included:

- Network adapters
- IPv4 and IPv6 configuration
- Subnet information
- Default gateway information
- DNS configuration
- Connection status

Local network information was redacted from screenshots before publication.

## Firewall Review

Microsoft Defender Firewall settings were reviewed to confirm the status of the available network profiles.

Windows uses separate firewall profiles for:

- Domain networks
- Private networks
- Public networks

Reviewing these profiles helps confirm that firewall protection is active and appropriate for the system’s current network environment.

## PowerShell

PowerShell was used as an administrative and troubleshooting interface for reviewing Windows system information.

PowerShell provides administrators and security professionals with tools for:

- System information collection
- Process review
- Service management
- Network troubleshooting
- Event-log analysis
- Security configuration review
- Automation

## Device Security and Health

Windows device security and health features were reviewed to better understand the protections and monitoring capabilities available within Windows 11.

The review included available hardware security features, system health indicators, storage status, application health, and Windows Update status.

## Windows Update

Windows Update was reviewed to confirm whether the operating system was current.

The update history was also examined to identify previously installed:

- Quality updates
- Driver updates
- Definition updates
- Feature updates
- Other Microsoft updates

Maintaining current operating system and security updates is an important part of vulnerability management and endpoint security.

## Screenshots and Evidence

### Windows Version

The `winver` utility confirmed the installed Windows edition and version.

![Windows version information](screenshots/2026-07-16_Lab04_Windows_01_windows-version-winver.png)

### System Information

System Information was reviewed to examine the operating system, processor, memory, system type, and hardware environment. Sensitive system-identifying information was redacted.

![Redacted Windows system information](screenshots/2026-07-16_Lab04_Windows_02_system-information-redacted.png)

### Task Manager Performance

Task Manager was used to review CPU, memory, disk, network, and system-performance information.

![Task Manager performance review](screenshots/2026-07-16_Lab04_Windows_03_task-manager-performance.png)

### Task Manager Processes

Running applications and background processes were reviewed for resource usage and system activity.

![Task Manager process review](screenshots/2026-07-16_Lab04_Windows_04_task-manager-processes.png)

### Task Manager Services

Windows services were reviewed through Task Manager to examine their current status and associated process information.

![Task Manager services review](screenshots/2026-07-16_Lab04_Windows_05_task-manager-services.png)

### Event Viewer Application Log

The Windows Application log was reviewed for informational events, warnings, errors, and application activity.

![Event Viewer Application log](screenshots/2026-07-16_Lab04_Windows_06_event-viewer-application-log.png)

### Event Viewer System Log

The Windows System log was reviewed for operating-system, driver, hardware, and service-related events.

![Event Viewer System log](screenshots/2026-07-16_Lab04_Windows_07_event-viewer-system-log.png)

### Windows Security Overview

The Windows Security dashboard was reviewed to examine the status of built-in endpoint protection and security features.

![Windows Security overview](screenshots/2026-07-16_Lab04_Windows_08_windows-security-overview.png)

### PowerShell Basic Commands

PowerShell was used to practice command-line navigation and basic Windows administration commands.

![PowerShell basic commands](screenshots/2026-07-16_Lab04_Windows_09_powershell-basic-commands.png)

### PowerShell Process Review

PowerShell commands were used to review active processes and system activity.

![PowerShell process review](screenshots/2026-07-16_Lab04_Windows_10_powershell-process-review.png)

### PowerShell Services Review

PowerShell was used to review Windows services and their current operating status.

![PowerShell services review](screenshots/2026-07-16_Lab04_Windows_11_powershell-services-review.png)

### Network Configuration

Windows network configuration was reviewed using `ipconfig`. Local IP addresses, gateway information, and other sensitive network details were redacted before publication.

![Redacted Windows network configuration](screenshots/2026-07-16_Lab04_Windows_12_ipconfig-network-info-redacted.png)

### Firewall and Network Protection

Microsoft Defender Firewall settings were reviewed to examine the available Domain, Private, and Public network profiles.

![Firewall and network protection](screenshots/2026-07-16_Lab04_Windows_13_firewall-network-protection.png)

### Protection History

Windows Security protection history was reviewed to examine previously detected or remediated security events.

![Windows Security protection history](screenshots/2026-07-16_Lab04_Windows_14_protection-history.png)

### Device Security

Windows device-security features were reviewed to identify available hardware-backed and operating-system protections.

![Windows device security](screenshots/2026-07-16_Lab04_Windows_15_device-security.png)

### Device Performance and Health

Device performance and health information was reviewed to examine storage, application, system, and update health.

![Windows device performance and health](screenshots/2026-07-16_Lab04_Windows_16_device-performance-health.png)

### Windows Update Status

Windows Update was reviewed to confirm the current operating-system update status.

![Windows Update status](screenshots/2026-07-16_Lab04_Windows_17_windows-update-status.png)

### Windows Update History

The Windows Update history was reviewed to identify previously installed quality, driver, definition, feature, and other Microsoft updates.

![Windows Update history](screenshots/2026-07-16_Lab04_Windows_18_windows-update-history.png)

## Security and Privacy

The evidence was reviewed before publication to prevent exposure of:

- Computer names
- User account information
- Local IP addresses
- Default gateway information
- DNS server information
- Wireless network information
- Device identifiers
- Personal files
- Unrelated applications or browser activity

## Importance

Windows remains one of the most widely used operating systems in business and government environments. IT support technicians and cybersecurity professionals must understand how to review system information, monitor performance, investigate event logs, examine security controls, troubleshoot network settings, and verify update status.

These built-in Windows tools provide a foundation for endpoint administration, technical support, security monitoring, and incident investigation.

## Lessons Learned

This lab reinforced that Windows includes many useful administration and security tools without requiring additional software.

Task Manager provides immediate visibility into processes and resource usage, while Event Viewer offers historical evidence of system and application activity. Windows Security centralizes endpoint protection, firewall, device-security, and health information. PowerShell provides a flexible interface for deeper administration and future automation.

The lab also reinforced the importance of reviewing screenshots for sensitive system and network information before including them in a public portfolio.

## Status

**Completed and portfolio ready**
