# Bingo Card & Presentation Suite

A Python desktop application & tool suite for generating custom Bingo cards from image collections, running an interactive Bingo caller, and presenting automated image slideshows.

---

## Overview

This project provides a complete setup for hosting visual Bingo games. It automates the creation of unique Bingo cards from image libraries and includes presentation tools to host the game on a screen.

The repository features two dedicated presentation modes: an interactive **Bingo Caller** (`random_image_selector.py`) that allows manually stepping through images after players check their cards, and an independent **Slideshow** (`diashow.py`) for displaying images automatically at fixed intervals.

---

## Features

- **Card Generator (`card_creator.py`):** Automatically selects and arranges images into custom printable Bingo grid layouts.
- **Interactive Bingo Caller (`random_image_selector.py`):** Manual fullscreen viewer controlled by keyboard inputs for live Bingo games.
- **Automated Slideshow (`diashow.py`):** Continuous, randomized image presentation with configurable display timers.
- **Central Configuration (`constants.py`):** Single location to configure image directory paths, layout dimensions, and display intervals.

---

## How to Use

- **Configure Settings:** Edit `src/constants.py` to set image folder locations, slideshow speed, or card dimensions.
- **Generate Cards:** Run `python src/card_creator.py` to process images and build formatted Bingo cards.
- **Host Bingo Game (Manual Caller):** Run `python src/random_image_selector.py` and use keyboard controls (`Space` / `Right Arrow` for next image, `Left Arrow` for previous, `Esc` to exit) to present drawn items at own pace.
- **Run Slideshow (Auto):** Run `python src/diashow.py` to display all images endlessly in random order with a fixed delay between transitions (reshuffles automatically when all images have been shown).

---

## Dependencies

- Python 3.11
- Pillow (PIL)
- ReportLab
- Tkinter (standard Python GUI library)

---

## Usage

```bash
conda env create -f environment.yml
conda activate bingo_creator

# start Card Generator
python src/card_creator.py

# start Interactive Bingo Caller
python src/random_image_selector.py

# start Automated Slideshow
python src/diashow.py
```
