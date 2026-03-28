## Task: Add Search to GET /api/items

Extend the existing `GET /api/items` endpoint to support filtering items by name via a query parameter.

### Requirements

1. Accept an optional `?q=<search_term>` query parameter on `GET /api/items`
2. If `q` is provided (non-empty), return only items whose `name` contains the search term (case-insensitive)
3. If `q` is empty or not provided, return all items (existing behavior preserved)
4. Response format is unchanged: HTTP **200** with a JSON array of item objects
5. Partial matches must be supported (e.g., `?q=api` should match "My API Item")

### Notes
- Use SQLAlchemy `.filter(Item.name.ilike(f"%{q}%"))` for case-insensitive search
- Do not break the existing behavior of `GET /api/items` with no query param
