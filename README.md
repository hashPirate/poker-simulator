# poker-simulator
an extremely fast method of calculating probabilities in poker

# Usage for the .txt files

- The first 2 letters of the filename will tell you the playercount (including yourself)
- The fields are separated by spaces
- The first field is your starting hand. (AQo would be Ace Queen off suit and A6s would be Ace Six suited)
- The next few fields are your percentage chance of winning, your percent chance with a random hand, your percent advantage over a random hand, the rank of the hand, the percentage of the rank.
- Then once the flop is out it shows your percentage increase/decrease depending on the pairs you made.

# Usage for the .py file

- Simply install treys, time and multiprocessing using pip
- Running the file will prompt you to enter the number of simulations and the number of players
- It will save the data to a file and you can use this data to run probabilities or train a model
- This program is incredibly fast and can do 5 million different games in under a minute. Enjoy!

# Future
- I will probably post the code used for analyzing the output and data as well that created the txt files. I am not happy with the speed yet.
