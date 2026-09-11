# Cloud Shell dry-run validation

This runbook validates the MyLife v2 backend and recovered backup without writing diary data to Datastore.

## Preconditions

- Project: `floodin-life`
- Branch: `mylife-v2`
- Recovered backup directory exists in Cloud Shell at `~/mylife-recovery`
- Portable backup has already been verified locally by SHA-256

## 1. Clone or update the repository

```bash
cd ~
if [ ! -d MyLife ]; then
  git clone https://github.com/suanhong/MyLife.git
fi
cd ~/MyLife
git fetch origin
git checkout mylife-v2
git pull --ff-only origin mylife-v2
```

## 2. Prepare Python environment

```bash
cd ~/MyLife/v2/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run tests

```bash
PYTHONPATH="$PWD" pytest -q
```

Expected result:

```text
3 passed
```

## 4. Run importer dry-run

This step reads `diaries.jsonl`, `images.json`, and `manifest.json`, summarizes them, and exits before any Datastore write.

```bash
PYTHONPATH="$PWD" python tools/import_backup_to_datastore.py \
  ~/mylife-recovery \
  --project floodin-life \
  --dry-run
```

Expected core counts:

```text
entries                 : 2822
images                  : 252
image_references        : 252
unique_image_references : 252
entries_with_images     : 251
Dry run only. No Datastore writes performed.
```

## 5. Optional local API smoke test

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

In another Cloud Shell tab:

```bash
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/entries?limit=5
```

This still uses the in-memory sample repository unless production settings are provided.

## Safety notes

- `--dry-run` performs no Datastore writes.
- Do not run the importer without `--dry-run` until the target Datastore kinds and rollback plan are reviewed.
- Do not deploy or modify the legacy App Engine `master` branch.
