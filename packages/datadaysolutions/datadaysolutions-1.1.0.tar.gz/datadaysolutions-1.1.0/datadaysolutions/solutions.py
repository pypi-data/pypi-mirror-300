"""
Provide hints, answers, and checks for questions in beginner python course.
"""

def reverse_list_hint():
    """Provides a hint for reversing a list."""
    print("Hint: You can use slicing to reverse a list. Try using lst[::-1].")


def variable_swap_check(a, b):
    if not (a==[30, 20, 10] and b==[10, 20, 30]):
        print("That is not correct!")
    else:
        print(
            """
            Nice Job!

            You probably used a temporarly third variable, but Python has another 
            solution that is more "Pythonic" and is what really makes coding fun!

            Try:
            a, b = b, a
            """
        )

def variable_swap_hint():
    print(
        """
        Try using a third variable, like 'z', as an interim step.
        """
    )


def variable_swap_solution():
    print(
        """
        Use an interim variable to store one of the values.
        z = x
        x = y
        y = z

        A more "Pythonic" (and fun) way is to use a concept called tuple unpacking.

        Try:
        a, b = b, a        
        """
    )

def list_index_check(student_list):
    if not student_list == ["ECM", "ACM", "TCM"]:
        print("That's not quite right!")
    else:
            print(
        """
        Very Nice!!

        Some solutions that would work are:
        truck_parts[1]
        truck_parts[-2]
        """
    )

def list_index_hint():
    print(
        """
        Remember that a list can contain a list of lists, and that lists are 0 based indexing, so which index would represent the second list?
        """
    )

def list_index_solution():
    print(
        """
        truck_parts[1] will return ["ECM", "ACM", "TCM"]
        truck_parts[-2] will also work.
        """
    )

    
def list_index_check2(part):
    if not part == "TCM":
        print("That's not quite right!")
    else:
        print(
            """
            Very Nice!!

            You can see that it is possible to use nested list indexing to get this sub-list value.

            Some solutions that would work are:
            truck_parts[1][2]
            truck_parts[-2][-1]
            """
        )

def list_index_hint2():
    print(
        """
        First think about how you could return the list that contains TCM.  
        
        Start by figuring out how to reach the outer list, and then drill down to the item you're looking for inside it.  
        
        There is a concept called "nested indexing".  Try searching the web for nested indexing.
        """
    )

def list_index_solution2():
    print(
        """
        Use a concept called "nested indexing".
        truck_parts[1][2]

        truck_parts[1] will return ["ECM", "ACM", "TCM"]
        And then the [2] further indexes this sub list to return "TCM".

        truck_parts[-2][-1] would also work.
        
        """
    )

def sort_order_check(student_answer, correct_answer = "c"):
    if student_answer.lower() == correct_answer:
        print(
            """
            That's correct! The reason is due to how functions and methods differ.

            Think of a method as giving direct instructions to the list. 
            When you tell the list to do something (like add or remove items), it changes the list itself. 
            It's like asking someone to change something for you—once they do it, the thing is different.
            
            A function is like a copy machine. 
            It works with the list and might give you a new result or do something with it, 
            but it doesn’t change the original list. 
            The original list stays the same unless you specifically tell it to change.

            Methods don't always operate like this but they often do. I just present this here to start 
            having you think about functions and methods differently.
            """
        )
    elif student_answer == "0":
        print("You need to replace the 0 with a letter.")
    else:
        print(
            """
            Try again.  One is a function and one is a method.  
            We didn't actually discuss this, so it's not 100% a fair question.
            Try looking up Python's documentation for List Methods and note the phrase "in place"
            """
        )


def sort_order_hint():
    print(
        """
        One is a function and one is a method.  
        We didn't actually discuss this, so it's not 100% a fair question.
        Try looking up Python's documentation for List Methods and note the phrase "in place"
        """
    )

def sort_order_solution():
    print(
        """
        The correct answer is c.

        The reason is due to how functions and methods differ.

        Think of a method as giving direct instructions to the list. 
        When you tell the list to do something (like add or remove items), it changes the list itself. 
        It's like asking someone to change something for you—once they do it, the thing is different.
        
        A function is like a copy machine. 
        It works with the list and might give you a new result or do something with it, 
        but it doesn’t change the original list. 
        The original list stays the same unless you specifically tell it to change.

        Methods don't always operate like this but they often do. I just present this here to start 
        having you think about functions and methods differently.        
        """
    )
    
def truck_count_check(student_answer, correct_answer = 5):
    if student_answer == correct_answer:
        print(
            """
            That's right! Nice Job!
            You probably could write your own function but why? 
            Python already has a built in method.  
            It's a good idea to check documentation if you are unsure if there is already an existing function.
            """
        )
    elif student_answer == 0:
        print("You need to replace the 0 with a number.")

    else:
        print(
        """
        That is not correct!
        """
        )

