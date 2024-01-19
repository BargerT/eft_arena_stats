from trees import Tree

def main():
    assault = Tree("Assault")
    cqb = Tree("CQB")
    scout = Tree("Scout")
    marksman = Tree("Marksman")
    
    print("Searching Tree for Sector")
    sector_search = assault.find_kit("Pharaoh")
    worst_case = assault.worst_case_unlock_time(sector_search[0])
    avg_case = assault.average_case_unlock_time(sector_search[0])
    best_case = assault.best_case_unlock_time(sector_search[0])
    print(f"Sector worst case unlock time = {worst_case} games")
    print(f"Sector best case unlock time = {best_case} games")
    print(f"Sector average case unlock time = {avg_case} games")

main()