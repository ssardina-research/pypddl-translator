from distutils.command import clean
import unittest

import re

from pypddl.pddlparser import PDDLParser
from pypddl.mtp import multi_tier_compilation_domain, multi_tier_compilation_problem
from pypddl.problem import Problem

# Check if the MTP compilation is correct
class TestMtpCompilation(unittest.TestCase):

    def test_mtp_problem(self):
        expected = '(define (problem p1)(:domain no_running_1)(:init(at c2)(adj c2 c1)(adj c1 c0)(adj c0 c1)(adj c1 c2)(act)(l_d3))(:goal (and (end))))'
        problem = PDDLParser.parse('pddl/mtp-example/labeled-problem.pddl')
        multi_tier_compilation_problem(problem, 'pddl/mtp-example/mtp-problem.pddl')
        
        with open('pddl/mtp-example/mtp-problem.pddl', 'r') as infile:
            aux = infile.read().strip().replace('\n','').replace('\t','')
        infile.close()
        new_problem_string = ''.join(aux)
        self.assertEqual(expected,new_problem_string,"Should be equal")

    def test_mtp_domain(self):
        expected = '(define (domain no_running_1)(:requirements :typing)(:types  cell)(:constants c0 c1 c2 - cell)(:predicates(at ?c - cell)(adj ?o - cell ?d - cell)(broken)(scratch)(end)(act)(l_d3)(e_d3)(eff_d3_walk)(eff_d3_run)(l_d2)(e_d2)(eff_d2_walk)(eff_d2_run)(l_d1)(e_d1)(eff_d1_walk)(eff_d1_run)(u_walk)(u_run))(:action continue_d3 :parameters ():precondition (and  (not (act)) (l_d3) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3))):effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action continue_d2 :parameters ():precondition (and  (not (act)) (l_d2) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3) (e_d2))):effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action continue_d1 :parameters ():precondition (and  (not (act)) (l_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3) (e_d2) (e_d1))):effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action degrade_d3_d2 :parameters ():precondition (and  (not (act)) (l_d3) (e_d2) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run))):effect (and (act) (l_d2) (not (l_d3)) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action degrade_d3_d1 :parameters ():precondition (and  (not (act)) (l_d3) (e_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run))):effect (and (act) (l_d1) (not (l_d3)) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action degrade_d2_d1 :parameters ():precondition (and  (not (act)) (l_d2) (e_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run))):effect (and (act) (l_d1) (not (l_d2)) (not (e_d3)) (not (e_d2)) (not (e_d1))))(:action walk_unfair_ :parameters ():precondition (and  (act) (u_walk)):effect (oneof (and (eff_d3_walk) (not (act))) (and (eff_d2_walk) (not (act))) (and (eff_d1_walk) (not (act)))))(:action walk_d3 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (l_d3) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at ?o)) (at ?d)) (u_walk)))(:action walk_d2 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (l_d2) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at ?o)) (at ?d)) (and (not (at ?o)) (at ?d) (scratch)) (u_walk)))(:action walk_d1 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (l_d1) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at ?o)) (at ?d)) (and (not (at ?o)) (at ?d) (scratch)) (scratch)))(:action walk_eff_d3_explained_by_d3 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d3_walk)):effect (and (not (at ?o)) (at ?d) (e_d3) (not (eff_d3_walk)) (not (act)) (not (u_walk))))(:action walk_eff_d2_explained_by_d3 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d2_walk) (scratch)):effect (and (not (at ?o)) (at ?d) (scratch) (e_d3) (not (eff_d2_walk)) (not (act)) (not (u_walk))))(:action walk_eff_d2_explained_by_d2 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d2_walk) (or (not (scratch)))):effect (and (not (at ?o)) (at ?d) (scratch) (e_d2) (not (eff_d2_walk)) (not (act)) (not (u_walk))))(:action walk_eff_d1_explained_by_d3 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (scratch) (not (at ?o)) (at ?d)):effect (and (scratch) (e_d3) (not (eff_d1_walk)) (not (act)) (not (u_walk))))(:action walk_eff_d1_explained_by_d2 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (not (at ?o)) (at ?d) (or (not (scratch)) (at ?o) (not (at ?d)))):effect (and (scratch) (e_d2) (not (eff_d1_walk)) (not (act)) (not (u_walk))))(:action walk_eff_d1_explained_by_d1 :parameters (?o - cell ?d - cell):precondition (and  (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (or (not (scratch)) (at ?o) (not (at ?d))) (or (at ?o) (not (at ?d)))):effect (and (scratch) (e_d1) (not (eff_d1_walk)) (not (act)) (not (u_walk))))(:action run_unfair_ :parameters ():precondition (and  (act) (u_run)):effect (oneof (and (eff_d3_run) (not (act))) (and (eff_d2_run) (not (act))) (and (eff_d1_run) (not (act)))))(:action run_d3 :parameters ():precondition (and  (at c2) (not (broken)) (l_d3) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at c2)) (at c0)) (u_run)))(:action run_d2 :parameters ():precondition (and  (at c2) (not (broken)) (l_d2) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at c2)) (at c0)) (and (not (at c2)) (at c0) (scratch)) (u_run)))(:action run_d1 :parameters ():precondition (and  (at c2) (not (broken)) (l_d1) (act) (not (u_walk)) (not (u_run))):effect (oneof (and (not (at c2)) (at c0)) (and (not (at c2)) (at c0) (scratch)) (broken)))(:action run_eff_d3_explained_by_d3 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d3_run)):effect (and (not (at c2)) (at c0) (e_d3) (not (eff_d3_run)) (not (act)) (not (u_run))))(:action run_eff_d2_explained_by_d3 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d2_run) (scratch)):effect (and (not (at c2)) (at c0) (scratch) (e_d3) (not (eff_d2_run)) (not (act)) (not (u_run))))(:action run_eff_d2_explained_by_d2 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d2_run) (or (not (scratch)))):effect (and (not (at c2)) (at c0) (scratch) (e_d2) (not (eff_d2_run)) (not (act)) (not (u_run))))(:action run_eff_d1_explained_by_d3 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d1_run) (broken) (not (at c2)) (at c0)):effect (and (broken) (e_d3) (not (eff_d1_run)) (not (act)) (not (u_run))))(:action run_eff_d1_explained_by_d2 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d1_run) (broken) (not (at c2)) (at c0) (scratch) (or (not (broken)) (at c2) (not (at c0)))):effect (and (broken) (e_d2) (not (eff_d1_run)) (not (act)) (not (u_run))))(:action run_eff_d1_explained_by_d1 :parameters ():precondition (and  (at c2) (not (broken)) (eff_d1_run) (or (not (broken)) (at c2) (not (at c0))) (or (not (broken)) (at c2) (not (at c0)) (not (scratch)))):effect (and (broken) (e_d1) (not (eff_d1_run)) (not (act)) (not (u_run))))(:action check_goal_d3 :parameters ():precondition (and  (at c0) (not (scratch)) (not (broken)) (l_d3) (act)):effect (end))(:action check_goal_d2 :parameters ():precondition (and  (at c0) (not (broken)) (l_d2) (act)):effect (end))(:action check_goal_d1 :parameters ():precondition (and  (at c2) (not (broken)) (l_d1) (act)):effect (end)))'
        
        domain = PDDLParser.parse('pddl/mtp-example/labeled-domain.pddl')
        problem = PDDLParser.parse('pddl/mtp-example/labeled-problem.pddl')
        
        # encode MTP problem and save it to file pddl/mtp-example/mtp-problem.pddl
        domain_models_hierarchy, goal_statement = multi_tier_compilation_problem(problem,
                                                                                 'pddl/mtp-example/mtp-problem.pddl')
        
        # encode MTP domain and save it to file pddl/mtp-example/mtp-problem.pddl
        multi_tier_compilation_domain(domain, domain_models_hierarchy, goal_statement,
                                      'pddl/mtp-example/mtp-domain.pddl')
        
        with open('pddl/mtp-example/mtp-domain.pddl', 'r') as infile:
            aux = infile.read().strip().replace('\n', '').replace('\t', '')
        infile.close()
        new_domain_string = ''.join(aux)
        self.assertEqual(expected, new_domain_string, "Should be equal")

