from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from more_itertools import collapse
from input_data_generation import *
from logging_actions import *
import random
from datetime import datetime  # Add this import for timestamp handling

def start_SUT_and_get_driver(website_url,preparations):
    """
    Starts up the System Under Test (SUT) by starting a Chrome WebDriver instance and
    performing any necessary preparation steps.

    Parameters:
    - website_url (str): The URL of the web application to be tested. This is where the WebDriver will navigate after starting.
    - preparations (list of functions): A list of preparation steps (functions) to be executed once the WebDriver is
      initialized and navigated to the target URL. These steps might include actions like logging in or setting up the
      initial application state. Each function in the list should accept the WebDriver instance as an argument.

    Returns:
    - WebDriver instance (driver) that can be used for further interactions within the SUT.
    """
    
    # Create ChromeOptions instance
    chrome_options = Options()
    
    # Performance optimization options
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for speed
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    
    # Add preferences to disable password manager leak detection
    chrome_options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    
    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    
    # Set aggressive timeouts for faster execution
    driver.set_page_load_timeout(15)  # 15 seconds max to load a page
    driver.implicitly_wait(2)  # 2 seconds implicit wait instead of default 10
    
    # Navigate to the URL of the application to be tested
    driver.get(website_url)
    
    # Execute the necesary preparations (i.e. login, etc.) if any.
    for prepare in preparations:
        prepare(driver)
    
    return driver


def derive_actionable_elements(driver, filter_elements):
    """
    Derives a list of actionable elements (widgets) from the current state of the web application.
    
    """
    # Use a more efficient CSS selector - request only what we need
    selectors = [
        "a", "button", "select",  # Most common interactive elements
        "input[type='submit']", "input[type='button']",
        "input[type='text']", "input[type='password']", 
        "input[type='checkbox']", "input[type='radio']",
        "textarea",
    ]

    # Combine all the selectors into a single CSS selector
    all_selectors = ", ".join(selectors)

    # Find all actionable elements
    actionable_elements = driver.find_elements(By.CSS_SELECTOR, all_selectors)
    
    # Filtra automaticamente i link che aprono nuove tab o puntano a siti esterni
    auto_filtered_elements = []
    current_url = driver.current_url
    base_domain = ""
    try:
        # Estrai il dominio base dall'URL corrente
        if "://" in current_url:
            base_domain = current_url.split("://")[1].split("/")[0]
    except:
        pass
        
    for element in actionable_elements:
        should_filter = False
        if element.tag_name.lower() == "a":
            # Had some issues with external tabs openening, so...
            
            # Filtra link con target="_blank" (aprono nuove tab)
            target = element.get_attribute("target")
            if target and target == "_blank":
                should_filter = True
                
            # Filtra link a siti esterni
            href = element.get_attribute("href")
            if href and base_domain and base_domain not in href:
                # Link esterno (non contiene il dominio base)
                should_filter = True
                
        if should_filter:
            auto_filtered_elements.append(element)
    
    # Compute the list of elements that should be filtered (user-defined filters + automatic ones)
    filtered_elements = list(collapse([f(driver) for f in filter_elements])) + auto_filtered_elements
    
    # Derive only those that are displayed and enabled and should not be filtered
    visible_actionable_elements = [
    element for element in actionable_elements
    if element.is_displayed() and element.is_enabled() and not (element in filtered_elements)
    ]
    
    print("visible_actionable_elements", len(visible_actionable_elements))

    return visible_actionable_elements

def derive_actions(driver, filter_elements):
    """
    Derives all possible actions on a randomly selected actionable element
    """
    visible_actionable_elements = derive_actionable_elements(driver, filter_elements)
    
    #select a random element from visible_actionable_elements
    #then we do not have to derive all actions for all elements, should make it faster
    selected_element_id = int(random.randint(0, len(visible_actionable_elements)-1))
    element = visible_actionable_elements[selected_element_id]
    
    #Make sure the element is in view to prevent ElementClickInterceptedException (on smaller screens)
    #Unfortunately scrollIntoView in JS (below) does not seem to work.... (not sure if it is only a specific browser config)
    #driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    
    #Can do it with Selenium action chains, but unfortunately makes it slower
    #create action chain object
    action = ActionChains(driver).scroll_to_element(element).perform()
    
    #List that will store all the derived actions for the selected element
    actions = []

    # Basic click
    actions.append(lambda el=element: (log("click", el), el.click()))
    
    # The lambda construction creates an anonymous function that captures the element
    # When called, it executes both the log function and the click action
    
    # Get element tag and type for conditional actions
    tag_name = element.tag_name.lower()
    element_type = element.get_attribute("type")
    
    # Actions for text input fields
    if tag_name == "input" and element_type in ["text", "password", "email", "search"]:
        random_text = generate_random_text(10)  # Assuming this function exists in input_data_generation
        actions.append(lambda el=element, txt=random_text: (
            log(f"input text: {txt}", el), 
            el.clear(), 
            el.send_keys(txt)
        ))
    
    # Actions for textareas
    elif tag_name == "textarea":
        random_text = generate_random_text(20)
        actions.append(lambda el=element, txt=random_text: (
            log(f"input textarea: {txt}", el), 
            el.clear(), 
            el.send_keys(txt)
        ))
    
    # Actions for select (dropdown) elements
    elif tag_name == "select":
        select = Select(element)
        if len(select.options) > 0:
            random_index = random.randint(0, len(select.options)-1)
            actions.append(lambda el=element, idx=random_index: (
                log(f"select option at index: {idx}", el), 
                Select(el).select_by_index(idx)
            ))
    
    # Special action for links to log as link clicks
    elif tag_name == "a":
        actions.append(lambda el=element: (log("click link", el), el.click()))
    

    return actions

 
