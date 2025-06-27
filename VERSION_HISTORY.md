# Pickish - Version History

## Version 3.1.0 (Current)
**Date**: December 2024
**Status**: ✅ Stable

### New Features:
- **Love Category**: New "❤️ LOVE" button to mark photos as perfect
- **PERFECT Folder**: Loved photos are moved to a "PERFECT" subfolder
- **Down Arrow Key**: Press Down arrow to love the current photo
- **Love Statistics**: Track and display count of loved photos
- **Undo Support**: Love actions are fully undoable with Up arrow or Undo button

### UI Improvements:
- **Four-Button Layout**: Dislike | Undo | Like | Love button arrangement
- **Updated Instructions**: Shows all keyboard shortcuts including Down=Love
- **Love Counter**: Orange "Loved: X" counter in the statistics bar
- **Completion Stats**: Shows loved count in completion screen

### Technical Improvements:
- **Full Undo Integration**: Love actions work seamlessly with existing undo system
- **Consistent Workflow**: Love follows the same pattern as Like/Dislike actions
- **Button State Management**: Love button properly enabled/disabled with other buttons
- **Move Queue Support**: Loved photos are processed through the same background move system

### Keyboard Shortcuts:
- **Left Arrow**: Skip/Dislike photo
- **Right Arrow**: Like photo  
- **Down Arrow**: Love photo (NEW)
- **Up Arrow**: Undo last action
- **Space**: Like photo

---

## Version 2.1.0 (Previous)
**Date**: December 2024
**Status**: ✅ Stable

### New Features:
- **Skipped Photos Tracking**: Photos you skip are now tracked separately in a dedicated list
- **Review Skipped Photos**: New "Review Skipped" button to review only previously skipped photos
- **Reset Skipped Photos**: New "Reset Skipped" button to put all skipped photos back in the main pool
- **Mode Indicator**: Shows when you're reviewing skipped photos vs. normal filtering
- **Smart Button States**: Review/Reset buttons are disabled when no photos are skipped

### Workflow Improvements:
- **Separate Review Mode**: You can now review skipped photos without affecting the main photo list
- **Flexible Workflow**: Skip photos during initial review, then review them separately later
- **Reset Capability**: Put skipped photos back into the main pool for re-evaluation
- **Better Statistics**: Shows actual count of skipped photos in separate list

### Technical Improvements:
- **Separate Photo Lists**: Main photos and skipped photos are tracked independently
- **Mode Management**: Clear distinction between normal filtering and skipped review modes
- **Dynamic Button States**: Buttons enable/disable based on available actions
- **Improved UX**: Better feedback about current mode and available actions

---

## Version 2.0.1 (Previous)
**Date**: December 2024
**Status**: ✅ Stable

### New Features:
- **Configuration Cache**: Input and output folders are automatically saved and restored
- **Top Statistics Bar**: Moved statistics to the top of the window for better visibility
- **Version Display**: Application title shows current version
- **Surface Pro Optimization**: Larger buttons and better touch interaction
- **Improved Image Display**: Better handling of vertical images (800x800px max)

### Bug Fixes:
- **Fixed UI Layout**: Resolved issues with non-interactive interface
- **Fixed Button Visibility**: Like/Dislike buttons now properly display and function
- **Fixed Vertical Images**: Images now display in their natural orientation with EXIF auto-rotation
- **Fixed Statistics Updates**: Real-time counter updates work correctly

### Technical Improvements:
- **JSON Configuration**: Persistent settings using `pickish_config.json`
- **Better Error Handling**: Improved error messages and recovery
- **Responsive Design**: Optimized for Surface Pro and touch devices
- **Code Organization**: Better structured and more maintainable

---

## Version 1.0.0 (Initial Release)
**Date**: December 2024
**Status**: ❌ Deprecated (UI issues)

### Features:
- Basic photo filtering functionality
- Date-based sorting (newest first)
- Keyboard shortcuts (arrow keys)
- Progress tracking
- Multiple photo format support

### Issues:
- UI layout problems causing non-interactive interface
- Missing or non-functional buttons
- Vertical images displayed incorrectly
- No configuration persistence

---

## Installation & Usage

### Requirements:
- Python 3.8 or higher
- Pillow library (`pip install Pillow`)

### Running:
```bash
python photo_filter_enhanced.py
```

### Configuration:
- Settings are automatically saved to `pickish_config.json`
- Previous folder selections are restored on startup

### New Workflow (v3.1.0):
1. **Start Filtering**: Review all photos in the input folder
2. **Skip Photos**: Use "👎 DISLIKE" to skip photos you're unsure about
3. **Like Photos**: Use "👍 LIKE" to move photos to FINAL folder
4. **Love Photos**: Use "❤️ LOVE" to move photos to PERFECT folder (NEW)
5. **Undo Actions**: Use "↶ UNDO" or Up arrow to undo any action
6. **Review Skipped**: Click "Review Skipped" to review only the skipped photos
7. **Reset if Needed**: Use "Reset Skipped" to put skipped photos back in main pool

---

## Known Issues:
- None currently reported

## Planned Features:
- Batch processing options
- Custom keyboard shortcuts
- Image preview thumbnails
- Export/import settings
- Additional categorization options 