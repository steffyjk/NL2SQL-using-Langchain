# main.py file
from connections import DatabaseConfigs, GroqConnetion
from constants import prompts
from sqlalchemy import text
from tabulate import tabulate
from load_env import LoadEnvData
env = LoadEnvData()



if __name__ == "__main__":

    # Create a database connection
    db_config = DatabaseConfigs(db_name='DB_NAME', db_host='DB_HOST', db_password='DB_PASSWORD', db_user='DB_USER', db_port='DB_PORT')
    db = db_config.create_db_connection(db_uri=db_config.get_postgres_uri())
    db_engine = db_config.create_engine(db_uri=db_config.get_postgres_uri())

    # Groq connection configs   
    groq_config = GroqConnetion(groq_api_key='GROQ_API_KEY')
    groq_client = groq_config.create_client()

 


    def get_sql(question):
        # SQL query to fetch data from the database
         # Generate the SQL query
        completion = groq_client.chat.completions.create(
            model= env.fetch_env_var('LLM_MODEL'),
            messages=[
                {
                    "role": "system",
                    "content":prompts['sql_generator']
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        sql_query = ""
        for chunk in completion:
            sql_query += chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""

        get_answer(sql_query=sql_query)

    def get_answer(sql_query):
          # Execute the query and fetch results
            if sql_query!= "":
                with db_engine.connect() as connection:
                    result = connection.execute(text(sql_query))
                    # Fetch all rows from the executed query
                    rows = result.fetchall()
                    columns = result.keys()

                # Print the results
                print("Query Results:")
                for row in rows:
                    print(row)
                print(tabulate(rows, headers=columns, tablefmt='grid'))

    get_sql(question="Give me the project which name contains Project")
    
