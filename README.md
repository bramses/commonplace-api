## Running

1. start a poetry env with `poetry shell`
2. install dependencies with `poetry install`
3. run the app with `uvicorn main:app --reload`

commonplace api spec (commonplaceapi.dev)

- /ingest
	- /image-rm-bg
	- /image
	- /idea
	- /quote
		- question?
		- tag?
		- margin-notes?
	- /contextual location data
- /transform
	- /tldr
	- /tag
	- /quiz
	- /draw
	- /share
	- /add-margin-note
	- /to-book
	- /poem
	- /thesis
- /explore
	- /wander
	- /delve
	- /search
	- /toc


datum schema:
- text
- embedding
- metadata
	- type
	- author
	- title
	- location
		- pageNo
		- index
		- link
		- anchorTag (?)
	- marginNotes
		- note
		- date
	- transformations
		- tldrs
		- questions
		- tags
		- quizzes
			- quiz
			- date
	- **any**


Basically a BaaS app for data ingestion, and surfacing in a way that is helpful to use for writers. I could have it downstream work with apps like Obsidian or some infinite canvas API