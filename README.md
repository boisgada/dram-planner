# Dram Planner 🥃

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python-based system for managing your spirits collection and creating a structured 2-year tasting schedule. **The only free application that offers scheduling functionality for spirits tastings!**

## ✨ Features

- 📅 **Tasting Schedule Generation** - Automatically create customizable tasting schedules
- ⚙️ **User Preferences** - Customize frequency, preferred days, avoid dates, category preferences, and seasonal adjustments
- 📊 **Collection Management** - Track your entire spirits collection in one place
- 📝 **Tasting Notes** - Record detailed notes and ratings for each tasting
- 📈 **Progress Tracking** - Monitor your progress by category and overall
- 🎯 **Smart Scheduling** - Prioritizes untasted bottles and ensures category variety
- 💻 **CLI Interface** - Powerful command-line tools for all operations
- 📥 **Multiple Import Formats** - Import from CSV, JSON, or Excel files
- 📷 **Barcode Scanning** - Automatic bottle lookup via barcode/UPC scanning
- 🆓 **100% Free** - No subscriptions, no limitations, completely open-source

## 🚀 Quick Installation

1. **Clone or download** this repository
2. **No installation required!** Just ensure you have Python 3.6+ installed
3. **Start using immediately** - no dependencies, no setup needed

```bash
# Check Python version
python3 --version  # Should be 3.6 or higher

# That's it! You're ready to go.
```

## 📋 Requirements

- **Python 3.6+** (core functionality uses only standard library)
- **Optional Dependencies** (for advanced features):
  - `requests` - For barcode lookup via Open Food Facts API
  - `pyzbar` + `pillow` - For barcode scanning from images
  - `openpyxl` - For Excel (.xlsx) import support

Install optional dependencies:
```bash
pip install requests pyzbar pillow openpyxl
# On macOS, you may also need: brew install zbar
```

## Quick Start

### 1. Set Up Your Collection

#### Option A: Add bottles one at a time
```bash
python3 add_bottle.py add "Buffalo Trace" bourbon --abv 45.0 --price 25.99
python3 add_bottle.py add "Macallan 12" scotch --abv 43.0 --price 65.00
```

#### Option B: Add via barcode lookup
```bash
# Manual UPC entry
python3 add_bottle.py barcode 012345678901 --price 25.99

# Scan from image file
python3 add_bottle.py barcode /path/to/barcode_image.jpg
```

#### Option C: Bulk import from CSV, JSON, or Excel
**CSV Import:**
Create a CSV file (`bottles.csv`) with format:
```csv
name,category,abv,price_paid,purchase_date,notes,barcode
Buffalo Trace,bourbon,45.0,25.99,2023-01-15,,
Macallan 12,scotch,43.0,65.00,2023-02-20,,
```

```bash
# Preview before importing
python3 add_bottle.py csv bottles.csv --preview

# Import
python3 add_bottle.py csv bottles.csv
```

**JSON Import:**
```bash
python3 add_bottle.py json bottles.json --preview
python3 add_bottle.py json bottles.json
```

**Excel Import:**
```bash
python3 add_bottle.py excel bottles.xlsx --preview
python3 add_bottle.py excel bottles.xlsx --sheet "My Collection"
```

### 2. Configure Your Preferences (Optional)

Customize your tasting schedule with user preferences:
```bash
# View current configuration
python3 tasting_manager.py config show

# Set preferred tasting days (e.g., Fridays only)
python3 tasting_manager.py config set user_preferences.preferred_days Friday

# Set tasting frequency
python3 tasting_manager.py config set user_preferences.tasting_frequency bi-weekly

# Add dates to avoid
python3 tasting_manager.py config set user_preferences.avoid_dates "2024-12-25,2025-01-01"

# Enable seasonal adjustments (lighter in summer, heavier in winter)
python3 tasting_manager.py config set user_preferences.seasonal_adjustments true

# Edit config file directly
python3 tasting_manager.py config edit
```

### 3. Generate Your Schedule

```bash
# Generate with default settings (or your configured preferences)
python3 schedule_generator.py

# Preview first 10 weeks
python3 schedule_generator.py --preview

# Start on a specific date
python3 schedule_generator.py --start-date 2024-01-01

# Custom duration (in weeks)
python3 schedule_generator.py --weeks 156  # 3 years
```

### 4. View Your Schedule

```bash
python3 tasting_manager.py schedule --weeks 10
```

### 5. Record a Tasting

After tasting a bottle:
```bash
python3 tasting_manager.py record 1 7.5 "Smooth, vanilla notes, good finish"
```

Where:
- `1` is the bottle ID
- `7.5` is your rating (0-10)
- `"..."` are your tasting notes

### 6. Track Progress

```bash
python3 tasting_manager.py progress
```

## Common Commands

### List Bottles
```bash
# All bottles
python3 tasting_manager.py list

# By category
python3 tasting_manager.py list --category bourbon

# Only untasted
python3 tasting_manager.py list --untasted

# Only tasted
python3 tasting_manager.py list --tasted
```

