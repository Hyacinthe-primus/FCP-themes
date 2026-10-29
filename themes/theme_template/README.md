# Custom theme starter

This folder is a complete, working theme you can copy instead of starting from
an empty file. It is a copy of the built-in **Light** theme: every widget is
already styled, so you only need to change the colors and details you care
about.

It lives outside `custom_themes/` on purpose, so the app does not list it in
the theme picker.

---

## Quick start

1. Copy this whole `theme_template` folder into `styles/custom_themes/`.
2. Rename the copy to your theme, for example `Ocean`.
3. Edit `metadata.ini`: set `name`, `author`, `version`, `description`, and
   `kind` (`light` or `dark`).
4. Recolor the `.qss` files. Start with `style.qss`; the other files cover
   specific screens.
5. Restart the app, open **Settings -> Themes**, and select your theme.

For development, the folders are `src/styles/theme_template/` and
`src/styles/custom_themes/`. In an installed app they are under
`styles/theme_template/` and `styles/custom_themes/`.

---

## Palette used by this starter

| Token | Default | Used for |
|-------|---------|----------|
| Background | `#f6f8fa` | Window and panel backgrounds |
| Surface | `#ffffff` | Cards, lists, inputs |
| Border | `#d0d7de` | Cards, separators, inputs |
| Text | `#1f2328` | Primary text |
| Text muted | `#57606a` | Hints, secondary labels |
| Accent | `#0969da` | Buttons, selection, progress |
| Accent strong | `#1d4ed8` | Hover, checked states |
| Danger | `#b91c1c` | Errors and warnings |
| Success | `#10b981` | Success messages and badges |

Find/replace these values across the theme files to recolor the whole theme
quickly, then adjust individual rules.

---

## Dashboard palette overrides

`metadata.ini` can include an optional `[dashboard]` section to give the
statistics dashboard explicit colors instead of deriving them from
`dashboard.qss`:

```ini
[dashboard]
background = #f0f2f7
surface = #ffffff
surface_alt = #f7faff
border = #dde3ec
text = #1a202c
muted = #4a5568
accent = #2b6cb0
accent_text = #2b6cb0
```

| Key | Used for |
|-----|----------|
| `background` | Dashboard window background |
| `surface` | Cards, tables, chart and filter panels |
| `surface_alt` | Stat-card tracks, section headers, alternate rows |
| `border` | Card, table and panel borders |
| `text` | Primary chart and table text |
| `muted` | Secondary labels, ticks and hints |
| `accent` | Chart bars, donut segments, progress and highlights |
| `accent_text` | Accent-colored text on surfaces (stat values, section titles) |

`accent_text` is separate so a bright accent such as yellow can stay on bars
while readable dark gold or navy is used for text. If the section is omitted,
the app derives the palette from the theme's `dashboard.qss` instead. Missing
or invalid keys fall back to the derived value.

---

## Required files

A `.fctheme` import is rejected if any of these files is missing:

| File | What it styles |
|------|----------------|
| `style.qss` | Main window, buttons, inputs, group boxes, menus, dialogs, tooltips |
| `advanced_conversions.qss` | Advanced Conversions dialog |
| `advanced_group.qss` | Checkable option groups |
| `contact_links.css` | Contact/about links (HTML) |
| `dashboard.qss` | Statistics dashboard |
| `lang_scroll.qss` | Language selector scroll area |
| `scrollbar.qss` | Scrollbars |
| `settings.qss` | Settings dialog |
| `templates.qss` | Template Manager |
| `terms.qss` | Terms of Use and Privacy dialogs |
| `terms_html.css` | HTML content inside Terms/Privacy |

## Optional files

These five are used automatically when present. If you delete them, the app
falls back to the dark/light stylesheet that matches `kind`.

| File | What it styles |
|------|----------------|
| `splash.qss` | Startup splash screen |
| `window_card.qss` | Quick Convert window opened from the Windows context menu |
| `word_to_pdf.qss` | Word to PDF options dialog preview |
| `buttons.qss` | Shared dialog action buttons |
| `achievements.qss` | Achievements dialog, cards, progress widgets and unlock popups |

