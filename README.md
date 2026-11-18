# Presidential Daily

Independent, nonpartisan presidential record. Not affiliated with the U.S. government.

## Live site
https://simplejournalist.github.io/presidential-daily/

## Automated editorial research (daily + weekly)

The GitHub Actions workflow `.github/workflows/editorial-drafts.yml` prepares **drafts**, not live articles or emails. Daily runs are scheduled for 12:15 UTC; weekly roundup drafts are scheduled for Sundays at 13:45 UTC. GitHub scheduled runs may be delayed or skipped. You can also use **Actions → Prepare editorial drafts → Run workflow** to test.

The daily generator queries the Federal Register API for recently published executive orders and proclamations, with links to original records. It is **not** a complete White House activity feed, and publication dates are not necessarily signing dates. Weekly drafts link to the daily research drafts and include a checklist for a human-written summary and historical feature.

### Required one-time GitHub setting

Go to **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and enable **Allow GitHub Actions to create and approve pull requests**, if the option is available. Save. If your repository or account restricts these settings, the workflow may run but cannot create its review pull request.

### Review process

1. Look under **Pull requests** for `Editorial review: presidential briefing drafts`.
2. Read the draft files and follow each source link.
3. Correct any errors and add verified summaries and history before approving.
4. Merging research drafts does **not** publish them to the website or email subscribers. That is intentionally a separate future stage.

### Local test

`python scripts/build_briefings.py daily`

`python scripts/build_briefings.py weekly`

Python standard library only. Internet access required for the daily Federal Register query.

## Subscriptions

No email capture, billing, or delivery is connected yet. The live page is a preview. Never collect subscribers or promise paid delivery until a provider and consent/unsubscribe flow are tested.
