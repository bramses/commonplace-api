'''
add idea to db
idea schema example:
{
    "idea": "string", # required
    "meta": {
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0], # required - vectorized quote  
        "transformations": {
            "tldr": [
                {
                    "text": "string",
                    "date": "Date"
                }
            ],
            "question": [
                {
                    "text": "string",
                    "date": "Date"
                }
            ],
            "quiz": [
                {
                    "question": "string",
                    "answer": "string",
                    "date": "Date"
                }
            "image": [
                {
                    "url": "string",
                    "date": "Date"
                }
            ]
        }
    }
}

add quote processing:
1. check if quote is already in db
2. if not, add quote to db
3. add vectorized quote to db
4. add specified transformations to db

options for llm:
- transform quote into a question
- transform quote into tldr
- transform quote into Q&A flashcard
- transform quote into a picture
'''