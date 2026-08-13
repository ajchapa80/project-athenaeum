# Lab 13: AI Alert Explainer v2 Requirements and Design

## Overview

Lab 13 defines the requirements and technical design for the next version of the Project Athenaeum AI Alert Explainer.

Lab 11 created the first functional Python-based alert explanation MVP. Lab 12 then tested and validated that MVP under normal and abnormal input conditions while preserving the published version as a stable baseline.

Rather than modifying the working MVP immediately, Lab 13 uses the Lab 12 findings to design the next version before implementation begins.

No production v2 code was developed during this lab.

## Objective

Create a clear, testable, and implementation-ready design for AI Alert Explainer v2 while preserving the validated Lab 11 MVP and Lab 12 testing baseline.

The design focuses on improving reliability, scalability, data handling, and analyst usability without prematurely introducing dashboard, automation, or commercial product features.

## Project Progression

```text
Lab 11
AI Alert Explainer MVP
        |
        v
Lab 12
Testing and Validation
        |
        v
Lab 13
Requirements and Design
        |
        v
Lab 14
Controlled v2 Implementation
```

## Design Principles

The v2 design follows several core principles:

* Preserve the validated Lab 11 MVP as a stable reference
* Use Lab 12 testing results to justify improvements
* Design before changing production code
* Process multiple alerts without allowing one failure to stop the entire batch
* Separate input data from generated output
* Normalize vendor-specific alert data before explanation logic
* Handle missing fields safely
* Prevent accidental report overwrites
* Maintain clear human-review requirements
* Keep testing repeatable
* Avoid unnecessary complexity during the first v2 implementation

## Requirements Identified

Lab 12 demonstrated that the MVP works but also identified areas that should be improved before the tool expands.

The v2 design includes the following requirements.

### Multiple Alert Processing

The current MVP processes one prepared alert sample at a time.

Version 2 should:

* Read multiple alert files from an input directory
* Process each alert independently
* Continue processing if one alert fails
* Generate one explanation report per alert
* Produce a summary of the batch-processing results

### Separate Input and Output Directories

The MVP stores its script, input file, and output file together.

Version 2 should separate these responsibilities.

Planned structure:

```text
ai-alert-explainer-v2/
├── input/
├── output/
├── samples/
├── src/
└── tests/
```

This structure will make the project easier to organize, test, and expand.

### Normalized Alert Model

Wazuh is the current alert source, but the internal explanation logic should not depend directly on Wazuh-specific field names.

The design introduces a normalized internal alert model.

Conceptual example:

```text
source_platform
timestamp
endpoint_name
endpoint_address
event_id
event_source
event_message
rule_id
rule_description
original_severity
normalized_severity
review_status
```

A Wazuh-specific parser can translate Wazuh alert fields into this common structure.

The explanation logic can then operate on normalized data rather than directly on vendor-specific fields.

## Vendor-Neutral Design

Wazuh remains the first supported alert source because it is already deployed in the Project Athenaeum lab.

However, the v2 architecture is designed so future security platforms could use separate adapters or parsers without rewriting the core explanation workflow.

Conceptual flow:

```text
Wazuh Alert
     |
     v
Wazuh Parser
     |
     v
Normalized Alert Model
     |
     v
Validation
     |
     v
Severity Normalization
     |
     v
Alert Explanation
     |
     v
Human Review
```

Additional vendor adapters are intentionally postponed.

## Severity Normalization

Lab 12 validated that the existing severity logic changes correctly when the Wazuh rule level changes.

Version 2 should separate the original platform severity from the normalized analyst-facing severity.

Planned normalized values may include:

```text
Informational
Low
Medium
High
Critical
Unknown
```

The original Wazuh rule level should still be preserved for evidence and analyst review.

Severity normalization is intended to improve consistency, not replace the source platform's original severity data.

## Missing-Field Handling

Lab 12 demonstrated that the MVP could still generate useful output when `rule.level` was missing.

Version 2 should expand this behavior.

Required design behavior:

* Missing fields should not automatically terminate processing
* Missing information should be clearly identified
* Unknown values should be represented consistently
* Required fields should be validated separately from optional fields
* Reports should identify incomplete data
* Human review should be required when important context is unavailable

The tool must not invent missing values.

## Validation Layer

Version 2 should include a validation stage between parsing and explanation.

The validation process should determine whether:

* The input file is readable
* The alert structure is supported
* Required fields are available
* Optional fields are missing
* Severity information can be interpreted
* The alert can safely continue through the explanation workflow

Validation results should become part of the final processing record.

## Review Status

The design introduces a simple review-status field to make human oversight explicit.

Potential statuses include:

```text
REVIEW_REQUIRED
INCOMPLETE_DATA
READY_FOR_REVIEW
PROCESSING_ERROR
```

These values describe workflow state.

They do not represent automated incident decisions.

## Isolated Failure Handling

One malformed or unsupported alert should not prevent other valid alerts from being processed.

Planned behavior:

```text
Alert 1 → Processed successfully
Alert 2 → Missing field → Report created with warning
Alert 3 → Invalid input → Error recorded
Alert 4 → Processed successfully
```

The batch should continue until all available alerts have been attempted.

## Unique Output Reports

Version 2 must avoid overwriting previous reports.

Each processed alert should receive a unique report filename.

A unique name may use combinations of:

* Timestamp
* Endpoint name
* Rule ID
* Event ID
* Processing identifier

