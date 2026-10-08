#!/usr/bin/env python3
"""Writes the sections every Enigvra Studio privacy policy shares.

    python3 tools/shared_sections.py          # rewrite every page in place
    python3 tools/shared_sections.py --check  # exit 1 if any page is stale

WHY. Seven apps, one studio, one set of laws. The parts of a policy that do not
depend on the app -- how advertising consent works, the GDPR legal bases, the
international transfers, the US state privacy notice, the rights people have in
each region, children -- were copy-pasted per page and drifted. They now live
here once, filled in with each app's own facts (APPS below), and are written
into each page between markers:

    <!-- shared:NAME:begin -->  ...generated...  <!-- shared:NAME:end -->

Everything outside the markers is the app's own text and is never touched.

ADS ARE COVERED IN EVERY POLICY, including apps that show none yet: "ads":
"future" writes the advertising sections as applying "to any version that shows
ads", so turning ads on later does not leave the published policy behind. When
an app starts showing ads, set it to "live" and run this script before the
release. A NEW APP: copy _template.html to <slug>.html, add it to APPS and to
index.html, and run this script. See README.md.

This is not legal advice; it is the studio's best statement of what its apps do.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "8 October 2026"
STUDIO = "Enigvra Studio"
OWNER = "Bilal Safdar"
EMAIL = "bilalsafdar3014@gmail.com"

# One entry per published page. Keep the facts true to the shipped build.
#   ads            "live"   -- this version shows ads
#                  "future" -- no ads in this version; the ad sections apply to
#                              any later version that shows them
#   analytics      True if the app sends Firebase Analytics
#   purchases      True if the app sells anything through Google Play Billing
#   ad_free        the name of the purchase that removes ads, or ""
#   ad_settings    where the in-app button that reopens Google's consent /
#                  privacy-options form lives ("" for "future")
#   analytics_off  where analytics is switched off in the app, or ""
#   delete_path    where Delete my data is
#   children       "13+" (not directed at under-13s) or "all" (all ages)
APPS = {
    "spark-logic": {
        "name": "SparkLogic", "ads": "live", "analytics": True, "purchases": True,
        "ad_free": "AD-FREE FOREVER",
        "ad_settings": "Settings → ABOUT &amp; LEGAL → ADS → AD PRIVACY SETTINGS",
        "analytics_off": "Settings → ABOUT &amp; LEGAL → ANALYTICS",
        "delete_path": "Settings → ABOUT &amp; LEGAL → PRIVACY POLICY → DELETE MY DATA",
        "children": "13+",
    },
    "blaze-assembly": {
        "name": "Blaze Assembly", "ads": "live", "analytics": True, "purchases": True,
        "ad_free": "Remove ads",
        "ad_settings": "Settings → About and legal → Data and analytics → Your data "
                       "and ad choices → Ad privacy settings",
        "analytics_off": "Settings → About and legal → Data and analytics",
        "delete_path": "Settings → About and legal → Privacy policy",
        "children": "13+",
    },
    "vertex-racer": {
        "name": "Vertex Racer", "ads": "live", "analytics": True, "purchases": True,
        "ad_free": "Remove ads",
        "ad_settings": "Settings → Privacy &amp; data → AD PRIVACY",
        "analytics_off": "",
        "delete_path": "Settings → Privacy &amp; data → Delete my data",
        "children": "13+",
    },
    "pipeline-pioneers": {
        "name": "Pipeline Pioneers", "ads": "live", "analytics": True, "purchases": True,
        "ad_free": "AD-FREE WORKSHOP",
        "ad_settings": "Settings → Privacy &amp; data",
        "analytics_off": "",
        "delete_path": "Settings → Privacy &amp; data → Delete my data",
        "children": "13+",
    },
    "pitch-alchemy": {
        "name": "Pitch Alchemy", "ads": "future", "analytics": False, "purchases": False,
        "ad_free": "", "ad_settings": "", "analytics_off": "",
        "delete_path": "Settings → Privacy → Delete my data",
        "children": "all",
    },
    "zb-chat": {
        "name": "ZB Chat", "ads": "future", "analytics": False, "purchases": False,
        "ad_free": "", "ad_settings": "", "analytics_off": "",
        "delete_path": "Settings → Privacy policy &amp; delete my data",
        "children": "13+",
    },
    "bunyadilm": {
        "name": "BunyadIlm", "ads": "future", "analytics": False, "purchases": False,
        "ad_free": "", "ad_settings": "", "analytics_off": "",
        "delete_path": "Settings → Privacy policy → Delete my data",
        "children": "13+",
    },
}

GOOGLE_PARTNERS = "https://policies.google.com/technologies/partner-sites"
GOOGLE_PRIVACY = "https://policies.google.com/privacy"
APPLOVIN_PRIVACY = "https://www.applovin.com/privacy/"
FIREBASE_PRIVACY = "https://firebase.google.com/support/privacy"
GOOGLE_ADS_SETTINGS = "https://support.google.com/googleplay/android-developer/answer/6048248"
EDPB = "https://edpb.europa.eu/about-edpb/about-edpb/members_en"


def _link(url: str, text: str) -> str:
    return f'<a href="{url}">{text}</a>'


# --- The sections --------------------------------------------------------------


def advertising(app: dict) -> str:
    """How ads, consent and the advertising ID work. Every page carries it."""
    future = app["ads"] == "future"
    name = app["name"]
    if future:
        intro = (
            f"<p><strong>This version of {name} shows no advertising and contains no "
            f"advertising SDK.</strong> {STUDIO} plans to support its apps with "
            "advertising, so this section already describes how advertising works in "
            f"any version of {name} that shows it. That version will not be released "
            "until this page names it, with the date at the top updated.</p>\n"
        )
        lead = "In a version that shows advertising:"
    else:
        intro = (
            f"<p>{name} shows advertising to stay free to play. This section applies "
            "to every advertisement in the app, from every network.</p>\n"
        )
        lead = "How it works:"
    remove = (
        f"<li><strong>Remove ads.</strong> The {app['ad_free']} purchase switches "
        "advertising off for good, on every network, and Google Play restores it if "
        "you reinstall on the same Google account.</li>\n"
        if app["ad_free"] else ""
    )
    settings = (
        f"<li><strong>Change your answer in the app</strong> at any time: "
        f"<strong>{app['ad_settings']}</strong> reopens Google's privacy form. It is "
        "shown wherever Google's form applies to you.</li>\n"
        if app["ad_settings"] else
        "<li><strong>Change your answer in the app</strong> at any time, from the "
        "app's privacy settings, wherever Google's form applies to you.</li>\n"
    )
    return f"""<h2 id="advertising-choices">Advertising and your ad choices</h2>
{intro}<p>{lead}</p>
<ul>
<li><strong>Who serves the ads.</strong> Google AdMob, which may also fill an ad
  slot through mediation with AppLovin (AppLovin MAX) and the ad networks they
  work with. Ad content is limited to a general-audience rating.</li>
