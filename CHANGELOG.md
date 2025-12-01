# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Hosted web application (ENH-004)
- Mobile applications for iPhone and Android (ENH-005)

## [0.2.0] - 2025-01-01

### Added
- **User Preferences & Custom Scheduling (ENH-001)**
  - Configuration system (`config.py`) for managing user preferences
  - Custom tasting frequency (weekly, bi-weekly, monthly, custom days)
  - Preferred tasting days (e.g., Fridays only)
  - Avoid certain dates (holidays, special occasions)
  - Category preferences with weighting system
  - Seasonal adjustments (lighter spirits in summer, heavier in winter)
  - Minimum days between same category tastings
  - Config management CLI commands (`config show`, `set`, `reset`, `edit`)
  
- **Barcode Scanning & Automatic Lookup (ENH-002)**
  - Barcode lookup module (`barcode_lookup.py`) with Open Food Facts API integration
  - Manual UPC entry option
  - Barcode scanning from image files (via pyzbar)
  - Automatic bottle information retrieval (name, category, ABV)
  - Category mapping from Open Food Facts to spirits categories
  - Barcode field added to bottle data structure
  - Graceful fallback if lookup fails
  
- **Enhanced External Import Capabilities (ENH-003)**
  - Unified import manager (`import_manager.py`) for all import formats
  - Enhanced CSV import with delimiter detection and flexible headers
  - JSON import supporting array and object formats
  - Excel import (.xlsx) with header mapping and sheet selection
  - Comprehensive validation and error reporting
  - Import preview functionality before committing
  - New import commands: `json`, `excel` (enhanced `csv`)
  - User confirmation prompts for errors

### Changed
- Schedule generation now respects user preferences from config
- CSV import enhanced with better format support
- Import commands support `--preview` flag for validation

### Documentation
- Updated README with all new features
- Added example files: `bottles.csv.example`, `bottles.json.example`, `config.json.example`
- Documented optional dependencies and installation
- Added configuration management section

### Dependencies
- Optional: `requests` (for barcode lookup)
- Optional: `pyzbar` + `pillow` (for barcode scanning)
- Optional: `openpyxl` (for Excel import)

## [Unreleased] (Previous)

### Added
- Comprehensive error handling and input validation
- Improved documentation and docstrings
- Project structure for public release

## [0.1.0] - 2024-12-19

### Added
- Initial release
- Collection database (JSON-based)
- 2-year tasting schedule generation
- Tasting notes tracking
- Progress monitoring
- CLI interface for all operations
- CSV import functionality
- Category-based organization
- Rating system (0-10 scale)

### Features
- Generate customizable tasting schedules (default: 2 years, 104 weeks)
- Track collection of spirits bottles
- Record detailed tasting notes and ratings
- Monitor progress by category
- View upcoming tastings
- Find bottles by name or ID
- List bottles with various filters

[Unreleased]: https://github.com/boisgada/dram-planner/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/boisgada/dram-planner/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/boisgada/dram-planner/releases/tag/v0.1.0

