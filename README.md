# NVE Weddings & Events – website

A single-page, black-and-white site (Weddings, Events, About, Book, Contact) in a Renaissance / Roman style.
No framework and no build step is needed to run it: `index.html` is the finished site.

## Quick start

1. Open `index.html` in a browser to preview it.
2. Upload `index.html` and the `img/` folder together to any static host (Netlify, Vercel, GitHub Pages, Cloudflare Pages, Squarespace/Wix custom code, or plain web hosting). Keep them side by side, because the page loads `img/…` by relative path.

## Folder contents

```
index.html            finished site (HTML, CSS and JS in one file)
img/
  hero-hands.jpg      home hero: hands and ring
  hero-arcade.jpg     Roman arcade strip (home hero and Events banner)
  rings.jpg           Weddings banner and Home panel
  arcade-side.jpg     Home panel for Events
  nve-logo-black.svg  logo, black on transparent (also .png)
  nve-logo-white.svg  logo, white on black (also .png)
source/
  index.template.html page source (placeholders for the logo, laurel and marble textures)
  build_site.py       fills the placeholders and writes ../index.html
  build_logo.py       draws the NVE monogram from the Cormorant Garamond font and writes the logo SVGs
  logo_symbol.svg     the monogram as an inline SVG symbol (used by build_site.py)
  fonts/              Cormorant Garamond 600 (SIL Open Font License), used only by build_logo.py
  artwork/            original ring-on-ring-finger illustration
```

Editing: for small text changes, edit `index.html` directly.
For bigger changes, edit `source/index.template.html`, then run `python3 source/build_site.py`.
To redraw the logo, install fontTools and Pillow (`pip install fonttools pillow`), then run `python3 source/build_logo.py` followed by `python3 source/build_site.py`.

## Settings (top of the script in index.html, search for `const CONFIG`)

| Setting | What it does |
|---|---|
| `studioEmail`, `studioPhone`, `studioLocation` | Shown on the Contact page when filled in. They are empty now. |
| `portraitSrc` | Path to your portrait for About Me, for example `img/portrait.jpg`. |
| `durationMinutes` | Length of a booking (60). |
| `open.days` | Bookable weekdays, 0 = Sunday … 6 = Saturday (currently Tuesday to Saturday). |
| `open.times` | Bookable start times (24-hour). |
| `open.minNoticeDays`, `open.horizonMonths` | Earliest and latest bookable dates. |
| `endpoint` | A form URL that receives submissions (see below). |

Placeholder text to replace before launch: service names, the "introductory consultation" wording, and the About Me copy.

## Booking and contact forms – important

The forms only save a request when there is somewhere to send it:

- Hosted as a Claude artifact: requests are stored in the artifact's database for signed-in Claude users. A visitor who is not signed in to Claude cannot submit, so this is not suitable for real public clients.
- Hosted anywhere else: set `endpoint` to a form service URL that accepts a JSON `POST`, such as Formspree, Basin, or a Zapier/Make webhook. Each booking or message is posted as JSON, and you receive it by email or in the service.
  - Booked times are not hidden from other visitors, and the site cannot stop two people requesting the same slot. Treat each booking as a request, then confirm it by email.
  - For real-time availability and confirmations, embed Calendly or Cal.com in the Book page instead.
- With neither of those, the page shows "Your request has not been sent" with a copy button. It never claims a request was sent when it was not.

## Notes

- Fonts (Cinzel and Cormorant Garamond) load from Google Fonts. Without a connection the page falls back to system serif fonts.
- Pages use `#weddings`, `#events`, `#about`, `#book`, `#contact` links.
  `#studio` is a private view of incoming requests, and it is useful only with the Claude artifact database.
- The images are black-and-white artwork. A higher-resolution version of the hero illustration would make the home page sharper on large screens.
