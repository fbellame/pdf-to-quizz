import json

# Function to transform quiz data into the desired format
def transform_quiz_data(quiz_data):
    transformed_data = []

    transformed_data.append({
            "updateFormInfo": {
                "info": {
                    "description": "Please complete this quiz based on the PDF you provided."
                },
                "updateMask": "description"
            }
    })

    transformed_data.append({
           "updateSettings": {
                "settings": {
                    "quizSettings": {
                        "isQuiz": True
                    }
                },
                "updateMask": "quizSettings.isQuiz"
            } 
    })

    index = 0         
    for question_data in quiz_data:
        # Extract the question and its options
        question_text = question_data.get('question')
        reponse_text = question_data.get("reponse")
        options = [
            {"value": question_data.get('A')},
            {"value": question_data.get('B')},
            {"value": question_data.get('C')},
            {"value": question_data.get('D')}
        ]

        correct_answer = question_data.get(reponse_text)

        # only add quizz where we have the correct answer!
        if correct_answer is not None:        
            # Assemble the new format for the question
            new_question_format = {          
                "createItem": {
                    "item": {
                        "title": f"{question_text}?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": {
                                    "pointValue": 1,
                                    "correctAnswers": {
                                        "answers": [
                                            {
                                                "value": correct_answer
                                            }
                                        ]
                                    },
                                    "whenRight": {"text": "You got it!"},
                                    "whenWrong": {"text": "Sorry, that's wrong"}
                                },
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": options,
                                    "shuffle": True
                                }
                            }
                        },
                    },
                    "location": {
                        "index": index
                    }
                }
            }
            
            transformed_data.append(new_question_format)
            index += 1
    
    return transformed_data

def generate_google_form_quiz_json(quiz_data):

    # Transform the quiz data
    transformed_quiz_data = transform_quiz_data(quiz_data)

    return transformed_quiz_data