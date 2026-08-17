import os
import random
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from constants import IMAGE_FOLDER, OUTPUT_PDF, NUM_CARDS, GRID_SIZE, VALID_EXTS

def get_image_paths(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(VALID_EXTS)]
    return files

def extract_winning_lines(grid):
    """
    Extracts all 12 winning lines as sorted tuples from image paths.
    """
    lines = []
    # rows
    for row in grid:
        lines.append(tuple(sorted(row)))
    # columns
    for col in range(GRID_SIZE):
        lines.append(tuple(sorted([grid[row][col] for row in range(GRID_SIZE)])))
    # diagonal 1
    lines.append(tuple(sorted([grid[i][i] for i in range(GRID_SIZE)])))
    # diagonal 2
    lines.append(tuple(sorted([grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)])))
    return lines

def generate_unique_cards(all_images, num_cards):
    used_winning_lines = set()
    cards = []
    attempts = 0
    max_attempts = 100000
    while len(cards) < num_cards and attempts < max_attempts:
        attempts += 1
        # 25 random images
        selected = random.sample(all_images, GRID_SIZE * GRID_SIZE)
        # 5x5 grid
        grid = [selected[i * GRID_SIZE : (i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
        # get winning lines
        lines = extract_winning_lines(grid)
        # check if any of the winning lines have been used
        if any(line in used_winning_lines for line in lines):
            continue
        # if unique, add to used lines and cards
        for line in lines:
            used_winning_lines.add(line)
        cards.append(grid)
    print(f"Successfully generated {len(cards)} unique bingo cards (after {attempts} attempts).")
    return cards

def create_pdf(cards, output_path):
    unique_paths = set()
    for card in cards:
        for row in card:
            for img_path in row:
                unique_paths.add(img_path)
    # downscale images
    image_cache = {}
    print(f"Preparing {len(unique_paths)} unique images for PDF...")
    for idx, path in enumerate(unique_paths, start=1):
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                img_copy = img.convert("RGB")
                img_copy.thumbnail((400, 400))
                image_cache[path] = ImageReader(img_copy)
        except Exception as e:
            print(f"Fehler bei Bild {path}: {e}")
            image_cache[path] = None
        if idx % 10 == 0 or idx == len(unique_paths):
            print(f"   -> {idx}/{len(unique_paths)} images prepared...")

    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4
    # Layout
    margin = 10 * mm
    title_height = 15 * mm
    grid_area_width = page_width - 2 * margin
    grid_area_height = page_height - 2 * margin - title_height

    cell_size = min(grid_area_width / GRID_SIZE, grid_area_height / GRID_SIZE)
    start_x = margin + (grid_area_width - cell_size * GRID_SIZE) / 2
    start_y = margin + (grid_area_height - cell_size * GRID_SIZE) / 2

    print(f"Creating PDF with {len(cards)} cards...")
    for card_idx, card in enumerate(cards, start=1):
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, page_height - margin - 12 * mm, f"Geburtstagsbingo - Karte #{card_idx}")

        # draw 5x5 grid
        for r in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                img_path = card[r][col]
                # calculate coordinates
                x = start_x + col * cell_size
                y = start_y + (GRID_SIZE - 1 - r) * cell_size
                # draw rectangle
                c.rect(x, y, cell_size, cell_size)
                # paste images
                try:
                    cached_img = image_cache.get(img_path)
                    if cached_img:
                        c.drawImage(cached_img, x + 1*mm, y + 1*mm,
                                    width=cell_size - 2*mm, height=cell_size - 2*mm,
                                    preserveAspectRatio=True)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
        if card_idx % 10 == 0 or card_idx == len(cards):
            print(f"   -> page {card_idx}/{len(cards)} created...")
        c.showPage()
    c.save()
    print(f"PDF saved to: {output_path}")

if __name__ == "__main__":
    images = get_image_paths(IMAGE_FOLDER)
    if len(images) < 25:
        print("Error: at least 25 images required")
    else:
        print(f"{len(images)} images found.")
        bingo_cards = generate_unique_cards(images, NUM_CARDS)
        create_pdf(bingo_cards, OUTPUT_PDF)
