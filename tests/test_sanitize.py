from mythic_edge_parser.sanitize import scrub_raw_log


def test_scrub_removes_bearer_and_user_path() -> None:
    raw = 'Authorization: Bearer abc.def.ghi\nC:\\Users\\Tahj\\AppData\\Local\\Temp'
    cleaned = scrub_raw_log(raw)
    assert 'abc.def.ghi' not in cleaned
    assert 'Tahj' not in cleaned


def test_scrub_removes_token_session_and_names() -> None:
    raw = (
        'Token: supersecret\n'
        '{"sessionId":"sess_123","screenName":"Tahj#1234","playerName":"Opponent#5678"}'
    )
    cleaned = scrub_raw_log(raw)
    assert "supersecret" not in cleaned
    assert "sess_123" not in cleaned
    assert "Tahj#1234" not in cleaned
    assert "Opponent#5678" not in cleaned


def test_scrub_removes_linux_and_macos_user_paths() -> None:
    raw = "/home/tahj/.config/mtga\n/Users/tahj/Library/Application Support"
    cleaned = scrub_raw_log(raw)
    assert "/home/tahj" not in cleaned
    assert "/Users/tahj" not in cleaned


def test_scrub_removes_client_and_account_ids() -> None:
    raw = '{"clientId":"client-123456","accountId":"acct-987654","userId":"user-222222"}'
    cleaned = scrub_raw_log(raw)
    assert "client-123456" not in cleaned
    assert "acct-987654" not in cleaned
    assert "user-222222" not in cleaned