<li><strong>What an ad network receives.</strong> Your device's advertising ID (a
  resettable identifier Android provides; the app declares the
  <code>AD_ID</code> permission for it), your IP address (from which the network
  infers an approximate location such as your country or city), technical
  information about your device and the app, and how each ad performed —
  whether it loaded, was shown or was tapped. We never give an ad network your
  name, email address, contacts, precise location or anything you type.</li>
<li><strong>The advertising ID is kept apart from analytics.</strong> It is read
  for advertising only and is never joined to the app's own statistics.</li>
<li><strong>Europe, the UK and Switzerland: consent first.</strong> In the
  European Economic Area, the United Kingdom and Switzerland the app shows
  Google's consent form (Google's User Messaging Platform, a Google-certified
  consent management platform that uses the IAB Transparency and Consent
  Framework) before any ad is requested. <strong>No ad is requested and the
  advertising ID is not read until you have answered.</strong> Ads are
  personalised only if you agree to personalisation; otherwise any ad you see is
  non-personalised, chosen from the app and the screen it appears on.</li>
<li><strong>United States: opt out of targeted advertising.</strong> Where a US
  state privacy law gives you the right to opt out of the “sale” or “sharing” of
  personal information or of targeted advertising, Google's privacy form offers
  that choice; see <a href="#us-privacy">US state privacy notice</a>.</li>
{settings}<li><strong>Anywhere in the world</strong> you can reset or delete your
  advertising ID, or opt out of ads personalisation, in your phone's own settings
  (usually <strong>Settings → Privacy → Ads</strong>, or <strong>Settings →
  Google → Ads</strong>). Ads still appear, but they are not based on a profile of
  you.</li>
{remove}<li><strong>Children.</strong> No personalised advertising is shown to anyone
  we know to be under 13.</li>
