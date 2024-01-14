from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
from datetime import datetime
import prompts


class BIAssistant:
    def __init__(self, api_key, database_uri) -> None:
        # Connect to the database
        self.db = SQLDatabase.from_uri(database_uri)
        # Initialize the Language Model
        self.llm = OpenAI(api_key=api_key, temperature=0, verbose=True)
        # Create a chain with the database and language model
        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True, return_intermediate_steps=True, prompt=prompts.SQLITE_PROMPT)


    def question_answering_imdb(self, question) -> str:
        """
        Function to answer questions using the IMDB database.
        Returns the response from the database.
        """
        # Query the database
        response = self.db_chain.invoke({question})
        return response['result']