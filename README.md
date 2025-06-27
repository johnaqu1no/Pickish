# Pickish - Photo Filter & Organizer

**Last updated:** June 2024

[![Build Status](https://github.com/apollyon600/pickish/workflows/Build%20Pickish%20Executable/badge.svg)](https://github.com/apollyon600/pickish/actions)
[![Release](https://img.shields.io/github/v/release/apollyon600/pickish)](https://github.com/apollyon600/pickish/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Pickish** is a powerful, user-friendly photo filtering and organization tool that helps you quickly sort through your photo collections using keyboard shortcuts and an intuitive interface.

## 🚀 Quick Start

### Download Latest Release
1. Go to [Releases](https://github.com/apollyon600/pickish/releases)
2. Download the latest `Pickish.exe` file
3. Double-click to run (no installation required)

> **Note:** Only the `.exe` file is distributed now. All documentation and instructions are available on the [GitHub repository](https://github.com/apollyon600/pickish).

## ✨ Features

### 📸 **Three-Category Organization**
- **❤️ LOVE** → Moves photos to "PERFECT" folder (your absolute favorites)
- **👍 LIKE** → Moves photos to "FINAL" folder (good photos)
- **👎 DISLIKE** → Moves photos to "SKIPPED" folder (photos to review later)

### ⌨️ **Keyboard Shortcuts**
- **Left Arrow**: Skip/Dislike photo
- **Right Arrow**: Like photo  
- **Down Arrow**: Love photo
- **Up Arrow**: Undo last action
- **Space**: Like photo

### 🔄 **Smart Features**
- **Undo Support**: Undo any action with Up arrow or Undo button
- **Auto-rotation**: Vertical images display correctly with EXIF data
- **Progress Tracking**: See your progress through the photo collection
- **Background Processing**: Smooth performance with large photo collections
- **Configuration Memory**: Remembers your folder selections
- **Move Queue**: Sequential file operations to prevent conflicts

## 📁 **Folder Structure**

After filtering, your photos will be organized into:

```
Your Input Folder/
├── FINAL/          (Liked photos)
├── PERFECT/        (Loved photos - your favorites)
├── SKIPPED/        (Disliked photos - for later review)
└── [remaining photos to filter]
```

## 🎯 **Workflow**

1. **Select Input Folder**: Choose the folder containing your photos
2. **Start Filtering**: Click "Start Filtering" to begin
3. **Quick Decisions**: Use arrow keys for fast filtering
4. **Review Skipped**: Later, review photos in the SKIPPED folder
5. **Perfect Organization**: Your best photos end up in PERFECT folder

## 💻 **System Requirements**

- **Windows 10/11** (64-bit)
- **No Python installation required** - everything is included!
- **Minimum 4GB RAM** (8GB recommended for large photo collections)
- **500MB free disk space** for the application

## 🔧 **Troubleshooting**

### If the app doesn't start:
- Make sure you're running Windows 10 or 11
- Try running as administrator
- Check that your antivirus isn't blocking the file

### If photos don't display:
- Supported formats: JPG, JPEG, PNG, BMP, TIFF, GIF, WEBP, HEIC, HEIF
- Make sure photos are in the selected input folder
- Check that photos aren't corrupted

### Performance tips:
- Close other applications for better performance
- For very large collections (1000+ photos), consider filtering in smaller batches

## 📝 **Version History**

See [GitHub Releases](https://github.com/apollyon600/pickish/releases) for version information.

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Built with Python and Tkinter
- Image processing with Pillow (PIL)
- Executable packaging with PyInstaller
- Automated builds with GitHub Actions

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/apollyon600/pickish/issues)
- **Discussions**: [GitHub Discussions](https://github.com/apollyon600/pickish/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/apollyon600/pickish/wiki)

---

**Enjoy organizing your photos with Pickish!** 📸✨

[⬆ Back to top](#pickish---photo-filter--organizer) 