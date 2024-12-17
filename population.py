from actor import *
from random import choice, randrange
from time import time

class Log:
    def __init__(self, avg_svo, proposal_vec, votes, state_summary):
        self.avg_svo = avg_svo
        self.proposal_vec = proposal_vec
        self.votes = votes
        self.state_summary = state_summary
        self.timestamp = time()

    def __str__(self):
        output = ""
        if None in self.proposal_vec:
            output = f"avg_svo: {self.avg_svo:.2f}\r\nproposal_vec: (None, None)\r\nvotes: n/a\r\n{self.state_summary}\r\ntimestamp: {self.timestamp:.2f}"
        else:
            output = f"avg_svo: {self.avg_svo:.2f}\r\nproposal_vec: ({self.proposal_vec[0]:.2f}, {self.proposal_vec[1]})\r\n"
            
            if self.votes[0] > self.votes[1]:
                output += "accepted: "
            else:
                output += "rejected: "
            
            output += f"{self.votes}\r\n"
            
            for summary in self.state_summary:
                output += f"{summary[0]}|num_actors:{len(summary[1])}|avg_svo:{summary[2]:.2f}\r\n"
            
            output += f"timestamp: {self.timestamp:.2f}"
        
        return output

class Population:
    def __init__(self, group_descriptions):
        #represents the population as a dictionary of actors grouped under different group names
        self.inner = {}

        #stores logs after iterations
        self.logs = []

        #total number of actors
        self.num_actors = 0

        #iterates through a list of group descriptions
        # and creates an ammount of actors that atch the descriptions
        for i, group_descrip in enumerate(group_descriptions):
            self.num_actors += group_descrip.num_actors

            group_actors = []

            for i in range(0, group_descrip.num_actors):
                try:
                    group_actors.append(Actor(group_descrip))
                except ValueError as e:
                    raise ValueError(f"Error while creating actor. Group ({group_descrip}) resulted in {e}")
            
            self.inner[group_descrip.name] = group_actors
        
        self.log()

    def get_avg_svo(self):
        avg_svo = 0.0
        num_actors = 0

        for group_actors in self.inner.values():
            num_actors += len(group_actors)

            for actor in group_actors:
                avg_svo += actor.svo


        avg_svo /= num_actors
        return avg_svo
    
    def get_indexed_actor(self, i):
        j = 0
        for group_name in self.inner.keys():
            for actor in self.inner[group_name]:
                if j == i:
                    return actor
                else:
                    j += 1

    def iterate(self):
        #selects an actor at random to make a proposal
        proposer_index = randrange(0, self.num_actors)
        proposer = self.get_indexed_actor(proposer_index)

        

        #generates proposal
        proposal_vec = proposer.gen_proposal()

        votes_for = 0
        votes_against = 0

        for group_actors in self.inner.values():
            for actor in group_actors:
                vote = actor.gen_vote(proposal_vec)
                
                if vote:
                    votes_for += 1
                else:
                    votes_against += 1
                
                if vote == False:
                    actor.adjust_svo(proposal_vec[0])
        
        #proposal is considered passed if ore than hale of the people voted for it
        self.log(proposal_vec, (votes_for, votes_against))
    
    def log(self, proposal_vec = (None, None), votes = (None, None)):
        self.logs.append(Log(self.get_avg_svo(), proposal_vec, votes, self.summarize_state()))

    def summarize_state(self):
        output = []

        for group_name, group_actors in self.inner.items():
            avg_svo = 0
            
            for actor in group_actors:
                avg_svo += actor.svo
            
            avg_svo /= len(group_actors)

            output.append((group_name, len(group_actors), avg_svo))
        
        return output

    def __str__(self):
        output = ""

        for group_name, group_actors in self.inner.items():
            output += "\r\n" + group_name
            
            for actor in group_actors:
                output += f"\t{str(actor)}"

        output = output.strip()
        
        return output
                