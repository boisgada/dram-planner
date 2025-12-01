# Dram Planner Enhancement Queue

This document tracks all planned enhancements, features, and improvements for Dram Planner.

## Queue Status

- **Total Items:** 5
- **In Progress:** 0
- **Completed:** 3
- **Pending:** 2

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
**Status:** ✅ Completed  
**Added:** 2024-12-19  
**Completed:** 2025-01-01  
**Priority:** 🟡 Medium  
**Effort:** 1-2 days  
**Dependencies:** Optional (openpyxl for Excel)

**Description:**
Enhance import capabilities to support multiple formats and external sources.

**Features:**
- [x] Enhanced CSV import (better format support)
- [x] JSON import (generic format)
- [x] Excel import (.xlsx files)
- [ ] Distiller import (if API available) - Deferred
- [ ] Generic API endpoint import - Deferred
- [x] Import validation and error handling
- [x] Import preview before committing

**Acceptance Criteria:**
- [x] Support multiple import formats
- [x] Validate imported data
- [x] Handle import errors gracefully
- [x] Clear import documentation

**Implementation Notes:**
- Created `import_manager.py` module with unified import handling
- Enhanced CSV import with delimiter detection and header support
- Added JSON import supporting multiple formats
- Added Excel import with header mapping
- Comprehensive validation and error reporting
- Preview functionality for all import types
- Updated `add_bottle.py` with new import commands (csv, json, excel)

**Related Issues:** None

---

#### ENH-004: Hosted Web Application
**Status:** 🟡 Pending  
**Added:** 2025-01-01  
**Priority:** 🟡 Medium  
**Effort:** 1-2 weeks  
**Dependencies:** Web framework (Flask/FastAPI), database (SQLite/PostgreSQL), hosting platform

**Description:**
Convert Dram Planner from CLI tool to a hosted web application for easier access and multi-device support.

**Features:**
- [ ] Web framework setup (Flask or FastAPI)
- [ ] RESTful API for all operations
- [ ] Web UI for collection management
- [ ] Web UI for schedule viewing and management
- [ ] User authentication and accounts
- [ ] Database migration from JSON to SQLite/PostgreSQL
- [ ] Responsive design (mobile-friendly)
- [ ] Hosting setup (Heroku, Railway, Render, or similar)
- [ ] Data export/import functionality
- [ ] Calendar integration (iCal export)
- [ ] Photo uploads for bottles
- [ ] Statistics and analytics dashboard

**Acceptance Criteria:**
- Users can access application via web browser
- All CLI functionality available via web interface
- User data securely stored and isolated
- Responsive design works on mobile devices
- Application deployed and accessible publicly
- Data can be exported/imported

**Considerations:**
- Maintain backward compatibility with CLI tool
- Consider keeping CLI as alternative interface
- Evaluate hosting costs and options
- Plan for user data privacy and security
- Consider migration path for existing users

**Related Issues:** None

---

#### ENH-005: Mobile Applications (iPhone & Android)
**Status:** 🟡 Pending  
**Added:** 2025-01-01  
**Priority:** 🟡 Medium  
**Effort:** 3-4 weeks  
**Dependencies:** Mobile development framework (React Native, Flutter, or native), API backend

**Description:**
Create native or cross-platform mobile applications for iPhone and Android to provide on-the-go access to Dram Planner.

**Features:**
- [ ] Cross-platform framework selection (React Native, Flutter, or native)
- [ ] iOS app development (iPhone/iPad)
- [ ] Android app development
- [ ] Collection management interface
- [ ] Schedule viewing and management
- [ ] Barcode scanning using device camera
- [ ] Tasting note entry
- [ ] Photo capture for bottles
- [ ] Offline data synchronization
- [ ] Push notifications for scheduled tastings
- [ ] Calendar integration
- [ ] Data sync with web/CLI versions
- [ ] App store submission (iOS App Store, Google Play)

**Acceptance Criteria:**
- Apps available on iOS App Store and Google Play Store
- All core functionality available on mobile
- Barcode scanning works reliably
- Offline mode supported
- Data syncs across devices
- Native mobile UX/UI design
- Apps pass store review guidelines

**Considerations:**
- Cross-platform vs native development trade-offs
- API backend required (may depend on ENH-004)
- App store fees and requirements
- Device camera permissions for barcode scanning
- Offline-first architecture
- Data synchronization strategy
- User authentication and cloud storage
- Consider PWA (Progressive Web App) as alternative

**Related Issues:** None

---

### 🟢 Low Priority

*None currently*

## Implementation Notes

### Current Focus
✅ **ENH-001: User Preferences** - Completed!
✅ **ENH-002: Barcode Scanning** - Completed!
✅ **ENH-003: Enhanced External Import Capabilities** - Completed!

### Next Up
All high-priority enhancements completed. Consider **ENH-004: Hosted Web Application** or **ENH-005: Mobile Applications**.

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

