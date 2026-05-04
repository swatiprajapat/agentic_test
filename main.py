from app.app import process_request

def main(): 
    print("AI Agent Active.(Type 'exit' to quit)")

    while True:
        user_input=input("\n You : ").strip()

        if user_input.lower()in ["exit","quit","q"]:
            print("Goodby!")
            break
        if not user_input:
            continue

        response=process_request(user_input)
        print(f"Agent:{response}")

if __name__ == "__main__":
    main()   
#main.py

from app.app import process_request

def main():
    print("AI Agent Active. (Type 'exit' to quit)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue

        response = process_request(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()