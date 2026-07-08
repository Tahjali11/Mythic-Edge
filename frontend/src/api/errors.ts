import type {
  AnalyticsHistoryErrorCode,
  ErrorReportApiErrorCode,
  LiveStatusErrorCode,
  ManualImportErrorCode,
  MatchJournalApiErrorCode,
  SetupStatusErrorCode
} from "../types";

export class SetupStatusApiError extends Error {
  code: SetupStatusErrorCode;

  constructor(code: SetupStatusErrorCode, message: string) {
    super(message);
    this.name = "SetupStatusApiError";
    this.code = code;
  }
}

export class LiveStatusApiError extends Error {
  code: LiveStatusErrorCode;

  constructor(code: LiveStatusErrorCode, message: string) {
    super(message);
    this.name = "LiveStatusApiError";
    this.code = code;
  }
}

export class ManualImportApiError extends Error {
  code: ManualImportErrorCode;

  constructor(code: ManualImportErrorCode, message: string) {
    super(message);
    this.name = "ManualImportApiError";
    this.code = code;
  }
}

export class AnalyticsHistoryApiError extends Error {
  code: AnalyticsHistoryErrorCode;

  constructor(code: AnalyticsHistoryErrorCode, message: string) {
    super(message);
    this.name = "AnalyticsHistoryApiError";
    this.code = code;
  }
}

export class MatchJournalApiError extends Error {
  code: MatchJournalApiErrorCode;

  constructor(code: MatchJournalApiErrorCode, message: string) {
    super(message);
    this.name = "MatchJournalApiError";
    this.code = code;
  }
}

export class ErrorReportApiError extends Error {
  code: ErrorReportApiErrorCode;

  constructor(code: ErrorReportApiErrorCode, message: string) {
    super(message);
    this.name = "ErrorReportApiError";
    this.code = code;
  }
}
