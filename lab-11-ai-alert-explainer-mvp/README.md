# Lab 11 — AI Alert Explainer MVP

## Can Python Make a Security Alert Easier to Understand?

Lab 10 proved that the Windows workstation could generate an event, Wazuh could detect it, and the resulting security data could be reviewed and sanitized.

That left a practical problem:

**Security alerts can contain a lot of technical information. How do you turn that data into something an analyst can quickly understand?**

Lab 11 builds the first functional security-analysis tool in Project Athenaeum.

Using Python and the sanitized Wazuh alert prepared in Lab 10, the MVP extracts selected security fields, interprets the available context, and produces a structured plain-language report.

The progression becomes:

```text
Windows Event
     ↓
Wazuh Detection
     ↓
Sanitized Alert Data
     ↓
Python Processing
     ↓
Plain-Language Security Report
     ↓
Human Review
```

This is the first point in Project Athenaeum where monitored security data becomes input for a custom security tool.

---

# A Note About the "AI" in AI Alert Explainer

The project is called the **AI Alert Explainer**, but this first MVP does not use an external AI model, machine-learning system, or API.

Its explanations are generated through:

- Structured field extraction
- Python functions
- Conditional logic
- Predefined severity rules
- Formatted analyst guidance

That is intentional.

Before adding AI-assisted capabilities later, I wanted a deterministic processing foundation whose behavior could be understood and tested.

So Lab 11 is best understood as:

> **The working alert-processing foundation that later AI-assisted capabilities can build on.**

---

# What the MVP Does

The Lab 11 processor:

- Locates the sanitized alert-data file
- Confirms that the input exists
- Confirms that the file contains data
- Reads selected `key: value` fields
- Ignores unsupported content
- Extracts endpoint information
- Extracts Windows event information
- Extracts Wazuh rule information
- Interprets the Wazuh rule level
- Builds a structured explanation
- Writes the result to an output file
- Recommends analyst review steps
- Requires human review before any security decision

The goal is not to automate the analyst out of the workflow.

The goal is to make the alert easier to understand.

---

# From Lab 10 Data to a Python Tool

Lab 10 produced the sanitized alert sample used here.

The relationship is:

```text
Lab 10
Controlled Windows Event
        ↓
Wazuh Alert
        ↓
Alert Reviewed
        ↓
Selected Fields Sanitized
        ↓
Lab 11
Python Reads the Data
        ↓
Security Context Extracted
        ↓
Explanation Generated
```

The original Wazuh server does not need to remain connected for this MVP.

Lab 11 works from the sanitized alert evidence already collected and reviewed.

<p align="center">
  <img
    src="screenshots/2026-07-29_Lab11_AIAlertExplainer_05_data-sample-copied-to-ai-folder.png"
    alt="Sanitized Lab 10 Wazuh alert sample prepared for Lab 11"
    width="850">
</p>

<p align="center">
  <em>The sanitized Wazuh sample from Lab 10 becomes the input for the first Python alert-processing workflow.</em>
</p>

---

# The Input

The MVP reads a sanitized text file containing selected Wazuh fields in a consistent:

```text
key: value
```

format.

The current version recognizes:

```text
agent.name
agent.ip
manager.name
data.win.system.eventID
data.win.system.providerName
data.win.system.severityValue
data.win.system.message
rule.description
rule.id
rule.level
rule.groups
decoder.name
location
```

Anything outside the expected field list is ignored.

That includes:

- Blank lines
- Lines without a colon
- Unsupported fields
- Unnecessary alert information

This keeps the MVP focused on the information needed for the explanation instead of copying an entire alert into the report.

---

# What the Tool Extracts

The selected fields are organized into several types of analyst context.

## Endpoint Context

The report identifies:

- Monitored workstation
- Endpoint IP address
- Wazuh manager

## Windows Event Context

It extracts:

- Event ID
- Event provider
- Windows severity
- Event message

## Wazuh Rule Context

It includes:

- Rule description
- Rule ID
- Rule level
- Rule groups
- Decoder
- Event location

The purpose is to turn scattered alert fields into a more readable security narrative.

---

# The Processing Workflow

The MVP follows a straightforward sequence:

```text
1. Locate the sanitized alert file
2. Confirm the file exists
3. Confirm the file contains data
4. Read expected key-value fields
5. Store selected alert information
6. Extract endpoint and event context
7. Interpret the Wazuh rule level
8. Build the explanation
9. Write the report
10. Display completion or error status
11. Require human review
```

