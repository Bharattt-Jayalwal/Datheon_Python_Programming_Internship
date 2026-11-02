
import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# File extension categories
FILE_TYPES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",

    ".py": "Code",
    ".java": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".cpp": "Code",
    ".c": "Code"
}

# Create a log file beside this Python script
LOG_FILE = Path(__file__).resolve().parent / "organizer.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_unique_path(destination):
    """Avoid overwriting files with the same name."""

    if not destination.exists():
        return destination

    folder = destination.parent
    stem = destination.stem
    extension = destination.suffix
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{extension}"
        new_path = folder / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):
    """Organize files into extension-based folders."""

    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print("Error: The selected folder does not exist.")
        return

    moved = 0
    skipped = 0
    failed = 0

    print("\n========== FILE ORGANIZER ==========")
    print(f"Selected folder: {folder}")
    print("Starting file organization...\n")

    try:
        # Inspect files in the selected directory
        for entry in os.scandir(folder):

            # Skip directories and symbolic links
            if not entry.is_file(follow_symlinks=False):
                continue

            source = Path(entry.path)

            # Find category using file extension
            category = FILE_TYPES.get(
                source.suffix.lower(),
                "Others"
            )

            try:
                # Create category folder automatically
                destination_folder = folder / category
                destination_folder.mkdir(exist_ok=True)

                # Generate a unique filename if needed
                destination = get_unique_path(
                    destination_folder / source.name
                )

                # Move the file
                shutil.move(str(source), str(destination))

                moved += 1

                message = f"Moved: {source.name} -> {category}"
                print(message)
                logging.info(message)

            except PermissionError:
                skipped += 1
                print(f"Permission denied: {source.name}")
                logging.warning(f"Permission denied: {source}")

            except FileExistsError:
                failed += 1
                print(f"File already exists: {source.name}")
                logging.error(f"File already exists: {source}")

            except OSError as error:
                failed += 1
                print(f"Could not move {source.name}: {error}")
                logging.error(f"Move failed for {source}: {error}")

    except PermissionError:
        print("Cannot access the selected directory.")
        logging.error(f"Cannot access directory: {folder}")
        return

    except OSError as error:
        print(f"Directory error: {error}")
        logging.error(f"Directory error: {error}")
        return

    # Display final summary
    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files successfully moved : {moved}")
    print(f"Files skipped            : {skipped}")
    print(f"Files failed             : {failed}")
    print(f"Log saved at             : {LOG_FILE}")
    print("==========================================")

    logging.info(
        f"Completed. Moved={moved}, "
        f"Skipped={skipped}, Failed={failed}"
    )


def main():
    print("STUDENT AUTOMATED FILE ORGANIZER")
    print("--------------------------------")

    default_folder = Path.home() / "Downloads"

    print(f"Default folder: {default_folder}")

    folder_path = input(
        "\nEnter folder path (press Enter for Downloads): "
    ).strip()

    if not folder_path:
        folder_path = str(default_folder)

    organize_files(folder_path)


if __name__ == "__main__":
    main()
