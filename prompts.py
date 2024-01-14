from langchain.prompts import PromptTemplate
from datetime import datetime


def _get_datetime() -> str:
    """
    Retrieve the current date and time in the format "Month/Day/Year, Hour:Minute:Second".

    Returns:
    str: A string representing the formatted date and time.
    """
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


PROMPT_SUFFIX = """Only use the following tables:
CREATE TABLE akas (
	title_id VARCHAR, 
	title VARCHAR, 
	region VARCHAR, 
	language VARCHAR, 
	types VARCHAR, 
	attributes VARCHAR, 
	is_original_title INTEGER -- this column is to describe if the title is the original language title,  possible values: This column has two possible values, 0 or 1
)

/*
3 rows from akas table:
title_id	title	region	language	types	attributes	is_original_title
tt0000001	Карменсіта	UA	None	imdbDisplay	None	0
tt0000001	Carmencita	DE	None	None	literal title	0
tt0000001	Carmencita - spanyol tánc	HU	None	imdbDisplay	None	0
*/


CREATE TABLE crew (
	title_id VARCHAR, 
	person_id VARCHAR, 
	category VARCHAR CHECK (category IN ('actor', 'actress', 'archive_footage', 'archive_sound', 'cinematographer', 'composer', 'director', 'editor', 'producer', 'production_designer', 'self', 'writer')), 
	job VARCHAR, 
	characters VARCHAR
)

/*
3 rows from crew table:
title_id	person_id	category	job	characters
tt0000001	nm1588970	self	None	["Self"]
tt0000001	nm0005690	director	None	None
tt0000001	nm0374658	cinematographer	director of photography	None
*/


CREATE TABLE episodes (
	episode_title_id VARCHAR, 
	show_title_id VARCHAR, 
	season_number INTEGER, 
	episode_number INTEGER
)

/*
3 rows from episodes table:
episode_title_id	show_title_id	season_number	episode_number
tt0041951	tt0041038	1	9
tt0042816	tt0989125	1	17
tt0042889	tt0989125	None	None
*/


CREATE TABLE people (
	person_id VARCHAR, 
	name VARCHAR, 
	born INTEGER, 
	died INTEGER, 
	PRIMARY KEY (person_id)
)

/*
3 rows from people table:
person_id	name	born	died
nm0000001	Fred Astaire	1899	1987
nm0000002	Lauren Bacall	1924	2014
nm0000003	Brigitte Bardot	1934	None
*/


CREATE TABLE ratings (
	title_id VARCHAR, 
	rating INTEGER, 
	votes INTEGER, 
	PRIMARY KEY (title_id)
)

/*
3 rows from ratings table:
title_id	rating	votes
tt0000001	5.7	2014
tt0000002	5.7	270
tt0000003	6.5	1937
*/


CREATE TABLE titles (
	title_id VARCHAR, 
	type VARCHAR CHECK (type IN ('movie', 'short', 'tvEpisode', 'tvMiniSeries', 'tvMovie', 'tvPilot', 'tvSeries', 'tvShort', 'tvSpecial', 'video', 'videoGame')), 
	primary_title VARCHAR, 
	original_title VARCHAR, 
	is_adult INTEGER, 
	premiered INTEGER, 
	ended INTEGER, 
	runtime_minutes INTEGER, 
	genres VARCHAR, 
	PRIMARY KEY (title_id)
)

/*
3 rows from titles table:
title_id	type	primary_title	original_title	is_adult	premiered	ended	runtime_minutes	genres
tt0000001	short	Carmencita	Carmencita	0	1894	None	1	Documentary,Short
tt0000002	short	Le clown et ses chiens	Le clown et ses chiens	0	1892	None	5	Animation,Short
tt0000003	short	Pauvre Pierrot	Pauvre Pierrot	0	1892	None	4	Animation,Comedy,Romance
*/

Question: {input}"""

_sqlite_prompt = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
The current date is {date}.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""

SQLITE_PROMPT = PromptTemplate(
    input_variables=["input", "top_k"],
    template=_sqlite_prompt + PROMPT_SUFFIX, partial_variables={"date": _get_datetime}
)