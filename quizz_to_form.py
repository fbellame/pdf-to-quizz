from __future__ import print_function
from form_util import generate_google_form_quiz_json
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

def quizz_to_form(quiz_data):


    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": "PDF-to-Quizz",
            "document_title" : "PDF-to-Quizz"
        }
    }

    NEW_QUESTION = {
        "requests": generate_google_form_quiz_json(quiz_data) 
    }

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()

    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=f'{result["formId"]}', body=NEW_QUESTION).execute()

    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()

    return get_result
