# Dram Planner Enhancement Queue

This document tracks all planned enhancements, features, and improvements for Dram Planner.

## Queue Status

- **Total Items:** 10
- **In Progress:** 1
- **Completed:** 3
- **Pending:** 6

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
**Status:** 🔵 In Progress  
**Added:** 2025-01-01  
**Started:** 2025-01-01  
**Priority:** 🟡 Medium  
**Effort:** 1-2 weeks  
**Dependencies:** Web framework (Flask/FastAPI), database (SQLite/PostgreSQL), hosting platform

**Description:**
Convert Dram Planner from CLI tool to a hosted web application for easier access and multi-device support.

**Features:**
- [x] Web framework setup (Flask)
- [x] RESTful API for all operations
- [x] Database models (SQLite/PostgreSQL ready)
- [x] User authentication and accounts
- [x] Web UI for collection management (CRUD operations)
- [x] Web UI for schedule viewing and management
- [x] Responsive design (mobile-friendly)
- [x] Data export/import functionality (CSV, JSON)
- [x] Calendar integration (iCal export)
- [x] Statistics and analytics dashboard
- [ ] Photo uploads for bottles
- [ ] Hosting setup (currently on vps05)

**Implementation Notes:**
- Flask application structure created
- Database models: User, Bottle, Schedule, ScheduleItem, UserConfig
- RESTful API endpoints for bottles, schedules, config, and auth
- Authentication system with registration and login
- SQLite database (PostgreSQL ready via DATABASE_URL)
- Application entry point and configuration system
- **Docker containerization complete:**
  - Production Dockerfile with Gunicorn
  - Development Dockerfile with hot-reload
  - docker-compose.yml for production (PostgreSQL)
  - docker-compose.dev.yml for development (SQLite)
  - Comprehensive Docker documentation
- **Web UI complete:**
  - Collection management with full CRUD
  - Schedule generation and viewing
  - User settings/preferences page
  - Export/import functionality (CSV, JSON, iCal)
  - Responsive mobile-friendly design
  - Enhanced dashboard with statistics
- **Deployed:** Running on vps05 with localhost-only binding

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

#### ENH-006: Master Beverage Catalog
**Status:** 🟡 Pending  
**Added:** 2025-12-01  
**Priority:** 🟡 Medium  
**Effort:** 2-3 weeks  
**Dependencies:** Database for master list (if maintained locally), or external API integration

**Description:**
Provide users with a master list/catalog of beverages to select from when adding bottles to their collection, eliminating the need for manual entry of common information.

**Features:**
- [ ] Research and evaluate options:
  - [ ] Maintain local master database of beverages
  - [ ] Integrate with external beverage database/API (e.g., Distiller, Whiskybase, etc.)
  - [ ] Hybrid approach (local + external lookup)
- [ ] Searchable beverage catalog
- [ ] Browse by category, brand, region
- [ ] Quick-add from catalog to user collection
- [ ] Pre-populate bottle information (name, category, ABV, etc.)
- [ ] Allow users to customize imported data before adding
- [ ] If maintaining local master list:
  - [ ] Import/export master list functionality
  - [ ] Admin interface for managing master list
  - [ ] Community contributions (optional)
  - [ ] Version control for master list updates

**Acceptance Criteria:**
- Users can search and browse beverage catalog
- Users can add bottles from catalog to collection with one click
- Bottle information is pre-populated from catalog
- If local master list: can be imported/exported
- If external API: graceful fallback if API unavailable
- Catalog search is fast and responsive

**Considerations:**
- **Local Master List:**
  - Storage and maintenance overhead
  - Keeping data current and accurate
  - Initial data population
  - Update mechanism
- **External API:**
  - API availability and reliability
  - Rate limits and costs
  - Data format consistency
  - Fallback strategy
- **Hybrid Approach:**
  - Cache frequently accessed items locally
  - Use external API for lookups
  - Best of both worlds
- Data licensing and attribution requirements
- User privacy (what data is sent to external APIs)

**Related Issues:** None

---

