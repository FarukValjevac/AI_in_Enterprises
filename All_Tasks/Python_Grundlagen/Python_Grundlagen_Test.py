import random

#
# def largest_number(my_list):
#     my_list.sort()
#     return my_list[-1]
#
#
# a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# print([i for i in a if i < 5])
#
# a = random.sample(range(1, 100), 20)
# b = random.sample(range(1, 100), 25)
# # print(set(a + b))
#
# print(largest_number(a))

number = random.randint(1, 15)
user_input = int(input("If you guess the random number between 1 and 15 you are the winner!\nPlease enter a number: "))
if number == user_input:
    print("We have a winner, you have guessed the correct number!!!")
elif number < user_input:
    print(f"Unfortunately you guessed to high, the winning number was {number} but you chose {user_input} :(")
else:
    print(f"Unfortunately you guessed to low, the winning number was {number} but you chose {user_input} :(")