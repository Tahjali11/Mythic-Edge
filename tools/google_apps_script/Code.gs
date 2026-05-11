// Global Settings
const WORKBOOK_SCHEMA = {
  spreadsheetId: "1upe46tFVy9Wjdmo_dBSfUc0uD_2e48O4htZszzwTJMg",
  deploymentTag: "matchlog_phase3_v1",
  sheets: {
    matchSummary: "MTGA Match Summary Feed",
    rawArchive: "MTGA Raw Archive",
    debug: "Webhook Debug",
    dashboard: "Dashboard",
    matchLog: "Match Log",
    gameLog: "Game Log",
    helperTable: "Helper Table",
    tierSourceData: "Tier Source Data",
    actionLog: "Action Log",
    deckSnapshot: "Deck Snapshot",
    collectionSnapshot: "Collection Snapshot",
    parserStatus: "Parser Status",
    cardPerformance: "Card Performance",
  },
  landingHeaders: {
    actionLog: [
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
    ],
    deckSnapshot: [
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
    ],
    collectionSnapshot: [
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
    ],
    parserStatus: [
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
    ],
    cardPerformance: [
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
    ],
  },
};

const SPREADSHEET_ID = WORKBOOK_SCHEMA.spreadsheetId;
const MATCH_SUMMARY_SHEET_NAME = WORKBOOK_SCHEMA.sheets.matchSummary;
const ARCHIVE_SHEET_NAME = WORKBOOK_SCHEMA.sheets.rawArchive;
const DEBUG_SHEET_NAME = WORKBOOK_SCHEMA.sheets.debug;
const DASHBOARD_SHEET_NAME = WORKBOOK_SCHEMA.sheets.dashboard;
const MATCH_LOG_SHEET_NAME = WORKBOOK_SCHEMA.sheets.matchLog;
const GAME_LOG_SHEET_NAME = WORKBOOK_SCHEMA.sheets.gameLog;
const HELPER_TABLE_SHEET_NAME = WORKBOOK_SCHEMA.sheets.helperTable;
const TIER_SOURCE_DATA_SHEET_NAME = WORKBOOK_SCHEMA.sheets.tierSourceData;
const ACTION_LOG_SHEET_NAME = WORKBOOK_SCHEMA.sheets.actionLog;
const DECK_SNAPSHOT_SHEET_NAME = WORKBOOK_SCHEMA.sheets.deckSnapshot;
const COLLECTION_SNAPSHOT_SHEET_NAME = WORKBOOK_SCHEMA.sheets.collectionSnapshot;
const PARSER_STATUS_SHEET_NAME = WORKBOOK_SCHEMA.sheets.parserStatus;
const CARD_PERFORMANCE_SHEET_NAME = WORKBOOK_SCHEMA.sheets.cardPerformance;
const DEPLOYMENT_TAG = WORKBOOK_SCHEMA.deploymentTag;
const MATCH_LOG_HEADER_ROW = 1;
const MATCH_LOG_DATE_HEADER = "Date";
const MATCH_LOG_ID_HEADER = "MTGA Match ID";
const GAME_LOG_HEADER_ROW = 1;
const GAME_LOG_DATE_HEADER = "Date";
const GAME_LOG_ID_HEADER = "MTGA Match ID";
const GAME_LOG_NUMBER_HEADER = "Game Number";
const HELPER_TIER_SOURCE_LABEL_CELL = "L2";
const HELPER_TIER_SOURCE_SELECTOR_CELL = "M2";
const HELPER_TIER_REFRESH_LABEL_CELL = "O2";
const HELPER_TIER_REFRESH_VALUE_CELL = "P2";
const HELPER_TIER_STATUS_LABEL_CELL = "Q2";
const HELPER_TIER_STATUS_VALUE_CELL = "R2";
const HELPER_TIER_NOTES_LABEL_CELL = "L3";
const HELPER_TIER_NOTES_VALUE_CELL = "M3";
const DASHBOARD_TIER_SOURCE_SELECTOR_CELL = "N3";
const LEGACY_MTGA_SHEET_NAMES = [
  "MTGA Match Helper",
  "MTGA Match Summary Feed",
  "MTGA Raw Archive",
];
const MATCH_LOG_PARSER_MANAGED_HEADERS = [
  "MGTA Start Time",
  "MTGA End Time",
  "MTGA Rank Raw",
  "MTGA Mulligans",
  "MTGA Sideboard Entered",
  "MTGA Submit Deck Seen",
];
const TIER_SOURCE_HEADERS = [
  "Source Key",
  "Source Label",
  "Refreshed At",
  "Source URL",
  "Meta Window",
  "Source Scope",
  "Status",
  "Notes",
  "Raw Archetype",
  "Normalized Archetype",
  "Meta Share %",
  "Tier Bucket",
  "Tier Letter",
];


// Opening Logic
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("MTGA Tools")
    .addItem("Test Match Log write", "testMatchLogWrite")
    .addItem("Test Game Log write", "testGameLogWrite")
    .addItem("Prepare workbook for phase 1", "prepareWorkbookForPhase1")
    .addItem("Prepare tier source helpers", "prepareTierSourceHelpers")
    .addToUi();
}


function getWorkbook_() {
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}


function getSheet_(ss, name) {
  return ss.getSheetByName(name);
}


function getSheetOrThrow_(ss, name) {
  const sheet = getSheet_(ss, name);
  if (!sheet) {
    throw new Error(`Sheet "${name}" not found.`);
  }
  return sheet;
}


function getHeaderMap_(sheet, headerRow) {
  const lastColumn = sheet.getLastColumn();
  if (lastColumn < 1) return {};

  const headers = sheet.getRange(headerRow, 1, 1, lastColumn).getDisplayValues()[0];
  const map = {};
  headers.forEach((header, index) => {
    const key = String(header || "").trim();
    if (key) {
      map[key] = index + 1;
    }
  });
  return map;
}


function getMatchLogHeaderMap_(sheet) {
  return getHeaderMap_(sheet, MATCH_LOG_HEADER_ROW);
}


function findLastNonBlankRowInColumn_(sheet, col, startRow) {
  const maxRows = sheet.getMaxRows();
  const numRows = maxRows - startRow + 1;
  if (numRows <= 0) return startRow - 1;

  const values = sheet.getRange(startRow, col, numRows, 1).getDisplayValues().flat();
  for (let i = values.length - 1; i >= 0; i--) {
    if (String(values[i]).trim() !== "") {
      return startRow + i;
    }
  }
  return startRow - 1;
}


function getNextMatchLogAppendRow_(sheet) {
  const headerMap = getMatchLogHeaderMap_(sheet);
  const dateCol = headerMap[MATCH_LOG_DATE_HEADER] || 1;
  const firstDataRow = MATCH_LOG_HEADER_ROW + 1;
  const lastUsedDate = findLastNonBlankRowInColumn_(sheet, dateCol, firstDataRow);
  return Math.max(firstDataRow, lastUsedDate + 1);
}


function getGameLogHeaderMap_(sheet) {
  return getHeaderMap_(sheet, GAME_LOG_HEADER_ROW);
}