The final naming convention will be selected during Lab 14 implementation and testing.

## Batch Summary Report

After processing multiple alerts, the tool should create a summary describing the batch.

The summary may include:

* Total files discovered
* Alerts processed successfully
* Alerts processed with missing fields
* Alerts that failed validation
* Reports created
* Errors encountered
* Files requiring manual review

This will provide a quick overview without requiring the analyst to open every report individually.

## Overwrite Protection

Generated reports should not silently replace existing evidence.

The v2 implementation should detect existing filenames and create a unique output rather than overwrite a prior report.

This supports repeatable testing and preserves historical evidence.

## Human Review Requirement

Human review remains a core requirement.

Version 2 will not automatically:

* Isolate endpoints
* Disable accounts
* Delete files
* Terminate processes
* Change firewall rules
* Close alerts
* Escalate incidents
* Make final incident decisions

Generated explanations and recommendations must be reviewed before action is taken.

```text
Automation supports analysis.
Human review controls decisions.
```

## Planned Test Samples

Lab 14 implementation should begin with five sanitized alert scenarios.

The planned test set includes:

1. Normal baseline alert
2. Lower-severity alert
3. Higher-severity alert
4. Alert with missing optional fields
5. Invalid or unsupported alert input

These samples will test both successful processing and controlled failure behavior.

## Proposed Processing Workflow

```text
Discover input files
        |
        v
Identify source format
        |
        v
Parse alert
        |
        v
Normalize fields
        |
        v
Validate data
        |
        v
Normalize severity
        |
        v
Generate explanation
        |
        v
Assign review status
        |
        v
Create unique report
        |
        v
Record batch result
        |
        v
Continue to next alert
        |
        v
Generate batch summary
```

## Implementation Boundaries

Lab 13 intentionally does not implement every future Business Guardian capability.

The following features are postponed:

* Additional security-platform adapters
* Live SIEM API connections
* Browser dashboard
* Automated containment
* Automated response actions
* Full approval engine
* Multi-user approval workflows
* Tenant separation
* Remote connectors
* Generative AI model integration
* MITRE ATT&CK mapping
* Cloud hosting
* Commercial deployment
* Licensing
* Billing
* Customer management
* Production credential management

These features may be considered later after the core alert-processing workflow is proven reliable.

## Security and Privacy

The Lab 13 design follows these requirements:

* Use only sanitized test data
* Do not publish credentials or secrets
* Do not use production or customer data
* Do not expose personal system paths
* Preserve the Lab 11 stable baseline
* Keep testing isolated from published working code
* Do not automatically perform security actions
* Require human review
* Document limitations
* Preserve evidence generated during testing

## Public Repository Boundary

Project Athenaeum documents the portfolio-safe progression of the alert-explanation project.

The public repository may contain:

* Sanitized requirements
* High-level architecture
* Test methodology
* Demonstration code
* Sanitized samples
* Portfolio-safe screenshots
* Validation results

More advanced Business Guardian product logic, proprietary workflows, sensitive configuration, commercial features, tenant logic, or product-level backend functionality remain outside the public Project Athenaeum repository.

## Work Completed

During this lab, I:

* Reviewed the Lab 11 MVP architecture
* Reviewed the Lab 12 validation results
* Preserved the existing MVP as a frozen baseline
* Identified requirements for multiple-alert processing
* Designed separate input and output handling
* Defined a vendor-neutral normalized alert model
* Defined a Wazuh-to-common-data translation layer
* Planned severity normalization
* Defined missing-field behavior
* Designed a validation layer
* Defined safe review-status values
* Planned isolated alert-processing failures
* Defined unique report requirements
* Planned overwrite protection
* Designed batch-summary reporting
* Defined five sanitized validation scenarios
* Documented human-review requirements
* Defined the public/private repository boundary
* Identified features that should be postponed
* Prepared the design for controlled implementation during Lab 14

## Design Outcome

Lab 13 produced an implementation-ready design without changing the validated MVP.

The completed design provides a controlled path from:

```text
Single prepared alert
```

to:

```text
Multiple independently processed alerts
        +
Normalized security data
        +
Improved validation
        +
Unique reports
        +
Batch reporting
        +
Human review
```

The technical design is approved for controlled implementation in Lab 14.

## Lessons Learned

Lab 13 reinforced that adding features immediately after testing is not always the best development approach.

Lab 12 identified how the current MVP behaves. Lab 13 converted those observations into explicit requirements before new code was written.

Separating requirements, architecture, implementation, and testing makes future changes easier to understand and verify.

The vendor-neutral normalized alert model is also important because it prevents the core explanation workflow from becoming permanently tied to one security platform.

Most importantly, the design keeps the next development step manageable. The goal is not to build the entire Business Guardian platform at once. The goal is to make one validated improvement at a time.

## Future Development

Lab 14 will begin the controlled implementation of AI Alert Explainer v2.

Initial implementation priorities include:

* Creating the v2 project structure
* Supporting multiple alert samples
* Separating input and output directories
* Building the normalized alert model
* Creating the first Wazuh parser
* Improving missing-field handling
* Adding severity normalization
* Generating unique reports
* Isolating per-alert failures
* Creating a batch summary
* Testing the five planned sanitized scenarios
* Comparing v2 behavior with the validated MVP baseline

Dashboard, advanced AI, automated response, and commercial features will remain postponed until the underlying workflow is validated.

## Status

**Requirements and technical design completed; approved for controlled Lab 14 implementation**
