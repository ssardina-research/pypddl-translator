(define (problem p1)
	(:domain no_running_1)
	(:init
		(at c2)
		(adj c2 c1)
		(adj c1 c0)
		(adj c0 c1)
		(adj c1 c2)
		(act)
		(l_d3))
	(:goal (and 
		(end)))
)
