class Test:
    def __init__(self):
        self.variable = 3
def change_var(var):
    var.variable += 1

testing_object = Test()
print(testing_object.variable)
change_var(testing_object)
print(testing_object.variable)