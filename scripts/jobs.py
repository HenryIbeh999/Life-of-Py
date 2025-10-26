class Job:
    def __init__(self,name,salary,energy_cost):
        self.name = name
        self.salary = float(salary)
        self.energy_cost = energy_cost
        self.happiness_cost = 10


def load_jobs():
    cashier = Job(name="Cashier",salary=17.5,energy_cost=20)
    salesman = Job(name="Salesman",salary=23.36,energy_cost=20)
    clerk = Job(name="Clerk",salary=26.0,energy_cost=20)
    accountant = Job(name="Accountant",salary=33.0,energy_cost=20)
    programmer = Job(name="Programmer",salary=50.76,energy_cost=25)
    doctor = Job(name="Doctor",salary=63.0,energy_cost=30)
    cook = Job(name="Cook",salary=19.0,energy_cost=25)

    return [cashier,salesman,clerk,accountant,programmer,doctor,cook]
