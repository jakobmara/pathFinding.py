class Node:
    def __init__(self, parent = None, coord = [None, None]):
        self.parent = parent
        self.f = 0
        if parent == None:
            self.g = 0
        else:
            self.g= parent.g + 1
        self.h = 0
        self.coord = coord
    
    def __eq__(self, o: object) -> bool:
        #checks to see if has same f value at same coord
        if o == None:
            return False
        return o.f == self.f and self.coord == o.coord
    
    def __str__(self):
        if self.parent == None:
            return (f"No Parent \ncurrent coord: {self.coord} g: {self.g} h: {self.h} f: {self.f}")
        return(f"parent coord: {self.parent.coord}\ncurrent coord: {self.coord} g: {self.g} h: {self.h} f: {self.f}")