function getNextGameLogAppendRow_(sheet) {
  const headerMap = getGameLogHeaderMap_(sheet);
  const dateCol = headerMap[GAME_LOG_DATE_HEADER] || 1;
  const firstDataRow = GAME_LOG_HEADER_ROW + 1;
  const lastUsedDate = findLastNonBlankRowInColumn_(sheet, dateCol, firstDataRow);
  return Math.max(firstDataRow, lastUsedDate + 1);
}


function ensureLandingSheet_(ss, name, headers) {
  let sheet = getSheet_(ss, name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }

  const requiredCols = headers.length;
  if (sheet.getMaxColumns() < requiredCols) {
    sheet.insertColumnsAfter(sheet.getMaxColumns(), requiredCols - sheet.getMaxColumns());
  }
  sheet.getRange(1, 1, 1, requiredCols).setValues([headers]);
  return sheet;
}


function buildRowValuesFromHeaders_(headers, rowObject) {
  return headers.map(header => {
    const value = rowObject[header];
    if (Array.isArray(value) || (value && typeof value === "object")) {
      return JSON.stringify(value);
    }
    return value === undefined || value === null ? "" : value;
  });
}


function readExistingKeyMap_(sheet, headerRow, keyHeaders) {
  const headerMap = getHeaderMap_(sheet, headerRow);
  const rowMap = {};
  const firstDataRow = headerRow + 1;
  const lastRow = sheet.getLastRow();
  if (lastRow < firstDataRow) {
    return { headerMap, rowMap };
  }

  const lastColumn = sheet.getLastColumn();
  const values = sheet.getRange(firstDataRow, 1, lastRow - headerRow, lastColumn).getDisplayValues();
  values.forEach((rowValues, index) => {
    const key = keyHeaders
      .map(header => {
        const col = headerMap[header];
        return col ? String(rowValues[col - 1] || "").trim() : "";
      })
      .join("||");
    if (key.replace(/\|/g, "").trim()) {
      rowMap[key] = firstDataRow + index;
    }
  });
  return { headerMap, rowMap };
}


function upsertLandingRows_(sheet, headerRow, headers, keyHeaders, rowObjects) {
  if (!rowObjects.length) return;

  const existing = readExistingKeyMap_(sheet, headerRow, keyHeaders);
  const rowWrites = [];
  const appendRows = [];
  const firstDataRow = headerRow + 1;
  let nextAppendRow = Math.max(firstDataRow, sheet.getLastRow() + 1);

  rowObjects.forEach(rowObject => {
    const key = keyHeaders.map(header => String(rowObject[header] || "").trim()).join("||");
    if (!key.replace(/\|/g, "").trim()) {
      return;
    }
    const values = buildRowValuesFromHeaders_(headers, rowObject);
    const existingRow = existing.rowMap[key];
    if (existingRow) {
      rowWrites.push({ row: existingRow, values });
      return;
    }
    appendRows.push(values);
    existing.rowMap[key] = nextAppendRow;
    nextAppendRow += 1;
  });

  rowWrites.forEach(write => {
    sheet.getRange(write.row, 1, 1, headers.length).setValues([write.values]);
  });

  if (appendRows.length) {
    const requiredLastRow = nextAppendRow - 1;
    if (sheet.getMaxRows() < requiredLastRow) {
      sheet.insertRowsAfter(sheet.getMaxRows(), requiredLastRow - sheet.getMaxRows());
    }
    sheet.getRange(nextAppendRow - appendRows.length, 1, appendRows.length, headers.length).setValues(appendRows);
  }
}


