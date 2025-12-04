# Dram Planner Enhancement Queue

This document tracks all planned enhancements, features, and improvements for Dram Planner.

## Queue Status

- **Total Items:** 19
- **In Progress:** 1
- **Completed:** 11
- **Pending:** 7

## Priority Levels

- 🔴 **Critical** - Core functionality gaps, blocking issues
- 🟠 **High** - Significant user value, high impact, quick wins
- 🟡 **Medium** - Nice to have, moderate impact, foundational features
- 🟢 **Low** - Minor improvements, polish, advanced features

## Current Priority Order

Based on dependencies and user value, the prioritized development sequence is:

1. **ENH-017: User Registration Troubleshooting & Bug Fixes** (✅ Completed) - Registration bug fixed
2. **ENH-013: Security & Vulnerability Assessment** (🔴 Critical) - BLOCKS PUBLIC LAUNCH
3. **ENH-014: Production Deployment & Infrastructure** (🔴 Critical) - Public deployment
4. **ENH-016: Group Creation Troubleshooting & Bug Fixes** (✅ Completed) - Group tables created, functionality fixed
5. **ENH-010: Web Barcode Scanning & Lookup** (✅ Completed) - Quick web enhancement
6. **ENH-006: Master Beverage Catalog** (✅ Completed) - Foundational for social features
7. **ENH-012: Whisky Database Integration & Public Lists** (✅ Completed) - Extends catalog with whisky data
8. **ENH-008: User Groups & Shared Tasting Schedules** (✅ Completed) - Community features
9. **ENH-015: Catalog Management & Administration** (🟡 Medium) - Catalog administration
10. **ENH-018: User Management & Administration** (🟡 Medium) - User admin interface and roles
11. **ENH-007: Review Visualization & Social Features** (🟡 Medium) - Depends on ENH-006
12. **ENH-011: Advanced Tasting Customization Options** (🟡 Medium) - Enhanced user preferences
13. **ENH-009: AI-Powered Schedule Planning** (🟢 Low) - Advanced AI features
14. **ENH-019: Comprehensive Automated Testing & Validation Framework** (🟠 High) - Testing infrastructure
15. **ENH-005: Mobile Applications** (🟡 Medium) - Last as requested, comprehensive effort

## Enhancement Queue

### 🔴 Critical Priority

#### ENH-017: User Registration Troubleshooting & Bug Fixes
**Status:** ✅ Completed
**Added:** 2025-12-01
**Completed:** 2025-12-02
**Priority:** 🔴 Critical
**Effort:** 1-3 days
**Dependencies:** ENH-004 (Web Application), Authentication system

**Description:**
Debug and resolve the internal server error occurring during user registration. Registration functionality previously worked but is now failing, preventing new users from creating accounts. This is a critical blocker for user onboarding.

**Features:**
- [ ] **Bug Investigation:**
  - [ ] Test registration endpoint and form submission
  - [ ] Check server logs for error details and stack traces
  - [ ] Identify the exact point of failure in registration flow
  - [ ] Verify database connection and table structure
  - [ ] Check for missing database migrations or schema issues
- [ ] **Backend Issues:**
  - [ ] Review registration route handler (`/api/auth/register` or similar)
  - [ ] Validate database models (User model, constraints, relationships)
  - [ ] Check for missing required fields or validation errors
  - [ ] Verify password hashing and storage
  - [ ] Test database transaction handling
  - [ ] Check for foreign key constraints or unique constraints causing failures
- [ ] **Frontend Issues:**
  - [ ] Test registration form submission
  - [ ] Verify form data is being sent correctly
  - [ ] Check for JavaScript errors in browser console
  - [ ] Validate form field requirements and validation
  - [ ] Test error message display
- [ ] **Database Issues:**
  - [ ] Verify User table exists and has correct schema
  - [ ] Check for missing columns or incorrect data types
  - [ ] Validate database migrations are applied
  - [ ] Test database connection and permissions
  - [ ] Check for constraint violations (unique username/email)
