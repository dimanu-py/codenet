---
created: 2026-03-06
status: Proposed
---

# Criteria Pagination Support

## Overview

Extend the Criteria pattern to support two pagination strategies: page-based (using page/page_size) and cursor-based (using start_cursor/page_size). This enables clients to paginate collection responses in a standardized way while keeping the domain decoupled from SQL concepts like LIMIT/OFFSET.

## Objectives

- Support page-based pagination with page number and page_size
- Support cursor-based pagination with opaque, secure cursors
- Integrate pagination into existing Criteria pattern
- Provide standardized paginated response structures
- Maintain backward compatibility (pagination is optional)
- Ensure one endpoint supports only one pagination type
- Keep domain concepts (page, page_size) separate from SQL concepts (LIMIT, OFFSET)

## Requirements

### Functional Requirements

#### Page-Based Pagination
- Accept `page` (required, > 0) and `page_size` (optional, default 10, max 100) query parameters
- Translate page/page_size to LIMIT/OFFSET in infrastructure layer
- Response includes `has_more: bool` indicating if more results exist
- Parameters explicit in URL for easy navigation

#### Cursor-Based Pagination
- Accept `start_cursor` (optional, omit for first page) and `page_size` (optional, default 10, max 100) query parameters
- Cursor is an opaque, cryptographically signed token encoding sort field and values
- Response includes `has_more: bool` and `next_cursor: str | null`
- Cursors cannot be manipulated by clients (signed/encrypted)

#### Response Structure
- Only endpoints returning collections (`data: list[dict]`) support pagination
- Each endpoint supports exactly one pagination type
- Paginated responses extend `SuccessResponse` with pagination metadata
- Easy-to-use response builders to avoid manual structure creation

### Non-Functional Requirements

- Reuse existing `Field` value object for sort fields in cursor
- Follow existing patterns (value objects, StrEnum)
- Extend `CriteriaToSqlalchemyConverter` without breaking existing functionality
- Cursor signing uses existing JWT secret from Settings
- Create comprehensive test coverage

## Usage Examples

### Example 1: Page-Based Pagination Request

```python
# URL: /users?filter={}&page=2&page_size=20

criteria = Criteria.from_primitives(
    expression={},
    sorts=[{"field": "created_at", "direction": "descending"}],
    pagination=PageBasedPagination(page=2, page_size=20)
)
```

### Example 2: Page-Based Pagination Response

```python
# Controller returns:
PagedOkResponse(
    data=[{"id": "1", "name": "John"}, ...],
    page=2,
    page_size=20,
    has_more=True
)

# JSON Response:
{
    "status": 200,
    "result": "success",
    "data": [{"id": "1", "name": "John"}, ...],
    "pagination": {
        "page": 2,
        "page_size": 20,
        "has_more": true
    }
}
```

### Example 3: Cursor-Based Pagination Request

```python
# First page: /users?filter={}&page_size=20
# Next page:  /users?filter={}&page_size=20&start_cursor=eyJmaWVsZCI6...

criteria = Criteria.from_primitives(
    expression={},
    sorts=[{"field": "created_at", "direction": "descending"}],
    pagination=CursorBasedPagination(start_cursor="eyJmaWVsZCI6...", page_size=20)
)
```

### Example 4: Cursor-Based Pagination Response

```python
# Controller returns:
CursorOkResponse(
    data=[{"id": "1", "name": "John"}, ...],
    page_size=20,
    has_more=True,
    next_cursor="eyJmaWVsZCI6ImNyZWF0ZWRfYXQiLCJ2YWx1ZSI6..."
)

# JSON Response:
{
    "status": 200,
    "result": "success",
    "data": [{"id": "1", "name": "John"}, ...],
    "pagination": {
        "page_size": 20,
        "has_more": true,
        "next_cursor": "eyJmaWVsZCI6ImNyZWF0ZWRfYXQiLCJ2YWx1ZSI6..."
    }
}
```

### Example 5: Generated SQLAlchemy Queries

```python
# Page-based: page=2, page_size=20
# SELECT * FROM users ORDER BY created_at DESC LIMIT 21 OFFSET 20
# (fetches 21 to determine has_more, returns 20)

# Cursor-based: start_cursor decodes to {field: "created_at", value: "2026-03-01", direction: "desc"}
# SELECT * FROM users WHERE created_at < '2026-03-01' ORDER BY created_at DESC LIMIT 21
```

## Design Analysis

### Current Architecture

