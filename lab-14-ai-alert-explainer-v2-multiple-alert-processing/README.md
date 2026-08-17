# Lab 14: AI Alert Explainer v2 Multiple Alert Processing

## Overview

Lab 14 implements the requirements and technical design established during Lab 13 and extends the validated AI Alert Explainer foundation created in Labs 11 and 12.

The original MVP processed one sanitized Wazuh alert at a time. Lab 14 moves the project to a controlled multiple-alert processing workflow capable of discovering several supported alert files during one execution, translating source-specific information into a normalized alert structure, validating each alert independently, generating individual analyst reports, and producing a batch-level summary.

The implementation preserves the previously validated MVP rather than replacing it. Labs 11 and 12 remain the historical baseline, while Lab 14 establishes the first validated multiple-alert processing baseline.

Lab 14 also continues the vendor-neutral design direction established in Lab 13. Wazuh remains the first supported alert source, but source-specific fields are translated into a common internal structure rather than becoming the permanent architecture of the application.

Core parsing, normalization, validation, severity translation, report generation, and processing decisions remain deterministic and testable.

## Objective

The objective of Lab 14 was to implement and validate the first version of the AI Alert Explainer v2 multiple-alert processing architecture.

The implementation needed to:

* Process multiple supported alert files during one execution
* Preserve source alert files without modification
* Translate supported Wazuh data into a normalized internal alert structure
* Apply platform-neutral severity categories
* Detect missing or malformed information
* Distinguish normal processing, warning conditions, and failed validation
* Continue processing when an individual alert fails
* Generate unique reports for processable alerts
* Create one batch summary for each processing run
* Preserve traceability between source alerts and generated reports
* Prevent previous output from being overwritten
* Require human review rather than automatically declaring alerts benign, malicious, confirmed, or resolved
* Match the deterministic validation target established before implementation in Lab 13

## Project Progression

Project Athenaeum preserves validated work and extends it rather than rebuilding completed components.

The AI Alert Explainer progression is:

* **Lab 10:** Collected and sanitized structured Wazuh alert data
* **Lab 11:** Built the single-alert AI Alert Explainer MVP
* **Lab 12:** Tested and validated the MVP
* **Lab 13:** Designed AI Alert Explainer v2 before additional coding
* **Lab 14:** Implemented and validated multiple-alert processing

Labs 11 and 12 remain preserved as the validated MVP baseline.

Lab 14 implements the controlled scope frozen during Lab 13 rather than retroactively changing earlier labs.

## Environment and Tools

Lab 14 was completed in the existing Project Athenaeum development environment using:

* Windows 11
* Python
* Visual Studio Code
* Windows File Explorer
* PowerShell
* Sanitized Wazuh alert data
* Synthetic security-alert test data
* Existing Lab 11 parsing and file-handling concepts
* Lab 13 v2 requirements and design documentation

All alert samples used for the lab were sanitized or synthetic.

No production systems, customer systems, employer systems, or unauthorized security data were used.

## Project Files

The public Lab 14 implementation includes the working Python application, complete controlled validation input set, selected generated output, validation results, and sanitized portfolio evidence.

### Application

* [Lab 14 Python Application](Lab14_AI_Alert_Explainer_v2.py)
* [Lab 14 Validation Results](Lab14_AI_Alert_Explainer_v2_Validation_Results.txt)

### Validation Inputs

The complete five-alert controlled validation set is available in the [`input`](input/) folder.

* [Input Folder Documentation](input/README.md)
* [Alert 001 — Windows Application Error](input/alert_001_windows_application_error.txt)
* [Alert 002 — Higher-Severity Alert](input/alert_002_high_severity.txt)
* [Alert 003 — Missing Fields](input/alert_003_missing_fields.txt)
* [Alert 004 — Invalid Severity](input/alert_004_invalid_severity.txt)
* [Alert 005 — Invalid Content](input/alert_005_invalid_content.txt)

### Representative Generated Output

Selected output from the validated processing workflow is available in the [`output`](output/) folder.

* [Output Folder Documentation](output/README.md)
* [Validated Batch Summary](output/batch_summary_20260817_105319.txt)
* [Missing-Fields Report](output/alert_003_missing_fields_report_20260817_124241.txt)
* [Malformed-Severity Report](output/alert_004_invalid_severity_report_20260817_124241.txt)

