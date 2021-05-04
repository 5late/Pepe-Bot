import random
correct_number = False
print("*****Halftime break! You get 3 tries to guess the correct number for an extra point*****\n Rules:\n 1.The number range is 1-5\n 2.The number changes every time you guess\n")

for i in range(2):
    while True:
        try:
            guess = int(input("What is your guess? "))
            break
        except ValueError:
            print("Please enter a number!")  
            continue
    if guess == random.choice([1, 2, 3, 4, 5]):
        print("\nCONGRATS you get an extra point. The quiz will continue.\n")
        correct_number = True
        total += 1
        break
    else:
        print("Try again\n")

#Last attempt and different statements 
if correct_number != True:
    while True:
      try:
        guess = int(input("What is your guess? "))
        break
      except ValueError:
          print("Please enter a number!")  
          continue
    if guess  == random.choice([1, 2, 3, 4, 5]):
      print("CONGRATS you get an extra point. The quiz will continue.\n")
      total += 1  
    else:
      print("Good try, the quiz will resume.\n")