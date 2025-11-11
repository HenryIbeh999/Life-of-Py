class Job:
    def __init__(self, name, base_salary, energy_cost, lvl_required):
        self.name = name
        self.base_salary = float(base_salary)
        self.energy_cost = energy_cost
        self.health_cost = 20
        self.lvl_required= int(lvl_required)



def load_jobs():
    cashier = Job(name="Cashier", base_salary=37.5, energy_cost=20, lvl_required=1)
    salesman = Job(name="Salesman", base_salary=43.36, energy_cost=20, lvl_required=1)
    clerk = Job(name="Clerk", base_salary=56.0, energy_cost=20, lvl_required=3)
    accountant = Job(name="Accountant", base_salary=63.0, energy_cost=20, lvl_required=5)
    programmer = Job(name="Programmer", base_salary=90.76, energy_cost=25, lvl_required=10)
    doctor = Job(name="Doctor", base_salary=105.00, energy_cost=30, lvl_required=15)
    cook = Job(name="Cook", base_salary=49.0, energy_cost=25, lvl_required=2)

    return [cashier,salesman,clerk,accountant,programmer,doctor,cook]
