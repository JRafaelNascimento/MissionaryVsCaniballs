import numpy as np

def quantity_caniball():
    return 3

def quantity_missionary():
    return 3

def quantity_boat():
    return 1

def index_caniball():
    return 0

def index_missionary():
    return 1

def index_boat():
    return 2

# Colocando todos do lado errado do Rio
primary = [quantity_caniball(), quantity_missionary(), quantity_boat()]
answer = [0, 0, 0]

def states(state):
    # Passando um canibal para o outro lado
    if state == 0:
        return [1, 0, 1]
    # Passando dois canibais para o outro lado
    elif state == 1:
        return [2, 0, 1]
    # Passando um missionario para o outro lado
    elif state == 2:
        return [0, 1, 1]
    # Passando dois missionario para o outro lado
    elif state == 3:
        return [0, 2, 1]
    # Passando um canibal e um missionario para o outro lado
    elif state == 4:
        return [1, 1, 1]

# Complementar do vetor primario no estado atual para o estado inicial
# Basicamente para checar as quantidades do outro lado do Rio
def complementary(vector):
    complementary = [quantity_caniball(),
                     quantity_missionary(),
                     quantity_boat()]
    return np.subtract(complementary, vector)

# Checar as regras do jogo
def is_valid(vector, is_complementary):
    # Checando se chegou ao resultado final
    if np.array_equal(vector, answer):
        return True

    # Checando se o vetor primario esta voltando ao estado inicial
    elif (vector[index_caniball()] == quantity_caniball() and
        vector[index_missionary()] == quantity_missionary() and
        not is_complementary):
        return False

    # Checando limite superior
    elif (vector[index_caniball()] > quantity_caniball() or
          vector[index_missionary()] > quantity_missionary()):
        return False

    # Checando limite inferior
    elif (vector[index_caniball()] < 0 or
          vector[index_missionary()] < 0):
        return False

    # Checando se existem mais canibais que missionarios
    elif vector[index_caniball()] > vector[index_missionary()] and vector[index_missionary()] > 0:
        return False
    
    return True

def check_state(is_increase, state):
    vector_under_test = []
    # Barco indo para o lado correto do rio
    if is_increase:
        vector_under_test = np.add(primary, states(state))
    # Barco indo para o lado errado do Rio
    else:
        vector_under_test = np.subtract(primary, states(state))
    if is_valid(vector_under_test, False) and is_valid(complementary(vector_under_test), True):
        return True

    return False

def print_result(result_states):
    initial = [quantity_caniball(), quantity_missionary(), quantity_boat()]
    # Apagando o no principal(pai de todos), ele nao eh relevante
    result_states.pop(0)
    is_increase = False
    print "M = Missionary, C = Caniball, B = Boat"
    print "  Left  --  Boat   --  Right"
    print 'C, M, B -- C, M, B -- C, M, B'
    side = ' -- 0, 0, 0 -- '
    print ', '.join(str(e) for e in initial) + side + ', '.join(str(e) for e in complementary(initial))
    for state in result_states:
        if is_increase:
            right = ', '.join(str(e) for e in initial)
            side = " <- " + ', '.join(str(e) for e in states(state)) + " -- "
            initial = np.add(initial, states(state))
            left = ', '.join(str(e) for e in complementary(initial))
            print right + side + left
        else:
            side = " -- " + ', '.join(str(e) for e in states(state)) + " -> "
            left = ', '.join(str(e) for e in complementary(initial))
            initial = np.subtract(initial, states(state))
            right = ', '.join(str(e) for e in initial)
            print right + side + left

        is_increase = not is_increase
        side = ' -- 0, 0, 0 -- '
        print ', '.join(str(e) for e in initial) + side + ', '.join(str(e) for e in complementary(initial))
    

def main():
    global primary
    is_increase = False
    result_states = [0]
    last_element = 0
    while not np.array_equal(primary, answer):
        valid = False
        for state in range(last_element, 5):
            # Checando os estados possiveis
            if check_state(is_increase, state) and state != result_states[-1]:
                # Caso seja um estado valido ele eh adicionado ao resultado                
                result_states.append(state)
                valid = True
                if is_increase:
                    primary = np.add(primary, states(state))
                else:
                    primary = np.subtract(primary, states(state))
                break
        
        # Caso nenhum estado seja possivel, entao o no anterior eh desfeito
        if not valid:
            last_element = result_states[-1]
            if is_increase:
                primary = np.add(primary, states(last_element))
            else:
                primary = np.subtract(primary, states(last_element))

            last_element = last_element + 1
            # Se o ultimo no for o maximo entao o problema nao eh possivel
            if last_element == 5:
                print "ERROR: Something is seriously wrong"
                exit()
            else:
                result_states = result_states[:-1]
                is_increase = not is_increase
        # Comecando um novo ciclo
        else:
            is_increase = not is_increase
            last_element = 0

    print "FINAL RESULT: "
    print_result(result_states)

if __name__ == "__main__":
    main()