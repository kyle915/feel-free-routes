# Feel Free — Summer 2026 Guerrilla Field-Sampling Routes

Hosting + collaborative source for the Feel Free weekly street-sampling route plan
(Ignite Productions). Edit one file, push, and the live site + all deliverables rebuild
themselves.

**Markets:** Miami · Ft. Lauderdale · Tampa/St. Pete · Austin · San Antonio (Phoenix excluded)
**Window:** Jun 25 – Jul 31, 2026 · 4 shifts/market/week · 2 BAs × 5.5 hrs

---

## What's in here

| File | What it is |
|------|------------|
| `build_data.py` | **The single source of truth.** Markets, warehouses, weekly corridor templates, and dated event overrides. **Edit this to change the plan.** |
| `build_xlsx.py` / `build_pdf.py` / `build_html.py` | Generators that read `schedule.json`. |
| `rebuild.sh` | Runs all four scripts in order. |
| `schedule.json` | Generated data (don't hand-edit). |
| `index.html` | The live site (also `Feel_Free_Summer2026_Routes_CLIENT.html`). |
| `Feel_Free_Summer2026_Route_Plan_INTERNAL.xlsx` | Internal ops workbook. |
| `Feel_Free_Summer2026_Routes_CLIENT.pdf` | Client one-pagers. |
| `Feel_Free_Sampling_Cowork_Prompt.md` | Prompt to extend/regenerate the plan in Cowork. |
| `.github/workflows/deploy.yml` | Auto-rebuilds + publishes on every push. |

---

## One-time setup (≈5 minutes)

1. **Create the repo.** On GitHub, click **New repository**, name it (e.g. `feel-free-routes`),
   keep it Private if you prefer, and create it.
2. **Upload these files.** Easiest no-terminal way: on the new repo page choose
   **uploading an existing file**, drag in everything from this folder
   (include the `.github` folder), and commit to `main`.
   *Terminal alternative:* `git init && git add . && git commit -m "init" && git branch -M main && git remote add origin <your-repo-url> && git push -u origin main`
3. **Turn on Pages.** Repo **Settings → Pages → Build and deployment → Source = "GitHub Actions."**
4. Done. The included workflow runs on the next push and gives you a live URL at
   **Settings → Pages** (and on each Actions run). Share that link with the client.

> First deploy: after step 2 the Action runs automatically. If Pages was off when you pushed,
> just re-run it from the **Actions** tab once Pages is set to "GitHub Actions."

---

## How your colleague updates it from Cowork

1. In her Cowork, she connects this **GitHub repo** (GitHub connector) or a synced clone of
   the folder, then opens it.
2. She edits `build_data.py` — or simply pastes `Feel_Free_Sampling_Cowork_Prompt.md` and tells
   Cowork what to change ("swap Austin's Friday corridor to East 6th", "add Week 7", etc.).
   Cowork edits `build_data.py` for her.
3. She **commits & pushes to `main`.**
4. The GitHub Action automatically reruns all generators and republishes the site —
   usually live within a minute or two. No manual rebuild, no re-upload.

She does **not** edit `index.html` directly — the data is generated into it. `build_data.py`
is the thing to change.

---

## Updating it yourself locally (optional)

```bash
pip install -r requirements.txt
# edit build_data.py
bash rebuild.sh        # regenerates schedule.json, the xlsx, the pdf, and index.html
```

Open `index.html` in a browser to preview before pushing.

---

## Notes & caveats
- 21+ corridors are stable, but specific 2026 event dates can shift — treat event tags as directional.
- Compliance guardrails (21+ kratom sampling, ID-gating, sidewalk-only, weekly Kratom Eligibility
  Schedule) appear on every deliverable; keep them when editing.
- Prepared by Ignite Productions for Botanic Tonics, LLC (d/b/a Feel Free).
