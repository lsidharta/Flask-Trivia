# Trivia App

## Introduction

Trivia App is an application to play and manage Trivia game. 

The features of this Trivia App are:
1. Display 10 questions on each page. Each question is shown with its category, difficulty level and answer. You may filter the questions by category.
2. Delete a question.
3. Add new question and its answer.
4. Search for a questions.
5. Play the Trivia game.

### Install the Trivia App

Trivia App is built on Flask, a Python's micro-framework for web app development. You can follow the following steps to install Trivia App.

1. Create a Python virtual environment.
2. Install project dependencies.

    `pip install -r requirements.txt`

3. Create the initial database from a running psql environment.

    `dropdb trivia`

    `createdb trivia`

    `psql trivia < trivia.psql`


### Start the Trivia's servers

Trivia App consists of Flask backend and React frontend.
To run the app, you need to start the backend and frontend servers separately.

1. Run the backend server

    `export FLASK_APP=flaskr`

    `export FLASK_DEBUG=true` 

    `flask run`


FLASK_DEBUG replaces the FLASK_ENV which is deprecated in Flask 2.3. 

The backend server is running in `http://localhost:5000`.

2. Run the frontend server

    `npm install` (first time only)

    `npm start`

The frontend server is running in `http://localhost:3000`.

After both servers run, you can play the Trivia game, display Trivia questions, select a category to filter the questions, create a new question, and play the game.

## APIs in Trivia App

### Base URL

`http://127.0.0.1:5000/`

### Error Handling

When the request fails, the API will return error messages as JSON objects. There are five errors types.

400: bad request
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

404: resource not found
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```

405: method not allowed
```
{
    "success": False, 
    "error": 405, 
    "message": "method not allowed"
}
```

422: unprocessable
```
{
    "success": False, 
    "error": 422, 
    "message": "unprocessable"
}
```

500: internal error
```
{
    "success": False, 
    "error": 500, 
    "message": "internal error"
}
```

### API Endpoints

#### 1. List of Questions

`curl -X GET http://127.0.0.1:5000/questions` or

`curl -X GET http://127.0.0.1:5000/questions?page=[page_number]`

Example of return values if page_number = 3:
```
{
  "page": 3,
  "questions": [
    {
      "answer": "answer1",
      "category": 1,
      "difficulty": 1,
      "id": 25,
      "question": "test1"
    }
  ],
  "success": true,
  "total_pages": 3,
  "total_questions": 21
}
```
 However, if you ask the page which exceeds the maximum available page, you will get an empty result.

 ```
 {
  "page": 4,
  "questions": [],
  "success": true,
  "total_pages": 3,
  "total_questions": 21
}
 ```

#### 2. Delete a question

`curl -X DELETE http://127.0.0.1:5000/questions/[question_id]`

If question id is 6, the success result will be as follows:
```
{
    "current_questions": [
        ...,
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 7,
            "question": "What boxer's original name is Cassius Clay?"
        },
        ...
    ]
    "deleted": 6,
    "success": true,
    "total_questions": 20
}
```
If the requested question is not available in the database, you will get a unsuccessful result that contains a 422 error message.
```
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```

#### 3. Search a question

`curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"test1"}' http://127.0.0.1:5000/questions`

Or if you use Postman, you can do a POST request to:

`http://localhost:5000/questions` 

and set the body of the request as
```
{
    "searchTerm": "world"
}
```
The success result will be as follows:
```
{
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```
On the other hand, the unsuccessful result is an empty questions array.
```
{
    "questions": [],
    "success": true,
    "total_questions": 0
}
```

#### 4. Create a New Question
`curl -X POST -H "Content-Type: application/json" -d '{"question":"test3", "answer":"answer3", "difficulty":3, "category":3}'`

Or in Postman, the body of the POST request can be setup such as:
```
{
    "question":"test3", 
    "answer":"answer3", 
    "difficulty":3, 
    "category":3
}
```

The successful result returns the id of the new created question "26".
```
{
    "created": 26,
    "questions": [
        ...
    ],
    "success": true,
    "total_questions": 21
}
```

However, if we entered the wrong URL, such as 

`curl -X POST -H "Content-Type: application/json" -d '{"question":"test1", "answer":"answer1", "difficulty":1, "category":1}' http://127.0.0.1:5000/questions/1000`,

the unsuccessfull created response is:
```
{
    "error": 405,
    "message": "method not allowed",
    "success": false
}
```

#### 5. Play the Quizz

`curl -X POST localhost:5000/quizzes -H "Content-Type:application/json" -d '{"previous_questions":[12], "quiz_category":{"type":"History", "id":"4"}}'`

Of in Postman, set the body of the POST request to the URL `http://localhost:5000/questions` as

```
{
    "previous_questions":[12], 
    "quiz_category":{
        "type":"History", 
        "id":"4"
    }
}
```
The result you will get is one question of category History that is chosen randomly.
```
{
    "question": {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    "success": true
}
```