The code is divided into smaller functions so file handling, severity interpretation, explanation generation, and program execution have clear responsibilities.

---

# Running the MVP

The public Lab 11 project contains:

- [`Lab11_AI_Alert_Explainer_MVP.py`](Lab11_AI_Alert_Explainer_MVP.py)
- [`Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt`](Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt)
- [`Lab11_Alert_Explanation_Output.txt`](Lab11_Alert_Explanation_Output.txt)

Keep the files together and run:

```powershell
python Lab11_AI_Alert_Explainer_MVP.py
```

A successful execution displays:

```text
AI Alert Explainer MVP completed successfully.
Input file: Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt
Output file: Lab11_Alert_Explanation_Output.txt
```

<p align="center">
  <img
    src="screenshots/2026-07-29_Lab11_AIAlertExplainer_07_script-ran-successfully.png"
    alt="Lab 11 AI Alert Explainer successful Python execution"
    width="900">
</p>

<p align="center">
  <em>The first complete execution successfully read the sanitized alert sample and created the expected report.</em>
</p>

---

# Turning Alert Data Into a Report

Successful execution generates:

```text
Lab11_Alert_Explanation_Output.txt
```

The report contains:

- Alert summary
- Windows event context
- Wazuh rule context
- Severity explanation
- Analyst context
- Recommended review steps
- Final assessment

<p align="center">
  <img
    src="screenshots/2026-07-29_Lab11_AIAlertExplainer_08_output-file-created.png"
    alt="Lab 11 generated alert explanation output file"
    width="850">
</p>

<p align="center">
  <em>The Python processor creates a separate explanation file from the sanitized source alert.</em>
</p>

---

# What the Generated Report Looks Like

The report is designed to answer several basic analyst questions.

## What Happened?

The alert summary identifies the monitored endpoint and the Wazuh rule that matched.

## What Windows Event Was Involved?

The event section provides the Windows event ID, provider, severity value, and message.

## Why Did Wazuh Care?

The Wazuh section presents the rule ID, rule level, groups, decoder, and location.

## How Important Might It Be?

The severity section converts the Wazuh rule level into simpler analyst-facing language.

## What Should Be Reviewed Next?

The report provides practical investigation steps rather than automatically taking action.

<p align="center">
  <img
    src="screenshots/2026-07-29_Lab11_AIAlertExplainer_09_output-report-viewed.png"
    alt="Lab 11 generated alert explanation report"
    width="900">
</p>

<p align="center">
  <em>The final report reorganizes selected alert evidence into a more readable analyst-oriented explanation.</em>
</p>

---

# First Severity Logic

The original MVP interprets Wazuh rule levels using simple deterministic ranges:

```text
Level 10 or higher
→ High-severity alert that should be reviewed quickly

Level 7 through 9
→ Notable alert that should be reviewed by an analyst

Level 4 through 6
→ Medium-level alert that may require review depending on context

Level 0 through 3
→ Low-level alert that may represent normal system activity
```

If the rule level cannot be converted into a number, the tool does not invent one.

Instead, severity requires manual review.

This early severity system is intentionally simple.

Later labs improve the architecture by separating Wazuh's source severity from a vendor-neutral normalized severity model.

---

# Severity Is Not Proof

Even in this first MVP, severity alone is not treated as proof that an event is malicious.

An analyst may also need to consider:

- The affected endpoint
- Event provider
- Windows event ID
- Event message
- Related alerts
- Expected system activity
- User activity
- Process information
- Business context

That distinction becomes increasingly important as Project Athenaeum develops into later triage and investigation workflows.

---

# Recommended Review Steps

The generated report recommends that an analyst:

1. Confirm whether the event was expected
2. Check whether the same event repeats
3. Review the provider, event ID, and endpoint
4. Look for related alerts before deciding whether escalation is needed

These are investigation suggestions.

They are not automated response actions.

---

# The Human Still Makes the Decision

The MVP does not automatically:

- Block an account
- Isolate an endpoint
- Terminate a process
- Delete a file
- Change firewall rules
- Close an alert
- Escalate an incident
- Make a final security decision

The design rule is:

```text
The tool supports the analyst.
It does not replace the analyst.
```