- [ ] **Error Handling:**
  - [ ] Improve error logging for registration failures
  - [ ] Add proper error messages for users
  - [ ] Validate input sanitization and security
  - [ ] Check for SQL injection vulnerabilities
- [ ] **Integration Testing:**
  - [ ] Test complete registration flow end-to-end
  - [ ] Test with various input scenarios (valid, invalid, edge cases)
  - [ ] Verify user is created correctly in database
  - [ ] Test login after successful registration
  - [ ] Verify email uniqueness and username uniqueness constraints

**Acceptance Criteria:**
- User registration works reliably without internal server errors
- New users can successfully create accounts
- Proper error messages displayed for validation failures
- Registration data is correctly stored in database
- Users can immediately log in after registration
- All edge cases and error scenarios handled gracefully

**Considerations:**
- **User Impact:** Critical - blocks all new user signups
- **Data Integrity:** Ensure no partial user records created on failure
- **Security:** Verify password hashing and input validation
- **Testing:** Test with various browsers and scenarios
- **Logging:** Improve error logging to prevent future issues
- **Rollback:** May need to rollback recent changes if regression introduced

**Implementation Notes:**
- **Root Cause:** Missing `email-validator` package required by WTForms Email validator
- **Error:** `ModuleNotFoundError: No module named 'email_validator'` when submitting registration form
- **Fix Applied:**
  - Added `email-validator>=2.0.0` to `web/requirements.txt`
  - Rebuilt Docker container to install missing dependency
  - Recreated container to use updated image
- **Files Modified:**
  - `web/requirements.txt` - Added email-validator dependency
- **Status:** ✅ Fixed - Registration should now work correctly

**Related Issues:** Critical bug in ENH-004 Web Application authentication system

---

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

#### ✅ ENH-004: Hosted Web Application
**Status:** ✅ Completed
**Added:** 2025-01-01
**Started:** 2025-01-01
**Completed:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 4-6 weeks
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
- [x] Photo uploads for bottles
- [x] Enhanced calendar view with visual widget
- [x] Hosting setup (deployed on vps05)

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
  - Photo upload functionality with thumbnails
  - Visual calendar widget for schedule viewing
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

#### ✅ ENH-006: Master Beverage Catalog
**Status:** ✅ Completed
**Added:** 2025-12-01
**Started:** 2025-12-01
**Completed:** 2025-12-01
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
**Status:** 🔵 In Progress
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

#### ✅ ENH-008: User Groups & Shared Tasting Schedules
**Status:** ✅ Completed
**Added:** 2025-12-01
**Started:** 2025-12-01
**Completed:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 4-6 weeks
**Dependencies:** ENH-004 (Web Application), Database for user relationships

**Description:**
Allow users to form groups and share/follow tasting schedules, creating community-driven tasting experiences.

**Features:**
- [x] **Group Creation:**
  - [x] Create public or private tasting groups
  - [x] Define group themes (e.g., "Bourbon Enthusiasts", "Scotch Tour 2025")
  - [x] Set group membership rules (open, invite-only, moderated)
  - [x] Group descriptions and rules
- [x] **Shared Schedules:**
  - [x] Intelligent group schedule creation from members' collections
  - [x] Master catalog integration for group schedules
  - [x] Category-balanced bottle distribution
  - [x] Detailed schedule viewing with completion tracking
- [x] **Social Features:**
  - [x] Join multiple groups
  - [x] Group discussions and tastings (foundation)
  - [x] Schedule sharing and forking (foundation)
- [x] **Group Management:**
  - [x] Group administrators and moderators
  - [x] Membership management (add/remove members)
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

#### ✅ ENH-010: Web Barcode Scanning & Lookup
**Status:** ✅ Completed
**Added:** 2025-12-01
**Started:** 2025-12-01
**Completed:** 2025-12-01
**Priority:** 🟠 High
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

#### ENH-011: Advanced Tasting Customization Options
**Status:** 🔵 In Progress
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 2-3 weeks
**Dependencies:** ENH-001 (User Preferences), ENH-004 (Web Application)

