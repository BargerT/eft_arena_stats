from trees import Tree

def main():
    assault = Tree("Assault")
    print("Searching Tree for Sector")
    sector_search = assault.find_kit("Sector")
    if sector_search != None:
        print("Sector was found the path was:")
        total_exp = 0
        for kit in sector_search:
            total_exp += kit.exp
            print(f"{kit.name}")
        print(f"Total exp is: {total_exp}")

main()