// Primary webhook entry
function doPost(e) {
  const ss = getWorkbook_();
  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);

  try {
    if (!e || !e.postData || !e.postData.contents) {
      throw new Error("Missing POST body.");
    }

    const data = JSON.parse(e.postData.contents);
    const matchId = String(data.match_id || data["MTGA Match ID"] || "").trim();
    const wroteTo = [];

    if (data.event_family === "TierSourceSnapshot") {
      upsertTierSourceSnapshot_(ss, data);
      wroteTo.push(TIER_SOURCE_DATA_SHEET_NAME, HELPER_TABLE_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", "", data, "tier_source_sync");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "MatchLogRow") {
      upsertMatchLogFromPayload_(ss, data);
      wroteTo.push(MATCH_LOG_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "match_log_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "GameLogRow") {
      upsertGameLogFromPayload_(ss, data);
      wroteTo.push(GAME_LOG_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "game_log_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "ActionLogRow") {
      upsertActionLogRow_(ss, data);
      wroteTo.push(ACTION_LOG_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "action_log_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "DeckSnapshotRow") {
      upsertDeckSnapshotRow_(ss, data);
      wroteTo.push(DECK_SNAPSHOT_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "deck_snapshot_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "CollectionSnapshotRow") {
      upsertCollectionSnapshotRow_(ss, data);
      wroteTo.push(COLLECTION_SNAPSHOT_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "collection_snapshot_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "ParserStatusRow") {
      upsertParserStatusRow_(ss, data);
      wroteTo.push(PARSER_STATUS_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "parser_status_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "CardPerformanceRow") {
      upsertCardPerformanceRow_(ss, data);
      wroteTo.push(CARD_PERFORMANCE_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "card_performance_only");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    if (data.event_family === "MatchSummary") {
      const summarySheet = getSheet_(ss, MATCH_SUMMARY_SHEET_NAME);
      if (summarySheet) {
        summarySheet.appendRow(buildSummaryRow_(data));
        wroteTo.push(MATCH_SUMMARY_SHEET_NAME);
      }
      upsertMatchLogFromPayload_(ss, data);
      wroteTo.push(MATCH_LOG_SHEET_NAME);
      logDebug_(debugSheet, "POST_OK", matchId, data, "match_summary_to_matchlog");
      return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });
    }

    const archiveSheet = getSheet_(ss, ARCHIVE_SHEET_NAME);
    if (archiveSheet) {
      archiveSheet.appendRow(buildArchiveRow_(data));
      wroteTo.push(ARCHIVE_SHEET_NAME);
    }

    if (matchId) {
      upsertMatchLogFromPayload_(ss, data);
      wroteTo.push(MATCH_LOG_SHEET_NAME);
    }

    logDebug_(debugSheet, "POST_OK", matchId, data, archiveSheet ? "archive_optional" : "matchlog_only_fallback");
    return jsonResponse_({ ok: true, deployment_tag: DEPLOYMENT_TAG, wrote_to: wroteTo });

  } catch (err) {
    if (debugSheet) {
      debugSheet.appendRow([
        new Date().toISOString(),
        "POST_ERROR",
        DEPLOYMENT_TAG,
        "",
        "",
        "",
        "",
        String(err),
      ]);
    }

    return jsonResponse_({
      ok: false,
      deployment_tag: DEPLOYMENT_TAG,
      error: String(err),
    });
  }
}


function buildSummaryRow_(data) {
  return [
    data.match_id || "",
    data.first_event_time || "",
    data.last_event_time || "",
    data.player_team || "",
    data.winner_team || "",
    data.match_wl || "",
    data.game_wins || "",
    data.game_losses || "",
    data.g1_play_draw || "",
    data.g1_winner_team || "",
    data.g2_play_draw || "",
    data.g2_winner_team || "",
    data.g3_play_draw || "",
    data.g3_winner_team || "",
    data.sideboarding_entered || false,
    data.submit_deck_seen || false,
    data.total_mulligans || 0,
    data.constructed_rank || "",
    data.result_type || "",
    data.result_reason || "",
    data.raw_json || "",
  ];
}


function buildArchiveRow_(data) {
  return [
    data.timestamp || "",
    data.event_family || "",
    data.event_type || "",
    data.scope || "",
    data.match_id || "",
    data.game_number || "",
    data.turn_number || "",
    data.active_player || "",
    data.player_team || "",
    data.winner_team || "",
    data.result_type || "",
    data.result_reason || "",
    data.mulligan_count || "",
    data.submit_deck_seen || "",
    data.sideboarding_entered || "",
    data.constructed_rank || "",
    data.raw_json || "",
  ];
}


function upsertActionLogRow_(ss, data) {
  const headers = WORKBOOK_SCHEMA.landingHeaders.actionLog;
  const sheet = ensureLandingSheet_(ss, ACTION_LOG_SHEET_NAME, headers);
  upsertLandingRows_(
    sheet,
    1,
    headers,
    ["MTGA Match ID", "Game Number", "Timestamp", "Action Type", "grpId", "From Zone", "To Zone"],
    [buildActionLogRowObject_(data)]
  );
}


function buildActionLogRowObject_(data) {
  return {
    "Generated At": String(data.generated_at || data.timestamp || "").trim(),
    "MTGA Match ID": String(data.match_id || "").trim(),
    "Game Number": firstDefinedNumber_(data.game_number),
    "Turn Number": firstDefinedNumber_(data.turn_number),
    "Timestamp": String(data.timestamp || "").trim(),
    "Action Type": String(data.action_type || "").trim(),
    "Cast Mode": String(data.cast_mode || "").trim(),
    "grpId": firstDefinedNumber_(data.grp_id),
    "Card Name": String(data.card_name || "").trim(),
    "Display Name": String(data.display_name || "").trim(),
    "Resolution Status": String(data.resolution_status || "").trim(),
    "Actor": String(data.actor_relation || "").trim(),
    "From Zone": String(data.from_zone_type || "").trim(),
    "To Zone": String(data.to_zone_type || "").trim(),
    "Summary": String(data.summary || "").trim(),
  };
}


function upsertDeckSnapshotRow_(ss, data) {
  const headers = WORKBOOK_SCHEMA.landingHeaders.deckSnapshot;
  const sheet = ensureLandingSheet_(ss, DECK_SNAPSHOT_SHEET_NAME, headers);
  upsertLandingRows_(
    sheet,
    1,
    headers,
    ["Deck Signature", "Section", "Arena ID"],
    [buildDeckSnapshotRowObject_(data)]
  );
}


function buildDeckSnapshotRowObject_(data) {
  return {
    "Generated At": String(data.generated_at || "").trim(),
    "Submitted At": String(data.submitted_at || "").trim(),
    "MTGA Match ID": String(data.match_id || "").trim(),
    "Deck Signature": String(data.deck_signature || "").trim(),
    "Deck Name": String(data.deck_name || "").trim(),
    "Deck Match Mode": String(data.deck_match_mode || "").trim(),
    "Deck Format": String(data.deck_format || "").trim(),
    "Section": String(data.section || "").trim(),
    "Arena ID": firstDefinedNumber_(data.arena_id),
    "Count": firstDefinedNumber_(data.count),
    "Card Name": String(data.card_name || "").trim(),
    "Rarity": String(data.rarity || "").trim(),
    "Set": String(data.set || "").trim(),
    "Type Line": String(data.type_line || "").trim(),
    "Colors": Array.isArray(data.colors) ? data.colors.join(", ") : String(data.colors || "").trim(),
    "Owned Copies": firstDefinedNumber_(data.owned_copies),
    "Missing Copies": firstDefinedNumber_(data.missing_copies),
  };
}


function upsertCollectionSnapshotRow_(ss, data) {
  const headers = WORKBOOK_SCHEMA.landingHeaders.collectionSnapshot;
  const sheet = ensureLandingSheet_(ss, COLLECTION_SNAPSHOT_SHEET_NAME, headers);
  upsertLandingRows_(sheet, 1, headers, ["Generated At"], [buildCollectionSnapshotRowObject_(data)]);
}


function buildCollectionSnapshotRowObject_(data) {
  return {
    "Generated At": String(data.generated_at || "").trim(),
    "Collection Available": boolToYesNo_(data.collection_available),
    "Inventory Available": boolToYesNo_(data.inventory_available),
    "Owned Unique Cards": firstDefinedNumber_(data.owned_unique_cards),
    "Owned Total Card Copies": firstDefinedNumber_(data.owned_total_card_copies),
    "Owned By Rarity": data.owned_by_rarity || {},
    "Inventory Gold": firstDefinedNumber_(data.inventory_gold),
    "Inventory Gems": firstDefinedNumber_(data.inventory_gems),
    "Wildcards Common": firstDefinedNumber_(data.wildcards_common),
    "Wildcards Uncommon": firstDefinedNumber_(data.wildcards_uncommon),
    "Wildcards Rare": firstDefinedNumber_(data.wildcards_rare),
    "Wildcards Mythic": firstDefinedNumber_(data.wildcards_mythic),
    "Active Deck Missing By Rarity": data.active_deck_missing_by_rarity || {},
    "Active Deck Completion Rate": firstDefined_(data.active_deck_completion_rate, ""),
    "Wanted Cards": data.wanted_cards || [],
  };
}


function upsertParserStatusRow_(ss, data) {
  const headers = WORKBOOK_SCHEMA.landingHeaders.parserStatus;
  const sheet = ensureLandingSheet_(ss, PARSER_STATUS_SHEET_NAME, headers);
  upsertLandingRows_(sheet, 1, headers, ["Updated At"], [buildParserStatusRowObject_(data)]);
}


function buildParserStatusRowObject_(data) {
  return {
    "Updated At": String(data.updated_at || "").trim(),
    "Status": String(data.status || "").trim(),
    "Current Match ID": String(data.current_match_id || "").trim(),
    "Current Game Number": firstDefinedNumber_(data.current_game_number),
    "Current Player Team": String(data.current_player_team || "").trim(),
    "Last Event Kind": String(data.last_event_kind || "").trim(),
    "Last Event At": String(data.last_event_at || "").trim(),
    "Webhook Successes": firstDefinedNumber_(data.webhook_successes),
    "Webhook Failures": firstDefinedNumber_(data.webhook_failures),
    "Event Failures": firstDefinedNumber_(data.event_failures),
    "Router Failures": firstDefinedNumber_(data.router_failures),
    "Active Deck Signature": String(data.active_deck_signature || "").trim(),
    "Active Deck Name": String(data.active_deck_name || "").trim(),
    "Active Match Action Count": firstDefinedNumber_(data.active_match_action_count),
  };
}


function upsertCardPerformanceRow_(ss, data) {
  const headers = WORKBOOK_SCHEMA.landingHeaders.cardPerformance;
  const sheet = ensureLandingSheet_(ss, CARD_PERFORMANCE_SHEET_NAME, headers);
  upsertLandingRows_(
    sheet,
    1,
    headers,
    ["Generated At", "Card Key"],
    [buildCardPerformanceRowObject_(data)]
  );
}


function buildCardPerformanceRowObject_(data) {
  return {
    "Generated At": String(data.generated_at || "").trim(),
    "Card Key": String(data.card_key || "").trim(),
    "grpId": firstDefinedNumber_(data.grp_id),
    "Card Name": String(data.card_name || "").trim(),
    "Display Name": String(data.display_name || "").trim(),
    "Resolution Status": String(data.resolution_status || "").trim(),
    "Layout": String(data.layout || "").trim(),
    "Card Faces": data.card_faces || [],
    "Games Seen": firstDefinedNumber_(data.games_seen),
    "Seen In Game": firstDefinedNumber_(data.seen_in_game_games),
    "Seen Win Rate": firstDefined_(data.seen_in_game_win_rate, ""),
    "Opening Hand Games": firstDefinedNumber_(data.opening_hand_games),
    "Opening Hand Win Rate": firstDefined_(data.opening_hand_win_rate, ""),
    "Cast Games": firstDefinedNumber_(data.cast_games),
    "Cast Win Rate": firstDefined_(data.cast_win_rate, ""),
    "Postboard Cast Games": firstDefinedNumber_(data.postboard_cast_games),
    "Postboard Cast Win Rate": firstDefined_(data.postboard_cast_win_rate, ""),
    "Mulliganed Away Games": firstDefinedNumber_(data.mulliganed_away_games),
    "Mulligan Tax": firstDefined_(data.mulligan_tax, ""),
    "Top Matchups": data.top_matchups || [],
    "Top Packages": data.top_packages || [],
  };
}


function upsertMatchLogFromPayload_(ss, data) {
  const matchId = String(data.match_id || data["MTGA Match ID"] || "").trim();
  if (!matchId) return null;

  const sheet = getSheetOrThrow_(ss, MATCH_LOG_SHEET_NAME);
  const row = ensureMatchLogRowForMatchId_(ss, matchId);
  if (!row) return null;

  const fieldMap = buildMatchLogFieldMap_(data);
  writeMatchLogFields_(sheet, row, fieldMap);
  applyMatchLogDefaults_(sheet, row, fieldMap);
  return row;
}


function upsertGameLogFromPayload_(ss, data) {
  const matchId = String(data.match_id || data["MTGA Match ID"] || "").trim();
  const gameNumber = firstDefinedNumber_(data["Game Number"], data.game_number);
  if (!matchId || gameNumber === "") return null;

  const sheet = getSheetOrThrow_(ss, GAME_LOG_SHEET_NAME);
  const row = ensureGameLogRowForMatchGame_(ss, matchId, gameNumber);
  if (!row) return null;

  const fieldMap = buildGameLogFieldMap_(data);
  writeGameLogFields_(sheet, row, fieldMap);
  return row;
}


function buildMatchLogFieldMap_(data) {
  const playerTeam = String(data.player_team || "").trim();
  const matchWin = String(data["Match Win?"] || data.match_wl || "").trim();
  const gamesWon = firstDefinedNumber_(data["Games Won"], data.game_wins);
  const gamesLost = firstDefinedNumber_(data["Games Lost"], data.game_losses);
  const totalGames = firstDefinedNumber_(data["Total Games"], computeTotalGames_(gamesWon, gamesLost));
  const gameWinPct = firstDefinedNumber_(data["Game Win %"], computeGameWinRate_(gamesWon, totalGames));

  return {
    "Date": parseDateOrBlank_(data["Date"] || data.first_event_time || data.timestamp || ""),
    "My Rank": String(data["My Rank"] || data.my_rank || deriveMyRank_(data)).trim(),
    "G1 Play / Draw": String(data["G1 Play / Draw"] || data.g1_play_draw || "").trim(),
    "Game 1 Result": String(data["Game 1 Result"] || data.g1_result || deriveGameResult_(data.g1_winner_team, playerTeam)).trim(),
    "G2 Play / Draw": String(data["G2 Play / Draw"] || data.g2_play_draw || "").trim(),
    "Game 2 Result": String(data["Game 2 Result"] || data.g2_result || deriveGameResult_(data.g2_winner_team, playerTeam)).trim(),
    "G3 Play / Draw": String(data["G3 Play / Draw"] || data.g3_play_draw || "").trim(),
    "Game 3 Result": String(data["Game 3 Result"] || data.g3_result || deriveGameResult_(data.g3_winner_team, playerTeam)).trim(),
    "Games Won": gamesWon,
    "Games Lost": gamesLost,
    "Match Win?": matchWin,
    "Total Games": totalGames,
    "Match Win Flag": firstDefinedNumber_(data["Match Win Flag"], deriveMatchWinFlag_(matchWin)),
    "Game Win %": gameWinPct,
    "MTGA Match ID": String(data["MTGA Match ID"] || data.match_id || "").trim(),
    "MTGA Format": String(data["MTGA Format"] || data.mtga_format || "").trim(),
    "MTGA Event ID": String(data["MTGA Event ID"] || data.event_id || "").trim(),
    "MTGA Queue Type": String(data["MTGA Queue Type"] || data.mtga_queue_type || "").trim(),
    "G1 Mulligans": firstDefinedNumber_(data["G1 Mulligans"], data.g1_mulligans),
    "G2 Mulligans": firstDefinedNumber_(data["G2 Mulligans"], data.g2_mulligans),
    "G3 Mulligans": firstDefinedNumber_(data["G3 Mulligans"], data.g3_mulligans),
    "G1 Turn Count": firstDefinedNumber_(data["G1 Turn Count"], data.g1_turn_count),
    "G2 Turn Count": firstDefinedNumber_(data["G2 Turn Count"], data.g2_turn_count),
    "G3 Turn Count": firstDefinedNumber_(data["G3 Turn Count"], data.g3_turn_count),
    "MGTA Start Time": String(data["MGTA Start Time"] || data.first_event_time || "").trim(),
    "MTGA End Time": String(data["MTGA End Time"] || data.last_event_time || data.timestamp || "").trim(),
    "MTGA Rank Raw": String(data["MTGA Rank Raw"] || data.constructed_rank || "").trim(),
    "MTGA Mulligans": firstDefinedNumber_(data["MTGA Mulligans"], data.total_mulligans),
    "MTGA Sideboard Entered": boolToYesNo_(firstDefined_(data["MTGA Sideboard Entered"], data.sideboarding_entered)),
    "MTGA Submit Deck Seen": boolToYesNo_(firstDefined_(data["MTGA Submit Deck Seen"], data.submit_deck_seen)),
    "MTGA Sync Status": String(data["MTGA Sync Status"] || "").trim(),
  };
}


function buildGameLogFieldMap_(data) {
  const gameNumber = firstDefinedNumber_(data["Game Number"], data.game_number);
  return {
    "Date": parseDateOrBlank_(data["Date"] || data.timestamp || ""),
    "MTGA Format": String(data["MTGA Format"] || "").trim(),
    "My Rank": String(data["My Rank"] || data.my_rank || deriveMyRank_(data)).trim(),
    "MTGA Match ID": String(data["MTGA Match ID"] || data.match_id || "").trim(),
    "Game Number": gameNumber,
    "Pre / Postboard": String(data["Pre / Postboard"] || "").trim(),
    "Play / Draw": String(data["Play / Draw"] || data.play_draw || "").trim(),
    "Mulligans": firstDefinedNumber_(data["Mulligans"], data.mulligan_count),
    "Opening Hand Size": firstDefinedNumber_(data["Opening Hand Size"], data.opening_hand_size),
    "Opening Hand": String(data["Opening Hand"] || data.opening_hand || "").trim(),
    "Mulliganed Away": String(data["Mulliganed Away"] || data.mulliganed_away || "").trim(),
    "Game Result": String(data["Game Result"] || "").trim(),
    "Turn Count": firstDefinedNumber_(data["Turn Count"], data.turn_count),
    "Game Duration": firstDefinedNumber_(data["Game Duration"], data.game_duration_seconds),
    "MTGA Event ID": String(data["MTGA Event ID"] || "").trim(),
    "MTGA Queue Type": String(data["MTGA Queue Type"] || "").trim(),
  };
}


function writeMatchLogFields_(sheet, row, fieldMap) {
  const headerMap = getMatchLogHeaderMap_(sheet);
  const lastColumn = sheet.getLastColumn();
  const rowValues = sheet.getRange(row, 1, 1, lastColumn).getValues()[0];
  Object.keys(fieldMap).forEach(header => {
    const col = headerMap[header];
    if (!col) return;

    const value = fieldMap[header];
    if (value === undefined || value === null) return;
    if (value === "") {
      rowValues[col - 1] = "";
      return;
    }
    rowValues[col - 1] = value;
  });
  sheet.getRange(row, 1, 1, lastColumn).setValues([rowValues]);
}


function writeGameLogFields_(sheet, row, fieldMap) {
  const headerMap = getGameLogHeaderMap_(sheet);
  const lastColumn = sheet.getLastColumn();
  const rowValues = sheet.getRange(row, 1, 1, lastColumn).getValues()[0];
  Object.keys(fieldMap).forEach(header => {
    const col = headerMap[header];
    if (!col) return;

    const value = fieldMap[header];
    if (value === undefined || value === null) return;
    if (value === "") {
      rowValues[col - 1] = "";
      return;
    }
    rowValues[col - 1] = value;
  });
  sheet.getRange(row, 1, 1, lastColumn).setValues([rowValues]);
}


function applyMatchLogDefaults_(sheet, row, fieldMap) {
  const headerMap = getMatchLogHeaderMap_(sheet);
  setIfBlank_(sheet, row, headerMap["Valid?"], "OK");
  setIfBlank_(sheet, row, headerMap["General Analysis?"], "Yes");

  if (fieldMap["Date"]) {
    setIfBlank_(sheet, row, headerMap["Date"], fieldMap["Date"]);
  }
  if (fieldMap["My Rank"]) {
    setIfBlank_(sheet, row, headerMap["My Rank"], fieldMap["My Rank"]);
  }
}


function ensureGameLogContextFormulas_(sheet) {
  const headerMap = getGameLogHeaderMap_(sheet);
  const formulas = {
    "Experiment ID": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$B$2:$B,\"\"),\"\")))`,
    "Deck Code": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$C$2:$C,\"\"),\"\")))`,
    "Opponent Archetype": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$D$2:$D,\"\"),\"\")))`,
    "Opponent Variant": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$E$2:$E,\"\"),\"\")))`,
    "Queue Bucket (Auto)": `=MAP($H2:$H,LAMBDA(matchId,IF(matchId=\"\",\"\",LET(queueBucket,IFNA(XLOOKUP(matchId,'Match Log'!$AF$2:$AF,'Match Log'!$AC$2:$AC,\"\"),\"\"),deckTier,IFNA(XLOOKUP(matchId,'Match Log'!$AF$2:$AF,'Match Log'!$H$2:$H,\"\"),\"\"),IF(queueBucket<>\"\",queueBucket,IF(deckTier=\"\",\"\",IF(LEFT(deckTier,6)=\"Tier 1\",\"Tier 1\",IF(LEFT(deckTier,6)=\"Tier 2\",\"Tier 2\",IF(LEFT(deckTier,6)=\"Tier 3\",\"Tier 3\",\"Fringe\")))))))))`,
    "Match Valid?": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$R$2:$R,\"\"),\"\")))`,
    "Match General Analysis?": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$S$2:$S,\"\"),\"\")))`,
    "Match Primary Comparison?": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$T$2:$T,\"\"),\"\")))`,
    "Match Deck Tier": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$H$2:$H,\"\"),\"\")))`,
    "Match Win?": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$Q$2:$Q,\"\"),\"\")))`,
    "Match Win Flag": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$AA$2:$AA,\"\"),\"\")))`,
    "Match Reason Tag": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$U$2:$U,\"\"),\"\")))`,
    "Match Pilot Error?": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$V$2:$V,\"\"),\"\")))`,
    "Match One-line note": `=ARRAYFORMULA(IF($H2:$H=\"\",\"\",IFNA(XLOOKUP($H2:$H,'Match Log'!$AF$2:$AF,'Match Log'!$W$2:$W,\"\"),\"\")))`,
  };

  Object.keys(formulas).forEach(header => {
    const col = headerMap[header];
    if (!col) return;
    sheet.getRange(2, col).setFormula(formulas[header]);
  });
}


function setIfBlank_(sheet, row, col, value) {
  if (!col || value === undefined || value === null || value === "") return;
  const cell = sheet.getRange(row, col);
  if (String(cell.getDisplayValue()).trim() === "") {
    cell.setValue(value);
  }
}


function firstDefined_(...values) {
  for (let i = 0; i < values.length; i++) {
    const value = values[i];
    if (value !== undefined && value !== null && value !== "") {
      return value;
    }
  }
  return "";
}


function firstDefinedNumber_(...values) {
  for (let i = 0; i < values.length; i++) {
    const raw = values[i];
    if (raw === undefined || raw === null || raw === "") continue;
    const num = Number(raw);
    if (!isNaN(num)) return num;
  }
  return "";
}


function computeTotalGames_(gamesWon, gamesLost) {
  if (gamesWon === "" || gamesLost === "") return "";
  return Number(gamesWon) + Number(gamesLost);
}


function computeGameWinRate_(gamesWon, totalGames) {
  if (gamesWon === "" || totalGames === "" || Number(totalGames) === 0) return "";
  return Number(gamesWon) / Number(totalGames);
}


function deriveMatchWinFlag_(matchWin) {
  if (matchWin === "W") return 1;
  if (matchWin === "L") return 0;
  return "";
}


function parseDateOrBlank_(value) {
  const text = String(value || "").trim();
  if (!text) return "";

  const dt = new Date(text);
  if (isNaN(dt.getTime())) return "";
  return dt;
}


function boolToYesNo_(value) {
  if (value === true) return "Yes";
  if (value === false) return "No";

  const text = String(value || "").trim().toLowerCase();
  if (!text) return "";
  if (["yes", "y", "true", "1"].includes(text)) return "Yes";
  if (["no", "n", "false", "0"].includes(text)) return "No";
  return String(value);
}


function deriveMyRank_(data) {
  const explicit = String(data.my_rank || "").trim();
  if (explicit) return explicit;

  const raw = String(data.constructed_rank || "").trim();
  if (!raw) return "";

  if (/^mythic/i.test(raw)) {
    return /\d+\.\d+/.test(raw) ? "Mythic %" : "Mythic #";
  }

  const match = raw.match(/^(Bronze|Silver|Gold|Platinum|Diamond|Mythic)/i);
  return match ? match[1].charAt(0).toUpperCase() + match[1].slice(1).toLowerCase() : "";
}


function deriveGameResult_(winnerTeam, playerTeam) {
  const winner = String(winnerTeam || "").trim();
  const player = String(playerTeam || "").trim();
  if (!winner || !player) return "";
  return winner === player ? "W" : "L";
}


function jsonResponse_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}


function logDebug_(debugSheet, status, matchId, data, destination) {
  if (!debugSheet) return;
  debugSheet.appendRow([
    new Date().toISOString(),
    status,
    DEPLOYMENT_TAG,
    matchId || "",
    data.event_family || "",
    data.event_type || "",
    data.scope || "",
    destination,
  ]);
}


// Tier source helpers
function prepareTierSourceHelpers() {
  const ss = getWorkbook_();
  const dashboardSheet = getSheet_(ss, DASHBOARD_SHEET_NAME);
  const helperSheet = getSheetOrThrow_(ss, HELPER_TABLE_SHEET_NAME);
  const tierSheet = ensureTierSourceDataSheet_(ss);
  configureHelperTableTierSourceControls_(helperSheet, tierSheet, dashboardSheet);
  hideSheetIfSafe_(ss, tierSheet);

  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);
  logDebug_(debugSheet, "TIER_HELPERS_PREPARED", "", {
    event_family: "Maintenance",
    event_type: "prepareTierSourceHelpers",
    scope: "Workbook",
  }, "tier_source_helpers");

  SpreadsheetApp.getActive().toast("Tier source helpers are ready.");
}


function upsertTierSourceSnapshot_(ss, data) {
  const dashboardSheet = getSheet_(ss, DASHBOARD_SHEET_NAME);
  const helperSheet = getSheetOrThrow_(ss, HELPER_TABLE_SHEET_NAME);
  const tierSheet = ensureTierSourceDataSheet_(ss);
  const records = Array.isArray(data.records) ? data.records : [];

  rewriteTierSourceData_(tierSheet, records);
  configureHelperTableTierSourceControls_(helperSheet, tierSheet, dashboardSheet);
  hideSheetIfSafe_(ss, tierSheet);
}


function ensureTierSourceDataSheet_(ss) {
  let sheet = getSheet_(ss, TIER_SOURCE_DATA_SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(TIER_SOURCE_DATA_SHEET_NAME);
  }
  return sheet;
}


function rewriteTierSourceData_(sheet, records) {
  const rows = records.map(record => buildTierSourceDataRow_(record));
  const targetRows = Math.max(2, rows.length + 1);
  const targetCols = TIER_SOURCE_HEADERS.length;

  if (sheet.getMaxRows() < targetRows) {
    sheet.insertRowsAfter(sheet.getMaxRows(), targetRows - sheet.getMaxRows());
  }
  if (sheet.getMaxColumns() < targetCols) {
    sheet.insertColumnsAfter(sheet.getMaxColumns(), targetCols - sheet.getMaxColumns());
  }

  sheet.clearContents();
  sheet.getRange(1, 1, 1, targetCols).setValues([TIER_SOURCE_HEADERS]);
  if (rows.length) {
    sheet.getRange(2, 1, rows.length, targetCols).setValues(rows);
  }
}


function buildTierSourceDataRow_(record) {
  return [
    record.source_key || "",
    record.source_label || "",
    record.refreshed_at || "",
    record.source_url || "",
    record.meta_window || "",
    record.source_scope || "",
    record.status || "",
    record.notes || "",
    record.raw_archetype || "",
    record.normalized_archetype || "",
    record.meta_share_pct === undefined || record.meta_share_pct === null || record.meta_share_pct === "" ? "" : Number(record.meta_share_pct),
    record.tier_bucket || "",
    record.tier_letter || "",
  ];
}


function configureHelperTableTierSourceControls_(helperSheet, tierSheet, dashboardSheet) {
  const lastRow = Math.max(tierSheet.getLastRow(), 2);
  const sourceLabels = getUniqueTierSourceLabels_(tierSheet, lastRow);

  helperSheet.getRange(HELPER_TIER_SOURCE_LABEL_CELL).setValue("Tier Source:");
  helperSheet.getRange(HELPER_TIER_REFRESH_LABEL_CELL).setValue("Last Refresh:");
  helperSheet.getRange(HELPER_TIER_STATUS_LABEL_CELL).setValue("Status:");
  helperSheet.getRange(HELPER_TIER_NOTES_LABEL_CELL).setValue("Notes:");

  const selectorCell = helperSheet.getRange(HELPER_TIER_SOURCE_SELECTOR_CELL);
  if (sourceLabels.length) {
    if (dashboardSheet) {
      configureDashboardTierSourceSelector_(dashboardSheet, selectorCell, sourceLabels);
    } else {
      const rule = SpreadsheetApp.newDataValidation()
        .requireValueInList(sourceLabels, true)
        .setAllowInvalid(false)
        .build();
      selectorCell.setDataValidation(rule);
      if (!sourceLabels.includes(String(selectorCell.getDisplayValue()).trim())) {
        selectorCell.setValue(sourceLabels[0]);
      }
    }
  } else if (dashboardSheet) {
    selectorCell.setFormula("='" + DASHBOARD_SHEET_NAME + "'!" + DASHBOARD_TIER_SOURCE_SELECTOR_CELL);
  }

  helperSheet.getRange(HELPER_TIER_REFRESH_VALUE_CELL).setFormula(
    "=IFERROR(INDEX(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$C$2:$C,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2),1),\"\")"
  );
  helperSheet.getRange(HELPER_TIER_STATUS_VALUE_CELL).setFormula(
    "=IFERROR(INDEX(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$G$2:$G,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2),1),\"\")"
  );
  helperSheet.getRange(HELPER_TIER_NOTES_VALUE_CELL).setFormula(
    "=IFERROR(TEXTJOIN(\" | \",TRUE,UNIQUE(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$H$2:$H,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$H$2:$H<>\"\"))),\"\")"
  );

  resetTierBucketSpillArea_(helperSheet);
}


function configureDashboardTierSourceSelector_(dashboardSheet, helperSelectorCell, sourceLabels) {
  const dashboardSelectorCell = dashboardSheet.getRange(DASHBOARD_TIER_SOURCE_SELECTOR_CELL);
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(sourceLabels, true)
    .setAllowInvalid(false)
    .build();

  dashboardSelectorCell.setDataValidation(rule);

  const dashboardValue = String(dashboardSelectorCell.getDisplayValue()).trim();
  const helperValue = String(helperSelectorCell.getDisplayValue()).trim();
  const initialValue = sourceLabels.includes(dashboardValue)
    ? dashboardValue
    : sourceLabels.includes(helperValue)
      ? helperValue
      : sourceLabels[0];

  dashboardSelectorCell.setValue(initialValue);
  helperSelectorCell.setFormula("='" + DASHBOARD_SHEET_NAME + "'!" + DASHBOARD_TIER_SOURCE_SELECTOR_CELL);
}


function getUniqueTierSourceLabels_(sheet, lastRow) {
  if (lastRow < 2) return [];
  const labels = sheet.getRange(2, 2, lastRow - 1, 1).getDisplayValues().flat();
  return [...new Set(labels.map(value => String(value).trim()).filter(Boolean))];
}


function resetTierBucketSpillArea_(helperSheet) {
  const startRow = 5;
  const maxRows = helperSheet.getMaxRows();
  const numRows = Math.max(1, maxRows - startRow + 1);
  const customTier1Range = "$Q$5:$Q";
  const customTier2Range = "$R$5:$R";
  const customTier3Range = "$S$5:$S";
  const customFringeRange = "$T$5:$T";
  helperSheet.getRange(startRow, 13, numRows, 4).clearContent();
  helperSheet.getRange("Q4:T4").setValues([[
    "Custom Tier 1",
    "Custom Tier 2",
    "Custom Tier 3",
    "Custom Fringe",
  ]]);

  helperSheet.getRange("M5").setFormula(
    "=LET(site,IFERROR(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$G$2:$G=\"ok\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$L$2:$L=\"Tier 1\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J<>\"\"),\"\"),custom,IFERROR(FILTER(" + customTier1Range + "," + customTier1Range + "<>\"\"),\"\"),combined,VSTACK(site,custom),IFERROR(SORT(UNIQUE(FILTER(combined,combined<>\"\"))),\"\"))"
  );
  helperSheet.getRange("N5").setFormula(
    "=LET(site,IFERROR(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$G$2:$G=\"ok\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$L$2:$L=\"Tier 2\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J<>\"\"),\"\"),custom,IFERROR(FILTER(" + customTier2Range + "," + customTier2Range + "<>\"\"),\"\"),combined,VSTACK(site,custom),IFERROR(SORT(UNIQUE(FILTER(combined,combined<>\"\"))),\"\"))"
  );
  helperSheet.getRange("O5").setFormula(
    "=LET(site,IFERROR(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$G$2:$G=\"ok\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$L$2:$L=\"Tier 3\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J<>\"\"),\"\"),custom,IFERROR(FILTER(" + customTier3Range + "," + customTier3Range + "<>\"\"),\"\"),combined,VSTACK(site,custom),IFERROR(SORT(UNIQUE(FILTER(combined,combined<>\"\"))),\"\"))"
  );
  helperSheet.getRange("P5").setFormula(
    "=LET(site,IFERROR(FILTER('" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$B$2:$B=$M$2,'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$G$2:$G=\"ok\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$L$2:$L=\"Fringe\",'" + TIER_SOURCE_DATA_SHEET_NAME + "'!$J$2:$J<>\"\"),\"\"),custom,IFERROR(FILTER(" + customFringeRange + "," + customFringeRange + "<>\"\"),\"\"),combined,VSTACK(site,custom,\"Other / Unknown\"),IFERROR(SORT(UNIQUE(FILTER(combined,combined<>\"\"))),\"\"))"
  );
}


function hideSheetIfSafe_(ss, sheet) {
  const activeSheet = ss.getActiveSheet();
  if (!sheet) return;
  if (activeSheet && activeSheet.getSheetId() === sheet.getSheetId()) return;
  if (!sheet.isSheetHidden()) {
    sheet.hideSheet();
  }
}


// Workbook cleanup helpers
function prepareWorkbookForPhase1() {
  const ss = getWorkbook_();
  const matchLogSheet = getSheetOrThrow_(ss, MATCH_LOG_SHEET_NAME);
  const gameLogSheet = getSheetOrThrow_(ss, GAME_LOG_SHEET_NAME);
  freezeParserManagedMatchLogColumns_(matchLogSheet);
  ensureGameLogContextFormulas_(gameLogSheet);
  ensureLandingSheet_(ss, ACTION_LOG_SHEET_NAME, WORKBOOK_SCHEMA.landingHeaders.actionLog);
  ensureLandingSheet_(ss, DECK_SNAPSHOT_SHEET_NAME, WORKBOOK_SCHEMA.landingHeaders.deckSnapshot);
  ensureLandingSheet_(ss, COLLECTION_SNAPSHOT_SHEET_NAME, WORKBOOK_SCHEMA.landingHeaders.collectionSnapshot);
  ensureLandingSheet_(ss, PARSER_STATUS_SHEET_NAME, WORKBOOK_SCHEMA.landingHeaders.parserStatus);
  ensureLandingSheet_(ss, CARD_PERFORMANCE_SHEET_NAME, WORKBOOK_SCHEMA.landingHeaders.cardPerformance);
  hideLegacyMtgaTabs_(ss);
  configureHelperTableTierSourceControls_(
    getSheetOrThrow_(ss, HELPER_TABLE_SHEET_NAME),
    ensureTierSourceDataSheet_(ss),
    getSheet_(ss, DASHBOARD_SHEET_NAME)
  );
  hideSheetIfSafe_(ss, ensureTierSourceDataSheet_(ss));

  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);
  logDebug_(debugSheet, "WORKBOOK_PREPARED", "", {
    event_family: "Maintenance",
    event_type: "prepareWorkbookForPhase1",
    scope: "Workbook",
  }, "phase1_cleanup");

  SpreadsheetApp.getActive().toast("Phase 1 workbook cleanup finished.");
}


function freezeParserManagedMatchLogColumns_(sheet) {
  const headerMap = getMatchLogHeaderMap_(sheet);
  const firstDataRow = MATCH_LOG_HEADER_ROW + 1;
  const maxRows = sheet.getMaxRows();
  const numRows = maxRows - firstDataRow + 1;
  if (numRows <= 0) return;

  MATCH_LOG_PARSER_MANAGED_HEADERS.forEach(header => {
    const col = headerMap[header];
    if (!col) return;
    const range = sheet.getRange(firstDataRow, col, numRows, 1);
    const values = range.getValues();
    range.setValues(values);
  });
}


function hideLegacyMtgaTabs_(ss) {
  const activeSheet = ss.getActiveSheet();
  LEGACY_MTGA_SHEET_NAMES.forEach(name => {
    const sheet = getSheet_(ss, name);
    if (!sheet) return;
    if (activeSheet && sheet.getSheetId() === activeSheet.getSheetId()) return;
    if (!sheet.isSheetHidden()) {
      sheet.hideSheet();
    }
  });
}


// Match Log row lookup
function ensureMatchLogRowForMatchId_(ss, matchId) {
  if (!matchId) return null;

  const sheet = getSheetOrThrow_(ss, MATCH_LOG_SHEET_NAME);
  const headerMap = getMatchLogHeaderMap_(sheet);
  const idCol = headerMap[MATCH_LOG_ID_HEADER];
  if (!idCol) {
    throw new Error(`Match Log is missing "${MATCH_LOG_ID_HEADER}" in header row ${MATCH_LOG_HEADER_ROW}.`);
  }

  const firstDataRow = MATCH_LOG_HEADER_ROW + 1;
  const maxRows = sheet.getMaxRows();
  const numRows = maxRows - firstDataRow + 1;
  if (numRows <= 0) {
    throw new Error("Match Log has no data rows available.");
  }

  const idValues = sheet.getRange(firstDataRow, idCol, numRows, 1).getDisplayValues().flat();
  const normalizedMatchId = String(matchId).trim();
  const existingIndex = idValues.findIndex(value => String(value).trim() === normalizedMatchId);
  if (existingIndex !== -1) {
    return firstDataRow + existingIndex;
  }

  let targetRow = getNextMatchLogAppendRow_(sheet);
  while (targetRow <= maxRows && String(sheet.getRange(targetRow, idCol).getDisplayValue()).trim() !== "") {
    targetRow++;
  }

  if (targetRow > maxRows) {
    sheet.insertRowsAfter(maxRows, 100);
  }

  sheet.getRange(targetRow, idCol).setValue(matchId);
  return targetRow;
}


function ensureGameLogRowForMatchGame_(ss, matchId, gameNumber) {
  if (!matchId || gameNumber === "") return null;

  const sheet = getSheetOrThrow_(ss, GAME_LOG_SHEET_NAME);
  const headerMap = getGameLogHeaderMap_(sheet);
  const idCol = headerMap[GAME_LOG_ID_HEADER];
  const numberCol = headerMap[GAME_LOG_NUMBER_HEADER];
  if (!idCol || !numberCol) {
    throw new Error(`Game Log is missing "${GAME_LOG_ID_HEADER}" or "${GAME_LOG_NUMBER_HEADER}" in header row ${GAME_LOG_HEADER_ROW}.`);
  }

  const firstDataRow = GAME_LOG_HEADER_ROW + 1;
  const maxRows = sheet.getMaxRows();
  const numRows = maxRows - firstDataRow + 1;
  if (numRows <= 0) {
    throw new Error("Game Log has no data rows available.");
  }

  const idValues = sheet.getRange(firstDataRow, idCol, numRows, 1).getDisplayValues().flat();
  const numberValues = sheet.getRange(firstDataRow, numberCol, numRows, 1).getDisplayValues().flat();
  const normalizedMatchId = String(matchId).trim();
  const normalizedGameNumber = String(gameNumber).trim();
  const existingIndex = idValues.findIndex((value, index) =>
    String(value).trim() === normalizedMatchId &&
    String(numberValues[index]).trim() === normalizedGameNumber
  );
  if (existingIndex !== -1) {
    return firstDataRow + existingIndex;
  }

  let targetRow = getNextGameLogAppendRow_(sheet);
  while (
    targetRow <= maxRows &&
    (
      String(sheet.getRange(targetRow, idCol).getDisplayValue()).trim() !== "" ||
      String(sheet.getRange(targetRow, numberCol).getDisplayValue()).trim() !== ""
    )
  ) {
    targetRow++;
  }

  if (targetRow > maxRows) {
    sheet.insertRowsAfter(maxRows, 100);
  }

  sheet.getRange(targetRow, idCol).setValue(matchId);
  sheet.getRange(targetRow, numberCol).setValue(gameNumber);
  return targetRow;
}


// Debugging & Testing Functions
function testMatchLogWrite() {
  const ss = getWorkbook_();
  upsertMatchLogFromPayload_(ss, {
    event_family: "MatchLogRow",
    event_type: "match_log_row",
    scope: "Match",
    match_id: "test-match-log-id",
    first_event_time: new Date().toISOString(),
    last_event_time: new Date().toISOString(),
    my_rank: "Diamond",
    g1_play_draw: "Play",
    g1_result: "W",
    g2_play_draw: "Draw",
    g2_result: "L",
    g3_play_draw: "Play",
    g3_result: "W",
    game_wins: 2,
    game_losses: 1,
    match_wl: "W",
    total_mulligans: 1,
    constructed_rank: "Diamond 2",
    sideboarding_entered: true,
    submit_deck_seen: true,
  });

  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);
  logDebug_(debugSheet, "TEST_WRITE", "test-match-log-id", {
    event_family: "MatchLogRow",
    event_type: "match_log_row",
    scope: "Match",
  }, "matchlog_only");
}


function testGameLogWrite() {
  const ss = getWorkbook_();
  upsertGameLogFromPayload_(ss, {
    event_family: "GameLogRow",
    event_type: "game_log_row",
    scope: "Game",
    match_id: "test-match-log-id",
    timestamp: new Date().toISOString(),
    "Date": new Date().toISOString(),
    "MTGA Format": "Constructed",
    "My Rank": "Diamond",
    "MTGA Match ID": "test-match-log-id",
    "Game Number": 1,
    "Pre / Postboard": "Preboard",
    "Play / Draw": "Play",
    "Mulligans": 1,
    "Opening Hand Size": 6,
    "Opening Hand": "Forest; Llanowar Elves; Cut Down; Swamp; Go for the Throat; Faerie Dreamthief",
    "Mulliganed Away": "Duress; Blooming Marsh; Sheoldred, the Apocalypse; Mosswood Dreadknight; Forest; Forest; Cut Down",
    "Game Result": "W",
    "Turn Count": 11,
    "Game Duration": 420,
    "MTGA Event ID": "Constructed_BestOf3",
    "MTGA Queue Type": "Best of 3",
  });

  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);
  logDebug_(debugSheet, "TEST_WRITE", "test-match-log-id", {
    event_family: "GameLogRow",
    event_type: "game_log_row",
    scope: "Game",
  }, "game_log_only");
}


