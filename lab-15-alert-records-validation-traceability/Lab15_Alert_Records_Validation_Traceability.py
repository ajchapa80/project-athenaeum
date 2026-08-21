"""
Project Athenaeum
Lab 15 — Alert Records, Validation, and Traceability

Public portfolio implementation.

Purpose:
- Convert supported sanitized alert files into vendor-neutral JSON records.
- Preserve source identifiers, timestamps, severity values, and source data.
- Detect missing or malformed information.
- Maintain deterministic validation outcomes and processing history.
- Isolate failures so one invalid alert does not stop the batch.
- Generate batch summaries from actual processing results.
- Avoid modifying source files or overwriting previous output.

This module intentionally contains no proprietary Business Guardian connector,
investigation, approval, remediation, or defensive-action implementation.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"

PROCESSED_NORMALLY = "Processed Normally"
PROCESSED_WITH_WARNINGS = "Processed With Warnings"
FAILED_VALIDATION = "Failed Validation"

REQUIRED_FIELDS = (
    "source_alert_id",
    "source_timestamp",
    "endpoint_name",
)

OPTIONAL_TRACKED_FIELDS = (
    "endpoint_ip",
    "event_provider",
)

SUPPORTED_FIELDS = {
    "source_alert_id",
    "source_platform",
    "source_timestamp",
    "endpoint_name",
    "endpoint_ip",
    "event_provider",
    "source_severity",
    "event_type",
    "message",
}

SEVERITY_LEVELS = {
    0: "INFORMATIONAL",
    1: "LOW",
    2: "LOW",
    3: "LOW",
    4: "LOW",
    5: "LOW",
    6: "MEDIUM",
    7: "MEDIUM",
    8: "MEDIUM",
    9: "MEDIUM",
    10: "HIGH",
    11: "HIGH",
    12: "HIGH",
    13: "HIGH",
    14: "CRITICAL",
    15: "CRITICAL",
}


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


def create_alert_record_id() -> str:
    """
    Create a non-sensitive record identifier.

    The identifier is intentionally unrelated to source data.
    """

    return f"AR-{uuid.uuid4()}"


@dataclass
class ProcessingHistoryEntry:
    """One auditable processing-history event."""

    stage: str
    timestamp: str
    outcome: str
    notes: str


@dataclass
class AlertRecord:
    """Vendor-neutral processable alert record."""

    schema_version: str
    alert_record_id: str

    source_alert_id: str
    source_platform: str
    source_file: str
    source_timestamp: str
    ingestion_timestamp: str

    endpoint_name: str | None
    endpoint_ip: str | None
    event_provider: str | None

    source_severity: str | None
    normalized_severity: str

    event_type: str | None
    message: str | None

    validation_outcome: str
    missing_fields: list[str] = field(default_factory=list)
    validation_notes: list[str] = field(default_factory=list)

    processing_history: list[ProcessingHistoryEntry] = field(
        default_factory=list
    )

    raw_supported_source_data: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProcessingResult:
    """Result of processing one source alert file."""

    source_file: str
    validation_outcome: str
    alert_record_id: str | None
    output_file: str | None
    notes: list[str] = field(default_factory=list)


def parse_alert_file(path: Path) -> dict[str, str]:
    """
    Parse a simple sanitized key=value alert file.

    Unknown fields are ignored by the normalized record but remain harmless
    input. Lines without '=' are not interpreted as instructions or code.
    """

    parsed: dict[str, str] = {}

    for raw_line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        normalized_key = key.strip()
        normalized_value = value.strip()

        if normalized_key:
            parsed[normalized_key] = normalized_value

    return parsed


def preserve_supported_source_data(
    parsed: dict[str, str],
) -> dict[str, str]:
    """Preserve supported source fields without inventing values."""

    return {
        key: value
        for key, value in parsed.items()
        if key in SUPPORTED_FIELDS
    }


def normalize_severity(
    source_value: str | None,
) -> tuple[str, list[str]]:
    """
    Normalize source severity safely.

    Malformed source values remain preserved elsewhere in the alert record.
    """

    notes: list[str] = []

    if source_value is None or not source_value.strip():
        notes.append(
            "Source severity was unavailable; normalized severity is UNKNOWN."
        )
        return "UNKNOWN", notes

    try:
        numeric_value = int(
            source_value.strip()
        )
    except ValueError:
        notes.append(
            "Source severity was malformed and was preserved without "
            "guessing a replacement value."
        )
        return "UNKNOWN", notes

    if numeric_value not in SEVERITY_LEVELS:
        notes.append(
            "Source severity was outside the supported normalization range; "
            "normalized severity is UNKNOWN."
        )
        return "UNKNOWN", notes

    return SEVERITY_LEVELS[numeric_value], notes


def determine_missing_fields(
    parsed: dict[str, str],
) -> list[str]:
    """Identify required or tracked information that is unavailable."""

    missing: list[str] = []

    for field_name in REQUIRED_FIELDS + OPTIONAL_TRACKED_FIELDS:
        value = parsed.get(
            field_name,
            "",
        ).strip()

        if not value:
            missing.append(
                field_name
            )

    return missing


def has_supported_alert_content(
    parsed: dict[str, str],
) -> bool:
    """
    Determine whether the file contains recognizable alert information.

    At least one core identifying field must exist before a processable
    record can be created.
    """

    core_fields = {
        "source_alert_id",
        "source_timestamp",
        "endpoint_name",
        "event_type",
        "message",
    }

    return any(
        parsed.get(field_name, "").strip()
        for field_name in core_fields
    )


def build_alert_record(
    *,
    source_file: Path,
    parsed: dict[str, str],
) -> AlertRecord:
    """Create one structured vendor-neutral alert record."""

    ingestion_timestamp = utc_now_iso()
    processing_history: list[ProcessingHistoryEntry] = []

    processing_history.append(
        ProcessingHistoryEntry(
            stage="INGESTION",
            timestamp=ingestion_timestamp,
            outcome="SOURCE RECEIVED",
            notes=(
                "Supported source file received for controlled "
                "record processing."
            ),
        )
    )

    missing_fields = determine_missing_fields(
        parsed
    )

    normalized_severity, severity_notes = normalize_severity(
        parsed.get(
            "source_severity"
        )
    )

    validation_notes = list(
        severity_notes
    )

    for field_name in missing_fields:
        validation_notes.append(
            f"{field_name} was unavailable in the source alert."
        )

    has_warning = bool(
        missing_fields
        or severity_notes
    )

    validation_outcome = (
        PROCESSED_WITH_WARNINGS
        if has_warning
        else PROCESSED_NORMALLY
    )

    processing_history.append(
        ProcessingHistoryEntry(
            stage="VALIDATION",
            timestamp=utc_now_iso(),
            outcome=validation_outcome,
            notes=(
                "Alert data validated without fabrication. "
                "Missing or malformed values were recorded explicitly."
            ),
        )
    )

    record_id = create_alert_record_id()

    processing_history.append(
        ProcessingHistoryEntry(
            stage="RECORD_CREATION",
            timestamp=utc_now_iso(),
            outcome="RECORD CREATED",
            notes=(
                "Vendor-neutral alert record created with a "
                "non-sensitive UUID-based identifier."
            ),
        )
    )

    def optional_value(
        field_name: str,
    ) -> str | None:
        value = parsed.get(
            field_name,
            "",
        ).strip()

        return value if value else None

    return AlertRecord(
        schema_version=SCHEMA_VERSION,
        alert_record_id=record_id,
        source_alert_id=parsed.get(
            "source_alert_id",
            "",
        ).strip(),
        source_platform=parsed.get(
            "source_platform",
            "UNKNOWN",
        ).strip()
        or "UNKNOWN",
        source_file=source_file.name,
        source_timestamp=parsed.get(
            "source_timestamp",
            "",
        ).strip(),
        ingestion_timestamp=ingestion_timestamp,
        endpoint_name=optional_value(
            "endpoint_name"
        ),
        endpoint_ip=optional_value(
            "endpoint_ip"
        ),
        event_provider=optional_value(
            "event_provider"
        ),
        source_severity=optional_value(
            "source_severity"
        ),
        normalized_severity=normalized_severity,
        event_type=optional_value(
            "event_type"
        ),
        message=optional_value(
            "message"
        ),
        validation_outcome=validation_outcome,
        missing_fields=missing_fields,
        validation_notes=validation_notes,
        processing_history=processing_history,
        raw_supported_source_data=preserve_supported_source_data(
            parsed
        ),
    )


def write_json(
    *,
    path: Path,
    data: dict[str, Any],
) -> None:
    """Write formatted JSON to a new output path."""

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def create_run_directory(
    output_root: Path,
) -> Path:
    """
    Create a unique run directory.

    Existing output is never overwritten.
    """

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    run_directory = output_root / f"run_{timestamp}"

    run_directory.mkdir(
        parents=True,
        exist_ok=False,
    )

    return run_directory


def process_alert_file(
    *,
    source_file: Path,
    run_directory: Path,
) -> ProcessingResult:
    """Process one alert independently from every other alert."""

    try:
        parsed = parse_alert_file(
            source_file
        )

        if not has_supported_alert_content(
            parsed
        ):
            return ProcessingResult(
                source_file=source_file.name,
                validation_outcome=FAILED_VALIDATION,
                alert_record_id=None,
                output_file=None,
                notes=[
                    (
                        "No recognized alert fields were found. "
                        "No processable alert record was created."
                    )
                ],
            )

        record = build_alert_record(
            source_file=source_file,
            parsed=parsed,
        )

        output_filename = (
            f"{source_file.stem}_record_"
            f"{record.alert_record_id}.json"
        )

        output_path = (
            run_directory
            / output_filename
        )

        write_json(
            path=output_path,
            data=asdict(record),
        )

        return ProcessingResult(
            source_file=source_file.name,
            validation_outcome=record.validation_outcome,
            alert_record_id=record.alert_record_id,
            output_file=output_filename,
            notes=list(
                record.validation_notes
            ),
        )

    except Exception as exc:
        return ProcessingResult(
            source_file=source_file.name,
            validation_outcome=FAILED_VALIDATION,
            alert_record_id=None,
            output_file=None,
            notes=[
                (
                    "Alert processing failed safely: "
                    f"{type(exc).__name__}"
                )
            ],
        )


def build_batch_summary(
    *,
    run_directory: Path,
    discovered_files: list[Path],
    results: list[ProcessingResult],
) -> dict[str, Any]:
    """Create an auditable summary using actual processing results."""

    normal_count = sum(
        result.validation_outcome
        == PROCESSED_NORMALLY
        for result in results
    )

    warning_count = sum(
        result.validation_outcome
        == PROCESSED_WITH_WARNINGS
        for result in results
    )

    failed_count = sum(
        result.validation_outcome
        == FAILED_VALIDATION
        for result in results
    )

    records_created = sum(
        result.alert_record_id
        is not None
        for result in results
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "summary_type": "LAB15_BATCH_SUMMARY",
        "generated_at": utc_now_iso(),
        "run_directory": run_directory.name,
        "total_supported_alert_files_discovered": len(
            discovered_files
        ),
        "processed_normally": normal_count,
        "processed_with_warnings": warning_count,
        "failed_validation": failed_count,
        "processable_alert_records_created": records_created,
        "batch_summaries_created": 1,
        "results": [
            asdict(result)
            for result in results
        ],
    }


def print_batch_summary(
    summary: dict[str, Any],
) -> None:
    """Display concise deterministic batch totals."""

    print(
        "Total Supported Alert Files Discovered:",
        summary[
            "total_supported_alert_files_discovered"
        ],
    )
    print(
        "Processed Normally:",
        summary[
            "processed_normally"
        ],
    )
    print(
        "Processed With Warnings:",
        summary[
            "processed_with_warnings"
        ],
    )
    print(
        "Failed Validation:",
        summary[
            "failed_validation"
        ],
    )
    print(
        "Processable Alert Records Created:",
        summary[
            "processable_alert_records_created"
        ],
    )
    print(
        "Batch Summaries Created:",
        summary[
            "batch_summaries_created"
        ],
    )


def main() -> None:
    """Run controlled Lab 15 batch processing."""

    lab_directory = Path(
        __file__
    ).resolve().parent

    input_directory = (
        lab_directory
        / "input"
    )

    output_root = (
        lab_directory
        / "output"
    )

    input_directory.mkdir(
        exist_ok=True
    )

    output_root.mkdir(
        exist_ok=True
    )

    discovered_files = sorted(
        path
        for path in input_directory.glob(
            "*.txt"
        )
        if path.is_file()
    )

    run_directory = create_run_directory(
        output_root
    )

    results: list[ProcessingResult] = []

    for source_file in discovered_files:
        result = process_alert_file(
            source_file=source_file,
            run_directory=run_directory,
        )

        results.append(
            result
        )

    summary = build_batch_summary(
        run_directory=run_directory,
        discovered_files=discovered_files,
        results=results,
    )

    summary_path = (
        run_directory
        / "Lab15_Batch_Summary.json"
    )

    write_json(
        path=summary_path,
        data=summary,
    )

    print_batch_summary(
        summary
    )


if __name__ == "__main__":
    main()