`splash.qss` must style `QFrame#SplashContainer`, `QLabel#SplashLogo`,
`QLabel#SplashTitle`, `QLabel#SplashSubtitle`, `QProgressBar#SplashProgress`,
`QProgressBar#SplashProgress::chunk`, and `QLabel#SplashProgressText`.

`window_card.qss` must style `#card`, `#title`, `#fileList`, `#separator`,
`QComboBox`, `QComboBox QAbstractItemView` (including a readable
`selection-color`), `QPushButton#convertBtn`, `QPushButton#cancelBtn`,
`QProgressBar`, `#statusOk`, `#statusErr`, and `#conversionLabel`.

`word_to_pdf.qss` must style `QTextEdit` and its vertical and horizontal
`QScrollBar` parts (`:vertical`, `::handle:vertical`, `:horizontal`,
`::handle:horizontal`). Keep the preview text readable against the background.

`buttons.qss` must style the shared action buttons, including their hover,
pressed and disabled states: `QPushButton#BtnOK`, `QPushButton#BtnCancel`,
`QPushButton#BtnDecline`, `QPushButton#BtnIndigo`, `QPushButton#BtnGhost`,
`QPushButton#BtnClose`, `QPushButton#BtnCancelGlassy`,
`QPushButton#BtnReconvert`, `QPushButton#BtnPrintPdf`,
`QPushButton#BtnExportJson`, `QPushButton#BtnDeleteSelection`,
`QPushButton#BtnClearAll`, `QPushButton#BtnHistoryClose`,
`QPushButton#BtnFolderAsItem`, and `QPushButton#BtnFolderContent`.

`achievements.qss` starts with an `AchievementsPalette { ... }` block. The app
reads that block for the custom-painted XP ring, achievement cards, rank badge
and stat bars; the rest of the file styles the dialog and popups. Keep the
palette keys and update them with the theme colors. The main selectors are
`QDialog#AchievementsDialog`, `QFrame#AchievementsHeader`,
`QLabel#AchievementsHeaderTitle`, `QLabel#AchievementsHeaderChip`,
`QPushButton#AchievementsNavPill`, `QTreeWidget#AchievementsCategoryTree`,
`QFrame#AchievementsFilterBar`, `QComboBox#AchievementsFilter`,
`QLineEdit#AchievementsSearch`, `QPushButton#AchievementsSecretsButton`,
`QGroupBox#AchievementsGroup`, `QPushButton#AchievementsCloseButton`,
`QFrame#AchievementPopupContainer`, `QFrame#RankPopupContainer`, and the
`AchievementPopup*` / `RankPopup*` labels. See the template file for the full
list and the palette keys.

The palette block also controls the painted details: `font_family`,
`ring_track`, `ring_progress`, `ring_glow`, `ring_tip`, `ring_complete`,
`progress_track`, `progress_fill`, `progress_fill_end`, `stat_track`,
`card_sheen`, `card_shadow`, `tier_<id>`, `tier_<id>_glow`,
`tier_<id>_hover`, `category_<id>`, and `rank_<id>`. Rank ids are `rookie`,
`initiate`, `adept`, `veteran`, `elite`, `champion`, `master`,
`grand_master`, `legendary`, and `mythic`. The file is loaded when the
achievements dialog opens, so editing it and reopening the dialog is enough;
no app rebuild is needed.

---

## Packaging as .fctheme

A `.fctheme` file is a ZIP archive of the theme folder:

1. Zip the folder that contains `metadata.ini` (not its parent).
2. Rename the archive to `<ThemeName>.fctheme`.
3. Import it from **Settings -> Themes**.

---

## Tips

- `kind` controls dark/light behavior such as the title bar and icons. Set it
  correctly even if your theme is a mix.
- QSS has no variables: use find/replace to keep the palette consistent.
- `preview.png` is optional and shown in the theme picker; replace it with a
  screenshot of your theme.
- Never rename the required files; import validation matches exact names.
