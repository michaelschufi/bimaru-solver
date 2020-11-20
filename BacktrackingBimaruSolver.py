import constraint as csp

class BacktrackingBimaruSolver(csp.Solver):
    """
    Bimaru solver with backtracking capabilities
    Examples:
    >>> result = [[('a', 1), ('b', 2)],
    ...           [('a', 1), ('b', 3)],
    ...           [('a', 2), ('b', 3)]]
    >>> problem = Problem(BacktrackingSolver())
    >>> problem.addVariables(["a", "b"], [1, 2, 3])
    >>> problem.addConstraint(lambda a, b: b > a, ["a", "b"])
    >>> solution = problem.getSolution()
    >>> sorted(solution.items()) in result
    True
    >>> for solution in problem.getSolutionIter():
    ...     sorted(solution.items()) in result
    True
    True
    True
    >>> for solution in problem.getSolutions():
    ...     sorted(solution.items()) in result
    True
    True
    True
    """

    def __init__(self, neighbourLookupTable, forwardcheck=True):
        """
        @param forwardcheck: If false forward checking will not be requested
                             to constraints while looking for solutions
                             (default is true)
        @type  forwardcheck: bool
        """

        self._forwardcheck = forwardcheck
        self._neighbourLookupTable = neighbourLookupTable
    
    def isNeighbourOfAssignedVar(self, variable, assignedVariables):
        for neighbour in self._neighbourLookupTable[variable]:
            if neighbour in assignedVariables:
                return 0
        return 1
        
    def getSolutionIter(self, domains, constraints, vconstraints):
        forwardcheck = self._forwardcheck
        assignments = {}

        queue = []

        while True:
            assignedVariables = []
            for var, value in assignments.items():
                if value != 7:
                    assignedVariables.append(var)

            lst = [
                (
                    # Minimum Remaing Values (MRV)
                    len(domains[variable]),

                    # 8-Neighbours
                    self.isNeighbourOfAssignedVar(variable, assignedVariables),

                    # Degree heuristic
                    -len(vconstraints[variable]),

                    # Actual variable
                    variable,
                )
                for variable in domains
            ]
            lst.sort()
            for item in lst:
                if item[-1] not in assignments:
                    # Found unassigned variable
                    variable = item[-1]
                    values = domains[variable][:]
                    if forwardcheck:
                        pushdomains = [
                            domains[x]
                            for x in domains
                            if x not in assignments and x != variable
                        ]
                    else:
                        pushdomains = None
                    break
            else:
                # No unassigned variables. We've got a solution. Go back
                # to last variable, if there's one.
                yield assignments.copy()
                if not queue:
                    return
                variable, values, pushdomains = queue.pop()
                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            while True:
                # We have a variable. Do we have any values left?
                if not values:
                    # No. Go back to last variable, if there's one.
                    del assignments[variable]
                    while queue:
                        variable, values, pushdomains = queue.pop()
                        if pushdomains:
                            for domain in pushdomains:
                                domain.popState()
                        if values:
                            break
                        del assignments[variable]
                    else:
                        return

                # Got a value. Check it.
                assignments[variable] = values.pop()

                if pushdomains:
                    for domain in pushdomains:
                        domain.pushState()

                for constraint, variables in vconstraints[variable]:
                    if not constraint(variables, domains, assignments, pushdomains):
                        # Value is not good.
                        break
                else:
                    break

                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            # Push state before looking for next variable.
            queue.append((variable, values, pushdomains))

        raise RuntimeError("Can't happen")

    def getSolution(self, domains, constraints, vconstraints):
        iter = self.getSolutionIter(domains, constraints, vconstraints)
        try:
            return next(iter)
        except StopIteration:
            return None

    def getSolutions(self, domains, constraints, vconstraints):
        return list(self.getSolutionIter(domains, constraints, vconstraints))
