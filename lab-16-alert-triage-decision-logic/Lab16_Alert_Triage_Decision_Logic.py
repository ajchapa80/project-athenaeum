# Lab 16 - Alert Triage and Decision Logic
# Project Athenaeum
#
# This public lab demonstrates vendor-neutral alert triage,
# deterministic classification, next-stage routing, stable
# AR-to-TR traceability, and controlled validation.
#
# Proprietary Business Guardian investigation, correlation,
# policy, approval, and defensive-action logic remains private.

import json

from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


# Define the Lab 16 workspace.
LAB_FOLDER = Path(__file__).parent
INPUT_FOLDER = LAB_FOLDER / "input"
OUTPUT_FOLDER = LAB_FOLDER / "output"


# Lab 16 accepts sanitized Lab 15-style JSON alert records.
SUPPORTED_EXTENSIONS = {".json"}


# Version of the public Lab 16 triage-decision schema.
TRIAGE_VERSION = "1.0"


# Allowed vendor-neutral triage classifications.
TRIAGE_CLASSIFICATIONS = {
    "KNOWN_COMMON",
    "UNUSUAL",
    "UNKNOWN",
    "INSUFFICIENT_DATA",
}


# Allowed next-stage routing decisions.
NEXT_STAGE_VALUES = {
    "POLICY_EVALUATION",
    "INVESTIGATION",
    "HUMAN_REVIEW",
    "NO_ACTION_YET",
}


# Lab 16 only accepts processable Lab 15 alert records.
ALLOWED_SOURCE_VALIDATION_STATUSES = {
    "Processed Normally",
    "Processed With Warnings",
}


# Platform-neutral technical severity values inherited from Lab 15.
ALLOWED_NORMALIZED_SEVERITIES = {
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
    "UNKNOWN",
}


def validate_workspace():
    """Verify the Lab 16 input folder and prepare the output folder."""

    # Controlled Lab 16 input records must already exist.
    if not INPUT_FOLDER.exists():
        raise FileNotFoundError(
            f"Required input folder was not found: {INPUT_FOLDER}"
        )

    if not INPUT_FOLDER.is_dir():
        raise NotADirectoryError(
            f"Input path is not a folder: {INPUT_FOLDER}"
        )

    # Generated triage output may be safely created if needed.
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def create_utc_timestamp():
    """Create an ISO 8601 UTC timestamp for Lab 16 processing events."""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def create_triage_id():
    """Create a unique, non-sensitive identifier for one triage decision."""

    return f"TR-{uuid4()}"


