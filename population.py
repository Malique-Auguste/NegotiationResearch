from actor import *

class Population:
    def __init__(self, group_descriptions):
        #represents the population as a dictionary of actors grouped under different group names
        self.inner = {}

        #iterates through a list of group descriptions
        # and creates an ammount of actors that atch the descriptions
        for group_descrip in group_descriptions:
            group_actors = []

            for i in range(0, group_descrip.num_actors):
                try:
                    group_actors.append(Actor(group_descrip))
                except ValueError as e:
                    raise ValueError(f"Error while creating actor. Group ({group_descrip}) resulted in {e}")
            
            self.inner[group_descrip.name] = group_actors

    def __str__(self):
        output = ""

        for group_name, actors in self.inner.items():
            output += group_name + "\r\n"
            
            for actor in actors:
                output += f"\t{str(actor)}\r\n"
        
        return output
                