### Find a Bottle
```bash
python3 tasting_manager.py find "Buffalo Trace"
# or by ID
python3 tasting_manager.py find 1
```

### View Schedule
```bash
# Next 10 weeks (default)
python3 tasting_manager.py schedule

# Next 20 weeks
python3 tasting_manager.py schedule --weeks 20
```

## Configuration

Dram Planner uses a `config.json` file to store user preferences. The file is automatically created on first run with defaults. You can manage it via CLI commands:

```bash
# Show current config
python3 tasting_manager.py config show

# Set a preference
python3 tasting_manager.py config set user_preferences.tasting_frequency monthly

# Reset to defaults
python3 tasting_manager.py config reset

# Edit directly
python3 tasting_manager.py config edit
```

### Available Preferences

- `tasting_frequency`: "weekly", "bi-weekly", "monthly", or "custom"
- `custom_interval_days`: Days between tastings (for custom frequency)
- `preferred_days`: List of preferred days (e.g., ["Friday", "Saturday"])
- `avoid_dates`: Dates to skip (e.g., ["2024-12-25", "2025-01-01"])
- `category_preferences`: Weight multipliers (e.g., {"bourbon": 2.0, "scotch": 1.5})
- `seasonal_adjustments`: Enable seasonal preferences (true/false)
- `min_days_between_category`: Minimum days between same category tastings
- `default_schedule_weeks`: Default schedule duration (default: 104)

## Collection Structure

Each bottle in `collection.json` contains:
- `id`: Unique identifier
- `name`: Bottle name
- `category`: Type (bourbon, scotch, irish, clear, liqueur, etc.)
- `abv`: Alcohol by volume (%)
- `price_paid`: Purchase price
- `purchase_date`: When you bought it
- `opened_date`: When you first opened it
- `notes`: General notes
- `barcode`: Barcode/UPC code (if added via barcode lookup)
- `tasted`: Boolean - has it been tasted?
- `tasting_date`: Date of tasting
- `rating`: Your rating (0-10)
- `tasting_notes`: Detailed tasting notes

## Tips for Success

1. **Start Fresh**: Generate a new schedule if you fall behind or want to adjust
2. **Be Flexible**: The schedule is a guide - adjust as needed for special occasions
3. **Document Immediately**: Record tastings right after drinking while notes are fresh
4. **Track Evolution**: Re-taste bottles after 6-12 months to see how your palate changes
5. **Category Balance**: The schedule tries to mix categories, but you can manually adjust if desired

## Import Formats

### CSV Format
Supports flexible CSV formats with or without headers:
```csv
name,category,abv,price_paid,purchase_date,notes,barcode
Buffalo Trace,bourbon,45.0,25.99,2023-01-15,,
Macallan 12,scotch,43.0,65.00,2023-02-20,,
```

### JSON Format
Supports array or object format:
```json
[
  {
    "name": "Buffalo Trace",
    "category": "bourbon",
    "abv": 45.0,
    "price_paid": 25.99,
    "purchase_date": "2023-01-15"
  }
]
```

Or:
```json
{
  "bottles": [
    {
      "name": "Buffalo Trace",
      "category": "bourbon",
      "abv": 45.0
    }
  ]
}
```

### Excel Format
Supports `.xlsx` files with flexible header mapping. Common headers are automatically detected:
- Name: name, bottle, spirit, product, title
- Category: category, type, kind
- ABV: abv, alcohol, alcohol %, proof
- Price: price, price_paid, cost, purchase price
- Date: purchase_date, date, purchase date, bought
- Notes: notes, note, description, desc
- Barcode: barcode, upc, ean, code

## Example Workflow

1. **Week 1**: Check schedule - "This week: Buffalo Trace (bourbon)"
2. **Tasting Day**: Pour neat, take notes using template
3. **After Tasting**: Record with `tasting_manager.py record`
4. **Review**: Check progress with `tasting_manager.py progress`
5. **Next Week**: Repeat!

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python3 -m pytest tests/
```

Or use unittest:

```bash
python3 -m unittest discover tests
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for spirits enthusiasts who want to systematically explore their collections
- Inspired by the need for scheduling functionality not available in other apps
- Community-driven development

## 🔮 Future Enhancements

Planned enhancements (see [ENHANCEMENT_QUEUE.md](ENHANCEMENT_QUEUE.md)):
- 🌐 **Hosted Web Application** - Web interface for easier access
- 📱 **Mobile Applications** - iPhone and Android apps
- 📊 **Enhanced Analytics** - Statistical analysis and insights
- 📅 **Calendar Export** - iCal format for calendar integration
- 🖼️ **Photo Storage** - Upload and store bottle photos

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

- [User Guide](README.md) - This file
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history
- [Tasting Notes Template](tasting_notes_template.md) - Template for detailed notes

## 🐛 Issues & Support

Found a bug or have a feature request? Please [open an issue](https://github.com/yourusername/dram-planner/issues).

---

**Happy Tasting!** 🥃

Remember: The goal is to enjoy the journey and develop your palate. Don't stress about sticking to the schedule perfectly - it's a guide, not a requirement!
