def printAroSummary_2(self,infile):
    """Gets atoms on each aro cycle, groups the adjacent ones and sets them into groups if any. Prints on terminal and 
    stores on text file with the same name as the .mol2 file
    """
    def list_duplicates(seq):
        """Function to returns the elements that appear more than once in a list."""
        seen = set()
        seen_add = seen.add
        seen_twice = set( x for x in seq if x in seen or seen_add(x) )
        return list( seen_twice )           

    newfile=open("aro_system_%s.txt"%self.name,"w")
    rings = self.aro_cycles
    pairs = []
    
    count = -1
    for x in rings:
        count += 1
        info = str(f"Atoms in cycle {count}: {x}")  
        print(info)
        newfile.write(f"{info}\n")

    #Creates a list with pairs of adjacent cycles
    #Goes through all but the last element in self.aro_cycles to avoid exceeding len(self.aro_cycles)
    ch = -1
    for cycle_hunt in rings[:-1]:
        ch += 1
        cp = 0
        for cycle_prey in rings[1:]:     
            cp += 1
            if cp>ch and  any( atm in cycle_prey for atm in cycle_hunt ): # Only wan atom shared is necesary to consider adjacency
                pairs.append([ch,cp])
    
    print(f"\nPairs of adjacent aro cycles:")
    newfile.write(f"\nPairs of adjacent aro cycles:\n")
    for x in pairs:
        cycs = (rings[x[0]],rings[x[1]])
        print(cycs)
        newfile.write(str(f"{cycs}\n"))

    groups = [pairs[0]]

    if len(pairs) >  1:  # Only if there is mor than one pair
        for p in pairs[1:]:
            flag = False
            cg = -1
            for g in groups:
                cg += 1
                if any(c in g for c in p): # If there is an element from the pair that is in this group
                flag = True             # Then, we make flag=True and break the cycle
                break                   # with the counter we know in which group it was
            if flag:                       # If clycle through groups end in break and flag =True
            g.append(p[0])              # Then we add the pair cycles to the group
            g.append(p[1])              #
            g = list(set(g))            # eliminate the repeated ones
            groups[cg]= g               # and update the groups list    
            else:
            groups.append(p)            # if elements of the pair aint in one group then
                                        # create its own group

        cycles_in_pairs = list(set([ x for p in pairs for x in p ]))
        cycles_in_groups = [ x for g in groups for x in g ]

        while not len(cycles_in_pairs) == len(cycles_in_groups): # every cycle in the list of pairs should appear in only one group
                                                                # if a cycle appears in two groups, then these groups should merge into one
        repeated = list_duplicates(cycles_in_groups)
        for rp in repeated:
            membership = [ ndx for ndx in range(len(groups)) if rp in groups[ndx] ]
            new_groups = [ groups[ndx] for ndx in range(len(groups)) if not ndx in membership ]
            ng = list(set([ c for ndx in membership for c in groups[ndx] ]))
            new_groups.append(ng)
            groups = new_groups
        cycles_in_groups = [ x for g in groups for x in g ]

    print("\nGroups of adjacent aro cycles:")
    newfile.write(f"\nGroups of adjacent aro cycles:\n")
    print(groups)
    newfile.write(str(f"{groups}\n"))
    newfile.close()
