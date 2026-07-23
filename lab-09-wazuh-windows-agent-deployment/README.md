# Lab 09: Wazuh Windows Agent Deployment

## Overview

This lab documents the installation, configuration, troubleshooting, and validation of the Wazuh Windows agent on the isolated `BusinessGuardian-Win11-Workstation`.

The Windows workstation was connected to the Wazuh monitoring server created in Lab 08. After correcting an agent configuration issue, the workstation successfully registered with the Wazuh manager and appeared as an active endpoint in the Wazuh dashboard.

The completed deployment established centralized endpoint monitoring for the Project Athenaeum Business Guardian environment.

## Objective

Install and configure the Wazuh Windows agent, connect the workstation to the Wazuh monitoring server at `192.168.70.20`, confirm active endpoint reporting, restore network isolation, and preserve clean recovery snapshots.

## Skills Demonstrated

- Windows endpoint administration
- Wazuh agent deployment
- SIEM endpoint integration
- Agent-manager communication
- Windows service management
- Configuration-file review
- XML configuration editing
- Network connectivity testing
- Troubleshooting
- Static IPv4 networking
- VirtualBox network isolation
- Dashboard validation
- Snapshot management
- Technical documentation
- Privacy-conscious evidence handling

## Environment and Tools

- Windows 11 host computer
- Oracle VirtualBox
- BusinessGuardian Windows 11 workstation
- Ubuntu-based Wazuh monitoring server
- Wazuh Windows agent
- Wazuh dashboard
- Windows Services
- Windows Command Prompt
- Windows File Explorer
- Text editor with administrator privileges
- VirtualBox NAT networking
- VirtualBox Internal Network named `BusinessGuardianLab`

## Lab Systems

### Windows Workstation

The monitored endpoint is:

```text
BusinessGuardian-Win11-Workstation
```

Static internal address:

```text
192.168.70.10/24
```

### Wazuh Monitoring Server

The Wazuh manager uses:

```text
192.168.70.20/24
```

### Internal Network

Both systems communicate through:

```text
BusinessGuardianLab
```

Network:

```text
192.168.70.0/24
```

## Network Architecture

```text
Windows 11 Host
        |
 Oracle VirtualBox
        |
 BusinessGuardianLab
 192.168.70.0/24
        |
        +-----------------------------+
        |                             |
Windows Workstation              Wazuh Server
192.168.70.10                    192.168.70.20
Wazuh Windows Agent              Wazuh Manager
```

Temporary NAT connectivity was used only when required for the authorized agent installation process. NAT was disabled after installation, and the workstation was returned to the isolated `BusinessGuardianLab` network.

No Bridged Adapter was used.

## Work Completed

During this lab, I:

- Started the Wazuh monitoring server
- Started the Business Guardian Windows 11 workstation
- Verified communication between the Windows workstation and Wazuh server
- Temporarily enabled controlled NAT connectivity for agent installation
- Accessed the Wazuh dashboard from the host computer
- Opened the Wazuh agent deployment interface
- Selected Windows as the endpoint operating system
- Entered the Wazuh manager address `192.168.70.20`
- Downloaded and installed the Wazuh Windows agent
- Verified that the agent files were installed
- Reviewed the Wazuh agent configuration file
- Identified an incorrect manager address of `0.0.0.0`
- Corrected the manager address to `192.168.70.20`
- Saved the corrected configuration with administrator privileges
- Restarted the Wazuh agent service
- Verified that the Wazuh agent service was running
- Confirmed that the Windows workstation appeared in the Wazuh dashboard
- Verified that the endpoint status was active
- Confirmed that the dashboard displayed the Windows 11 agent at `192.168.70.10`
- Disabled temporary NAT connectivity
- Restored the workstation to the isolated `BusinessGuardianLab` network
- Confirmed successful communication with the Wazuh server
- Confirmed that public internet connectivity was unavailable
- Created post-agent recovery snapshots
- Completed the screenshot log, technical notes, and final portfolio writeup

## Agent Deployment

The Wazuh dashboard deployment interface was used to generate the Windows agent installation instructions.

The Wazuh manager address was configured as:

```text
192.168.70.20
```

The agent was installed on the authorized Windows 11 workstation.

After installation, the Wazuh agent service and configuration were reviewed to confirm that the endpoint was prepared to communicate with the monitoring server.

## Configuration Troubleshooting

The Windows agent initially failed to report correctly to the Wazuh manager.

The agent configuration file was reviewed at the Wazuh installation location. The manager address was found to contain:

```text
0.0.0.0
```

This address did not identify the actual Wazuh monitoring server and prevented proper agent-manager communication.

The configuration was corrected to:

```text
192.168.70.20
```

The file was saved with administrator privileges, and the Wazuh agent service was restarted.

