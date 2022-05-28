import argparse
import copy

from pypddl.pddlparser import PDDLParser

from pypddl.predicate import Predicate
from pypddl.term      import Term
from pypddl.literal   import Literal
from pypddl.action    import Action
from pypddl.problem import Problem

def generate_explicability_formula(d_prime_domain, current_effects, all_effects, highest_domain, hierarchy):
    formula_result = []
    positive = []
    negative = []
    # First part of the conjunction
    # Make sure that the higher (or equal) level d_prime explain the effects
    other_effects = all_effects[highest_domain.index(d_prime_domain)]
    explicability = effect_explicability(current_effects, other_effects)
    if len(explicability) > 0:
        positive.append(explicability)

    # Second part of the conjunction:
    # Make sure that no level higher than d_prime explains the effects
    d_double_prime_domains = hierarchy[0:hierarchy.index(d_prime_domain)]
    for other_level_2 in d_double_prime_domains:
        other_effects_2 = all_effects[highest_domain.index(other_level_2)]
        explicability = effect_explicability(current_effects, other_effects_2)
        if len(explicability) > 0:
            negative.append([explicability])

    # Create the formula
    for y in positive:
        formula_result += y
    if len(negative) > 0:
        for clause in negative:
            this_clause = []  # This is each not Explains statement
            for pred in clause:
                for p in pred:
                    if p.is_positive():
                        aux_pred = p.predicate
                        this_clause += [Literal(aux_pred, False)]
                    else:
                        aux_pred = p.predicate
                        this_clause += [Literal(aux_pred, True)]
            formula_result.append(this_clause)

    return formula_result


def effect_explicability(eff1, eff2):
    differences = extract_differences(eff1[0], eff2[0], [])
    differences = extract_differences(eff2[0], eff1[0], differences)

    return differences


# This method is thought to be able to handle conditional effects.
# However, by now we are only dealing with STRIPS, so only some part of the method are useful
def extract_differences(eff1, eff2, discriminants):
    # In all predicates we have:
    #   - In the keys, the predicates that appear in the effects.
    #       - If they are restricted to a conditional effect, the conditions appear in the form of a list as values of the dict
    #       - Otherwise, this list is empty, meaning that this effect does not have any particualr condition
    all_predicates = {}
    for pred in eff1:
        if isinstance(pred, tuple):
            all_predicates[pred] = []
        else:
            left = pred[0]
            right = pred[1]
            for r in right:
                if r in all_predicates:
                    if len(all_predicates[r]) == 0:
                        continue
                    else:
                        all_predicates[r].append(left)
                else:
                    all_predicates[r] = [left]

    # Here we filter those cases where a given set of effects are restricted to a particular condition,
    # which is already ensured by the other effects in the action
    aux_dict = dict(all_predicates)
    for key, value in aux_dict.items():
        if len(value) > 0:
            all = True
            for x in value:
                for y in x:
                    if y in all_predicates:
                        continue
                    else:
                        all = False
                        break
                if all:
                    all_predicates[key] = []

    # Here we compute the discriminants
    for key, value in all_predicates.items():
        # Transform the key to a proper literal
        x = key
        difference = []
        x_in_eff2 = False  # this means that it appears univocally, without condition
        # It is just a predicate
        if len(value) == 0:
            # We can break the loop at the moment that:
            #   1 - See the effect in the left part of a condition
            #   2 - See the effect in a normal predicate of the other level
            for y in eff2:
                if isinstance(y, list):
                    # The effect x is in the right part
                    if x in y[1]:
                        # And everything from the left part is present in the previous state
                        # We add all the when part
                        this_when = []
                        # more than one lement
                        if isinstance(y[0], list):
                            for p in y[0]:
                                this_when.append(p)
                        else:
                            this_when = y[0]
                        difference.append(this_when)
                else:
                    if x == y:
                        x_in_eff2 = True
                        difference = []
                        break

            # x does NOT appear univocally in the other effects
            if not x_in_eff2:
                # but it appears in the right part of a condition
                if len(difference) > 0:
                    discriminants.append([x, difference])  # We add x or difference
                else:
                    discriminants.append(x[1])

        # It is a conditional statement
        else:
            # We can break the loop at the moment that:
            #   1 - See the effect in the left part of a condition
            #   2 - See the effect in a normal predicate of the other level
            for y in eff2:
                if isinstance(y, list):
                    # The effect x is in the right part
                    if x in y[0][1]:
                        # And everything from the left part is present in the previous state
                        # We add all the when part (which will be negated)
                        this_when = []
                        for p in y[0][0]:
                            this_when.append(p)
                        difference.append(this_when)

                else:
                    if x == y:
                        x_in_eff2 = True
                        difference = []
                        break

            # x does NOT appear in the right part
            if not x_in_eff2:
                if len(difference) > 0:
                    discriminants.append([x, difference])
                else:
                    aux = value[0][1].negative(value[0][1].predicate)
                    discriminants.append([x, (1.0, aux)])

    return discriminants

