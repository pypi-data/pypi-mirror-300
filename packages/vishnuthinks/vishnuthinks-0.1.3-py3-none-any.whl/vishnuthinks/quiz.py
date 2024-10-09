import random

# Step 1: Create a pool of Python-related quiz questions with options
quiz_pool = [
    {"question": "What is the output of `print(2 ** 3)`?", "options": ["8", "6", "4"], "answer": "1"},
    {"question": "Which method is used to add an element to a list?", "options": [".add()", ".append()", ".insert()"], "answer": "2"},
    {"question": "What is the result of `10 // 3`?", "options": ["3", "4", "2"], "answer": "1"},
    {"question": "How do you define a function in Python?", "options": ["function_name()", "def function_name()", "define function_name()"], "answer": "2"},
    {"question": "What is the correct way to import the 'math' module?", "options": ["import math", "from math import *", "import math_lib"], "answer": "1"},
    {"question": "What keyword is used to handle exceptions?", "options": ["try-except", "catch", "finally"], "answer": "1"},
    {"question": "How do you create a tuple in Python?", "options": ["using parentheses, e.g., (1, 2, 3)", "using square brackets, e.g., [1, 2, 3]", "using curly braces, e.g., {1, 2, 3}"], "answer": "1"},
    {"question": "What is the method to remove an item from a dictionary?", "options": [".remove()", ".pop()", ".delete()"], "answer": "2"},
    {"question": "What is the difference between `==` and `is`?", "options": ["`==` checks value equality, `is` checks object identity", "`==` checks object identity, `is` checks value equality", "`==` and `is` are the same"], "answer": "1"},
    {"question": "How do you reverse a string in Python?", "options": ["using slicing, e.g., `string[::-1]`", "using string.reverse()", "using list reverse()"], "answer": "1"},
    {"question": "Which of the following is used to create an empty dictionary?", "options": ["{}", "[]", "set()"], "answer": "1"},
    {"question": "How can you check the type of a variable?", "options": ["type(variable)", "typeof(variable)", "checktype(variable)"], "answer": "1"},
    {"question": "What is the output of `print(7 % 2)`?", "options": ["1", "3", "2"], "answer": "1"},
    {"question": "Which of the following is a mutable data type?", "options": ["list", "tuple", "string"], "answer": "1"},
    {"question": "What is the purpose of the `pass` keyword?", "options": ["To break a loop", "To create a placeholder for code", "To stop a function"], "answer": "2"},
    {"question": "What is the default value of a function parameter if no value is passed?", "options": ["None", "0", "undefined"], "answer": "1"},
    {"question": "Which of the following is the correct way to remove all elements from a list?", "options": ["list.clear()", "list.remove()", "list.del()"], "answer": "1"},
    {"question": "How do you write a comment in Python?", "options": ["// This is a comment", "# This is a comment", "<!-- Comment -->"], "answer": "2"},
    {"question": "How do you concatenate two lists in Python?", "options": ["list1 + list2", "list1.append(list2)", "list1.concat(list2)"], "answer": "1"},
    {"question": "What is the output of `len([1, 2, 3])`?", "options": ["3", "6", "2"], "answer": "1"},
    {"question": "How can you find the maximum value in a list?", "options": ["max(list)", "list.max()", "max(list())"], "answer": "1"},
    {"question": "What is the difference between `deep copy` and `shallow copy`?", "options": ["Shallow copy creates a new object, deep copy does not", "Shallow copy shares references to objects, deep copy does not", "They are the same"], "answer": "2"},
    {"question": "Which method can be used to get the last element of a list?", "options": ["list[-1]", "list[0]", "list.last()"], "answer": "1"},
    {"question": "What will `print('Hello'.startswith('H'))` output?", "options": ["True", "False", "Error"], "answer": "1"},
    {"question": "Which function is used to sort a list in Python?", "options": ["list.sort()", "sort(list)", "list.order()"], "answer": "1"},
    {"question": "Which of the following is used to check if a key exists in a dictionary?", "options": ["key in dict", "key.exists(dict)", "dict.has_key(key)"], "answer": "1"},
    {"question": "What is the output of `print(3 + 2 * 3)`?", "options": ["9", "15", "7"], "answer": "1"},
    {"question": "What is a generator in Python?", "options": ["A type of function that returns a value", "A type of function that yields values one at a time", "A type of list"], "answer": "2"},
    {"question": "How do you define a class in Python?", "options": ["class ClassName:", "def ClassName:", "define ClassName:"], "answer": "1"},
    {"question": "Which of the following is used to format strings in Python?", "options": ["string.format()", "f-strings", "Both"], "answer": "3"},
    {"question": "What is the purpose of the `self` keyword in Python?", "options": ["To refer to the current instance of the class", "To initialize the class", "To create a new function"], "answer": "1"},
    {"question": "Which of the following is the correct way to call a function in Python?", "options": ["function_name()", "function call", "function.call()"], "answer": "1"},
    {"question": "What is the output of `print(type('Hello'))`?", "options": ["<class 'str'>", "<type 'str'>", "string"], "answer": "1"},
    {"question": "What does `//` do in Python?", "options": ["Floor division", "Exponentiation", "Modulo"], "answer": "1"},
    {"question": "Which of the following is the correct way to create a dictionary?", "options": ["{key: value}", "key: value{}", "dict(key = value)"], "answer": "1"},
    {"question": "How do you check if an element is in a list?", "options": ["element in list", "list.contains(element)", "list.has(element)"], "answer": "1"},
    {"question": "What does the `zip()` function do in Python?", "options": ["It merges two lists", "It compresses a list", "It joins two strings"], "answer": "1"},
    {"question": "Which of the following is a built-in function to find the length of a string?", "options": ["len()", "length()", "string.len()"], "answer": "1"},
    {"question": "How do you remove duplicates from a list?", "options": ["set(list)", "list.unique()", "list.remove_duplicates()"], "answer": "1"},
]

# Global variable to store the total score
total_score = 0

def run_quiz():
    global total_score  # Access the global score variable
    
    # Select 10 random questions from the pool
    selected_questions = random.sample(quiz_pool, 10)
    
    # Initialize the score for this quiz
    score = 0
    
    print("\nWelcome to the VishnuThinks Python Quiz!\n")
    
    # Loop through the selected questions and get user input
    for idx, q in enumerate(selected_questions, 1):
        print(f"Question {idx}: {q['question']}")
        
        # Display options
        for i, option in enumerate(q['options'], 1):
            print(f"  {i}. {option}")
        
        # Get user's answer (they choose the option number)
        user_answer = input("Choose your answer (1, 2, or 3): ").strip()
        
        # Validate answer
        if user_answer == q['answer']:
            print("Correct!\n")
            score += 1
        else:
            correct_option = int(q['answer']) - 1
            print(f"Wrong! The correct answer is: {q['options'][correct_option]}\n")
    
    # Show the score for this quiz and update total score
    print(f"Your score for this quiz is: {score}/10\n")
    total_score += score  # Update global total score
    
    # Ask if the user wants to play again
    play_again = input("Do you want to try again? (yes/no): ").strip().lower()
    if play_again == 'yes':
        run_quiz()  # Recursively call the quiz function to restart
    else:
        print(f"Thank you for playing! Your total score is: {total_score}")

# Run the quiz for the first time
run_quiz()