The complete local output set is intentionally not published. These representative artifacts demonstrate the validated processing behavior without unnecessarily duplicating every generated report.

### Portfolio Evidence

* [Screenshot Evidence Folder](screenshots/)
* [Screenshot Documentation](screenshots/README.md)

Six selected sanitized screenshots are published from the complete 54-screenshot internal documentation record.

## Workspace Structure

Lab 14 introduced separate input and output locations for the v2 processing workflow.

The public project structure is:

```text
lab-14-ai-alert-explainer-v2-multiple-alert-processing/
├── README.md
├── Lab14_AI_Alert_Explainer_v2.py
├── Lab14_AI_Alert_Explainer_v2_Validation_Results.txt
├── input/
│   ├── README.md
│   ├── alert_001_windows_application_error.txt
│   ├── alert_002_high_severity.txt
│   ├── alert_003_missing_fields.txt
│   ├── alert_004_invalid_severity.txt
│   └── alert_005_invalid_content.txt
├── output/
│   ├── README.md
│   ├── batch_summary_20260817_105319.txt
│   ├── alert_003_missing_fields_report_20260817_124241.txt
│   └── alert_004_invalid_severity_report_20260817_124241.txt
└── screenshots/
    ├── README.md
    └── six selected sanitized screenshots
```

This structure separates source input, generated output, application code, validation evidence, and portfolio screenshots.

## Multiple-Alert Discovery

The v2 workflow discovers multiple supported `.txt` alert files from the designated input location.

Supported files are processed in predictable filename order.

This allows several alerts to be evaluated during one controlled execution rather than requiring the program to be run manually for every alert.

Source alert files are not modified during processing.

## Wazuh Source Handling

Wazuh is the first supported security-data source for the v2 architecture.

Lab 14 introduces an initial Wazuh source-handling layer that reads supported source fields and translates them into the common normalized alert model.

This prevents shared downstream processing from permanently depending on Wazuh-specific field names.

The goal is not to remove Wazuh support. The design allows additional security platforms to eventually provide data to the same normalized processing workflow through their own source-specific translation layers.

## Normalized Alert Model

Supported source data is translated into a common normalized alert structure.

The normalized model provides consistent internal representations for information such as:

* Alert source
* Endpoint identity
* Endpoint IP address
* Event identifiers
* Event provider
* Event message
* Source rule information
* Original source severity
* Normalized severity
* Missing fields
* Validation notes
* Processing outcome
* Review status
* Source traceability

Recognized source information is retained so the normalized representation does not eliminate traceability back to the original data.

## Normalized Severity

Lab 14 uses platform-neutral severity categories instead of treating Wazuh numeric rule levels as the permanent internal severity model.

Supported normalized categories are:

* `INFORMATIONAL`
* `LOW`
* `MEDIUM`
* `HIGH`
* `CRITICAL`
* `UNKNOWN`

A malformed, missing, or unsupported source severity is not guessed.

When valid translation cannot be completed, the normalized severity becomes:

```text
UNKNOWN
```

The original source value remains preserved for traceability.

Severity determines review priority. It does not automatically determine whether an alert is benign, malicious, confirmed, or resolved.

## Validation Outcomes

Every discovered alert is evaluated independently.

Lab 14 supports three validation outcomes.

### Processed Normally

The alert contains the supported information required for normal processing and an individual analyst report can be generated.

### Processed With Warnings

The alert contains enough supported information to produce a report, but missing, malformed, or uncertain information requires additional analyst attention.

An individual report is generated and the validation issue is documented.

### Failed Validation

The input does not contain enough recognized supported alert information to safely generate an individual analyst report.

The failure is recorded in the batch results, but no individual analyst report is created.

A failed alert does not stop the remaining alerts from being processed.

## Review Status

All processable alerts default to:

```text
Requires Review
```

The application does not automatically mark an alert as:

* Benign
* Malicious
* Confirmed
* Resolved

Those conclusions require sufficient evidence and human judgment.

This prevents the processing layer from presenting unsupported security conclusions as facts.

