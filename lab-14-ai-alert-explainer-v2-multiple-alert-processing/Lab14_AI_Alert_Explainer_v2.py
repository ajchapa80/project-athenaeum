# Import tools for file paths and processing-run timestamps.
from pathlib import Path
from datetime import datetime


# Define the Lab 14 workspace locations.
LAB_FOLDER = Path(__file__).parent
INPUT_FOLDER = LAB_FOLDER / "input"
OUTPUT_FOLDER = LAB_FOLDER / "output"

# Lab 14 initially supports sanitized text-based alert samples.
SUPPORTED_EXTENSIONS = {".txt"}


def validate_workspace():
    """Verify the required input folder and prepare the output folder."""

    if not INPUT_FOLDER.exists():
        raise FileNotFoundError(
            f"Required input folder was not found: {INPUT_FOLDER}"
        )

    if not INPUT_FOLDER.is_dir():
        raise NotADirectoryError(
            f"Input path is not a folder: {INPUT_FOLDER}"
        )

    # The output folder contains generated data and may be safely created.
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def create_run_timestamp():
    """Create one sortable timestamp for the current processing run."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def discover_alert_files():
    """Find all supported alert files in the input folder."""

    alert_files = [
        file_path
        for file_path in INPUT_FOLDER.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    # Sort filenames so processing order remains predictable.
    return sorted(alert_files, key=lambda path: path.name.lower())


# Wazuh is the first supported alert source.
# These source-specific fields are translated into the
# vendor-neutral normalized alert model.
WAZUH_SOURCE_FIELDS = {
    "agent.name",
    "agent.ip",
    "manager.name",
    "data.win.system.eventID",
    "data.win.system.providerName",
    "data.win.system.severityValue",
    "data.win.system.message",
    "rule.description",
    "rule.id",
    "rule.level",
    "rule.groups",
    "decoder.name",
    "location",
}


def load_wazuh_alert(file_path):
    """Read one supported Wazuh alert file and return recognized source fields."""

    # Confirm the discovered source file still exists before reading it.
    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file was not found: {file_path.name}"
        )

    # Empty files contain no usable alert information.
    if file_path.stat().st_size == 0:
        raise ValueError(
            f"Input file is empty: {file_path.name}"
        )

    source_data = {}

    # Reuse the validated Lab 11 UTF-8 field:value parsing approach.
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Ignore blank lines and lines that do not use field:value format.
            if not line or ":" not in line:
                continue

            # Split only at the first colon so colons inside event messages remain.
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Preserve only fields supported by the initial Wazuh adapter.
            if key in WAZUH_SOURCE_FIELDS:
                source_data[key] = value

    # A file with no recognized fields cannot represent a supported alert.
    if not source_data:
        raise ValueError(
            f"No recognized supported alert fields were found: {file_path.name}"
        )

    return source_data


def translate_wazuh_to_normalized(source_data):
    """Translate recognized Wazuh fields into the common normalized alert model."""

    # Build a vendor-neutral representation for shared downstream processing.
    normalized_alert = {
        "alert_id": None,
        "timestamp": None,
        "source_platform": "Wazuh",
        "endpoint_name": source_data.get("agent.name"),
        "endpoint_ip": source_data.get("agent.ip"),
        "event_type": source_data.get("rule.description"),
        "event_id": source_data.get("data.win.system.eventID"),
        "event_provider": source_data.get("data.win.system.providerName"),
        "event_message": source_data.get("data.win.system.message"),
        "source_rule_id": source_data.get("rule.id"),
        "source_rule_description": source_data.get("rule.description"),
        "source_severity": source_data.get("rule.level"),
        "normalized_severity": None,
        "source_groups": source_data.get("rule.groups"),
        "source_location": source_data.get("location"),
        "source_decoder": source_data.get("decoder.name"),
        "validation_status": None,
        "missing_fields": [],
        "validation_notes": [],
        "review_status": "Requires Review",
        "raw_source_data": dict(source_data),
    }

    return normalized_alert


def normalize_wazuh_severity(source_severity):
    """Translate a Wazuh rule level into the common normalized severity scale."""

    # Missing severity cannot be safely inferred.
    if source_severity is None or source_severity == "":
        return "UNKNOWN", "Source severity is missing."

    # Preserve malformed values rather than guessing what they were intended to mean.
    try:
        severity_level = int(source_severity)
    except (TypeError, ValueError):
        return (
            "UNKNOWN",
            f"Source severity could not be interpreted reliably: {source_severity}",
        )

    # Values outside the supported Wazuh range must not be forced into a category.
    if severity_level < 0 or severity_level > 16:
        return (
            "UNKNOWN",
            f"Source severity is outside the supported Wazuh range: {source_severity}",
        )

    if severity_level <= 3:
        return "INFORMATIONAL", None

    if severity_level <= 6:
        return "LOW", None

    if severity_level <= 9:
        return "MEDIUM", None

    if severity_level <= 12:
        return "HIGH", None

    return "CRITICAL", None


def apply_severity_normalization(normalized_alert):
    """Apply normalized severity and preserve any severity validation warning."""

    # Translate the original source severity without altering its source value.
    severity, severity_note = normalize_wazuh_severity(
        normalized_alert.get("source_severity")
    )

    normalized_alert["normalized_severity"] = severity

    # Record a warning when severity could not be translated reliably.
    if severity_note:
        normalized_alert["validation_notes"].append(severity_note)

    return normalized_alert


# Normalized fields expected from the initial supported Wazuh alert format.
EXPECTED_CONTEXT_FIELDS = {
    "endpoint_name",
    "endpoint_ip",
    "event_type",
    "event_id",
    "event_provider",
    "event_message",
    "source_rule_id",
    "source_rule_description",
    "source_severity",
}

# Useful fields that are not required for normal Lab 14 processing.
OPTIONAL_CONTEXT_FIELDS = {
    "alert_id",
    "timestamp",
    "source_groups",
    "source_location",
    "source_decoder",
}


def identify_missing_fields(normalized_alert):
    """Identify expected normalized fields that are unavailable."""

    missing_fields = []

    # Check only fields that the initial supported alert format is expected to provide.
    for field_name in sorted(EXPECTED_CONTEXT_FIELDS):
        value = normalized_alert.get(field_name)

        # Treat None and empty strings as unavailable information.
        if value is None or value == "":
            missing_fields.append(field_name)

    normalized_alert["missing_fields"] = missing_fields

    return normalized_alert


def has_usable_event_evidence(normalized_alert):
    """Determine whether the alert contains enough event evidence to describe."""

    # At least one meaningful event-description field must contain usable data.
    evidence_fields = (
        "event_type",
        "event_message",
        "source_rule_description",
    )

    for field_name in evidence_fields:
        value = normalized_alert.get(field_name)

        if value is not None and str(value).strip():
            return True

    return False


def validate_normalized_alert(normalized_alert):
    """Assign the appropriate validation result for one normalized alert."""

    # Record any expected context that was not supplied by the source alert.
    identify_missing_fields(normalized_alert)

    # An analyst report must not be created without usable event evidence.
    if not has_usable_event_evidence(normalized_alert):
        failure_note = (
            "The alert does not contain enough usable event evidence "
            "to describe a supported security event reliably."
        )

        if failure_note not in normalized_alert["validation_notes"]:
            normalized_alert["validation_notes"].append(failure_note)

        normalized_alert["validation_status"] = "Failed Validation"
        return normalized_alert

    # Missing fields or other validation notes require a warning.
    if (
        normalized_alert["missing_fields"]
        or normalized_alert["validation_notes"]
    ):
        normalized_alert["validation_status"] = "Processed With Warnings"
        return normalized_alert

    # The alert contains the expected usable context with no identified warnings.
    normalized_alert["validation_status"] = "Processed Normally"

    return normalized_alert


def process_single_alert(file_path, run_timestamp):
    """Process one alert independently and return its structured result."""

    try:
        # Load the supported source fields from the alert file.
        source_data = load_wazuh_alert(file_path)

        # Translate Wazuh-specific fields into the common alert model.
        normalized_alert = translate_wazuh_to_normalized(source_data)

        # Add normalized severity while preserving the original source severity.
        apply_severity_normalization(normalized_alert)

        # Determine whether processing completed normally, with warnings, or failed.
        validate_normalized_alert(normalized_alert)

        if normalized_alert["validation_status"] == "Failed Validation":
            processing_result = "Failed"
        elif normalized_alert["validation_status"] == "Processed With Warnings":
            processing_result = "Processed With Warnings"
        else:
            processing_result = "Processed Successfully"

        # Create a report only when validation produced usable alert information.
        if processing_result != "Failed":
            report_path = write_individual_report(
                normalized_alert,
                file_path.name,
                run_timestamp,
            )
        else:
            report_path = None

        return {
            "source_file": file_path.name,
            "processing_result": processing_result,
            "normalized_alert": normalized_alert,
            "report_path": report_path,
            "error": None,
        }

    except (OSError, UnicodeError, ValueError) as error:
        # Contain expected source-data failures to this alert whenever possible.
        return {
            "source_file": file_path.name,
            "processing_result": "Failed",
            "normalized_alert": None,
            "report_path": None,
            "error": str(error),
        }


def explain_normalized_severity(normalized_severity):
    """Return safe plain-English guidance for a normalized severity category."""

    explanations = {
        "INFORMATIONAL": (
            "This event has little or no immediate security significance but may "
            "provide useful operational or audit context."
        ),
        "LOW": (
            "This event has limited security relevance or represents low-priority "
            "abnormal activity."
        ),
        "MEDIUM": (
            "This event has meaningful security relevance and should normally "
            "be reviewed by an analyst."
        ),
        "HIGH": (
            "This event represents a significant security concern and should "
            "receive prioritized analyst review."
        ),
        "CRITICAL": (
            "This event represents a severe or highly significant security condition "
            "requiring prompt analyst attention."
        ),
        "UNKNOWN": (
            "The source severity could not be translated reliably. The original "
            "source value should be reviewed before a severity conclusion is made."
        ),
    }

    return explanations.get(
        normalized_severity,
        explanations["UNKNOWN"],
    )


def display_value(value):
    """Return a safe display value without inventing missing source information."""

    if value is None or value == "":
        return "Unavailable"

    return str(value)


def build_report_header(normalized_alert, source_filename, run_timestamp):
    """Build the report header and processing-status section."""

    return (
        "AI Alert Explainer v2 Report\n\n"
        f"Processing Run: {run_timestamp}\n"
        f"Source Alert File: {source_filename}\n\n"
        "Processing Status\n"
        f"Validation Status: {display_value(normalized_alert.get('validation_status'))}\n"
        f"Review Status: {display_value(normalized_alert.get('review_status'))}"
    )


def build_alert_context(normalized_alert):
    """Build the alert summary, endpoint context, and event context sections."""

    event_type = display_value(normalized_alert.get("event_type"))
    endpoint_name = display_value(normalized_alert.get("endpoint_name"))
    endpoint_ip = display_value(normalized_alert.get("endpoint_ip"))
    event_id = display_value(normalized_alert.get("event_id"))
    event_provider = display_value(normalized_alert.get("event_provider"))
    event_message = display_value(normalized_alert.get("event_message"))

    return (
        "Alert Summary\n"
        f"Event Type: {event_type}\n"
        f"Endpoint: {endpoint_name}\n\n"
        "Endpoint Context\n"
        f"Endpoint Name: {endpoint_name}\n"
        f"Endpoint IP: {endpoint_ip}\n\n"
        "Event Context\n"
        f"Event Type: {event_type}\n"
        f"Event ID: {event_id}\n"
        f"Event Provider: {event_provider}\n"
        f"Event Message: {event_message}"
    )


def build_security_context(normalized_alert):
    """Build source-security context and normalized severity explanation sections."""

    source_platform = display_value(normalized_alert.get("source_platform"))
    source_rule_id = display_value(normalized_alert.get("source_rule_id"))
    source_rule_description = display_value(
        normalized_alert.get("source_rule_description")
    )
    source_severity = display_value(normalized_alert.get("source_severity"))
    normalized_severity = display_value(
        normalized_alert.get("normalized_severity")
    )

    severity_explanation = explain_normalized_severity(
        normalized_alert.get("normalized_severity")
    )

    return (
        "Source Security Context\n"
        f"Source Platform: {source_platform}\n"
        f"Source Rule ID: {source_rule_id}\n"
        f"Source Rule Description: {source_rule_description}\n"
        f"Source Severity: {source_severity}\n"
        f"Normalized Severity: {normalized_severity}\n\n"
        "Severity Explanation\n"
        f"{severity_explanation}"
    )


def build_validation_information(normalized_alert):
    """Build missing-field and validation-note sections for the report."""

    missing_fields = normalized_alert.get("missing_fields") or []
    validation_notes = normalized_alert.get("validation_notes") or []

    # Display an explicit None when no expected fields are missing.
    if missing_fields:
        missing_fields_text = "\n".join(
            f"- {field_name}" for field_name in missing_fields
        )
    else:
        missing_fields_text = "None"

    # Preserve validation warnings exactly as processing recorded them.
    if validation_notes:
        validation_notes_text = "\n".join(
            f"- {note}" for note in validation_notes
        )
    else:
        validation_notes_text = "None"

    return (
        "Validation Information\n"
        f"Missing Fields:\n{missing_fields_text}\n\n"
        f"Validation Notes:\n{validation_notes_text}"
    )


def build_review_guidance(normalized_alert):
    """Build analyst review guidance and a safe assessment for the alert."""

    # Reuse and improve the general review guidance established in the MVP.
    review_steps = (
        "1. Confirm whether the event was expected or unexpected.",
        "2. Review the endpoint and event context that is available.",
        "3. Check whether similar or related activity occurred around the same time.",
        "4. Review source rule and severity information.",
        "5. Determine whether additional investigation or escalation is appropriate.",
    )

    review_guidance = "\n".join(review_steps)

    # Validation warnings require additional caution before a security conclusion.
    if normalized_alert.get("validation_status") == "Processed With Warnings":
        assessment = (
            "The available information was sufficient to create a report, but "
            "validation warnings were identified. The alert requires analyst review, "
            "and missing or uncertain information should be considered before a "
            "security conclusion is made."
        )
    else:
        assessment = (
            "The available information has been processed successfully, but the "
            "alert requires analyst review before a security conclusion is made."
        )

    return (
        "Analyst Review Guidance\n"
        f"{review_guidance}\n\n"
        "Assessment\n"
        f"{assessment}"
    )


def build_source_traceability(normalized_alert, source_filename):
    """Build source-traceability information for the generated report."""

    source_platform = display_value(normalized_alert.get("source_platform"))
    alert_id = display_value(normalized_alert.get("alert_id"))
    timestamp = display_value(normalized_alert.get("timestamp"))

    return (
        "Source Traceability\n"
        f"Original Input File: {source_filename}\n"
        f"Source Platform: {source_platform}\n"
        f"Source Alert ID: {alert_id}\n"
        f"Source Event Timestamp: {timestamp}"
    )


def build_individual_report(normalized_alert, source_filename, run_timestamp):
    """Assemble the complete v2 analyst report from reusable report sections."""

    # Failed-validation alerts must not receive an invented analyst report.
    if normalized_alert.get("validation_status") == "Failed Validation":
        raise ValueError(
            "An individual analyst report cannot be created for a failed-validation alert."
        )

    report_sections = [
        build_report_header(
            normalized_alert,
            source_filename,
            run_timestamp,
        ),
        build_alert_context(normalized_alert),
        build_security_context(normalized_alert),
        build_validation_information(normalized_alert),
        build_review_guidance(normalized_alert),
        build_source_traceability(
            normalized_alert,
            source_filename,
        ),
    ]

    # Separate each reusable section with one blank line.
    return "\n\n".join(report_sections)


def create_unique_report_path(source_filename, run_timestamp):
    """Create a unique output path without overwriting an existing report."""

    source_stem = Path(source_filename).stem
    base_name = f"{source_stem}_report_{run_timestamp}"
    report_path = OUTPUT_FOLDER / f"{base_name}.txt"

    # Add a numeric suffix if a filename collision still occurs.
    collision_number = 2

    while report_path.exists():
        report_path = OUTPUT_FOLDER / (
            f"{base_name}_{collision_number}.txt"
        )
        collision_number += 1

    return report_path


def write_individual_report(normalized_alert, source_filename, run_timestamp):
    """Build and safely write one processable alert report to the output folder."""

    report_text = build_individual_report(
        normalized_alert,
        source_filename,
        run_timestamp,
    )

    report_path = create_unique_report_path(
        source_filename,
        run_timestamp,
    )

    # Write generated reports only to the designated output location.
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    return report_path


def process_alert_batch():
    """Process all discovered supported alerts during one controlled batch run."""

    # Confirm the required workspace is ready before processing begins.
    validate_workspace()

    # Create one timestamp shared by every result produced during this run.
    run_timestamp = create_run_timestamp()

    # Discover all supported alert files in predictable filename order.
    alert_files = discover_alert_files()

    batch_results = []

    # Process each alert independently so one expected failure does not stop the batch.
    for file_path in alert_files:
        result = process_single_alert(
            file_path,
            run_timestamp,
        )
        batch_results.append(result)

           # Build the batch record after every discovered alert has been attempted.
    batch_data = {
        "run_timestamp": run_timestamp,
        "alert_files": alert_files,
        "results": batch_results,
    }

    # Calculate totals from what actually occurred during this processing run.
    batch_data["totals"] = calculate_batch_totals(batch_data)

    # Create one batch summary after all discovered alerts have been attempted.
    summary_path = write_batch_summary(batch_data)
    batch_data["summary_path"] = summary_path

    return batch_data


def calculate_batch_totals(batch_data):
    """Calculate processing totals from the collected per-alert batch results."""

    results = batch_data.get("results", [])
    alert_files = batch_data.get("alert_files", [])

    # Count each processing outcome independently from the collected results.
    successfully_processed = sum(
        1
        for result in results
        if result.get("processing_result") == "Processed Successfully"
    )

    processed_with_warnings = sum(
        1
        for result in results
        if result.get("processing_result") == "Processed With Warnings"
    )

    failed = sum(
        1
        for result in results
        if result.get("processing_result") == "Failed"
    )

    # A report counts as created only when an actual report path was returned.
    reports_created = sum(
        1
        for result in results
        if result.get("report_path") is not None
    )

    return {
        "total_discovered": len(alert_files),
        "successfully_processed": successfully_processed,
        "processed_with_warnings": processed_with_warnings,
        "failed": failed,
        "reports_created": reports_created,
    }


def build_batch_result_entry(result):
    """Build one per-alert result entry for the batch summary."""

    normalized_alert = result.get("normalized_alert")
    report_path = result.get("report_path")

    # Use normalized processing information when an alert record was constructed.
    if normalized_alert is not None:
        validation_status = display_value(
            normalized_alert.get("validation_status")
        )
        normalized_severity = display_value(
            normalized_alert.get("normalized_severity")
        )
    else:
        # Expected source-data failures are recorded as failed validation.
        validation_status = "Failed Validation"
        normalized_severity = "Unavailable"

    # Identify the generated report by filename rather than its full local path.
    if report_path is not None:
        report_filename = report_path.name
    else:
        report_filename = "Not Created"

    entry_lines = [
        f"Source File: {display_value(result.get('source_file'))}",
        f"Processing Result: {display_value(result.get('processing_result'))}",
        f"Validation Status: {validation_status}",
        f"Normalized Severity: {normalized_severity}",
        f"Report: {report_filename}",
    ]

    # Failed alerts must explain why processing could not continue.
    if result.get("processing_result") == "Failed":
        failure_reason = result.get("error")

        if not failure_reason and normalized_alert is not None:
            validation_notes = normalized_alert.get("validation_notes") or []

            if validation_notes:
                failure_reason = "; ".join(validation_notes)

        if not failure_reason:
            failure_reason = "Alert processing failed without a detailed reason."

        entry_lines.append(
            f"Failure Reason: {failure_reason}"
        )

    return "\n".join(entry_lines)


def build_batch_summary(batch_data):
    """Build the complete processing-run summary from actual batch results."""

    run_timestamp = display_value(batch_data.get("run_timestamp"))
    results = batch_data.get("results", [])
    totals = batch_data.get("totals") or calculate_batch_totals(batch_data)

    # Build one traceable summary entry for every attempted alert.
    if results:
        per_alert_results = "\n\n".join(
            build_batch_result_entry(result)
            for result in results
        )
    else:
        per_alert_results = "No supported alert files were processed."

    # Confirm whether every discovered supported file produced a recorded result.
    if len(results) == totals.get("total_discovered", 0):
        completion_status = (
            "All discovered supported alert files were attempted."
        )
    else:
        completion_status = (
            "The processing run ended before all discovered supported alert "
            "files were attempted."
        )

    return (
        "AI Alert Explainer v2 Batch Summary\n\n"
        f"Processing Run: {run_timestamp}\n"
        f"Input Location: {INPUT_FOLDER.name}\n"
        f"Output Location: {OUTPUT_FOLDER.name}\n\n"
        "Processing Totals\n"
        f"Total Supported Alert Files Discovered: "
        f"{totals.get('total_discovered', 0)}\n"
        f"Successfully Processed: "
        f"{totals.get('successfully_processed', 0)}\n"
        f"Processed With Warnings: "
        f"{totals.get('processed_with_warnings', 0)}\n"
        f"Failed: {totals.get('failed', 0)}\n"
        f"Individual Reports Created: "
        f"{totals.get('reports_created', 0)}\n\n"
        "Per-Alert Results\n"
        f"{per_alert_results}\n\n"
        "Batch Completion\n"
        f"{completion_status}"
    )


def create_unique_batch_summary_path(run_timestamp):
    """Create a unique batch-summary path without overwriting an existing file."""

    base_name = f"batch_summary_{run_timestamp}"
    summary_path = OUTPUT_FOLDER / f"{base_name}.txt"

    # Protect an existing summary if a filename collision occurs.
    collision_number = 2

    while summary_path.exists():
        summary_path = OUTPUT_FOLDER / (
            f"{base_name}_{collision_number}.txt"
        )
        collision_number += 1

    return summary_path


def write_batch_summary(batch_data):
    """Build and safely write the processing-run summary to the output folder."""

    summary_text = build_batch_summary(batch_data)

    summary_path = create_unique_batch_summary_path(
        batch_data.get("run_timestamp")
    )

    # Write the generated batch summary only to the designated output folder.
    with open(summary_path, "w", encoding="utf-8") as file:
        file.write(summary_text)

    return summary_path


def main():
    """Run the Lab 14 multiple-alert processing workflow."""

    try:
        batch_data = process_alert_batch()

        totals = batch_data["totals"]
        summary_path = batch_data["summary_path"]

        print("AI Alert Explainer v2 processing complete.")
        print(f"Alerts discovered: {totals['total_discovered']}")
        print(f"Successfully processed: {totals['successfully_processed']}")
        print(f"Processed with warnings: {totals['processed_with_warnings']}")
        print(f"Failed: {totals['failed']}")
        print(f"Individual reports created: {totals['reports_created']}")
        print(f"Batch summary: {summary_path.name}")

    except (OSError, UnicodeError, ValueError) as error:
        print(f"Processing could not start or complete safely: {error}")


if __name__ == "__main__":
    main()








