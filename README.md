# Enigvra Studio — privacy policies

The public privacy policies for every Android app and game developed and
published by **Enigvra Studio**, served by GitHub Pages from `main`:

https://bilalsafdar4130.github.io/privacy-policies/

| App | Page |
|---|---|
| SparkLogic | `spark-logic.html` |
| Blaze Assembly | `blaze-assembly.html` |
| Vertex Racer | `vertex-racer.html` |
| Pipeline Pioneers | `pipeline-pioneers.html` |
| Pitch Alchemy | `pitch-alchemy.html` |
| ZB Chat | `zb-chat.html` |
| BunyadIlm | `bunyadilm.html` |

Each page is the URL its Play Console listing, its AdMob privacy message and its
in-app privacy screen link to,
so **renaming a page breaks a live app** — add a new page and redirect instead.
Every page carries a "Delete your data" section (`#delete-your-data`) that must
match the in-app **Delete my data** button.

## Shared sections: ads, consent, US and EU law

The sections that do not depend on the app — **Advertising and your ad choices**
(Google AdMob and AppLovin, Google's UMP consent form in the EEA/UK/Switzerland,
the US opt-out, the advertising ID), **Legal bases** (GDPR), **Where data is
processed** (international transfers), **How long data is kept**, the **US state
privacy notice** (CCPA/CPRA and the other state laws), **Your privacy rights,
wherever you live** and **Children** (COPPA) — are written by one script into
every page, between `<!-- shared:NAME:begin -->` / `end` markers:

```
python3 tools/shared_sections.py          # rewrite every page
python3 tools/shared_sections.py --check  # fail if a page is out of date
```

Each app's facts (ads live or not yet, analytics, purchases, where its in-app
privacy buttons are) are in `APPS` at the top of the script. Apps that show no
ads yet are set to `"future"`: their policy already covers advertising, so
turning ads on later only needs `"live"` and a re-run before the release.

**A new app:** copy `_template.html` to `<slug>.html`, fill in its TODOs, add it
to `APPS` and to `index.html`, run the script.

### Before an app with ads goes live (outside this repository)

1. **AdMob → Privacy & messaging → European regulations** — create and publish
   the GDPR message for the app, with its policy URL from the table above.
   Without it Google's consent form has nothing to show, and no ad is served in
   the EEA, the UK or Switzerland.
2. **AdMob → Privacy & messaging → US state regulations** — create and publish
   the US message, so the in-app privacy button offers the US opt-out.
3. **Play Console → App content → Data safety** — declare *Device or other IDs*
   (advertising ID), *Approximate location* (from IP, by the ad SDK) and *App
   interactions*, collected and **shared** for **Advertising or marketing**;
   analytics data collected for *Analytics*; purchase history if the app sells
   anything. **Advertising ID** → *Yes*. **Contains ads** → *Yes*.
4. **Play Console → Store settings** — the privacy policy URL is this site's
   page for the app.

Shared look: `assets/site.css`, the Enigvra Studio logo (`assets/enigvra-logo-*.svg`)
and favicon. The logo is the studio's own artwork; the wordmark is set in
Orbitron (SIL Open Font License 1.1), converted to outlines.

© 2026 Enigvra Studio. All rights reserved. The policy texts and the Enigvra
Studio logo are not licensed for reuse.
