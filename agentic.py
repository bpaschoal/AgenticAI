import ollama
from report import generate_report


def analyze_trends():
    """
    Use Ollama to analyze AI trends with a simple prompt
    """
    print("\n" + "="*60)
    print("AGENTIC AI - Tech Researcher Agent")
    print("="*60)
    print("\nTask: Analyze the top 3 AI trends for 2025")
    print("Model: Llama3 (Local via Ollama)")
    print("\nGenerating response...\n")
    
    prompt = """You are an expert AI researcher. Analyze and provide the top 3 AI trends for 2025.
    
For each trend, provide:
1. Trend Name
2. Brief Description
3. Impact/Importance

Format your response clearly with numbers and bullet points."""
    
    try:
        # Call Ollama model
        response = ollama.generate(
            model="llama3",
            prompt=prompt,
            stream=False
        )
        
        print("="*60)
        print("RESEARCH RESULTS:")
        print("="*60)
        print(response['response'])
        
        # Generate and save reports
        generate_report(
            response_text=response['response'],
            task="Analyze the top 3 AI trends for 2025",
            model="Llama3 (Local via Ollama)"
        )
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")
        return False


if __name__ == "__main__":
    success = analyze_trends()
    if success:
        print("\nAgent execution completed successfully!")
        print("Files saved:")
        print("   - research_results.json")
        print("   - research_results.html")
    else:
        print("\nAgent execution failed")