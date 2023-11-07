from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

class GoogleForm:
    def __init__(self):
        self.form_service = None
        self.login()

    def login(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.form_service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Function to transform quiz data into the desired format
    def _transform_quiz_data(self, quiz_data):
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

    def quiz_to_form(self, quiz_data):
        # Request body for creating a form
        new_form = {
            "info": {
                "title": "PDF-to-Quizz",
                "document_title": "PDF-to-Quizz"
            }
        }

        # Creates the initial form
        result = self.form_service.forms().create(body=new_form).execute()
        form_id = result["formId"]

        # Add questions to the form
        new_question = {
            "requests": self._transform_quiz_data(quiz_data)
        }
        question_setting = self.form_service.forms().batchUpdate(formId=form_id, body=new_question).execute()

        # Retrieves the updated form and returns it
        get_result = self.form_service.forms().get(formId=form_id).execute()
        return get_result


