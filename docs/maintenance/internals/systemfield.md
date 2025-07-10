# System fields

## Overview

System fields are a powerful abstraction layer in InvenioRDM that provide managed access to record data through Python descriptors. They bridge the gap between the raw JSON dictionary structure of records and object-oriented Python interfaces, enabling sophisticated data management, validation, and integration with related objects.

At its core, System fields transform simple attribute access (`record.title`) into complex operations that can involve:

- Data validation and transformation
- Integration with external services and databases
- Caching and performance optimization
- Record lifecycle event handling
- Denormalization and data synchronization

## Architecture and core concepts

Every system field inherits from `SystemField`, which implements Python's descriptor protocol (`__get__`, `__set__`, `__set_name__`). This allows fields to intercept attribute access and customize behavior:

```python
class MyRecord(Record, SystemFieldsMixin):
    title = ConstantField('metadata.title', 'Default Title')

# record.title calls ConstantField.__get__
# record.title = "New Title" calls ConstantField.__set__
```

### Mixin and Metaclass

The `SystemFieldsMixin` uses the `SystemFieldsMeta` metaclass to automatically:

1. Discover all SystemField instances on the class
2. Respect inheritance (fields from parent classes are included)
3. Handle lifecycle events and set field names

### Record Lifecycle Integration

SystemFields hook into the record lifecycle through the extension system:

- `pre_init` / `post_init`: Record creation and initialization
- `pre_dump` / `post_dump`: Serialization to JSON
- `pre_load` / `post_load`: Deserialization from JSON
- `pre_create` / `post_create`: Database creation
- `pre_commit` / `post_commit`: Database transaction commit
- `pre_delete` / `post_delete`: Record deletion
- `pre_revert` / `post_revert`: Record version reversion

### When to Use SystemFields

**Use SystemFields when you need to:**

1. **Integrate with External Systems**: Connect record fields to databases, APIs, or services
2. **Add Validation Logic**: Implement complex validation that goes beyond JSON schema
3. **Manage Related Objects**: Handle relationships between records and other entities
4. **Optimize Performance**: Implement caching, denormalization, or lazy loading
5. **Enforce Business Rules**: Add custom logic that must run during record operations
6. **Provide Clean APIs**: Hide complexity behind simple attribute access

### When NOT to Use SystemFields

**Avoid SystemFields when:**

1. **Simple Data Storage**: For basic key-value storage, use the record dictionary directly
2. **Performance Critical Paths**: The descriptor overhead may impact performance
3. **Temporary Calculations**: For ephemeral data that doesn't need persistence
4. **External Processing**: When data transformation happens outside the record lifecycle

### Why Choose SystemFields Over Alternatives

**Advantages:**

- **Transparent Integration**: Fields look like normal Python attributes
- **Lifecycle Hooks**: Automatic integration with record operations
- **Caching Built-in**: Automatic caching mechanisms available

**Trade-offs:**

- **Complexity**: Adds abstraction layers
- **Performance Overhead**: Descriptor calls have overhead
- **Debugging Difficulty**: Magic behavior can be hard to trace
- **Learning Curve**: Requires understanding of descriptors and metaclasses

## Building your own SystemField

### Basic custom field example

```python
from invenio_records.api import Record
from invenio_records.systemfields import SystemField, SystemFieldsMixin
class UppercaseField(SystemField):
    """A field that automatically converts values to uppercase."""

    def __get__(self, record, owner=None):
        if record is None:
            return self  # Class-level access

        # instance-level access
        # Get value from record dictionary
        value = self.get_dictkey(record)
        return value.upper() if value else None

    def __set__(self, record, value):
        if value is not None:
            # Store lowercase in record, display uppercase
            self.set_dictkey(record, value.lower(), create_if_missing=True)

# Usage in the API class
class MyRecord(Record, SystemFieldsMixin):
    title = UppercaseField('metadata.title')

record = MyRecord({'metadata': {'title': 'hello world'}})
print(MyRecord.title)  # <__main__.UppercaseField object at 0x7b9a3ec49fd0>
print(record.title)  # "HELLO WORLD"
record.title = "New Title"
print(record['metadata']['title']) # "new title"
```

### Advanced Field with Lifecycle Hooks