</ul>
<p>Each network uses the information under its own privacy policy:
{_link(GOOGLE_PARTNERS, "How Google uses information from apps that use its services")}
· {_link(GOOGLE_PRIVACY, "Google Privacy Policy")}
· {_link(APPLOVIN_PRIVACY, "AppLovin Privacy Policy")}.</p>
"""


def legal_bases(app: dict) -> str:
    """GDPR Art. 6 bases, for the EEA, the UK and Switzerland."""
    future = app["ads"] == "future"
    rows = []
    if app["analytics"]:
        rows.append((
            "Anonymous usage statistics (Firebase Analytics)",
            "Your consent (Art. 6(1)(a)); in the EEA, the UK and Switzerland they "
            "stay off until you agree.",
        ))
    rows.append((
        "Advertising, including reading the advertising ID" + (
            " (in a version that shows ads)" if future else ""
        ),
        "Your consent (Art. 6(1)(a)), given in Google's consent form, for storing "
        "and reading information on your device and for personalised ads. You can "
        "withdraw it at any time, as easily as you gave it.",
    ))
    if app["purchases"]:
        rows.append((
            "Completing and restoring a purchase",
            "Performance of a contract with you (Art. 6(1)(b)). Google Play is the "
            "seller of record and processes the payment.",
        ))
    rows.append((
        "Keeping the app secure, preventing fraud and invalid ad traffic",
        "Our legitimate interests (Art. 6(1)(f)) in a working, honest app.",
    ))
    rows.append((
        "Answering your requests and meeting legal duties",
        "Legal obligation (Art. 6(1)(c)).",
    ))
    body = "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f"""<h2 id="legal-bases">Legal bases (EEA, UK and Switzerland)</h2>
<p>The data controller is {OWNER}, trading as {STUDIO}
({_link("mailto:" + EMAIL, EMAIL)}). Where the GDPR, the UK GDPR or the Swiss FADP
applies, we rely on these bases:</p>
<div class="tablewrap"><table>
<thead><tr><th>Purpose</th><th>Legal basis</th></tr></thead>
<tbody>
{body}
</tbody></table></div>
<p>No decision with a legal or similarly significant effect is made about you by
automated means.</p>
"""


def transfers(app: dict) -> str:
    """International transfers to the services that process data."""
    who = ["Google (Firebase Analytics and AdMob)" if app["analytics"] else "Google (AdMob)",
           "AppLovin"]
    if app["purchases"]:
        who.insert(1, "Google Play Billing")
    scope = (
        "" if app["ads"] == "live" or app["analytics"] else
        " This version sends nothing to them; this applies to any version that "
        "shows advertising."
    )
    return f"""<h2 id="transfers">Where data is processed</h2>
<p>{", ".join(who)} process data on servers in the United States and other
countries.{scope} Transfers from the EEA, the UK and Switzerland rely on the EU–US
Data Privacy Framework (and its UK and Swiss extensions) where the recipient is
certified under it, and otherwise on the European Commission's Standard
Contractual Clauses or an equivalent safeguard. {STUDIO} itself runs no server
that receives your data.</p>
"""


def us_notice(app: dict) -> str:
    """CCPA/CPRA and the other US state privacy laws."""
    future = app["ads"] == "future"
    qualifier = " in a version that shows ads" if future else ""
    rows = [(
        "Identifiers",
        "Advertising ID, IP address" + (", app instance ID (analytics)" if app["analytics"] else ""),
        "Ad networks (Google AdMob, AppLovin)" + (", Google Firebase" if app["analytics"] else ""),
        "Advertising ID and IP address: yes, when ads are personalised" + qualifier,
    ), (
        "Internet or other electronic network activity",
        "How ads performed" + ("; how the app is used" if app["analytics"] else ""),
        "Ad networks" + (", Google Firebase" if app["analytics"] else ""),
        "Ad interactions: yes, when ads are personalised" + qualifier
        + ("; app usage statistics: no" if app["analytics"] else ""),
    ), (
        "Geolocation data",
        "Approximate location inferred from IP address (never precise location)",
        "Ad networks" + (", Google Firebase" if app["analytics"] else ""),
        "Yes, when ads are personalised" + qualifier,
    ), (
        "Inferences",
        "Interests an ad network may infer to personalise ads",
        "Drawn by the ad network itself",
        "Yes, when ads are personalised" + qualifier,
    )]
    if app["purchases"]:
        rows.insert(2, (
            "Commercial information",
            "Which product was bought and the price shown (never card details)",
            "Google Play Billing" + (", Google Firebase" if app["analytics"] else ""),
            "No",
        ))
    body = "\n".join(
        f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows
    )
    current = (
        "<p><strong>This version collects none of these</strong>: it shows no ads"
        + (" and sends no analytics" if not app["analytics"] else "")
        + ". The table describes a version that shows ads.</p>\n"
        if future else ""
    )
    opt_out = (
        f"<strong>{app['ad_settings']}</strong> in the app (Google's privacy form), "
        if app["ad_settings"] else
        "the privacy form in the app (once it shows ads), "
    )
    return f"""<h2 id="us-privacy">US state privacy notice</h2>
