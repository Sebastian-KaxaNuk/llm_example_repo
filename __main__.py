#Personal Modules
from src.llms_example_repo import fmp_functions as fmp

#Libraries
from dotenv import load_dotenv
import os
import openai
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

#logging config
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')

#%%

# Ruta al archivo .env
dotenv_path = 'Config/.env'

# Cargamos las variables de entorno desde el archivo .env
load_dotenv(dotenv_path)

# Obtenemos el valor de la variable
api_key_fmp = os.getenv('KNDC_API_KEY_FMP')
api_key_openai = os.getenv('KNDC_API_KEY_OPENAI')

#Validaciones
if not api_key_fmp:
    raise ValueError("Environment variable api_key_fmp is missing or empty. Please check your .env file.")

if not api_key_openai:
    raise ValueError("Environment variable api_key_openai is missing or empty. Please check your .env file.")


#%%

stocks = ['NVDA']
earnings_calls_years = 2022

quarterly_reports = fmp.earnings_calls(api_key=api_key_fmp, 
                                       stocks=stocks, 
                                       earnings_calls_start_year=earnings_calls_years)

last_2024 = quarterly_reports['NVDA'][2024]['content'][0]

#%%

text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], 
                                               chunk_size=1200,
                                               chunk_overlap=0)

chunks = text_splitter.create_documents([last_2024])

#%%

os.environ['OPENAI_API_KEY'] = api_key_openai

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1200,
    )

response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hola"}],
        temperature=1,
        )

logger.info(response.choices[0].message.content)

#%%

tokens = llm.get_num_tokens(last_2024)
logger.info(f"number of tokens in this document {tokens}")

#%%

map_prompt = """
Write a concise summary of the following, emphasizing on financial information:
"{text}"
CONCISE SUMMARY:
"""
combine_prompt = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in the 3 most important bullet points which covers the key financial points 
of the text for investment purposes.
Why should we invest in that company? Answer me as if you were an investment advisor.
```{text}```
BULLET POINT SUMMARY:
"""

#%%

combine_prompt_template = PromptTemplate(template=combine_prompt, 
                                         input_variables=["text"])

map_prompt_template = PromptTemplate(template=map_prompt, 
                                     input_variables=["text"])

chain = load_summarize_chain(llm=llm, 
                             chain_type='map_reduce',
                             map_prompt=map_prompt_template,
                             combine_prompt=combine_prompt_template,
                             verbose=True)

summary = chain.run(chunks)
logger.info(summary)


#%%


response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hola, dame un chiste"}],
        temperature=1,
        )

print(response.choices[0].message.content)