---
created: 2026-03-05
status: Proposed
---

# Criteria Sorting Support

## Overview

Extend the Criteria pattern to support ordering results via a `sorts` query parameter containing field/direction pairs, enabling clients to specify single or multiple sort criteria.

## Objectives

- Support sorting results by one or more fields
- Allow ascending and descending sort directions
- Integrate sorting into existing Criteria pattern
- Maintain backward compatibility (sorting is optional)
- Follow established domain/infrastructure separation

## Requirements

### Functional Requirements

- Accept `sorts` query parameter as list of dictionaries
- Each sort dictionary contains:
  - `field`: name of the field to sort by
  - `direction`: either `"ascending"` or `"descending"`
- Support multiple sort fields (applied in order)
- Empty `sorts` list or omitted parameter means no ordering
- Invalid sort field names raise domain exception
- Invalid direction values raise domain exception

### Non-Functional Requirements

- Reuse existing `Field` value object
- Follow existing patterns (StrEnum for direction, value objects for Sort)
- Extend `CriteriaToSqlalchemyConverter` without breaking existing functionality
- Create comprehensive test coverage

## Usage Examples

### Example 1: Single Field Sort

```python
criteria = Criteria.from_primitives(
    expression={"field": "status", "equals": "active"},
    sorts=[{"field": "created_at", "direction": "descending"}]
)
```

### Example 2: Multiple Field Sort

```python
criteria = Criteria.from_primitives(
    expression={},
    sorts=[
        {"field": "last_name", "direction": "ascending"},
        {"field": "first_name", "direction": "ascending"}
    ]
)
```

### Example 3: No Sorting (Backward Compatible)

```python
# Both are equivalent - no sorting applied
criteria = Criteria.from_primitives(expression={"field": "name", "equals": "John"})
criteria = Criteria.from_primitives(expression={"field": "name", "equals": "John"}, sorts=[])
```

### Example 4: Generated SQLAlchemy Query

```python
# Input
criteria = Criteria.from_primitives(
    expression={"field": "status", "equals": "active"},
    sorts=[{"field": "name", "direction": "ascending"}]
)

# Generated SQL
# SELECT * FROM users WHERE status = 'active' ORDER BY name ASC
```

## Design Analysis

### Current Architecture

**Domain Layer** (`src/shared/domain/criteria/`):
- `Criteria` - Entry point with `from_primitives(filter_expression)` method
- `Expression` - Filter expression hierarchy
- `Field` - Value object wrapping field name (reusable for sorting)
- `Operator` - StrEnum for comparison operators

**Infrastructure Layer** (`src/shared/infra/criteria/`):
- `CriteriaToSqlalchemyConverter` - Converts Criteria to SQLAlchemy Select
- `ExpressionToSqlConverter` - Handles WHERE clause generation

### Design Decision: Sort Structure

**Option A - Single sort object**:

```python
sorts={"field": "name", "direction": "ascending"}
```

❌ Cannot support multiple sort fields
❌ Would require API change later

**Option B - List of sort objects** (Recommended):

```python
sorts=[{"field": "name", "direction": "ascending"}]
```

✅ Supports single and multiple sorts
✅ Order in list determines sort priority
✅ Empty list means no sorting

**Decision**: Use Option B - list of sort dictionaries.

### Design Decision: Direction Values

**Option A - Short form**: `"asc"`, `"desc"`

**Option B - Full form**: `"ascending"`, `"descending"` (Recommended)

✅ More explicit and readable
✅ Consistent with verbose style of existing operators (`"greater_than"`, not `"gt"`)
✅ Self-documenting API

**Decision**: Use full form - `"ascending"` and `"descending"`.

### Design Decision: EmptySorts Class

**Question**: Should we create an `EmptySorts` class similar to `EmptyExpression`?

**Analysis of `EmptyExpression`**:

- `Expression` is an abstract base class with polymorphic hierarchy (`ComparisonExpression`, `CompositeExpression`, `EmptyExpression`)
- `Criteria.is_empty()` uses `isinstance(self._expression, EmptyExpression)` for type checking
- Implements Null Object Pattern for a tree structure with different node types

**Option A - Create `EmptySorts` class**:

```python
class Sorts(ABC): ...
class NonEmptySorts(Sorts): ...
class EmptySorts(Sorts): ...
```

❌ Over-engineering - adds complexity without benefit
❌ `Sorts` is a simple collection, not a polymorphic hierarchy
❌ No use case requiring type-based distinction

**Option B - Simple empty list** (Recommended):

```python
class Sorts:
    def is_empty(self) -> bool:
        return len(self._sorts) == 0
    
    @classmethod
    def empty(cls) -> Self:
        return cls([])
```

✅ Simple and Pythonic
✅ Empty list naturally represents "no sorting"
✅ `Sorts.empty()` factory method provides clear intent
✅ YAGNI - no abstraction until needed

**Decision**: No `EmptySorts` class. Use `Sorts` with an empty list and `is_empty()` method. The `EmptyExpression` pattern exists because `Expression` is a polymorphic tree structure - `Sorts` is just a collection wrapper where an empty list suffices.

## Proposed Architecture

### New Domain Components

