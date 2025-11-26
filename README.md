# Dram Planner 🥃

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python-based system for managing your spirits collection and creating a structured 2-year tasting schedule. **The only free application that offers scheduling functionality for spirits tastings!**

## ✨ Features

- 📅 **Tasting Schedule Generation** - Automatically create 2-year (104 weeks) tasting schedules
- 📊 **Collection Management** - Track your entire spirits collection in one place
- 📝 **Tasting Notes** - Record detailed notes and ratings for each tasting
- 📈 **Progress Tracking** - Monitor your progress by category and overall
- 🎯 **Smart Scheduling** - Prioritizes untasted bottles and ensures category variety
- 💻 **CLI Interface** - Powerful command-line tools for all operations
- 📥 **CSV Import** - Bulk import your collection from CSV files
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

- **Python 3.6+** (uses only standard library - no dependencies!)
- **No external packages required** - completely self-contained

## Quick Start

### 1. Set Up Your Collection

#### Option A: Add bottles one at a time
```bash
python3 add_bottle.py add "Buffalo Trace" bourbon --abv 45.0 --price 25.99
python3 add_bottle.py add "Macallan 12" scotch --abv 43.0 --price 65.00
```

#### Option B: Bulk import from CSV
Create a CSV file (`bottles.csv`) with format:
```csv
name,category,abv,price_paid,purchase_date,notes
Buffalo Trace,bourbon,45.0,25.99,2023-01-15,
Macallan 12,scotch,43.0,65.00,2023-02-20,
```

Then import:
```bash
python3 add_bottle.py csv bottles.csv
```

### 2. Generate Your Schedule

```bash
python3 schedule_generator.py
```

This creates a 2-year schedule starting today. To preview first 10 weeks:
```bash
python3 schedule_generator.py --preview
```

To start on a specific date:
```bash
python3 schedule_generator.py --start-date 2024-01-01
```

### 3. View Your Schedule

```bash
python3 tasting_manager.py schedule --weeks 10
```

### 4. Record a Tasting

After tasting a bottle:
```bash
python3 tasting_manager.py record 1 7.5 "Smooth, vanilla notes, good finish"
```

Where:
- `1` is the bottle ID
- `7.5` is your rating (0-10)
- `"..."` are your tasting notes

### 5. Track Progress

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

## Customization

### Adjust Schedule Duration
```bash
python3 schedule_generator.py --weeks 156  # 3 years instead of 2
```

### Modify Schedule Logic
Edit `schedule_generator.py` to adjust:
- Category rotation patterns
- Seasonal preferences
- Repeat frequency

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

Ideas for future versions (contributions welcome!):
- Web interface for easier note-taking
- Photo storage for bottle labels
- Statistical analysis of preferences
- Export to spreadsheet (CSV, Excel)
- Calendar export (iCal format)
- Integration with spirit databases (e.g., Distiller API)
- Mobile-friendly web interface
- Reminder notifications

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
