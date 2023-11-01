# To Do
- [ ] Database
    - [-] Local Postgres
    - [ ] Supabase Postgres
- [ ] Embeddings
    - [x] OpenAI Embeddings
    - [-] Sentence Transformers
- [ ] Transformation
    - [-] Mistral
    - [x] GPT-4
    - [x] Transform an existing quote and cache it optionally also be able to edit the text in the transformation
    - [x] A base schema for transformations to return
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
    - [x] Is a Highlight Different than an Idea?
        An example of an idea = "I should write a book about X"
        An example of a highlight = "This is a good quote"
        Both can be vectorized, transformed, and explored. Both can be expanded upon. I can use a type field to differentiate between the two.
    - [ ] Ingesting Images
        - [x] Cloudflare Image URL
        - [ ] rembg (https://github.com/danielgatis/rembg)
    - [ ] Add Margin Note to existing Highlight
- [ ] Error Handling
- [x] Logging
    - [ ] Add logger to the rest of the code
- [ ] Authentication
    - [ ] Social
    - [ ] Email
- [ ] Deployment
- [ ] Testing
- [ ] Margin Notes Smart UI
    - [ ] An API route that spins up an idempotent margin note UI
    - [ ] Passes in highlight context to pre fill the system commands
    - [ ] The chat asks helpful questions to guide the user through the process of expanding on their thoughts
    - [ ] two views (1) the chat and (2) the margin note
        - [ ] once margin note is submitted it is opened to a second page where user can make edits
    - [ ] should i spin up an entire frontend or just use a flask page? (https://dev.to/jethrolarson/streaming-chatgpt-api-responses-with-python-and-javascript-22d0) (https://fastapi.tiangolo.com/advanced/templates/)

    Here's a rough idea of what the chat could look like:
    ```
    {
        system_commands: ["You are a good listener that help your clients expand on a thought. You can do this by asking questions like 'What do you mean by X?' or 'Can you give me an example of X?'", "Here is the context you were given before your meeting: {json of highlight and source and other margin notes}", "Here is the margin note your client wrote wrote before your meeting: {margin_note}", "After user inputs their answer to question, you rewrite the margin note and ask them if they want to add anything else."],
        first message: Hi there! I see you're working on the margin note: {margin_note}. Can you tell me more about it?
    }
    ```

