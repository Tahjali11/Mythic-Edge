import live_print_filtered_v11_match_summary as legacy_entrypoint
import main as modular_entrypoint


def test_legacy_entrypoint_delegates_to_modular_main() -> None:
    assert legacy_entrypoint.run_parser is modular_entrypoint.run_parser
