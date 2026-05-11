import gzip
import json
from pathlib import Path

from mythic_edge_parser.app import card_catalog as card_catalog_module
from mythic_edge_parser.app.card_catalog import (
    CatalogSyncResult,
    build_catalog_from_bulk_file,
    ensure_grp_id_overrides_file,
    is_relevant_card,
    iter_bulk_cards,
    load_combined_card_lookup,
    load_grp_id_overrides,
    maybe_sync_card_catalog,
    parse_wotc_standard_set_names,
    reduce_card,
    retain_latest_raw_source,
    source_stamp_from_bulk_item,
    write_catalog_outputs,
)


def test_iter_bulk_cards_streams_json_array(tmp_path: Path) -> None:
    bulk_path = tmp_path / "bulk.json"
    bulk_path.write_text(
        json.dumps(
            [
                {"name": "Card A", "arena_id": 1},
                {"name": "Card B", "arena_id": 2},
            ]
        ),
        encoding="utf-8",
    )

    cards = list(iter_bulk_cards(bulk_path))

    assert [card["name"] for card in cards] == ["Card A", "Card B"]


def test_is_relevant_card_requires_format_legality_and_arena_id() -> None:
    card = {
        "legalities": {"standard": "legal", "modern": "not_legal"},
        "arena_id": 93940,
        "games": ["paper", "arena"],
    }

    assert is_relevant_card(card, "standard") is True
    assert is_relevant_card(card, "modern") is False

    card["arena_id"] = None
    assert is_relevant_card(card, "standard") is False


def test_is_relevant_card_can_keep_any_arena_card_without_legality_filter() -> None:
    card = {
        "legalities": {"standard": "not_legal", "historic": "legal"},
        "arena_id": 12345,
        "games": ["arena"],
    }

    assert is_relevant_card(card, "arena") is True
    assert is_relevant_card(card, "all") is True


def test_reduce_card_keeps_arena_relevant_fields_only() -> None:
    card = {
        "arena_id": 93940,
        "oracle_id": "oracle-1",
        "id": "scryfall-1",
        "name": "Llanowar Elves",
        "rarity": "common",
        "set": "fdn",
        "set_name": "Foundations",
        "collector_number": "227",
        "released_at": "2024-11-15",
        "layout": "normal",
        "mana_cost": "{G}",
        "cmc": 1,
        "type_line": "Creature — Elf Druid",
        "oracle_text": "{T}: Add {G}.",
        "colors": ["G"],
        "color_identity": ["G"],
        "keywords": [],
        "produced_mana": ["G"],
        "games": ["arena", "paper"],
        "artist": "Someone We Do Not Need",
        "card_faces": [
            {
                "name": "Front Face",
                "mana_cost": "{1}{G}",
                "type_line": "Creature",
                "oracle_text": "Text",
                "colors": ["G"],
                "artist": "Ignored",
            }
        ],
    }

    reduced = reduce_card(card)

    assert reduced["arena_id"] == 93940
    assert reduced["name"] == "Llanowar Elves"
    assert reduced["rarity"] == "common"
    assert reduced["games"] == ["arena", "paper"]
    assert "artist" not in reduced
    assert reduced["parser_fingerprint"]["colors"] == ["Green"]
    assert reduced["parser_fingerprint"]["card_types"] == ["Creature"]
    assert reduced["parser_fingerprint"]["subtypes"] == ["Druid", "Elf"]
    assert reduced["parser_fingerprint"]["produced_mana"] == ["Green"]
    assert reduced["parser_fingerprint"]["face_names"] == ["Front Face"]
    assert reduced["parser_fingerprint"]["games"] == ["arena", "paper"]
    assert reduced["card_faces"] == [
        {
            "name": "Front Face",
            "mana_cost": "{1}{G}",
            "type_line": "Creature",
            "oracle_text": "Text",
            "colors": ["G"],
            "parser_fingerprint": {
                "name": "Front Face",
                "layout": "",
                "face_names": [],
                "games": [],
                "mana_cost": "{1}{G}",
                "mana_cost_signature": "1xGreen + 1xColorless",
                "cmc": None,
                "type_line": "Creature",
                "super_types": [],
                "card_types": ["Creature"],
                "subtypes": [],
                "colors": ["Green"],
                "color_identity": [],
                "color_indicator": [],
                "keywords": [],
                "oracle_text": "Text",
                "power": "",
                "toughness": "",
                "loyalty": "",
                "defense": "",
                "produced_mana": [],
            },
        }
    ]