<p>This notice is for residents of California (CCPA as amended by the CPRA) and of
the other US states with a comprehensive privacy law, including Colorado,
Connecticut, Delaware, Indiana, Iowa, Kentucky, Maryland, Minnesota, Montana,
Nebraska, New Hampshire, New Jersey, Oregon, Rhode Island, Tennessee, Texas, Utah
and Virginia.</p>
{current}<div class="tablewrap"><table>
<thead><tr><th>Category</th><th>Examples</th><th>Disclosed to</th><th>“Sold” or “shared”?</th></tr></thead>
<tbody>
{body}
</tbody></table></div>
<p><strong>We do not sell personal information for money.</strong> When ads are
personalised, letting an ad network use your advertising ID and related
information to target ads may count as “sharing” for cross-context behavioural
advertising (California) or as “targeted advertising” or a “sale” under other
state laws. <strong>To opt out</strong>, use {opt_out}or delete your advertising
ID or opt out of ads personalisation in your phone's settings, or email us. Ads
keep appearing, but they are no longer personalised. We collect no sensitive
personal information, and we do not knowingly sell or share the personal
information of anyone under 16.</p>
<p><strong>Your rights</strong> are to know what we collect and why, to access it,
to correct it, to delete it, and to opt out as above — without being treated
differently for exercising them. Because the app has no account, we hold nothing
that identifies you, so the quickest route to deletion is
<strong>{app['delete_path']}</strong>. To make any request, or to use an
authorised agent, email {_link("mailto:" + EMAIL, EMAIL)}; we answer within 45
days and will never ask for a password. If we decline a request you may appeal
by replying to our answer; if the appeal is declined you may contact your
state's Attorney General.</p>
<p><strong>Retention:</strong> see <a href="#data-retention">How long data is kept</a>.</p>
"""


def retention(app: dict) -> str:
    analytics = (
        "<li><strong>Firebase Analytics</strong> event data: 14 months, then Google "
        "deletes it automatically. Aggregate reports with no identifier attached may "
        "be kept longer.</li>\n" if app["analytics"] else ""
    )
    return f"""<h2 id="data-retention">How long data is kept</h2>
<ul>
<li><strong>On your device:</strong> until you delete it in the app or uninstall
  the app.</li>
{analytics}<li><strong>Advertising data</strong> is kept by each ad network under its own
  retention policy. Google, for example, anonymises advertising data in its logs
  by removing part of the IP address after 9 months and cookie information after
  18 months.</li>
<li><strong>Emails you send us</strong> are kept only as long as we need them to
  answer you, and deleted on request.</li>
</ul>
"""


def rights(app: dict) -> str:
    """The rights people have, by region, and how to use them."""
    analytics = (
        f" Switch analytics off in <strong>{app['analytics_off']}</strong>."
        if app["analytics_off"] else ""
    )
    return f"""<h2 id="your-rights">Your privacy rights, wherever you live</h2>
<p>Whatever the law where you live, you can ask us what we hold about you, ask us
to correct or delete it, and withdraw any consent you gave. Because the app has
no account, it holds nothing that identifies you personally, so in practice
<strong>{app['delete_path']}</strong> deletes everything the app keeps, on the
spot.{analytics} For anything else, email
{_link("mailto:" + EMAIL, EMAIL)}; we answer within 30 days (45 days for US state
requests) and never ask for a password.</p>
<ul>
<li><strong>EEA, UK and Switzerland</strong> (GDPR, UK GDPR, FADP): access,
  rectification, erasure, restriction, objection, data portability, and
  withdrawing consent at any time. You may complain to your data protection
  authority — in the EEA, {_link(EDPB, "your national authority")}; in the UK, the
  {_link("https://ico.org.uk/make-a-complaint/", "ICO")}; in Switzerland, the
  {_link("https://www.edoeb.admin.ch/", "FDPIC")}.</li>
<li><strong>United States</strong>: see the
  <a href="#us-privacy">US state privacy notice</a>.</li>
