# Pickish - Photo Filter & Organizer

[![Build Status](https://github.com/apollyon600/pickish/workflows/Build%20Pickish%20Executable/badge.svg)](https://github.com/apollyon600/pickish/actions)
[![Release](https://img.shields.io/github/v/release/apollyon600/pickish)](https://github.com/apollyon600/pickish/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Pickish** is a powerful, user-friendly photo filtering and organization tool that helps you quickly sort through your photo collections using keyboard shortcuts and an intuitive interface.

## 🚀 Quick Start

### Download Latest Release
1. Go to [Releases](https://github.com/apollyon600/pickish/releases)
2. Download the latest `Pickish_vX.X.X.zip`
3. Extract and run `Pickish.exe`

### From Source
```bash
git clone https://github.com/apollyon600/pickish.git
cd pickish
pip install -r requirements.txt
python photo_filter_enhanced.py
```

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
- **Python 3.8+** (for development)
- **4GB RAM** minimum (8GB recommended for large photo collections)
- **500MB free disk space** for the application

## 🛠️ **Development**

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/apollyon600/pickish.git
cd pickish

# Install dependencies
pip install -r requirements.txt

# Run the application
python photo_filter_enhanced.py
```

### Building Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python -m PyInstaller pickish.spec --clean

# Or use the provided batch file
build_exe.bat
```

### Project Structure
```
pickish/
├── photo_filter_enhanced.py    # Main application
├── requirements.txt            # Python dependencies
├── pickish.spec               # PyInstaller configuration
├── README.md                  # This file
├── VERSION_HISTORY.md         # Version history
├── .github/workflows/         # GitHub Actions
│   ├── build.yml             # Build workflow
│   ├── test.yml              # Test workflow
│   └── release.yml           # Release workflow
└── .gitignore                # Git ignore rules
```

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

### Reporting Issues
1. Check existing issues first
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Submitting Changes
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to your fork: `git push origin feature/amazing-feature`
7. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update version number in `photo_filter_enhanced.py`
- Update `VERSION_HISTORY.md` with changes
- Test on Windows before submitting

## 📝 **Version History**

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for detailed version information.

### Latest Version (3.1.0)
- **NEW**: Love category for perfect photos
- **NEW**: Down arrow key for quick loving
- **NEW**: PERFECT folder organization
- **IMPROVED**: Four-button layout with Love button
- **ENHANCED**: Full undo support for all actions

## 🔧 **Troubleshooting**

### Common Issues

**App doesn't start:**
- Ensure you're running Windows 10/11
- Try running as administrator
- Check antivirus isn't blocking the file

**Photos don't display:**
- Supported formats: JPG, JPEG, PNG, BMP, TIFF, GIF, WEBP, HEIC, HEIF
- Check photos are in the selected input folder
- Verify photos aren't corrupted

**Performance issues:**
- Close other applications
- For large collections (1000+ photos), filter in smaller batches
- Ensure sufficient RAM (8GB recommended)

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