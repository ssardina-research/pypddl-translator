(define (domain no_running_1)

  (:requirements
    :typing
  )

  (:types Cell)

  (:constants
    c0 c1 c2 - Cell
  )

  (:predicates
  	(at ?c - Cell)
  	(adj ?o - Cell ?d - Cell)
    (broken)
    (scratch)
  )

(:action walk
:parameters (?o - Cell ?d - Cell)
:precondition (and
(at ?o)
(adj ?o ?d)
(not (broken))
)
:effect (oneof

  (d3
    (and 
      (not (at ?o))
      (at ?d)
    )
  )

  (d2
    (and 
      (not (at ?o))
      (at ?d)
      (scratch)
    )
  )

  (d1
    (and 
      (scratch)
    )
  )
)
)

(:action run
:parameters ()
:precondition (and
(at c2)
(not (broken))
)
:effect (oneof

  (d3
    (and 
      (not (at c2))
      (at c0)
    )
  )

  (d2
    (and 
      (not (at c2))
      (at c0)
      (scratch)
    )
  )

  (d1
    (and 
      (broken)
    )
  )
)
)



)