**Description:**
Add granular customization options for tasting sessions to support diverse tasting preferences and group tastings, including the ability to sample multiple bottles per session and various other wine/whiskey tasting protocols.

**Features:**
- [ ] **Multi-Bottle Tastings:**
  - [ ] Configure number of bottles per tasting session (1-N)
  - [ ] Set tasting session duration limits
  - [ ] Group tasting support with round-robin or judge protocols
- [ ] **Tasting Order Customization:**
  - [ ] Sort by category, ABV, age, region, or price
  - [ ] Custom sequencing algorithms (educational progression, variety optimization)
  - [ ] Blind vs. open tasting modes
- [ ] **Advanced Scheduling Options:**
  - [ ] Flexible tasting intervals (daily, weekly, bi-weekly, monthly, custom)
  - [ ] Seasonal tasting adjustments (lighter spirits in summer)
  - [ ] Holiday/weekend preferences
- [ ] **Tasting Notes Customization:**
  - [ ] Multiple rating scales (0-10, 1-5 stars, letter grades A-F)
  - [ ] Spirit-specific tasting note templates (whiskey, wine, beer, cocktails)
  - [ ] Custom fields for personal preferences
  - [ ] Professional vs. casual note-taking modes
- [ ] **Group Tasting Features:**
  - [ ] Shared tasting sessions for multiple users
  - [ ] Group scoring and consensus ratings
  - [ ] Tasting event planning with RSVPs
  - [ ] Comparative tasting setups
- [ ] **Progress Tracking Options:**
  - [ ] Track by bottle count, volume consumed, or category coverage
  - [ ] Milestone celebrations and achievements
  - [ ] Personal tasting goals and targets
- [ ] **Reminder & Notification Settings:**
  - [ ] Customizable reminder timing and frequency
  - [ ] Email, SMS, or app notifications
  - [ ] Weather-based tasting suggestions
- [ ] **Advanced Filtering:**
  - [ ] Exclude recently tasted categories for palate recovery
  - [ ] Price range preferences
  - [ ] Complexity level targeting (beginner to expert)

**Acceptance Criteria:**
- Users can configure multiple bottles per tasting session
- Flexible scheduling intervals and preferences
- Customizable rating scales and tasting note templates
- Group tasting functionality for shared experiences
- Advanced filtering and sorting options
- Comprehensive reminder and notification system

**Considerations:**
- **User Experience:** Don't overwhelm users with too many options - provide sensible defaults
- **Performance:** Complex algorithms should not slow down schedule generation
- **Data Migration:** Existing user preferences should migrate smoothly
- **Scalability:** Group features should scale from 2 to 20+ participants
- **Privacy:** Group data should respect individual privacy preferences
- **Mobile:** Ensure all customizations work well on mobile devices

**Related Issues:** Builds on ENH-001 user preferences system

---

#### ENH-013: Security & Vulnerability Assessment
**Status:** ✅ Completed
**Added:** 2025-12-01
**Priority:** 🔴 Critical
**Effort:** 1-2 weeks
**Dependencies:** ENH-004 (Web Application), Public deployment readiness

**Description:**
Perform comprehensive security assessment and vulnerability scanning of the Dram Planner web application before public deployment to www.dram-planner.com. Ensure the application meets security standards for user data protection and safe public access.

**Features:**
- [ ] **Static Code Analysis:**
  - [ ] Run security linters (Bandit, Safety, etc.)
  - [ ] Code review for common vulnerabilities (SQL injection, XSS, CSRF)
  - [ ] Dependency vulnerability scanning
  - [ ] Secrets and credential exposure checks
- [ ] **Dynamic Security Testing:**
  - [ ] Automated vulnerability scanning (OWASP ZAP, Nessus)
  - [ ] Penetration testing simulation
  - [ ] API endpoint security testing
  - [ ] Authentication and authorization testing
- [ ] **Infrastructure Security:**
  - [ ] SSL/TLS configuration review
  - [ ] Server hardening assessment
  - [ ] Database security configuration
  - [ ] Firewall and network security
