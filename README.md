# Paycrest Protocol Analytics

On-chain analytics for the **Paycrest Protocol**, tracked on Dune.

📊 **Live dashboard:** https://dune.com/iamphantasm0/paycrest-protocol-analytics

## Queries

The dashboard is powered by the Dune queries listed in [`queries.yml`](queries.yml).
Their SQL is version-controlled in the [`queries/`](queries/) directory and kept in
sync with Dune by a GitHub Action (see below).

| Query ID | Open on Dune | SQL |
|----------|--------------|-----|
| 7527000 | https://dune.com/queries/7527000 | [`queries/7527000.sql`](queries/7527000.sql) |
| 7527002 | https://dune.com/queries/7527002 | [`queries/7527002.sql`](queries/7527002.sql) |
| 7527004 | https://dune.com/queries/7527004 | [`queries/7527004.sql`](queries/7527004.sql) |
| 7527006 | https://dune.com/queries/7527006 | [`queries/7527006.sql`](queries/7527006.sql) |
| 7527005 | https://dune.com/queries/7527005 | [`queries/7527005.sql`](queries/7527005.sql) |

## Keeping the repo in sync with Dune

The queries are authored on Dune; this repo mirrors their SQL for version control.

### One-time setup

1. Get a Dune API key: https://dune.com/settings/api
2. Add it to this repository as an Actions secret named **`DUNE_API_KEY`**
   (GitHub → repo → *Settings* → *Secrets and variables* → *Actions* → *New repository secret*).

### Pulling the SQL

- **Automatically:** the [`Sync Dune queries`](.github/workflows/sync-dune.yml) workflow
  runs daily and can be triggered manually from the *Actions* tab. It fetches each
  query's SQL from Dune and commits any changes.
- **Locally:**

  ```bash
  export DUNE_API_KEY=your_key_here
  python scripts/sync_queries.py
  ```

To add a new query to the dashboard, add its ID to `queries.yml` and re-run the sync.
