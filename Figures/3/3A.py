import matplotlib.pyplot as plt
import matplotlib
import cPickle as pic

print "Loading Aromatic"
aromatic = pic.load(open('aromatic.pkl','rb'))
aromatic = [i/max(aromatic) for i in aromatic]

print "Loading Positive"
positive = pic.load(open('positive.pkl','rb'))
positive = [i/max(positive) for i in positive]

print "Loading Negative"
negative = pic.load(open('negative.pkl','rb'))
negative = [i/max(negative) for i in negative]

# leucine = pic.load(open('leucine.pkl','rb'))
# leucine = [i/max(leucine) for i in leucine]

# n_amine = pic.load(open('n_amine.pkl','rb'))
# n_amine = [i/max(n_amine) for i in n_amine]

everything = pic.load(open('all.pkl','rb'))
everything = [i/max(everything) for i in everything]

x = range(3,23)

fig, ax = plt.subplots(figsize=(10,5))
# ax.set_title("EMRinger Score over 5-frame average dose windows", y=1.05)
ax.set_xlabel("Center frame of 5-frame window", labelpad=10)
ax.set_ylabel("Normalized EMRinger score", labelpad=10)
ax.set_ylim(-1,1.2)
ax.plot(x, everything, label="All", color='k')
ax.plot(x, aromatic, label="Aromatic", color='#EE9A00')
ax.plot(x, positive, label="Positively charged", color='#5DA5DA')
ax.plot(x, negative, label="Negatively charged", color='#F15854')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xlim(3,22)
ax.axhspan(-0.005,0.005,color='0.1',alpha=0.3, linewidth=0)
# ax.plot(x, leucine, label="Leucine residues")
# ax.plot(x, n_amine, label="Glutamine and Asparagine")
# plt.legend(loc='lower center', ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.set_ticks_position('left') # this one is optional but I still recommend it...
ax.xaxis.set_ticks_position('bottom')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
leg = ax.legend(bbox_to_anchor=(0.01, 0.95, 1., .1), loc=3,
       	ncol=4, mode="expand", borderaxespad=0., fontsize=16)
leg.get_frame().set_linewidth(0.0)
fig.savefig('3A.png')
