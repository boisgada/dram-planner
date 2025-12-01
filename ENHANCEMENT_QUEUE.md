# Dram Planner Enhancement Queue

This document tracks all planned enhancements, features, and improvements for Dram Planner.

## Queue Status

- **Total Items:** 3
- **In Progress:** 0
- **Completed:** 2
- **Pending:** 1

## Priority Levels

- 🔴 **Critical** - Core functionality gaps, blocking issues
- 🟠 **High** - Significant user value, high impact
- 🟡 **Medium** - Nice to have, moderate impact
- 🟢 **Low** - Minor improvements, polish

## Enhancement Queue

### 🔴 Critical Priority

*None currently*

### 🟠 High Priority

#### ENH-001: User Preferences & Custom Scheduling
**Status:** ✅ Completed  
**Added:** 2024-12-19  
**Completed:** 2025-01-01  
**Priority:** 🟠 High  
**Effort:** 1-2 days  
**Dependencies:** None

**Description:**
Add user-specific scheduling preferences to allow customization of tasting schedules.

**Features:**
- [x] User configuration file (`config.json`)
- [x] Custom tasting frequency (weekly, bi-weekly, monthly, custom)
- [x] Preferred tasting days (e.g., Fridays only)
- [x] Avoid certain dates (holidays, special occasions)
- [x] Category preferences (favor/avoid certain categories)
- [x] Seasonal adjustments (lighter in summer, heavier in winter)
- [x] Minimum time between same category tastings
- [x] CLI commands to manage preferences

**Acceptance Criteria:**
- [x] Users can configure scheduling preferences
- [x] Schedule generator respects user preferences
- [x] Preferences persist across schedule generations
- [x] Clear documentation for preference options

**Implementation Notes:**
- `config.py` module created with helper functions
- `schedule_generator.py` updated to use config preferences
- `tasting_manager.py` updated with config management commands (show, set, reset, edit)
- All preference features implemented and integrated

**Related Issues:** None

---

#### ENH-002: Barcode Scanning & Automatic Lookup
**Status:** ✅ Completed  
**Added:** 2024-12-19  
**Completed:** 2025-01-01  
**Priority:** 🟠 High  
**Effort:** 2-3 days  
**Dependencies:** Optional (pyzbar, requests, pillow)

**Description:**
Add barcode scanning capability to automatically retrieve bottle information.

**Features:**
- [x] Barcode scanning support (UPC-A, EAN-13) - via pyzbar
- [x] Manual UPC entry option
- [x] Open Food Facts API integration (free)
- [x] Automatic bottle information retrieval
- [x] Store barcode/UPC in bottle data
- [x] Fallback to manual entry if lookup fails
- [x] CLI command for barcode entry (`add_bottle.py barcode`)

**Acceptance Criteria:**
- [x] Users can scan or enter barcodes
- [x] Automatic lookup retrieves bottle information
- [x] Graceful fallback if lookup fails
- [x] Barcode stored in collection for future reference

**Implementation Notes:**
- Created `barcode_lookup.py` module with Open Food Facts API integration
- Updated `add_bottle.py` with `barcode` command
- Added barcode field to bottle data structure
- Supports manual UPC entry and image file scanning
- Category mapping from Open Food Facts to spirits categories
- ABV extraction from product data
- Optional dependencies documented in requirements.txt

**Related Issues:** None

---

### 🟡 Medium Priority

#### ENH-003: Enhanced External Import Capabilities
**Status:** 🟡 Pending  
**Added:** 2024-12-19  
**Priority:** 🟡 Medium  
**Effort:** 1-2 days  
**Dependencies:** Optional (openpyxl for Excel)

**Description:**
Enhance import capabilities to support multiple formats and external sources.

**Features:**
- [ ] Enhanced CSV import (better format support)
- [ ] JSON import (generic format)
- [ ] Excel import (.xlsx files)
- [ ] Distiller import (if API available)
- [ ] Generic API endpoint import
- [ ] Import validation and error handling
- [ ] Import preview before committing

**Acceptance Criteria:**
- Support multiple import formats
- Validate imported data
- Handle import errors gracefully
- Clear import documentation

**Related Issues:** None

---

### 🟢 Low Priority

*None currently*

## Implementation Notes

### Current Focus
✅ **ENH-001: User Preferences** - Completed!
✅ **ENH-002: Barcode Scanning** - Completed!

### Next Up
Proceeding with **ENH-003: Enhanced External Import Capabilities**.

## Adding New Enhancements

When adding new items to the queue:
1. Assign unique ID (ENH-XXX)
2. Set priority level
3. Estimate effort
4. List dependencies
5. Define acceptance criteria
6. Add to appropriate priority section

## Status Legend

- 🟡 **Pending** - Not started
- 🔵 **In Progress** - Currently being worked on
- ✅ **Completed** - Finished and tested
- ⏸️ **Blocked** - Waiting on dependencies
- ❌ **Cancelled** - No longer needed

---

**Last Updated:** 2025-01-01 (ENH-002 completed)

