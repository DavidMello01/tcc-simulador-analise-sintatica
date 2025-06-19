# Importacoes
import pandas as pd

from IPython.display import HTML
import pandas as pd

def color_error_suggestions(action_table):
    # Create a styled DataFrame for display
    df = pd.DataFrame(action_table).T
    styled_df = df.style
    
    # Apply color to error cells with suggestions
    def highlight_errors(val):
        if isinstance(val, str):
            if "ERRO!" in val:
                return 'background-color: #FFCDD2; color: #B71C1C'  # Light red background, dark red text
            elif "Sugestão:" in val:
                return 'background-color: #C8E6C9; color: #1B5E20'  # Light green background, dark green text
        return ''
    
    return styled_df.applymap(highlight_errors)

def enhance_action_table_with_suggestions(action_table):
    enhanced_table = {}
    for token in action_table:
        enhanced_table[token] = {}
        for state in action_table[token]:
            if action_table[token][state] == "ERRO!":
                # Add specific suggestions based on state and token
                if token == ";" and state == 0:
                    enhanced_table[token][state] = "ERRO! Sugestão: Remova ';' ou insira 'a'/'(' antes"
                elif token == "$" and state == 0:
                    enhanced_table[token][state] = "ERRO! Sugestão: Insira 'a' ou '('"
                elif token == ")" and state in [0, 1, 2, 5, 7, 8]:
                    enhanced_table[token][state] = "ERRO! Sugestão: Remova ')' ou insira '(' antes"
                elif token == "a" and state in [2, 5, 8]:
                    enhanced_table[token][state] = "ERRO! Sugestão: Insira ';' entre os 'a's"
                else:
                    expected = []
                    for t in action_table:
                        if action_table[t].get(state, "") != "ERRO!":
                            expected.append(t)
                    enhanced_table[token][state] = f"ERRO! Esperava: {', '.join(expected)}"
            else:
                enhanced_table[token][state] = action_table[token][state]
    return enhanced_table

def bottom_up_algorithm(action_table, goto_table, input):
    # Enhance the action table with suggestions
    enhanced_action_table = enhance_action_table_with_suggestions(action_table)
    
    # Display the colored table
    display(color_error_suggestions(enhanced_action_table))
    
    # Rest of your existing implementation...
    stack = ["0"]
    pointer = 0
    aux_cont = 0
    input_tape = input.split(" ")
    input_tape.append("$")

    # [Rest of your existing bottom_up_algorithm function...]
    
    # When handling errors, use the enhanced table:
    def handle_error(input_tape, pointer, stack, action_table):
        current_state = int(stack[-1])
        current_token = input_tape[pointer]
        
        # Get the enhanced error message from our table
        if current_token in enhanced_action_table and current_state in enhanced_action_table[current_token]:
            error_msg = enhanced_action_table[current_token][current_state]
            if "Sugestão:" in error_msg:
                return {
                    "Erro": error_msg.split("Sugestão:")[0].strip(),
                    "Sugestão": error_msg.split("Sugestão:")[1].strip()
                }
        
        # Fallback to original error handling
        expected_tokens = [
            token for token in action_table.keys()
            if action_table[token].get(current_state, "ERRO!") != "ERRO!"
        ]
        
        return {
            "Erro": f"Token '{current_token}' inesperado no estado {current_state}",
            "Sugestão": f"Esperava um dos: {', '.join(expected_tokens)}"
        }

    # [Continue with the rest of your function...]

# Obtem a tabela de analise do site: https://smlweb.cpsc.ucalgary.ca/
def get_parsing_table(grammar, analysis_type):
    if analysis_type == "ll1":
        aux_type = "ll1-table"
    elif analysis_type == "slr1":
        aux_type = "lr0"
    else:
        aux_type = analysis_type

    url = f"https://smlweb.cpsc.ucalgary.ca/{aux_type}.php?grammar={grammar}"
    url = url.replace(" ", "%20")

    parsing_table = pd.read_html(url)
    if analysis_type == "lr0" or analysis_type == "lr1":
        return parsing_table[2]
    elif analysis_type == "ll1":
        return parsing_table[1]
    elif analysis_type == "slr1" or analysis_type == "lalr1":
        return parsing_table[3]
    else:
        return {"Erro": "Houve um erro!"}