**Domain Layer** (`src/shared/domain/criteria/`):
- `Criteria` - Entry point with `from_primitives(filter_expression, sorts)` method
- `Expression` - Filter expression hierarchy
- `Sorts` - Collection of sort specifications (from design doc 0003)

**Infrastructure Layer** (`src/shared/infra/criteria/`):
- `CriteriaToSqlalchemyConverter` - Converts Criteria to SQLAlchemy Select

**API Layer** (`src/shared/infra/api/`):
- `SuccessResponse` - Base response with `data: dict | list[dict]`
- `OkResponse` - 200 response extending SuccessResponse

### Design Decision: Pagination Type Strategy

**Option A - Single pagination class with type discriminator**:
```python
pagination=Pagination(type="page", page=2, page_size=20)
pagination=Pagination(type="cursor", start_cursor="...", page_size=20)
```
❌ Mixing concerns in one class
❌ Optional fields depending on type
❌ Runtime type checking needed

**Option B - Separate pagination classes** (Recommended):
```python
pagination=PageBasedPagination(page=2, page_size=20)
pagination=CursorBasedPagination(start_cursor="...", page_size=20)
```
✅ Clear type safety
✅ Each class has only relevant fields
✅ Polymorphic behavior via abstract base

**Decision**: Use Option B - separate pagination classes with shared abstract base.

### Design Decision: Domain Vocabulary

**Option A - Use SQL terms (limit/offset)**:
❌ Leaks infrastructure concepts into domain
❌ Less intuitive for API consumers

**Option B - Use page/page_size terms** (Recommended):
✅ Domain-driven vocabulary
✅ More intuitive for clients
✅ Translation to LIMIT/OFFSET happens in infrastructure

**Decision**: Domain uses page/page_size. Infrastructure translates to LIMIT/OFFSET.

### Design Decision: has_more Implementation

**Option A - Count total records**:
```sql
SELECT COUNT(*) FROM users WHERE ...
SELECT * FROM users WHERE ... LIMIT 20 OFFSET 20
```
❌ Two queries required
❌ Count can be expensive on large tables

**Option B - Fetch N+1 records** (Recommended):
```sql
SELECT * FROM users WHERE ... LIMIT 21 OFFSET 20
-- If 21 returned, has_more=True, return only 20
-- If ≤20 returned, has_more=False
```
✅ Single query
✅ Efficient for any table size
✅ Common pagination pattern

**Decision**: Fetch page_size + 1 records to determine has_more.

### Design Decision: Cursor Security

**Option A - Base64 encode only**:
❌ Easily decoded and manipulated
❌ Security risk (SQL injection potential)

**Option B - Signed JWT token** (Recommended):
```python
cursor_payload = {"field": "created_at", "value": "2026-03-01", "direction": "desc"}
cursor = jwt.encode(cursor_payload, settings.jwt_secret_key, algorithm="HS256")
```
✅ Tamper-proof (signature verification)
✅ Reuses existing JWT infrastructure
✅ Opaque to clients

**Decision**: Use JWT-signed cursors with existing secret key.

### Design Decision: Empty Pagination Classes

**Question**: Should we create `EmptyPagination` similar to `EmptyExpression`?

**Analysis**:
- `Pagination` will be an abstract base with two concrete implementations
- Unlike `Expression` tree structure, pagination is a simple value holder
- `None` naturally represents "no pagination" in Python

**Decision**: No `EmptyPagination` class. Use `Optional[Pagination]` where `None` means no pagination. This follows the same reasoning as the `EmptySorts` decision in design doc 0003.

### Design Decision: Response Structure

**Option A - Flat response with pagination fields**:
```json
{"status": 200, "data": [...], "page": 2, "has_more": true}
```
❌ Mixes data and pagination at same level
❌ Inconsistent between pagination types

**Option B - Nested pagination object** (Recommended):
```json
{"status": 200, "data": [...], "pagination": {"page": 2, "has_more": true}}
```
✅ Clear separation of concerns
✅ Extensible for future pagination metadata
✅ Consistent structure across pagination types

**Decision**: Use nested `pagination` object in response.

## Proposed Architecture

### New Domain Components

**Pagination abstract base** (`src/shared/domain/criteria/pagination.py`):
```python
from abc import ABC, abstractmethod
from typing import Self

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


class Pagination(ABC):
    _page_size: int

    def __init__(self, page_size: int | None = None) -> None:
        self._page_size = self._validate_page_size(page_size)

    @property
    def page_size(self) -> int:
        return self._page_size

    @property
    def limit(self) -> int:
        """Returns page_size + 1 to determine has_more"""
        return self._page_size + 1

    @abstractmethod
    def to_primitives(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_primitives(cls, data: dict) -> Self:
        raise NotImplementedError

    @staticmethod
    def _validate_page_size(page_size: int | None) -> int:
        size = page_size or DEFAULT_PAGE_SIZE
        if size < 1 or size > MAX_PAGE_SIZE:
            raise InvalidPageSize(size)
        return size
```

