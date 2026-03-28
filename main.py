from agent.planner import Planner
def main():
    print("Hello from ai-coding-agent!")
    
    planner = Planner()
    
    prompt = "You are a helpful assistant"
    planner.create_plan(prompt)


if __name__ == "__main__":
    main()