function testTierSourceWrite() {
  const ss = getWorkbook_();
  upsertTierSourceSnapshot_(ss, {
    event_family: "TierSourceSnapshot",
    event_type: "tier_source_snapshot",
    scope: "Workbook",
    records: [
      {
        source_key: "mtggoldfish",
        source_label: "MTGGoldfish",
        refreshed_at: new Date().toISOString(),
        source_url: "https://www.mtggoldfish.com/metagame/standard#paper",
        meta_window: "Past 14 days",
        source_scope: "Standard paper meta, public site",
        status: "ok",
        notes: "",
        raw_archetype: "Izzet Prowess",
        normalized_archetype: "Izzet Prowess",
        meta_share_pct: 17.7,
        tier_bucket: "Tier 1",
        tier_letter: "",
      },
      {
        source_key: "mtgtop8",
        source_label: "MTGTop8",
        refreshed_at: new Date().toISOString(),
        source_url: "https://www.mtgtop8.com/archetype?a=770&meta=50&f=ST",
        meta_window: "Past 14 days",
        source_scope: "Standard tournament meta, public site",
        status: "ok",
        notes: "",
        raw_archetype: "UR Aggro",
        normalized_archetype: "UR Aggro",
        meta_share_pct: 14,
        tier_bucket: "Tier 1",
        tier_letter: "",
      },
    ],
  });

  const debugSheet = getSheet_(ss, DEBUG_SHEET_NAME);
  logDebug_(debugSheet, "TEST_WRITE", "", {
    event_family: "TierSourceSnapshot",
    event_type: "tier_source_snapshot",
    scope: "Workbook",
  }, "tier_source_sync");
}