**PageBasedPagination** (`src/shared/domain/criteria/page_based_pagination.py`):
```python
class PageBasedPagination(Pagination):
    _page: int

    def __init__(self, page: int, page_size: int | None = None) -> None:
        super().__init__(page_size)
        self._page = self._validate_page(page)

    @property
    def page(self) -> int:
        return self._page

    @property
    def offset(self) -> int:
        return (self._page - 1) * self._page_size

    @classmethod
    def from_primitives(cls, data: dict) -> Self:
        return cls(page=data["page"], page_size=data.get("page_size"))

    def to_primitives(self) -> dict:
        return {"page": self._page, "page_size": self._page_size}

    @staticmethod
    def _validate_page(page: int) -> int:
        if page < 1:
            raise InvalidPageNumber(page)
        return page
```

**CursorBasedPagination** (`src/shared/domain/criteria/cursor_based_pagination.py`):
```python
class CursorBasedPagination(Pagination):
    _start_cursor: str | None
    _decoded_cursor: dict | None

    def __init__(
        self,
        page_size: int | None = None,
        start_cursor: str | None = None,
        decoded_cursor: dict | None = None
    ) -> None:
        super().__init__(page_size)
        self._start_cursor = start_cursor
        self._decoded_cursor = decoded_cursor

    @property
    def start_cursor(self) -> str | None:
        return self._start_cursor

    @property
    def decoded_cursor(self) -> dict | None:
        return self._decoded_cursor

    @property
    def is_first_page(self) -> bool:
        return self._start_cursor is None

    @classmethod
    def from_primitives(cls, data: dict) -> Self:
        return cls(
            page_size=data.get("page_size"),
            start_cursor=data.get("start_cursor"),
            decoded_cursor=data.get("decoded_cursor")
        )

    def to_primitives(self) -> dict:
        return {
            "page_size": self._page_size,
            "start_cursor": self._start_cursor
        }
```

**New exceptions** (`src/shared/domain/criteria/invalid_criteria.py`):
```python
class InvalidPageSize(InvalidCriteria):
    def __init__(self, size: int) -> None:
        super().__init__(message=f"Page size must be between 1 and 100, got {size}")

class InvalidPageNumber(InvalidCriteria):
    def __init__(self, page: int) -> None:
        super().__init__(message=f"Page number must be greater than 0, got {page}")

class InvalidCursor(InvalidCriteria):
    def __init__(self) -> None:
        super().__init__(message="Invalid or tampered cursor")
```

### New Infrastructure Components

**CursorCodec** (`src/shared/infra/criteria/cursor_codec.py`):
```python
import jwt
from src.shared.delivery.settings import Settings

class CursorCodec:
    def __init__(self, settings: Settings) -> None:
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm

    def encode(self, field: str, value: str, direction: str) -> str:
        payload = {"field": field, "value": value, "direction": direction}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode(self, cursor: str) -> dict:
        try:
            return jwt.decode(cursor, self._secret_key, algorithms=[self._algorithm])
        except jwt.InvalidTokenError:
            raise InvalidCursor()
```

### Modified Infrastructure Components

**CriteriaToSqlalchemyConverter** (extended):
```python
class CriteriaToSqlalchemyConverter:
    def convert(self, model: type[Base], criteria: Criteria) -> Select:
        query = select(model)

        if not criteria.is_empty():
            where_predicate = self._build_where_predicate(criteria, model)
            if where_predicate is not None:
                query = query.where(where_predicate)

        if criteria.has_sorts():
            query = self._apply_sorts(query, model, criteria.sorts)

        if criteria.has_pagination():
            query = self._apply_pagination(query, model, criteria.pagination)

        return query

    def _apply_pagination(
        self, query: Select, model: type[Base], pagination: Pagination
    ) -> Select:
        if isinstance(pagination, PageBasedPagination):
            return query.limit(pagination.limit).offset(pagination.offset)

        if isinstance(pagination, CursorBasedPagination):
            if not pagination.is_first_page:
                query = self._apply_cursor_filter(query, model, pagination)
            return query.limit(pagination.limit)

        return query

    def _apply_cursor_filter(
        self, query: Select, model: type[Base], pagination: CursorBasedPagination
    ) -> Select:
        cursor = pagination.decoded_cursor
        column = getattr(model, cursor["field"])
        if cursor["direction"] == "descending":
            return query.where(column < cursor["value"])
        return query.where(column > cursor["value"])
```

