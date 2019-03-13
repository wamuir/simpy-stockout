#!/usr/bin/env python3

import itertools
import simpy
import numpy

"""
Discrete-Event Simulation of Single-Product Inventory System (s,S)

This is a SimPy replication of the C program given by Law and Kelton
(2000, pp. 73--79) to simulate a single-product inventory system.

William Muir (2019)

"""


class Inventory(object):
    """
    Normally this would simply inherit class simpy.Container, however
    as Law and Kelton (2000) allow for negative inventories (see pages
    76 and 78, `demand(void)` and `update_time_avg_stats(void)`) some
    some customization is required for consistency.
    """

    def __init__(self, env, db, parameters):
        self._env = env
        self._db = db
        self._lastEvent = self._env.now
        self._openOrder = False
        self._parameters = parameters
        self.level = parameters["initial_inventory_level"]

    def get(self, size):
        """
        Take from inventory
        """
        self.level -= size
        self.update_time_avg_stats()

    def put(self, size):
        """
        Add to inventory
        """
        self.level += size
        self.update_time_avg_stats()

    def reorder(self, order):
        """
        Place an order with supplier
        """
        setup_cost = self._parameters["K"]
        incremental_cost = self._parameters["i"]
        if not self._openOrder:
            self._openOrder = True
            self._db["total_ordering_cost"] += (
                setup_cost + incremental_cost * order.size
            )
            yield self._env.timeout(order.lag)
            self.put(order.size)
            self._openOrder = False

    def update_time_avg_stats(self):
        """
        Corresponds to `update_time_avg_stats(void)`, p. 78
        """
        time_since_last_event = self._env.now - self._lastEvent
        if self.level < 0:
            self._db["area_shortage"] -= (
                self.level * time_since_last_event
            )
        elif self.level > 0:
            self._db["area_holding"] += (
                self.level * time_since_last_event
            )
        self._lastEvent = self._env.now


class ReOrder(object):
    """
    A class for reorders
    """

    def __init__(self, size, lag_range):
        self.size = size
        self.lag = numpy.random.uniform(*lag_range)


class Demand(object):
    """
    A class for demand
    """

    def __init__(self, size):
        self.size = size


def demand_generator(env, inventory, parameters):
    """
    Generate demand following exponential distribution
    """
    sizes = [i + 1 for i in range(parameters["number_of_demand_sizes"])]
    probabilities = numpy.diff(
        (0, *parameters["distribution_function_of_demand_sizes"])
    )
    while True:
        demand = Demand(
            size=numpy.random.choice(a=sizes, size=1, p=probabilities)[
                0
            ]
        )
        iat = numpy.random.exponential(
            parameters["mean_interdemand_time"]
        )
        yield env.timeout(iat)
        inventory.get(demand.size)


def evaluation_generator(env, inventory, policy):
    """
    Generate inventory evaluations against s,S policy
    """
    while True:
        if inventory.level < policy["minimum"]:
            order = ReOrder(
                size=policy["target"] - inventory.level,
                lag_range=parameters["delivery_lag_range"],
            )
            env.process(inventory.reorder(order))
        yield env.timeout(1)


def report(row_format, parameters, policy, db):
    """
    Write out a data row for the report, following Law and Kelton, p. 79
    """
    length = parameters["length_of_the_simulation"]
    aoc = db["total_ordering_cost"] / length
    ahc = db["area_holding"] * parameters["h"] / length
    asc = db["area_shortage"] * parameters["pi"] / length
    row = row_format.format(
        "({},{})".format(*[str(i).rjust(3) for i in policy.values()]),
        format(aoc + ahc + asc, ".2f"),
        format(aoc, ".2f"),
        format(ahc, ".2f"),
        format(asc, ".2f"),
    )
    print(row)


if __name__ == "__main__":

    """
    These are the parameters and inventory policies given in Law and
    Kelton (2000, p. 79) and as described in the FORTRAN code on p. 67
    """

    parameters = dict(
        initial_inventory_level=60,
        number_of_demand_sizes=4,
        distribution_function_of_demand_sizes=(
            0.167,
            0.500,
            0.833,
            1.000,
        ),
        mean_interdemand_time=0.10,
        delivery_lag_range=(0.50, 1.00),
        length_of_the_simulation=120,
        K=32.0,
        i=3.0,
        h=1.0,
        pi=5.0,
        number_of_policies=9,
    )

    policies = [
        dict(minimum=s, target=S)
        for s, S in itertools.product([20, 40, 60], [40, 60, 80, 100])
        if s < S
    ]

    """
    Write out a header row for the report
    """
    row_format = "\n{:>10}{:>25}{:>25}{:>25}{:>25}"
    header = row_format.format(
        "Policy",
        "Average total cost",
        "Average ordering cost",
        "Average holding cost",
        "Average shortage cost",
    )
    print(header)

    """
    Run the simulation.  As per Law and Kelton (2000), this only a
    single replication is run.  Given differences in random number
    generators (e.g., they use a LCG), results will not be identical.
    """
    numpy.random.seed(1234)
    for policy in policies:
        env = simpy.Environment()
        db = dict(
            last_event=float(),
            total_ordering_cost=float(),
            area_holding=float(),
            area_shortage=float(),
        )
        inventory = Inventory(env, db, parameters)
        dmd_gen = env.process(
            demand_generator(env, inventory, parameters)
        )
        eval_gen = env.process(
            evaluation_generator(env, inventory, policy)
        )
        env.run(until=120)
        report(row_format, parameters, policy, db)