## Missing-Field Handling

Missing supported information is explicitly reported.

For example, if a source alert does not contain a supported endpoint IP address or event provider, those normalized fields are recorded as unavailable rather than receiving fabricated replacement values.

Missing expected information may cause an alert to receive:

```text
Processed With Warnings
```

when enough other supported information remains available for meaningful processing.

## Malformed-Value Handling

Malformed information is handled separately from missing information.

For example:

```text
rule.level: invalid
```

is not treated as though the severity field were absent.

The original malformed value remains preserved, the normalized severity becomes:

```text
UNKNOWN
```

and a validation note records that the source value could not be interpreted reliably.

This preserves the distinction between:

* Information that is missing
* Information that exists but cannot be safely interpreted

## Per-Alert Failure Isolation

Lab 14 isolates alert-processing failures.

If one alert fails validation, the application records that failure and continues processing the remaining supported files.

This prevents one malformed or unsupported alert from stopping the complete batch.

Failure isolation is an important reliability improvement over an all-or-nothing processing workflow.

## Individual Reports

Every processable alert receives its own analyst report.

Individual reports provide:

* Processing run information
* Original source filename
* Validation status
* Review status
* Alert summary
* Endpoint context
* Event context
* Source security context
* Original source severity
* Normalized severity
* Severity explanation
* Missing-field information
* Validation notes
* Analyst review guidance
* Safe assessment language
* Source traceability

Failed-validation inputs do not receive individual analyst reports.

## Batch Summary

Each complete processing execution creates one batch summary.

The batch summary records:

* Processing run identifier
* Input and output locations
* Total supported alert files discovered
* Successfully processed alerts
* Alerts processed with warnings
* Failed alerts
* Individual reports created
* Per-alert processing results
* Validation status
* Normalized severity
* Report creation status
* Failure reason when applicable
* Batch-completion status

Batch totals are calculated from the actual collected results.

They are not hard-coded to match the expected test result.

## Overwrite Protection

Lab 14 includes overwrite protection for:

* Individual alert reports
* Batch-summary reports

Generated filenames use the processing-run timestamp.

If a filename collision still occurs, a numeric suffix is added rather than overwriting an existing file.

A second complete validation execution created a new set of output files while preserving the first-run results.

## Controlled Validation Set

Five sanitized or synthetic alert samples were used to validate the Lab 14 architecture.

### Test 1 — Baseline Windows Application Error

File:

[`alert_001_windows_application_error.txt`](input/alert_001_windows_application_error.txt)

Purpose:

* Reuse the sanitized alert sample from the validated Lab 11 workflow
* Confirm compatibility with the v2 architecture

Source severity:

```text
9
```

Normalized severity:

```text
MEDIUM
```

Expected outcome:

```text
Processed Normally
```

### Test 2 — Higher-Severity Alert

File:

[`alert_002_high_severity.txt`](input/alert_002_high_severity.txt)

Purpose:

* Test a synthetic higher-severity authentication alert
* Validate higher-severity translation

Source severity:

```text
11
```

Normalized severity:

```text
HIGH
```

Expected outcome:

```text
Processed Normally
```

### Test 3 — Missing Fields

File:

[`alert_003_missing_fields.txt`](input/alert_003_missing_fields.txt)

The alert deliberately omits supported information corresponding to:

```text
endpoint_ip
event_provider
```

Source severity:

```text
5
```

Normalized severity:

```text
LOW
```

Expected outcome:

```text
Processed With Warnings
```

Purpose:

* Confirm that missing information is reported rather than fabricated
* Confirm that an incomplete but still processable alert can generate an analyst report

Representative generated output:

[Missing-Fields Report](output/alert_003_missing_fields_report_20260817_124241.txt)

### Test 4 — Malformed Severity

File:

[`alert_004_invalid_severity.txt`](input/alert_004_invalid_severity.txt)

Source value:

```text
rule.level: invalid
```

Normalized severity:

```text
UNKNOWN
```

Expected outcome:

```text
Processed With Warnings
```

Purpose:

* Preserve the malformed source value
* Avoid guessing a replacement severity
* Record the issue in validation notes
* Distinguish malformed information from missing information

Representative generated output:

