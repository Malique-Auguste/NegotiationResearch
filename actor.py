from random import uniform
from math import sqrt, erf, exp, pi
from scipy.special import erfinv

class Actor:
    def __init__(self, svo, sd, svo_delta, w, group):
        if svo > 1.0 or svo < 0.0:
            raise ValueError(f"svo ({svo}) is out of range. Expected 0 <= svo <= 1")
        elif sd > 1.0 or sd <= 0.0:
            raise ValueError(f"sd ({sd}) is out of range. Expected 0 < sd <= 1")
        elif svo_delta > 1.0 or svo_delta < 0.0:
            raise ValueError(f"svo_delta ({svo_delta}) is out of range. Expected 0 <= svo_delta <= 1")
        elif svo != 0.0 and svo_delta != 0.0:
            raise ValueError(f"Actor is pro self (given svo = {svo}), therefore their svo cannot change (given svo_delta = {svo_delta}).")
        elif w > 2.0 or w <= 0.0:
            raise ValueError(f"w ({w}) is out of range. Expected 0 < w <= 2")

        
        #social value orientation
        # 0 <= svo <= 1
        # svo = 0     => 100% pro social
        # svo = 0.5   => 50% pro self, 50% pro social
        # svo = 1     => 100% pro self
        self.svo = svo

        #stadard deviation of normal distribution
        # 0 < sd <= 1
        self.sd = sd

        #change in svo
        # 0 <= svo_delta <= 1
        # this is only non zero, if the actor is initially 100% pro social
        self.svo_delta = svo_delta

        #width of the range used to calculate probability of voting
        # 0 < w <= 2
        self.w = w

        #used to indicate which group an actor belongs to
        self.group = group


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
        proposal_vec = (proposal_svo, self.group)

        return proposal_vec
    
    #calculates the probability of voting for a proposal
    def gen_vote_prob(self, proposal_svo):
        vote_prob = exp(-((proposal_svo - self.svo)**2) / (2 * (self.sd ** 2)))
        
        return vote_prob


    def gen_vote(self, proposal_vec):
        proposal_svo = proposal_vec[0]

        #if the proposal doesn't benefit the actor's group, it benefit's another group
        # thus it's svo is negative not positive
        if proposal_vec[1] != self.group:
            proposal_svo *= -1
        
        #calcultes the probability fo voting for this policy
        vote_prob = self.gen_vote_prob(proposal_svo)

        #calculates vote
        vote = True
        if uniform(0.0, 1.0) > vote_prob:
            vote = False

        return vote
    
    def __str__(self):
        return f"svo:{self.svo}|sd:{self.sd}|svo_delta:{self.svo_delta}|w:{self.w}|group:{self.group}"



        