def truck_count_hint():
    print(
        """
        Did you find this link? https://docs.python.org/3/tutorial/datastructures.html
        """
    )

def truck_count_solution():
    print(
        """
        Check out https://docs.python.org/3/tutorial/datastructures.html
        
        list.count(x) --> Return the number of times x appears in the list.
        
        locs.count("Santiago") 
        """
    )

def truck_count_check2(student_answer, correct_answer = 5):
    if student_answer == correct_answer:
        print(
            """
            That's right! Nice Job!
            """
        )
    elif student_answer == 0:
        print("0 is the initialized value.  You need to update plant_count with the correct count.")

    else:
        print(
        """
        That is not correct!
        """
        )

def truck_count_hint2():
    print(
        """
        Take a look at the original case example from the lesson.  Can you incorporate a nested if statement?

        Also, if you are not sure how to increment the value of plant_count, check out the below link.
        https://stackoverflow.com/questions/2632677/python-integer-incrementing-with

        If you need help finding the correct coparison operator to use for an if statement, see this link:
        https://www.w3schools.com/python/gloss_python_comparison_operators.asp
        
        """
    )

def truck_count_solution2():
    print(
        """
        for loc in locs:
            if loc == "Santiago":
                plant_count += 1

        Another solution using list comprehension but the readability isn't as nice
        plant_count = sum([1 for loc in locs if loc == "Santiago"])

        True also is treated like a 1 in Python when summing
        plant_count = sum([True for loc in locs if loc == "Santiago"])

        
        """
    )

def list_comp_check(student_answer, correct_answer=[5, 7, 9, 11, 13]):
    if student_answer == correct_answer:
        print("""
        That's right! Nice Job!        
        """)
    
    elif student_answer == 0:
        print("You need to replace 0 with your list comprehension code.")
    
    else:
        print(
        """
        That is not correct!
        """
        )

def list_comp_hint():
    print(
        """
        Review the example from the lesson or look online for some examples.
        """
    )

def list_comp_solution():
    print(
        """
        result_list = [num * 2 + 3 for num in numbers]
        """
    )

def list_length_check(student_answer, correct_answer=[3, 2, 0, 4]):    
    if student_answer == correct_answer:
        print(
            """
            That's right! Nice Job!
            """
        )
    elif student_answer == [0]:
        print("[0] is the initialized value.  You need to update the list with the correct values.")

    else:
        print(
        """
        That is not correct!
        """
        )

def list_length_solution():
    print(
        """
        Correct answer: [3, 2, 0, 4]
        a: straightforward with length of 3 values
        b: The inner list counts as a single item
        c: Empty lists have a length of 0
        d: the [1:] indexing will return [4, 9, 8, 7] which is a length of 4
        """
    )

def list_zip_check():
    print(
        """
        Self-check.     
        
        Your output should look like the following where each (name, age) pair is printed on a new line.

        ('Alice', 25)
        ('Bob', 30)
        ('Charlie', 35)
        """
    )

def list_zip_hint():
    print(
        """
        How could you use zip along with a for loop?

        If you are still stuck, see this site https://stackoverflow.com/questions/49783594/for-loop-and-zip-in-python
        """
    )

def list_zip_solution():
    print(
        """
        for x in zip(names, ages):
            print(x)
        """
    )

def mighty_numbers_check(student_answer, correct_answer=[12, 16, 20, 24]):
    if sorted(student_answer) == correct_answer:
        print(
        """
        That's correct! Nice job!
        """)

    else:
        print(
            """
            That is not correct.
            """
        )

def mighty_numbers_hint1():
    print(
        """
        Have you tried using the modulus operator (%).  If you are unsure of its usage check out this website https://stackoverflow.com/questions/4432208/what-is-the-result-of-modulo-operator-percent-sign-in-python
        """
    )

def mighty_numbers_hint2():
    print(
        """
        Remember that you have to initialize mighty_list as an empty list.

        From there you will need to loop over each number (for loop).  And the for each number perform a test to check if the number is divisiable by 4 (using hint1) and also > 10. 
        """
    )

def mighty_numbers_solution():
    print(
        """
        Here is one possible solution:
        mighty_list = []
        for num in favorite_numbers:
            if num % 4 == 0 and num > 10:
                mighty_list.append(num)                        
        """
    )

def identify_bug_check():
    print("""
    Self check:
    If successful you should be able to run the code cell without error and see the following output printed:
    Corp HQ
    TEC
    Corp 3
    Corp 12
    Corp 9
    Corp 2
    """)

def identify_bug_hint():
    print("""
    Remember from the lesson that the variable declared in the for loop needs to be used in some way as part of the loop.
    
    """)

def identify_bug_solution():
    print("""
    From the syntax outlined in the class:  The variable name that is part of the loop (i) must match the variable called in the loop.

    So either of the below solutions would work:

    for i in corp_locations:
        print(i)

    OR

    for corp_location in corp_locations:
        print(corp_location)
    
    """)