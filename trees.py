import xml.etree.ElementTree as ET
import math

class Kit:
    def __init__(self, name, exp, ammo, armor, price):
        self.name = name
        self.exp = exp
        # first value is damage
        # second value is penetration
        # third value is rpm of the weapon
        self.ammo = ammo
        # first value is helmet armor value
        # second value is face shield armor value
        # third value is chest armor value
        self.armor = armor
        self.price = price
        self._parent = None
        self._children = []

# reads class trees from XML files and populate them into this custom data type
# holds the list of both root nodes in each tree
# the root has a children list that stores the kits it can move to
# to traverse a tree we walk down the list of children until reaching the bottom
class Tree:
    def __init__(self, class_type):
        self.class_type = class_type
        self.root = []
        self.create_tree()

    # populates the tree with kit values from the list
    def create_tree(self):
        # Path to the XML file to be read
        xml_file = ET.parse("XML/" + self.class_type + ".xml")
        root = xml_file.getroot()
        # For the two children at the top level of the tree
        for child in root:
            # add the tree from that top level child to the root
            kit = Kit(child.attrib["id"], child[0].text, [child[1][0].text, child[1][1].text, child[1][0].text], [child[2][0].text, child[2][1].text, child[2][2].text], child[3].text)
            # add the root kit to the top level of the tree and build the tree under it
            self.root.append(self.create_tree_r(child))
    
    # take a xml file root
    # work through the branches while appending them to the tree
    # return the kit and append to the list of children from the previous call
    def create_tree_r(self, root, parent=None):
        make_kit = []
        for child in root:
            # if we are looking at ammo it is a list of values
            if child.tag == "ammo":
                ammo_list = []
                for grandchild in child:
                    ammo_list.append(int(grandchild.text))
                make_kit.append(ammo_list)
            # if we are looking at armor it is also a list of values
            elif child.tag == "armor":
                armor_list = []
                for grandchild in child:
                    armor_list.append(int(grandchild.text))
                make_kit.append(armor_list)
            elif child.tag == "kit":
                continue
            # since this file is in order it does not cause issues
            # the exp and cost tags should trigger this
            else:
                make_kit.append(int(child.text))
            
        kit = Kit(root.attrib["id"], make_kit[0], make_kit[1], make_kit[2], make_kit[3])

        # if we are not at the top level kits then set the parent of the kit
        if parent != None:
            kit._parent = parent
        # if the kit does not have a child attribute return the kit because we have reached the leaf
        if len(root) < 5:
            return kit
        # if the kit has two children
        elif len(root) == 6:
            kit._children.append(self.create_tree_r(root[5], kit))
            kit._children.append(self.create_tree_r(root[4], kit))
            return kit
        # if the kit has one child
        else:
            kit._children.append(self.create_tree_r(root[4], kit))
            return kit
        
    # given a name of a kit return a list of the kits in the path
    def find_kit(self, name, kit=None):
        # search both sides of the kit
        if kit == None:
            first_search = self.find_kit(name, self.root[0])
            second_search = self.find_kit(name, self.root[1])
            if first_search != None:
                return first_search
            return second_search
        
        # if the kit matches than record the path back to the top and return it
        elif kit.name.lower() == name.lower():
            cur_kit = kit
            path_to_kit = []
            while cur_kit._parent != None:
                path_to_kit.append(cur_kit)
                cur_kit = cur_kit._parent
            # don't forget the root of the tree
            path_to_kit.append(cur_kit)
            return path_to_kit
        else:
            # if we have reached the bottom and not found it then return None
            if not kit._children:
                return None
            # else if the current kit has two children search both subtrees and return the solution or None
            elif len(kit._children) == 2:
                first_search = self.find_kit(name, kit._children[0])
                second_search = self.find_kit(name, kit._children[1])
                if first_search != None:
                    return first_search
                return second_search 
            # otherwise the kit only has one child. Search the subtree and return the result
            else:
                return self.find_kit(name, kit._children[0])
        
    # This function returns the total exp required to unlock a specific kit in the tree
    def get_total_exp(self, kit):
        path_to_kit = self.find_kit(kit.name)
        total_exp = 0
        for node in path_to_kit:
            total_exp += node.exp
        
        return total_exp
    
    # This function takes a kit and calculates the longest time to unlock
    # It is based on experience gained for losing a match with 0 eliminations and the exp required
    def worst_case_unlock_time(self, kit):
        total_exp = self.get_total_exp(kit)
        return math.ceil(total_exp / 3500)
    
    # This function takes a kit and calculates the shorted time to unlock
    # It is based on experience gained for winning a match with 10 eliminations
    # Each elimination is worth 250 exp and a win is 5500 experience
    def best_case_unlock_time(self, kit):
        total_exp = self.get_total_exp(kit)
        return math.ceil(total_exp / 8000)

    # Take the best and the worst case and average it to find the average case unlock time
    def average_case_unlock_time(self, kit):
        return math.ceil((self.worst_case_unlock_time(kit) + self.best_case_unlock_time(kit)) / 2)
    
    # This function takes a kit and finds the efficiency of it by comparing its DPS and Armor to EXP required
    def calculate_efficiency(self, kit):
        rps = kit.ammo[2] / 60
        # This attempts to normalzie damage against tier 5 armor
        # Tarkov damage technically takes durability away from armor with each shot
        # Any ammo with penetration > armor level has ~90% chance to penetrate
        # Also as armor durability declines armor level declines as well
        # This is why this formula is extremely simple compared to the true calculations
        if kit.ammo[1] > 50:
            normalized_penetration = 1.00
        else:
            normalized_penetration = (kit.ammo[1] * 2) / 100 
        ammo_damage = kit.ammo[0]

        dps = (ammo_damage * normalized_penetration) * rps

        # High tier armor is extremely valuable and adding 4 or 5 points is negligable to the total so increase the benefit
        armor_value = (kit.armor[0] * 10000) + (kit.armor[1] * 10000) + (kit.armor[2] * 10000)
        
        # The first kits are free and require 0 experience
        # if one is trying to be calculated it should be penalized heavily
        # As the first kits will never be the most efficient
        avg_case = self.average_case_unlock_time(kit)
        if avg_case == 0:
            return round((dps + armor_value) / 60, 2)
        elif avg_case <= 50:
            return round((dps + armor_value) / 40, 2)
        else:
            return round((dps + armor_value) / avg_case, 2)
    
    # Takes nothing as input and returns the most efficient kit in this tree
    def find_most_efficient(self, kit=None, cur_max=None):
        # Lets search both sides of the tree and return the most efficient
        if kit == None:
            left_branch = self.find_most_efficient(self.root[0], self.root[0])
            right_branch = self.find_most_efficient(self.root[1], self.root[1])
            if left_branch != None:
                if right_branch != None:
                    if self.calculate_efficiency(left_branch) > self.calculate_efficiency(right_branch):
                        return left_branch
                    else:
                        return right_branch
                return left_branch
            return right_branch
        
        # if the current max efficiency kit is still empty keep searching
        if cur_max == None:
            # else if the current kit has two children search both subtrees and return the solution
            if len(kit._children) == 2:
                first_search = self.find_most_efficient(kit._children[0], kit)
                second_search = self.find_most_efficient(kit._children[1], kit)
                if first_search != None:
                    if second_search != None:
                        if self.calculate_efficiency(first_search) > self.calculate_efficiency(second_search):
                            return first_search
                        else:
                            return second_search
                    return first_search
                return second_search 
            # otherwise the kit only has one child. Search the subtree and return the result
            else:
                return self.find_most_efficient(kit._children[0], kit)
        else:
            # If our current kit is more efficient it becomes our new cur max
            if self.calculate_efficiency(kit) > self.calculate_efficiency(cur_max):
                cur_max = kit
            # If we are at the bottom of this branch return the max
            if not kit._children: 
                return cur_max
            # else if the current kit has two children search both subtrees for a more efficient kit
            elif len(kit._children) == 2:
                first_search = self.find_most_efficient(kit._children[0], cur_max)
                second_search = self.find_most_efficient(kit._children[1], cur_max)
                if first_search != None:
                    if second_search != None:
                        if self.calculate_efficiency(first_search) > self.calculate_efficiency(second_search):
                            return first_search
                        else:
                            return second_search
                    return first_search
                return second_search 
            # otherwise the kit only has one child. Search the subtree and return the result
            else:
                return self.find_most_efficient(kit._children[0], cur_max)