# Variables for the project card
product_name = "InternGuide"
description = "Explains how many internship hours and credits an engineering student needs under AICTE rules, how they are evaluated, and which government internship schemes they can apply to."
target_user = "A third-year E&TC student at Sanjivani checking if online internships and NSS camps count for credit."
data_source = "AICTE and UGC policy PDFs"

# Printing the card using f-strings
print("="*50)
print(f"Welcome to {product_name}!")
print(f"About: {description}")
print(f"Designed for: {target_user}")
print(f"Data Sources: {data_source}")
print("="*50)

# Asking for user input
user_name = input("\nPlease enter your name: ")
user_question = input(f"Hello {user_name}, what is your question about AICTE internship rules today? ")

print(f"\nThanks, {user_name}. I have recorded your question: '{user_question}'")