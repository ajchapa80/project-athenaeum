from pathlib import Path


EXPECTED_FIELDS = [
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
]


def load_alert_sample(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Input file was not found: {file_path.name}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {file_path.name}")

    alert_data = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key in EXPECTED_FIELDS:
                alert_data[key] = value

    if not alert_data:
        raise ValueError("No expected alert fields were found in the input file.")

    return alert_data


def explain_severity(rule_level):
    try:
        level = int(rule_level)
    except ValueError:
        return "The Wazuh rule level could not be read, so the severity needs manual review."

    if level >= 10:
        return "This is a high-severity alert and should be reviewed quickly."
    elif level >= 7:
        return "This is a notable alert that should be reviewed by an analyst."
    elif level >= 4:
        return "This is a medium-level alert that may require review depending on context."
    else:
        return "This is a low-level alert and may be normal system activity."


def build_alert_explanation(alert_data):
    agent_name = alert_data.get("agent.name", "Unknown endpoint")
    agent_ip = alert_data.get("agent.ip", "Unknown IP address")
    manager_name = alert_data.get("manager.name", "Unknown Wazuh manager")
    event_id = alert_data.get("data.win.system.eventID", "Unknown event ID")
    provider_name = alert_data.get("data.win.system.providerName", "Unknown provider")
    severity_value = alert_data.get("data.win.system.severityValue", "Unknown Windows severity")
    message = alert_data.get("data.win.system.message", "No event message available")
    rule_description = alert_data.get("rule.description", "No Wazuh rule description available")
    rule_id = alert_data.get("rule.id", "Unknown rule ID")
    rule_level = alert_data.get("rule.level", "Unknown rule level")
    rule_groups = alert_data.get("rule.groups", "No rule groups available")
    decoder_name = alert_data.get("decoder.name", "Unknown decoder")
    location = alert_data.get("location", "Unknown location")

    severity_explanation = explain_severity(rule_level)

    explanation = f"""
AI Alert Explainer MVP Report

Alert Summary:
The monitored Windows workstation {agent_name} generated an event that was collected by {manager_name}. The endpoint IP address was {agent_ip}. Wazuh classified the event as: {rule_description}

Windows Event Context:
The Windows event ID was {event_id}. The event came from provider {provider_name} and had a Windows severity value of {severity_value}. The event message was: {message}

Wazuh Rule Context:
Wazuh matched this activity to rule ID {rule_id} with rule level {rule_level}. The rule groups were: {rule_groups}. The event was decoded using {decoder_name} from location {location}.

Severity Explanation:
{severity_explanation}

Analyst Context:
In this lab, the event was intentionally created as a safe simulation for alert review and AI data collection practice. No malicious activity is indicated in this controlled lab context.

Recommended Review Steps:
1. Confirm whether the event was expected or unexpected.
2. Check whether the same event repeats over time.
3. Review the provider, event ID, and endpoint involved.
4. Look for related alerts before deciding whether escalation is needed.

Final Assessment:
This alert is benign in the Lab 11 environment because it came from a controlled test event. In a real environment, the alert would need additional context before being closed or escalated.
"""

    return explanation.strip()


def main():
    lab_folder = Path(__file__).parent
    input_file = lab_folder / "Lab11_AI_Data_Sample_01_Windows_Application_Error_Event.txt"
    output_file = lab_folder / "Lab11_Alert_Explanation_Output.txt"

    try:
        alert_data = load_alert_sample(input_file)
        explanation = build_alert_explanation(alert_data)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(explanation)

        print("AI Alert Explainer MVP completed successfully.")
        print(f"Input file: {input_file.name}")
        print(f"Output file: {output_file.name}")

    except Exception as error:
        print("AI Alert Explainer MVP did not complete.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()