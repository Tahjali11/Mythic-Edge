from mythic_edge_parser.app.tier_sync import (
    _scrape_mtggoldfish,
    _scrape_mtgtop8,
    _scrape_untapped,
    classify_tier_bucket,
    normalize_archetype_name,
)


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


class _FakeSession:
    def __init__(self, html: str) -> None:
        self.html = html

    def get(self, url: str, **kwargs) -> _FakeResponse:
        return _FakeResponse(self.html)


def test_classify_tier_bucket_supports_percent_thresholds() -> None:
    assert classify_tier_bucket(5.0, "") == "Tier 1"
    assert classify_tier_bucket(2.5, "") == "Tier 2"
    assert classify_tier_bucket(1.2, "") == "Tier 3"
    assert classify_tier_bucket(0.8, "") == "Fringe"


def test_classify_tier_bucket_supports_letter_tiers() -> None:
    assert classify_tier_bucket(None, "A") == "Tier 1"
    assert classify_tier_bucket(None, "B") == "Tier 2"
    assert classify_tier_bucket(None, "C") == "Tier 3"
    assert classify_tier_bucket(None, "D") == "Fringe"


def test_normalize_archetype_name_uses_source_specific_override() -> None:
    overrides = {
        "global": {"uw control": "Azorius Control"},
        "mtggoldfish": {"ur aggro": "Izzet Prowess"},
        "mtgtop8": {},
        "untapped": {},
    }

    assert normalize_archetype_name("mtggoldfish", "UR Aggro", overrides) == "Izzet Prowess"
    assert normalize_archetype_name("mtgtop8", "UW Control", overrides) == "Azorius Control"
    assert normalize_archetype_name("mtgtop8", "Golgari Midrange", overrides) == "Golgari Midrange"


def test_scrape_mtggoldfish_extracts_archetypes_and_meta_share() -> None:
    html = """
    <div class="archetype-tile">
      <div class="archetype-tile-title">
        <span class="deck-price-paper"><a href="/archetype/standard-izzet-prowess">Izzet Prowess</a></span>
      </div>
      <div class="archetype-tile-statistic metagame-percentage">
        <div class="archetype-tile-statistic-value">17.7% <span>(299)</span></div>
      </div>
    </div>
    """

    rows = _scrape_mtggoldfish(
        _FakeSession(html),
        "2026-04-17T23:00:00+00:00",
        {"global": {}, "mtggoldfish": {}, "mtgtop8": {}, "untapped": {}},
    )

    assert len(rows) == 1
    assert rows[0].raw_archetype == "Izzet Prowess"
    assert rows[0].meta_share_pct == 17.7
    assert rows[0].tier_bucket == "Tier 1"


def test_scrape_mtgtop8_extracts_breakdown_rows() -> None:
    html = """
    <div class="hover_tr">
      <div style="display:flex;">
        <div align="center" style="width:100%;">
          <div class="S14"><a href="archetype?a=207&amp;meta=50&amp;f=ST">UR Aggro</a></div>
          <div><div class="S14" style="display:inline-block;width:48%;">14 %</div></div>
        </div>
      </div>
    </div>
    """

    rows = _scrape_mtgtop8(
        _FakeSession(html),
        "2026-04-17T23:00:00+00:00",
        {"global": {}, "mtggoldfish": {}, "mtgtop8": {}, "untapped": {}},
    )

    assert len(rows) == 1
    assert rows[0].raw_archetype == "UR Aggro"
    assert rows[0].meta_share_pct == 14.0
    assert rows[0].tier_bucket == "Tier 1"


def test_scrape_untapped_reports_unavailable_when_public_html_is_premium_locked() -> None:
    html = """
    <html>
      <body>
        <div>Total matches: 270,000</div>
        <div>Winrate and Popularity Stats for Standard Best of 3 are only available to Premium users.</div>
      </body>
    </html>
    """

    rows = _scrape_untapped(
        _FakeSession(html),
        "2026-04-17T23:00:00+00:00",
        {"global": {}, "mtggoldfish": {}, "mtgtop8": {}, "untapped": {}},
    )

    assert len(rows) == 1
    assert rows[0].status == "unavailable"
    assert "premium" in rows[0].notes.lower()
