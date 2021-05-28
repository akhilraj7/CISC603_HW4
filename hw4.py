from re import I
import pandas as pd
from pandas import ExcelWriter


def main():
    df = pd.read_excel('input.xlsx') # reading and getting the data from the input file
    nfa = df.set_index(['state']).T.to_dict('list')

    states = ['0', '1']         # states in the list
    for key, values in nfa.items():     #iterating through nfa dictionary to get the values accordingly
        val0 = str(values[0]).split()
        val1 = str(values[1]).split()
        res = [val0, val1]
        values = {states[i]: res[i] for i in range(len(states))}
        nfa[key] = values

    nfa_table = pd.DataFrame(nfa)   # storing the table in a dataframe
    print(nfa_table.transpose())

    new_states_list = []  # this will have all the new states created in dfa
    dfa = {}  # dfa dictionary for the output df
    # this will have all the states in nfa 
    # and also the states which are created in dfa and keeps appending till a condition is met
    list_of_keys = list(list(nfa.keys())[0])
    list_of_path = list(nfa[list_of_keys[0]].keys())

    # Here we are computing the first row of DFA table

    dfa[list_of_keys[0]] = {}  # creating a nested dictionary in dfa
    for y in range(len(states)):
        # creating a single string from all the elements of the list which is in new state
        var = "".join(nfa[list_of_keys[0]][list_of_path[y]])
        # assigning the state in DFA table
        dfa[list_of_keys[0]][list_of_path[y]] = var
        if var not in list_of_keys:  # check if the state is new and append it to the new_states_list
            new_states_list.append(var)
            # also add to the list_of_keys which has all the states
            list_of_keys.append(var)


    # Computing the other rows of DFA transition table
    for i in range(len(new_states_list)+4):
        # getting the first element of the new_states_list and checking
        dfa[new_states_list[0]] = {}
        for _ in range(len(new_states_list[0])):
            for i in range(len(list_of_path)):
                temp = []  # temp list
                for items in (new_states_list):
                    # getting rid of nan error
                    if 'nan' in items:
                        tmp = str(items)
                        tmp = tmp.replace('nan', "")
                        new_states_list[new_states_list.index(items)] = tmp

                for j in range(len(new_states_list[0])):
                    # Capturing all of the states
                    temp += nfa[new_states_list[0][j]][list_of_path[i]]
                    print(temp)
                s = ""

                # creating a single string which is a new state from all the elements of the list
                s = s.join(temp)
                if s not in list_of_keys:  # Checking if the state is new and then appending it to the new_states_list
                    new_states_list.append(s)
                    # also append to the list_of_keys which has all the states
                    list_of_keys.append(s)
                # add new state in the DFA table
                dfa[new_states_list[0]][list_of_path[i]] = s

        # Removing the first element in the new_states_list
        new_states_list.remove(new_states_list[0])

    print("\nDFA :- \n")
    print(dfa)  # Printing the DFA created
    print("\nPrinting DFA table :- ")
    dfa_table = pd.DataFrame(dfa)
    dfa_table = dfa_table.transpose()
    writer = ExcelWriter('Output.xlsx')
    dfa_table.to_excel(writer, 'Sheet5')
    writer.save()
    print(dfa_table)

main()
