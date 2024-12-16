from random import seed

from actor import Actor

seed(0)

a = Actor(0.0, 0.3, 0.1, 0.4, "FUP")

print(a)
print("0 pdf:", a.pdf(0.0))
print("0.6 pdf:", a.pdf(0.6))
print("0 cdf:", a.cdf(0.0))
print("0.6 cdf:", a.cdf(0.6))
print("0 cdf_inv:", a.cdf_inv(0.0))
print("0.6 cdf_inv:", a.cdf_inv(0.6))
print("proposals:", a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal())
print("0 vote_prob:", a.gen_vote_prob(0.0))
print("0.6 vote_prob:", a.gen_vote_prob(0.6))
print("0 FUP votes:", a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")))
print("0.6 FUP votes:", a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), 
      a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")))
print("0.6 HAC votes:", a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")),
      a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")))

print("\n-----\n")

a = Actor(0.5, 0.3, 0.0, 0.4, "FUP")

print(a)
print("0 pdf:", a.pdf(0.0))
print("0.6 pdf:", a.pdf(0.6))
print("0 cdf:", a.cdf(0.0))
print("0.6 cdf:", a.cdf(0.6))
print("0 cdf_inv:", a.cdf_inv(0.0))
print("0.6 cdf_inv:", a.cdf_inv(0.6))
print("proposals:", a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal())
print("0 vote_prob:", a.gen_vote_prob(0.0))
print("0.6 vote_prob:", a.gen_vote_prob(0.6))
print("1 vote_prob:", a.gen_vote_prob(1.0))
print("0 FUP votes:", a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")))
print("0.6 FUP votes:", a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), 
      a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")))
print("1.0 FUP votes:", a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), 
      a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")), a.gen_vote((1.0, "FUP")))



print("\n-----\n")

a = Actor(1.0, 0.3, 0.0, 0.4, "HAC")

print(a)
print("0 pdf:", a.pdf(0.0))
print("0.6 pdf:", a.pdf(0.6))
print("0 cdf:", a.cdf(0.0))
print("0.6 cdf:", a.cdf(0.6))
print("0 cdf_inv:", a.cdf_inv(0.0))
print("0.6 cdf_inv:", a.cdf_inv(0.6))
print("proposals:", a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal(), a.gen_proposal())
print("0 vote_prob:", a.gen_vote_prob(0.0))
print("0.6 vote_prob:", a.gen_vote_prob(0.6))
print("0.9 vote_prob:", a.gen_vote_prob(0.9))
print("0 FUP votes:", a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")), a.gen_vote((0.0, "FUP")))
print("0.6 FUP votes:", a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), 
      a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")), a.gen_vote((0.6, "FUP")))
print("0.6 HAC votes:", a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")),
      a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")), a.gen_vote((0.6, "HAC")))
print("0.9 HAC votes:", a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), 
      a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")), a.gen_vote((0.9, "HAC")))