```python
from invenio_records.api import Record
from invenio_records.systemfields import SystemField, SystemFieldsMixin

class TimestampField(SystemField):
    """A field that tracks creation and modification times."""

    def __init__(self, creation_key='created', modified_key='modified'):
        super().__init__()
        self.creation_key = creation_key
        self.modified_key = modified_key

    def __get__(self, record, owner=None):
        if record is None:
            return self

        return {
            'created': record.get(self.creation_key),
            'modified': record.get(self.modified_key)
        }

    def __set__(self, record, value):
        # Don't allow direct setting
        raise AttributeError("Timestamps are managed automatically")

    def post_init(self, record, data, model=None, field_data=None):
        """Set creation timestamp on new records."""
        from datetime import datetime
        now = datetime.utcnow().isoformat()

        if self.creation_key not in record:
            record[self.creation_key] = now
        record[self.modified_key] = now

    def pre_commit(self, record):
        """Update modification timestamp before saving."""
        from datetime import datetime
        record[self.modified_key] = datetime.utcnow().isoformat()

# Usage
class MyRecord(Record, SystemFieldsMixin):
    timestamps = TimestampField()

record = MyRecord({})  # Automatically sets created/modified
# ... later modifications will update modified timestamp
```

## Relations

Relations are specialized SystemFields that manage connections between records and other entities (other records, database models, APIs, etc.).

### Basic Relation Concepts

Relations consist of several components:

- **RelationsField**: The main system field that manages multiple relations
- **Relation Classes**: Define how to resolve and validate specific relation types
- **Result Classes**: Handle the returned values when accessing relations
- **Mapping Class**: Provides the interface for managing relations on a record

### Primary Key Relations (PKRelation)

```python
from invenio_records.systemfields.relations import RelationsField, PKRelation

class ArticleRecord(Record, SystemFieldsMixin):
    relations = RelationsField(
        # Connect to other ArticleRecords by ID
        parent=PKRelation(
            'metadata.parent',
            record_cls=ArticleRecord
        ),
        # Connect to User records
        creator=PKRelation(
            'metadata.creator_id',
            record_cls=User
        )
    )

# Usage
article = ArticleRecord({'metadata': {'creator_id': 'user123'}})
creator = article.relations.creator()  # Returns User record instance
article.relations.parent = parent_article  # Set relation
```

### List Relations for Multiple Connections

```python
from invenio_records.systemfields.relations import PKListRelation

class ArticleRecord(Record, SystemFieldsMixin):
    relations = RelationsField(
        # Multiple authors
        authors=PKListRelation(
            'metadata.authors',
            record_cls=User
        ),
        # Multiple subjects/tags
        subjects=PKListRelation(
            'metadata.subjects',
            record_cls=Subject
        )
    )

# Usage
article.relations.authors = [user1, user2, user3]  # Set multiple
for author in article.relations.authors():  # Iterate resolved records
    print(author.name)
```

### Custom Relations

You can create custom relation types for specific integration needs:

```python
from invenio_records.systemfields.relations import RelationBase

class APIRelation(RelationBase):
    """Relation that fetches data from an external API."""

    def __init__(self, key, api_endpoint, **kwargs):
        super().__init__(key, **kwargs)
        self.api_endpoint = api_endpoint

    def resolve(self, id_):
        """Fetch object from external API."""
        if id_ in self.cache:
            return self.cache[id_]

        import requests
        response = requests.get(f"{self.api_endpoint}/{id_}")
        if response.status_code == 200:
            obj = response.json()
            self.cache[id_] = obj
            return obj
        return None

    def exists(self, id_):
        """Check if the external resource exists."""
        import requests
        response = requests.head(f"{self.api_endpoint}/{id_}")
        return response.status_code == 200

# Usage
class ArticleRecord(Record, SystemFieldsMixin):
    relations = RelationsField(
        external_author=APIRelation(
            'metadata.external_author_id',
            api_endpoint='https://api.example.com/authors'
        )
    )
```

## Performance Optimization Strategies

### Caching

SystemFields provide built-in caching mechanisms to avoid repeated expensive operations:

#### Field-Level Caching

```python
class ExpensiveField(SystemField):
    def __get__(self, record, owner=None):
        if record is None:
            return self

        # Check if value is already cached
        cached = self._get_cache(record)
        if cached is not None:
            return cached

        # Perform expensive operation
        value = self.expensive_computation(record)

        # Cache the result
        self._set_cache(record, value)
        return value

    def expensive_computation(self, record):
        # Simulate expensive operation
        import time
        time.sleep(1)
        return f"Computed value for {record.id}"
```

#### Relation Caching

Relations automatically cache resolved objects to avoid repeated database queries:

```python
# First access hits the database
author = article.relations.creator()

# Subsequent accesses use cached version
same_author = article.relations.creator()  # No database query
```

### Denormalization for Performance

Denormalization stores computed or related data directly in the record for fast access:

```python
class DenormalizedRelation(SystemField):
    """Stores related data directly in the record."""

    def dereference(self, record):
        """Copy data from related records into this record."""
        creator_id = record['metadata']['creator_id']
        creator = User.get_record(creator_id)

        # Store creator data directly in record
        record.setdefault('metadata', {})['creator'] = {
            'id': creator.id,
            'name': creator['name'],
            'email': creator['email'],
            '@v': f"{creator.id}::{creator.revision_id}"  # Version for staleness detection
        }

    def clean(self, record):
        """Remove denormalized data, keeping only the ID."""
        creator_data = record.get('metadata', {}).get('creator', {})
        creator_id = creator_data.get('id')
        if creator_id:
            record['metadata']['creator'] = {'id': creator_id}
```

