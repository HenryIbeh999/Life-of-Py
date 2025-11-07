class Job:
    def __init__(self,name,salary,energy_cost):
        self.name = name
        self.salary = float(salary)
        self.energy_cost = energy_cost
        self.health_cost = 20


def load_jobs():
    cashier = Job(name="Cashier",salary=37.5,energy_cost=20)
    salesman = Job(name="Salesman",salary=43.36,energy_cost=20)
    clerk = Job(name="Clerk",salary=46.0,energy_cost=20)
    accountant = Job(name="Accountant",salary=63.0,energy_cost=20)
    programmer = Job(name="Programmer",salary=80.76,energy_cost=25)
    doctor = Job(name="Doctor",salary=105.00,energy_cost=30)
    cook = Job(name="Cook",salary=39.0,energy_cost=25)

    return [cashier,salesman,clerk,accountant,programmer,doctor,cook]