<li><strong>Brazil</strong> (LGPD): confirmation, access, correction,
  anonymisation, deletion, portability and information about sharing; complaints
  to the {_link("https://www.gov.br/anpd/", "ANPD")}.</li>
<li><strong>Canada</strong> (PIPEDA and Quebec's Law 25): access and correction;
  complaints to the
  {_link("https://www.priv.gc.ca/", "Office of the Privacy Commissioner")}.</li>
<li><strong>Elsewhere</strong> — including Australia, India, Japan, South Korea,
  Pakistan, Turkey, South Africa and the Gulf states — we honour the same requests
  under your local law, and you may complain to your local data protection
  authority.</li>
</ul>
"""


def children(app: dict) -> str:
    name = app["name"]
    future = app["ads"] == "future"
    if app["children"] == "all":
        audience = (
            f"<p>{name} is suitable for all ages and collects no personal "
            "information from anyone. If a future version shows advertising, any "
            "player who may be a child will be shown only non-personalised ads, "
            "requested as child-directed and from ad networks certified for Google "
            "Play's Families programme, as the Children's Online Privacy Protection "
            "Act (COPPA) and Google Play's Families policy require.</p>\n"
        )
    else:
        audience = (
            f"<p>{name} is not directed at children under 13, and its target "
            "audience in Google Play is 13 and over. We do not knowingly collect "
            "personal information from children under 13 (or under 16 in regions "
            "that set that age), and "
            + ("any version that shows ads" if future else "the app")
            + " never shows personalised advertising to anyone we know to be "
            "under 13.</p>\n"
        )
    return f"""<h2 id="children">Children</h2>
{audience}<p>If you believe a child has given us personal information, email
{_link("mailto:" + EMAIL, EMAIL)} and we will delete it.</p>
"""


SECTIONS = [
    ("advertising", advertising),
    ("legal-bases", legal_bases),
    ("transfers", transfers),
    ("retention", retention),
    ("us-privacy", us_notice),
    ("rights", rights),
    ("children", children),
]

# Sections a page replaced with the shared ones. Removed once, the first time
# the page is processed, so their content is not said twice.
RETIRED_HEADINGS = [
    r'<h2 id="ad-partners">Advertising partners</h2>',
    r'<h2 id="advertising">Advertising</h2>',
    r'<h2>Children</h2>',
    r'<h2>Children and guardians</h2>',
    r'<h2>Data retention</h2>',
]


def _strip_section(html: str, heading: str) -> str:
    """Removes one hand-written <h2> section, up to the next <h2> or marker."""
    start = html.find(heading)
    if start < 0:
        return html
    nxt = re.search(r"\n(<h2[ >]|<!-- shared:)", html[start + len(heading):])
    end = start + len(heading) + (nxt.start() + 1 if nxt else 0)
    return html[:start] + html[end:]


def render(slug: str, html: str) -> str:
    app = APPS[slug]
    begin_any = "<!-- shared:"
    if begin_any not in html:
        for heading in RETIRED_HEADINGS:
            html = _strip_section(html, heading)
        anchor = html.find('<h2 id="delete-your-data">')
        if anchor < 0:
            raise SystemExit(f"{slug}: no delete-your-data section to insert before")
        blocks = "".join(
            f"<!-- shared:{key}:begin -->\n<!-- shared:{key}:end -->\n\n"
            for key, _ in SECTIONS
        )
        html = html[:anchor] + blocks + html[anchor:]
    for key, build in SECTIONS:
        pattern = re.compile(
            rf"(<!-- shared:{re.escape(key)}:begin -->\n).*?(<!-- shared:{re.escape(key)}:end -->)",
            re.S,
        )
        if not pattern.search(html):
            raise SystemExit(f"{slug}: missing the shared:{key} markers")
        html = pattern.sub(lambda m: m.group(1) + build(app) + m.group(2), html)
    html = re.sub(
        r'(<p class="updated">Last updated: )[^·<]+( ·)', rf"\g<1>{UPDATED}\g<2>", html, count=1
    )
    return html


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for slug in APPS:
        path = ROOT / f"{slug}.html"
        old = path.read_text(encoding="utf-8")
        new = render(slug, old)
        if new != old:
            stale.append(slug)
            if not check:
                path.write_text(new, encoding="utf-8")
    if check and stale:
        print("stale: " + ", ".join(stale) + " -- run python3 tools/shared_sections.py")
        return 1
    print(("checked" if check else "wrote") + f" {len(APPS)} pages"
          + (f" ({len(stale)} changed)" if not check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
