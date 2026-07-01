from mythic_edge_parser.sanitize import scrub_raw_log


def test_scrub_removes_bearer_and_user_path() -> None:
    windows_path = "C:" + "\\" + "Users" + "\\" + "ArenaUser" + "\\AppData\\Local\\Temp"
    raw = "Authorization: Bearer abc.def.ghi\n" + windows_path
    cleaned = scrub_raw_log(raw)
    assert 'abc.def.ghi' not in cleaned
    assert 'ArenaUser' not in cleaned


def test_scrub_removes_token_session_and_names() -> None:
    raw = (
        "Token: " + "supersecret\n"
        '{"sessionId":"sess_123","screenName":"ArenaPilot#1234","playerName":"Opponent#5678"}'
    )
    cleaned = scrub_raw_log(raw)
    assert "supersecret" not in cleaned
    assert "sess_123" not in cleaned
    assert "ArenaPilot#1234" not in cleaned
    assert "Opponent#5678" not in cleaned


def test_scrub_removes_linux_and_macos_user_paths() -> None:
    home_path = "/" + "home/arena-user/.config/mtga"
    mac_path = "/" + "Users/arena-user/Library/Application Support"
    raw = home_path + "\n" + mac_path
    cleaned = scrub_raw_log(raw)
    assert home_path not in cleaned
    assert mac_path not in cleaned


def test_scrub_removes_client_and_account_ids() -> None:
    raw = '{"clientId":"client-123456","accountId":"acct-987654","userId":"user-222222"}'
    cleaned = scrub_raw_log(raw)
    assert "client-123456" not in cleaned
    assert "acct-987654" not in cleaned
    assert "user-222222" not in cleaned
