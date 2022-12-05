import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app) # Allow CORS for all domains on all routes.
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        # True means allow cookies
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        # Query the categories
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in selection}
        
        if len(categories) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(Category.query.all())
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        questions = []
        current_questions = []
        total_questions = 0
        try:
            # Query the categories
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {category.id: category.type for category in categories}
            
            # Query the questions
            questions = Question.query.order_by(Question.id).all()

            if questions is None:
                abort(404)
            elif questions == []:
                current_questions = []
                total_questions = 0
                print("get_questions -- total_questions : {}".format(total_questions))
            else:
                current_questions = paginated(request, questions)
                total_questions = len(Question.query.all())
            
            return jsonify({
                "success": True,
                "total_questions": total_questions, 
                "questions": current_questions,
                "categories": formatted_categories,
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            """ Query the categories """
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {category.id: category.type for category in categories}
            
            """ Delete the designated question """
            question = Question.query.filter(Question.id == question_id).one_or_none()
            print("delete_question -- question: {}".format(question))
            # Abort if the designated question doesn't exist
            if question is None:
                abort(422)
            # Delete the question
            question.delete()

            """ Query for the response """
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginated(request, questions)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "current_questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "categories": formatted_categories
                }
            )

        except:
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def create_search_question():
        body = request.get_json()
        searchTerm = body.get("searchTerm", None)
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        
        try:
            if searchTerm:
                searched_questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(searchTerm))).all()
                            
                if searched_questions is None:
                    abort(404)
                elif searched_questions == []:
                    current_questions = []
                    total_questions = 0
                else:
                    current_questions = paginated(request, searched_questions)
                    total_questions = len(searched_questions)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": total_questions,
                    }
                )
            else:
                new_question_obj = Question(question=new_question, 
                                    answer=new_answer, 
                                    difficulty=new_difficulty,
                                    category=new_category)
                new_question_obj.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginated(request, selection)
                
                # if the just created question is not unique
                created_id = new_question_obj.id
                
                return jsonify(
                    {
                        "success": True,
                        "created": created_id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                )

        except Exception as e:
            print(e)
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        # Query the category_id's type
        current_category = Category.query.filter(Category.id==category_id).one_or_none() #returns obj
        try:
            # Query the questions of the category_id
            questions = Question.query.filter(Question.category==category_id).all()
            if questions is None:
                abort(404)

            elif questions == []:
                current_questions = []
                total_questions = 0
                print("get_questions -- total_questions : {}".format(total_questions))
            else:
                current_questions = paginated(request, questions)
                total_questions = len(Question.query.all())
        
            return jsonify({
                "success": True,
                "total_questions": total_questions,
                "questions": current_questions,
                "categories": current_category.type
            })
        except Exception as e:
            print(e)
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quizz():
        body = request.get_json()
        cat = body.get("quiz_category", None)
        print(cat)
        prev_questions = body.get("previous_questions", None)
        try:
            print (cat)
            if cat == {'type': 'click', 'id': 0}:
                question = Question.query.filter(Question.id.notin_(prev_questions)).\
                    order_by(func.random()).first()
            else:
                question = Question.query.filter(Question.category==cat['id']).\
                    filter(Question.id.notin_(prev_questions)).\
                    order_by(func.random()).first()
            print(question)
            if question == None:
                abort(404)
            else:
                current_question = question.format()
                print(question.format())
            return jsonify(
                    {
                        "success": True,
                        "question": current_question,
                    }
                )
        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "bad request"
                }), 
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
                }),
            404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
                }), 
            405
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
                }),
            422,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "internal error"
                }), 
            500
        )

    return app
    

