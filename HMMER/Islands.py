# Normal float values do not store enough decimal places.
# The probabilities generated by the HMM are so small we 
# must allow more decimal places to be allocated. 
from decimal import *
getcontext().prec = 28

states = ('A+', 'T+', 'C+', 'G+', 'A-', 'T-', 'G-', 'C-')
 
observations = []
with open('chr_22.txt') as f:
  while True:
    c = f.read(1)
    if not c:
      break 
    observations.append(c)
 
start_probability = {'A+': Decimal(0.125), 'T+': Decimal(0.125), 'G+': Decimal(0.125), 'C+': Decimal(0.125), 'A-': Decimal(0.125), 'T-': Decimal(0.125), 'G-': Decimal(0.125), 'C-': Decimal(0.125)}
 
###################### VALUE TO CHANGE ############################    
##################### TRANSITION WEIGHT ########################### 
p = 0.4


transition_probability = {
   'A+' : {'A+': Decimal(0.180 * (1-p)), 'C+': Decimal(0.268 * (1-p)), 'G+': Decimal(0.430 * (1-p)), 'T+': Decimal(0.122 * (1-p)), 'A-': Decimal(0.25 * p), 'C-': Decimal(0.25 * p), 'G-': Decimal(0.25 * p), 'T-': Decimal(0.25 * p)},
   'C+' : {'A+': Decimal(0.191 * (1-p)), 'C+': Decimal(0.299 * (1-p)), 'G+': Decimal(0.299 * (1-p)), 'T+': Decimal(0.211 * (1-p)), 'A-': Decimal(0.25 * p), 'C-': Decimal(0.25 * p), 'G-': Decimal(0.25 * p), 'T-': Decimal(0.25 * p)},
   'G+' : {'A+': Decimal(0.161 * (1-p)), 'C+': Decimal(0.346 * (1-p)), 'G+': Decimal(0.373 * (1-p)), 'T+': Decimal(0.120 * (1-p)), 'A-': Decimal(0.25 * p), 'C-': Decimal(0.25 * p), 'G-': Decimal(0.25 * p), 'T-': Decimal(0.25 * p)},
   'T+' : {'A+': Decimal(0.082 * (1-p)), 'C+': Decimal(0.357 * (1-p)), 'G+': Decimal(0.391 * (1-p)), 'T+': Decimal(0.170 * (1-p)), 'A-': Decimal(0.25 * p), 'C-': Decimal(0.25 * p), 'G-': Decimal(0.25 * p), 'T-': Decimal(0.25 * p)},
   

   'A-' : {'A+': Decimal(0.25 * p), 'C+': Decimal(0.25 * p), 'G+': Decimal(0.25 * p), 'T+': Decimal(0.25 * p), 'A-': Decimal(0.300 * (1-p)), 'C-': Decimal(0.200 * (1-p)), 'G-': Decimal(0.290 * (1-p)), 'T-': Decimal(0.210 * (1-p))},
   'C-' : {'A+': Decimal(0.25 * p), 'C+': Decimal(0.25 * p), 'G+': Decimal(0.25 * p), 'T+': Decimal(0.25 * p), 'A-': Decimal(0.319 * (1-p)), 'C-': Decimal(0.302 * (1-p)), 'G-': Decimal(0.081 * (1-p)), 'T-': Decimal(0.291 * (1-p))},   
   'G-' : {'A+': Decimal(0.25 * p), 'C+': Decimal(0.25 * p), 'G+': Decimal(0.25 * p), 'T+': Decimal(0.25 * p), 'A-': Decimal(0.251 * (1-p)), 'C-': Decimal(0.251 * (1-p)), 'G-': Decimal(0.299 * (1-p)), 'T-': Decimal(0.199 * (1-p))},
   'T-' : {'A+': Decimal(0.25 * p), 'C+': Decimal(0.25 * p), 'G+': Decimal(0.25 * p), 'T+': Decimal(0.25 * p), 'A-': Decimal(0.176 * (1-p)), 'C-': Decimal(0.242 * (1-p)), 'G-': Decimal(0.291 * (1-p)), 'T-': Decimal(0.291 * (1-p))}

   }
 
emission_probability = {
   'A+' : {'A': Decimal(1.0), 'T': Decimal(0.0), 'G': Decimal(0.0), 'C': Decimal(0.0)},
   'T+' : {'A': Decimal(0.0), 'T': Decimal(1.0), 'G': Decimal(0.0), 'C': Decimal(0.0)},
   'G+' : {'A': Decimal(0.0), 'T': Decimal(0.0), 'G': Decimal(1.0), 'C': Decimal(0.0)},
   'C+' : {'A': Decimal(0.0), 'T': Decimal(0.0), 'G': Decimal(0.0), 'C': Decimal(1.0)},
   'A-' : {'A': Decimal(1.0), 'T': Decimal(0.0), 'G': Decimal(0.0), 'C': Decimal(0.0)},
   'T-' : {'A': Decimal(0.0), 'T': Decimal(1.0), 'G': Decimal(0.0), 'C': Decimal(0.0)},
   'G-' : {'A': Decimal(0.0), 'T': Decimal(0.0), 'G': Decimal(1.0), 'C': Decimal(0.0)},
   'C-' : {'A': Decimal(0.0), 'T': Decimal(0.0), 'G': Decimal(0.0), 'C': Decimal(1.0)}
   }
   
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])
 
# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

def example():
    t= viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)
    islands=""
    for i in t[1]:
        islands+=i[1]
    return t[0], str(islands) 

print(example())
    
	
