# Lab 07: BusinessGuardianLab Network Setup

## Overview

This lab documents the creation of a new isolated VirtualBox environment named `BusinessGuardianLab`.

The environment was designed as the technical foundation for future small-business IT support, endpoint monitoring, cybersecurity, automation, and AI-assisted security exercises within Project Athenaeum.

A Windows 11 workstation was installed, isolated from the internet, assigned a persistent static IPv4 address, and preserved with a VirtualBox snapshot.

## Objective

Create and validate a safe, isolated Windows 11 workstation environment that can later support security monitoring, simulated business activity, troubleshooting, logging, and incident-response exercises.

## Skills Demonstrated

- Oracle VirtualBox administration
- Windows 11 virtual-machine deployment
- Virtual network configuration
- Network isolation
- Static IPv4 configuration
- Windows networking troubleshooting
- APIPA identification
- Connectivity testing
- Snapshot management
- Security boundary validation
- Technical documentation
- Screenshot evidence management

## Environment and Tools

- Windows 11 host computer
- Oracle VirtualBox
- Windows 11 Pro virtual machine
- VirtualBox NAT networking during initial installation
- VirtualBox Internal Network
- Windows Command Prompt
- Windows network configuration tools
- Project Athenaeum documentation system

## Virtual Machine

### BusinessGuardian-Win11-Workstation

The Windows 11 virtual machine created for this lab is named:

```text
BusinessGuardian-Win11-Workstation
```

The workstation uses Windows 11 Pro and a local lab account named:

```text
BusinessUser
```

The virtual machine will eventually represent a simulated small-business workstation used for IT support, endpoint monitoring, security testing, backup validation, and incident-response exercises.

## Network Design

The isolated VirtualBox Internal Network is named:

```text
BusinessGuardianLab
```

The workstation was initially connected through NAT so Windows installation and setup could be completed.

After setup, the network adapter was changed from NAT to the isolated `BusinessGuardianLab` Internal Network.

No Bridged Adapter was used.

## Network Configuration

The Windows 11 workstation was assigned the following static IPv4 configuration:

```text
IP address: 192.168.70.10
Subnet prefix length: 24
Network: 192.168.70.0/24
```

A default gateway and public DNS server were not required for this isolated stage of the lab.

## Work Completed

During this lab, I:

- Created the Lab 07 documentation folder
- Created the Lab 07 screenshot folder
- Created the Windows 11 virtual machine
- Installed Windows 11 Pro
- Created the local `BusinessUser` account
- Used NAT temporarily during Windows installation
- Shut down the workstation before changing its network configuration
- Changed Adapter 1 to the VirtualBox Internal Network named `BusinessGuardianLab`
- Confirmed that Adapters 2 through 4 were disabled
- Confirmed that no Bridged Adapter was enabled
- Started the Windows workstation on the isolated network
- Tested internet connectivity using `ping 8.8.8.8`
- Confirmed that the internet connectivity test failed after isolation
- Identified an APIPA address before static configuration
- Assigned the static address `192.168.70.10/24`
- Verified the completed IPv4 configuration
- Created a clean VirtualBox snapshot
- Completed the Lab 07 screenshot log
- Began the Lab 07 technical notes

## Isolation Validation

After the workstation was moved from NAT to the `BusinessGuardianLab` Internal Network, an internet connectivity test was performed:

```powershell
ping 8.8.8.8
```

The test failed as expected.

This confirmed that the Windows 11 workstation could not access the public internet through the isolated internal network.

The failed ping was a successful security validation rather than a configuration failure.

## APIPA Troubleshooting

Before the static IPv4 address was assigned, Windows displayed an Automatic Private IP Addressing address.

APIPA addresses commonly use the following range:

```text
169.254.0.0/16
```

The APIPA address indicated that the workstation did not receive an address from a DHCP server.

This was expected because the isolated `BusinessGuardianLab` network did not yet contain a DHCP server.

The issue was resolved by assigning the planned static IPv4 address.

## Static IPv4 Address

The workstation was configured with:

```text
192.168.70.10/24
```

This provides a predictable address for future monitoring servers, administrative systems, scripts, dashboards, and other virtual machines added to the environment.

## VirtualBox Snapshot

After Windows installation, network isolation, and static IPv4 configuration were completed, the virtual machine was preserved using the snapshot:

```text
Lab07-Win11-Installed-Isolated-StaticIP
```

The snapshot provides a known-good recovery point before additional software, monitoring agents, simulated business applications, or security tools are installed.

## Security and Safety Boundaries

This lab follows these safety rules:

- The environment uses personally owned and authorized virtual systems
- The Windows workstation uses the isolated `BusinessGuardianLab` Internal Network
- No Bridged Adapter is enabled
- Public, employer, City, school, or customer systems are not scanned or tested
- No real customer or financial information is used
- Future business activity will be synthetic and created specifically for the lab
- Screenshots are reviewed before publication
- Passwords, personal information, and sensitive host details are excluded from GitHub
- Snapshots are created before major system changes

## Importance

A secure monitoring environment must begin with a controlled network foundation.

Creating the isolated workstation first ensures that future security tools, simulated business activity, endpoint agents, scripts, and monitoring systems can be tested without exposing an intentionally controlled environment to public or production networks.

The static address and clean snapshot also improve repeatability, troubleshooting, and recovery.

## Lessons Learned

This lab demonstrated the difference between NAT and an Internal Network in VirtualBox.

NAT allowed the workstation to access the internet during installation, while the Internal Network isolated the workstation after setup.

The APIPA address also demonstrated what happens when Windows is configured for automatic addressing but no DHCP server is available.

Assigning a static IPv4 address created a predictable foundation for later monitoring and security work.

The lab also reinforced that a failed internet ping can represent a successful security control when isolation is the intended result.

## Future Development

This environment will support later Project Athenaeum work involving:

- A Wazuh monitoring server
- A Wazuh agent on the Windows workstation
- Windows event and endpoint telemetry
- Synthetic small-business activity
- Simulated accounting and financial-risk events
- Backup and recovery monitoring
- Python-based detection and correlation
- AI-assisted alert explanations
- Human approval controls
- Security dashboards
- Incident-response documentation

These components have not yet been implemented and will be added during later stages of the Business Guardian project.

## Documentation Created

The following documentation is being retained locally:

- Lab 07 screenshot log
- Lab 07 technical notes
- Sanitized supporting screenshots
- Final portfolio writeup after documentation is completed

## Status

**Network setup completed and GitHub evidence upload in progress**
