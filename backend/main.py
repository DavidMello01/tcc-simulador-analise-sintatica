# Importacoes
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importar funcoes
from app import parsing_table
from app import parsing_algorithm
from app import utils

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5173",
    "localhost:5173",
    "https://sasc.netlify.app",
    "https://sascfront.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Testar API
@app.get("/")
async def home() -> dict:
    return {"boas-vindas": "Bem-vindo a API do SASC."}


# Testar API
@app.get("/test/")
async def read_root() -> dict:
    return {"message": "Testando api"}


"""
@app.get("/analyze/{grammar}/{input}/{analysis_type}")
async def get_table(input: str, grammar: str, analysis_type: str):
    new_grammar = utils.grammar_formatter(grammar)
    treated_grammar = utils.symbol_treat(grammar)

    goto_action_tables = parsing_table.get_goto_action_tables(
        treated_grammar, analysis_type
    )

    steps_parsing = parsing_algorithm.bottom_up_algorithm(
        utils.dict_treat(goto_action_tables["action_table"]),
        utils.dict_treat(goto_action_tables["goto_table"]),
        input,
    )

    return {
        "ERROR_CODE": 0,
        "parsingTable": goto_action_tables,
        "stepsParsing": steps_parsing,
        "grammar": new_grammar,
    }
"""


@app.get("/analyze/{analysis_type}/{grammar}/{input}")
async def get_table(input: str, grammar: str, analysis_type: str):
    try:
        new_grammar = utils.grammar_formatter(grammar)
        goto_action_tables = parsing_table.get_goto_action_tables(
            grammar, analysis_type
        )
        steps_parsing = parsing_algorithm.bottom_up_algorithm(
            goto_action_tables["action_table"],
            goto_action_tables["goto_table"],
            input,
        )
        return {
            "ERROR_CODE": 0,
            "parsingTable": goto_action_tables,
            "stepsParsing": steps_parsing,
            "grammar": new_grammar,
        }

    except Exception as e:
        return {"ERROR_CODE": 1, "errorMessage": f"Houve um erro! {e}"}