### New API Response Components

**Paginated responses** (`src/shared/infra/api/paginated_response.py`):
```python
from pydantic import BaseModel, Field
from src.shared.infra.api.success_response import SuccessResponse

class PagePaginationMeta(BaseModel):
    page: int
    page_size: int
    has_more: bool

class CursorPaginationMeta(BaseModel):
    page_size: int
    has_more: bool
    next_cursor: str | None

class PagedSuccessResponse(SuccessResponse):
    data: list[dict]
    pagination: PagePaginationMeta

class CursorSuccessResponse(SuccessResponse):
    data: list[dict]
    pagination: CursorPaginationMeta

class PagedOkResponse(PagedSuccessResponse):
    status: int = Field(default=200)

    @classmethod
    def build(
        cls,
        items: list[dict],
        page: int,
        page_size: int,
        has_more: bool
    ) -> "PagedOkResponse":
        return cls(
            data=items,
            pagination=PagePaginationMeta(
                page=page,
                page_size=page_size,
                has_more=has_more
            )
        )

class CursorOkResponse(CursorSuccessResponse):
    status: int = Field(default=200)

    @classmethod
    def build(
        cls,
        items: list[dict],
        page_size: int,
        has_more: bool,
        next_cursor: str | None
    ) -> "CursorOkResponse":
        return cls(
            data=items,
            pagination=CursorPaginationMeta(
                page_size=page_size,
                has_more=has_more,
                next_cursor=next_cursor
            )
        )
```

### Modified Criteria Class

**Criteria** (extended):
```python
class Criteria:
    def __init__(
        self,
        expression: Expression,
        sorts: Sorts,
        pagination: Pagination | None = None
    ) -> None:
        self._expression = expression
        self._sorts = sorts
        self._pagination = pagination

    @classmethod
    def from_primitives(
        cls,
        filter_expression: dict[str, Any],
        sorts: list[dict[str, str]] | None = None,
        pagination: Pagination | None = None
    ) -> Self:
        return cls(
            expression=ExpressionFactory.from_primitives(filter_expression)
                if filter_expression
                else ExpressionFactory.empty(),
            sorts=Sorts.from_primitives(sorts) if sorts else Sorts.empty(),
            pagination=pagination
        )

    def has_pagination(self) -> bool:
        return self._pagination is not None

    @property
    def pagination(self) -> Pagination | None:
        return self._pagination
```

## Implementation Steps

1. **Add pagination exceptions** to `src/shared/domain/criteria/invalid_criteria.py` - `InvalidPageSize`, `InvalidPageNumber`, `InvalidCursor`

2. **Create `Pagination` abstract base** in `src/shared/domain/criteria/pagination.py` with page_size validation and limit property

3. **Create `PageBasedPagination`** in `src/shared/domain/criteria/page_based_pagination.py` with page/offset logic

4. **Create `CursorBasedPagination`** in `src/shared/domain/criteria/cursor_based_pagination.py` with cursor handling

5. **Create `CursorCodec`** in `src/shared/infra/criteria/cursor_codec.py` for JWT-based cursor encoding/decoding

6. **Extend `Criteria`** class to accept optional `pagination` parameter

7. **Extend `CriteriaToSqlalchemyConverter`** to apply LIMIT/OFFSET for page-based and cursor filters for cursor-based

8. **Create paginated response classes** in `src/shared/infra/api/paginated_response.py` with builder methods

9. **Create test mothers** for `PageBasedPagination`, `CursorBasedPagination`, and paginated responses

10. **Add unit tests** for pagination classes, cursor codec, and converter pagination logic

11. **Add integration tests** for `CriteriaToSqlalchemyConverter` with pagination scenarios

## Open Questions

None.

## Notes

- Cursor-based pagination requires sorting to work correctly - the sort field becomes part of the cursor
- Page-based pagination with high page numbers can be slow on large tables (OFFSET performance)
- Cursor-based pagination is more efficient for large datasets but doesn't support jumping to arbitrary pages
- The `limit + 1` pattern is a common optimization to avoid COUNT queries
- Response builders (`PagedOkResponse.build()`, `CursorOkResponse.build()`) ensure consistent structure
- Cursors include sort direction to ensure consistent ordering across pages
- This design depends on sorting support (design doc 0003) being implemented first

