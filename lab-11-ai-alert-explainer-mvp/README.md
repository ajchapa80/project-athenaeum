# Lab 11: AI Alert Explainer MVP

## Overview

This lab documents the development of the first functional alert-explanation tool in Project Athenaeum.

The Python-based MVP uses the sanitized Wazuh alert data prepared during Lab 10. It reads structured JSON fields and converts them into a beginner-friendly security explanation containing an alert summary, severity explanation, analyst context, and recommended review steps.

The project was developed locally on the Windows host computer. No additional virtual machines were required because the Wazuh alert sample had already been collected and sanitized.

## Objective

Build a beginner-friendly Python tool that reads a sanitized Wazuh alert sample and produces a clear, structured explanation that can support entry-level alert triage and analyst review.

## Skills Demonstrated

- Python fundamentals
- JSON parsing
- Structured security-data processing
- Wazuh alert interpretation
- Alert-field extraction
- Conditional logic
- Functions and reusable code
- Plain-language technical communication
- Security severity interpretation
- Analyst workflow development
- Error handling
- Human-in-the-loop decision support
- Testing and troubleshooting
- Technical documentation
- Privacy-conscious data handling

## Environment and Tools

- Windows 11 host computer
- Python
- Visual Studio Code or local text editor
- Windows Terminal or Command Prompt
- Sanitized Wazuh JSON alert sample from Lab 10
- Project Athenaeum documentation system
- GitHub

## Project Relationship

Lab 11 builds directly on the work completed during Lab 10.

```text
Lab 10
Wazuh alert generated and reviewed
          |
          v
Alert JSON examined and sanitized
          |
          v
Lab 11
Python reads the alert sample
          |
          v
Important fields are extracted
          |
          v
Plain-language explanation is generated
          |
          v
Human analyst reviews the result
```

## Input Data

The tool uses a sanitized JSON alert sample containing selected Wazuh fields.

Useful fields may include:

- Alert timestamp
- Agent name
- Agent IP address
- Wazuh rule ID
- Wazuh rule level
- Rule description
- Windows event source
- Event ID
- Event message
- Additional analyst context

Unnecessary, repetitive, personal, or sensitive fields were excluded before the alert sample was used.

## Core Features

The MVP performs the following functions:

- Opens a sanitized JSON alert file
- Reads the structured alert data
- Extracts important investigation fields
- Identifies the affected endpoint
- Identifies the Wazuh rule and severity level
- Produces a plain-English alert summary
- Explains what the severity level means
- Provides analyst context
- Recommends practical review steps
- Displays a human-review reminder
- Handles missing or incomplete fields without immediately failing

## Work Completed

During this lab, I:

- Created the Lab 11 documentation structure
- Reviewed the sanitized Wazuh alert sample from Lab 10
- Identified the JSON fields needed by the tool
- Created the initial Python script
- Added JSON file-reading functionality
- Extracted the alert timestamp
- Extracted the agent name and address
- Extracted the Wazuh rule ID
- Extracted the rule level
- Extracted the rule description
- Added plain-language alert-summary logic
- Added severity-explanation logic
- Added analyst-context output
- Added recommended review steps
- Added a human-review requirement
- Tested the script with the sanitized alert sample
- Reviewed the generated explanation
- Corrected formatting or logic issues found during testing
- Verified that the final output was readable and organized
- Collected technical screenshots
- Completed the Lab 11 technical notes
- Prepared the lab for portfolio publication

## Alert-Processing Workflow

The tool follows a simple and repeatable workflow:

```text
1. Load sanitized JSON
2. Read the alert fields
3. Extract important values
4. Interpret the rule level
5. Build a plain-language summary
6. Add analyst context
7. Produce recommended review steps
8. Require human verification
```

## Plain-Language Alert Summary

Security alerts frequently contain technical fields that may be difficult for a new analyst or business user to understand.

The MVP converts those fields into a structured explanation describing:

- What event was detected
- Which endpoint generated the alert
- When the activity occurred
- Which Wazuh rule matched
- How serious the alert may be
- What evidence should be reviewed next

The generated summary supports investigation but does not replace analyst judgment.

## Severity Explanation

The Wazuh rule level is used to provide basic severity context.

The tool explains that higher rule levels generally deserve greater attention, while lower-level events may represent normal activity, informational events, or activity that requires additional context before escalation.

Severity alone is not treated as proof of malicious behavior.

The analyst must also consider:

- The affected system
- The event source
- The user or process involved
- Related alerts
- Expected business activity
- Previous endpoint behavior
- Available supporting evidence

