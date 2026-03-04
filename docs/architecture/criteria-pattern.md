# Criteria Pattern Architecture
## Overview
The Criteria pattern provides a Domain-Specific Language (DSL) for building flexible, type-safe queries without coupling domain logic to infrastructure concerns. It separates query specification (domain) from query execution (infrastructure).
## Architecture Layers
### Domain Layer (`src/shared/domain/criteria/`)
Defines the DSL and business rules for query construction.
#### Core Components
**Criteria** - Entry point for query specification
- Main method: `from_primitives(filter_expression: dict) -> Criteria`
- Delegates expression parsing to `ExpressionFactory`
- Validates and encapsulates the query specification
**Expression** - Abstract base for filter expressions
- `ComparisonExpression` - Atomic filter (field + operator + value)
- `CompositeExpression` - Logical grouping (AND/OR + list of expressions)
- `EmptyExpression` - Represents no filtering
**Field** - Value object wrapping field name
**Operator** - Enum of comparison operators:
- `equals`, `does_not_equal`
- `greater_than`, `greater_or_equal_to`
- `less_than`, `less_or_equal_to`
- `contains`, `not_contains`
**Value** - Value object wrapping comparison value (currently string-only)
**LogicalOperator** - Enum: `AND`, `OR`
#### Expression Structure
**ComparisonExpression**:
```
field: Field
operator: Operator
value: Value
```
**CompositeExpression**:
```
logical_operator: LogicalOperator (AND/OR)
conditions: list[Expression]
```
### Infrastructure Layer (`src/shared/infra/criteria/`)
Translates domain DSL to SQLAlchemy queries.
#### Core Components
**CriteriaToSqlalchemyConverter**
- Entry point for translation
- Converts `Criteria` to SQLAlchemy `Select` statement
- Handles empty criteria (SELECT * from table)
- Delegates expression conversion
**ExpressionToSqlConverter** - Converts expressions to SQLAlchemy predicates
- `ComparatorExpressionToSqlConverter` - Handles ComparisonExpression
- `AndCompositeExpressionToSqlConverter` - Aggregates with AND
- `OrCompositeExpressionToSqlConverter` - Aggregates with OR
- `ExpressionToSqlConverterFactory` - Selects appropriate converter
**OperatorToSqlTranslator** - Maps DSL operators to SQLAlchemy operations
- `EqualOperatorToSqlTranslator` - `column == value`
- `NotEqualOperatorToSqlTranslator` - `column != value`
- `ContainsOperatorToSqlTranslator` - `column.ilike(f"%{value}%")`
- `GreaterThanOperatorToSqlTranslator` - `column > value`
- `LessThanOperatorToSqlTranslator` - `column < value`
- Plus corresponding `>=`, `<=`, `NOT LIKE` variants
## DSL Syntax
### Simple Expression
Atomic comparison on single field:
```python
{
    "field": "username",
    "equals": "dimanu"
}
```
### Composite Expression (AND)
Multiple conditions that must all be true:
```python
{
    "and": [
        {"field": "username", "contains": "dimanu"},
        {"field": "bio", "contains": "TDD Developer"}
    ]
}
```
### Composite Expression (OR)
Multiple conditions where at least one must be true:
```python
{
    "or": [
        {"field": "likes", "greater_than": 10000},
        {"field": "followers", "greater_than": 1000000}
    ]
}
```
### Nested Composite Expression
Complex logical groupings:
```python
{
    "or": [
        {"field": "likes", "greater_than": 10000},
        {
            "and": [
                {"field": "followers", "greater_than": 10000000},
                {"field": "country", "equals": "Spain"}
            ]
        }
    ]
}
```
### Empty Expression
No filtering applied (equivalent to SELECT * FROM table):
```python
{}  # Empty dictionary
```
## Usage Patterns
### Application Layer
```python
class UserSearcher:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    async def execute(self, filters: dict) -> list[User]:
        criteria = Criteria.from_primitives(filters)
        return await self._repository.matching(criteria)
```
### Repository Layer
```python
class PostgresUserRepository(UserRepository):
    async def matching(self, criteria: Criteria) -> list[User]:
        converter = CriteriaToSqlalchemyConverter()
        query = converter.convert(UserModel, criteria)
        results = await self._session.scalars(query)
        return [user.to_domain() for user in results]
```
## Current Limitations
- **Value types**: Only string values supported
- **Operators**: Limited to comparison and text search
- **Null handling**: No semantic support for IS NULL/IS NOT NULL
- **IN clause**: No support for list-based filtering
- **Sorting**: Not supported
- **Pagination**: Not supported
## Design Principles
**Separation of Concerns**: Domain DSL independent of database technology
**Open/Closed**: New operators added without modifying existing code
**Single Responsibility**: Each converter handles one expression type
**Dependency Inversion**: Domain doesn't depend on infrastructure
## Extension Points
### Adding New Operator
1. Add to `Operator` enum
2. Create `OperatorToSqlTranslator` implementation
3. Register in `OperatorToSqlTranslatorFactory`
### Supporting New Database
1. Create new converter (e.g., `CriteriaToMongoConverter`)
2. Implement database-specific operator translators
3. No changes to domain layer needed
## Related Files
- Domain: `src/shared/domain/criteria/`
- Infrastructure: `src/shared/infra/criteria/`
- Tests: `tests/shared/domain/criteria/`, `tests/shared/infra/criteria/`
