import os
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from constants import IMAGE_FOLDER, OUTPUT_PDF, NUM_CARDS, GRID_SIZE, VALID_EXTS

def get_image_paths(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(VALID_EXTS)]
    return files

def extract_winning_lines(grid):
    """
    Extracts all 12 winning lines as sorted tuples from image paths.
    """
    lines = []
    # 1. Rows
    for row in grid:
        lines.append(tuple(sorted(row)))
    # 2. Columns
    for col in range(GRID_SIZE):
        lines.append(tuple(sorted([grid[row][col] for row in range(GRID_SIZE)])))
    # 3. Diagonal 1
    lines.append(tuple(sorted([grid[i][i] for i in range(GRID_SIZE)])))
    # 4. Diagonal 2
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
        # check winning lines
        lines = extract_winning_lines(grid)
        # check if any of the winning lines have been used
        if any(line in used_winning_lines for line in lines):
            continue
        # If unique, add to used lines and cards
        for line in lines:
            used_winning_lines.add(line)
        cards.append(grid)

    print(f"Erfolgreich {len(cards)} einzigartige Bingokarten generiert!")
    return cards

def create_pdf(cards, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    # Layout
    margin = 15 * mm
    title_height = 20 * mm
    grid_area_width = page_width - 2 * margin
    grid_area_height = page_height - 2 * margin - title_height

    cell_size = min(grid_area_width / GRID_SIZE, grid_area_height / GRID_SIZE)
    start_x = margin + (grid_area_width - cell_size * GRID_SIZE) / 2
    start_y = margin + (grid_area_height - cell_size * GRID_SIZE) / 2

    for card_idx, card in enumerate(cards, start=1):
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, page_height - margin - 12 * mm, f"BINGO - Karte #{card_idx}")

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
                    c.drawImage(img_path, x + 1.5*mm, y + 1.5*mm, width=cell_size - 3*mm, height=cell_size - 3*mm, preserveAspectRatio=True)
                except Exception as e:
                    print(f"Fehler beim Laden von Bild {img_path}: {e}")
        c.showPage()
    c.save()
    print(f"PDF gespeichert unter: {output_path}")

if __name__ == "__main__":
    images = get_image_paths(IMAGE_FOLDER)
    if len(images) < 25:
        print("Fehler: Du benötigst mindestens 25 Bilder für ein 5x5 Bingo!")
    else:
        print(f"{len(images)} Bilder im Ordner gefunden.")
        bingo_cards = generate_unique_cards(images, NUM_CARDS)
        create_pdf(bingo_cards, OUTPUT_PDF)