# Check if the printing, and hence the grammar, is correct
class TestPrint(unittest.TestCase):

    def test_print_domain_strips(self):
        expected = """(define (domain blocks)
            (:requirements :strips :typing :equality)
            (:types 
                block
            )
            (:predicates
                (on ?x - block ?y - block)
                (ontable ?x - block)
                (clear ?x - block)
                (handempty)
                (holding ?x - block)
            )
            (:action pick-up 
                :parameters (?x - block)
                :precondition (and  (clear ?x) (ontable ?x) (handempty))
                :effect (and (not (ontable ?x)) (not (clear ?x)) (not (handempty)) (holding ?x))
            )
            (:action put-down 
                :parameters (?x - block)
                :precondition (and  (holding ?x))
                :effect (and (not (holding ?x)) (clear ?x) (handempty) (ontable ?x))
            )
            (:action stack 
                :parameters (?x - block ?y - block)
                :precondition (and  (not (= ?x ?y)) (holding ?x) (clear ?y))
                :effect (and (not (holding ?x)) (not (clear ?y)) (clear ?x) (handempty) (on ?x ?y))
            )
            (:action unstack 
                :parameters (?x - block ?y - block)
                :precondition (and  (not (= ?x ?y)) (on ?x ?y) (clear ?x) (handempty))
                :effect (and (holding ?x) (clear ?y) (not (clear ?x)) (not (handempty)) (not (on ?x ?y)))
            )
        )
        """
        domain = PDDLParser.parse('pddl/blocksworld/domain.pddl')
        
        new_domain_string = repr(domain)
        self.assertEqual(clean_up_str(expected), clean_up_str(new_domain_string))

    def test_print_problem_strips(self):
        test_problem_string = '(define (problem blocks-4-0)\n\t(:domain blocks)\n\t(:objects d b a c - block)\n\t(:init\n\t\t(clear c)\n\t\t(clear a)\n\t\t(clear b)\n\t\t(clear d)\n\t\t(ontable c)\n\t\t(ontable a)\n\t\t(ontable b)\n\t\t(ontable d)\n\t\t(handempty))\n\t(:goal (and \n\t\t(on d c)\n\t\t(on c b)\n\t\t(on b a)))\n)'
        problem = PDDLParser.parse('pddl/blocksworld/problems/probBLOCKS-04-0.pddl')
        new_domain_string = repr(problem)
        self.assertEqual(test_problem_string,new_domain_string)

    def test_print_domain_probabilistic(self):
        test_domain_string = '(define (domain triangle-tire)\n\t(:requirements :typing :strips :probabilistic-effects)\n\t(:types \n\t\t location\n\t)\n\t(:predicates\n\t\t(road ?from - location ?to - location)\n\t\t(spare-in ?loc - location)\n\t\t(vehicle-at ?loc - location)\n\t\t(not-flattire)\n\t\t(hasspare)\n\t)\n\t(:action move-car \n\t\t:parameters (?from - location ?to - location)\n\t\t:precondition (and  (vehicle-at ?from) (road ?from ?to) (not-flattire))\n\t\t:effect (and (vehicle-at ?to) (not (vehicle-at ?from)) (not (not-flattire)))\n\t)\n\t(:action load-tire \n\t\t:parameters (?loc - location)\n\t\t:precondition (and  (vehicle-at ?loc) (spare-in ?loc))\n\t\t:effect (and (hasspare) (not (spare-in ?loc)))\n\t)\n\t(:action change-tire \n\t\t:parameters ()\n\t\t:precondition (and  (hasspare))\n\t\t:effect (and (not (hasspare)) (not-flattire))\n\t)\n)'
        domain = PDDLParser.parse('pddl/triangle-tireworld/domain.ppddl')
        new_domain_string = repr(domain)
        self.assertEqual(test_domain_string,new_domain_string)

    def test_print_problem_probabilistic(self):
        test_problem_string = '(define (problem tireworld-01)\n\t(:domain triangle-tire)\n\t(:objects x01y05 x02y04 x01y03 x03y03 x02y02 x01y01 - location)\n\t(:init\n\t\t(road x01y01 x01y03)\n\t\t(road x01y01 x02y02)\n\t\t(road x01y03 x01y05)\n\t\t(road x01y03 x02y04)\n\t\t(road x02y02 x01y03)\n\t\t(road x02y02 x03y03)\n\t\t(road x02y04 x01y05)\n\t\t(road x03y03 x02y04)\n\t\t(spare-in x02y02)\n\t\t(spare-in x02y04)\n\t\t(spare-in x03y03)\n\t\t(vehicle-at x01y01)\n\t\t(not-flattire)\n\t\t(hasspare))\n\t(:goal (and \n\t\t(vehicle-at x01y05)))\n)'
        problem = PDDLParser.parse('pddl/triangle-tireworld/problems/p01.ppddl')
        new_problem_string = repr(problem)
        self.assertEqual(test_problem_string,new_problem_string)

    def test_print_domain_labeled(self):
        expected = """(define (domain no_running_1)
            (:requirements :typing)
            (:types 
                cell
            )
            (:constants 
                c0 c1 c2 - cell
            )
            (:predicates
                (at ?c - cell)
                (adj ?o - cell ?d - cell)
                (broken)
                (scratch)
            )
            (:action walk 
                :parameters (?o - cell ?d - cell)
                :precondition (and  (at ?o) (adj ?o ?d) (not (broken)))
                :effect (oneof (d3 (and (not (at ?o)) (at ?d))) (d2 (and (not (at ?o)) (at ?d) (scratch))) (d1 (scratch)))
            )
            (:action run 
                :parameters ()
                :precondition (and  (at c2) (not (broken)))
                :effect (oneof (d3 (and (not (at c2)) (at c0))) (d2 (and (not (at c2)) (at c0) (scratch))) (d1 (broken)))
            )
            )
        """
        
        domain = PDDLParser.parse('pddl/mtp-example/labeled-domain.pddl')
        new_domain_string = repr(domain)
        
        
        self.assertEqual(clean_up_str(expected), clean_up_str(new_domain_string))

    def test_print_problem_labeled(self):
        test_problem_string = '(define (problem p1)\n\t(:domain no_running_1)\n\t(:init\n\t\t(at c2)\n\t\t(adj c2 c1)\n\t\t(adj c1 c0)\n\t\t(adj c0 c1)\n\t\t(adj c1 c2))\n\t(:goal (and \n\t\t(d3 (and (at c0) (not (scratch)) (not (broken))))\n\t\t(d2 (and (at c0) (not (broken))))\n\t\t(d1 (and (at c2) (not (broken))))\n\t\t))\n)'
        problem = PDDLParser.parse('pddl/mtp-example/labeled-problem.pddl')
        new_problem_string = repr(problem)
        
        self.assertEqual(test_problem_string,new_problem_string)

    def test_print_domain_oneof_or(self):
        expected = '''(define (domain no_running_1)
            (:requirements :typing)
            (:types
                cell
            )
            (:constants
                c0 c1 c2 - cell
            )
            (:predicates
                (at ?c - cell)
                (adj ?o - cell ?d - cell)
                (broken)
                (scratch)
                (end)
                (act)
                (l_d3)
                (e_d3)
                (eff_d3_walk)
                (eff_d3_run)
                (l_d2)
                (e_d2)
                (eff_d2_walk)
                (eff_d2_run)
                (l_d1)
                (e_d1)
                (eff_d1_walk)
                (eff_d1_run)
                (u_walk)
                (u_run)
            )
            (:action continue_d3
                :parameters ()
                :precondition (and (not (act)) (l_d3) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3)))
                :effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action continue_d2
                :parameters ()
                :precondition (and (not (act)) (l_d2) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3) (e_d2)))
                :effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action continue_d1
                :parameters ()
                :precondition (and (not (act)) (l_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)) (or (e_d3) (e_d2) (e_d1)))
                :effect (and (act) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action degrade_d3_d2
                :parameters ()
                :precondition (and (not (act)) (l_d3) (e_d2) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)))
                :effect (and (act) (l_d2) (not (l_d3)) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action degrade_d3_d1
                :parameters ()
                :precondition (and (not (act)) (l_d3) (e_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)))
                :effect (and (act) (l_d1) (not (l_d3)) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action degrade_d2_d1
                :parameters ()
                :precondition (and (not (act)) (l_d2) (e_d1) (not (eff_d3_walk)) (not (eff_d3_run)) (not (eff_d2_walk)) (not (eff_d2_run)) (not (eff_d1_walk)) (not (eff_d1_run)))
                :effect (and (act) (l_d1) (not (l_d2)) (not (e_d3)) (not (e_d2)) (not (e_d1)))
            )
            (:action walk_unfair_
                :parameters ()
                :precondition (and (act) (u_walk))
                :effect (oneof
                    (and (eff_d3_walk) (not (act)))
                    (and (eff_d2_walk) (not (act)))
                    (and (eff_d1_walk) (not (act))))
            )
            (:action walk_d3
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (l_d3) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at ?o)) (at ?d))
                    (u_walk))
            )
            (:action walk_d2
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (l_d2) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at ?o)) (at ?d))
                    (and (not (at ?o)) (at ?d) (scratch))
                    (u_walk))
            )
            (:action walk_d1
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (l_d1) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at ?o)) (at ?d))
                    (and (not (at ?o)) (at ?d) (scratch))
                    (scratch))
            )
            (:action walk_eff_d3_explained_by_d3
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d3_walk))
                :effect (and (not (at ?o)) (at ?d) (e_d3) (not (eff_d3_walk)) (not (act)) (not (u_walk)))
            )
            (:action walk_eff_d2_explained_by_d3
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d2_walk) (scratch))
                :effect (and (not (at ?o)) (at ?d) (scratch) (e_d3) (not (eff_d2_walk)) (not (act)) (not (u_walk)))
            )
            (:action walk_eff_d2_explained_by_d2
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d2_walk) (or (not (scratch))))
                :effect (and (not (at ?o)) (at ?d) (scratch) (e_d2) (not (eff_d2_walk)) (not (act)) (not (u_walk)))
            )
            (:action walk_eff_d1_explained_by_d3
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (scratch) (not (at ?o)) (at ?d))
                :effect (and (scratch) (e_d3) (not (eff_d1_walk)) (not (act)) (not (u_walk)))
            )
            (:action walk_eff_d1_explained_by_d2
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (not (at ?o)) (at ?d) (or (not (scratch)) (at ?o) (not (at ?d))))
                :effect (and (scratch) (e_d2) (not (eff_d1_walk)) (not (act)) (not (u_walk)))
            )
            (:action walk_eff_d1_explained_by_d1
                :parameters (?o - cell ?d - cell)
                :precondition (and (at ?o) (adj ?o ?d) (not (broken)) (eff_d1_walk) (or (not (scratch)) (at ?o) (not (at ?d))) (or (at ?o) (not (at ?d))))
                :effect (and (scratch) (e_d1) (not (eff_d1_walk)) (not (act)) (not (u_walk)))
            )
            (:action run_unfair_
                :parameters ()
                :precondition (and (act) (u_run))
                :effect (oneof
                    (and (eff_d3_run) (not (act)))
                    (and (eff_d2_run) (not (act)))
                    (and (eff_d1_run) (not (act))))
            )
            (:action run_d3
                :parameters ()
                :precondition (and (at c2) (not (broken)) (l_d3) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at c2)) (at c0))
                    (u_run))
            )
            (:action run_d2
                :parameters ()
                :precondition (and (at c2) (not (broken)) (l_d2) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at c2)) (at c0))
                    (and (not (at c2)) (at c0) (scratch))
                    (u_run))
            )
            (:action run_d1
                :parameters ()
                :precondition (and (at c2) (not (broken)) (l_d1) (act) (not (u_walk)) (not (u_run)))
                :effect (oneof
                    (and (not (at c2)) (at c0))
                    (and (not (at c2)) (at c0) (scratch))
                    (broken))
            )
            (:action run_eff_d3_explained_by_d3
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d3_run))
                :effect (and (not (at c2)) (at c0) (e_d3) (not (eff_d3_run)) (not (act)) (not (u_run)))
            )
            (:action run_eff_d2_explained_by_d3
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d2_run) (scratch))
                :effect (and (not (at c2)) (at c0) (scratch) (e_d3) (not (eff_d2_run)) (not (act)) (not (u_run)))
            )
            (:action run_eff_d2_explained_by_d2
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d2_run) (or (not (scratch))))
                :effect (and (not (at c2)) (at c0) (scratch) (e_d2) (not (eff_d2_run)) (not (act)) (not (u_run)))
            )
            (:action run_eff_d1_explained_by_d3
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d1_run) (broken) (not (at c2)) (at c0))
                :effect (and (broken) (e_d3) (not (eff_d1_run)) (not (act)) (not (u_run)))
            )
            (:action run_eff_d1_explained_by_d2
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d1_run) (broken) (not (at c2)) (at c0) (scratch) (or (not (broken)) (at c2) (not (at c0))))
                :effect (and (broken) (e_d2) (not (eff_d1_run)) (not (act)) (not (u_run)))
            )
            (:action run_eff_d1_explained_by_d1
                :parameters ()
                :precondition (and (at c2) (not (broken)) (eff_d1_run) (or (not (broken)) (at c2) (not (at c0))) (or (not (broken)) (at c2) (not (at c0)) (not (scratch))))
                :effect (and (broken) (e_d1) (not (eff_d1_run)) (not (act)) (not (u_run)))
            )
            (:action check_goal_d3
                :parameters ()
                :precondition (and (at c0) (not (scratch)) (not (broken)) (l_d3) (act))
                :effect (end)
            )
            (:action check_goal_d2
                :parameters ()
                :precondition (and (at c0) (not (broken)) (l_d2) (act))
                :effect (end)
            )
            (:action check_goal_d1
                :parameters ()
                :precondition (and (at c2) (not (broken)) (l_d1) (act))
                :effect (end)
            )
        )
        '''
   
        domain = PDDLParser.parse('pddl/mtp-example/mtp-domain.pddl')
        new_domain_string = repr(domain)
        
        expected = clean_up_str(expected)
        new_domain_string = clean_up_str(new_domain_string) 
        self.assertEqual(expected,new_domain_string)

    # def test_print_domain_conditional_effects(self):
    #     test_domain_string = '(define (domain ce)\n\t(:requirements :strips :typing :equality)\n\t(:predicates\n\t\t(p)\n\t\t(q)\n\t\t(r)\n\t\t(s)\n\t)\n\t(:action ce1 \n\t\t:parameters ()\n\t\t:precondition (and  (p))\n\t\t:effect (and (not (p)) (when (and (q))(and (s)))\n\t)\n)'
    #     domain = PDDLParser.parse('pddl/conditional_effects/domain.pddl')
    #     new_domain_string = repr(domain)
    #     self.assertEqual(test_domain_string,new_domain_string)

def clean_up_str(string):
    string = string.strip()
    string = re.sub(r"^\s+","", string) 
    string = re.sub(r"\s*\n\s+","\n", string) 
    string = re.sub(r"\t","", string) 
    string = re.sub(r"\s+"," ", string) 
    
    return string

if __name__ == '__main__':
    unittest.main()