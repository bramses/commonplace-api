from .dependencies import router as explore_router
from .schemas import Filter
'''
- [ ] Explore    
    - [ ] Return all public highlights (highlights.published = True)
    - [ ] Form a collection from a season of highlights (highlights.created_at = 2021-01-01 - 2021-03-31) for example
    - [ ] Return all highlights from a book (highlights.book = "The Almanack of Naval Ravikant")
    - [ ] Return all highlights from an author (highlights.author = "Naval Ravikant")
    - [ ] Return all highlights from a tag (highlights.tags = "philosophy")
    - [ ] A combination of these filters


AI workflows:
- [ ] Return all highlights from a agent search (start query makes N subqueries, and returns the top N results)
- [ ] Random 3 question surfacer function (https://www.postgresql.org/docs/current/sql-createfunction.html) (wander)
- [ ] Cosine Similarity
'''

@explore_router.post("/highlights")
async def fetch_highlights_by_filter(filter: Filter):
    where_clause, params = filter.to_sql()
    print(where_clause)
    print(params)
    highlights = []

    return highlights