### Handling Stale Data

When using denormalization, you need strategies to handle stale data:

```python
from elasticsearch_dsl import Search

def reindex_stale_records():
    """Find and reindex records with stale denormalized data."""

    # Find records with outdated version stamps
    search = Search(index='records')

    # Query for records where the version doesn't match current
    for hit in search.scan():
        record_data = hit.to_dict()
        creator_data = record_data.get('metadata', {}).get('creator', {})
        version_stamp = creator_data.get('@v', '')

        if version_stamp:
            creator_id, revision_id = version_stamp.split('::')
            current_creator = User.get_record(creator_id)

            if str(current_creator.revision_id) != revision_id:
                # Record has stale data, reindex it
                record = MyRecord.get_record(hit.meta.id)
                record.relations.creator.dereference()
                record.commit()
```

## JSON vs Python: Data Format Considerations

### JSON Storage Format

SystemFields ultimately store data in the record's JSON dictionary. Consider how your field's data will be serialized:

```python
class DateField(SystemField):
    """Field that handles date objects."""

    def __get__(self, record, owner=None):
        if record is None:
            return self

        date_str = self.get_dictkey(record)
        if date_str:
            from datetime import datetime
            return datetime.fromisoformat(date_str)
        return None

    def __set__(self, record, value):
        if value is not None:
            from datetime import datetime
            if isinstance(value, datetime):
                # Store as ISO string in JSON
                self.set_dictkey(record, value.isoformat(), create_if_missing=True)
            elif isinstance(value, str):
                # Validate string format
                datetime.fromisoformat(value)  # Raises if invalid
                self.set_dictkey(record, value, create_if_missing=True)
            else:
                raise ValueError("Date must be datetime object or ISO string")
```

### Handling Complex Objects

For complex objects that don't serialize naturally to JSON:

```python
class GeolocationField(SystemField):
    """Field for geographic coordinates."""

    class GeoPoint:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

        def to_dict(self):
            return {'lat': self.lat, 'lon': self.lon}

        @classmethod
        def from_dict(cls, data):
            return cls(data['lat'], data['lon'])

    def __get__(self, record, owner=None):
        if record is None:
            return self

        data = self.get_dictkey(record)
        if data:
            return self.GeoPoint.from_dict(data)
        return None

    def __set__(self, record, value):
        if value is not None:
            if isinstance(value, self.GeoPoint):
                self.set_dictkey(record, value.to_dict(), create_if_missing=True)
            else:
                raise ValueError("Value must be GeoPoint instance")
```

## Idempotence and Data Consistency

SystemFields are designed to be idempotent - running the same operation multiple times should produce the same result:

```python
class IdempotentComputedField(SystemField):
    """Field that computes values idempotently."""

    def __get__(self, record, owner=None):
        if record is None:
            return self

        # Check if value is already computed and valid
        computed_data = record.get('_computed', {})
        if self.attr_name in computed_data:
            stored_hash = computed_data[self.attr_name]['hash']
            current_hash = self._compute_input_hash(record)

            if stored_hash == current_hash:
                # Data hasn't changed, return cached result
                return computed_data[self.attr_name]['value']

        # Compute new value
        value = self._compute_value(record)

        # Store with hash for future idempotence checks
        record.setdefault('_computed', {})[self.attr_name] = {
            'value': value,
            'hash': self._compute_input_hash(record)
        }

        return value

    def _compute_input_hash(self, record):
        """Hash the input data used for computation."""

        # Hash relevant fields that affect the computation
        relevant_data = {
            'title': record.get('metadata', {}).get('title'),
            'authors': record.get('metadata', {}).get('authors', [])
        }

        data_str = json.dumps(relevant_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()

    def _compute_value(self, record):
        """Perform the actual computation."""
        # Example: compute a search-friendly version of the title
        title = record.get('metadata', {}).get('title', '')
        return title.lower().replace(' ', '_')
```

## Record Lifecycle Hooks Deep Dive

Understanding when each lifecycle hook is called is crucial for proper SystemField implementation:

### Initialization Hooks

```python
class InitializationField(SystemField):
    def pre_init(self, record, data, model=None, **kwargs):
        """Called before record.__init__."""
        print(f"Pre-init: {data}")

    def post_init(self, record, data, model=None, field_data=None, **kwargs):
        """Called after record.__init__."""
        print(f"Post-init: record={record}, field_data={field_data}")
        # field_data contains any data passed for this specific field
        if field_data is not None:
            self.__set__(record, field_data)
```