def select_action(possible_actions):
    """
    Returns a randomly selected element from a list 

    """
    if not possible_actions:
        return None
    
    # Basic random selection
    if random.random() < 0.7:  # 70% of the time use random selection
        selected_action_id = int(random.randint(0, len(possible_actions)-1))
        return possible_actions[selected_action_id]
    
    # Weighted selection based on action type - prioritize text inputs and buttons
    # This helps with better exploration of form interactions
    else:
        weighted_actions = []
        for action in possible_actions:
            action_str = str(action)
            if "input text" in action_str or "textarea" in action_str:
                # Higher weight for text inputs
                weighted_actions.extend([action] * 3)
            elif "select option" in action_str:
                # Higher weight for dropdowns
                weighted_actions.extend([action] * 2)
            else:
                # Normal weight for other actions
                weighted_actions.append(action)
        
        selected_action_id = int(random.randint(0, len(weighted_actions)-1))
        return weighted_actions[selected_action_id]

    
def execute_action(action):
    """
    Executes an action on a given WebElement based on its type (e.g., click, input text, select a checkbox).

    """
    action()

    
def check_oracles(driver, seq, acc, skip_accessibility=False, skip_image_check=True):
    """
    Check oracles to detect problems in the application
    
    Parameters:
    - driver: WebDriver instance
    - seq: Current sequence number
    - acc: Action number in the sequence
    - skip_accessibility: If True, skip accessibility checks
    - skip_image_check: If True, skip checking for broken images
    """
    # Check for JavaScript errors in console
    js_errors = driver.execute_script("""
        return window.jsErrors || [];
    """)
    if js_errors:
        print(f"Oracle violation: JavaScript errors detected: {js_errors}")
    
    # Check for HTTP error codes in the current page
    if "404" in driver.title or "500" in driver.title or "Error" in driver.title:
        print(f"Oracle violation: Error page detected: {driver.title}")
    
    # Check for visible error messages
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert, [role='alert']")
    for error in error_elements:
        if error.is_displayed():
            print(f"Oracle violation: Error message displayed: {error.text}")
    
    # Simple and fast check for broken images - skip by default for performance
    if not skip_image_check:
        # Use a single JavaScript call to check all images at once
        broken_images = driver.execute_script("""
            const images = document.getElementsByTagName('img');
            const brokenImages = [];
            
            for (let i = 0; i < images.length; i++) {
                const img = images[i];
                if (img.complete && 
                    typeof img.naturalWidth !== 'undefined' && 
                    img.naturalWidth === 0 &&
                    !img.classList.contains('icon') && 
                    !img.classList.contains('svg')) {
                    
                    brokenImages.push({
                        src: img.src || 'no-src',
                        alt: img.alt || 'no-alt'
                    });
                }
            }
            return brokenImages;
        """)
        
        # Report any broken images found
        for img in broken_images:
            print(f"Oracle violation: Broken image detected: {img['src']}")
    
    # Skip accessibility checks if requested
    if not skip_accessibility:
        # Initialize dictionary to track violations already found
        accessibility_violations = {}
        
        # Basic accessibility check - ensure interactive elements have accessible names
        interactive_elements = driver.find_elements(By.CSS_SELECTOR, "button, a, input, select")
        for el in interactive_elements:
            if el.is_displayed() and el.is_enabled():
                # Improve the detection of accessible names
                accessible_name = (
                    el.get_attribute("aria-label") or 
                    el.get_attribute("title") or 
                    el.get_attribute("alt") or  # For images in links
                    el.text or 
                    el.get_attribute("value")  # For buttons with value
                )
                
                # Also check child content for links
                if not accessible_name and el.tag_name.lower() == "a":
                    # Check if there's an image with alt text
                    img_children = el.find_elements(By.TAG_NAME, "img")
                    for img in img_children:
                        alt_text = img.get_attribute("alt")
                        if alt_text:
                            accessible_name = alt_text
                            break
                
                # For inputs, also consider the placeholder as accessible name
                if el.tag_name.lower() == "input":
                    accessible_name = accessible_name or el.get_attribute("placeholder")
                
                # Skip some known elements that generate false positives
                if not accessible_name and el.tag_name.lower() not in ["input"]:
                    # Get unique identifier for the element
                    element_id = f"{el.tag_name}:{el.get_attribute('id') or el.get_attribute('class') or 'unknown'}"
                    
                    # Record the violation only if we haven't seen it in this session
                    if element_id not in accessibility_violations:
                        accessibility_violations[element_id] = True
                        print(f"Oracle violation: Interactive element without accessible name: {el.tag_name}")
    
    print(f"Oracle check after action {acc} in sequence {seq}")
   
