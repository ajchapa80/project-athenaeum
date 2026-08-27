# ============================================================
# Project Athenaeum
# Lab 17 - Policy Evaluation and Approval Logic
#
# Purpose:
# Evaluate sanitized Lab 16-style triage records against a
# deterministic public-safe policy model.
#
# This lab creates policy and approval records only.
# It DOES NOT execute defensive actions or remediation.
# ============================================================

import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


# ------------------------------------------------------------
# LAB WORKSPACE
# ------------------------------------------------------------

# Use the folder containing this Python script as the Lab 17
# workspace. This keeps the script portable and prevents us
# from hard-coding personal Windows paths.
LAB_FOLDER = Path(__file__).parent

INPUT_FOLDER = LAB_FOLDER / "input"
OUTPUT_FOLDER = LAB_FOLDER / "output"

SUPPORTED_EXTENSIONS = {".json"}


# ------------------------------------------------------------
# LAB 17 VERSION
# ------------------------------------------------------------

POLICY_VERSION = "1.0"
APPROVAL_VERSION = "1.0"


# ------------------------------------------------------------
# FROZEN POLICY OUTCOMES
# ------------------------------------------------------------

ALLOWED_POLICY_OUTCOMES = {
    "AUTHORIZED",
    "REQUIRES_APPROVAL",
    "NOT_AUTHORIZED",
    "DEFERRED_TO_INVESTIGATION",
}


# ------------------------------------------------------------
# FROZEN APPROVAL STATUSES
# ------------------------------------------------------------

ALLOWED_APPROVAL_STATUSES = {
    "NOT_REQUIRED",
    "PENDING",
    "APPROVED",
    "DENIED",
}


# ------------------------------------------------------------
# FROZEN FINAL WORKFLOW STATES
# ------------------------------------------------------------

ALLOWED_FINAL_WORKFLOW_STATES = {
    "READY_FOR_ACTION",
    "AWAITING_APPROVAL",
    "INVESTIGATION",
    "NO_ACTION_AUTHORIZED",
}


# ------------------------------------------------------------
# SUPPORTED SOURCE VALUES
# ------------------------------------------------------------

ALLOWED_TRIAGE_CLASSIFICATIONS = {
    "KNOWN_COMMON",
    "UNUSUAL",
    "UNKNOWN",
    "INSUFFICIENT_DATA",
}

ALLOWED_TRIAGE_NEXT_STAGES = {
    "POLICY_EVALUATION",
    "INVESTIGATION",
    "HUMAN_REVIEW",
    "NO_ACTION_YET",
}

ALLOWED_NORMALIZED_SEVERITIES = {
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
    "UNKNOWN",
}

ALLOWED_CONTROLLED_APPROVAL_RESPONSES = {
    "PENDING",
    "APPROVED",
    "DENIED",
}


# ------------------------------------------------------------
# WORKSPACE VALIDATION
# ------------------------------------------------------------

def validate_workspace():
    """
    Confirm that the expected Lab 17 folders exist before
    processing begins.

    The output folder may be empty, but both input and output
    folders must already exist.
    """

    if not INPUT_FOLDER.exists():
        raise FileNotFoundError(
            f"Input folder not found: {INPUT_FOLDER}"
        )

    if not INPUT_FOLDER.is_dir():
        raise NotADirectoryError(
            f"Input path is not a folder: {INPUT_FOLDER}"
        )

    if not OUTPUT_FOLDER.exists():
        raise FileNotFoundError(
            f"Output folder not found: {OUTPUT_FOLDER}"
        )

    if not OUTPUT_FOLDER.is_dir():
        raise NotADirectoryError(
            f"Output path is not a folder: {OUTPUT_FOLDER}"
        )


# ------------------------------------------------------------
# UTC TIMESTAMP HELPERS
# ------------------------------------------------------------

def create_utc_timestamp():
    """
    Create a consistent UTC timestamp for JSON records and
    chronological policy / approval history.
    """

    return datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def create_filename_timestamp():
    """
    Create a Windows-safe UTC timestamp for batch-summary
    filenames.

    Example:
        20260827_171500Z
    """

    return datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%SZ"
    )


# ------------------------------------------------------------
# RECORD IDENTITY HELPERS
# ------------------------------------------------------------

def create_policy_decision_id():
    """
    Create a unique Policy Decision identifier.

    Existing AR and TR identifiers are never replaced.
    """

    return f"PD-{uuid4()}"


def create_approval_id():
    """
    Create a unique Approval Record identifier.

    This function should only be used when policy requires
    a separate approval record.
    """

    return f"AP-{uuid4()}"


# ------------------------------------------------------------
# INPUT DISCOVERY
# ------------------------------------------------------------

def discover_policy_inputs():
    """
    Find supported JSON policy-input files in the Lab 17
    input folder.

    Sorting the filenames keeps processing order predictable
    and makes batch validation easier to compare between runs.
    """

    policy_inputs = []

    for file_path in INPUT_FOLDER.iterdir():
        if (
            file_path.is_file()
            and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        ):
            policy_inputs.append(file_path)

    return sorted(policy_inputs)


# ------------------------------------------------------------
# JSON INPUT LOADER
# ------------------------------------------------------------

