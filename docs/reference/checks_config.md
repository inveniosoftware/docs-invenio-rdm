# Metadata Checks Configuration Schema

This documentation explains the schema and configuration format for creating metadata validation rules in the checks system.

## Overview

The system provides a flexible way to define validation rules for record metadata using JSON stored in the database. Rules can check individual fields, compare values, and validate lists of items with complex conditions. This schema provides a powerful way to define complex validation logic while remaining human-readable and maintainable.

## Rule Configuration

A rule configuration is a dictionary with the following structure:

```python
{
    "id": "unique-rule-id",  # Required
    "title": "Human-readable title",
    "message": "Error message shown when rule fails",
    "description": "Detailed description of the rule",
    "level": "info|warning|failure",  # Default: "info"
    "condition": {  # Optional condition expression
        "type": "expression_type",
        # ... expression configuration
    },
    "checks": [  # List of check expressions
        {
            "type": "expression_type",
            # ... expression configuration
        }
    ]
}
```

This object is stored in the `params` section of the check_config in the database.

## Expression Types

### 1. Field Expression

Accesses a fiel, or nested field, from the metadata using dot notation, returning that value to the check.

```python
{
    "type": "field",
    "path": "metadata.title"  # Path to the field
}
```

### 2. Comparison Expression

Compares two values using one of the following operators:

- `==` - **Equal to**
- `!=` - **Not equal to**
- `in` - Value is **in** list/dict/string
- `not in` - Value is **not in** list/dict/string
- `~=` - List/dict/string **contains** value
- `!~=` - List/dict/string does **not contain** value
- `^=` - **Starts with**
- `!^=` - Does **not start with**
- `$=` - **Ends with**
- `!$=` - Does **not end with**

```python
{
    "type": "comparison",
    "left": {  # Left operand (can be another expression)
        "type": "field",
        "path": "metadata.title"
    },
    "operator": "==",  # Comparison operator
    "right": "Expected Value"  # Right operand (literal value)
}
```

### 3. Logical Expression

Combines multiple expressions with logical operators.

```python
{
    "type": "logical",
    "operator": "and",  # "and" or "or"
    "expressions": [  # List of expressions to combine
        {
            "type": "field",
            "path": "metadata.title"
        },
        {
            "type": "comparison",
            # ... comparison config
        }
    ]
}
```

### 4. List Expression

Validates lists of items using one of three operators:

- `exists` - Checks if the list exists and is not empty
- `any` - At least one item must match the predicate
- `all` - All items must match the predicate

```python
{
    "type": "list",
    "operator": "any",  # "any", "all", or "exists"
    "path": "metadata.creators",  # Path to the list field
    "predicate": {  # Condition to apply to list items (required for "any" and "all")
        "type": "expression_type",
        # ... expression configuration
    }
}
```

## Complete Example

Here's a complete example showing multiple rules with different expression types:

```python
{
    "id": "metadata-validation",
    "title": "Metadata Validation",
    "description": "Validates basic metadata requirements",
    "rules": [
        {
            "id": "license:exists",
            "level": "error",
            "title": "Record license",
            "checks": [
                {
                    "path": "metadata.rights",
                    "type": "list",
                    "operator": "exists",
                    "predicate": {}
                }
            ],
            "message": "Licenses are required.",
            "description": "All submissions must specify the licensing terms."
        },
        {
            "id": "creators:identifier",
            "level": "info",
            "title": "Creator Identifiers",
            "checks": [
                {
                    "path": "metadata.creators",
                    "type": "list",
                    "operator": "all",
                    "predicate": {
                        "type": "logical",
                        "operator": "and",
                        "expressions": [
                            {
                                "path": "person_or_org.identifiers",
                                "type": "field"
                            },
                            {
                                "path": "person_or_org.identifiers",
                                "type": "list",
                                "operator": "any",
                                "predicate": {
                                    "path": "identifier",
                                    "type": "field"
                                }
                            }
                        ]
                    }
                }
            ],
            "message": "Affiliations are recommended for all creators (e.g. an ORCID)",
            "condition": {
                "path": "metadata.creators",
                "type": "list",
                "operator": "exists",
                "predicate": {
                }
            },
            "description": "All creators should have a persistent identifier (e.g. an ORCID)"
        },
    ]
}
```
