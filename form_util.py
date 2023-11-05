import json

# Function to transform quiz data into the desired format
def transform_quiz_data(quiz_data):
    transformed_data = []
    
    for index, question_data in enumerate(quiz_data):
        # Extract the question and its options
        question_text = question_data.get('question')
        options = [
            {"value": question_data.get('A')},
            {"value": question_data.get('B')},
            {"value": question_data.get('C')},
            {"value": question_data.get('D')}
        ]
        
        # Assemble the new format for the question
        new_question_format = {
            "createItem": {
                "item": {
                    "title": question_text,
                    "questionItem": {
                        "question": {
                            "required": True,
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
    
    return transformed_data

def generate_google_form_quiz_json(quiz_data):

    # Transform the quiz data
    transformed_quiz_data = transform_quiz_data(quiz_data)

    return transformed_quiz_data