(define (problem p1)
    (:domain no_running_1)
    (:init
        (at c2)
        (adj c2 c1)
        (adj c1 c0)
        (adj c0 c1)
        (adj c1 c2)
    )
    (:goal
        (oneof    ; goals at different levels
            (d3   
                (and (at c0) (not (scratch)) (not (broken))))
            (d2
                (and (at c0) (not (broken))))
            (d1
                (and (at c2) (not (broken))))
        )
    )
)