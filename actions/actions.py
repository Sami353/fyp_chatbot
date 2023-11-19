# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

    
from typing import Any, Dict, Text, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2

# Ensure you have installed psycopg2-binary with pip
# pip install psycopg2-binary

# Define the action class to fetch course details
class ActionFetchCourseDetails(Action):
    def name(self) -> Text:
        return "action_provide_course_info"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the course name from the slot set by user input
        course_name = tracker.get_slot('course')

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            port="5432",
            user="postgres",
            password="vVcikBtONZer9zFw",
            host="db.atbayqaypnhvvabtjyxo.supabase.co"
        )
        
        # Create a cursor object
        cursor = conn.cursor()

        # Query the database for course information
        cursor.execute("SELECT * FROM courses WHERE courses = %s", (course_name,))
        course_details = cursor.fetchone()
        
        # Close the database connection
        cursor.close()
        conn.close()

        # Check if the course was found and create a response
        if course_details:
            # Assuming the order of course_details follows the schema of your table
            response = (f"Course ID: {course_details[0]}, "
                        f"Name: {course_details[1]}, "
                        f"Classification: {course_details[2]}, "
                        f"Duration: {course_details[3]} years, "
                        f"Semesters: {course_details[4]}, "
                        f"Accreditation: {course_details[5]}, "
                        f"Fee Structure: {course_details[6]}, "
                        f"Scholarship: {course_details[7]}")
        else:
            response = "I'm sorry, I couldn't find details for that course."

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []
