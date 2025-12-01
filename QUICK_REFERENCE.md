# Dram Planner - Quick Reference Guide

A quick reference for common commands and operations.

## Collection Management

### Add Bottles

```bash
# Add single bottle manually
python3 add_bottle.py add "Bottle Name" category --abv 45.0 --price 25.99

# Add via barcode lookup
python3 add_bottle.py barcode 012345678901

# Import from CSV (with preview)
python3 add_bottle.py csv bottles.csv --preview
python3 add_bottle.py csv bottles.csv

# Import from JSON
python3 add_bottle.py json bottles.json --preview

# Import from Excel
python3 add_bottle.py excel bottles.xlsx --preview
python3 add_bottle.py excel bottles.xlsx --sheet "Sheet Name"
```

### View Collection

```bash
# List all bottles
python3 tasting_manager.py list

# List by category
python3 tasting_manager.py list --category bourbon

# List only untasted
python3 tasting_manager.py list --untasted

# Find specific bottle
python3 tasting_manager.py find "Bottle Name"
python3 tasting_manager.py find 1  # by ID
```

## Configuration

### View and Manage Preferences

```bash
# Show current configuration
python3 tasting_manager.py config show

# Set a preference
python3 tasting_manager.py config set user_preferences.tasting_frequency bi-weekly
python3 tasting_manager.py config set user_preferences.preferred_days "Friday,Saturday"
python3 tasting_manager.py config set user_preferences.avoid_dates "2024-12-25,2025-01-01"

# Reset to defaults
python3 tasting_manager.py config reset

# Edit config file directly
python3 tasting_manager.py config edit
```

### Common Preference Settings

```bash
# Weekly tastings on Fridays
python3 tasting_manager.py config set user_preferences.tasting_frequency weekly
python3 tasting_manager.py config set user_preferences.preferred_days Friday

# Bi-weekly tastings
python3 tasting_manager.py config set user_preferences.tasting_frequency bi-weekly

# Monthly tastings
python3 tasting_manager.py config set user_preferences.tasting_frequency monthly

# Custom interval (every 10 days)
python3 tasting_manager.py config set user_preferences.tasting_frequency custom
python3 tasting_manager.py config set user_preferences.custom_interval_days 10

# Enable seasonal adjustments
python3 tasting_manager.py config set user_preferences.seasonal_adjustments true

# Set category preferences (higher = more likely)
python3 tasting_manager.py config set user_preferences.category_preferences '{"bourbon": 2.0, "scotch": 1.5}'

# Minimum days between same category
python3 tasting_manager.py config set user_preferences.min_days_between_category 7
```

## Schedule Generation

### Generate Schedule

```bash
# Generate with current preferences
python3 schedule_generator.py

# Preview first 10 weeks
python3 schedule_generator.py --preview

# Custom start date
python3 schedule_generator.py --start-date 2025-01-01

# Custom duration (in weeks)
python3 schedule_generator.py --weeks 156  # 3 years

# Use specific config file
python3 schedule_generator.py --config my_config.json
```

### View Schedule

```bash
# Next 10 weeks (default)
python3 tasting_manager.py schedule

# Next 20 weeks
python3 tasting_manager.py schedule --weeks 20

# Custom schedule file
python3 tasting_manager.py schedule --schedule my_schedule.json --weeks 10
```

## Tasting Management

### Record Tasting

```bash
# Record with rating and notes
python3 tasting_manager.py record 1 7.5 "Smooth, vanilla notes, good finish"

# Record with specific date
python3 tasting_manager.py record 1 8.0 "Excellent" --date 2025-01-15
```

### Track Progress

```bash
# View progress statistics
python3 tasting_manager.py progress

# View by collection file
python3 tasting_manager.py progress --collection my_collection.json
```

## Import Formats

### CSV Format

```csv
name,category,abv,price_paid,purchase_date,notes,barcode
Buffalo Trace,bourbon,45.0,25.99,2023-01-15,,
Macallan 12,scotch,43.0,65.00,2023-02-20,,
```

### JSON Format

```json
{
  "bottles": [
    {
      "name": "Buffalo Trace",
      "category": "bourbon",
      "abv": 45.0,
      "price_paid": 25.99,
      "purchase_date": "2023-01-15"
    }
  ]
}
```

### Excel Format

- Supports `.xlsx` files
- Auto-detects common headers (name, category, abv, price, etc.)
- Can specify sheet name with `--sheet` option

## File Locations

- **Collection:** `collection.json` (default)
- **Schedule:** `tasting_schedule.json` (default)
- **Config:** `config.json` (auto-created on first run)
- **Examples:** `examples/` directory

## Common Workflows

### Initial Setup

```bash
# 1. Add bottles (choose one method)
python3 add_bottle.py csv bottles.csv
# or
python3 add_bottle.py json bottles.json

# 2. Configure preferences (optional)
python3 tasting_manager.py config set user_preferences.tasting_frequency weekly
python3 tasting_manager.py config set user_preferences.preferred_days Friday

# 3. Generate schedule
python3 schedule_generator.py

# 4. View schedule
python3 tasting_manager.py schedule
```

### Weekly Routine

```bash
# 1. Check this week's tasting
python3 tasting_manager.py schedule --weeks 1

# 2. After tasting, record notes
python3 tasting_manager.py record <bottle_id> <rating> "notes"

# 3. Check progress
python3 tasting_manager.py progress
```

### Adding New Bottles

```bash
# Option 1: Manual entry
python3 add_bottle.py add "New Bottle" category --abv 45.0

# Option 2: Barcode lookup
python3 add_bottle.py barcode 012345678901

# Option 3: Import from file
python3 add_bottle.py csv new_bottles.csv --preview
```

## Tips

- **Always preview imports** before committing: use `--preview` flag
- **Backup your data:** `collection.json` contains all your data
- **Regenerate schedule** if you add many new bottles or change preferences
- **Use config commands** to customize your experience
- **Check progress regularly** to stay motivated

## Troubleshooting

### Import Errors
- Use `--preview` to see errors before importing
- Check file format matches examples
- Ensure required fields (name, category) are present

### Schedule Issues
- Verify config file is valid: `python3 tasting_manager.py config show`
- Check collection has bottles: `python3 tasting_manager.py list`
- Try regenerating schedule with `--preview` first

### Barcode Lookup Fails
- Ensure `requests` library is installed: `pip install requests`
- Check internet connection
- Try manual entry as fallback

---

For detailed documentation, see [README.md](README.md)

