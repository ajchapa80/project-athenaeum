# Lab 12 — AI Alert Explainer Testing and Validation

## A Tool Working Once Does Not Mean It Is Reliable

Lab 11 produced the first functional AI Alert Explainer MVP.

It could read a prepared security alert, extract useful information, apply deterministic severity logic, and generate an analyst-oriented explanation.

That proved the basic concept worked.

But there was a bigger question:

**What happens when the input is missing, empty, incomplete, or different from the example the tool was built around?**

Lab 12 deliberately tests those conditions.

Instead of adding new features, this lab takes the published Lab 11 MVP, preserves it as a stable baseline, creates a separate testing workspace, and tries to break copied versions of it safely.

The progression becomes:

```text
Build the MVP
      ↓
Preserve the Working Baseline
      ↓
Test Normal Behavior
      ↓
Create Failure Conditions
      ↓
Observe the Results
      ↓
Restore the Baseline
      ↓
Use Evidence to Plan the Next Version
```

The published Lab 11 source was never rewritten or replaced during this lab.

**Nothing gets built twice.**

---

# What Lab 12 Tests

The validation plan covers seven areas:

1. Normal baseline execution
2. Output-file creation
3. Missing input-file handling
4. Empty input-file handling
5. Missing `rule.level` behavior
6. Severity-logic changes
7. Final baseline restoration

The goal is not simply to make the script complete without crashing.

The goal is to understand how it behaves when the environment is not perfect.

---

# Protecting the Working Version

The published Lab 11 files remained the known-good reference.

Copied versions were placed in a separate Lab 12 testing workspace:

```text
Lab11_AI_Alert_Explainer_MVP.py
Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt
Lab11_Alert_Explanation_Output.txt
```

The filenames intentionally remain `Lab11`.

Lab 12 is testing the existing MVP, not pretending that a new version of the application was created.

A temporary backup of the alert sample was also used during destructive test preparation and removed before publication.

This approach allowed me to create missing files, empty files, incomplete data, and changed severity values without damaging the working project.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_02_testing-workspace-created.png"
    alt="Lab 12 separate testing workspace"
    width="850">
</p>

<p align="center">
  <em>A separate testing workspace protected the published Lab 11 baseline while failure conditions were created safely.</em>
</p>

---

# Establishing the Known-Good Baseline

Before introducing any failure conditions, the copied MVP was executed exactly as it had been published.

The script completed successfully and generated:

```text
Lab11_Alert_Explanation_Output.txt
```

The report contained the expected:

- Alert summary
- Windows event context
- Wazuh rule context
- Severity explanation
- Analyst context
- Recommended review steps
- Final assessment language

This established the reference behavior for every test that followed.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_03_baseline-script-success.png"
    alt="Lab 12 baseline script execution"
    width="900">
</p>

<p align="center">
  <em>The copied MVP successfully completed its normal workflow before any test conditions were introduced.</em>
</p>

## Baseline Result

```text
PASS
```

---

# Test 1 — Can the Program Handle a Missing File?

The expected alert-data file was temporarily renamed.

From the program's perspective, the input had disappeared.

The expected behavior was:

```text
Do not crash unexpectedly
Stop safely
Explain what is missing
```

The script detected that the expected input file could not be found and displayed a readable error message.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_06_missing-input-error-handled.png"
    alt="Lab 12 missing input file handled safely"
    width="900">
</p>

<p align="center">
  <em>The MVP stopped safely and explained that the expected input file could not be found.</em>
</p>

## Result

**PASS**

---

# Test 2 — What If the File Exists but Contains Nothing?

An empty file was created using the exact filename expected by the application.

This tests a different problem.

```text
Missing file
      ≠
Empty file
```

The file exists, but there is nothing useful to process.

The MVP detected the empty input and displayed a readable message explaining that the file contained no data.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_08_empty-input-error-handled.png"
    alt="Lab 12 empty input file handled safely"
    width="900">
</p>

<p align="center">
  <em>The script distinguished an empty file from a missing file and handled the condition without an unexplained failure.</em>
</p>

## Result

**PASS**

---

# Test 3 — What Happens When One Alert Field Is Missing?

The original sanitized alert data was restored.

Then the Wazuh field:

```text
rule.level
```

was removed from the copied sample.

The question was:

**Should one missing value make the entire alert unusable?**

For this MVP, the expected behavior was to continue processing the available information while clearly identifying the missing severity value.

The script still generated a report.

The output showed:

```text
Unknown rule level
```

and indicated that severity required manual review.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_12_missing-field-output-reviewed.png"
    alt="Lab 12 missing rule-level output"
    width="900">
</p>

<p align="center">
  <em>The report remained usable while clearly identifying that severity information was unavailable.</em>
</p>

## Result

**PASS**

This became an important design lesson for later labs:

> **Missing information should be identified, not invented.**

---

# Test 4 — Does the Severity Logic Actually Change?

The sanitized baseline originally contained:

```text
rule.level: 9
```

The test copy was changed to:

```text
rule.level: 3
```

The purpose was simple:

**Does changing the source severity actually change the explanation?**

With level `9`, the MVP used notable-alert language and recommended analyst review.

With level `3`, it shifted to lower-level language and noted that the event may represent normal system activity.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_15_severity-output-reviewed.png"
    alt="Lab 12 severity logic validation"
    width="900">
</p>

<p align="center">
  <em>Changing the Wazuh rule level from 9 to 3 produced the expected change in severity language.</em>
</p>

## Result

**PASS**

The test confirmed that the severity branch was responding to the supplied value rather than always producing the same explanation.

It also exposed an area for future improvement: the original severity logic relied on simple predefined ranges tied to Wazuh.

