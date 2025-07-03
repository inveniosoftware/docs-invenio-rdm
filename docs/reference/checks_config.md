# Metadata Checks Configuration Schema

This documentation explains the schema and configuration format for creating metadata validation rules in the checks system.

## Overview

The system provides a flexible way to define validation rules for record metadata using JSON stored in the database. Rules can check individual fields, compare values, and validate lists of items with complex conditions. This schema provides a powerful way to define complex validation logic while staying human-readable and maintainable.

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

This object is stored in the `params` section of the `CheckConfig` model in the database.

## Expression Types

In order to describe the rules which make up a check or condition, we have created a grammar of **expressions** which can be composed in JSON. An expression is a structured, logical unit which can 1. contain expressions and 2. be evaluated. It can be thought of as how you might compose an Excel cell formula, where each cell reference or function is an expression. We start from the most basic expression, the `field.`

### 1. Field Expression

Accesses a field from the metadata using dot notation, returning that value.

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
            "message": "Licenses are required.",
            "description": "All submissions must specify the licensing terms.",
            "checks": [
                {
                    "path": "metadata.rights",
                    "type": "list",
                    "operator": "exists",
                    "predicate": {}
                }
            ]
        },
        {
            "id": "creators:identifier",
            "level": "info",
            "title": "Creator Identifiers",
            "message": "Affiliations are recommended for all creators",
            "description": "All creators should have a persistent identifier (e.g. an ORCID)",
            "condition": {
                "path": "metadata.creators",
                "type": "list",
                "operator": "exists",
                "predicate": {
                }
            },
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
            ]
        },
    ]
}
```

If these checks fail for a draft or record, the following error messages will be returned in the draft

```javascript
 "errors": [
    {
        "field": "metadata.rights",
        "messages": [
            "Licenses are required."
        ],
        "description": "All submissions must specify the licensing terms.",
        "severity": "error",
        "context": {
            "community": "<community-uuid>"
        }
    },
    {
        "field": "metadata.creators",
        "messages": [
            "Affiliations are recommended for all creators"
        ],
        "description": "All creators should have a persistent identifier (e.g. an ORCID)",
        "severity": "info",
        "context": {
            "community": "<community-uuid>"
        }
    },
],
```
