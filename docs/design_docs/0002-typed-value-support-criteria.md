---
created: 2026-03-04
status: Proposed
---

# Typed Value Support in Criteria Pattern

## Overview

Extend the Criteria pattern to support multiple value types (boolean, date, number, string, list, null) with type-specific operators and semantic null handling, while maintaining extensibility for future features like sorting and pagination.

## Objectives

- Support 6 value types: boolean, date, number, string, list, null
- Define type-specific allowed operators (e.g., no `contains` for numbers)
- Handle `IS NULL` / `IS NOT NULL` semantically in DSL
- Minimize file changes when adding new types (Open/Closed Principle)
- Avoid duplicating OperatorToSqlTranslator for each type when possible
- Keep DSL clean and intuitive
- Prepare for future extensions (sorting, pagination)

## Requirements

### Functional Requirements

- Support boolean values (true/ false)
- Support date values (ISO format datetime with or without time)
- Support numeric values (integers and floats)
- Support string values (current behavior)
- Support list values (for IN operations)
- Support null values (for IS NULL / IS NOT NULL)
- Each type restricts operators to semantically valid ones
- Type detection can be automatic or explicit
- Null checks use dedicated syntax: `{"field": "name", "is_null": true/false}`
- Existing DSL expressions continue working unchanged

### Non-Functional Requirements

- Adding new type requires minimal file modifications
- No operator duplication across types unless necessary
- Type system is extensible for future value types
- Architecture supports future sorting/pagination features
- Backward compatible with existing criteria usage

## Design Analysis

### Current Architecture

**Domain Layer** (`src/shared/domain/criteria/`):
- `Criteria` - Entry point, uses `from_primitives()` to parse filter expressions
- `Expression` - Abstract base with 3 implementations:
  - `ComparisonExpression` - Leaf expression (field + operator + value)
  - `CompositeExpression` - Contains logical operator (AND/OR) + list of expressions
  - `EmptyExpression` - Represents no filters
- `Field` - Wraps field name (string)
- `Operator` - Enum of comparison operators
- `Value` - Current string-only value wrapper (to be deleted and replaced by `StringValue`)

**Infrastructure Layer** (`src/shared/infra/criteria/`):
- `CriteriaToSqlalchemyConverter` - Main converter entry point
- `ExpressionToSqlConverter` - Converts expression types to SQLAlchemy predicates
- `OperatorToSqlTranslator` - Maps DSL operators to SQLAlchemy column operations

### Design Decision: Type Handling Strategy

**Option A - Explicit Type in DSL** (Initially considered):

```python
{"field": "comments", "number": {"greater_than": 100}}
```

✅ Clear type declaration
❌ More verbose
❌ Breaking change for existing code

**Option B - Auto-detection with Type System** (Recommended):

```python
{"field": "comments", "greater_than": 100}  # Auto-detects number
```

✅ Clean, minimal DSL
✅ Backward compatible
✅ Type validation happens at Value object level
❌ Requires runtime type inspection

**Decision**: Use Option B with typed Value objects that auto-detect and validate.

### Design Decision: Operator per Type Strategy

**Option A - Separate OperatorToSqlTranslator per type**:

- Classes: `NumberEqualsTranslator`, `StringEqualsTranslator`, etc.

❌ High duplication (most operators work identically)
❌ Many files to maintain

**Option B - Smart base translators with type adapters** (Recommended):

- Keep current translators (they work for most types)
- Create type-specific adapters only when behavior differs
- Example: `DateValueAdapter` parses ISO strings before comparison

✅ Minimal duplication
✅ Open/Closed principle
✅ Easy to extend

**Decision**: Use Option B - Extend current translators, add type adapters where needed.

### Design Decision: Domain/Infrastructure Separation

**Challenge**: How to handle type-specific conversions without coupling domain to infrastructure?

**Option A - Domain has `to_sql_value()` method**:
❌ Couples domain to SQLAlchemy
❌ Would need `to_elastic_value()`, `to_mongo_value()` for other databases
❌ Violates dependency inversion principle

**Option B - Infrastructure adapts domain values** (Recommended):
✅ Domain only validates types and operators
✅ Infrastructure handles database-specific conversions
✅ TypedValue exposes raw `.value` property
✅ Adapters in infrastructure layer transform values when needed

**Decision**: Domain layer handles type detection, validation, and operator compatibility. Infrastructure layer adapts domain values to database-specific formats.

### Design Decision: DateValue Internal Storage

**Challenge**: Dates arrive as ISO 8601 strings in filter requests (e.g., `"2025-06-12"`), but domain value objects and database columns use `datetime` type.

**Option A - Store as string in domain, parse in infrastructure**:
❌ Inconsistent with domain value objects like `AccountCreatedAt` which use `datetime`
❌ Domain cannot validate date semantics (e.g., valid date ranges)

