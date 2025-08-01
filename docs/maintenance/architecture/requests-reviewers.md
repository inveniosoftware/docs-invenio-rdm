# Requests Reviewers Feature

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

This guide provides detailed documentation for the requests reviewers feature implemented in commit 389b754, covering architecture, implementation details, and usage patterns.

## Overview

The reviewers feature enables assignment and management of reviewers throughout the request lifecycle in Invenio Requests. This comprehensive implementation includes frontend UI components, backend services, database schema updates, and timeline tracking capabilities.

## Architecture Components

### Backend Components

#### 1. RequestReviewersComponent
**Location:** `invenio_requests/services/requests/components.py:57`

Service layer component that handles reviewer management operations:
- **Validation**: Validates reviewer data against configuration limits and permissions
- **Event Tracking**: Creates timeline events when reviewers are added/removed/updated
- **Permissions**: Enforces reviewer-specific access control

Key methods:
- `_reviewers_updated()`: Determines event type (added/removed/updated) based on reviewer changes
- `_validate_reviewers()`: Validates reviewer data against system constraints
- `update()`: Main update method that processes reviewer changes and creates timeline events

#### 2. ReviewersUpdatedType Event
**Location:** `invenio_requests/customizations/event_types.py:134`

Custom event type for tracking reviewer changes in the timeline:
- **Type ID**: "R"
- **Payload Schema**: Supports event type, content, format, and reviewers list
- **Timeline Integration**: Creates entries when reviewers are modified

### Frontend Components

#### 1. RequestReviewers Component
**Location:** `invenio_requests/assets/semantic-ui/js/invenio_requests/request/reviewers/RequestReviewers.js`

Main React component for reviewer management:
- **Search Functionality**: Supports searching for users and groups
- **Selection Management**: Handles reviewer selection and removal
- **API Integration**: Communicates with backend through InvenioRequestsAPI

#### 2. Supporting UI Components

- **CollapsedHeader**: `components/CollapsedHeader.js` - Expandable header for reviewer section
- **ReviewerSearch**: `components/ReviewerSearch.js` - Search interface for finding reviewers
- **SelectedReviewersList**: `components/SelectedReviewersList.js` - Displays and manages selected reviewers

### Database & Schema Updates

#### 1. JSON Schema Extensions
**Location:** `invenio_requests/records/jsonschemas/requests/`

- Added `reviewers` field definition in `definitions-v1.0.0.json`
- Updated main schema in `request-v1.0.0.json` to include reviewers reference

#### 2. OpenSearch Mappings
**Locations:** `invenio_requests/records/mappings/`

Updated mappings across all versions (os-v1, os-v2, v7):
- Added dynamic templates for reviewer entity references
- Support for both user and group reviewers
- Proper indexing for search and filtering

#### 3. Entity Reference System
**Location:** `invenio_requests/records/systemfields/entity_reference.py`

Enhanced multi-entity reference support to handle reviewer entities alongside existing topic/receiver references.

## Configuration & Permissions

### Configuration Options
**Location:** `invenio_requests/config.py`

Key configuration variables:
- `REQUESTS_REVIEWERS_ENABLED`: Enable/disable reviewers feature
- `REQUESTS_REVIEWERS_MAX_NUMBER`: Maximum number of reviewers per request
- `USERS_RESOURCES_GROUPS_ENABLED`: Enable group reviewers

### Permission Generators
**Location:** `invenio_requests/services/generators.py`

New permission generators for reviewer-specific access control:
- Reviewer-based permission checks
- Integration with existing request permission system

## API Integration

### Service Extensions
**Location:** `invenio_requests/services/requests/service.py`

- Extended request service with reviewer update capabilities
- Proper validation and error handling for reviewer operations
- Integration with permission system

### Parameters & Results
**Locations:** 
- `invenio_requests/services/requests/params.py`
- `invenio_requests/services/requests/results.py`
- `invenio_requests/services/results.py`

Enhanced API parameters and result handling to support reviewer operations.

## Timeline Integration

### Event Timeline
**Location:** `invenio_requests/assets/semantic-ui/js/invenio_requests/timelineEvents/`

- Updated `timelineActionEvents.js` to handle reviewer events
- Enhanced `TimelineCommentEvent.js` for reviewer-related timeline entries

## Usage Examples

### Backend Usage

```python
# Updating reviewers through the service
reviewers = [
    {"user": "user123"},
    {"group": "editors"}
]

# This triggers validation, permission checks, and timeline events
service.update(identity, id, {"reviewers": reviewers})
```

### Frontend Integration

```javascript
// RequestReviewers component usage
<RequestReviewers
  request={request}
  permissions={permissions}
  allowGroupReviewers={true}
  maxReviewers={5}
/>
```

## Security & Validation

- **Permission Enforcement**: Only users with appropriate permissions can modify reviewers
- **Data Validation**: Validates reviewer data structure and limits
- **Configuration Respect**: Honors system-wide reviewer settings
- **Timeline Tracking**: All reviewer changes are logged in the request timeline

## Backward Compatibility

The implementation maintains full backward compatibility with existing request functionality:
- Existing requests continue to work without reviewers
- No breaking changes to existing APIs
- Optional feature that can be enabled/disabled via configuration

## Configuration Setup

To enable the reviewers feature:

1. Set `REQUESTS_REVIEWERS_ENABLED = True` in your configuration
2. Configure `REQUESTS_REVIEWERS_MAX_NUMBER` as needed (default limits apply)
3. Ensure proper permissions are set for reviewer management
4. Update request type configurations to support reviewers if needed

## Implementation Details

### Key Files Modified

The reviewers feature implementation spans 36 files with 797 additions and 49 deletions:

#### Frontend Changes (JavaScript/React)
- `InvenioRequestsApp.js` - Main app integration
- `InvenioRequestApi.js` - API client extensions
- `RequestDetails.js` - Request details page integration
- `RequestMetadata.js` - Metadata display updates
- New reviewer components in `request/reviewers/` directory

#### Backend Changes (Python)
- `components.py` - RequestReviewersComponent service layer
- `event_types.py` - ReviewersUpdatedType event implementation
- `config.py` - Configuration options and defaults
- `permissions.py` - Reviewer-specific permission generators
- Various service, API, and schema updates

#### Database Schema
- JSON schema definitions for reviewers field
- OpenSearch mappings across all versions
- Entity reference system enhancements

### Testing & Quality Assurance

The implementation includes:
- Updated test configurations and fixtures
- Comprehensive test coverage for reviewer functionality  
- Code style and linting compliance
- Error handling and validation testing

This comprehensive reviewers system provides a complete workflow for reviewer assignment, management, and tracking while maintaining the flexibility and extensibility of the Invenio Requests system.