def discover_alert_records():
    """Find supported Lab 15-style alert records in predictable order."""

    record_files = [
        file_path
        for file_path in INPUT_FOLDER.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    # Predictable ordering makes controlled validation repeatable.
    return sorted(record_files, key=lambda path: path.name.lower())


def load_alert_record(file_path):
    """Read one sanitized Lab 15-style JSON alert record."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Alert record was not found: {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            f"Alert record is empty: {file_path.name}"
        )

    with file_path.open("r", encoding="utf-8") as record_file:
        alert_record = json.load(record_file)

    # Lab 16 expects one JSON object representing one alert record.
    if not isinstance(alert_record, dict):
        raise ValueError(
            f"Alert record must contain one JSON object: {file_path.name}"
        )

    return alert_record


# Fields that must exist in every Lab 15-style record entering triage.
REQUIRED_ALERT_RECORD_FIELDS = {
    "record_id",
    "record_version",
    "source_platform",
    "event_type",
    "source_rule_id",
    "normalized_severity",
    "validation_status",
    "missing_fields",
    "validation_notes",
    "processing_history",
}


def validate_alert_record_for_triage(alert_record, source_filename):
    """Validate one Lab 15-style alert record before triage begins."""

    # Require the expected record structure without inventing absent fields.
    missing_schema_fields = sorted(
        field_name
        for field_name in REQUIRED_ALERT_RECORD_FIELDS
        if field_name not in alert_record
    )

    if missing_schema_fields:
        raise ValueError(
            f"Alert record is missing required schema fields "
            f"{missing_schema_fields}: {source_filename}"
        )

    record_id = alert_record.get("record_id")

    # Lab 16 only accepts existing Lab 15 alert-record identities.
    if not isinstance(record_id, str) or not record_id.startswith("AR-"):
        raise ValueError(
            f"Alert record does not contain a valid AR identifier: "
            f"{source_filename}"
        )

    validation_status = alert_record.get("validation_status")

    if validation_status not in ALLOWED_SOURCE_VALIDATION_STATUSES:
        raise ValueError(
            f"Alert record is not processable for Lab 16 triage: "
            f"{source_filename}"
        )

    normalized_severity = alert_record.get("normalized_severity")

    if normalized_severity not in ALLOWED_NORMALIZED_SEVERITIES:
        raise ValueError(
            f"Alert record contains an unsupported normalized severity: "
            f"{source_filename}"
        )

    # Missing-field and validation-note information must remain structured.
    if not isinstance(alert_record.get("missing_fields"), list):
        raise ValueError(
            f"missing_fields must be a list: {source_filename}"
        )

    if not isinstance(alert_record.get("validation_notes"), list):
        raise ValueError(
            f"validation_notes must be a list: {source_filename}"
        )

    if not isinstance(alert_record.get("processing_history"), list):
        raise ValueError(
            f"processing_history must be a list: {source_filename}"
        )

    return alert_record


def add_triage_history(
    triage_record,
    stage,
    outcome,
    notes="",
    timestamp=None,
):
    """Add one chronological event to a triage decision history."""

    history_timestamp = timestamp or create_utc_timestamp()

    history_entry = {
        "stage": stage,
        "timestamp": history_timestamp,
        "outcome": outcome,
        "notes": notes,
    }

    triage_record["triage_history"].append(history_entry)

    return triage_record


def create_triage_record(alert_record):
    """Create one vendor-neutral triage record linked to an existing AR record."""

    triage_timestamp = create_utc_timestamp()

    # Copy inherited list values so triage processing cannot modify
    # the corresponding lists inside the originating alert record.
    source_missing_fields = list(
        alert_record.get("missing_fields", [])
    )
    source_validation_notes = list(
        alert_record.get("validation_notes", [])
    )

    triage_record = {
        "triage_id": create_triage_id(),
        "triage_version": TRIAGE_VERSION,
        "record_id": alert_record["record_id"],
        "triage_timestamp": triage_timestamp,
        "source_validation_status": alert_record["validation_status"],
        "source_normalized_severity": alert_record["normalized_severity"],
        "source_missing_fields": source_missing_fields,
        "source_validation_notes": source_validation_notes,
        "triage_classification": None,
        "triage_confidence": None,
        "matched_rule_id": None,
        "classification_reason": None,
        "investigation_required": None,
        "human_review_required": None,
        "next_stage": None,
        "decision_notes": "",
        "triage_history": [],
    }

    # Use the same timestamp for the first lifecycle event so record
    # creation and the start of its history remain intentionally aligned.
    add_triage_history(
        triage_record,
        stage="Triage Record Created",
        outcome="Created",
        notes=(
            "Vendor-neutral Lab 16 triage record created and linked "
            "to the originating alert record."
        ),
        timestamp=triage_timestamp,
    )

    return triage_record


# Material context used by the controlled Lab 16 evidence-quality rule.
MATERIAL_TRIAGE_CONTEXT_FIELDS = {
    "endpoint_ip",
    "event_provider",
}


# Public-safe deterministic patterns used by the controlled Lab 16 rules.
KNOWN_APPLICATION_ERROR_PATTERN = {
    "event_type": "Windows application error event.",
    "source_rule_id": "60602",
}

KNOWN_AUTHENTICATION_FAILURE_PATTERN = {
    "event_type": "Repeated failed authentication activity.",
    "source_rule_id": "61002",
}

UNUSUAL_CONFIGURATION_CHANGE_PATTERN = {
    "event_type": "Controlled unusual configuration-change event.",
    "source_rule_id": "64004",
}


def apply_triage_decision(
    triage_record,
    classification,
    confidence,
    matched_rule_id,
    reason,
    investigation_required,
    human_review_required,
    next_stage,
    decision_notes="",
):
    """Apply one complete deterministic triage decision to a TR record."""

    # Refuse values outside the frozen Lab 16 design.
    if classification not in TRIAGE_CLASSIFICATIONS:
        raise ValueError(
            f"Unsupported triage classification: {classification}"
        )

    if confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
        raise ValueError(
            f"Unsupported triage confidence value: {confidence}"
        )

    if next_stage not in NEXT_STAGE_VALUES:
        raise ValueError(
            f"Unsupported next-stage routing value: {next_stage}"
        )

    triage_record["triage_classification"] = classification
    triage_record["triage_confidence"] = confidence
    triage_record["matched_rule_id"] = matched_rule_id
    triage_record["classification_reason"] = reason
    triage_record["investigation_required"] = investigation_required
    triage_record["human_review_required"] = human_review_required
    triage_record["next_stage"] = next_stage
    triage_record["decision_notes"] = decision_notes

    add_triage_history(
        triage_record,
        stage="Triage Decision Assigned",
        outcome=classification,
        notes=(
            f"{matched_rule_id} assigned {classification} "
            f"and routed the record to {next_stage}."
        ),
    )

    return triage_record


def has_material_evidence_quality_problem(alert_record):
    """Check whether material missing context prevents reliable triage."""

    missing_fields = set(
        alert_record.get("missing_fields", [])
    )

    material_missing_fields = sorted(
        missing_fields.intersection(
            MATERIAL_TRIAGE_CONTEXT_FIELDS
        )
    )

    return material_missing_fields


def apply_insufficient_data_rule(alert_record, triage_record):
    """Apply TRIAGE-RULE-001 when material triage evidence is unavailable."""

    material_missing_fields = has_material_evidence_quality_problem(
        alert_record
    )

    if not material_missing_fields:
        return False

    reason = (
        "The available alert record is processable, but material evidence "
        "needed for reliable triage is missing or unreliable."
    )

    decision_notes = (
        "Material missing fields: "
        + ", ".join(material_missing_fields)
        + ". Evidence-quality problems take priority over known-pattern matching."
    )

    apply_triage_decision(
        triage_record,
        classification="INSUFFICIENT_DATA",
        confidence="HIGH",
        matched_rule_id="TRIAGE-RULE-001",
        reason=reason,
        investigation_required=True,
        human_review_required=False,
        next_stage="INVESTIGATION",
        decision_notes=decision_notes,
    )

    return True


def matches_pattern(alert_record, pattern):
    """Check whether an alert record matches one controlled deterministic pattern."""

    return all(
        alert_record.get(field_name) == expected_value
        for field_name, expected_value in pattern.items()
    )


def apply_known_application_error_rule(alert_record, triage_record):
    """Apply TRIAGE-RULE-002 to the supported application-error pattern."""

    if not matches_pattern(
        alert_record,
        KNOWN_APPLICATION_ERROR_PATTERN,
    ):
        return False

    apply_triage_decision(
        triage_record,
        classification="KNOWN_COMMON",
        confidence="HIGH",
        matched_rule_id="TRIAGE-RULE-002",
        reason=(
            "The event matches the documented Lab 16 Windows application "
            "error pattern using validated event and rule context."
        ),
        investigation_required=False,
        human_review_required=False,
        next_stage="POLICY_EVALUATION",
        decision_notes=(
            "KNOWN_COMMON identifies a supported deterministic pattern. "
            "It does not mean the condition is benign, resolved, or "
            "authorized for remediation."
        ),
    )

    return True


def apply_known_authentication_failure_rule(alert_record, triage_record):
    """Apply TRIAGE-RULE-003 to the supported authentication-failure pattern."""

    if not matches_pattern(
        alert_record,
        KNOWN_AUTHENTICATION_FAILURE_PATTERN,
    ):
        return False

    apply_triage_decision(
        triage_record,
        classification="KNOWN_COMMON",
        confidence="HIGH",
        matched_rule_id="TRIAGE-RULE-003",
        reason=(
            "The event matches the documented Lab 16 repeated authentication "
            "failure pattern using validated event and rule context."
        ),
        investigation_required=False,
        human_review_required=False,
        next_stage="POLICY_EVALUATION",
        decision_notes=(
            "The deterministic event and rule pattern caused this classification. "
            "HIGH technical severity did not independently determine the result."
        ),
    )

    return True


def apply_unusual_configuration_change_rule(alert_record, triage_record):
    """Apply TRIAGE-RULE-004 to the controlled unusual configuration pattern."""

    if not matches_pattern(
        alert_record,
        UNUSUAL_CONFIGURATION_CHANGE_PATTERN,
    ):
        return False

    apply_triage_decision(
        triage_record,
        classification="UNUSUAL",
        confidence="MEDIUM",
        matched_rule_id="TRIAGE-RULE-004",
        reason=(
            "The event matches the documented Lab 16 controlled unusual "
            "configuration-change pattern and falls outside the currently "
            "supported known/common response catalog."
        ),
        investigation_required=True,
        human_review_required=False,
        next_stage="INVESTIGATION",
        decision_notes=(
            "UNUSUAL identifies a supported triage pattern requiring "
            "investigation. It does not automatically mean malicious activity."
        ),
    )

    return True


def apply_unknown_fallback_rule(alert_record, triage_record):
    """Apply TRIAGE-RULE-005 when no more specific supported rule matched."""

    apply_triage_decision(
        triage_record,
        classification="UNKNOWN",
        confidence="LOW",
        matched_rule_id="TRIAGE-RULE-005",
        reason=(
            "Usable evidence exists, but the currently supported deterministic "
            "rules cannot establish a more reliable triage classification."
        ),
        investigation_required=True,
        human_review_required=False,
        next_stage="INVESTIGATION",
        decision_notes=(
            "UNKNOWN preserves uncertainty until additional evidence supports "
            "a more reliable determination. Technical severity does not "
            "convert the condition into a known or safe state."
        ),
    )

    return True


def evaluate_triage_rules(alert_record, triage_record):
    """Evaluate Lab 16 triage rules in the frozen deterministic priority order."""

    add_triage_history(
        triage_record,
        stage="Triage Rule Evaluation Started",
        outcome="Started",
        notes=(
            "Deterministic triage rules are evaluated in the frozen "
            "Lab 16 priority order."
        ),
    )

    # Rule 001 has highest priority because evidence-quality problems
    # must override otherwise recognizable event patterns.
    if apply_insufficient_data_rule(alert_record, triage_record):
        return triage_record

    # Known/common rules are considered only after evidence quality passes.
    if apply_known_application_error_rule(alert_record, triage_record):
        return triage_record

    if apply_known_authentication_failure_rule(alert_record, triage_record):
        return triage_record

    # The controlled unusual pattern is evaluated after supported
    # known/common patterns have been ruled out.
    if apply_unusual_configuration_change_rule(alert_record, triage_record):
        return triage_record

    # Anything still processable but not established by a more specific
    # supported rule retains an explicit UNKNOWN classification.
    apply_unknown_fallback_rule(alert_record, triage_record)

    return triage_record


def process_single_alert_record(file_path):
    """Process one Lab 15 alert record independently through Lab 16 triage."""

    try:
        # Load the existing Lab 15-style alert record.
        alert_record = load_alert_record(file_path)

        # Confirm the record is structurally eligible for Lab 16 triage.
        validate_alert_record_for_triage(
            alert_record,
            file_path.name,
        )

        # Create a separate TR decision record without changing the AR record.
        triage_record = create_triage_record(alert_record)

        # Apply the frozen deterministic rule sequence.
        evaluate_triage_rules(
            alert_record,
            triage_record,
        )

	 # Preserve the completed decision as a separate structured TR record.
        triage_path = write_triage_record(
            triage_record,
            file_path.name,
        )

        return {
            "source_file": file_path.name,
            "processing_result": "Triaged Successfully",
            "record_id": alert_record["record_id"],
            "triage_record": triage_record,
            "triage_path": triage_path,
            "error": None,
        }

    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
    ) as error:
        return {
            "source_file": file_path.name,
            "processing_result": "Failed",
            "record_id": None,
            "triage_record": None,
            "triage_path": None,
            "error": str(error),
        }


def create_unique_triage_path(source_filename, triage_id):
    """Create a unique output path for one Lab 16 triage decision record."""

    source_stem = Path(source_filename).stem
    base_name = f"{source_stem}_{triage_id}"
    triage_path = OUTPUT_FOLDER / f"{base_name}.json"

    collision_number = 2

    while triage_path.exists():
        triage_path = OUTPUT_FOLDER / (
            f"{base_name}_{collision_number}.json"
        )
        collision_number += 1

    return triage_path


def write_triage_record(triage_record, source_filename):
    """Write one structured Lab 16 triage decision without overwriting prior output."""

    triage_path = create_unique_triage_path(
        source_filename,
        triage_record["triage_id"],
    )

    # Record that the decision has reached the controlled output stage.
    add_triage_history(
        triage_record,
        stage="Triage Output Prepared",
        outcome="Prepared",
        notes=(
            "Structured Lab 16 triage decision prepared for JSON output."
        ),
    )

    with triage_path.open("w", encoding="utf-8") as triage_file:
        json.dump(
            triage_record,
            triage_file,
            indent=4,
            ensure_ascii=False,
        )

    return triage_path


def calculate_batch_totals(batch_data):
    """Calculate Lab 16 totals from actual per-record triage results."""

    results = batch_data["results"]
    alert_files = batch_data["alert_files"]

    known_common = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["triage_classification"] == "KNOWN_COMMON"
    )

    insufficient_data = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["triage_classification"] == "INSUFFICIENT_DATA"
    )

    unusual = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["triage_classification"] == "UNUSUAL"
    )

    unknown = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["triage_classification"] == "UNKNOWN"
    )

    policy_evaluation = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["next_stage"] == "POLICY_EVALUATION"
    )

    investigation = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["next_stage"] == "INVESTIGATION"
    )

    human_review = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["next_stage"] == "HUMAN_REVIEW"
    )

    no_action_yet = sum(
        1
        for result in results
        if result["triage_record"] is not None
        and result["triage_record"]["next_stage"] == "NO_ACTION_YET"
    )

    records_created = sum(
        1
        for result in results
        if result["triage_path"] is not None
    )

    failed = sum(
        1
        for result in results
        if result["processing_result"] == "Failed"
    )

    return {
        "total_discovered": len(alert_files),
        "known_common": known_common,
        "insufficient_data": insufficient_data,
        "unusual": unusual,
        "unknown": unknown,
        "policy_evaluation": policy_evaluation,
        "investigation": investigation,
        "human_review": human_review,
        "no_action_yet": no_action_yet,
        "records_created": records_created,
        "failed": failed,
    }


def process_alert_batch():
    """Process all supported Lab 16 alert records during one controlled run."""

    validate_workspace()

    # Record when this controlled batch-processing run began.
    run_timestamp = create_utc_timestamp()

    alert_files = discover_alert_records()
    results = []

    # Each record is processed independently so one failure cannot
    # prevent the remaining records from reaching triage.
    for file_path in alert_files:
        result = process_single_alert_record(file_path)
        results.append(result)

    batch_data = {
        "run_timestamp": run_timestamp,
        "alert_files": alert_files,
        "results": results,
    }

    # Calculate totals only after every discovered record was attempted.
    batch_data["totals"] = calculate_batch_totals(batch_data)

    # Create one auditable summary for this controlled processing run.
    summary_path = write_batch_summary(batch_data)
    batch_data["summary_path"] = summary_path

    return batch_data

def display_value(value):
    """Return a readable value for Lab 16 summary output."""

    if value is None or value == "":
        return "Unavailable"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def build_batch_result_entry(result):
    """Build one AR-to-TR traceability entry for the Lab 16 batch summary."""

    triage_record = result["triage_record"]
    triage_path = result["triage_path"]

    if triage_record is not None:
        record_id = display_value(
            triage_record.get("record_id")
        )
        triage_id = display_value(
            triage_record.get("triage_id")
        )
        classification = display_value(
            triage_record.get("triage_classification")
        )
        confidence = display_value(
            triage_record.get("triage_confidence")
        )
        matched_rule_id = display_value(
            triage_record.get("matched_rule_id")
        )
        investigation_required = display_value(
            triage_record.get("investigation_required")
        )
        human_review_required = display_value(
            triage_record.get("human_review_required")
        )
        next_stage = display_value(
            triage_record.get("next_stage")
        )
    else:
        record_id = display_value(
            result.get("record_id")
        )
        triage_id = "Unavailable"
        classification = "Unavailable"
        confidence = "Unavailable"
        matched_rule_id = "Unavailable"
        investigation_required = "Unavailable"
        human_review_required = "Unavailable"
        next_stage = "Unavailable"

    triage_file = (
        triage_path.name
        if triage_path is not None
        else "Not Created"
    )

    entry_lines = [
        f"Source File: {result['source_file']}",
        f"Processing Result: {result['processing_result']}",
        f"Alert Record ID: {record_id}",
        f"Triage Decision ID: {triage_id}",
        f"Triage Classification: {classification}",
        f"Triage Confidence: {confidence}",
        f"Matched Rule ID: {matched_rule_id}",
        f"Investigation Required: {investigation_required}",
        f"Human Review Required: {human_review_required}",
        f"Next Stage: {next_stage}",
        f"Triage Record File: {triage_file}",
    ]

    if result["processing_result"] == "Failed":
        failure_reason = result["error"]

        if not failure_reason:
            failure_reason = (
                "Alert-record triage failed without a detailed reason."
            )

        entry_lines.append(
            f"Failure Reason: {failure_reason}"
        )

    return "\n".join(entry_lines)


def build_batch_summary(batch_data):
    """Build one auditable Lab 16 batch-processing summary."""

    totals = batch_data["totals"]
    results = batch_data["results"]

    if results:
        per_record_results = "\n\n".join(
            build_batch_result_entry(result)
            for result in results
        )
    else:
        per_record_results = (
            "No supported alert records were processed."
        )

    if len(results) == totals["total_discovered"]:
        completion_status = (
            "All discovered supported alert records were attempted."
        )
    else:
        completion_status = (
            "Batch processing ended before all discovered records "
            "were attempted."
        )

    return (
        "Lab 16 - Alert Triage and Decision Logic\n"
        "Batch Summary\n\n"
        f"Processing Run: {batch_data['run_timestamp']}\n"
        f"Input Location: {INPUT_FOLDER.name}\n"
        f"Output Location: {OUTPUT_FOLDER.name}\n\n"

        "Processing Totals\n"
        f"Total Processable Alert Records Discovered: "
        f"{totals['total_discovered']}\n"
        f"KNOWN_COMMON: {totals['known_common']}\n"
        f"INSUFFICIENT_DATA: {totals['insufficient_data']}\n"
        f"UNUSUAL: {totals['unusual']}\n"
        f"UNKNOWN: {totals['unknown']}\n\n"

        "Next-Stage Routing Totals\n"
        f"POLICY_EVALUATION: {totals['policy_evaluation']}\n"
        f"INVESTIGATION: {totals['investigation']}\n"
        f"HUMAN_REVIEW: {totals['human_review']}\n"
        f"NO_ACTION_YET: {totals['no_action_yet']}\n\n"

        "Output Totals\n"
        f"Triage Decision Records Created: "
        f"{totals['records_created']}\n"
        f"Failed: {totals['failed']}\n\n"

        "Per-Record AR-to-TR Traceability\n"
        f"{per_record_results}\n\n"

        "Batch Completion\n"
        f"{completion_status}\n\n"

        "Safety Statement\n"
        "Lab 16 classified and routed alert records only. "
        "No defensive action was authorized or executed.\n"
    )


def create_filename_timestamp():
    """Create a Windows-safe UTC timestamp for generated filenames."""

    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def create_unique_batch_summary_path():
    """Create a unique output path for one Lab 16 batch summary."""

    filename_timestamp = create_filename_timestamp()
    base_name = f"batch_summary_{filename_timestamp}"
    summary_path = OUTPUT_FOLDER / f"{base_name}.txt"

    collision_number = 2

    while summary_path.exists():
        summary_path = OUTPUT_FOLDER / (
            f"{base_name}_{collision_number}.txt"
        )
        collision_number += 1

    return summary_path


def write_batch_summary(batch_data):
    """Write one Lab 16 batch summary without overwriting prior output."""

    summary_text = build_batch_summary(batch_data)
    summary_path = create_unique_batch_summary_path()

    with summary_path.open("w", encoding="utf-8") as summary_file:
        summary_file.write(summary_text)

    return summary_path


def main():
    """Run the complete Lab 16 alert-triage validation workflow."""

    try:
        batch_data = process_alert_batch()

        totals = batch_data["totals"]
        summary_path = batch_data["summary_path"]

        print("Lab 16 alert-triage processing complete.")
        print(
            f"Alert records discovered: "
            f"{totals['total_discovered']}"
        )
        print(
            f"KNOWN_COMMON: "
            f"{totals['known_common']}"
        )
        print(
            f"INSUFFICIENT_DATA: "
            f"{totals['insufficient_data']}"
        )
        print(
            f"UNUSUAL: "
            f"{totals['unusual']}"
        )
        print(
            f"UNKNOWN: "
            f"{totals['unknown']}"
        )
        print(
            f"POLICY_EVALUATION: "
            f"{totals['policy_evaluation']}"
        )
        print(
            f"INVESTIGATION: "
            f"{totals['investigation']}"
        )
        print(
            f"HUMAN_REVIEW: "
            f"{totals['human_review']}"
        )
        print(
            f"NO_ACTION_YET: "
            f"{totals['no_action_yet']}"
        )
        print(
            f"Triage decision records created: "
            f"{totals['records_created']}"
        )
        print(
            f"Failed: "
            f"{totals['failed']}"
        )
        print(
            f"Batch summary: "
            f"{summary_path.name}"
        )

    except (
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
    ) as error:
        print(
            f"Lab 16 processing could not start or "
            f"complete safely: {error}"
        )


if __name__ == "__main__":
    main()