That observation later contributes to the platform-neutral severity design introduced in Lab 13.

---

# Restoring the Original Baseline

Testing is not complete if the workspace is left in a modified or uncertain state.

After all test conditions were finished:

- The original alert data was restored
- `rule.level` was returned to `9`
- The temporary backup was deleted
- The application was executed again

The final execution reproduced the original expected behavior.

<p align="center">
  <img
    src="screenshots/2026-08-01_Lab12_AIAlertTesting_17_final-baseline-restored-success.png"
    alt="Lab 12 final baseline restoration"
    width="900">
</p>

<p align="center">
  <em>The original configuration was restored and successfully revalidated after all test conditions were complete.</em>
</p>

## Final Restoration Result

**PASS**

---

# Complete Validation Results

Every planned Lab 12 validation passed.

| Test | Result |
| --- | --- |
| Baseline execution | **PASS** |
| Output-file creation | **PASS** |
| Missing input-file handling | **PASS** |
| Empty input-file handling | **PASS** |
| Missing `rule.level` handling | **PASS** |
| Severity logic `9 → 3` | **PASS** |
| Final baseline restoration | **PASS** |

Additional behavior confirmed:

- Missing severity produced `Unknown rule level`
- Manual-review language appeared when severity was unavailable
- Changing the rule level changed the generated explanation
- Original test data was restored afterward
- The published Lab 11 baseline remained untouched

---

# Published Project Files

The restored baseline files used during testing are included with Lab 12:

- [`Lab11_AI_Alert_Explainer_MVP.py`](Lab11_AI_Alert_Explainer_MVP.py)
- [`Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt`](Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt)
- [`Lab11_Alert_Explanation_Output.txt`](Lab11_Alert_Explanation_Output.txt)

These represent the final restored state after testing was complete.

The full screenshot set remains available in the [`screenshots/`](screenshots/) folder.

---

# What Lab 12 Revealed

The purpose of this lab was not just to collect seven PASS results.

Testing exposed several design lessons that directly influence the next version.

## A Program Should Explain Why It Stopped

Readable error messages made the missing-file and empty-file tests much easier to troubleshoot.

A controlled failure is much more useful than an unexplained crash.

---

## One Missing Field Does Not Always Mean Total Failure

Removing `rule.level` showed that useful alert information could still be processed even when one expected value was missing.

That leads toward more structured missing-field handling later in the project.

---

## Severity Logic Needs to Be Tested With More Than One Value

A severity function cannot be considered validated because one alert happened to produce the expected language.

Changing the Wazuh rule level from `9` to `3` proved that different branches of the logic actually worked.

---

## Testing Should Not Destroy the Baseline

Using copied files allowed the test environment to be manipulated freely while preserving the historical working version.

That becomes part of the broader Project Athenaeum development approach:

```text
Build
  ↓
Preserve Baseline
  ↓
Test
  ↓
Document
  ↓
Restore
  ↓
Plan the Next Improvement
```

---

# Intentional Limitations

Lab 12 validates the original MVP within its intended scope.

It does not claim that the tool is production-ready.

Known limitations include:

- Only one sanitized alert example
- Structured text rather than full JSON records
- One alert processed at a time
- No alert correlation
- Only selected failure conditions
- No automated unit-test suite
- Simple predefined Wazuh severity ranges
- No independent malicious-intent determination
- No graphical interface
- No external or local AI model used
- Human review remains necessary

These limitations are useful.

They identify exactly what later development needs to address.

---

# Security and Privacy

All Lab 12 testing remained inside the authorized local environment.

The lab used:

- Copied and sanitized Lab 11 files
- No Wazuh credentials
- No passwords
- No API keys
- No access tokens
- No production security data
- No customer data
- No employer data
- No school data
- No external AI service receiving alert information
- No automated security actions

The temporary backup file used during testing was deleted before publication.

Screenshots were reviewed before being added to GitHub.

---

# What Lab 12 Proves

Lab 12 demonstrates that software validation requires more than confirming that the happy path works.

The MVP successfully:

- Completed its normal workflow
- Generated its expected output
- Detected a missing file
- Detected an empty file
- Continued when one expected field was missing
- Identified unavailable severity information
- Changed severity language when the rule level changed
- Returned to its original working configuration afterward

Most importantly:

> **Future improvements now have evidence to build from instead of assumptions.**

---

# Skills Demonstrated

- Python application testing
- Baseline validation
- Error-handling verification
- Missing-file testing
- Empty-file testing
- Missing-field testing
- Severity-logic testing
- Output comparison
- Controlled test preparation
- Regression-style validation
- Change control
- Test-data restoration
- Security-data handling
- Evidence collection
- Technical documentation
- Human-reviewed security analysis

---

# Where the Project Goes From Here

Lab 11 answered:

**Can I build a working Python tool that turns a security alert into a more understandable analyst report?**

Lab 12 answered:

**Does it still behave predictably when the input is not perfect?**

The testing passed—but it also showed where the architecture needed to grow.

The next questions became:

- How do we process more than one alert?
- How do we stop tying the internal design directly to Wazuh?
- How should missing and malformed data be represented?
- How do we prevent one bad alert from stopping everything?
- How do we define correct behavior before implementing the next version?

[Lab 13 — AI Alert Explainer v2: Requirements and Design](../lab-13-ai-alert-explainer-v2-requirements-design/README.md) takes those questions and turns them into the design for the next architecture.

The progression becomes:

```text
Working MVP
     ↓
Controlled Testing
     ↓
Documented Weaknesses
     ↓
Requirements
     ↓
Designed v2 Architecture
```

Lab 12 is where Project Athenaeum stops asking only:

**"Does it work?"**

and starts asking:

**"Do I understand how it fails?"**
