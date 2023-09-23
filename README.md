# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

For Windows users:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad Request"
}
```

The API will return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints

#### GET /categories

- General:
  - Returns a list of all available categories.
  - The response includes a dictionary of category IDs (keys) and their corresponding names (values).
- Sample: `curl http://127.0.0.1:5000/categories`

```{
  "categories": {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
    },
  "success": true,
}
```

#### GET /questions?page=${integer}

- General:

  - Return a paginated list of questions, a total number of questions, all categories.
  - You must specify the page parameter in the query to indicate the page number.

- `curl http://127.0.0.1:5000/questions?page=1`

```
{
  "success": true,
  "questions": [
     {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    // Additional questions...
  ],
  "total_questions": 100,
  "categories": {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  }
}
```

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
- `curl -X DELETE http://127.0.0.1:5000/questions/1`

```
{
  "question_id": 1,
  "success": true,
}
```

#### POST /questions

- General:
  - Create a new question. Returns the newly created question id, success value.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "This is a question", "answer": "This is an answer", "category": 1, "difficulty": 1}'`

```
{
  "success": true,
  "created_question_id": 1
}
```

#### POST /questions

- General:
  - Search questions base on user's input. Returns list of questions that match the searchTerm value.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what is this"}'`

```
{
  "success": true,
  "total_questions": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ]
}
```

#### GET /categories/{category_id}/questions

- General:
  - Get all questions that belong to a specific category. Returns list of questions belong to the category, total question number and success value.
- `curl http://127.0.0.1:5000/categories/5/questions`

```
{
  "success": true,
  "totalQuestions": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ]
}
```

#### POST /quizzes

- General:
  - Retrieve quiz questions for playing a quiz game. Returns a random quiz question or null if no more questions are available
    `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": 1, "type": "Science"}, "previous_questions": [1, 2, 3]}'`

```
{
  "success": true,
  "question": {
    "id": 4,
    "question": "What is the chemical symbol for gold?",
    "answer": "Au",
    "difficulty": 2,
    "category": 1
  }
}
```

## Deployment N/A

## Authors

Yours truly, Truong Nguyen
