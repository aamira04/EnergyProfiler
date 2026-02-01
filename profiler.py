import cProfile, pstats, psutil, time, os, re, sys, io
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# Replace with your actual Gemini API key from Google AI Studio
GEMINI_API_KEY = "AIzaSyABrlcbi9t6pBYKYIVWtQBSlnrynzopy5I" 

genai.configure(api_key=GEMINI_API_KEY)

LAPTOP_TDP = 25  # Estimated power draw in Watts for calculation

def run_profiler(file_path):
    profiler = cProfile.Profile()
    profiler.enable()

    with open(file_path) as f:
        code = f.read()
        exec(code, {})

    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(10)

    return stats.stats

def get_ai_optimization(original_code, joules):
    prompt = f"""
    You are a Green Computing expert. The following Python code used {joules:.6f} Joules.
    1. Identify the 'Energy Hotspot' (the most inefficient part).
    2. Provide an optimized version of the entire script.
    3. Explain why the fix reduces CPU cycles.
    
    Return the optimized code inside a standard ```python ``` block.

    Original Code:
    {original_code}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        content = response.text
        
        # Regex to extract code between backticks for automation
        match = re.search(r"```python\n(.*?)```", content, re.DOTALL)
        optimized_code = match.group(1).strip() if match else None
        
        return optimized_code, content
    except Exception as e:
        print(f"❌ AI API Error: {e}")
        return None, None
    
    

