from constraint_programming import constraint_programming

maison = [1,2,3,4,5]
categories = [["bleu", "blanc", "vert","jaune", "rouge"],\
["norvegien", "anglais", "espagnol", "ukrainien", "japonais"],\
["cheval", "chien", "escargot", "renard", "zebre"],\
["kools", "cravens", "old golds", "gitanes", "chesterfields"],\
["lait","café","thé", "vin", "eau"]]


var = {x: set(maison) for category in categories for x in category}
var["norvegien"] = set([1])
var["bleu"] = set([2])
var["lait"] = set([3])

P = constraint_programming(var)
EQ = { (i, i) for i in maison }
NEQ = { (i, j) for i in maison for j in maison if i!=j }
COTE = { (i, j) for i in maison for j in maison if abs(i-j)==1 }
NEXT = { (i, j) for i in maison for j in maison if i==j+1 }

P.addConstraint("anglais", "rouge", EQ)
P.addConstraint("vert", "café", EQ)
P.addConstraint("jaune", "kools", EQ)
P.addConstraint("blanc", "vert", NEXT)
P.addConstraint("espagnol", "chien", EQ)
P.addConstraint("ukrainien", "thé", EQ)
P.addConstraint("japonais", "cravens", EQ)
P.addConstraint("old golds", "escargot", EQ)
P.addConstraint("gitanes", "vin", EQ)
P.addConstraint("chesterfields", "renard", COTE)
P.addConstraint("kools", "cheval", COTE)

for category in categories:
    for x in category:
        for y in category:
            if x!=y:
                P.addConstraint(x, y, NEQ)

sol = P.solve()

owner = "Not found"
zebre_num = sol["zebre"]
for nationality in categories[1]:
    if sol[nationality] == zebre_num:
        owner = nationality

print("Le propriétaire est le {}".format(owner))