[Malformed-Severity Report](output/alert_004_invalid_severity_report_20260817_124241.txt)

### Test 5 — Unsupported / Invalid Content

File:

[`alert_005_invalid_content.txt`](input/alert_005_invalid_content.txt)

Purpose:

* Test input containing no recognized supported Wazuh alert fields
* Confirm safe failure behavior
* Confirm that remaining alerts continue processing

Expected outcome:

```text
Failed Validation
```

Expected individual analyst report:

```text
None
```

## Lab 13 Validation Target

Before Lab 14 implementation began, Lab 13 established the following deterministic acceptance criteria:

```text
Total Supported Alert Files Discovered: 5
Successfully Processed: 2
Processed With Warnings: 2
Failed: 1
Individual Reports Created: 4
Batch Summaries Created: 1
```

The expected result was frozen before implementation so Lab 14 could be tested against a predetermined target rather than adjusting expectations after coding.

## Observed Lab 14 Results

The first validated processing run was:

```text
20260817_105319
```

Observed result:

```text
Total Supported Alert Files Discovered: 5
Successfully Processed: 2
Processed With Warnings: 2
Failed: 1
Individual Reports Created: 4
Batch Summaries Created: 1
```

This was an exact match with the acceptance criteria established during Lab 13.

The published batch record is available here:

[Validated Batch Summary](output/batch_summary_20260817_105319.txt)

## Second Validation Run

A second complete processing run was performed to validate repeatability and overwrite protection:

```text
20260817_110753
```

The second run produced the same processing result:

```text
5 alerts discovered
2 processed normally
2 processed with warnings
1 failed validation
4 individual reports
1 batch summary
```

The first-run output files remained intact after the second execution.

## Validation Results

Lab 14 successfully validated the following behaviors:

* Five supported alert files were discovered
* Two alerts were processed normally
* Two alerts were processed with warnings
* One alert failed validation
* Four individual analyst reports were created
* One batch summary was created per run
* One failed alert did not stop the remaining alerts
* Missing information was reported instead of fabricated
* Malformed severity was preserved rather than guessed
* Malformed severity normalized to `UNKNOWN`
* Malformed information was recorded in validation notes
* Missing and malformed information were treated differently
* Failed validation generated no individual analyst report
* Source alert files remained unchanged
* Source traceability was preserved
* All processable alerts received unique reports
* Batch summaries received unique filenames
* Batch totals were calculated from actual processing results
* A second execution created a separate set of outputs
* First-run output remained intact
* The reused Lab 11 alert remained compatible with the v2 architecture
* All processable alerts retained the default `Requires Review` status

The complete public validation record is available here:

[Lab14_AI_Alert_Explainer_v2_Validation_Results.txt](Lab14_AI_Alert_Explainer_v2_Validation_Results.txt)

## Portfolio Evidence

Only a selected subset of the complete Lab 14 screenshot record is published publicly.

The internal Lab 14 Screenshot Log contains all 54 screenshots captured during development, testing, and validation.

The public repository uses six selected sanitized screenshots that demonstrate the strongest technical evidence.

### Multiple-Alert Batch Processing

![Multiple-alert batch processing](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_29_multiple-alert-batch-processing.png)

Demonstrates the core multiple-alert batch-processing implementation and the transition from the validated single-alert MVP to the v2 workflow.

### First Successful Batch Execution

![First successful batch execution](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_45_first-batch-execution-success.png)

Shows the first successful complete execution of the five-alert validation set and the expected `5 / 2 / 2 / 1 / 4` result.

### Validated Batch Summary

![Validated batch summary](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_47_validated-batch-summary.png)

Shows the batch-level processing record and the outcome of each controlled alert sample.

### Missing-Field Validation

![Missing-field validation](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_50_report3-missing-fields-validation.png)

Demonstrates safe processing of an incomplete alert, including explicit missing-field reporting without fabricated information.

### Malformed-Severity Validation

![Malformed-severity validation](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_51_report4-malformed-severity-validation.png)

Demonstrates preservation of malformed source severity, normalization to `UNKNOWN`, and explicit validation reporting.

### Overwrite-Protection Validation

