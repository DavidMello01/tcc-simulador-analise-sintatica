def bottom_up_algorithm(action_table, goto_table, input):
    stack = ["0"]
    pointer = 0
    aux_cont = 0
    unclosed_parens = 0
    input_tape = input.split(" ")
    input_tape.append("$")
    error_list = []

    def handle_error(input_tape, pointer, stack, action_table):
        nonlocal unclosed_parens
        current_token = input_tape[pointer]
        current_state = int(stack[-1])
        expected_tokens = [
            token for token in action_table.keys()
            if action_table[token].get(current_state, "ERRO!") != "ERRO!"
        ]

        error_entry = {
            "erro": "",
            "sugestao": "",
            "contexto": input_tape[:pointer],
            "estado": current_state,
            "token": current_token,
            "producao": None,
            "index": pointer
        }

        if unclosed_parens > 0 and current_token == "$":
            error_entry["erro"] = "ERRO SINTÁTICO: Parêntese não fechado"
            error_entry["sugestao"] = f"Feche {unclosed_parens} parêntese"
        elif current_token == "$" and "(" in input_tape and ")" not in input_tape:
            error_entry["erro"] = "ERRO SINTÁTICO: Parêntese não fechado após 'a'"
            error_entry["sugestao"] = "Adicione ')' após o conteúdo dentro dos parênteses"
        elif current_token == ";" and len(stack) == 1:
            error_entry["erro"] = "Token ';' inesperado no início. Esperava 'a' ou '('"
            error_entry["sugestao"] = "Remova ';' ou insira 'a'/'(' antes"
        elif current_token == "$" and pointer == 0:
            error_entry["erro"] = "Entrada vazia. A gramática exige pelo menos 'a' ou '('"
            error_entry["sugestao"] = "Insira 'a' ou '('"
        elif current_token == ")" and unclosed_parens < 0:
            error_entry["erro"] = "Token ')' inesperado. Não há '(' aberto"
            error_entry["sugestao"] = "Remova ')' ou insira '(' antes"
        elif current_token == ")" and input_tape[pointer-1] == "(":
            error_entry["erro"] = "Parênteses vazios. Esperava 'a' ou '(' dentro"
            error_entry["sugestao"] = "Insira 'a' ou '(' entre os parênteses"
        elif current_token == "a" and pointer > 0 and input_tape[pointer-1] == "a":
            error_entry["erro"] = "Dois termos 'a' consecutivos. Esperava ';' entre eles"
            error_entry["sugestao"] = "Insira ';' entre os 'a's: '(a;a)'"
        else:
            error_entry["erro"] = f"Token '{current_token}' inesperado no estado {current_state}"
            error_entry["sugestao"] = (
                f"Remova o token e adicione um dos: "
                f"[{' '.join(token for token in expected_tokens if (token != current_token and token != "$"))}]"
            )

        return error_entry

    detailed_steps = [
        {
            "stepByStep": ["Inicio da análise"],
            "stepByStepDetailed": [["A análise sintática será iniciada!"]],
            "stack": stack[::-1].copy(),
            "input": input_tape.copy(),
            "pointer": pointer,
            "stepMarker": ["", ""],
        }
    ]

    run = True
    while run:
        aux_cont += 1

        if input_tape[pointer] == "(":
            unclosed_parens += 1
        elif input_tape[pointer] == ")":
            unclosed_parens -= 1

        if aux_cont > 1000:
            break

        step_by_step = []
        step_by_step_detailed = []

        action = ["", ""]
        transition = ["", ""]

        action[0] = int(stack[-1]) + 1
        action[1] = input_tape[pointer]
        if action[1] not in action_table:
            error_entry = {
                "erro": f"Token '{action[1]}' não reconhecido na linguagem (erro léxico)",
                "sugestao": f"Corrija ou remova o token '{action[1]}'",
                "contexto": input_tape[:pointer],
                "estado": int(stack[-1]),
                "token": action[1],
                "producao": None
            }
            error_list.append(error_entry)
            step_by_step.append(f"Erro léxico em: {action[1]}")
            step_by_step_detailed.append(
                [
                    f"A entrada tem um erro léxico em: {action[1]}.",
                    "Um erro léxico ocorre quando um token identificado não pertence à gramática da linguagem fonte.",
                ]
            )
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": ["", ""],
                }
            )
            break

        action_movement = action_table[action[1]][action[0]].split("[")
        action_movement[0] = action_movement[0].strip()
        if action_movement[0] not in ["ACEITO", "ERRO!"]:
            action_movement[1] = action_movement[1].strip("] ").strip()

        step_by_step.append(f"AÇÃO[{action[1]}, {action[0] - 1}] => {action_movement}")
        step_by_step_detailed.append(
            [
                "Realizada uma busca na tabela de ações.",
                f"Na coluna >>{action[1]}<< e linha >>{action[0] - 1}<< encontrado movimento: {action_movement}",
            ]
        )
        detailed_steps.append(
            {
                "stepByStep": step_by_step.copy(),
                "stepByStepDetailed": step_by_step_detailed.copy(),
                "stack": stack[::-1].copy(),
                "input": input_tape.copy(),
                "pointer": pointer,
                "stepMarker": [f"{action[1]}", action[0] - 1],
            }
        )

        if action_movement[0][:8] == "REDUZIR":
            array_action_movement = action_movement[1].split(" ")
            reduce_elements = array_action_movement[2:]
            qt_unstack = 2 * len(reduce_elements)

            for _ in range(qt_unstack):
                stack.pop()

            step_by_step.append(f"Desempilhar {qt_unstack} elementos")
            step_by_step_detailed.append(
                [
                    "O primeiro passo do movimento de reduzir é desempilhar.",
                    f"Nesse caso 2 * {len(reduce_elements)} = {qt_unstack}",
                ]
            )
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": ["", ""],
                }
            )

            transition[0] = int(stack[-1]) + 1
            transition[1] = array_action_movement[0]
            goto_movement = goto_table[transition[1]][transition[0]]

            step_by_step.append(
                f"TRANSIÇÃO[{transition[1]}, {transition[0] - 1}] => {goto_movement}"
            )
            step_by_step_detailed.append(
                [
                    "O segundo passo do movimento de reduzir é consultar a tabela de transições.",
                    f"Na coluna >>{transition[1]}<< e linha >>{transition[0] - 1}<< encontrado movimento: {goto_movement}",
                ]
            )
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": [f"{transition[1]}", transition[0] - 1],
                }
            )

            stackUp = str(int(goto_movement[10:].split(" ")[0]))
            if goto_movement.startswith("EMPILHAR"):
                stack.append(array_action_movement[0])
                stack.append(stackUp)
            else:
                break

            step_by_step.append(f"Empilhar {array_action_movement[0]}, {stackUp}")
            step_by_step_detailed.append(
                [
                    "O terceiro passo do movimento de reduzir é empilhar.",
                    f"Empilhado o símbolo ➜{array_action_movement[0]} e o estado ➜{stackUp}.",
                ]
            )
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": ["", ""],
                }
            )

        elif action_movement[0][:8] == "EMPILHAR":
            stack.append(action[1])
            stack.append(action_movement[1])

            step_by_step.append(f"Empilhar: {action[1]} e {action_movement[1]}")
            step_by_step_detailed.append(
                [
                    "Movimento de EMPILHAR ou SHIFT.",
                    f"No caso é empilhado o simbolo >>{action[1]}<< e o estado >>{action_movement[1]}<<.",
                ]
            )
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": ["", ""],
                }
            )
            pointer += 1

        elif action_movement[0] == "ACEITO":
            step_by_step.append(f"A entrada foi aceita!")
            step_by_step_detailed.append([f"Aceito"])
            detailed_steps.append(
                {
                    "stepByStep": step_by_step.copy(),
                    "stepByStepDetailed": step_by_step_detailed.copy(),
                    "stack": stack[::-1].copy(),
                    "input": input_tape.copy(),
                    "pointer": pointer,
                    "stepMarker": ["", ""],
                }
            )
            break

        elif action_movement[0] == "ERRO!":
            error_entry = handle_error(input_tape, pointer, stack, action_table)
            error_list.append(error_entry)
            detailed_steps.append({
                "stepByStep": [f"ERRO: {error_entry['erro']}"],
                "stepByStepDetailed": [[error_entry["sugestao"]]],
                "stack": stack[::-1].copy(),
                "input": input_tape.copy(),
                "pointer": pointer,
                "stepMarker": ["", ""]
            })
            break

        else:
            return {"Erro": "Houve um erro!"}

    return {
        "steps": detailed_steps,
        "errors": error_list
    }