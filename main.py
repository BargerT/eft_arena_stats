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
    assault_most_efficient = assault.find_most_efficient()
    scout_most_efficient = scout.find_most_efficient()
    cqb_most_efficient = cqb.find_most_efficient()
    marskman_most_efficient = marksman.find_most_efficient()
    print(f"The most efficient kit in assault is {assault_most_efficient.name}")
    print(f"The most efficient kit in scout is {scout_most_efficient.name}")
    print(f"The most efficient kit in cqb is {cqb_most_efficient.name}")
    print(f"The most efficient kit in marksman is {marskman_most_efficient.name}")    

main()