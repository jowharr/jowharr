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
