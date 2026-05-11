from __future__ import annotations

from dataclasses import dataclass

MATCH_LOG_SYNC_FIELDS: tuple[str, ...] = (
    "Date",
    "My Rank",
    "G1 Play / Draw",
    "Game 1 Result",
    "G2 Play / Draw",
    "Game 2 Result",
    "G3 Play / Draw",
    "Game 3 Result",
    "Games Won",
    "Games Lost",
    "Match Win?",
    "Total Games",
    "Match Win Flag",
    "Game Win %",
    "MTGA Match ID",
    "MTGA Format",
    "MTGA Event ID",
    "MTGA Queue Type",
    "G1 Mulligans",
    "G2 Mulligans",
    "G3 Mulligans",
    "G1 Turn Count",
    "G2 Turn Count",
    "G3 Turn Count",
    "MGTA Start Time",
    "MTGA End Time",
    "MTGA Rank Raw",
    "MTGA Mulligans",
    "MTGA Sideboard Entered",
    "MTGA Submit Deck Seen",
    "MTGA Sync Status",
)


GAME_LOG_SYNC_FIELDS: tuple[str, ...] = (
    "Date",
    "MTGA Format",
    "My Rank",
    "MTGA Match ID",
    "Game Number",
    "Pre / Postboard",
    "Play / Draw",
    "Mulligans",
    "Opening Hand Size",
    "Opening Hand",
    "Mulliganed Away",
    "Game Result",
    "Turn Count",
    "Game Duration",
    "MTGA Event ID",
    "MTGA Queue Type",
)


ACTION_LOG_HEADERS: tuple[str, ...] = (
    "Generated At",
    "MTGA Match ID",
    "Game Number",
    "Turn Number",
    "Timestamp",
    "Action Type",
    "Cast Mode",
    "grpId",
    "Card Name",
    "Display Name",
    "Resolution Status",
    "Actor",
    "From Zone",
    "To Zone",
    "Summary",
)


DECK_SNAPSHOT_HEADERS: tuple[str, ...] = (
    "Generated At",
    "Submitted At",
    "MTGA Match ID",
    "Deck Signature",
    "Deck Name",
    "Deck Match Mode",
    "Deck Format",
    "Section",
    "Arena ID",
    "Count",
    "Card Name",
    "Rarity",
    "Set",
    "Type Line",
    "Colors",
    "Owned Copies",
    "Missing Copies",
)


COLLECTION_SNAPSHOT_HEADERS: tuple[str, ...] = (
    "Generated At",
    "Collection Available",
    "Inventory Available",
    "Owned Unique Cards",
    "Owned Total Card Copies",
    "Owned By Rarity",
    "Inventory Gold",
    "Inventory Gems",
    "Wildcards Common",
    "Wildcards Uncommon",
    "Wildcards Rare",
    "Wildcards Mythic",
    "Active Deck Missing By Rarity",
    "Active Deck Completion Rate",
    "Wanted Cards",
)


PARSER_STATUS_HEADERS: tuple[str, ...] = (
    "Updated At",
    "Status",
    "Current Match ID",
    "Current Game Number",
    "Current Player Team",
    "Last Event Kind",
    "Last Event At",
    "Webhook Successes",
    "Webhook Failures",
    "Event Failures",
    "Router Failures",
    "Active Deck Signature",
    "Active Deck Name",
    "Active Match Action Count",
)


CARD_PERFORMANCE_HEADERS: tuple[str, ...] = (
    "Generated At",
    "Card Key",
    "grpId",
    "Card Name",
    "Display Name",
    "Resolution Status",
    "Layout",
    "Card Faces",
    "Games Seen",
    "Seen In Game",
    "Seen Win Rate",
    "Opening Hand Games",
    "Opening Hand Win Rate",
    "Cast Games",
    "Cast Win Rate",
    "Postboard Cast Games",
    "Postboard Cast Win Rate",
    "Mulliganed Away Games",
    "Mulligan Tax",
    "Top Matchups",
    "Top Packages",
)


@dataclass(frozen=True, slots=True)
class RuntimeSheetSpec:
    family: str
    event_type: str
    scope: str
    headers: tuple[str, ...]


ACTION_LOG_FAMILY = "ActionLogRow"
DECK_SNAPSHOT_FAMILY = "DeckSnapshotRow"
COLLECTION_SNAPSHOT_FAMILY = "CollectionSnapshotRow"
PARSER_STATUS_FAMILY = "ParserStatusRow"
CARD_PERFORMANCE_FAMILY = "CardPerformanceRow"


RUNTIME_SHEET_SPECS: dict[str, RuntimeSheetSpec] = {
    ACTION_LOG_FAMILY: RuntimeSheetSpec(
        family=ACTION_LOG_FAMILY,
        event_type="action_log_row",
        scope="Match",
        headers=ACTION_LOG_HEADERS,
    ),
    DECK_SNAPSHOT_FAMILY: RuntimeSheetSpec(
        family=DECK_SNAPSHOT_FAMILY,
        event_type="deck_snapshot_row",
        scope="Deck",
        headers=DECK_SNAPSHOT_HEADERS,
    ),
    COLLECTION_SNAPSHOT_FAMILY: RuntimeSheetSpec(
        family=COLLECTION_SNAPSHOT_FAMILY,
        event_type="collection_snapshot_row",
        scope="Collection",
        headers=COLLECTION_SNAPSHOT_HEADERS,
    ),
    PARSER_STATUS_FAMILY: RuntimeSheetSpec(
        family=PARSER_STATUS_FAMILY,
        event_type="parser_status_row",
        scope="Runtime",
        headers=PARSER_STATUS_HEADERS,
    ),
    CARD_PERFORMANCE_FAMILY: RuntimeSheetSpec(
        family=CARD_PERFORMANCE_FAMILY,
        event_type="card_performance_row",
        scope="Card",
        headers=CARD_PERFORMANCE_HEADERS,
    ),
}


SYNC_FIELDS_BY_ROW_KIND: dict[str, tuple[str, ...]] = {
    "match_log": MATCH_LOG_SYNC_FIELDS,
    "game_log": GAME_LOG_SYNC_FIELDS,
}


def runtime_sheet_spec(event_family: str) -> RuntimeSheetSpec:
    return RUNTIME_SHEET_SPECS[event_family]


def runtime_sheet_headers(event_family: str) -> tuple[str, ...]:
    return runtime_sheet_spec(event_family).headers


def sync_fields(row_kind: str) -> tuple[str, ...]:
    return SYNC_FIELDS_BY_ROW_KIND[row_kind]
