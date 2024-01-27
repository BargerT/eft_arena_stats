from trees import Tree

def remove_spaces_and_lower(fix):
    return fix.replace(" ", "").lower()

def list_of_kits_to_string(name, list):
    ret_str = f"Path to {name} is:"
    for i in range(len(list) - 1, 0, -1):
        if i == 1:
            ret_str += " " + list[i].name
        else:
            ret_str += " " + list[i].name + ","
    ret_str += "\n"
    return ret_str

def search_all_trees(command, name=None, tree=None):
    assault = Tree("Assault")
    cqb = Tree("CQB")
    scout = Tree("Scout")
    marksman = Tree("Marksman")

    if command == "most":
        if tree == "assault":
            return assault.find_most_efficient()
        elif tree == "cqb":
            return cqb.find_most_efficient()
        elif tree == "scout":
            return scout.find_most_efficient()
        elif tree == "marksman":
            return marksman.find_most_efficient()
        elif tree == "all":
            return assault.find_most_efficient(), cqb.find_most_efficient(), scout.find_most_efficient(), marksman.find_most_efficient(), assault, cqb, scout, marksman
        else:
            print(f"{tree} is not a valid class name. Please check spelling and try again\n")
    else:
        assault_search = assault.find_kit(name)
        if not assault_search:
            cqb_search = cqb.find_kit(name)
            if not cqb_search:
                scout_search = scout.find_kit(name)
                if not scout_search:
                    marksman_search = marksman.find_kit(name)
                    if not marksman_search:
                        print(f"{name} was not found in any class trees. Please check your spelling or try another name\n")
                        return None
                    else:
                        print(f"{name} found in the Marksman tree")
                        return marksman_search, marksman
                else:
                    print(f"{name} found in the Scout tree")
                    return scout_search, scout
            else:
                print(f"{name} found in the CQB tree")
                return cqb_search, cqb
        else:
            print(f"{name} found in the Assault tree")
            return assault_search, assault

def search():
    find = input("What is name of the kit you would like to find?\n")
    print("")
    formatted_find = remove_spaces_and_lower(find)
    path = search_all_trees("search", formatted_find)
    if path:
        print(list_of_kits_to_string(formatted_find, path[0]))

def gamesrequired():
    kit = input("what is the kit you would like to unlock?\n")
    formatted_kit = remove_spaces_and_lower(kit)
    path = search_all_trees("games", formatted_kit)
    if path:
        best_case = path[1].best_case_unlock_time(path[0][0])
        worst_case = path[1].worst_case_unlock_time(path[0][0])
        avg_case = path[1].average_case_unlock_time(path[0][0])
        print(f"{formatted_kit} would take {best_case} games at best, {worst_case} at worst, and {avg_case} on average\n")

def mostefficient():
    tree = input("Which tree would you like to search? (Assault, CQB, Scout, Marksman, All)\n")
    formatted_tree = remove_spaces_and_lower(tree)
    most_efficient = search_all_trees("most", None, formatted_tree)
    if len(most_efficient) > 2:
        efficiency_list = []
        for i in range(0, 4):
            efficiency_list.append(most_efficient[i + 4].calculate_efficiency(most_efficient[i]))
        
        most_efficient_index = efficiency_list.index(max(efficiency_list))
        print(f"The most efficient kit in all trees is: {most_efficient[most_efficient_index].name}\n")
    else:
        print(f"The most efficienct kit from the {formatted_tree} is {most_efficient[0].name}\n")
        
def efficiency():
    find = input("What kit would you like to know the efficiency for?\n")
    formatted_find = remove_spaces_and_lower(find)
    found = search_all_trees("efficiency", formatted_find)
    if found:
        print(f"The effiency of {formatted_find} is: {found[1].calculate_efficiency(found[0][0])}")
        print("This is calculated by combining its potential DPS and Armor Values and dividing by the games required to unlock\n")

def main():
    print("What would you like to do?")
    while True:
        command = input("Commands: Search, Games Required, Most Efficient, Efficiency, Exit\n")
        formatted_command = remove_spaces_and_lower(command)
        print("")
        if formatted_command == "exit":
            print("Now Exiting")
            break
        elif formatted_command == "search":
            search()
        elif formatted_command == "gamesrequired":
            gamesrequired()
        elif formatted_command == "mostefficient":
            mostefficient()
        elif formatted_command == "efficiency":
            efficiency()
        else:
            print("Command Invalid: Please check spelling and try again")
        

main()