#### ENH-007: Review Visualization & Social Features
**Status:** 🟡 Pending
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 3-4 weeks
**Dependencies:** ENH-004 (Web Application), ENH-006 (Master Database)

**Description:**
Add social features to view and compare tasting reviews from other users and visualize community preferences.

**Features:**
- [ ] **Review Visualization:**
  - [ ] View community reviews for bottles in your collection
  - [ ] Visualize rating distributions and trends
  - [ ] Compare your ratings with community averages
  - [ ] See most popular bottles by category and region
- [ ] **Social Discovery:**
  - [ ] Browse reviews by other users (anonymized)
  - [ ] Follow other users or categories
  - [ ] Discover new bottles through community recommendations
  - [ ] Community-curated "best of" lists
- [ ] **Review Analytics:**
  - [ ] Charts showing rating trends over time
  - [ ] Category preference analysis (what the community likes)
  - [ ] Seasonal drinking patterns visualization
  - [ ] Bottle age vs. rating correlation analysis
- [ ] **Privacy Controls:**
  - [ ] Choose review visibility (public, friends-only, private)
  - [ ] Anonymized community statistics
  - [ ] Opt-out of social features
- [ ] **Community Features:**
  - [ ] Like/upvote helpful reviews
  - [ ] Comment on reviews (optional)
  - [ ] Share reviews to social media
  - [ ] Create public tasting notes

**Acceptance Criteria:**
- Users can view community reviews for bottles
- Visual charts show rating distributions and trends
- Users can compare their preferences with community
- Privacy controls allow users to manage visibility
- Social discovery helps find new bottles to try

**Considerations:**
- **Privacy:** All reviews should be anonymous by default
- **Data Aggregation:** Community stats should never reveal individual user data
- **Content Moderation:** Basic moderation for inappropriate content
- **Performance:** Large review datasets need efficient querying
- **User Experience:** Balance social features with core functionality

**Related Issues:** Depends on ENH-004, ENH-006

---

#### ENH-008: User Groups & Shared Tasting Schedules
**Status:** 🟡 Pending
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 4-6 weeks
**Dependencies:** ENH-004 (Web Application), Database for user relationships

**Description:**
Allow users to form groups and share/follow tasting schedules, creating community-driven tasting experiences.

**Features:**
- [ ] **Group Creation:**
  - [ ] Create public or private tasting groups
  - [ ] Define group themes (e.g., "Bourbon Enthusiasts", "Scotch Tour 2025")
  - [ ] Set group membership rules (open, invite-only, moderated)
  - [ ] Group descriptions and rules
- [ ] **Shared Schedules:**
  - [ ] Subscribe to group tasting schedules
  - [ ] Group-curated bottle selections
  - [ ] Collaborative schedule creation
  - [ ] Group progress tracking
- [ ] **Social Features:**
  - [ ] Join multiple groups
  - [ ] Follow other users' public schedules
  - [ ] Group discussions and tastings
  - [ ] Schedule sharing and forking
- [ ] **Group Management:**
  - [ ] Group administrators and moderators
  - [ ] Membership management
  - [ ] Group statistics and analytics
  - [ ] Group events and deadlines
- [ ] **Subscription Model:**
  - [ ] Follow/pre-subscribe to group schedules
  - [ ] Automatic schedule updates from groups
  - [ ] Group notifications and reminders
  - [ ] Personalized group recommendations

**Acceptance Criteria:**
- Users can create and join tasting groups
- Groups can create and share tasting schedules
- Users can subscribe to group schedules
- Group progress and discussions work
- Privacy and moderation controls exist

**Considerations:**
- **Scale:** How to handle large groups efficiently
- **Moderation:** Tools for group administrators
- **Discovery:** How users find relevant groups
- **Engagement:** Features to keep groups active
- **Legal:** Terms of service for user-generated content

**Related Issues:** Depends on ENH-004

---

#### ENH-009: AI-Powered Schedule Planning
**Status:** 🟡 Pending
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 4-6 weeks
**Dependencies:** ENH-004 (Web Application), ENH-006 (Master Database), AI/ML libraries

