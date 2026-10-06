# Profile artwork

The README uses original, self-contained SVG images. The dark card layout is
inspired by [Alan Thomas Shaji's profile](https://github.com/alan-thomas-shaji),
and the terminal is inspired by the neofetch-style screenshot supplied for this
profile. The ASCII portrait is sampled directly from Jowhar’s supplied photo.

## Updating the artwork

Edit the profile text in scripts/generate_assets.py and the toolkit in
scripts/generate_stack.py, then run:

~~~sh
python3 scripts/generate_assets.py
~~~

Commit the regenerated assets/*.svg files with the README. No build service,
API token, downloaded font, package installation, or scheduled job is needed.
Keep the ordinary Markdown text and image descriptions in sync when changing
profile content.

## Animation and accessibility

The terminal reveals its rows from top to bottom in about 3.6 seconds on desktop and 4.3 seconds on mobile, then holds
the completed image. The animation runs when the SVG image loads; returning via
GitHub navigation or the browser's back button may reuse a finished image.
GitHub READMEs cannot control page navigation or run JavaScript.

Animation is enabled only when prefers-reduced-motion: no-preference matches.
Reduced-motion readers and renderers without CSS animation support see the
complete artwork immediately. A normal picture element selects a dedicated
mobile composition at viewport widths of 600px or less. Real contact links and
the text version of the toolkit remain in Markdown because links inside an
SVG used as an image are not interactive.

## Content

The toolkit combines the existing public README with the user's earlier
portfolio brief. Learning topics are shown as “Currently exploring,” without
expertise ratings. GitHub statistics are not hardcoded into the terminal.

## Portrait

The portrait is native SVG text rendered from assets/portrait.txt, with no
external image dependency. It is derived directly from the supplied photo,
without generating or changing facial features. The original photo and its
metadata are not stored in this repository.

To update it from another photo, decode a temporary BMP with macOS sips, then run
scripts/photo_to_ascii.py with the BMP path and an appropriate --crop rectangle
(left, top, width, height). Run scripts/generate_assets.py afterward. The mobile
terminal places the same portrait above the profile text.

## Reference-aligned layout

The centered glowing hero, compact floating technology badges,
exploring pills, contact buttons, and footer follow the visual direction of
[the reference repository](https://github.com/alan-thomas-shaji/alan-thomas-shaji).
The portrait data and its top-to-bottom reveal are retained.

The user explicitly selected the reference's six "Currently exploring" topics.
They describe interests rather than proficiency.

Edit scripts/generate_focus.py to change those topics. The shared generator
rebuilds both desktop and mobile focus cards, plus the contact assets.

Current public contact: jowhar.dev@gmail.com.
Current portfolio: https://portfolio-jowhar.vercel.app/.

## GitHub activity

The streak image is supplied by
[GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats).
It displays total contributions, the current daily streak, and the longest
streak. It uses the public jowharr profile; no token is included in the README.
The hosted service and GitHub's image cache determine refresh timing, so updates
are not instantaneous. The card has no profile-overview link, which avoids navigating back to the top of the same profile.

This remote statistics card is separate from the self-contained local artwork.
The originally considered activity-graph endpoint returned HTTP 402 during
verification, so it is not embedded.

## Card motion

The technology chips and exploring topics have staggered entrance animations,
bright traveling border accents, pulsing borders, and soft indicator halos. Motion is
restricted to decorative details; labels stay readable after their entrance.
All effects are inside the no-preference reduced-motion media query, leaving
a static, fully visible composition for readers who prefer less motion.
The ASCII portrait retains its original top-to-bottom reveal.

The reading order is hero, profile.sh portrait terminal, then tech stack.
The chip and topic border accents loop every 3.2 seconds so their motion stays
visible after the initial entrance. Labels remain stationary. The trace overlays
are hidden when reduced motion is requested, leaving the static base borders.