def test_build_catalog_from_bulk_file_filters_and_indexes_cards(tmp_path: Path) -> None:
    bulk_path = tmp_path / "bulk.json"
    bulk_path.write_text(
        json.dumps(
            [
                {
                    "arena_id": 93940,
                    "oracle_id": "oracle-1",
                    "id": "scryfall-1",
                    "name": "Llanowar Elves",
                    "rarity": "common",
                    "set": "fdn",
                    "set_name": "Foundations",
                    "collector_number": "227",
                    "released_at": "2024-11-15",
                    "layout": "normal",
                    "mana_cost": "{G}",
                    "cmc": 1,
                    "type_line": "Creature",
                    "oracle_text": "{T}: Add {G}.",
                    "colors": ["G"],
                    "color_identity": ["G"],
                    "keywords": [],
                    "produced_mana": ["G"],
                    "games": ["arena", "paper"],
                    "legalities": {"standard": "legal"},
                },
                {
                    "arena_id": None,
                    "name": "Paper Only Card",
                    "games": ["paper"],
                    "legalities": {"standard": "legal"},
                },
            ]
        ),
        encoding="utf-8",
    )

    catalog = build_catalog_from_bulk_file(
        bulk_path=bulk_path,
        format_key="standard",
        bulk_item={
            "type": "default_cards",
            "updated_at": "2026-04-20T21:11:02.475+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260420211102.json",
        },
    )

    assert catalog["format"] == "standard"
    assert catalog["bulk_type"] == "default_cards"
    assert catalog["total_cards"] == 1
    assert catalog["cards"][0]["name"] == "Llanowar Elves"
    assert catalog["cards"][0]["rarity"] == "common"
    assert catalog["cards_by_arena_id"]["93940"]["name"] == "Llanowar Elves"


def test_retain_latest_raw_source_writes_gzip_copy(tmp_path: Path) -> None:
    bulk_path = tmp_path / "bulk.json"
    bulk_path.write_text('[{"name":"Forest","arena_id":1}]', encoding="utf-8")

    retained = retain_latest_raw_source(
        bulk_path=bulk_path,
        bulk_type="default_cards",
        output_dir=tmp_path,
    )

    assert retained.name == "scryfall-default_cards-latest-source.json.gz"
    with gzip.open(retained, "rt", encoding="utf-8") as handle:
        assert handle.read() == '[{"name":"Forest","arena_id":1}]'


