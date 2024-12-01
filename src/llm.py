import json
import os

from openai import OpenAI

# from src.models import QuestionsType
from src.prompts import (
    TEXT2SQL_SYSTEM_MESSAGE,
    ANALYST_SYSTEM_MESSAGE,
    format_sql_prompt,
    format_analyst_prompt
)
from src.utils import create_logger, log_execution_time
from src.db import execute_sql
TEMPERATURE = 0
MAX_COMPLETION_TOKENS = 1024

logger = create_logger(logger_name="llm", log_file="api.log", log_level="info")

model = os.environ.get("CHAT_MODEL")
if not model:
    logger.error("CHAT_MODEL environment variable is not set.")
    raise ValueError("CHAT_MODEL environment variable is not set.")

client = OpenAI()

@log_execution_time(logger=logger)
def generate_sql_query(
    user_question: str, 
) -> str:
    logger.debug(f"user_question:\t{user_question}")
    user_message = format_sql_prompt(user_question=user_question)
    print(f"{user_message = }")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": TEXT2SQL_SYSTEM_MESSAGE},
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            model=model,
            temperature=TEMPERATURE,
            max_tokens=MAX_COMPLETION_TOKENS,
        )
        response = completion.choices[0].message.content
        print(response)
        return response
    except Exception as e:
        logger.error(f"Error generating questions for user_message '{user_message}': {e}")
        raise

@log_execution_time(logger=logger)
def generate_question_answer(
    user_question: str, 
    sql_query: str, 
    sql_result: str
) -> str:
    user_message = format_analyst_prompt(user_question, sql_query, sql_result)
    print(f"{user_message = }")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": ANALYST_SYSTEM_MESSAGE},
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            model=model,
            temperature=TEMPERATURE,
            max_tokens=MAX_COMPLETION_TOKENS,
        )
        response = completion.choices[0].message.content
        print(response)
        return response
    except Exception as e:
        logger.error(f"Error generating questions for user_message '{user_message}': {e}")
        raise

def handle_user_message(user_question):
    raw_sql_response = generate_sql_query(user_question=user_question)
    sql_query = raw_sql_response.replace("```sql", "").replace("```", "")
    sql_result = execute_sql(sql_query)
    final_resposne = generate_question_answer(user_question=user_question, sql_query=sql_query, sql_result=sql_result)
    print(final_resposne)   
    return final_resposne