## Analyst Context

The tool adds context intended to help a beginning analyst understand why the alert may deserve review.

The context focuses on questions such as:

- Is the activity expected on this endpoint?
- Did the event occur at an unusual time?
- Are related events present?
- Does the event match an approved administrative action?
- Is the alert isolated or part of a larger pattern?
- Is additional endpoint or log evidence available?

This helps move the output beyond merely repeating the raw alert description.

## Recommended Review Steps

The MVP provides practical next steps such as:

1. Confirm the endpoint and alert timestamp
2. Review the full Windows event details
3. Check for related Wazuh alerts
4. Identify the user, application, or process involved
5. Compare the activity with expected system behavior
6. Review additional endpoint or authentication evidence
7. Document findings
8. Escalate only when the available evidence supports it

The recommendations are investigative rather than automatic response actions.

## Human Review Requirement

The tool does not automatically block accounts, isolate systems, terminate processes, delete files, or make final incident decisions.

All output must be reviewed by a person before action is taken.

```text
AI-assisted output supports the analyst.
It does not replace the analyst.
```

This control is important because alert data may be incomplete, misleading, or missing important business context.

## Error Handling

The tool was designed to handle common data problems, including:

- Missing JSON files
- Invalid JSON formatting
- Missing alert fields
- Empty values
- Unexpected field structures

Readable error messages make troubleshooting easier and prevent the program from failing without explanation.

## Testing and Validation

The completed script was tested using the sanitized alert sample created during Lab 10.

Validation confirmed that the tool could:

- Open the JSON data
- Extract selected fields
- Interpret the alert level
- Produce a structured explanation
- Display recommended investigation steps
- Preserve the requirement for human review

The generated output was reviewed manually to ensure it remained consistent with the original Wazuh alert data.

## Security and Privacy

This lab followed these rules:

- Only sanitized alert data was used
- No Wazuh passwords or administrator credentials were included
- No API keys or access tokens were stored in the project
- No real customer, financial, City, employer, or production data was used
- Internal lab data was reviewed before publication
- The tool does not perform automatic containment or remediation
- Human approval remains required
- Screenshots were reviewed before being added to GitHub
- Public source files are checked for sensitive paths and personal information

## Limitations

This MVP has several intentional limitations:

- It processes a prepared alert sample rather than a live Wazuh feed
- Its explanations depend on the fields present in the input data
- It does not independently verify whether activity is malicious
- It does not correlate multiple alerts
- It does not replace a trained security analyst
- It does not take automatic response actions
- It requires additional testing with other alert types
- Its severity explanation is general and must be combined with business context

Documenting these limitations helps prevent the tool from being presented as more capable than it is.

## Importance

Security platforms generate detailed alerts, but the raw information may not be immediately understandable to every analyst or business stakeholder.

This project demonstrates how Python can transform structured security data into a clearer explanation while preserving human review and responsible decision-making.

The lab also connects several Project Athenaeum skills:

- Wazuh monitoring
- Windows telemetry
- JSON analysis
- Python programming
- Alert triage
- Technical communication
- AI-assisted decision support
- Documentation and verification

## Lessons Learned

This lab demonstrated that the quality of an alert explanation depends on the quality of the input data.

Selecting a smaller set of useful fields made the final explanation easier to understand than simply displaying the full Wazuh JSON record.

The project also reinforced the value of separating the alert-processing workflow into smaller functions. This made the code easier to read, test, troubleshoot, and improve.

Most importantly, the lab demonstrated that AI-assisted security tools should support human reasoning rather than replace it. Clear limitations, verification steps, and approval controls are necessary when building tools that influence security decisions.

## Documentation Created

The following Lab 11 documentation was completed and retained locally:

- `AJ_Chapa_Lab_11_AI_Alert_Explainer_MVP_Notes_v1.0.docx`
- Lab 11 screenshot log
- Sanitized Wazuh JSON alert sample
- Python alert-explainer script
- Generated explanation output
- Supporting screenshots
- Final portfolio documentation

## Future Development

Later versions may include:

- Processing additional Wazuh alert types
- Accepting multiple alert files
- Comparing related alerts
- Creating reusable severity mappings
- Exporting explanations to text or JSON
- Generating incident-summary templates
- Adding a simple graphical interface
- Connecting to a local or approved AI model
- Adding validation rules for AI-generated explanations
- Creating analyst feedback and correction controls
- Measuring explanation accuracy
- Building a simplified Business Guardian dashboard

## Status

**Technical work and local documentation completed; GitHub files and evidence upload in progress**
