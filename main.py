import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Your OpenRouter API key
OPENROUTER_API_KEY = "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"

def get_random_search_word():
    """Generate random search terms using OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # More varied prompts for better search terms
    prompts = [
        "Generate a random topic people commonly search for online. Just the search term.",
        "Give me a random question or topic for web search. Only the search phrase.",
        "Create a random search query about any interesting topic. Just return the search terms.",
        "Generate a random word or phrase someone might google. Only the search term.",
        "Give me a random educational or entertaining search topic. Just the phrase."
    ]
    
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": random.choice(prompts)},
            {"role": "user", "content": "Please provide only the search term without quotes or explanation."}
        ],
        "max_tokens": 20,
        "temperature": 1.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        search_term = result['choices'][0]['message']['content'].strip()
        # Clean up the response
        search_term = search_term.replace('"', '').replace("'", "").strip()
        return search_term[:100]  # Limit length
    except Exception as e:
        print(f"API Error: {e}")
        # Fallback terms if API fails
        fallback_terms = [
            "healthy recipes", "travel tips", "technology news", "fitness routines",
            "cooking tutorials", "space exploration", "wildlife photography", 
            "digital art", "sustainable living", "productivity hacks"
        ]
        return random.choice(fallback_terms)

def human_like_typing(element, text):
    """Type text with human-like delays and occasional mistakes"""
    element.clear()
    time.sleep(random.uniform(0.3, 0.8))
    
    for i, char in enumerate(text):
        element.send_keys(char)
        
        # Random typing speed (faster for common letters)
        if char in 'aeiou ':
            delay = random.uniform(0.05, 0.15)  # Faster for vowels and spaces
        else:
            delay = random.uniform(0.08, 0.25)  # Slower for consonants
        
        time.sleep(delay)
        
        # Occasional pause (like thinking)
        if random.random() < 0.1:  # 10% chance
            time.sleep(random.uniform(0.5, 1.5))
        
        # Very rare typo simulation (backspace and retype)
        if random.random() < 0.03 and i < len(text) - 1:  # 3% chance, not on last char
            time.sleep(random.uniform(0.2, 0.5))
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(random.uniform(0.1, 0.3))
            element.send_keys(char)

def human_like_scrolling(driver, search_count):
    """Perform human-like scrolling behavior"""
    try:
        # Different scrolling patterns based on search count
        if search_count % 4 == 0:  # Every 4th search - scroll up as requested
            print("📜 Scrolling up (every 4th search)")
            # First scroll down a bit
            scroll_amount = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1.0, 2.5))
            
            # Then scroll up
            scroll_up = random.randint(200, 600)
            driver.execute_script(f"window.scrollBy(0, -{scroll_up});")
            time.sleep(random.uniform(0.8, 2.0))
            
            # Maybe scroll up more
            if random.random() < 0.6:
                additional_up = random.randint(100, 400)
                driver.execute_script(f"window.scrollBy(0, -{additional_up});")
                time.sleep(random.uniform(0.5, 1.5))
        
        else:  # Normal scrolling behavior
            scroll_actions = random.randint(2, 5)  # 2-5 scroll actions
            
            for _ in range(scroll_actions):
                # Random scroll direction (mostly down, sometimes up)
                if random.random() < 0.8:  # 80% chance to scroll down
                    scroll_amount = random.randint(200, 600)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                else:  # 20% chance to scroll up
                    scroll_amount = random.randint(100, 300)
                    driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                
                # Random pause between scrolls
                time.sleep(random.uniform(0.5, 2.0))
        
        # Occasionally scroll to a random position
        if random.random() < 0.3:  # 30% chance
            random_position = random.randint(0, 1000)
            driver.execute_script(f"window.scrollTo(0, {random_position});")
            time.sleep(random.uniform(0.5, 1.5))
            
    except Exception as e:
        print(f"Scrolling error: {e}")

def simulate_human_reading(driver):
    """Simulate human reading behavior on search results"""
    try:
        # Sometimes click on a search result (but don't navigate away)
        if random.random() < 0.3:  # 30% chance
            search_results = driver.find_elements(By.CSS_SELECTOR, "h2 a, .b_algo h2 a")
            if search_results:
                # Hover over a random result (simulate reading titles)
                result = random.choice(search_results[:5])  # Only top 5 results
                driver.execute_script("""
                    arguments[0].style.backgroundColor = 'rgba(0,123,255,0.1)';
                    setTimeout(() => arguments[0].style.backgroundColor = '', 1000);
                """, result)
                time.sleep(random.uniform(0.8, 2.0))
        
        # Simulate reading time with random mouse movements
        simulate_mouse_movement(driver)
        
    except Exception as e:
        print(f"Reading simulation error: {e}")

def simulate_mouse_movement(driver):
    """Simulate random mouse movements"""
    try:
        # Random mouse movements
        movements = random.randint(3, 8)
        for _ in range(movements):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                document.dispatchEvent(event);
            """)
            time.sleep(random.uniform(0.2, 0.8))
    except:
        pass  # Ignore mouse movement errors

