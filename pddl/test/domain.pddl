;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
( define ( domain blocks )
	( :requirements :strips :typing :equality )
	( :types block )
	( :predicates
		( on ?x - block ?y - block )
		( ontable ?x - block )
		( clear ?x - block )
		( handempty )
		( holding ?x - block )
	)
	( :action pick-up1
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (ontable ?x )
	)

	( :action pick-up2
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (not (ontable ?x ))
	)

	( :action pick-up3
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (and (handempty) (not (ontable ?x )))
	)

	( :action pick-up4
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (oneof (handempty) (not (ontable ?x )))
	)

	( :action pick-up5
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (oneof 
					( and
						( not ( ontable ?x ) )
						( not ( clear ?x ) )
						( not ( handempty ) )
						( holding ?x ) )
					( ontable ?x )
					(and (handempty) ( ontable ?x ))
				)
	)

	( :action pick-up6
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (oneof 
					( and
						( not ( ontable ?x ) )
						( not ( clear ?x ) )
						( not ( handempty ) )
						( holding ?x ) )
					( ontable ?x )
					(oneof (handempty) ( clear ?x ) (and (handempty) ( ontable ?x )))
				)
	)

	( :action pick-up7
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (oneof
					(d1 ( and
						( not ( ontable ?x ) )
						( not ( clear ?x ) )
						( not ( handempty ) )
						( holding ?x ) ))
					(d2 ( ontable ?x ))
					(oneof (handempty) ( clear ?x ) (and (handempty) ( ontable ?x )))
				)
	)
	( :action pick-up8
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (when (handempty) (not (ontable ?x )))
	)

	( :action pick-up9
		:parameters ( ?x - block )
		:precondition ( and
			( clear ?x )
			( ontable ?x )
			( handempty )
		)
		:effect (oneof
					( and
						( not ( ontable ?x ) )
						( not ( clear ?x ) )
						( not ( handempty ) )
						( holding ?x ) )
					(d2 (when (and (handempty) (clear ?c)) ( ontable ?x )))
					(oneof (handempty) ( clear ?x ) (and (handempty) ( ontable ?x )))
				)
	)
)