# Converter tabela em dicionario
def get_parsing_dict(parsing_table):
    parsing_table = parsing_table.drop([0], axis=1)
    parsing_table.columns = parsing_table.iloc[0]
    parsing_table = parsing_table[1:]
    parsing_table = parsing_table.fillna(" ")

    return parsing_table.to_dict()


# Separar terminais e nao-terminais -- AGORA FUNCIONA MESMO COM ESPAÇOS, ANTES O SPLIT
def sep_terminals_nonterminals(grammar):
    terminals = []
    nonterminals = []

    grammar_array = grammar.split(".")
    grammar_array.pop()

    for line in grammar_array:
        aux = line.split("->")
        nonterminals.append(aux[0].strip())  # Remove espaços extras
        aux1 = aux[1].split("|")
        for i in aux1:
            aux2 = i.strip().split(" ")  # Remove espaços antes do split
            for j in aux2:
                if j:  # Ignora strings vazias
                    terminals.append(j)

    for i in nonterminals:
        for j in terminals:
            if i == j:
                terminals.remove(i)

    return {"terminals": list(set(terminals)), "nonterminals": list(set(nonterminals))}


# Separar tabela de acoes e transicoes
def get_goto_action_tables(grammar, analysis_type):
    parsing_table = get_parsing_dict(get_parsing_table(grammar, analysis_type))
    term_nterm = sep_terminals_nonterminals(grammar)

    action = {
        key: parsing_table[key]
        for key in parsing_table.keys() & term_nterm["terminals"]
    }
    action["$"] = parsing_table["$"]

    action = replace_dict(action, " ", "ERRO!")
    action = replace_dict(action, "acc", "ACEITO")
    action = replace_functions(action)
    action = replace_functions(action)

    goto = {
        key: parsing_table[key]
        for key in parsing_table.keys() & term_nterm["nonterminals"]
    }
    validate_grammar_coverage(grammar, action, goto)
    goto = replace_functions(goto)

    return {
        "terminals_nonterminals": term_nterm,
        "action_table": action,
        "goto_table": goto,
    }


def replace_dict(dictionary, original, final):
    for key in dictionary.keys():
        for index, value in dictionary[key].items():
            if value == original:
                dictionary[key][index] = value.replace(original, final)

    return dictionary


def replace_functions(dictionary):
    for key in dictionary.keys():
        for index, value in dictionary[key].items():
            if value[0] == "r":
                dictionary[key][index] = value.replace(
                    value, f"REDUZIR[ {value[2:-1]} ]"
                )
            elif value[0] == "s":
                # print(value[1:])
                dictionary[key][index] = value.replace(
                    value, f"EMPILHAR[ {value[1:]} ]"
                )
    return dictionary

def validate_grammar_coverage(grammar, action_table, goto_table):
    term_nterm = sep_terminals_nonterminals(grammar)
    missing_tokens = [
        t for t in term_nterm["terminals"] 
        if t not in action_table
    ]
    if missing_tokens:
        raise ValueError(
            f"Tokens da gramática faltando na tabela de ações: {missing_tokens}"
        )


# open_site('https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/')
# print(get_parsing_table('SOMA->A|d.A->b.A->c.', 'slr1'))
# print(get_parsing_dict(get_parsing_table('SOMA->A|d.A->b.A->c.', 'slr1')))
# print(
#    get_goto_action_tables(
#        "E->E v T.E->T.T->T and F.T->F.F->parenteses_esq E parenteses_dir.F->id.",
#        "slr1",
#    )
# )
