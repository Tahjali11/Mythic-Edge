# Mythic Edge License Policy

This document explains the project-specific license and open-core boundary for
Mythic Edge in plain English. It is not legal advice and does not replace or
modify the Apache License 2.0 text in [LICENSE](LICENSE).

## What Is Licensed

The committed public/local Mythic Edge source code in this repository is
licensed under Apache-2.0.

This includes committed source files, committed documentation, committed tests,
committed contracts and handoffs, committed validation tooling, and committed
package metadata unless a later reviewed artifact says otherwise.

## Local Open Core

The local open core is the source needed for a user or developer to run Mythic
Edge locally. It includes:

- the local MTGA parser and parser-owned fact normalization;
- local SQLite analytics schema, migrations, ingest, and deterministic views;
- local FastAPI backend and React/Vite frontend source;
- manual JSONL import and live Player.log capture support;
- Match Journal local functionality;
- local analytics and decision-support views;
- private-local-v1 setup and launcher tooling;
- committed tests, docs, workflow templates, and validation tooling.

The local open core preserves the current project shape: Mythic Edge is a
private local MTG Arena analytics and review app.

## Future Hosted Services

Future hosted or paid services may be separate from the local open core. A
future service could include account-based cloud sync, multi-machine analytics,
hosted dashboards, managed backups, hosted storage, hosted AI review summaries,
convenience hosting, managed deployments, or private production
infrastructure.

This policy does not implement or authorize those services. Any future hosted,
cloud, payment, account, OpenAI/model-provider, or production work needs its
own issue, contract, privacy boundary, credential policy, and explicit user
approval.

## Private And Generated Data

Private/generated/local artifacts are not source merely because Mythic Edge can
create or read them. Do not commit, paste into reports, or treat as licensed
source:

- private user data;
- raw MTGA Player.log files;
- private JSONL import artifacts;
- generated SQLite databases and sidecar files;
- local app data roots;
- runtime logs;
- failed posts;
- workbook exports;
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, and
  environment values;
- production configs and private deployment infrastructure;
- hosted service account data;
- private service operations data;
- generated/local-only artifacts that are not committed source.

## Trademarks And Brand Assets

Apache-2.0 does not grant trademark rights. Mythic Edge names, logos, brand
assets, domain names, and other project identity assets are not licensed by
implication unless a later reviewed policy explicitly says so.

## No Legal Advice

This policy is project governance documentation. It is not legal advice, a
terms-of-service document, a privacy policy, a production-readiness claim, or a
commercial-service promise.

## Current Non-Claims

Mythic Edge does not currently claim:

- public release readiness;
- production readiness;
- hosted service readiness;
- payment, account, cloud, or managed deployment readiness;
- OpenAI/model-provider runtime integration;
- AI coaching, hidden-card inference, gameplay advice, or best-line truth;
- a trademark policy beyond the boundary stated here;
- a third-party dependency license audit.
