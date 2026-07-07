from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "event_bus_queue_pressure_metrics.v1"
CONSUMER_CLASSIFICATION_SOURCE = "event_bus_consumer_delivery_classification.v1"
NON_CLAIMS = (
    "not_runtime_reliability_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_readiness",
    "not_parser_truth",
    "not_delivery_policy_authorization",
    "not_consumer_classification_change",
    "not_workbook_truth",
    "not_webhook_truth",
    "not_api_contract",
    "not_ci_gate",
    "not_security_assurance",
    "not_privacy_assurance",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
)

_CONSUMER_CLASSIFICATIONS = {
    "parser_runner_main_loop": ("truth_critical", "classified"),
    "local_app_live_capture_supervisor": ("mixed", "classified"),
    "mtga_event_stream_start": ("publisher_or_factory", "publisher_or_factory"),
    "event_bus_test_subscriber": ("test_fixture_only", "test_fixture_only"),
    "unknown_subscriber": ("unknown", "classification_required"),
}


@dataclass(slots=True)
class SubscriberMetrics:
    subscriber_ref: str
    consumer_id: str
    consumer_class: str
    classification_status: str
    max_queue_depth: int = 0
    publish_wait_count: int = 0


def consumer_metadata(consumer_id: str) -> tuple[str, str, str]:
    if not isinstance(consumer_id, str):
        return "unknown_subscriber", "unknown", "classification_unknown_fail_closed"
    metadata = _CONSUMER_CLASSIFICATIONS.get(consumer_id)
    if metadata is None:
        return "unknown_subscriber", "unknown", "classification_unknown_fail_closed"
    consumer_class, classification_status = metadata
    return consumer_id, consumer_class, classification_status


def wait_bucket(publish_wait_count: int, max_wait_seconds: float) -> str:
    if publish_wait_count <= 0:
        return "wait_none"
    if max_wait_seconds <= 0.05:
        return "wait_observed_short"
    if max_wait_seconds <= 1.0:
        return "wait_observed_moderate"
    return "wait_observed_long"


def event_rate_bucket(publish_calls: int, elapsed_seconds: float) -> str:
    if publish_calls <= 0:
        return "rate_not_observed"
    if elapsed_seconds <= 0:
        return "rate_unknown"
    events_per_second = publish_calls / elapsed_seconds
    if events_per_second < 1:
        return "rate_low"
    if events_per_second < 10:
        return "rate_moderate"
    if events_per_second < 100:
        return "rate_high"
    return "rate_burst"