def load_policy_input(file_path):
    """
    Safely load one Lab 17 policy-input JSON file.

    The file must:
    - exist;
    - contain data;
    - contain valid UTF-8 JSON;
    - contain one JSON object.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Policy input file not found: {file_path.name}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            f"Policy input file is empty: {file_path.name}"
        )

    try:
        with file_path.open(
            "r",
            encoding="utf-8"
        ) as input_file:
            policy_input = json.load(input_file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path.name}: {error}"
        ) from error

    if not isinstance(policy_input, dict):
        raise ValueError(
            f"Policy input must contain one JSON object: "
            f"{file_path.name}"
        )

    return policy_input


# ------------------------------------------------------------
# SOURCE RECORD VALIDATION
# ------------------------------------------------------------

def validate_policy_input(policy_input, source_filename):
    """
    Validate the Lab 16-style triage record before any
    Lab 17 policy rule is allowed to evaluate it.

    Lab 17 must fail safely rather than invent missing
    evidence, authorization, or approval state.
    """

    required_fields = {
        "record_id",
        "triage_id",
        "triage_classification",
        "triage_confidence",
        "source_normalized_severity",
        "next_stage",
        "investigation_required",
        "human_review_required",
        "triage_rule_id",
        "triage_reason",
        "triage_history",
        "requested_action",
    }

    missing_fields = [
        field_name
        for field_name in required_fields
        if field_name not in policy_input
    ]

    if missing_fields:
        raise ValueError(
            f"{source_filename} is missing required fields: "
            f"{', '.join(sorted(missing_fields))}"
        )

    record_id = policy_input["record_id"]
    triage_id = policy_input["triage_id"]

    if (
        not isinstance(record_id, str)
        or not record_id.startswith("AR-")
    ):
        raise ValueError(
            f"{source_filename} contains an invalid record_id."
        )

    if (
        not isinstance(triage_id, str)
        or not triage_id.startswith("TR-")
    ):
        raise ValueError(
            f"{source_filename} contains an invalid triage_id."
        )

    triage_classification = policy_input[
        "triage_classification"
    ]

    if (
        triage_classification
        not in ALLOWED_TRIAGE_CLASSIFICATIONS
    ):
        raise ValueError(
            f"{source_filename} contains an unsupported "
            f"triage classification: {triage_classification}"
        )

    next_stage = policy_input["next_stage"]

    if next_stage not in ALLOWED_TRIAGE_NEXT_STAGES:
        raise ValueError(
            f"{source_filename} contains an unsupported "
            f"next_stage: {next_stage}"
        )

    normalized_severity = policy_input[
        "source_normalized_severity"
    ]

    if (
        normalized_severity
        not in ALLOWED_NORMALIZED_SEVERITIES
    ):
        raise ValueError(
            f"{source_filename} contains an unsupported "
            f"normalized severity: {normalized_severity}"
        )

    requested_action = policy_input["requested_action"]

    if (
        not isinstance(requested_action, str)
        or not requested_action.strip()
    ):
        raise ValueError(
            f"{source_filename} must contain a non-empty "
            f"requested_action."
        )

    if not isinstance(policy_input["triage_history"], list):
        raise ValueError(
            f"{source_filename} contains an invalid "
            f"triage_history. Expected a list."
        )

    controlled_approval_response = policy_input.get(
        "controlled_approval_response"
    )

    if (
        controlled_approval_response is not None
        and controlled_approval_response
        not in ALLOWED_CONTROLLED_APPROVAL_RESPONSES
    ):
        raise ValueError(
            f"{source_filename} contains an unsupported "
            f"controlled_approval_response: "
            f"{controlled_approval_response}"
        )

    if not isinstance(
        policy_input["investigation_required"],
        bool
    ):
        raise ValueError(
            f"{source_filename} contains an invalid "
            f"investigation_required value."
        )

    if not isinstance(
        policy_input["human_review_required"],
        bool
    ):
        raise ValueError(
            f"{source_filename} contains an invalid "
            f"human_review_required value."
        )

    return True


# ------------------------------------------------------------
# POLICY HISTORY HELPER
# ------------------------------------------------------------

def add_policy_history(
    policy_record,
    stage,
    details,
    rule_id=None
):
    """
    Add one chronological entry to the Policy Decision
    history.

    A rule ID is included only when a specific deterministic
    policy rule is associated with the history event.
    """

    history_entry = {
        "timestamp": create_utc_timestamp(),
        "stage": stage,
        "details": details,
    }

    if rule_id is not None:
        history_entry["rule_id"] = rule_id

    policy_record["policy_history"].append(
        history_entry
    )


# ------------------------------------------------------------
# POLICY DECISION RECORD CREATION
# ------------------------------------------------------------

def create_policy_decision_record(policy_input):
    """
    Create a new Policy Decision record while preserving the
    original Alert Record and Triage Decision identities.

    Lab 17 creates a new PD identifier. It does not replace or
    modify the existing AR or TR identifiers.
    """

    policy_timestamp = create_utc_timestamp()

    policy_record = {
        # ----------------------------------------------------
        # POLICY IDENTITY
        # ----------------------------------------------------
        "policy_decision_id":
            create_policy_decision_id(),

        "policy_version":
            POLICY_VERSION,

        "policy_timestamp":
            policy_timestamp,

        # ----------------------------------------------------
        # SOURCE TRACEABILITY
        # ----------------------------------------------------
        "record_id":
            policy_input["record_id"],

        "triage_id":
            policy_input["triage_id"],

        "source_triage_classification":
            policy_input["triage_classification"],

        "source_triage_confidence":
            policy_input["triage_confidence"],

        "source_normalized_severity":
            policy_input["source_normalized_severity"],

        "source_next_stage":
            policy_input["next_stage"],

        "source_investigation_required":
            policy_input["investigation_required"],

        "source_human_review_required":
            policy_input["human_review_required"],

        "source_triage_rule_id":
            policy_input["triage_rule_id"],

        # ----------------------------------------------------
        # REQUEST
        # ----------------------------------------------------
        "requested_action":
            policy_input["requested_action"],

        "action_risk":
            None,

        # ----------------------------------------------------
        # POLICY RESULT
        # ----------------------------------------------------
        "policy_rule_id":
            None,

        "policy_outcome":
            None,

        "policy_reason":
            None,

        # ----------------------------------------------------
        # APPROVAL
        # ----------------------------------------------------
        "approval_required":
            False,

        "approval_id":
            None,

        "approval_status":
            None,

        # ----------------------------------------------------
        # FINAL WORKFLOW
        # ----------------------------------------------------
        "final_workflow_state":
            None,

        # ----------------------------------------------------
        # DOCUMENTATION
        # ----------------------------------------------------
        "decision_notes":
            [],

        "policy_history":
            [],
    }

    add_policy_history(
        policy_record,
        "Policy Record Created",
        (
            "A new Policy Decision record was created while "
            "preserving the original AR and TR identities."
        )
    )

    return policy_record


# ------------------------------------------------------------
# PUBLIC-SAFE ACTION CATALOG
# ------------------------------------------------------------

PUBLIC_ACTION_CATALOG = {
    "ADD_MONITORING_NOTE": {
        "risk": "LOW",
        "policy_behavior": "PRE_AUTHORIZED",
    },

    "TEMPORARY_BLOCK_SOURCE": {
        "risk": "MEDIUM",
        "policy_behavior": "REQUIRES_APPROVAL",
    },

    "DISABLE_USER_ACCOUNT": {
        "risk": "HIGH",
        "policy_behavior": "NOT_AUTHORIZED",
    },
}


# ------------------------------------------------------------
# POLICY DECISION ASSIGNMENT
# ------------------------------------------------------------

def apply_policy_decision(
    policy_record,
    rule_id,
    policy_outcome,
    policy_reason,
    approval_required,
    approval_status,
    final_workflow_state,
    action_risk="UNKNOWN",
    decision_note=None,
):
    """
    Apply one deterministic policy decision to a Policy
    Decision record.

    This function validates every frozen Lab 17 outcome before
    assigning it.

    It records authorization state only.
    It never executes the requested action.
    """

    if policy_outcome not in ALLOWED_POLICY_OUTCOMES:
        raise ValueError(
            f"Unsupported policy outcome: {policy_outcome}"
        )

    if approval_status not in ALLOWED_APPROVAL_STATUSES:
        raise ValueError(
            f"Unsupported approval status: {approval_status}"
        )

    if (
        final_workflow_state
        not in ALLOWED_FINAL_WORKFLOW_STATES
    ):
        raise ValueError(
            "Unsupported final workflow state: "
            f"{final_workflow_state}"
        )

    if not isinstance(approval_required, bool):
        raise ValueError(
            "approval_required must be True or False."
        )

    # --------------------------------------------------------
    # SAFETY CONSISTENCY CHECKS
    # --------------------------------------------------------

    if (
        approval_required
        and approval_status == "NOT_REQUIRED"
    ):
        raise ValueError(
            "An approval-required policy cannot use "
            "NOT_REQUIRED approval status."
        )

    if (
        not approval_required
        and approval_status
        in {"PENDING", "APPROVED", "DENIED"}
    ):
        raise ValueError(
            "A policy that does not require approval cannot "
            "contain a human approval state."
        )

    if (
        approval_required
        and approval_status != "APPROVED"
        and final_workflow_state == "READY_FOR_ACTION"
    ):
        raise ValueError(
            "An approval-required action cannot become "
            "READY_FOR_ACTION without explicit APPROVED state."
        )

    if (
        policy_outcome == "NOT_AUTHORIZED"
        and final_workflow_state == "READY_FOR_ACTION"
    ):
        raise ValueError(
            "A NOT_AUTHORIZED policy outcome cannot become "
            "READY_FOR_ACTION."
        )

    if (
        policy_outcome == "DEFERRED_TO_INVESTIGATION"
        and final_workflow_state != "INVESTIGATION"
    ):
        raise ValueError(
            "A deferred investigation outcome must remain "
            "in the INVESTIGATION workflow state."
        )

    # --------------------------------------------------------
    # ASSIGN POLICY RESULT
    # --------------------------------------------------------

    policy_record["action_risk"] = action_risk
    policy_record["policy_rule_id"] = rule_id
    policy_record["policy_outcome"] = policy_outcome
    policy_record["policy_reason"] = policy_reason
    policy_record["approval_required"] = approval_required
    policy_record["approval_status"] = approval_status
    policy_record[
        "final_workflow_state"
    ] = final_workflow_state

    if decision_note is not None:
        policy_record["decision_notes"].append(
            decision_note
        )

    add_policy_history(
        policy_record,
        "Policy Rule Matched",
        policy_reason,
        rule_id=rule_id,
    )

    add_policy_history(
        policy_record,
        "Final Workflow State Assigned",
        (
            "Final workflow state assigned as "
            f"{final_workflow_state}."
        ),
        rule_id=rule_id,
    )

    return policy_record


# ------------------------------------------------------------
# APPROVAL HISTORY HELPER
# ------------------------------------------------------------

def add_approval_history(
    approval_record,
    stage,
    details,
):
    """
    Add one chronological entry to an Approval Record.

    Approval history remains separate from Policy Decision
    history while preserving AR -> TR -> PD -> AP traceability.
    """

    approval_record["approval_history"].append(
        {
            "timestamp": create_utc_timestamp(),
            "stage": stage,
            "details": details,
        }
    )


# ------------------------------------------------------------
# APPROVAL RECORD CREATION
# ------------------------------------------------------------

def create_approval_record(
    policy_input,
    policy_record,
):
    """
    Create a separate Approval Record only when the matched
    policy requires explicit human approval.

    Lab 17 records approval state only.
    It does not execute the requested action.
    """

    if not policy_record["approval_required"]:
        raise ValueError(
            "Approval Record requested for a policy that "
            "does not require approval."
        )

    if (
        policy_record["policy_outcome"]
        != "REQUIRES_APPROVAL"
    ):
        raise ValueError(
            "Approval Records may only be created for "
            "REQUIRES_APPROVAL policy outcomes."
        )

    approval_status = policy_input.get(
        "controlled_approval_response",
        "PENDING",
    )

    if (
        approval_status
        not in ALLOWED_CONTROLLED_APPROVAL_RESPONSES
    ):
        raise ValueError(
            "Unsupported controlled approval response: "
            f"{approval_status}"
        )

    approval_id = create_approval_id()
    approval_timestamp = create_utc_timestamp()

    # Preserve the AP identity in the Policy Decision record
    # so the complete chain remains traceable.
    policy_record["approval_id"] = approval_id

    approval_record = {
        # ----------------------------------------------------
        # APPROVAL IDENTITY
        # ----------------------------------------------------
        "approval_id":
            approval_id,

        "approval_version":
            APPROVAL_VERSION,

        "approval_timestamp":
            approval_timestamp,

        # ----------------------------------------------------
        # TRACEABILITY
        # ----------------------------------------------------
        "record_id":
            policy_record["record_id"],

        "triage_id":
            policy_record["triage_id"],

        "policy_decision_id":
            policy_record["policy_decision_id"],

        # ----------------------------------------------------
        # REQUEST
        # ----------------------------------------------------
        "requested_action":
            policy_record["requested_action"],

        "action_risk":
            policy_record["action_risk"],

        # ----------------------------------------------------
        # APPROVAL STATE
        # ----------------------------------------------------
        "approval_status":
            approval_status,

        "reviewer_type":
            "CONTROLLED_HUMAN_REVIEWER",

        "approval_reason":
            None,

        # ----------------------------------------------------
        # DOCUMENTATION
        # ----------------------------------------------------
        "approval_history":
            [],
    }

    add_approval_history(
        approval_record,
        "Approval Record Created",
        (
            "A separate Approval Record was created because "
            "the matched policy requires explicit human "
            "approval."
        ),
    )

    # --------------------------------------------------------
    # RECORD THE CONTROLLED HUMAN RESPONSE
    # --------------------------------------------------------

    if approval_status == "APPROVED":
        approval_record["approval_reason"] = (
            "Controlled human approval explicitly granted "
            "for validation purposes."
        )

    elif approval_status == "DENIED":
        approval_record["approval_reason"] = (
            "Controlled human approval explicitly denied "
            "for validation purposes."
        )

    else:
        approval_record["approval_reason"] = (
            "Human approval remains pending."
        )

    add_approval_history(
        approval_record,
        "Approval State Recorded",
        (
            "Controlled approval state recorded as "
            f"{approval_status}."
        ),
    )

    add_approval_history(
        approval_record,
        "Final Approval State Confirmed",
        (
            "Approval processing completed with state "
            f"{approval_status}."
        ),
    )

    return approval_record


# ------------------------------------------------------------
# RULE 1 - INVESTIGATION LANE PROTECTION
# ------------------------------------------------------------

def apply_investigation_lane_rule(
    policy_input,
    policy_record,
):
    """
    Protect unresolved investigation cases from being pulled
    into an action workflow.

    The source workflow lane takes priority over the requested
    action.
    """

    if policy_input["next_stage"] != "INVESTIGATION":
        return False

    requested_action = policy_input["requested_action"]

    action_metadata = PUBLIC_ACTION_CATALOG.get(
        requested_action
    )

    action_risk = (
        action_metadata["risk"]
        if action_metadata is not None
        else "UNKNOWN"
    )

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-001",
        policy_outcome="DEFERRED_TO_INVESTIGATION",
        policy_reason=(
            "The source triage record remains in the "
            "INVESTIGATION lane. The requested action cannot "
            "override an unresolved investigation requirement."
        ),
        approval_required=False,
        approval_status="NOT_REQUIRED",
        final_workflow_state="INVESTIGATION",
        action_risk=action_risk,
        decision_note=(
            "Investigation-lane protection took priority over "
            "the requested action."
        ),
    )

    return True


# ------------------------------------------------------------
# RULE 2 - UNSUPPORTED ACTION DENIAL
# ------------------------------------------------------------

def apply_unsupported_action_rule(
    policy_input,
    policy_record,
):
    """
    Deny any requested action that does not exist in the
    public-safe supported-action catalog.

    Business Guardian must not improvise unsupported actions.
    """

    requested_action = policy_input["requested_action"]

    if requested_action in PUBLIC_ACTION_CATALOG:
        return False

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-002",
        policy_outcome="NOT_AUTHORIZED",
        policy_reason=(
            "The requested action is not present in the "
            "public-safe supported-action catalog."
        ),
        approval_required=False,
        approval_status="NOT_REQUIRED",
        final_workflow_state="NO_ACTION_AUTHORIZED",
        action_risk="UNKNOWN",
        decision_note=(
            "Unsupported actions fail closed and cannot become "
            "READY_FOR_ACTION."
        ),
    )

    return True


# ------------------------------------------------------------
# RULE 3 - PROHIBITED HIGH-RISK DEMONSTRATION ACTION
# ------------------------------------------------------------

def apply_prohibited_high_risk_rule(
    policy_input,
    policy_record,
):
    """
    Explicitly deny the controlled high-risk demonstration
    action.

    This public rule demonstrates that technical capability
    does not equal authorization.
    """

    requested_action = policy_input["requested_action"]

    if requested_action != "DISABLE_USER_ACCOUNT":
        return False

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-003",
        policy_outcome="NOT_AUTHORIZED",
        policy_reason=(
            "The public demonstration policy explicitly "
            "prohibits DISABLE_USER_ACCOUNT."
        ),
        approval_required=False,
        approval_status="NOT_REQUIRED",
        final_workflow_state="NO_ACTION_AUTHORIZED",
        action_risk="HIGH",
        decision_note=(
            "A consequential action may be technically "
            "possible while remaining unauthorized by policy."
        ),
    )

    return True


# ------------------------------------------------------------
# RULE 4 - PRE-AUTHORIZED LOW-RISK ACTION
# ------------------------------------------------------------

def apply_preauthorized_low_risk_rule(
    policy_input,
    policy_record,
):
    """
    Authorize the controlled low-risk demonstration action
    only when the source triage record is explicitly routed
    to POLICY_EVALUATION.

    Authorization is created by the deterministic policy,
    not by severity.
    """

    if policy_input["next_stage"] != "POLICY_EVALUATION":
        return False

    requested_action = policy_input["requested_action"]

    if requested_action != "ADD_MONITORING_NOTE":
        return False

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-004",
        policy_outcome="AUTHORIZED",
        policy_reason=(
            "ADD_MONITORING_NOTE is a supported low-risk "
            "action explicitly pre-authorized by the public "
            "demonstration policy."
        ),
        approval_required=False,
        approval_status="NOT_REQUIRED",
        final_workflow_state="READY_FOR_ACTION",
        action_risk="LOW",
        decision_note=(
            "Technical severity did not create authorization. "
            "The explicit deterministic policy did."
        ),
    )

    return True


# ------------------------------------------------------------
# RULE 5 - APPROVAL-REQUIRED MEDIUM-RISK ACTION
# ------------------------------------------------------------

def apply_approval_required_rule(
    policy_input,
    policy_record,
):
    """
    Require explicit human approval for the controlled
    TEMPORARY_BLOCK_SOURCE action.

    HIGH severity, a known classification, or the existence
    of a requested action cannot bypass this approval gate.
    """

    if policy_input["next_stage"] != "POLICY_EVALUATION":
        return False

    requested_action = policy_input["requested_action"]

    if requested_action != "TEMPORARY_BLOCK_SOURCE":
        return False

    approval_response = policy_input.get(
        "controlled_approval_response",
        "PENDING",
    )

    if approval_response == "APPROVED":
        approval_status = "APPROVED"
        final_workflow_state = "READY_FOR_ACTION"

        decision_note = (
            "Explicit controlled human approval satisfied "
            "the approval-required policy. No action was "
            "executed."
        )

    elif approval_response == "DENIED":
        approval_status = "DENIED"
        final_workflow_state = "NO_ACTION_AUTHORIZED"

        decision_note = (
            "Explicit controlled human denial prevented the "
            "requested action from becoming ready."
        )

    else:
        approval_status = "PENDING"
        final_workflow_state = "AWAITING_APPROVAL"

        decision_note = (
            "Human approval has not been granted. The "
            "requested action remains blocked."
        )

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-005",
        policy_outcome="REQUIRES_APPROVAL",
        policy_reason=(
            "TEMPORARY_BLOCK_SOURCE is a supported "
            "medium-risk action that requires explicit "
            "human approval under the public demonstration "
            "policy."
        ),
        approval_required=True,
        approval_status=approval_status,
        final_workflow_state=final_workflow_state,
        action_risk="MEDIUM",
        decision_note=decision_note,
    )

    return True


# ------------------------------------------------------------
# RULE 6 - SAFE POLICY FALLBACK
# ------------------------------------------------------------

def apply_safe_fallback_rule(
    policy_input,
    policy_record,
):
    """
    Fail closed when no earlier deterministic policy rule
    safely authorizes or routes the request.

    Unknown policy behavior must never become authorization.
    """

    requested_action = policy_input["requested_action"]

    action_metadata = PUBLIC_ACTION_CATALOG.get(
        requested_action
    )

    action_risk = (
        action_metadata["risk"]
        if action_metadata is not None
        else "UNKNOWN"
    )

    apply_policy_decision(
        policy_record=policy_record,
        rule_id="POLICY-RULE-006",
        policy_outcome="NOT_AUTHORIZED",
        policy_reason=(
            "No earlier deterministic policy rule safely "
            "authorized or routed the requested action."
        ),
        approval_required=False,
        approval_status="NOT_REQUIRED",
        final_workflow_state="NO_ACTION_AUTHORIZED",
        action_risk=action_risk,
        decision_note=(
            "The policy engine failed closed rather than "
            "inventing authorization."
        ),
    )

    return True


# ------------------------------------------------------------
# DETERMINISTIC POLICY EVALUATION
# ------------------------------------------------------------

def evaluate_policy_rules(
    policy_input,
    policy_record,
):
    """
    Evaluate Lab 17 policy rules in the frozen priority order.

    The first matching rule wins.

    Lower-priority rules must never override:
    - investigation-lane protection;
    - unsupported-action denial;
    - prohibited-action denial;
    - explicit approval requirements.
    """

    add_policy_history(
        policy_record,
        "Policy Evaluation Started",
        (
            "Deterministic Lab 17 policy evaluation began. "
            "No defensive action was executed."
        ),
    )

    # --------------------------------------------------------
    # PRIORITY 1 - INVESTIGATION LANE PROTECTION
    # --------------------------------------------------------

    if apply_investigation_lane_rule(
        policy_input,
        policy_record,
    ):
        return None

    # --------------------------------------------------------
    # PRIORITY 2 - UNSUPPORTED ACTION DENIAL
    # --------------------------------------------------------

    if apply_unsupported_action_rule(
        policy_input,
        policy_record,
    ):
        return None

    # --------------------------------------------------------
    # PRIORITY 3 - PROHIBITED HIGH-RISK ACTION
    # --------------------------------------------------------

    if apply_prohibited_high_risk_rule(
        policy_input,
        policy_record,
    ):
        return None

    # --------------------------------------------------------
    # PRIORITY 4 - PRE-AUTHORIZED LOW-RISK ACTION
    # --------------------------------------------------------

    if apply_preauthorized_low_risk_rule(
        policy_input,
        policy_record,
    ):
        return None

    # --------------------------------------------------------
    # PRIORITY 5 - APPROVAL-REQUIRED ACTION
    # --------------------------------------------------------

    if apply_approval_required_rule(
        policy_input,
        policy_record,
    ):
        approval_record = create_approval_record(
            policy_input,
            policy_record,
        )

        add_policy_history(
            policy_record,
            "Approval Requirement Assigned",
            (
                "A separate Approval Record was created "
                "because the matched policy requires "
                "explicit human approval."
            ),
            rule_id="POLICY-RULE-005",
        )

        return approval_record

    # --------------------------------------------------------
    # PRIORITY 6 - SAFE FALLBACK
    # --------------------------------------------------------

    apply_safe_fallback_rule(
        policy_input,
        policy_record,
    )

    return None


# ------------------------------------------------------------
# UNIQUE OUTPUT PATH HELPERS
# ------------------------------------------------------------

def create_unique_policy_output_path(
    source_filename,
    policy_decision_id,
):
    """
    Create a unique JSON output path for one Policy Decision
    record.

    The source filename and unique PD identifier provide
    traceability while preventing previous outputs from being
    overwritten.
    """

    source_stem = Path(source_filename).stem

    base_filename = (
        f"{source_stem}_{policy_decision_id}.json"
    )

    output_path = OUTPUT_FOLDER / base_filename

    counter = 2

    while output_path.exists():
        output_path = OUTPUT_FOLDER / (
            f"{source_stem}_{policy_decision_id}_{counter}.json"
        )
        counter += 1

    return output_path


def create_unique_approval_output_path(
    source_filename,
    approval_id,
):
    """
    Create a unique JSON output path for one Approval Record.

    Approval records remain separate from Policy Decision
    records and never overwrite an earlier approval record.
    """

    source_stem = Path(source_filename).stem

    base_filename = (
        f"{source_stem}_{approval_id}.json"
    )

    output_path = OUTPUT_FOLDER / base_filename

    counter = 2

    while output_path.exists():
        output_path = OUTPUT_FOLDER / (
            f"{source_stem}_{approval_id}_{counter}.json"
        )
        counter += 1

    return output_path


# ------------------------------------------------------------
# POLICY DECISION JSON WRITER
# ------------------------------------------------------------

def write_policy_decision_record(
    policy_record,
    source_filename,
):
    """
    Write one Policy Decision record as readable UTF-8 JSON.

    Writing the record does not execute or authorize any
    defensive action beyond the policy state already recorded.
    """

    add_policy_history(
        policy_record,
        "Policy Output Prepared",
        (
            "Policy Decision JSON output was prepared for "
            "audit and validation. No defensive action was "
            "executed."
        ),
        rule_id=policy_record["policy_rule_id"],
    )

    output_path = create_unique_policy_output_path(
        source_filename,
        policy_record["policy_decision_id"],
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(
            policy_record,
            output_file,
            indent=4,
            ensure_ascii=False,
        )

    return output_path


# ------------------------------------------------------------
# APPROVAL JSON WRITER
# ------------------------------------------------------------

def write_approval_record(
    approval_record,
    source_filename,
):
    """
    Write one Approval Record as readable UTF-8 JSON.

    Approval output records the controlled approval state only.
    It does not perform the requested defensive action.
    """

    output_path = create_unique_approval_output_path(
        source_filename,
        approval_record["approval_id"],
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(
            approval_record,
            output_file,
            indent=4,
            ensure_ascii=False,
        )

    return output_path


# ------------------------------------------------------------
# SINGLE-RECORD PROCESSING
# ------------------------------------------------------------

def process_single_policy_input(file_path):
    """
    Process one Lab 17 policy input from beginning to end.

    Workflow:
    1. Load JSON.
    2. Validate the Lab 16-style source record.
    3. Create a new Policy Decision record.
    4. Evaluate deterministic policy rules.
    5. Create an Approval Record when required.
    6. Write the generated JSON outputs.

    A failure in one record is returned to the batch processor
    so other valid inputs can still be attempted.
    """

    result = {
        "source_file": file_path.name,
        "processing_result": "FAILED",
        "record_id": None,
        "triage_id": None,
        "policy_record": None,
        "approval_record": None,
        "policy_path": None,
        "approval_path": None,
        "error": None,
    }

    try:
        # ----------------------------------------------------
        # LOAD AND VALIDATE SOURCE INPUT
        # ----------------------------------------------------

        policy_input = load_policy_input(file_path)

        validate_policy_input(
            policy_input,
            file_path.name,
        )

        result["record_id"] = policy_input["record_id"]
        result["triage_id"] = policy_input["triage_id"]

        # ----------------------------------------------------
        # CREATE POLICY DECISION RECORD
        # ----------------------------------------------------

        policy_record = create_policy_decision_record(
            policy_input
        )

        # ----------------------------------------------------
        # EVALUATE DETERMINISTIC POLICY RULES
        # ----------------------------------------------------

        approval_record = evaluate_policy_rules(
            policy_input,
            policy_record,
        )

        # ----------------------------------------------------
        # WRITE POLICY DECISION OUTPUT
        # ----------------------------------------------------

        policy_path = write_policy_decision_record(
            policy_record,
            file_path.name,
        )

        # ----------------------------------------------------
        # WRITE APPROVAL OUTPUT WHEN REQUIRED
        # ----------------------------------------------------

        approval_path = None

        if approval_record is not None:
            approval_path = write_approval_record(
                approval_record,
                file_path.name,
            )

        # ----------------------------------------------------
        # RETURN SUCCESSFUL RESULT
        # ----------------------------------------------------

        result["processing_result"] = "SUCCESS"
        result["policy_record"] = policy_record
        result["approval_record"] = approval_record
        result["policy_path"] = policy_path
        result["approval_path"] = approval_path

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        OSError,
    ) as error:
        result["error"] = str(error)

    return result


# ------------------------------------------------------------
# BATCH TOTAL CALCULATION
# ------------------------------------------------------------

def calculate_batch_totals(batch_results):
    """
    Calculate observed Lab 17 totals from actual processing
    results.

    These values are derived from generated records.
    They are not hard-coded to match the frozen validation
    targets.
    """

    totals = {
        "inputs_discovered": len(batch_results),

        "policy_outcomes": {
            "AUTHORIZED": 0,
            "REQUIRES_APPROVAL": 0,
            "DEFERRED_TO_INVESTIGATION": 0,
            "NOT_AUTHORIZED": 0,
        },

        "approval_records_created": 0,

        "approval_statuses": {
            "PENDING": 0,
            "APPROVED": 0,
            "DENIED": 0,
        },

        "final_workflow_states": {
            "READY_FOR_ACTION": 0,
            "AWAITING_APPROVAL": 0,
            "INVESTIGATION": 0,
            "NO_ACTION_AUTHORIZED": 0,
        },

        "policy_decision_records_created": 0,
        "failed": 0,
    }

    for result in batch_results:
        if result["processing_result"] != "SUCCESS":
            totals["failed"] += 1
            continue

        policy_record = result["policy_record"]

        policy_outcome = policy_record["policy_outcome"]

        if policy_outcome in totals["policy_outcomes"]:
            totals["policy_outcomes"][
                policy_outcome
            ] += 1

        final_workflow_state = policy_record[
            "final_workflow_state"
        ]

        if (
            final_workflow_state
            in totals["final_workflow_states"]
        ):
            totals["final_workflow_states"][
                final_workflow_state
            ] += 1

        totals["policy_decision_records_created"] += 1

        approval_record = result["approval_record"]

        if approval_record is not None:
            totals["approval_records_created"] += 1

            approval_status = approval_record[
                "approval_status"
            ]

            if (
                approval_status
                in totals["approval_statuses"]
            ):
                totals["approval_statuses"][
                    approval_status
                ] += 1

    return totals                                    


# ------------------------------------------------------------
# BATCH PROCESSING WORKFLOW
# ------------------------------------------------------------

def process_policy_batch():
    """
    Process every supported Lab 17 policy-input record.

    Each record is handled independently so one failed input
    does not prevent the remaining valid records from being
    attempted.

    Returns a batch-data dictionary containing:
    - processing timestamps;
    - per-record results;
    - observed totals.
    """

    validate_workspace()

    batch_started = create_utc_timestamp()

    policy_inputs = discover_policy_inputs()

    batch_results = []

    for file_path in policy_inputs:
        result = process_single_policy_input(
            file_path
        )

        batch_results.append(result)

    batch_completed = create_utc_timestamp()

    totals = calculate_batch_totals(
        batch_results
    )

    batch_data = {
        "batch_started":
            batch_started,

        "batch_completed":
            batch_completed,

        "results":
            batch_results,

        "totals":
            totals,
    }

    return batch_data


# ------------------------------------------------------------
# DISPLAY HELPER
# ------------------------------------------------------------

def display_value(value):
    """
    Convert values into clean human-readable text for the
    batch summary.
    """

    if value is None or value == "":
        return "Unavailable"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


# ------------------------------------------------------------
# PER-RECORD BATCH SUMMARY ENTRY
# ------------------------------------------------------------

def build_batch_result_entry(result):
    """
    Build one human-readable summary entry while preserving
    AR -> TR -> PD -> optional AP traceability.
    """

    lines = []

    lines.append(
        f"Source File: {result['source_file']}"
    )

    lines.append(
        f"Processing Result: "
        f"{result['processing_result']}"
    )

    lines.append(
        f"Alert Record ID: "
        f"{display_value(result['record_id'])}"
    )

    lines.append(
        f"Triage Decision ID: "
        f"{display_value(result['triage_id'])}"
    )

    if result["processing_result"] != "SUCCESS":
        lines.append(
            f"Error: {display_value(result['error'])}"
        )

        return "\n".join(lines)

    policy_record = result["policy_record"]

    lines.append(
        f"Policy Decision ID: "
        f"{policy_record['policy_decision_id']}"
    )

    lines.append(
        f"Requested Action: "
        f"{policy_record['requested_action']}"
    )

    lines.append(
        f"Action Risk: "
        f"{policy_record['action_risk']}"
    )

    lines.append(
        f"Policy Rule: "
        f"{policy_record['policy_rule_id']}"
    )

    lines.append(
        f"Policy Outcome: "
        f"{policy_record['policy_outcome']}"
    )

    lines.append(
        f"Approval Required: "
        f"{display_value(policy_record['approval_required'])}"
    )

    lines.append(
        f"Approval Status: "
        f"{policy_record['approval_status']}"
    )

    lines.append(
        f"Final Workflow State: "
        f"{policy_record['final_workflow_state']}"
    )

    approval_record = result["approval_record"]

    if approval_record is not None:
        lines.append(
            f"Approval Record ID: "
            f"{approval_record['approval_id']}"
        )
    else:
        lines.append(
            "Approval Record ID: Not Required"
        )

    return "\n".join(lines)


# ------------------------------------------------------------
# HUMAN-READABLE BATCH SUMMARY
# ------------------------------------------------------------

def build_batch_summary(batch_data):
    """
    Build the complete Lab 17 validation summary from actual
    observed processing results.
    """

    totals = batch_data["totals"]

    policy_outcomes = totals[
        "policy_outcomes"
    ]

    approval_statuses = totals[
        "approval_statuses"
    ]

    workflow_states = totals[
        "final_workflow_states"
    ]

    lines = []

    lines.append(
        "LAB 17 - POLICY EVALUATION AND APPROVAL LOGIC"
    )

    lines.append(
        "CONTROLLED BATCH SUMMARY"
    )

    lines.append("=" * 60)

    lines.append(
        f"Batch Started: "
        f"{batch_data['batch_started']}"
    )

    lines.append(
        f"Batch Completed: "
        f"{batch_data['batch_completed']}"
    )

    lines.append("")

    lines.append("OBSERVED TOTALS")
    lines.append("-" * 60)

    lines.append(
        f"Inputs Discovered: "
        f"{totals['inputs_discovered']}"
    )

    lines.append("")

    lines.append("Policy Outcomes:")

    lines.append(
        f"  AUTHORIZED: "
        f"{policy_outcomes['AUTHORIZED']}"
    )

    lines.append(
        f"  REQUIRES_APPROVAL: "
        f"{policy_outcomes['REQUIRES_APPROVAL']}"
    )

    lines.append(
        f"  DEFERRED_TO_INVESTIGATION: "
        f"{policy_outcomes['DEFERRED_TO_INVESTIGATION']}"
    )

    lines.append(
        f"  NOT_AUTHORIZED: "
        f"{policy_outcomes['NOT_AUTHORIZED']}"
    )

    lines.append("")

    lines.append(
        f"Approval Records Created: "
        f"{totals['approval_records_created']}"
    )

    lines.append("")

    lines.append("Approval Statuses:")

    lines.append(
        f"  PENDING: "
        f"{approval_statuses['PENDING']}"
    )

    lines.append(
        f"  APPROVED: "
        f"{approval_statuses['APPROVED']}"
    )

    lines.append(
        f"  DENIED: "
        f"{approval_statuses['DENIED']}"
    )

    lines.append("")

    lines.append("Final Workflow States:")

    lines.append(
        f"  READY_FOR_ACTION: "
        f"{workflow_states['READY_FOR_ACTION']}"
    )

    lines.append(
        f"  AWAITING_APPROVAL: "
        f"{workflow_states['AWAITING_APPROVAL']}"
    )

    lines.append(
        f"  INVESTIGATION: "
        f"{workflow_states['INVESTIGATION']}"
    )

    lines.append(
        f"  NO_ACTION_AUTHORIZED: "
        f"{workflow_states['NO_ACTION_AUTHORIZED']}"
    )

    lines.append("")

    lines.append(
        f"Policy Decision Records Created: "
        f"{totals['policy_decision_records_created']}"
    )

    lines.append(
        f"Failed: {totals['failed']}"
    )

    lines.append("")
    lines.append("=" * 60)

    lines.append(
        "PER-RECORD TRACEABILITY"
    )

    lines.append("=" * 60)

    for index, result in enumerate(
        batch_data["results"],
        start=1,
    ):
        lines.append("")
        lines.append(
            f"Record {index}"
        )

        lines.append("-" * 60)

        lines.append(
            build_batch_result_entry(result)
        )

    lines.append("")
    lines.append("=" * 60)

    lines.append("SAFETY STATEMENT")

    lines.append("-" * 60)

    lines.append(
        "Lab 17 evaluated policy and approval state only. "
        "No defensive action was executed."
    )

    return "\n".join(lines)


# ------------------------------------------------------------
# UNIQUE BATCH SUMMARY PATH
# ------------------------------------------------------------

def create_unique_batch_summary_path():
    """
    Create an overwrite-protected filename for one Lab 17
    batch summary.

    Each controlled run receives its own timestamped summary.
    """

    timestamp = create_filename_timestamp()

    output_path = OUTPUT_FOLDER / (
        f"batch_summary_{timestamp}.txt"
    )

    counter = 2

    while output_path.exists():
        output_path = OUTPUT_FOLDER / (
            f"batch_summary_{timestamp}_{counter}.txt"
        )
        counter += 1

    return output_path


# ------------------------------------------------------------
# BATCH SUMMARY WRITER
# ------------------------------------------------------------

def write_batch_summary(batch_data):
    """
    Write the human-readable Lab 17 batch summary without
    overwriting an earlier controlled run.
    """

    summary_text = build_batch_summary(
        batch_data
    )

    summary_path = create_unique_batch_summary_path()

    with summary_path.open(
        "w",
        encoding="utf-8",
    ) as summary_file:
        summary_file.write(summary_text)

    return summary_path


# ------------------------------------------------------------
# CONSOLE RESULTS DISPLAY
# ------------------------------------------------------------

def display_batch_results(
    batch_data,
    summary_path,
):
    """
    Display the observed Lab 17 batch results in the console.

    The values shown here come from actual generated records,
    not from the frozen expected-results document.
    """

    totals = batch_data["totals"]

    policy_outcomes = totals[
        "policy_outcomes"
    ]

    approval_statuses = totals[
        "approval_statuses"
    ]

    workflow_states = totals[
        "final_workflow_states"
    ]

    print()
    print(
        "Lab 17 policy evaluation and approval processing "
        "complete."
    )

    print()

    print(
        f"Policy inputs discovered: "
        f"{totals['inputs_discovered']}"
    )

    print()

    print("Policy Outcomes:")

    print(
        f"  AUTHORIZED: "
        f"{policy_outcomes['AUTHORIZED']}"
    )

    print(
        f"  REQUIRES_APPROVAL: "
        f"{policy_outcomes['REQUIRES_APPROVAL']}"
    )

    print(
        f"  DEFERRED_TO_INVESTIGATION: "
        f"{policy_outcomes['DEFERRED_TO_INVESTIGATION']}"
    )

    print(
        f"  NOT_AUTHORIZED: "
        f"{policy_outcomes['NOT_AUTHORIZED']}"
    )

    print()

    print(
        f"Approval records created: "
        f"{totals['approval_records_created']}"
    )

    print()

    print("Approval Statuses:")

    print(
        f"  PENDING: "
        f"{approval_statuses['PENDING']}"
    )

    print(
        f"  APPROVED: "
        f"{approval_statuses['APPROVED']}"
    )

    print(
        f"  DENIED: "
        f"{approval_statuses['DENIED']}"
    )

    print()

    print("Final Workflow States:")

    print(
        f"  READY_FOR_ACTION: "
        f"{workflow_states['READY_FOR_ACTION']}"
    )

    print(
        f"  AWAITING_APPROVAL: "
        f"{workflow_states['AWAITING_APPROVAL']}"
    )

    print(
        f"  INVESTIGATION: "
        f"{workflow_states['INVESTIGATION']}"
    )

    print(
        f"  NO_ACTION_AUTHORIZED: "
        f"{workflow_states['NO_ACTION_AUTHORIZED']}"
    )

    print()

    print(
        f"Policy Decision records created: "
        f"{totals['policy_decision_records_created']}"
    )

    print(
        f"Failed: "
        f"{totals['failed']}"
    )

    print()

    print(
        f"Batch summary: "
        f"{summary_path.name}"
    )

    print()

    print(
        "Safety: Lab 17 evaluated policy and approval state "
        "only. No defensive action was executed."
    )


# ------------------------------------------------------------
# PROGRAM ENTRY POINT
# ------------------------------------------------------------

def main():
    """
    Run one controlled Lab 17 batch.

    Lab 17 evaluates policy and approval state only.
    It does not execute defensive actions.
    """

    try:
        batch_data = process_policy_batch()

        summary_path = write_batch_summary(
            batch_data
        )

        display_batch_results(
            batch_data,
            summary_path,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        OSError,
    ) as error:
        print()
        print(
            "Lab 17 processing could not start or complete."
        )

        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()            