**SortDirection enum** (`src/shared/domain/criteria/sort_direction.py`):
```python
from enum import StrEnum

class SortDirection(StrEnum):
    ASCENDING = "ascending"
    DESCENDING = "descending"
```

**Sort value object** (`src/shared/domain/criteria/sort.py`):
```python
from src.shared.domain.criteria.field import Field
from src.shared.domain.criteria.sort_direction import SortDirection

class Sort:
    _field: Field
    _direction: SortDirection

    def __init__(self, field: str, direction: str) -> None:
        self._field = Field(field)
        self._direction = SortDirection(direction)

    @classmethod
    def from_primitives(cls, sort: dict[str, str]) -> Self:
        return cls(field=sort["field"], direction=sort["direction"])

    def to_primitives(self) -> dict[str, str]:
        return {"field": self._field.value, "direction": self._direction.value}

    @property
    def field(self) -> Field:
        return self._field

    @property
    def direction(self) -> SortDirection:
        return self._direction
```

**Sorts collection** (`src/shared/domain/criteria/sorts.py`):
```python
class Sorts:
    _sorts: list[Sort]

    def __init__(self, sorts: list[Sort]) -> None:
        self._sorts = sorts

    @classmethod
    def from_primitives(cls, sorts: list[dict[str, str]]) -> Self:
        return cls([Sort.from_primitives(sort) for sort in sorts])

    @classmethod
    def empty(cls) -> Self:
        return cls([])

    def to_primitives(self) -> list[dict[str, str]]:
        return [sort.to_primitives() for sort in self._sorts]

    def is_empty(self) -> bool:
        return len(self._sorts) == 0

    def __iter__(self):
        return iter(self._sorts)
```

**New exceptions** (`src/shared/domain/criteria/invalid_criteria.py`):
```python
class InvalidSortStructure(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Sort must contain 'field' and 'direction'")

class InvalidSortDirection(InvalidCriteria):
    def __init__(self, direction: str) -> None:
        super().__init__(message=f"Invalid sort direction: '{direction}'. Must be 'ascending' or 'descending'")
```

### Modified Domain Components

**Criteria** (`src/shared/domain/criteria/criteria.py`):
```python
class Criteria:
    def __init__(self, expression: Expression, sorts: Sorts) -> None:
        self._expression = expression
        self._sorts = sorts

    @classmethod
    def from_primitives(
        cls,
        filter_expression: dict[str, Any],
        sorts: list[dict[str, str]] | None = None
    ) -> Self:
        return cls(
            expression=ExpressionFactory.from_primitives(filter_expression)
                if filter_expression
                else ExpressionFactory.empty(),
            sorts=Sorts.from_primitives(sorts) if sorts else Sorts.empty()
        )

    def to_primitives(self) -> dict[str, Any]:
        return {
            "filter": self._expression.to_primitives(),
            "sorts": self._sorts.to_primitives()
        }

    def has_sorts(self) -> bool:
        return not self._sorts.is_empty()

    @property
    def sorts(self) -> Sorts:
        return self._sorts
```

### Modified Infrastructure Components

**CriteriaToSqlalchemyConverter** (`src/shared/infra/criteria/criteria_to_sqlalchemy_converter.py`):
```python
from sqlalchemy import asc, desc

class CriteriaToSqlalchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if not criteria.is_empty():
            where_predicate = self._build_where_predicate(criteria, model)
            if where_predicate is not None:
                query = query.where(where_predicate)

        if criteria.has_sorts():
            query = self._apply_sorts(query, model, criteria.sorts)

        return query

    def _apply_sorts(self, query: Select, model: type[Base], sorts: Sorts) -> Select:
        for sort in sorts:
            column = getattr(model, sort.field.value)
            if sort.direction == SortDirection.ASCENDING:
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))
        return query
```

## Implementation Steps

1. **Create `SortDirection` enum** in `src/shared/domain/criteria/sort_direction.py`
2. **Create `Sort` value object** in `src/shared/domain/criteria/sort.py` with `Field` and `SortDirection`
3. **Create `Sorts` collection** in `src/shared/domain/criteria/sorts.py` wrapping `list[Sort]`
4. **Add exceptions** `InvalidSortStructure` and `InvalidSortDirection` to `src/shared/domain/criteria/invalid_criteria.py`
5. **Extend `Criteria`** class to accept `sorts` parameter in `from_primitives()` and add `has_sorts()` method
6. **Extend `CriteriaToSqlalchemyConverter`** to apply `ORDER BY` when sorts are present
7. **Create test mothers** `SortMother` and `SortsMother` in `tests/shared/domain/criteria/mothers/`
8. **Update `CriteriaMother`** to support sorts parameter
9. **Add unit tests** for `Sort`, `Sorts`, and updated `Criteria`
10. **Add integration tests** for `CriteriaToSqlalchemyConverter` with sorting scenarios

## Open Questions

None.

## Notes

- This implementation prepares the architecture for future pagination support (limit/offset)
- The `Criteria` class is becoming an aggregator of concerns (filtering, sorting, future pagination)
- Each concern has its own converter component following Single Responsibility Principle
- Sorting is applied after filtering in the query building process

