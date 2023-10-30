# To Do
- [ ] Database
    - [ ] Local Postgres
    - [ ] Supabase Postgres
- [ ] Embeddings
    - [ ] OpenAI Embeddings
    - [ ] Sentence Transformers
- [ ] Transformation
    - [ ] Mistral
    - [ ] GPT-4
    - [ ] Transform an existing quote and cache it optionally also be able to edit the text in the transformation
    - [ ] A base schema for transformations to return
        Off the top of my head I'm thinking that most transformations will return text (or a url). But tags returns an array of strings...I could always just split the string on a delimiter and return an array of strings. I think that's the way to go.
        As long as it has a text representation, it can be transformed by a LLM.
    - [ ] A error message if the transformation fails or if the source material overwhelms context window
- [ ] Explore
    - [ ] How will exploring be done outside Discord and its buttons async calls writing etc
    - [ ] Cosine Similarity
    - [ ] Random 3 question surfacer function (https://www.postgresql.org/docs/current/sql-createfunction.html) (wander)
    - [ ] Return all public highlights (highlights.published = True)
    - [ ] Form a collection from a season of highlights (highlights.created_at = 2021-01-01 - 2021-03-31) for example
    - [ ] Return all highlights from a book (highlights.book = "The Almanack of Naval Ravikant")
    - [ ] Return all highlights from an author (highlights.author = "Naval Ravikant")
    - [ ] Return all highlights from a tag (highlights.tags = "philosophy")
    - [ ] Return all highlights from a agent search (start query makes N subqueries, and returns the top N results)
    - [ ] A combination of these filters
    {
        "query": "wealth is a mindset",
        "filters": {
            "books": ["The Almanack of Naval Ravikant"],
            "authors": ["Naval Ravikant"],
            "tags": ["philosophy", "life"],
            "date_range": "2021-01-01 - 2021-03-31",
            "limit": 10,
            "from_sources": ["books"], # isnt this implied by the other filters? I guess it limits the search space
            "published": True,
        },
        "sort": "cosine_similarity",
        "return_as_transformation": "question",
    }
    {
        query: "what have i written about oranges",
        filters: {
            "from_sources": ["ideas"],
        }
    }
- [ ] Ingest
    - [ ] Add Highlight to DB
    - [ ] Is a Highlight Different than an Idea?
        An example of an idea = "I should write a book about X"
        An example of a highlight = "This is a good quote"
        Both can be vectorized, transformed, and explored. Both can be expanded upon. I can use a type field to differentiate between the two.
    - [ ] Ingesting Images
        - [ ] Cloudflare Image URL
        - [ ] rembg (https://github.com/danielgatis/rembg)
    - [ ] Add Margin Note to existing Highlight
- [ ] Error Handling
- [ ] Logging

# In Progress

# Done



B R B