After the correction, the endpoint successfully connected to the Wazuh manager.

## Agent Service Validation

Windows Services was used to confirm that the Wazuh agent service was installed and running.

A running agent service is necessary for the workstation to:

- Collect local endpoint information
- Monitor configured Windows events
- Communicate with the Wazuh manager
- Receive configuration updates
- Forward security telemetry
- Support centralized alerting and investigation

## Dashboard Validation

The Wazuh dashboard confirmed that the Windows endpoint was successfully registered.

The dashboard displayed:

```text
Active agents: 1
```

The monitored endpoint was identified as a Windows 11 system using the internal address:

```text
192.168.70.10
```

This confirmed that:

- The Wazuh agent was installed
- The agent service was running
- The manager address was correct
- The workstation could communicate with the server
- The Wazuh manager accepted the endpoint
- The dashboard received updated agent information

## Network Isolation Validation

After the Wazuh agent installation and validation were complete, temporary NAT connectivity was disabled.

The Windows workstation was returned to the isolated VirtualBox Internal Network named:

```text
BusinessGuardianLab
```

Connectivity testing confirmed that the workstation could still reach the Wazuh server:

```powershell
ping 192.168.70.20
```

A public internet connectivity test failed as expected:

```powershell
ping 8.8.8.8
```

These results confirmed that the endpoint could communicate with the monitoring server while remaining isolated from the public internet.

## Snapshots and Recovery

Post-agent snapshots were created after the following conditions were verified:

- Wazuh agent installed
- Manager address corrected
- Agent service running
- Endpoint active in the dashboard
- Temporary NAT disabled
- Internal communication successful
- Public internet connectivity unavailable

The snapshots provide known-good recovery points before controlled alert generation, telemetry review, or additional Business Guardian development.

## Troubleshooting Process

The troubleshooting process followed a layered approach:

1. Confirm the Wazuh server was running
2. Verify the Windows workstation network configuration
3. Test communication with `192.168.70.20`
4. Confirm that the Windows agent was installed
5. Review the agent service
6. Inspect the agent configuration file
7. Identify the incorrect manager address
8. Correct the address to `192.168.70.20`
9. Restart the agent service
10. Verify active status in the Wazuh dashboard
11. Remove temporary NAT connectivity
12. Revalidate network isolation

This process demonstrated the importance of validating networking, services, configuration files, and dashboard status separately.

## Security and Safety Boundaries

This lab followed these safety rules:

- All systems were personally owned and explicitly authorized
- The Windows workstation and Wazuh server used the isolated `BusinessGuardianLab` network
- NAT connectivity was temporary and limited to authorized installation needs
- No Bridged Adapter was enabled
- No real customer, financial, employer, City, or production data was used
- Monitoring was limited to Project Athenaeum virtual systems
- Credentials and sensitive configuration details were excluded from public evidence
- Screenshots were reviewed before publication
- Recovery snapshots were created before future testing
- Controlled events will be generated only inside the authorized lab

## Importance

Endpoint agents provide visibility that cannot be obtained through network scanning alone.

The Wazuh Windows agent allows the monitoring server to receive endpoint information and security telemetry directly from the workstation. This creates the foundation for centralized monitoring, alert generation, file-integrity monitoring, authentication review, system-event analysis, and incident investigation.

Successfully integrating the Windows workstation moved the Business Guardian environment from basic infrastructure into an operational monitoring lab.

## Lessons Learned

This lab demonstrated that successful software installation does not automatically guarantee successful communication.

The Wazuh agent was present on the workstation, but an incorrect manager address prevented it from reporting properly. Reviewing the configuration file and correcting the address resolved the issue.

The lab also reinforced the value of checking each technical layer separately. Network connectivity, service status, configuration settings, dashboard registration, and isolation controls all required individual validation.

Finally, the lab demonstrated that temporary internet access can be removed after installation while preserving communication between authorized systems on an isolated internal network.

## Documentation Created

The following Lab 09 documentation was completed and retained locally:

- Lab 09 screenshot log
- Detailed Lab 09 technical notes
- Lab 09 final portfolio writeup
- Agent installation evidence
- Configuration troubleshooting evidence
- Windows service evidence
- Wazuh dashboard evidence
- Network-isolation evidence
- Post-agent snapshot evidence
- Sanitized public screenshots

## Future Development

The next Business Guardian phase may include:

- Reviewing Windows endpoint inventory
- Examining Windows system and security telemetry
- Generating controlled authentication events
- Creating controlled file-integrity events
- Reviewing Wazuh alerts and rule details
- Documenting alert severity and supporting evidence
- Developing Python-based event correlation
- Adding AI-assisted alert explanations
- Building response recommendations
- Creating incident reports and investigation timelines

## Status

**Technical work and local documentation completed; GitHub evidence upload in progress**
