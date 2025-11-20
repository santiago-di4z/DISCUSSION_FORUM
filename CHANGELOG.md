# CHANGELOG
All notable changes to this project will be documented in this file

## Version 0.1 - Initial Project Structure
### Added
- Two core apps created: "Forum" and "Users"
- Django project initialized
- Implemented all core models: BOARD, THREAD & COMMENT (Forum); USER (User)
- ORM diagram and data dictionaries for al entities

## Version 0.2 - Authentication & User System
### Added
- User registration, login, and logout functionality.
- Basic form implementations for authentication.
- Class-Based Views (CBVs) and/or Django Auth Views for handling authentication workflows.
- Initial user stories document added to the Docs/ directory.
### Improved
- Basic validation logic for authentication forms.
- General project structure by organizing views, forms, and auth flows.
### Tests
- Added test for registration
- Added test for login
- Added test for logout

## Version 0.3 - Boards, Threads & Comments
### Added
- Functionality for creating threads within a board.
- Functionality for adding comments to existing threads.
- Board listing page to browse available discussion topics.
- Each board page now includes a New Threads section and a Popular Threads section for easier navigation.
- Visual indicator in each thread to show when a comment was posted by the original thread creator.
### Improved
- Updated the models Board, Thread, and Comment to use AutoField instead of IntegerField for primary keys.
- Added a seed_boards.py script to generate initial boards for testing and setup.
### Tests
- Added tests for thread creation flow.
- Added tests for commenting functionality.
- Added tests for board listing and activity-based popular thread ordering.

## Version 0.4 - Thread & Comment Access Restrictions
### Added
- Restriction preventing unregistered users from creating threads.
- Restriction preventing unregistered users from posting comments.
### Improved
- "HOME" button added to the header for easy navigation back to the main page.
### Tests
- Updated tests from version 0.3:
    - 2 tests verify that registered users can create threads and comments.
    - 2 tests verify that unregistered users cannot create threads or comments.