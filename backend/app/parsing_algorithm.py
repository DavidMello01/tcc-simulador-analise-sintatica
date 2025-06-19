def bottom_up_algorithm(action_table, goto_table, input):
    stack = ["0"]
    pointer = 0

    aux_cont = 0


    unclosed_parens = 0  # Contador de parênteses abertos
    input_tape = input.split(" ")
    input_tape.append("$")

    def handle_error(input_tape, pointer, stack, action_table):
        nonlocal unclosed_parens
        current_token = input_tape[pointer]
        current_state = int(stack[-1])
        expected_tokens = [
            token for token in action_table.keys()
            if action_table[token].get(current_state, "ERRO!") != "ERRO!"
        ]

        # Verifica parênteses não fechados quando chega no final
        if unclosed_parens > 0 and current_token == "$":
            return {
                "Erro": "ERRO SINTÁTICO: Parêntese não fechado",
                "Sugestão": f"Faltam {unclosed_parens} ')' para fechar os parênteses",
                "Contexto": f"Encontrado: {input_tape[:pointer]}"
            }
        
        # Caso específico para "a(" sem fechamento
        if current_token == "$" and "(" in input_tape and ")" not in input_tape:
            return {
                "Erro": "ERRO SINTÁTICO: Parêntese não fechado após 'a'",
                "Sugestão": "Adicione ')' após o conteúdo dentro dos parênteses",
                "Contexto": f"Encontrado: {input_tape[:pointer]}"
            }
        
        # Restante dos casos específicos originais
        if current_token == ";" and len(stack) == 1:
            return {
                "Erro": "Token ';' inesperado no início. Esperava 'a' ou '('",
                "Sugestão": "Remova ';' ou insira 'a'/'(' antes"
            }
        elif current_token == "$" and pointer == 0:
            return {
                "Erro": "Entrada vazia. A gramática exige pelo menos 'a' ou '('",
                "Sugestão": "Insira 'a' ou '('"
            }
        elif current_token == ")" and unclosed_parens <= 0:
            return {
                "Erro": "Token ')' inesperado. Não há '(' aberto",
                "Sugestão": "Remova ')' ou insira '(' antes"
            }
        elif current_token == ")" and input_tape[pointer-1] == "(":
            return {
                "Erro": "Parênteses vazios. Esperava 'a' ou '(' dentro",
                "Sugestão": "Insira 'a' ou '(' entre os parênteses"
            }
        elif current_token == "a" and pointer > 0 and input_tape[pointer-1] == "a":
            return {
                "Erro": "Dois termos 'a' consecutivos. Esperava ';' entre eles",
                "Sugestão": "Insira ';' entre os 'a's: '(a;a)'"
            }
        else:
            return {
                "Erro": f"Token '{current_token}' inesperado no estado {current_state}",
                "Sugestão": f"Esperava um dos: {', '.join(expected_tokens)}",
                "Contexto": f"Pilha: {stack}, Fita restante: {input_tape[pointer:]}"
            }
            
            if "(" in input_tape and ")" not in input_tape:
                return {
                    "Erro": "ERRO SINTÁTICO: Parêntese não fechado. Esperava ')'",
                    "Contexto": f"Encontrado: {input_tape}"
                }

    # Detalhamento do passo a passo
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
    while run == True:
        aux_cont += 1

        # Dentro do loop while, antes de verificar o token
        if input_tape[pointer] == "(":
            unclosed_parens += 1
        elif input_tape[pointer] == ")":
            unclosed_parens -= 1

        if aux_cont > 1000:
            break
        # Label do passo a passo
        step_by_step = []
        step_by_step_detailed = []

        action = ["", ""]
        transition = ["", ""]

        action[0] = int(stack[len(stack) - 1]) + 1
        action[1] = input_tape[pointer]
        if not action[1] in action_table:
            step_by_step.append(f"A entrada foi rejeitada devido a um erro léxico!")
            step_by_step_detailed.append(
                [
                    f"A entrada tem um erro lexico em: {action[1]}.",
                    "Um erro léxico ocorre quando um token identificado não pertence a gramática da linguagem fonte.",
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
        if action_movement[0] != "ACEITO" and action_movement[0] != "ERRO!":
            action_movement[1] = action_movement[1].strip("]")
            action_movement[1] = action_movement[1].strip()

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

            # Movimento de desempilhar
            # Elementos ao lado esquerdo da producao
            reduce_elements = array_action_movement[2:]
            qt_unstack = 2 * len(reduce_elements)

            for i in range(qt_unstack):
                stack.pop()

            step_by_step.append(f"Desempilhar {qt_unstack} elementos")
            step_by_step_detailed.append(
                [
                    "O primeiro passo do movimento de reduzir é desempilhar.",
                    "Nesse passo são desempilhados elementos igual à quantidade de símbolos à direita da produção apontada multiplicada por dois.",
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

            transition[0] = int(stack[len(stack) - 1]) + 1
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
            if goto_movement[0] == "E":
                stack.append(array_action_movement[0])
                stack.append(stackUp)
            else:
                break

            step_by_step.append(f"Empilhar {array_action_movement[0]}, {stackUp}")
            step_by_step_detailed.append(
                [
                    "O terceiro passo do movimento de reduzir é empilhar.",
                    "São colocados na pilha o símbolo do lado esquerdo da produção e o estado encontrado na tabela de transições.",
                    f"No caso é empilhado o simbolo ➜{array_action_movement[0]} e o estado ➜{str(int(goto_movement[10]))}.",
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
                    "São colocados na pilha o símbolo apontado na fita de entrada e o estado encontrado na tabela de ações.",
                    f"No caso é empilhado o simbolo >>{action[1]}<< e o estado >>{action_movement[1]}<<.",
                    "Nesse movimento o ponteiro é deslocado uma posição na fita de entrada.",
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
            print("parse alg 6")
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
            error_info = handle_error(input_tape, pointer, stack, action_table)
            detailed_steps.append({
                "stepByStep": [f"ERRO: {error_info['Erro']}"],
                "stepByStepDetailed": [[error_info["Sugestão"]]],
                "stack": stack[::-1].copy(),
                "input": input_tape.copy(),
                "pointer": pointer,
                "stepMarker": ["", ""]
            })
            print(detailed_steps)
            break
        else:
            print("parse alg 7")
            return {"Erro": "Houve um erro!"}
    return detailed_steps
