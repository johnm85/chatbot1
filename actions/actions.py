from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker,Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
import pandas as pd
import sqlite3
from sqlite3 import Error
import csv
import os

class information_form(FormAction):
    """Example of a custom form action"""

    # def create_connection(self):

    #     conn = None
    #     try:
    #         conn = sqlite3.connect("/actions/database1.db")
    #         return conn
    #     except Error as e:
    #         pass

    #     return conn
    
    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_user(self, conn):

        sql = ''' INSERT INTO users(name,day,time,email_id)
                VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid


    def fetch_slots(self, conn):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM slots;')

        rows = cur.fetchall()

        slots = []
        for row in rows:
            slots.append(row)

        return slots

    def create_calender(self, conn, calender):
        sql = ''' INSERT INTO calender(user_id,slot_id)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, calender)
        conn.commit()
        return cur.lastrowid






    def name(self) -> Text:
        """Unique identifier of the form"""

        return "information_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["day", "time", "name", "email_id"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        #print(self)
        return {
            "day": self.from_text(intent=None),
            "time": self.from_text(intent=None),
            "name": self.from_text(intent=None),
            "email_id": self.from_text(intent=None),
        }
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        name1 = tracker.get_slot("name")
        day1 = tracker.get_slot("day")
        time1 = tracker.get_slot("time")
        email_id1 = tracker.get_slot("email_id")
        
        # print(name1)
        # print(day1)
        
        # # name of csv file 
        filename = os.getcwd() + "/filled_forms1.csv"
        fields = ["day", "time", "name", "email_id"]
        rows = [[day1, time1, name1, email_id1]]
            
        # writing to csv file 
        with open(filename, 'a', newline='') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            # csvwriter.writerow(fields) 
            csvwriter.writerows(rows)
        
        # conn = self.create_connection()
        
        # sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
        #                                 day text,
        #                                 time text,
        #                                 name text,
        #                                 email_id text
        #                             ); """

        # cur = conn.cursor()
        # cur.execute(sql_create_users_table)
        # conn.commit()
        
        # params = (day1, time1, name1, email_id1)
        # cur = conn.cursor()
        
        # cur.execute("INSERT INTO users (day, time, name, email_id) VALUES (?,?,?,?)", params)
        # conn.commit()
        
       
        dispatcher.utter_message(template="utter_submit")
        # dispatcher.utter_template('utter_submit', tracker)
        return []