def test_write_catalog_outputs_prunes_dated_artifacts_and_keeps_latest_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    raw_source_path = output_dir / "scryfall-default_cards-latest-source.json.gz"
    raw_source_path.write_bytes(b"placeholder")

    (output_dir / "scryfall-default_cards-arena-20260101010101.json").write_text("{}", encoding="utf-8")
    (output_dir / "scryfall-default_cards-arena-20260101010101-arena-lookup.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (output_dir / "scryfall-default_cards-arena-20260101010101.csv").write_text("", encoding="utf-8")

    catalog = {
        "object": "manasight_card_catalog",
        "generated_at": "2026-05-08T12:00:00+00:00",
        "format": "arena",
        "bulk_type": "default_cards",
        "bulk_updated_at": "2026-05-08T09:02:43.122+00:00",
        "source_download_url": "https://data.scryfall.io/default-cards/default-cards-20260508090243.json",
        "total_cards": 1,
        "cards": [
            {
                "arena_id": 1,
                "oracle_id": "o1",
                "scryfall_id": "s1",
                "name": "Forest",
                "rarity": "common",
                "set": "fdn",
                "set_name": "Foundations",
                "collector_number": "281",
                "released_at": "2024-11-15",
                "layout": "normal",
                "mana_cost": "",
                "cmc": 0,
                "type_line": "Basic Land - Forest",
                "oracle_text": "({T}: Add {G}.)",
                "colors": [],
                "color_identity": ["G"],
                "keywords": [],
                "produced_mana": ["G"],
                "games": ["arena"],
                "card_faces": [],
            }
        ],
        "cards_by_arena_id": {
            "1": {"name": "Forest"}
        },
    }

    result = write_catalog_outputs(
        catalog,
        output_dir,
        raw_source_path=raw_source_path,
    )

    assert result.catalog_json_path.name == "scryfall-default_cards-arena-latest.json"
    assert result.arena_lookup_json_path.name == "scryfall-default_cards-arena-latest-arena-lookup.json"
    assert result.csv_path.name == "scryfall-default_cards-arena-latest.csv"
    assert not (output_dir / "scryfall-default_cards-arena-20260101010101.json").exists()
    assert not (output_dir / "scryfall-default_cards-arena-20260101010101-arena-lookup.json").exists()
    assert not (output_dir / "scryfall-default_cards-arena-20260101010101.csv").exists()


def test_load_grp_id_overrides_ignores_blank_entries(tmp_path: Path) -> None:
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "96185": {"name": "Swamp"},
                    "100574": {"name": ""},
                }
            }
        ),
        encoding="utf-8",
    )

    overrides = load_grp_id_overrides(path=override_path)

    assert overrides == {"96185": {"name": "Swamp"}}


def test_load_combined_card_lookup_prefers_grp_id_overrides(tmp_path: Path) -> None:
    lookup_path = tmp_path / "scryfall-default_cards-standard-latest-arena-lookup.json"
    lookup_path.write_text(
        json.dumps(
            {
                "cards_by_arena_id": {
                    "96185": {"name": "Unknown Swamp"},
                    "93940": {"name": "Llanowar Elves"},
                }
            }
        ),
        encoding="utf-8",
    )
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "96185": {"name": "Swamp", "notes": "manual override"},
                }
            }
        ),
        encoding="utf-8",
    )

    combined = load_combined_card_lookup(
        grp_id_override_path=override_path,
        arena_lookup_path=lookup_path,
    )

    assert combined["96185"]["name"] == "Swamp"
    assert combined["93940"]["name"] == "Llanowar Elves"


def test_ensure_grp_id_overrides_file_creates_empty_template(tmp_path: Path) -> None:
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"

    created = ensure_grp_id_overrides_file(path=override_path)

    payload = json.loads(created.read_text(encoding="utf-8"))
    assert created == override_path
    assert payload["object"] == "manasight_grp_id_overrides"
    assert payload["cards_by_grp_id"] == {}


def test_source_stamp_from_bulk_item_uses_bulk_updated_at() -> None:
    bulk_item = {
        "updated_at": "2026-04-20T21:11:02.475+00:00",
        "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260420211102.json",
    }

    assert source_stamp_from_bulk_item(bulk_item) == "20260420211102"


def test_parse_wotc_standard_set_names_extracts_sets_from_format_page() -> None:
    html_text = """
    <html>
      <body>
        <script>ignore_me()</script>
        <h2>What Sets Are Legal in Standard?</h2>
        <ul>
          <li>Magic: The Gathering Foundations</li>
          <li>Aetherdrift</li>
          <li>Tarkir: Dragonstorm</li>
        </ul>
        <h2>Different Ways to Play</h2>
      </body>
    </html>
    """

    assert parse_wotc_standard_set_names(html_text) == [
        "Magic: The Gathering Foundations",
        "Aetherdrift",
        "Tarkir: Dragonstorm",
    ]


class _DummySession:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}

    def close(self) -> None:
        return None


def test_maybe_sync_card_catalog_skips_when_source_stamp_is_unchanged(tmp_path: Path, monkeypatch) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    (output_dir / "scryfall-default_cards-standard-latest-arena-lookup.json").write_text(
        json.dumps({"cards_by_arena_id": {}}),
        encoding="utf-8",
    )
    (output_dir / "card-catalog-sync-state.json").write_text(
        json.dumps(
            {
                "last_synced_source_stamp": "20260420211102",
                "last_synced_wotc_standard_sets": ["Foundations", "Aetherdrift"],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(card_catalog_module.requests, "Session", _DummySession)
    monkeypatch.setattr(
        card_catalog_module,
        "fetch_wotc_standard_set_names",
        lambda session: ["Foundations", "Aetherdrift"],
    )
    monkeypatch.setattr(
        card_catalog_module,
        "get_bulk_item",
        lambda session, bulk_type: {
            "type": "default_cards",
            "updated_at": "2026-04-20T21:11:02.475+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260420211102.json",
        },
    )
    monkeypatch.setattr(
        card_catalog_module,
        "sync_card_catalog",
        lambda **kwargs: (_ for _ in ()).throw(AssertionError("sync_card_catalog should not be called")),
    )

    decision = maybe_sync_card_catalog(output_dir=output_dir, format_key="standard")

    assert decision.synced is False
    assert decision.reason == "Scryfall bulk source stamp is unchanged"
    assert decision.state_path.name == "card-catalog-sync-state-default_cards-standard.json"


def test_maybe_sync_card_catalog_waits_for_wotc_standard_change_before_syncing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    latest_lookup = output_dir / "scryfall-default_cards-standard-latest-arena-lookup.json"
    latest_lookup.write_text(json.dumps({"cards_by_arena_id": {}}), encoding="utf-8")
    (output_dir / "card-catalog-sync-state.json").write_text(
        json.dumps(
            {
                "last_synced_source_stamp": "20260301010101",
                "last_synced_wotc_standard_sets": ["Foundations", "Aetherdrift"],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(card_catalog_module.requests, "Session", _DummySession)
    monkeypatch.setattr(
        card_catalog_module,
        "fetch_wotc_standard_set_names",
        lambda session: ["Foundations", "Aetherdrift", "Tarkir: Dragonstorm"],
    )
    monkeypatch.setattr(
        card_catalog_module,
        "get_bulk_item",
        lambda session, bulk_type: {
            "type": "default_cards",
            "updated_at": "2026-04-20T21:11:02.475+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260420211102.json",
        },
    )

    def _fake_sync_card_catalog(**kwargs) -> CatalogSyncResult:
        return CatalogSyncResult(
            format_key="standard",
            bulk_type="default_cards",
            source_download_url="https://data.scryfall.io/default-cards/default-cards-20260420211102.json",
            bulk_file_path=output_dir / "_downloads" / "default-cards-20260420211102.json",
            catalog_json_path=output_dir / "scryfall-default_cards-standard-latest.json",
            arena_lookup_json_path=latest_lookup,
            csv_path=output_dir / "scryfall-default_cards-standard-latest.csv",
            total_cards=4321,
            generated_at="2026-04-27T12:00:00+00:00",
        )

    monkeypatch.setattr(card_catalog_module, "sync_card_catalog", _fake_sync_card_catalog)

    decision = maybe_sync_card_catalog(output_dir=output_dir, format_key="standard")

    assert decision.synced is True
    assert decision.reason == "Scryfall bulk source changed after the live WotC Standard set list changed"
    state_payload = json.loads(decision.state_path.read_text(encoding="utf-8"))
    assert state_payload["last_synced_source_stamp"] == "20260420211102"
    assert state_payload["last_synced_wotc_standard_sets"] == [
        "Foundations",
        "Aetherdrift",
        "Tarkir: Dragonstorm",
    ]
