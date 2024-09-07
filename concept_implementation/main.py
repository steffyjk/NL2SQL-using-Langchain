# main.py file
from connections import DatabaseConfigs, GroqConnetion
from constants import prompts
from sqlalchemy import text
from tabulate import tabulate
from load_env import LoadEnvData
import streamlit as st

env = LoadEnvData()


if __name__ == "__main__":

    # Create a database connection
    db_config = DatabaseConfigs(
        db_name="DB_NAME",
        db_host="DB_HOST",
        db_password="DB_PASSWORD",
        db_user="DB_USER",
        db_port="DB_PORT",
    )
    db = db_config.create_db_connection(db_uri=db_config.get_postgres_uri())
    db_engine = db_config.create_engine(db_uri=db_config.get_postgres_uri())

    # Groq connection configs
    groq_config = GroqConnetion(groq_api_key="GROQ_API_KEY")
    groq_client = groq_config.create_client()

    def get_sql(question):
        # SQL query to fetch data from the database
        # Generate the SQL query
        completion = groq_client.chat.completions.create(
            model=env.fetch_env_var("LLM_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": prompts["sql_generator_with_modification_of_greetings"],
                },
                {"role": "user", "content": question},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        sql_query = ""
        for chunk in completion:
            sql_query += (
                chunk.choices[0].delta.content
                if chunk.choices[0].delta.content is not None
                else ""
            )

        ans = get_answer(sql_query=sql_query)
        return ans, sql_query

    def get_answer(sql_query):
        # Execute the query and fetch results
        try:
            if sql_query != "":
                with db_engine.connect() as connection:
                    result = connection.execute(text(sql_query))
                    # Fetch all rows from the executed query
                    rows = result.fetchall()
                    columns = result.keys()
                    for row in rows:
                        print(row)
                    print(tabulate(rows, headers=columns, tablefmt="grid"))
                    return tabulate(rows, headers=columns, tablefmt="grid")
        except:
            return sql_query
        
    # Basic StreamLit app structure

    # st.title("NL 2 SQL Response APP")

    # # Take user input
    # user_input = st.text_input("Enter your Question:")

    # if st.button("Submit"):
    #     if user_input:
    #         # Send request to backend
    #         response = get_sql(question=user_input)
    #         # Display response
    #         st.write(f"{response}")
    #     else:
    #         st.warning("Please enter a value before submitting.")

    
    # styled streamlit app
    st.markdown(
        """
        <style>
        /* Apply background color */
        .main {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Set input field and button colors */
        input, .stButton button {
            background-color: #262730;
            color: #fafafa;
        }
        
        /* Change text input placeholder color */
        input::placeholder {
            color: #fafafa;
        }

        /* Change font and text color */
        h1, h2, h3, h4, h5, h6, p, div {
            color: #fafafa;
        }

        /* Customize warning message style */
        .stAlert {
            background-color: #262730;
            color: #fafafa;
        }

        /* Code block styling */
        pre {
            background-color: #1e1e1e;
            color: #fafafa;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title and Subtitle
    st.title("Natural Language to SQL Query to Response Generator")
    # st.subheader("Convert your questions into SQL queries effortlessly")


    # Input Field
    user_input = st.text_input("Enter your question:", placeholder="e.g., 'Give me the project which name contains Project.'")

    # Adding some space before the button
    st.markdown("<br>", unsafe_allow_html=True)

    # Button and interaction
    if st.button("Submit"):
        if user_input:
            # Placeholder for backend call (replace with actual function)
            response, sql = get_sql(question=user_input)
            
            # Display response
            st.success("Here is your SQL query:")
            st.code(f"{sql}", language='sql')  
            st.success("Here is your Response:")
            st.write(f"{response}")
        else:
            st.warning("Please enter a value before submitting.")

    # Add a footer or a message
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Need help? Reach out to our support team for any queries!")
