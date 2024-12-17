from random import uniform
from math import sqrt, erf, exp, pi
from scipy.special import erfinv


class GroupDescription:
    def __init__(self, num_actors, svo, sd, svo_delta, w, name):
        if num_actors <= 0 and not isinstance(num_actors, int):
            raise ValueError(f"num_actors ({num_actors}) mus tbe an integer grater than 0.")
        elif svo > 1.0 or svo < 0.0:
            raise ValueError(f"svo ({svo}) is out of range. Expected 0 <= svo <= 1")
        elif sd > 1.0 or sd <= 0.0:
            raise ValueError(f"sd ({sd}) is out of range. Expected 0 < sd <= 1")
        elif svo_delta > 1.0 or svo_delta < 0.0:
            raise ValueError(f"svo_delta ({svo_delta}) is out of range. Expected 0 <= svo_delta <= 1")
        elif svo != 0.0 and svo_delta != 0.0:
            raise ValueError(f"Actors are not 100% pro social (given svo = {svo}), therefore their svo cannot change (however, given svo_delta = {svo_delta}).")
        elif w > 2.0 or w <= 0.0:
            raise ValueError(f"w ({w}) is out of range. Expected 0 < w <= 2")
        
        self.num_actors = num_actors
        self.svo = svo
        self.sd = sd
        self.svo_delta = svo_delta
        self.w = w
        self.name = name
    
    def __str__(self):
        return f"num_actors:{self.num_actors}|svo:{self.svo}|sd:{self.sd}|svo_delta:{self.svo_delta}|w:{self.w}|name:{self.group_name}"


class Actor:
    def __init__(self, group_description):        
        #social value orientation
        # 0 <= svo <= 1
        # svo = 0     => 100% pro social
        # svo = 0.5   => 50% pro self, 50% pro social
        # svo = 1     => 100% pro self
        self.svo = group_description.svo

        #stadard deviation of normal distribution
        # 0 < sd <= 1
        self.sd = group_description.sd

        #change in svo
        # 0 <= svo_delta <= 1
        # this is only non zero, if the actor is initially 100% pro social
        self.svo_delta = group_description.svo_delta

        #width of the range used to calculate probability of voting
        # 0 < w <= 2
        self.w = group_description.w

        #used to indicate which group an actor belongs to
        self.group_name = group_description.name


    #probability density function
    def pdf(self, input):
        #computes
        a = 2 * exp(-((input - self.svo) ** 2) / (2 * (self.sd ** 2))) / (self.sd * sqrt(2 * pi))
        b = erf((1 + self.svo) / (self.sd * sqrt(2))) + erf((1 - self.svo) / (self.sd * sqrt(2)))
        c = a / b

        return c

    #cummulative distribution function
    # of this actor's internal distribution
    def cdf(self, input):
        #performs calculations
        a = erf((sqrt(2) * (input - self.svo)) / (2 * self.sd)) + 1
        b = a / (erf((1 + self.svo) / (self.sd * sqrt(2))) + erf((1 - self.svo) / (self.sd * sqrt(2))))

        return b

    #inverse of the cummulative distribution function
    # of this actor's internal distribution
    def cdf_inv(self, input):
        #performs calculations
        a = erf((1 + self.svo) / (self.sd * sqrt(2))) + erf((1 - self.svo) / (self.sd * sqrt(2)))
        b = (sqrt(2) * self.sd * erfinv((input * a) - 1)) + self.svo

        #clamps output to a range from 0.0 to 1.0
        c = max(0.0, min(b, 1.0))

        return c

    #implements inverse transform sampling to generate random numbers matching the actor's unique distribution
    def gen_proposal(self):
        # initial random number obtained by uniformally sampling the approproite range
        u = uniform(self.cdf(-1.0), self.cdf(1.0))
        proposal_svo = self.cdf_inv(u)

        #returns a proposal vector
        # where the 1st number indicates to what degree it benefits everyone versus a group
        # and the 2nd number indicates which group the preference is towards.
        # i.e magnitude and direction
        proposal_vec = (proposal_svo, self.group_name)

        return proposal_vec
    
    #calculates the probability of voting for a proposal
    def gen_vote_prob(self, proposal_svo):
        vote_prob = exp(-((proposal_svo - self.svo)**2) / (2 * (self.sd ** 2)))
        
        return vote_prob

    #returns true/false if the actor votes ro doesnt for the proposed policy
    def gen_vote(self, proposal_vec):
        proposal_svo = proposal_vec[0]

        #if the proposal doesn't benefit the actor's group, it benefit's another group
        # thus it's svo is negative not positive
        if proposal_vec[1] != self.group_name:
            proposal_svo *= -1
        
        #calcultes the probability fo voting for this policy
        vote_prob = self.gen_vote_prob(proposal_svo)

        #calculates vote
        vote = True
        if uniform(0.0, 1.0) > vote_prob:
            vote = False

        return vote
    
    #adjusts svo if actor doesn't vote for a policy
    def adjust_svo(self, proposal_svo):
        self.svo += self.svo_delta * (1.0 - (2 * exp(-((proposal_svo)**2) / (2 * (self.sd ** 2)))))
        self.svo = max(0.0, min(self.svo, 1.0))
    
    def __str__(self):
        return f"svo:{self.svo:.2f}|sd:{self.sd:.2f}|svo_delta:{self.svo_delta:.2f}|w:{self.w:.2f}|group:{self.group_name}"