That boundary matters because security alerts can be incomplete, misleading, or missing important context that software does not have.

---

# Error Handling

The first MVP also includes basic protections for common input problems.

It checks for:

- Missing input files
- Empty input files
- No recognized alert fields
- Rule levels that cannot be converted to numbers
- Unexpected processing errors
- Output-writing errors

Readable console messages indicate whether execution succeeded or explain what went wrong.

This error handling becomes the focus of more deliberate testing in Lab 12.

---

# Initial Validation

The completed MVP was tested using the sanitized Lab 10 Wazuh alert.

Validation confirmed that it could:

- Locate the expected alert-data file
- Confirm that the file contained data
- Parse the selected key-value fields
- Extract endpoint information
- Extract Windows event information
- Extract Wazuh rule information
- Interpret the rule level
- Generate a structured explanation
- Write the explanation to an output file
- Provide recommended review steps
- Preserve human review

The generated report was manually compared against the source alert sample to confirm that the explanation remained consistent with the available evidence.

## Initial Validation Status

| Validation Area | Result |
| --- | --- |
| Python execution | **PASS** |
| Input file located | **PASS** |
| Expected fields parsed | **PASS** |
| Endpoint context extracted | **PASS** |
| Windows event context extracted | **PASS** |
| Wazuh rule context extracted | **PASS** |
| Severity explanation generated | **PASS** |
| Output file created | **PASS** |
| Human review preserved | **PASS** |

Lab 12 later expands this testing to abnormal and failure conditions.

---

# What This MVP Does Not Do

Lab 11 is intentionally limited.

It:

- Processes one prepared alert at a time
- Reads structured text rather than a full Wazuh JSON record
- Does not connect directly to live Wazuh
- Does not use an external AI model
- Does not use a machine-learning model
- Uses predefined Python explanation logic
- Depends on the fields available in the input sample
- Does not correlate multiple alerts
- Does not independently determine malicious intent
- Does not validate related users, processes, or network activity
- Does not execute response actions
- Requires human review

Those limitations are not hidden.

They define the starting point from which later labs grow.

---

# Security and Privacy

The MVP was built entirely with authorized, sanitized lab data.

The public project contains:

- No Wazuh administrator credentials
- No passwords
- No API keys
- No access tokens
- No customer information
- No financial information
- No employer or production security data
- No external AI processing of the alert sample

All activity occurred on personally owned and authorized systems.

The input and screenshots were reviewed before publication.

---

# What Lab 11 Proves

Lab 11 demonstrates that Python can take selected security-alert fields and reorganize them into a clearer analyst-facing report.

It combines:

- Wazuh monitoring
- Windows telemetry
- Structured data parsing
- Python programming
- Severity interpretation
- Technical communication
- Security review guidance

But the most important accomplishment is not the report itself.

It is the transition:

```text
Security Data
     ↓
Programmatic Processing
     ↓
Human-Readable Context
```

Project Athenaeum is no longer only collecting security evidence.

It is starting to build tools that can work with that evidence.

---

# Skills Demonstrated

- Python fundamentals
- Functions
- Conditional logic
- File input and output
- Structured text parsing
- Security-data processing
- Wazuh alert interpretation
- Windows event analysis
- Field extraction
- Error handling
- Severity interpretation
- Plain-language technical communication
- Analyst workflow design
- Human-in-the-loop decision support
- Testing and troubleshooting
- Privacy-conscious data handling
- Technical documentation

---

# Where the Project Goes From Here

Lab 10 answered:

**Can the lab generate, detect, inspect, and sanitize real security-event data?**

Lab 11 answered:

**Can I write a Python tool that turns selected alert data into a clearer analyst report?**

The answer was yes.

But one successful execution creates another question:

**What happens when the input is not perfect?**

What if:

- The file is missing?
- The file is empty?
- An expected field disappears?
- Severity changes?

[Lab 12 — AI Alert Explainer Testing and Validation](../lab-12-ai-alert-explainer-testing-validation/README.md) takes the working Lab 11 MVP, preserves it as a stable baseline, and deliberately tests those failure conditions.

The progression becomes:

```text
Wazuh Alert
     ↓
Python Alert Explainer
     ↓
Working MVP
     ↓
Controlled Failure Testing
     ↓
Validated Baseline
```

Lab 11 is where Project Athenaeum makes an important transition:

**from reviewing security data to building software that can help explain it.**
