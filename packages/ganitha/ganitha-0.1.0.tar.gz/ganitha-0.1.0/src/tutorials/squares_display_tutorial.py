#we are going to calculate the square of a number using methods mentioned in the Text Lilavati
#get the number from the user
number = int(input("Enter a number: "))

"""given a number, 
assign a placeholder for each digit starting with a, b, c, d etc.
for each digit in the number(given by its placeholder): 
i. append (placeholder_value)^2 to a list
ii. append 2*placeholder_value*all the digits  it in the number to the list
iii. finally display the list with plus operator between them
"""
# Initialize an empty list to store the terms
terms = []

# Assign placeholders for each digit
placeholders = 'abcdefghijklmnopqrstuvwxyz'

# Convert the number to a string for easy digit access
num_str = str(number)

# Iterate through each digit in the number
for i, digit in enumerate(num_str):
    digit = int(digit)
    placeholder = placeholders[i]
    
    # Append (placeholder_value)^2 to the list
    terms.append(f"({placeholder}^2)")
    
    # Append 2*placeholder_value*all the digits to its right
    if i < len(num_str) - 1:
        right_digits = num_str[i+1:]
        for j, right_digit in enumerate(right_digits):
            terms.append(f"(2*{placeholder}*{placeholders[i+j+1]})")

# Display the list with plus operators between terms
result = " + ".join(terms)
print(f"Expanded form: {result}")

"""given a number, 
for each digit in the number: 
i. find its place value, multiply by the digit. let this be result array
ii. assign for the result a placeholder starting with a, b, c, d etc. placeholder_dict
Now for each placeholder:
i. append (placeholder's value)^2 to a list
ii. append 2*placeholder's'*all the other digits placeholder's value to the list
iii. display the list
"""
# Initialize an empty list to store the result array
result_array = []

# Initialize a dictionary to store placeholders
placeholder_dict = {}

# Convert the number to a string for easy digit access
num_str = str(number)

# Step 1: Calculate place value and multiply by digit
for i, digit in enumerate(num_str):
    digit = int(digit)
    place_value = 10 ** (len(num_str) - i - 1)
    result = digit * place_value
    result_array.append(result)
    placeholder_dict[placeholders[i]] = result

# Initialize a list to store the expanded terms
expanded_terms = []
expanded_values = []  # New list to store numerical values

# Step 2: Generate expanded form
for i, placeholder in enumerate(placeholder_dict):
    value = placeholder_dict[placeholder]
    
    # Append (placeholder's value)^2 to the list
    expanded_terms.append(f"({value}^2)")
    expanded_values.append(value ** 2)  # Add numerical value
    
    # Append 2 * placeholder's value * all other placeholders' values
    for j, other_placeholder in enumerate(placeholder_dict):
        if i != j:
            other_value = placeholder_dict[other_placeholder]
            expanded_terms.append(f"(2*{value}*{other_value})")
            expanded_values.append(2 * value * other_value)  # Add numerical value

# Display the result array
print("Result array:", result_array)

# Display the expanded form
print("Expanded form (using place values):")
print(" + ".join(expanded_terms))

# Sum of the expanded terms
sum_of_expanded_terms = sum(expanded_values)
print("Sum of the expanded terms:", sum_of_expanded_terms)

# "Perform place value decomposition
# #multiply place and value
# digits = []
# temp = number
# while temp > 0:
#     digits.insert(0, temp % 10)
#     temp //= 10

# # Display the decomposition
# print("Place value decomposition:")
# for i, digit in enumerate(digits):
#     place_value = 10 ** (len(digits) - i - 1)
#     print(f"{digit} * {place_value}")








# #getting a number from the user
# number = int(input("Enter a number: "))


# #method 1 Sliding method
# #step 1: display the box for the final answer

# #convert the number to string
# number_str = str(number)

# #get the length of the number
# length = len(number_str)

# #number of digits in the final answer is the length of the number*2
# number_of_digits = length*2

# #print 'Result -> ' with _ for the number of digits
# print("Result -> " + "_" * number_of_digits)


# #get the first digit
# first_digit = int(number_str[0])

def lilavati_square(number):
    num_str = str(number)
    length = len(num_str)
    result = 0

    for i, digit in enumerate(num_str):
        digit = int(digit)
        place_value = 10 ** (length - i - 1)
        term = digit * place_value
        
        # Square of the term
        result += term ** 2
        
        # Cross products
        for j in range(i + 1, length):
            other_digit = int(num_str[j])
            other_place_value = 10 ** (length - j - 1)
            result += 2 * term * other_digit * other_place_value

    return result

# Example usage
number = 123
print(f"Square of {number} using Lilavati's method: {lilavati_square(number)}")