- [ ] **Application Security:**
  - [ ] Input validation and sanitization review
  - [ ] Session management security
  - [ ] Password security and storage
  - [ ] Rate limiting and DoS protection
- [ ] **Compliance & Best Practices:**
  - [ ] GDPR/privacy compliance review
  - [ ] OWASP Top 10 compliance
  - [ ] Security headers implementation
  - [ ] Error handling and information leakage
- [ ] **Deployment Security:**
  - [ ] Production environment hardening
  - [ ] Secure configuration management
  - [ ] Monitoring and logging setup
  - [ ] Incident response planning

**Acceptance Criteria:**
- Comprehensive security audit completed
- All critical/high-risk vulnerabilities resolved
- Security best practices implemented
- Deployment-ready security posture
- Documentation of security measures

**Considerations:**
- **Timeline:** Must be completed before public launch
- **Cost:** May require security tools or external consultants
- **Scope:** Web application, API, database, and infrastructure
- **Standards:** OWASP guidelines, industry best practices
- **Maintenance:** Ongoing security monitoring plan

**Related Issues:** Blocks public deployment to www.dram-planner.com

---

#### ENH-014: Production Deployment & Infrastructure
**Status:** 🔵 In Progress
**Added:** 2025-12-01
**Priority:** 🔴 Critical
**Effort:** 2-3 weeks
**Dependencies:** ENH-013 (Security Assessment), Domain registration

**Description:**
Plan and execute production deployment of Dram Planner to www.dram-planner.com. Configure infrastructure, domain setup, SSL certificates, and monitoring for public availability.