![Overwrite-protection validation](screenshots/2026-08-17_Lab14_AIAlertExplainerV2_54_overwrite-protection-validation.png)

Demonstrates repeatable execution and preservation of previous reports through unique output filenames.

## Key Improvements Over the MVP

Lab 14 extends the validated single-alert MVP with:

* Multiple-alert processing
* Separate input and output locations
* Predictable file discovery
* Vendor-neutral normalized alert data
* Initial Wazuh source translation
* Platform-neutral severity
* Missing-field detection
* Malformed-value validation
* Explicit processing outcomes
* Per-alert failure isolation
* Default human-review status
* Modular report generation
* Unique report filenames
* Batch-level reporting
* Actual-result-derived totals
* Non-destructive input handling
* Source traceability
* Overwrite protection
* Repeatable validation

These improvements were added without modifying or replacing the validated Lab 11 and Lab 12 baseline.

## Development Principles Demonstrated

Lab 14 follows the broader Project Athenaeum development approach:

* Preserve validated work rather than rebuilding it unnecessarily
* Extend existing components when practical
* Define acceptance criteria before implementation
* Keep source-specific information separate from reusable processing logic
* Use deterministic logic for core parsing, validation, normalization, severity handling, and control decisions
* Report missing information rather than inventing values
* Preserve malformed information for traceability
* Isolate individual failures
* Preserve source evidence
* Protect previous output
* Test before publication
* Require human review for consequential security conclusions

## Security and Reliability Considerations

Lab 14 intentionally avoids unsupported security conclusions.

The application does not assume that:

* A high-severity alert is malicious
* A low-severity alert is safe
* Missing data can be safely guessed
* A malformed value should be silently replaced
* A generated report means an incident is resolved

Instead, the processing layer organizes and validates available information and identifies conditions requiring additional review.

The architecture is intended to support later investigation and controlled-response capabilities without embedding those future capabilities into the Lab 14 baseline.

## Public Repository Boundary

Lab 14 is published as a sanitized Project Athenaeum portfolio project.

The public repository demonstrates:

* Python programming
* Multiple-file processing
* Security-data normalization
* Source-specific translation
* Validation logic
* Safe error handling
* Deterministic testing
* Report generation
* Batch processing
* Failure isolation
* Traceability
* Repeatability
* Overwrite protection
* Human-review requirements

Business Guardian product-level implementation remains private.

The public Lab 14 project does not expose proprietary:

* Remediation logic
* Investigation workflows
* Policy engines
* Approval mechanisms
* Advanced backend architecture
* Customer or tenant logic
* Sensitive security data
* Secrets-related configuration
* Commercial workflows
* Production infrastructure
* Product-specific automation

## Lessons Learned

Lab 14 demonstrated that reliable multiple-alert processing requires more than placing a loop around the original single-alert program.

Safe batch processing requires:

* Clear source boundaries
* Normalized internal data
* Independent validation
* Failure isolation
* Explicit warning conditions
* Traceability
* Unique output handling
* Repeatable testing
* Preserved source evidence

The lab also reinforced the importance of defining acceptance criteria before implementation.

Because the expected `5 / 2 / 2 / 1 / 4` result was established during Lab 13, Lab 14 could be evaluated against a measurable target rather than relying on subjective observations after development was complete.

## Future Development

Lab 14 establishes the validated multiple-alert processing baseline.

Future Project Athenaeum work may extend this foundation with portfolio-safe capabilities such as:

* Additional controlled alert types
* Expanded normalized source fields
* Complete JSON parsing
* Additional security-platform adapters
* Improved data-quality validation
* Structured processing records
* Multiple-alert correlation
* Reusable report components
* Context-aware investigation guidance
* Evidence-collection workflows
* Structured incident reporting
* Human-approved security workflows
* Browser-based dashboard development
* AI-assisted explanation and enrichment

Future capabilities will be built as separate controlled development stages rather than retroactively added to Lab 14.

## Status

**Technical Implementation: COMPLETE**

**Controlled Validation: PASS**

**Expected Result: MATCHED**

**Repeatability Validation: PASS**

**Overwrite Protection: PASS**

**Multiple-Alert Processing Baseline: ESTABLISHED**

**Public Portfolio Publication: COMPLETE**