**Option B - Parse to datetime in domain** (Recommended):
✅ Consistent with existing domain value objects (e.g., `AccountCreatedAt`)
✅ Domain can validate date format and semantics
✅ Database columns use `DateTime(timezone=True)`, so no conversion needed in infrastructure
✅ All dates stored in UTC timezone

**Decision**: `DateValue` parses ISO 8601 strings to `datetime` with UTC timezone during construction in the domain layer. Since the database stores `DateTime` columns, SQLAlchemy handles the comparison directly without needing infrastructure adapters.

## Proposed Architecture

### New Domain Components

**ValueType enum**:
```python
class ValueType(StrEnum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    LIST = "list"
    NULL = "null"
```

**TypedValue hierarchy** (replaces single `Value` class):

```python
# Abstract base
class TypedValue(ABC):
    _value: Any
    
    @property
    @abstractmethod
    def type(self) -> ValueType: ...
    
    @property
    @abstractmethod
    def allowed_operators(self) -> set[Operator]: ...
    
    @property
    def value(self) -> Any:
        return self._value
    
    def validate_operator(self, operator: Operator) -> None:
        if operator not in self.allowed_operators():
            raise InvalidOperatorForType(...)

# Concrete implementations
class StringValue(TypedValue):
    def __init__(self, value: str): ...
    
class NumberValue(TypedValue):
    def __init__(self, value: int | float): ...
    
class BooleanValue(TypedValue):
    def __init__(self, value: bool): ...
    
class DateValue(TypedValue):
    def __init__(self, value: str):  # ISO 8601 string input
        self._value = self._parse_iso_to_utc_datetime(value)  # Stored as datetime
        
    def _parse_iso_to_utc_datetime(self, value: str) -> datetime:
        # Parse ISO 8601 string and ensure UTC timezone
        ...
    
class ListValue(TypedValue):
    def __init__(self, value: list): ...
    
class NullValue(TypedValue):
    def __init__(self): ...
```

**ValueFactory**:

- Auto-detects type from raw primitive value using `isinstance()` checks
- Returns appropriate TypedValue instance
- Order: None → bool → int/float → list → str (fallback)

**NullCheckExpression** (new Expression type):

- Handles `{"field": "name", "is_null": true}`
- Separate from ComparisonExpression (semantic clarity)

### Files to Delete

- `src/shared/domain/criteria/value.py` - Replaced entirely by `StringValue` in `typed_value.py`

### Infrastructure Changes

**Update existing OperatorToSqlTranslator**:
- Change `build(column, value: str)` to `build(column, value: Any)`
- Keep existing logic - SQLAlchemy handles type conversion
- Most translators work unchanged
- No `DateValueAdapter` needed since `DateValue.value` is already `datetime` and database columns are `DateTime`

**New translators for new operators**:
- `InListOperatorToSqlTranslator` - Uses `column.in_(value)` for list matching
- `IsNullOperatorToSqlTranslator` - Uses `column.is_(None)` or `column.is_not(None)`

### Test Infrastructure Changes

**Update `DummyModel`** in `tests/shared/infra/criteria/dummy_model.py`:

Add new columns to support testing all value types:
```python
class DummyModel(Base):
    __tablename__ = "test_table"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    # New columns for typed value testing
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

**Update `CriteriaMother`** in `tests/shared/domain/criteria/mothers/criteria_mother.py`:

Change `with_one_condition` to accept `Any` value type:
```python
@staticmethod
def with_one_condition(field: str, operator: str, value: Any) -> Criteria:
    return Criteria.from_primitives({"field": field, f"{operator}": value})