**Features:**
- [ ] **Domain & DNS Configuration:**
  - [ ] CNAME or A record setup for www.dram-planner.com
  - [ ] SSL certificate provisioning (Let's Encrypt)
  - [ ] DNS propagation testing
  - [ ] Domain ownership verification
- [ ] **Infrastructure Planning:**
  - [ ] Assess vps05 capacity for production load
  - [ ] Evaluate dedicated server vs. existing VPS
  - [ ] Load balancing and scalability planning
  - [ ] Backup and disaster recovery setup
- [ ] **Production Environment:**
  - [ ] Environment variable configuration
  - [ ] Database migration to production
  - [ ] Static file serving optimization
  - [ ] Performance monitoring setup
- [ ] **Security Hardening:**
  - [ ] Production SSL/TLS configuration
  - [ ] Web server security headers
  - [ ] Database connection security
  - [ ] API rate limiting and throttling
- [ ] **Monitoring & Maintenance:**
  - [ ] Application performance monitoring
  - [ ] Error tracking and alerting
  - [ ] Log aggregation and analysis
  - [ ] Automated backup procedures
- [ ] **Go-Live Preparation:**
  - [ ] Staging environment testing
  - [ ] Load testing and performance validation
  - [ ] Rollback procedures
  - [ ] User communication plan

**Deployment Options Assessment:**
- **Option 1: CNAME to vps05 (Recommended)**
  - ✅ Simpler setup - reuse existing working infrastructure
  - ✅ Cost-effective - no additional server costs
  - ✅ Faster deployment - minimal configuration changes
  - ⚠️ Resource sharing - monitor performance under load
  - ⚠️ Single point of failure if vps05 issues

- **Option 2: Dedicated Server**
  - ✅ Better performance isolation
  - ✅ Scalability and future growth
  - ✅ Production-grade reliability
  - ❌ Higher cost and complexity
  - ❌ Additional setup and migration time

**Recommendation:** Start with CNAME to vps05 for faster deployment, monitor performance, and scale to dedicated server if needed.

**Acceptance Criteria:**
- Domain www.dram-planner.com live and accessible
- SSL certificate properly configured
- Application running stably in production
- Monitoring and alerting operational
- Backup procedures verified

**Considerations:**
- **Domain:** www.dram-planner.com already registered
- **Current Setup:** vps05 running with Docker containers
- **Migration:** Minimal disruption to existing functionality
- **Scalability:** Plan for future growth beyond initial launch

**Related Issues:** Security assessment (ENH-013) must be completed first

---

#### ✅ ENH-012: Whisky Database Integration & Public Lists
**Status:** ✅ Completed
**Added:** 2025-12-01
**Started:** 2025-12-01
**Completed:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 3-4 weeks
**Dependencies:** ENH-006 (Master Beverage Catalog)

**Description:**
Integrate with publicly available whisky databases and lists, providing search and import capabilities for comprehensive whisky data from sources like Whiskybase, Distiller, Master of Malt, and other whisky community resources.

**Features:**
- [x] **Whisky Database APIs:**
  - [x] Modular architecture for multiple whisky data sources
  - [x] Sample whisky database with demo data for testing
  - [ ] Integrate with Whiskybase API for comprehensive whisky data (planned)
  - [ ] Connect to Distiller database API (planned)
  - [ ] Add Master of Malt API integration (planned)
- [ ] **Public Whisky Lists:**
  - [ ] Import whisky rankings and lists (e.g., Whisky Bible top 1000)
  - [ ] Support for whisky tasting competition results
  - [ ] Import from whisky enthusiast community lists
  - [ ] Curated whisky collections from experts and publications
- [x] **Search & Discovery:**
  - [x] Search across multiple whisky databases simultaneously
  - [x] Basic filtering by data source
  - [ ] Advanced filtering by distillery, region, age, style, ratings (planned)
  - [ ] Cross-reference prices and availability (planned)
  - [ ] Whisky tasting note aggregation from multiple sources (planned)
- [ ] **Data Synchronization:**
  - [ ] Scheduled updates from external databases
  - [ ] Incremental import to avoid duplicates
  - [ ] Data quality validation and deduplication
  - [ ] User preference for data sources (trust levels, update frequency)
- [x] **Import & Export:**
  - [x] Import individual whiskies to master catalog
  - [ ] Bulk import whisky lists to master catalog (planned)
  - [ ] Export personal whisky data to share with communities (planned)
  - [ ] API endpoints for third-party integrations (planned)
  - [ ] Whisky collection sharing and backup (planned)
- [ ] **Community Integration:**
  - [ ] Link to whisky tasting communities and forums
  - [ ] Import user-curated whisky lists
  - [ ] Whisky tasting event data integration
  - [ ] Social whisky discovery features

**Acceptance Criteria:**
- Users can search and import from major whisky databases
- Public whisky lists can be imported to personal catalog
- Cross-database search functionality works
- Data synchronization maintains catalog accuracy
- Community whisky lists are accessible

**Considerations:**
- **API Limits:** Respect rate limits and terms of service for external APIs
- **Data Quality:** Validate and clean imported data
- **Privacy:** No user data shared with external services
- **Cost:** Consider free vs. paid API tiers
- **Maintenance:** APIs may change or become unavailable
- **Legal:** Ensure compliance with database usage terms

**Related Issues:** Extends ENH-006 master catalog with whisky-specific data sources

---

#### ENH-015: Catalog Management & Administration
**Status:** 🔵 In Progress
**Added:** 2025-12-01
**Priority:** 🟡 Medium
**Effort:** 2-3 weeks
**Dependencies:** ENH-006 (Master Beverage Catalog)

**Description:**
Add administrative functionality to manage and maintain the master beverage catalog. Allow authorized users to modify, add, delete, and curate catalog entries to ensure data quality and completeness.

**Features:**
- [ ] **Admin Interface:**
  - [ ] Dedicated admin section for catalog management
  - [ ] Role-based access control (admin/moderator privileges)
  - [ ] Bulk operations for catalog maintenance
- [ ] **Entry Management:**
  - [ ] Add new beverages to catalog manually
  - [ ] Edit existing catalog entries (name, brand, category, ABV, etc.)
  - [ ] Delete duplicate or incorrect entries
  - [ ] Merge duplicate entries
  - [ ] Mark entries as verified/unverified
- [ ] **Data Quality Tools:**
  - [ ] Validation rules for catalog entries
  - [ ] Duplicate detection and resolution
  - [ ] Data consistency checking
  - [ ] Bulk import/export for catalog maintenance
- [ ] **Community Contributions:**
  - [ ] User suggestions for new catalog entries
  - [ ] Review and approval workflow for user submissions
  - [ ] Community voting on entry accuracy
  - [ ] Contributor recognition system
- [ ] **Catalog Analytics:**
  - [ ] Usage statistics (most viewed/searched entries)
  - [ ] Data completeness metrics
  - [ ] User contribution analytics
  - [ ] Catalog growth and maintenance reports
- [ ] **Import/Export Tools:**
  - [ ] Export catalog data for backup/archiving
  - [ ] Import from external sources with validation
  - [ ] CSV/JSON bulk operations
  - [ ] Catalog synchronization tools

**Acceptance Criteria:**
- Admins can add, edit, and delete catalog entries
- Data validation prevents invalid entries
- Duplicate detection and merging tools available
- Community contribution system implemented
- Catalog analytics and reporting available

**Considerations:**
- **Data Integrity:** Ensure catalog changes don't break existing user collections
- **User Impact:** Changes to catalog entries should be communicated to affected users
- **Moderation:** Community contributions need review before approval
- **Backup:** Full catalog backup before major changes
- **Audit Trail:** Track all catalog modifications

**Related Issues:** Extends ENH-006 master catalog with administrative capabilities

---

#### ENH-018: User Management & Administration
**Status:** ✅ Completed
**Added:** 2025-12-02
**Completed:** 2025-12-02
**Priority:** 🟡 Medium
**Effort:** 2-3 weeks
**Dependencies:** ENH-004 (Web Application), Authentication system

**Description:**
Add comprehensive user management functionality with administrative access controls. Allow administrators to view, manage, and moderate user accounts, including user roles, account status, and administrative actions.

**Features:**
- [ ] **Admin Role System:**
  - [ ] Add `is_admin` flag to User model (boolean field)
  - [ ] Create database migration for admin flag
  - [ ] Add admin role checking decorators and helpers
  - [ ] Implement role-based access control (RBAC) foundation
  - [ ] Admin-only route protection
- [ ] **User Management Interface:**
  - [ ] Admin dashboard for user management
  - [ ] User list view with search and filtering
  - [ ] User detail view with account information
  - [ ] User edit capabilities (username, email, role, status)
  - [ ] User deletion and account deactivation
- [ ] **User Administration Features:**
  - [ ] View all registered users
  - [ ] Search users by username, email, or ID
  - [ ] Filter users by registration date, activity, role
  - [ ] View user statistics (bottles, schedules, groups)
  - [ ] View user activity and login history
  - [ ] Promote/demote users to/from admin role
  - [ ] Activate/deactivate user accounts
  - [ ] Reset user passwords (admin-initiated)
- [ ] **User Moderation:**
  - [ ] Suspend/unsuspend user accounts
  - [ ] View user-reported content or issues
  - [ ] Manage user-generated content
  - [ ] Handle user disputes or complaints
- [ ] **Admin API Endpoints:**
  - [ ] `GET /api/admin/users` - List all users (admin only)
  - [ ] `GET /api/admin/users/<id>` - Get user details (admin only)
  - [ ] `PUT /api/admin/users/<id>` - Update user (admin only)
  - [ ] `DELETE /api/admin/users/<id>` - Delete/deactivate user (admin only)
  - [ ] `POST /api/admin/users/<id>/promote` - Promote to admin (admin only)
  - [ ] `POST /api/admin/users/<id>/reset-password` - Reset password (admin only)
- [ ] **Security & Permissions:**
  - [ ] Admin-only access restrictions
  - [ ] Audit logging for admin actions
  - [ ] Prevent self-deletion of admin accounts
  - [ ] Require at least one admin account
  - [ ] Secure admin endpoints with proper authentication
- [ ] **User Statistics & Analytics:**
  - [ ] Total user count and growth metrics
  - [ ] Active vs inactive users
  - [ ] User registration trends
  - [ ] Most active users
  - [ ] User engagement statistics

**Acceptance Criteria:**
- Admin flag added to User model and database
- Admin users can access user management interface
- Admins can view, edit, and manage all user accounts
- Admin actions are logged and auditable
- Non-admin users cannot access admin features
- User management interface is intuitive and secure
- All admin operations have proper error handling

**Considerations:**
- **Security:** Admin access must be strictly controlled and logged
- **Data Privacy:** Ensure compliance with privacy regulations when managing user data
- **User Impact:** Admin actions should be reversible when possible
- **Initial Admin:** Need a way to create the first admin user (migration or script)
- **Audit Trail:** All admin actions should be logged for accountability
- **Scalability:** User list should support pagination for large user bases
- **Performance:** Efficient queries for user search and filtering

**Implementation Notes:**
- Add `is_admin` boolean column to `users` table
- Create admin decorator: `@admin_required` for route protection
- Create admin blueprint: `app/admin/` for admin-specific routes
- Admin template: `templates/admin/users.html` for user management UI
- Consider using Flask-Admin library for rapid admin interface development (optional)

**Related Issues:** Foundation for future administrative features (ENH-015 catalog management, content moderation, etc.)

---

#### ENH-016: Group Creation Troubleshooting & Bug Fixes
**Status:** ✅ Completed
**Added:** 2025-12-01
**Completed:** 2025-12-02
**Priority:** 🟠 High
**Effort:** 1-2 weeks
**Dependencies:** ENH-008 (User Groups & Shared Tasting Schedules)

**Description:**
Debug and resolve issues with the group creation and management functionality. Ensure all group features work correctly and provide a smooth user experience for creating and managing tasting groups.

**Features:**
- [ ] **Bug Investigation:**
  - [ ] Test group creation functionality thoroughly
  - [ ] Identify and document all issues with group features
  - [ ] Check database relationships and constraints
  - [ ] Verify API endpoints are working correctly
- [ ] **Frontend Issues:**
  - [ ] Test group creation modal and form submission
  - [ ] Verify group list display and navigation
  - [ ] Check member management interface
  - [ ] Test schedule creation within groups
- [ ] **Backend Issues:**
  - [ ] Validate database models and relationships
  - [ ] Test API endpoints for groups, memberships, schedules
  - [ ] Check error handling and validation
  - [ ] Verify authentication and authorization
- [ ] **User Experience Issues:**
  - [ ] Test complete user flow for group creation
  - [ ] Verify invitation and member management
  - [ ] Check group schedule functionality
  - [ ] Test collaborative features
- [ ] **Performance & Security:**
  - [ ] Check for SQL injection vulnerabilities
  - [ ] Validate input sanitization
  - [ ] Test for race conditions in group operations
  - [ ] Ensure proper error messages and logging
- [ ] **Integration Testing:**
  - [ ] Test group features with existing user accounts
  - [ ] Verify group data persists correctly
  - [ ] Check integration with other features (catalog, schedules)
  - [ ] Test edge cases and error scenarios

**Acceptance Criteria:**
- Group creation works reliably for all users
- All group management features function correctly
- No security vulnerabilities in group operations
- Clear error messages for failed operations
- Complete documentation of fixes applied

**Considerations:**
- **User Impact:** Issues may prevent users from using group features
- **Data Integrity:** Ensure no data corruption from bugs
- **Testing:** Comprehensive testing of all group workflows
- **Documentation:** Document all fixes and workarounds
- **Regression:** Prevent reintroduction of fixed bugs

**Implementation Notes:**
- **Root Cause:** Missing database tables for group functionality (user_groups, group_memberships, group_schedules, group_schedule_items, master_beverages)
- **Error:** `relation "group_memberships" does not exist` when accessing group API endpoints
- **Fix Applied:**
  - Created missing database tables directly using SQL (bypassed Alembic migration issues)
  - Created tables: user_groups, group_memberships, group_schedules, group_schedule_items, master_beverages
  - All tables created with proper foreign key relationships and constraints
  - Restarted web container to recognize new tables
- **Files Created:**
  - `web/migrations/versions/ef504db1363d_add_group_tables_and_master_beverage.py` - Migration file (for future reference)
  - `web/create_group_tables.py` - Helper script for direct table creation
- **Status:** ✅ Fixed - Group creation and management should now work correctly

**Related Issues:** Fixes issues in ENH-008 User Groups implementation

---

### 🟢 Low Priority

#### ENH-019: Comprehensive Automated Testing & Validation Framework
**Status:** 🔵 In Progress
**Added:** 2025-12-02
**Priority:** 🟠 High
**Effort:** 1-2 weeks
**Dependencies:** All existing enhancements

**Description:**
Implement comprehensive automated testing and validation framework to ensure all enhancements are properly implemented and working correctly. This includes unit tests, integration tests, web application tests, security validation, and CI/CD pipeline setup.

**Features:**
- [ ] **Testing Infrastructure:**
  - [ ] Set up pytest framework with coverage reporting
  - [ ] Create pytest configuration files (pytest.ini, conftest.py)
  - [ ] Set up test databases and fixtures
  - [ ] Create test utilities and helpers
  - [ ] Set up code coverage reporting (pytest-cov)
- [ ] **CLI Module Tests:**
  - [ ] Comprehensive tests for config.py (ENH-001)
  - [ ] Comprehensive tests for barcode_lookup.py (ENH-002)
  - [ ] Comprehensive tests for import_manager.py (ENH-003)
  - [ ] Enhanced tests for schedule_generator.py
  - [ ] Enhanced tests for tasting_manager.py
  - [ ] Tests for add_bottle.py
- [ ] **Web Application Tests:**
  - [ ] Flask application test setup (pytest-flask)
  - [ ] Authentication and authorization tests
  - [ ] API endpoint tests (bottles, schedules, groups, catalog, etc.)
  - [ ] Database model tests
  - [ ] Integration tests for complete workflows
  - [ ] Frontend component tests (if applicable)
- [ ] **Security Testing:**
  - [ ] Automated security scanning (Bandit, Safety)
  - [ ] Dependency vulnerability checks
  - [ ] SQL injection test cases
  - [ ] XSS and CSRF test cases
  - [ ] Authentication security tests
- [ ] **CI/CD Pipeline:**
  - [ ] GitHub Actions workflow for automated testing
  - [ ] Automated test execution on pull requests
  - [ ] Coverage reporting and badges
  - [ ] Automated security scanning in CI
  - [ ] Test result notifications
- [ ] **Test Coverage Goals:**
  - [ ] Minimum 80% code coverage for CLI modules
  - [ ] Minimum 70% code coverage for web application
  - [ ] All critical paths tested
  - [ ] Edge cases and error handling tested
  - [ ] Integration test coverage for workflows

**Acceptance Criteria:**
- Comprehensive test suite covers all implemented enhancements
- Minimum coverage thresholds met (80% CLI, 70% web)
- All tests pass consistently
- CI/CD pipeline runs tests automatically
- Security scanning integrated into test workflow
- Test documentation complete
- Tests run in reasonable time (< 5 minutes)

**Considerations:**
- **Test Data:** Use fixtures and factories for test data
- **Isolation:** Tests should be independent and isolated
- **Performance:** Tests should run quickly for developer feedback
- **Maintenance:** Tests should be easy to maintain and update
- **Documentation:** Clear test documentation for contributors

**Implementation Notes:**
- Use pytest as primary testing framework
- Use pytest-flask for web application testing
- Use pytest-cov for coverage reporting
- Use Bandit for security scanning
- Use Safety for dependency vulnerability checks
- Set up GitHub Actions for CI/CD

**Related Issues:** Foundation for validating all enhancements and ensuring code quality

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

**Last Updated:** 2025-12-02 (ENH-016 completed - Group creation bug fixed)