# Compilation of the domain
def multi_tier_compilation_domain(domain, hierarchy, goal_statement, mtp_domain_file):
    # ..:: PREDICATES ::..
    domain.add_pred('end', [])
    domain.add_pred('act', [])
    for level in hierarchy:
        domain.add_pred('l_' + level, [])
        domain.add_pred('e_' + level, [])
        for a in domain.operators:
            domain.add_pred('eff_' + level + '_' + a.name, [])
    for o in domain.operators:
        domain.add_pred('u_' + o.name, [])

    # ..:: ACTIONS ::..
    original_domain_operators = list(domain.operators)
    # We clean the original actions
    domain.operators = []

    # For each domain level, we have one *CONTINUE* action that checks whether the seen effects are aligned
    # with the current domain level
    for level in hierarchy:
        # *Preconditions*
        # 1. act predicate negated
        # 2. higher level that explains the observed effects (e_Dx)
        # 3. current domain model (l_Dx)
        # 4.  We force the negation of all the predicates used for the compilation of conditional effects
        #     to ensure that the alignment actions only occur after the actions replacing CE take place
        new_preconditions = [Literal(Predicate('act', []), False)] + \
                            [Literal(Predicate('l_' + level, []), True)]
        for y in hierarchy:
            for aname in original_domain_operators:
                new_preconditions += [Literal(Predicate('eff_' + y + '_' + aname.name, []),
                                              False)]
        possible_e = []
        for x in range(0, hierarchy.index(level) + 1):
            possible_e += [Literal(Predicate('e_' + hierarchy[x], []), True)]
        new_preconditions.append(possible_e)

        # *Effects*
        # 1. act predicate set to true
        # 2. reset all e_D variables
        new_effects = [(1.0, Literal(Predicate('act', []), True))]
        for x in hierarchy:
            new_effects += [(1.0, Literal(Predicate('e_' + x, []), False))]

        # *Add the action to the domain*
        domain.add_action('continue_' + level, [], new_preconditions, [new_effects])

    # For each pair of domain levels (always in decreasing order, we only accept degradation), we have one
    # *DEGRADE* action that checks the observed affects and degrades to the proper level
    for lev1 in hierarchy:
        for lev2 in hierarchy:
            name1 = '_'.join(lev1.split('_')[:-1])
            name2 = '_'.join(lev2.split('_')[:-1])
            index1 = hierarchy.index(lev1)
            index2 = hierarchy.index(lev2)
            if (index1 < index2) and ((name1 != name2) or (name1 == name2 == '')):  # To check the lattice structure
                # *Preconditions*
                # 1. act predicate negated
                # 2. higher level that explains the observed effects (e_Dy)
                # 3. current domain model (l_Dx)
                # 4.  We force the negation of all the predicates used for the compilation of conditional effects
                #     to ensure that the alignment actions only occur after the actions replacing CE take place
                new_preconditions = [Literal(Predicate('act', []), False)] + \
                                    [Literal(Predicate('l_' + lev1, []), True)] + \
                                    [Literal(Predicate('e_' + lev2, []), True)]
                for y in hierarchy:
                    for aname in original_domain_operators:
                        new_preconditions += [Literal(Predicate('eff_' + y + '_' + aname.name, []),
                                                      False)]

                # *Effects*
                # 1. act predicate set to true
                # 2. reset all e_D variables
                # 3. set to false l_Dx and set to true l_Dy
                new_effects = [(1.0, Literal(Predicate('act', []), True))] + \
                              [(1.0, Literal(Predicate('l_' + lev2, []), True))] + \
                              [(1.0, Literal(Predicate('l_' + lev1, []), False))]
                for x in hierarchy:
                    new_effects += [(1.0, Literal(Predicate('e_' + x, []), False))]

                # *Add the action to the domain*
                domain.add_action('degrade_' + lev1 + '_' + lev2, [], new_preconditions, [new_effects])

    # We generate the fair and unfair actions
    for action in original_domain_operators:
        # First of all we have to check the number of different effects that can appear with this action
        different_effects = []  # effects i
        higher_domain_effects = []  # higher domain where effect i appears
        for domain_effects in action.effects:
            dom = domain_effects[0]
            effects = domain_effects[1]
            if effects not in different_effects:
                different_effects.append(effects)
                higher_domain_effects.append(dom)

        # *UNFAIR ACTION* that contemplates all the possible effects
        # We compile away the conditional effects by replacing them with eff_Dx_action predicates
        # *Preconditions*
        # 1. act predicate
        # 2. action's unfair predicate
        new_preconditions = [Literal(Predicate('act', []), True)] + \
                            [Literal(Predicate('u_' + action.name, []), True)]

        # *Effects*
        # Oneof containing, for each domain level:
        # 1. Eff_Dx_action predicate to handle the conditional effects
        # 2. Negation of unfair predicate corresponding to the action
        final_effects = []
        for e, d in zip(different_effects, higher_domain_effects):
            new_effects = [(1.0, Literal(Predicate('eff_' + d + '_' + action.name, []), True))] + \
                          [(1.0, Literal(Predicate('act', []), False))]
            final_effects.append(new_effects)
        domain.add_action(action.name + '_unfair_', [], new_preconditions,
                          final_effects)

        # For each action in the domain, and each domain level, we have an *ACTION_LEVEL_FAIR* action.
        # It represents the set of fair effects from a given domain level
        current_levels = []
        for lev in hierarchy:
            current_levels.append(lev)

            # *Preconditions*:
            # 1. Current level
            # 2. act predicate
            # 3. Previous preconditions
            # 4. Negation of the unfair predicates
            new_preconditions = action.precond + \
                                [Literal(Predicate('l_' + current_levels[-1], []), True)] + \
                                [Literal(Predicate('act', []), True)]
            for c in original_domain_operators:
                new_preconditions += [Literal(Predicate('u_' + c.name, []), False)]

            # *Effects*
            # 1. Negated act predicate
            # 2. Subset of all the oneof effects, depending on the level we are in
            # 3. Unfair predicate for the lower levels
            new_effects = []
            for domain_l in action.effects:
                level = domain_l[0]
                effects = []
                if level in current_levels:
                    for h in domain_l[1]:
                        for x in h:
                            if isinstance(x, tuple):
                                effects.append(x)
                        new_effects += [effects]
                else:
                    # Unfair part of the action
                    effects = [(1.0, Literal(Predicate('u_' + action.name, []), True))]
                    new_effects += [effects]
                    break

            # We add the action without conditional effects
            domain.add_action(action.name + '_' + lev, action.params,
                              new_preconditions, new_effects)

        # This part creates the actions that make the system only degrade when *really* needed
        # As a result of the compilation of conditional effects
        for e, d in zip(different_effects, higher_domain_effects):
            # lev1 = hierarchy.index(d)
            for d_prime in hierarchy:
                name1 = '_'.join(d.split('_')[:-1])
                name2 = '_'.join(d_prime.split('_')[:-1])
                index1 = hierarchy.index(d)
                index2 = hierarchy.index(d_prime)
                if (index1 >= index2) and (
                        (name1 != name2) or (name1 == name2 == '')):  # To check the lattice structure
                    precond = list(action.precond)
                    precond += [Literal(Predicate('eff_' + d + '_' + action.name, []), True)]
                    aux = generate_explicability_formula(d_prime, e, different_effects, higher_domain_effects,
                                                         hierarchy)
                    for x in aux:
                        precond += [x]
                    eff = []
                    for effec in list(action.effects[hierarchy.index(d)][1][0]):
                        eff.append(effec)
                    #eff = list(action.effects[hierarchy.index(d)][1])
                    eff += ([(1.0, Literal(Predicate('e_' + d_prime, []), True))])
                    eff += [(1.0, Literal(Predicate('eff_' + d + '_' + action.name, []), False))]
                    eff += [(1.0, Literal(Predicate('act', []), False))]
                    eff += [(1.0, Literal(Predicate('u_' + action.name, []), False))]
                    domain.add_action(action.name + '_eff_' + d + '_explained_by_' + d_prime,
                                      action.params, precond, [eff])

    # For each goal statement in the problem, we will have a *CHECK_GOAL* action that checks that a given goal
    # is achieved when being at a certain domain level
    for goal in goal_statement:
        domain_level = goal[0]
        goal_predicates = goal[1]
        # The preconditions will be formed by the goal statement and the proper level
        new_preconditions = []
        or_statement = False
        for p in goal_predicates:
            # If the goal statement for this level does not have an or
            if isinstance(p, tuple):
                new_preconditions += [p[1]]
            # Otherwise, we have to create as many check_goal actions as parts of the or
            else:
                new_preconditions = []
                or_statement = True
                for pred in p:
                    new_preconditions += [pred[1]]
                new_preconditions += [Literal(Predicate('l_' + str(domain_level), []), True)]

                new_preconditions += [Literal(Predicate('act', []), True)]

                new_effects = [(1.0, Literal(Predicate('end', []), True))]

                domain.add_action('check_goal_' + domain_level, [],
                                  new_preconditions,
                                  [new_effects])

        if not or_statement:
            new_preconditions += [Literal(Predicate('l_' + str(domain_level), []), True)]

            new_preconditions += [Literal(Predicate('act', []), True)]

            new_effects = [(1.0, Literal(Predicate('end', []), True))]

            domain.add_action('check_goal_' + domain_level, [], new_preconditions, [new_effects])

    # Write the domain
    with open(mtp_domain_file, 'w') as f:
        print(repr(domain), file=f)


# Compilation of the problem
def multi_tier_compilation_problem(problem,mtp_problem_file):
    # Get the list/hierarchy of domains
    # Here we assume:
    #   - Each domain has an associated goal
    #   - This relationship is ordered in the problem file
    #   - Lattice structures are denoted by '_'
    domains = []
    for d in problem.goal:
        domain = d[0]
        domains.append(domain)

    # Update the initial state
    problem.init.append(Predicate('act'))  # act predicate
    problem.init.append(Predicate('l_' + (str(domains[0]))))  # initial domain level (top model in the hierarchy)

    # Update the goal
    original_goal = list(problem.goal)
    problem.goal = [Predicate('end')]  # new goal condition

    # Write the problem
    with open(mtp_problem_file, 'w') as f:
        print(repr(problem), file=f)

    # Return the list/hierarchy of domain models
    return domains, original_goal

