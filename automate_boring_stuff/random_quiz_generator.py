#! C:/Users/neron/Anaconda3/envs/python37 python

###
# Nikola Dordic
# https://nidjo.com
# 19-Aug-2019
###

"""   
    random_quiz_generator.py - Creates quizzes with questions and answers in 
    random order, along with the answer key.

    Say you’re a geography teacher with 35 students in your class and you want 
    to give a pop quiz on US state capitals.
    Here is what the program does:
    Creates 35 different quizzes.
    Creates 50 multiple-choice questions for each quiz, in random order.
    Provides the correct answer and three random wrong answers for each 
    question, in random order.
    Writes the quizzes to 35 text files.
    Writes the answer keys to 35 text files.

    Project: Generating Random Quiz Files
    https://automatetheboringstuff.com/chapter8
"""

import random

# The quiz data. Keys are states and values are their capitals.
capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 
'NewMexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 
'WestVirginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

path = 'automate_boring_stuff/quiz_files/'

# Generate 35 quiz files.
for quizNum in range(1):

    # Create the quiz and answer key files.
    quizFile = open(path + 'capitalsquiz%s.txt' %(quizNum + 1), 'w')
    answerKeyFile = open(path + 'capitalsquiz_answers%s.txt' %(quizNum + 1), 'w')

    # Write out the header for the quiz.
    quizFile.write('Name:\n\nDate:\n\nPeriod:\n\n')
    quizFile.write((' ' * 20) + 'State Capitals Quiz (Form%s)' %(quizNum + 1))
    quizFile.write('\n\n')

    # Shuffle the order of the states.
    states = list(capitals.keys())
    random.shuffle(states)

    # Loop through all 50 states, making a question for each.
    for questionNum in range(50):

        # Get right and wrong answers.
        correctAnswer = capitals[states[questionNum]]
        wrongAnswers = list(capitals.values())
        del wrongAnswers[wrongAnswers.index(correctAnswer)]
        wrongAnswers = random.sample(wrongAnswers, 3)
        answerOptions = wrongAnswers + [correctAnswer]
        random.shuffle(answerOptions)
          
        # Write the question and answer options to the quiz file.
        quizFile.write('%s. What is the capital of %s\n' %(questionNum + 1, states[questionNum]))
        for i in range(4):
            quizFile.write('%s. %s\n' %('ABCD'[i], answerOptions[i]))
        quizFile.write('\n\n')

        # Write the answer key to a file.
        answerKeyFile.write('%s. %s\n' %(questionNum + 1, 'ABCD'[answerOptions.index(correctAnswer)]))
    
    quizFile.close()
    answerKeyFile.close()

     