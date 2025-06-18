def bottom_up_algorithm(action_table, goto_table, input):
    stack = ["0"]
    pointer = 0

    aux_cont = 0

    input_tape = input.split(" ")
    input_tape.append("$")

    
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
            print("parse alg 7")
           elif action_movement[0] == "ERRO!":
            # Erro detahado
            expected_tokens = [
                token for token in action_table.keys() 
                if action_table[token][action[0]] != "ERRO!"
            ]
            expected_str = ", ".join(f"'{t}'" for t in expected_tokens)
            
            step_by_step.append(f"ERRO SINTÁTICO: Token inesperado '{input_tape[pointer]}'")
            step_by_step_detailed.append([
                f"ERRO na posição {pointer}:",
                f"Encontrado: '{input_tape[pointer]}'",
                f"Esperava um dos: {expected_str}",
                f"Contexto: Pilha: {stack}, Fita: {input_tape[pointer:]}"  # Adiciona contexto
            ])
            break
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
        else:
            print("parse alg 7")
            return {"Erro": "Houve um erro!"}
    return detailed_steps