**Description:**
Use artificial intelligence to create personalized tasting schedules based on user preferences, tasting history, and community data.

**Features:**
- [ ] **Preference Learning:**
  - [ ] Analyze user's tasting notes and ratings
  - [ ] Learn flavor preferences from text analysis
  - [ ] Identify preferred characteristics (sweet, smoky, peaty, etc.)
  - [ ] Build user taste profile over time
- [ ] **Smart Recommendations:**
  - [ ] Suggest bottles based on past preferences
  - [ ] Predict ratings for untried bottles
  - [ ] Recommend next bottles to try
  - [ ] Seasonal and occasion-based suggestions
- [ ] **Schedule Optimization:**
  - [ ] AI-optimized tasting order
  - [ ] Balance variety with preference matching
  - [ ] Avoid fatigue from similar-tasting bottles
  - [ ] Optimize for palate development
- [ ] **Community Integration:**
  - [ ] Use community reviews for recommendations
  - [ ] Compare preferences with similar users
  - [ ] Trend analysis for emerging favorites
  - [ ] Collaborative filtering for bottle suggestions
- [ ] **Advanced Features:**
  - [ ] Natural language tasting note analysis
  - [ ] Mood and occasion-based recommendations
  - [ ] Pairing suggestions (food, music, etc.)
  - [ ] Learning from explicit feedback

**Acceptance Criteria:**
- AI learns from user's tasting history
- Personalized recommendations improve over time
- Schedule generation considers learned preferences
- Users can provide feedback on recommendations
- System adapts to user feedback

**Considerations:**
- **Privacy:** User data used only for personalization
- **Accuracy:** Clear about AI limitations and suggestions
- **Fallback:** Traditional scheduling always available
- **Bias:** Avoid reinforcing existing preferences too strongly
- **Performance:** AI processing shouldn't slow down UI
- **Explainability:** Users understand why recommendations are made

**Related Issues:** Depends on ENH-004, ENH-006, ENH-007

---

#### ENH-010: Web Barcode Scanning & Lookup
**Status:** 🟡 Pending
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 1-2 weeks
**Dependencies:** ENH-004 (Web Application), existing CLI barcode functionality

**Description:**
Add barcode scanning and automatic product lookup functionality to the web GUI, leveraging the existing CLI barcode lookup implementation.

**Features:**
- [ ] **Barcode Lookup API:**
  - [ ] Create `/api/barcode/lookup/<barcode>` endpoint
  - [ ] Integrate existing `barcode_lookup.py` module
  - [ ] Add `requests` dependency to web requirements
  - [ ] Handle API errors gracefully
- [ ] **Web UI Integration:**
  - [ ] Add barcode input field to "Add Bottle" form
  - [ ] Add "Lookup" button next to barcode field
  - [ ] Auto-populate form fields when product found
  - [ ] Show lookup results with confirmation
- [ ] **Enhanced UX:**
  - [ ] Camera scanning support (if possible in browser)
  - [ ] Manual UPC entry option
  - [ ] Clear indication when lookup succeeds/fails
  - [ ] Option to override auto-populated fields
- [ ] **Error Handling:**
  - [ ] Network timeout handling
  - [ ] API unavailable fallback
  - [ ] Invalid barcode feedback
  - [ ] Product not found messaging

**Acceptance Criteria:**
- Users can enter barcode manually in web UI
- Lookup button calls Open Food Facts API
- Form fields auto-populate with product data
- Clear feedback for successful lookups and errors
- Graceful fallback when API unavailable

**Considerations:**
- **Dependencies:** CLI barcode module already exists, just needs web integration
- **API Reliability:** Open Food Facts API may be slow or unavailable
- **Privacy:** No user data sent to external API (only barcode)
- **Browser Support:** Camera scanning may not work on all devices
- **Caching:** Consider caching lookup results to improve performance

**Related Issues:** Leverages ENH-002 CLI barcode functionality

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

**Last Updated:** 2025-12-01 (ENH-006, ENH-007, ENH-008, ENH-009, ENH-010 added)