### Serialization Hooks

```python
class SerializationField(SystemField):
    def pre_dump(self, record, data, dumper=None):
        """Called before record is serialized to JSON."""
        # Add computed fields to the output
        data['computed_title'] = record.get('title', '').upper()

    def post_dump(self, record, data, dumper=None):
        """Called after record is serialized to JSON."""
        # Clean up sensitive data from output
        data.pop('internal_notes', None)

    def pre_load(self, data, loader=None):
        """Called before data is loaded into a record."""
        # Normalize incoming data
        if 'title' in data:
            data['title'] = data['title'].strip()

    def post_load(self, record, data, loader=None):
        """Called after data is loaded into a record."""
        # Validate loaded data
        if not record.get('title'):
            raise ValueError("Title is required")
```

### Database Hooks

```python
class CustomModelField(SystemField):
    def pre_create(self, record):
        """Called before record is inserted into database."""
        # Set creation metadata
        record['created_by'] = current_user.id

    def post_create(self, record):
        """Called after record is inserted into database."""
        # Trigger external notifications
        self.notify_creation(record)

    def pre_commit(self, record):
        """Called before database transaction is committed."""
        # Final validations
        self.validate_before_save(record)
        # Clean denormalized data
        self.clean_relations(record)

    def post_commit(self, record):
        """Called after database transaction is committed."""
        # Index in search engine
        self.index_record(record)
        # Send notifications
        self.send_notifications(record)

    def pre_delete(self, record):
        """Called before record is deleted."""
        # Clean up related data
        self.cleanup_relations(record)

    def post_delete(self, record):
        """Called after record is deleted."""
        # Remove from search index
        self.remove_from_index(record)
```

## Advanced Patterns and Best Practices

### Field Composition

Combine multiple fields for complex behavior:

```python
class CompositeMetadataField(SystemField):
    """Field that manages multiple related metadata fields."""

    def __init__(self):
        super().__init__()
        self.title_field = UppercaseField('metadata.title')
        self.date_field = DateField('metadata.date')
        self.tags_field = PKListRelation('metadata.tags', record_cls=Tag)

    def __get__(self, record, owner=None):
        if record is None:
            return self

        return {
            'title': self.title_field.__get__(record, owner),
            'date': self.date_field.__get__(record, owner),
            'tags': self.tags_field.get_value(record)
        }

    def __set__(self, record, value):
        if isinstance(value, dict):
            if 'title' in value:
                self.title_field.__set__(record, value['title'])
            if 'date' in value:
                self.date_field.__set__(record, value['date'])
            # Handle tags through relations field...
```

### Validation Integration

Integrate SystemFields with record validation:

```python
class ValidatedField(SystemField):
    """Field with built-in validation."""

    def __init__(self, key, validators=None):
        super().__init__(key)
        self.validators = validators or []

    def __set__(self, record, value):
        # Run validation before setting
        for validator in self.validators:
            validator(value)

        self.set_dictkey(record, value, create_if_missing=True)

    def pre_commit(self, record):
        """Validate before database commit."""
        value = self.get_dictkey(record)
        if value is not None:
            for validator in self.validators:
                validator(value)

# Usage with custom validators
def validate_email(value):
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
        raise ValueError("Invalid email address")

class UserRecord(Record, SystemFieldsMixin):
    email = ValidatedField('metadata.email', validators=[validate_email])
```

### Error Handling

Implement robust error handling in your fields:

```python
import logging

class RobustField(SystemField):
    """Field with comprehensive error handling."""

    def __get__(self, record, owner=None):
        if record is None:
            return self
        try:
            return self.get_dictkey(record)
        except KeyError:
            # Log the error but don't crash
            logging.warning(f"Field {self.attr_name} not found in record {record.id}")
            return None
        except Exception as e:
            # Handle unexpected errors gracefully
            import logging
            logging.error(f"Error accessing field {self.attr_name}: {e}")
            return None

    def __set__(self, record, value):
        try:
            self.set_dictkey(record, value, create_if_missing=True)
        except Exception as e:
            logging.error(f"Error setting field {self.attr_name}: {e}")
            raise ValueError(f"Could not set {self.attr_name}: {e}")
```

## Conclusion

SystemFields provide a powerful abstraction for managing complex record behavior in InvenioRDM. They enable:

- Clean separation between data storage and business logic
- Automatic integration with record lifecycle events
- Performance optimization through caching and denormalization
- Type safety and validation
- Integration with external systems and services

When designing SystemFields, consider:

- The JSON serialization format
- Performance implications of your operations
- Idempotence and data consistency
- Error handling and debugging
- Testing strategies

By following these patterns and best practices, you can create robust, maintainable System fields that enhance InvenioRDM's capabilities while maintaining clean, readable code.
