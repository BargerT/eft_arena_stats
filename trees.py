import xml.etree.ElementTree as ET

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
        if kit.name.lower() == name.lower():
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