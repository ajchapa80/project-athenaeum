# Lab 14 Screenshots

This folder contains selected sanitized screenshots from **Lab 14: AI Alert Explainer v2 Multiple Alert Processing**.

The complete internal Lab 14 Screenshot Log contains all 54 screenshots captured during development, testing, and validation. Only the strongest portfolio-safe evidence is published here.

The selected screenshots demonstrate the most important Lab 14 capabilities without publishing unnecessary internal development detail or proprietary Business Guardian implementation information.

## Published Evidence

### 1. Multiple-Alert Batch Processing

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_29_multiple-alert-batch-processing.png`

Demonstrates the core multiple-alert batch-processing implementation and the transition from the validated single-alert MVP to the v2 workflow.

---

### 2. First Successful Batch Execution

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_45_first-batch-execution-success.png`

Shows the first successful complete execution of the five-alert validation set.

Observed result:

* 5 alerts discovered
* 2 processed normally
* 2 processed with warnings
* 1 failed validation
* 4 individual reports created

This matched the deterministic acceptance criteria established during Lab 13.

---

### 3. Validated Batch Summary

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_47_validated-batch-summary.png`

Shows the batch-level processing record and the outcomes produced for the complete controlled validation set.

This screenshot provides evidence that processing totals were calculated from actual results and that individual alert outcomes were retained for traceability.

---

### 4. Missing-Field Validation

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_50_report3-missing-fields-validation.png`

Demonstrates safe processing of an incomplete alert.

The alert was intentionally missing supported source information. The application reported the missing normalized fields rather than fabricating replacement data and processed the alert with warnings.

---

### 5. Malformed-Severity Validation

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_51_report4-malformed-severity-validation.png`

Demonstrates safe handling of malformed source severity data.

The invalid source severity was preserved for traceability, normalized severity became `UNKNOWN`, and the issue was recorded as a validation note rather than being incorrectly treated as a missing field.

---

### 6. Overwrite-Protection Validation

**Filename:**

`2026-08-17_Lab14_AIAlertExplainerV2_54_overwrite-protection-validation.png`

Demonstrates repeatable batch execution and overwrite protection.

A second complete processing run created a separate set of individual reports and a new batch summary while preserving the output from the first validated run.

## Evidence Selection

These six screenshots were selected from the complete 54-screenshot Lab 14 documentation record because they demonstrate:

* Multiple-alert processing
* Successful deterministic validation
* Batch-level accountability
* Missing-data handling
* Malformed-data handling
* Repeatability
* Overwrite protection
* Source traceability
* Safe processing behavior

The complete internal screenshot record is retained in the local Project Athenaeum documentation but is not published publicly.

## Security and Privacy

All screenshots published in this folder were reviewed for public portfolio use.

The evidence uses sanitized or synthetic data and does not intentionally expose:

* Passwords or credentials
* Personal information
* Employer or customer information
* Production-system data
* Secrets or tokens
* Sensitive configuration
* Proprietary Business Guardian product logic
* Private remediation or approval workflows
* Tenant or commercial implementation details

All security testing was performed using personally owned or authorized systems in controlled lab environments.