def random_page_interaction(driver):
    """Perform random page interactions"""
    try:
        interactions = [
            lambda: time.sleep(random.uniform(0.5, 2.0)),  # Just wait/read
            lambda: driver.execute_script("window.scrollBy(0, 100);"),  # Small scroll
            lambda: simulate_mouse_movement(driver),  # Mouse movements
        ]
        
        # Pick 1-3 random interactions
        num_interactions = random.randint(1, 3)
        selected_interactions = random.sample(interactions, num_interactions)
        
        for interaction in selected_interactions:
            interaction()
            time.sleep(random.uniform(0.3, 1.0))
            
    except Exception as e:
        print(f"Page interaction error: {e}")

def setup_human_like_browser():
    """Setup browser with human-like options"""
    EDGEDRIVER_PATH = "C:/Users/kesha/Downloads/msedgedriver.exe"
    service = Service(EDGEDRIVER_PATH)
    
    options = webdriver.EdgeOptions()
    
    # Anti-detection options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Human-like browser settings
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Random window size (but reasonable)
    window_sizes = [(1366, 768), (1920, 1080), (1440, 900), (1536, 864)]
    width, height = random.choice(window_sizes)
    options.add_argument(f"--window-size={width},{height}")
    
    driver = webdriver.Edge(service=service, options=options)
    
    # Remove automation indicators
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def main():
    """Main automation function"""
    driver = setup_human_like_browser()
    search_count = 0
    
    print("🤖 Starting human-like browser automation...")
    print("📊 Features: Random typing, scrolling, mouse movements, reading simulation")
    print("-" * 60)
    
    try:
        for search_num in range(10):  # Number of searches to perform
            search_count += 1
            
            # Get random search term
            query = get_random_search_word()
            print(f"\n🔍 Search {search_count}/10: '{query}'")
            
            # Navigate to Bing with random delay
            driver.get("https://www.bing.com")
            initial_wait = random.uniform(2, 5)
            print(f"⏱️ Page load wait: {initial_wait:.2f}s")
            time.sleep(initial_wait)
            
            try:
                # Find search box with multiple selectors
                search_box = None
                selectors = ["name=q", "id=sb_form_q", "css=[name='q']"]
                
                for selector in selectors:
                    try:
                        if selector.startswith("name="):
                            search_box = driver.find_element(By.NAME, selector[5:])
                        elif selector.startswith("id="):
                            search_box = driver.find_element(By.ID, selector[3:])
                        elif selector.startswith("css="):
                            search_box = driver.find_element(By.CSS_SELECTOR, selector[4:])
                        break
                    except NoSuchElementException:
                        continue
                
                if not search_box:
                    print("❌ Could not find search box")
                    continue
                
                # Human-like typing
                print("⌨️ Typing search term...")
                human_like_typing(search_box, query)
                
                # Random delay before pressing Enter
                pre_enter_delay = random.uniform(0.5, 2.0)
                time.sleep(pre_enter_delay)
                
                # Press Enter
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results to load
                results_wait = random.uniform(3, 6)
                print(f"📄 Waiting for results: {results_wait:.2f}s")
                time.sleep(results_wait)
                
                # Human-like behaviors on results page
                print("👁️ Simulating reading behavior...")
                simulate_human_reading(driver)
                
                # Scrolling behavior (special behavior every 4th search)
                human_like_scrolling(driver, search_count)
                
                # Random page interactions
                random_page_interaction(driver)
                
                # Random reading/viewing time
                reading_time = random.uniform(5, 15)
                print(f"📖 Reading time: {reading_time:.2f}s")
                time.sleep(reading_time)
                
                # Tab management (except for last search)
                if search_num < 9:  # Not the last search
                    print("🔄 Opening new tab and closing current...")
                    
                    # Open new tab
                    driver.execute_script("window.open('');")
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Close current tab
                    driver.close()
                    
                    # Switch to new tab
                    driver.switch_to.window(driver.window_handles[-1])
                    
                    # Random delay between searches
                    between_search_delay = random.uniform(2, 8)
                    print(f"⏳ Delay before next search: {between_search_delay:.2f}s")
                    time.sleep(between_search_delay)
                
            except Exception as e:
                print(f"❌ Error during search: {e}")
                time.sleep(3)  # Wait before continuing
        
        print("\n✅ Automation completed successfully!")
        print("🎉 All searches performed with human-like behavior")
        
        # Keep browser open briefly before closing
        print("🔚 Closing browser in 5 seconds...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n⚠️ Automation stopped by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
    finally:
        try:
            driver.quit()
            print("🚪 Browser closed")
        except:
            pass

if __name__ == "__main__":
    main()