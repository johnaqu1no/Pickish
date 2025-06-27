# Pickish - Photo Filter & Organizer

A modern Windows application for photographers to quickly filter through their photos and organize them into selected folders.

## Features

- **Recursive Photo Scanning**: Automatically finds all photos in the selected input folder and its subfolders
- **Date-Based Sorting**: Photos are sorted by modification date (newest first) for efficient review
- **Multiple Format Support**: Supports JPG, JPEG, PNG, BMP, TIFF, GIF, WebP, HEIC, and HEIF formats
- **Intuitive Interface**: Clean, modern UI with easy-to-use controls
- **Real-Time Statistics**: Live count of liked and skipped photos
- **Multiple Input Methods**: 
  - Click buttons for Like/Dislike
  - Use keyboard shortcuts (Left arrow = Like, Right arrow = Dislike, Space = Like)
- **Progress Tracking**: Visual progress bar and photo counter
- **Duplicate Handling**: Automatically handles duplicate filenames in the output folder
- **Error Handling**: Graceful handling of corrupted or unsupported image files
- **Date Information**: Shows modification date for each photo

## Installation

1. **Install Python** (if not already installed):
   - Download Python 3.8 or higher from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**:
   ```bash
   python photo_filter.py
   ```
   Or use the batch files:
   - `run_pickish.bat` (basic version)
   - `run_pickish_enhanced.bat` (enhanced version)

2. **Select Folders**:
   - Click "Browse" next to "Input Folder" to select the folder containing your photos
   - Click "Browse" next to "Output Folder" to select where you want to move your liked photos

3. **Start Filtering**:
   - Click "Start Filtering" to begin the photo review process
   - The app will scan all photos in the input folder (including subfolders)
   - Photos are automatically sorted by modification date (newest first)

4. **Review Photos**:
   - **Like a photo**: Click the "👍 Like" button, press Left arrow key, or press Space
   - **Dislike a photo**: Click the "👎 Dislike" button or press Right arrow key
   - Photos you like will be moved to your selected output folder
   - Real-time counters show your progress

5. **Completion**:
   - When you've reviewed all photos, you'll see a completion message with final statistics
   - Click "Start New Session" to begin filtering another folder

## Keyboard Shortcuts

- **Left Arrow** or **Space**: Like the current photo (moves it to output folder)
- **Right Arrow**: Dislike the current photo (leaves it in place)

## Supported Photo Formats

- JPG/JPEG
- PNG
- BMP
- TIFF/TIF
- GIF
- WebP
- HEIC/HEIF

## Features Overview

### **Date Sorting**
Photos are automatically sorted by modification date, showing the newest photos first. This helps you review your most recent work efficiently.

### **Real-Time Statistics**
- **Current Count**: Shows which photo you're viewing (e.g., "Photo 5 of 25")
- **Liked Count**: Tracks how many photos you've liked so far
- **Skipped Count**: Tracks how many photos you've disliked/skipped
- **Progress Bar**: Visual representation of your progress through the collection

### **Simple Controls**
- **Like Button**: Green button with thumbs up emoji
- **Dislike Button**: Red button with thumbs down emoji
- **Keyboard Shortcuts**: Quick navigation without using the mouse

## Tips

- The app automatically handles duplicate filenames by adding a number suffix
- Photos are displayed at a maximum size of 600x400 pixels for optimal viewing
- You can see the current photo's filename and modification date below the image
- The progress bar shows your progress through the photo collection
- The app creates the output folder automatically if it doesn't exist
- Photos are sorted by modification date, so you'll see your newest photos first

## Troubleshooting

**"No photos found" error**: Make sure your input folder contains supported image files and that the folder path is correct.

**"Failed to move photo" error**: This usually occurs if the photo is currently open in another application. Close any applications that might be using the photo and try again.

**Image loading errors**: Some image formats might not be supported or the file might be corrupted. The app will skip these files and continue with the next photo.

## System Requirements

- Windows 10 or later
- Python 3.8 or higher
- At least 4GB RAM (recommended for large photo collections)
- Sufficient disk space for your photo collection

## License

This project is open source and available under the MIT License. 