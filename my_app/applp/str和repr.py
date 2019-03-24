class Classes:
    def __init__(self, name):
        self.name = name
        self.students = []

    def __str__(self):
        return "<Classes object: {}>".format(self.name)


class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Student object: {}>".format(self.name)

    # def __repr__(self):
    #     return "<学生 object: {}>".format(self.name)
    __repr__ = __str__

c1 = Classes('py16')
s1 = Student('alex')
s2 = Student('wusir')
c1.students.append(s1)
c1.students.append(s2)
# print(c1)
print(s1)
print(s2)
print(c1.students)
