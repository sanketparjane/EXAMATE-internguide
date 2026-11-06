while True:
    print("\n--- InternGuide Main Menu ---")
    print("1: About InternGuide")
    print("2: Sample Questions")
    print("3: Check Internship Duration Rule")
    print("0: Exit")
    
    choice = input("Please select an option (0-3): ")
    
    if choice == '1':
        print("\nInternGuide helps engineering students understand AICTE internship hours, credits, and evaluation rules.")
    elif choice == '2':
        print("\nSample Questions you can ask:")
        print("- Does a 4-week online internship count?")
        print("- How many credits do I get for a rural NSS camp?")
        print("- Am I eligible for the PM Internship Scheme?")
    elif choice == '3':
        print("\n--- Internship Duration Rule Check ---")
        weeks = int(input("How many weeks was your internship? "))
        
        # One if/elif rule check from the domain
        if weeks < 3:
            print("Under AICTE rules, this might be too short to qualify for standard internship credits. Minimum is usually 3-4 weeks.")
        elif 3 <= weeks <= 4:
            print("A 3-4 week internship typically qualifies for a short-term internship credit block.")
        else:
            print("Internships longer than 4 weeks are excellent and can count towards major degree credits.")
    elif choice == '0':
        print("\nExiting InternGuide. Goodbye!")
        break
    else:
        print("\nInvalid selection. Please try again.")