# To collect testing statistics
test_statistics = {
    'actions_executed': 0,
    'errors_encountered': 0,
    'unique_urls_visited': set(),
    'element_types_interacted': {},
    'start_time': None,
    'end_time': None
}

def testar(url, num_runs, length_sequence, filter_elements, preparations, skip_accessibility=False, skip_image_check=False):
    """
    Automated scriptless testing of a web application by executing sequences of actions on the System Under Test (SUT).
    
    Parameters:
    - url: URL of the web application to test
    - num_runs: Number of test executions
    - length_sequence: Length of each test sequence
    - filter_elements: Functions to filter elements not to test
    - preparations: Functions to prepare the initial state (e.g. login)
    - skip_accessibility: If True, skip accessibility checks
    - skip_image_check: If True, skip checking for broken images (default: True for better performance)
    """
    # Reset statistics and set start time
    test_statistics['actions_executed'] = 0
    test_statistics['errors_encountered'] = 0
    test_statistics['unique_urls_visited'] = set()
    test_statistics['element_types_interacted'] = {}
    test_statistics['start_time'] = datetime.now()
    
    # Outer loop, that iterates through the number of test runs specified
    for run_cnt in range(1, num_runs+1):
        # Start the SUT and get the driver
        driver = start_SUT_and_get_driver(url, preparations)
        
        print(f"Starting test sequence number {run_cnt} of {num_runs}")
        
        # Track current URL
        test_statistics['unique_urls_visited'].add(driver.current_url)
        
        # Inner loop that executes the test sequence with the specified number of actions (length_sequence)
        for acc_cnt in range(1, length_sequence+1):
            try:
                #derive the actionable widgets in the current state
                possible_actions = derive_actions(driver, filter_elements)
                
                #select actionable widgets
                selected_action = select_action(possible_actions)
                
                if selected_action:
                    #execute action
                    print(f"Action {acc_cnt} of {length_sequence}")
                    
                    # Get element type for statistics before executing action
                    action_str = str(selected_action)
                    if "click" in action_str:
                        action_type = "click"
                    elif "input text" in action_str:
                        action_type = "text_input"
                    elif "select option" in action_str:
                        action_type = "select"
                    else:
                        action_type = "other"
                    
                    test_statistics['element_types_interacted'][action_type] = test_statistics['element_types_interacted'].get(action_type, 0) + 1
                    test_statistics['actions_executed'] += 1
                    
                    execute_action(selected_action)
                    
                    # Record URL after action
                    test_statistics['unique_urls_visited'].add(driver.current_url)
                    
                    #check oracles
                    check_oracles(driver, run_cnt, acc_cnt, skip_accessibility, skip_image_check)
                else:
                    print("No actions available, skipping step")
            except Exception as e:
                print(f"Error during action execution: {e}")
                test_statistics['errors_encountered'] += 1
                
        # Close the SUT and browser
        driver.quit()
        
    # Print the results
    test_statistics['end_time'] = datetime.now()
    print_test_summary()

def print_test_summary():
    """
    Prints a summary of the test execution including:
    - Number of actions executed
    - Any errors encountered
    - Coverage of different pages/URLs
    - Duration of testing
    - Summary of element types interacted with
    """
    duration = test_statistics['end_time'] - test_statistics['start_time']
    
    print("\n" + "="*50)
    print("TEST EXECUTION SUMMARY")
    print("="*50)
    print(f"Total actions executed: {test_statistics['actions_executed']}")
    print(f"Errors encountered: {test_statistics['errors_encountered']}")
    print(f"Unique URLs visited: {len(test_statistics['unique_urls_visited'])}")
    print(f"URLs: {', '.join(list(test_statistics['unique_urls_visited'])[:5])}{'...' if len(test_statistics['unique_urls_visited']) > 5 else ''}")
    print(f"Element types interacted with:")
    for elem_type, count in test_statistics['element_types_interacted'].items():
        print(f"  - {elem_type}: {count} interactions")
    print(f"Total test duration: {duration}")
    print("="*50)


