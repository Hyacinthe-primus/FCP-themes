# Contributing a theme

Thanks for wanting to add a theme. You only need a text editor, a screenshot and a bit of patience with QSS. Python is optional, it just lets you check your work before opening a pull request.

## The short version

1. Fork this repo.
2. Copy `themes/theme_template` to `themes/Your_Theme_Name` and delete the `README.md` from your copy.
3. Edit `metadata.ini`, then restyle the QSS/CSS files.
4. Replace `preview.png` and add a full screenshot named `Your_Theme_Name.png`.
5. Open a pull request that only touches your folder.

Once it's merged, a workflow adds your theme to `themes.json`, builds the `.fctheme` and updates the README gallery. You don't do any of that yourself.

## 1. Start from the template

`themes/theme_template` is a complete, working theme: a copy of the built-in Light theme, with every widget already styled. Change the colours and details you care about instead of starting from an empty file. Its own [README](themes/theme_template/README.md) has the palette table and the selectors the optional files must style.

Copy the whole folder and rename it after your theme, with underscores instead of spaces. The folder name is used in URLs, so stick to letters, digits, `_` and `-`.

```
themes/
  Your_Theme_Name/
    metadata.ini
    preview.png
    Your_Theme_Name.png
    style.qss
    ... the other QSS/CSS files
```

## 2. Fill in `metadata.ini`

```ini
[theme]
name = Your Theme Name
author = Your name
version = 1.0.0
description = One or two sentences. Palette, mood, shapes.
kind = dark
preview = preview.png
```

| Field | Notes |
| --- | --- |
| `name` | Shown in the app and in `themes.json`. Must be unique in the repo. |
| `author` | Your name or GitHub handle. |
| `version` | Bump it when you update the theme. |
| `description` | Shown in the app and in `themes.json`. Keep it short. |
| `kind` | `dark` or `light`. The app uses it for things like the title bar and icons, so set it correctly even if your theme mixes both. |
| `preview` | The thumbnail shown in the theme picker. Leave it as `preview.png`. |

`name`, `description` and `author` are copied as they are into `themes.json`, so check the spelling.

## 3. Restyle the files

Each file styles one part of the app. These eleven are required. The app rejects an import if one is missing, and so do the checks here. Never rename them.

| File | What it styles |
| --- | --- |
| `style.qss` | The main window, buttons, inputs, group boxes, menus, dialogs and tooltips. Start here. |
| `advanced_conversions.qss` | The Advanced Conversions dialog. |
| `advanced_group.qss` | The checkable option groups. |
| `contact_links.css` | The contact and about links (HTML, so real CSS). |
| `dashboard.qss` | The statistics dashboard. |
| `lang_scroll.qss` | The language selector scroll area. |
| `scrollbar.qss` | Scrollbars. |
| `settings.qss` | The Settings dialog. |
| `templates.qss` | The Template Manager. |
| `terms.qss` | The Terms of Use and Privacy dialogs. |
| `terms_html.css` | The HTML content inside those dialogs (real CSS). |

Three more files are optional. If you remove them, the app falls back to its own dark or light stylesheet matching your `kind`:

| File | What it styles |
| --- | --- |
| `splash.qss` | The startup splash screen. |
| `window_card.qss` | The Quick Convert window opened from the Windows context menu. |
| `word_to_pdf.qss` | The Word to PDF options dialog preview (the text area and its scrollbars). |

They need specific selectors, listed in the template README. Keep them as they are unless you restyle those rules too, and check the splash, the Quick Convert window and the Word to PDF preview in the app.

Things worth knowing:

- QSS has no variables. Use find and replace on the palette values to recolour the template, then adjust individual rules.
- Dialogs don't inherit from the main window. Each dialog file needs to style its own widgets.
- The `.css` files are rendered by Qt's rich text engine, which supports only a subset of CSS. Test them in the app.
- Use fonts that ship with Windows, and always add a fallback (`'Segoe UI', sans-serif`). A font the user doesn't have silently falls back to the default.
- Only `.qss` and `.css` files are picked up. Don't add scripts, executables or anything that fetches remote content.

## 4. Add the images

You need two PNG files:

- **`preview.png`** is the small thumbnail shown in the theme picker. It is optional for the app, but please replace the template's with one of your own. It is packed inside the `.fctheme`.
- **`Your_Theme_Name.png`** is a full screenshot of the app with your theme applied. It is used in the README gallery and as the `image` in `themes.json`, and it is not packed in the `.fctheme`. Show the whole main window, and keep the file reasonably light (a PNG under 1 MB is plenty).

## 5. Test it

Build your archive and install it like any other theme:

```
python scripts/build_themes.py --pack Your_Theme_Name
```

This writes `themes/Your_Theme_Name.fctheme`. In File Converter Pro, go to **Settings**, **Themes**, **Install a theme (.fctheme)**, pick that file and apply it. Click through every screen and dialog, not only the main window. The dialogs are where themes usually break.

Then run the same check the pull request will run:

```
python scripts/build_themes.py --check
```

It fails if `metadata.ini` still has the template placeholders, a field is missing, `kind` isn't `dark` or `light`, one of the eleven required files is missing, a stylesheet has unbalanced braces, the preview or the screenshot is missing, or two themes share the same name. It needs Python 3.9 or newer and nothing else.

## 6. Open the pull request

Commit your theme folder and nothing else. Title the pull request `[create-theme]: <theme-name>` for a new theme, or `[update-theme]: <theme-name>` for a change. Please don't edit `themes.json` or the gallery in `README.md`. They are generated, and hand edits get overwritten.

Including the `.fctheme` in your pull request is optional. The workflow builds it anyway. The pull request description comes pre-filled with a checklist, please go through it.

A pull request needs:

- A passing `Themes` check.
- A screenshot of your theme in the PR description, if you can.
- Work that is yours, or that you have the right to share under the [MIT license](LICENSE) of this repo. If your theme is based on someone else's palette or design, say so in the description.

I'll review for readability (contrast, text that can't disappear into its background, hover and disabled states that are visible), coverage (all the files styled, dialogs included), and general polish. Feedback comes as review comments, so don't worry about getting it perfect on the first try.

## What happens after the merge

On every push to `main` that touches `themes/`, the `Themes` workflow runs `scripts/build_themes.py` and commits the result as `github-actions[bot]`:

- `themes.json` gets one entry per theme folder. The `id` is generated once and then never changes, `publish_date` is the date of the commit that first added the theme, and `widgets` is the list of its QSS/CSS files. `name`, `description` and `author` come from `metadata.ini`.
- `themes/<Name>.fctheme` is rebuilt if its content changed.
- The gallery in `README.md` is refreshed.
- Deleting a theme folder removes it from all of the above.

## Updating or removing a theme

To update your theme, change the files, bump `version` in `metadata.ini` and open a pull request. The `id` and the publish date stay the same. To remove it, delete its folder.

## Maintainers

The workflow pushes to `main` directly. If you protect that branch, allow `github-actions[bot]` to bypass the protection, or the generated commit will be rejected.