```

### Operator Support Matrix

| Type    | equals | not_equals | gt/gte/lt/lte | contains | in_list | is_null |
|---------|--------|------------|---------------|----------|---------|---------|
| string  | ✓      | ✓          | ✓             | ✓        | ✓       | ✓       |
| number  | ✓      | ✓          | ✓             | ✗        | ✓       | ✓       |
| boolean | ✓      | ✓          | ✗             | ✗        | ✗       | ✓       |
| date    | ✓      | ✓          | ✓             | ✗        | ✓       | ✓       |
| list    | ✗      | ✗          | ✗             | ✗        | ✗       | ✓       |
| null    | ✗      | ✗          | ✗             | ✗        | ✗       | ✓       |

## Usage Examples

### Example 1: Auto-detection with Number

```python
# DSL remains unchanged
criteria = Criteria.from_primitives({
    "field": "comments",
    "greater_than": 100  # Auto-detects as NumberValue
})
```

### Example 2: Boolean Comparison
```python
criteria = Criteria.from_primitives({
    "field": "is_active",
    "equals": True  # Auto-detects as BooleanValue
})
```

### Example 3: Date Range
```python
criteria = Criteria.from_primitives({
    "and": [
        {"field": "created_at", "greater_than": "2026-01-01"},
        {"field": "created_at", "less_than": "2026-12-31"}
    ]
})
```

### Example 4: Null Check
```python
# New semantic syntax for null checks
criteria = Criteria.from_primitives({
    "field": "deleted_at",
    "is_null": True  # IS NULL
})
criteria = Criteria.from_primitives({
    "field": "email",
    "is_null": False  # IS NOT NULL
})
```

### Example 5: List (IN clause)
```python
criteria = Criteria.from_primitives({
    "field": "status",
    "in_list": ["active", "pending", "approved"]
})
```

### Example 6: Invalid Operator for Type
```python
# This should raise InvalidOperatorForType error
criteria = Criteria.from_primitives({
    "field": "age",
    "contains": "25"  # Numbers don't support contains
})
```

## Implementation Steps

1. Create `ValueType` enum in `src/shared/domain/criteria/value_type.py`
2. Create abstract `TypedValue` base class in `src/shared/domain/criteria/typed_value.py` with `type()`, `allowed_operators()`, and `value` property
3. Implement concrete value classes: `StringValue`, `NumberValue`, `BooleanValue`, `DateValue`, `ListValue`, `NullValue` with type validation and operator restrictions
4. Create `ValueFactory` in `src/shared/domain/criteria/value_factory.py` with auto-detection logic (None → bool → int/float → list → str)
5. Add `InvalidOperatorForType` error to `src/shared/domain/criteria/criteria_error.py`
6. Create `NullCheckExpression` class for null comparisons in `expression.py`
7. Add `IN_LIST` and `IS_NULL` operators to `Operator` enum
8. Update `ComparisonExpression` to use `TypedValue` and call `validate_operator()` during construction
9. Update `ExpressionFactory` to detect `is_null` key and create `NullCheckExpression`
10. Delete `src/shared/domain/criteria/value.py` and update imports to use `StringValue` from `typed_value.py`
11. Update `OperatorToSqlTranslator.build()` signature from `value: str` to `value: Any`
12. Create `InListOperatorToSqlTranslator` and `IsNullOperatorToSqlTranslator` in infrastructure
13. Create `NullCheckExpressionToSqlConverter` in infrastructure layer
14. Update `ComparatorExpressionToSqlConverter` to extract raw value using `typed_value.value` before passing to translator
15. Update `DummyModel` with new columns: `age` (Integer), `is_active` (Boolean), `created_at` (DateTime), `deleted_at` (DateTime nullable)
16. Update `CriteriaMother.with_one_condition` to accept `value: Any`
17. Add tests to cover all 6 types, operator validations, and invalid operator scenarios
18. Verify backward compatibility with existing string-based criteria usage

## Resolved Questions

1. ✅ **Date format validation**: Strict ISO 8601 only. **Decision: Yes, strict ISO 8601.**
2. ✅ **List value type homogeneity**: Should `in_list` enforce all elements are same type? **Decision: No, keep flexible - no type enforcement on list elements.**
3. ✅ **Number precision**: Should we distinguish int vs float? **Decision: No, single `NumberValue` accepts both int and float.**
4. ✅ **Case sensitivity**: Should string comparisons be case-insensitive by default? **Decision: Keep current behavior (case-insensitive for `contains` via `ilike`).**
5. ✅ **Type coercion**: Should `"100"` (string) be coerced to `100` (number) automatically? **Decision: No - keep the type as passed. Client error if wrong type provided.**
6. ✅ **DateValue internal storage**: Should DateValue store string or datetime? **Decision: Store as `datetime` with UTC timezone, consistent with domain value objects like `AccountCreatedAt`.**
7. ✅ **Old value.py file**: Should it be kept as alias? **Decision: Delete entirely, replace with `StringValue` from `typed_value.py`.**

## Future Extensibility

### Sorting Support (Future)

```python
criteria = Criteria.from_primitives(
    expression={...},
    sort={"field": "created_at", "direction": "desc"}
)
```

Add `Sort` class alongside `Expression`. Criteria becomes a container for both filtering and sorting.

### Pagination Support (Future)

```python
criteria = Criteria.from_primitives(
    expression={...},
    pagination={"limit": 20, "offset": 40}
)
```

Add `Pagination` class. Converter translates to `.limit()` and `.offset()` in SQLAlchemy.

### Architecture Preparation

- Keep `Expression` hierarchy focused on filtering only
- `Criteria` class becomes aggregator of concerns (filtering, sorting, pagination)
- Each concern has its own converter component
- Changes localized to single responsibility areas

## Notes

- Backward compatibility maintained: existing string-based filters work unchanged
- Type system is additive: no breaking changes to current API
- Open/Closed: new types added without modifying existing type classes
- Infrastructure changes minimal: leverage existing translator pattern
- Auto-detection reduces DSL verbosity while maintaining type safety
- Date handling: ISO 8601 strings parsed to UTC `datetime` in domain, matching database `DateTime` columns

## Related Documentation
- See `docs/architecture/criteria-pattern.md` for current implementation details
- See tests in `tests/shared/domain/criteria/` for usage examples
- See `src/auth/account/domain/account_created_at.py` for datetime value object pattern
