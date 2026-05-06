
import requests
import csv
import time
import subprocess
import sys

# Function to install requests library
def install_requests():
    try:
        import requests
    except ImportError:
        print("Requests library not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    finally:
        import requests  # Import after installation

install_requests()

# Function to load vendor data from a CSV file
def load_vendor_data(file_path, vendor_type):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if vendor_type == "printing":
                    data.append({
                        "name": row["name"],
                        "address": row["address"],
                        "contact": row["contact"],
                        "services": row["services"]
                    })
                else:
                    data.append({
                        "name": row["name"],
                        "contact": row["contact"],
                        "address": row["address"],
                        "average_price": row.get("average_price", "N/A")
                    })
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []
# class NLPEngine:

#     def detect_intent(self, text):
#             text = text.lower()

#         if any(word in text for word in ["cheap", "low", "budget", "affordable"]):
#             print "low"
#         elif any(word in text for word in ["luxury", "premium", "grand"]):
#             print "high"
#         else:
#             print "medium"

#     def extract_event_type(self, text):
#         events = ["wedding", "birthday", "corporate", "party", "engagement"]
#         for e in events:
#             if e in text.lower():
#                     return e
#         print "general"

#         def extract_location(self, text):
#         # simple extraction (can be upgraded)
#             words = text.lower().split()
#             return words[-1]  # last word as location

# # # Function to get event enhancement suggestions from GPT-4V API
def get_event_suggestions(event_type):
    GPT4V_KEY = "9776e4337cbf451baffbff9a2b452bc3"
    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4V_KEY
    }

    # GPT4V_ENDPOINT = "https://tabsonsnct.openai.azure.com/openai/deployments/tabsonsai/chat/completions?api-version=2024-02-15-preview"
    GPT4V_ENDPOINT = "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"

    prompt = f"Provide unique and creative ideas to enhance a {event_type} event. Include activities, themes, and other suggestions."
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        suggestions = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        return suggestions
    except Exception as e:
        return """Try adding live music, themed decoration, and interactive games for guests.
                Ask the staff to be much more attentive
                Add props for guests to take pictures
                Add a photo booth"""
        

# ShubhMilan AI Model
class ShubhMilanAI:
    def __init__(self, venues, decorations, printing, catering):
        self.venues = venues
        self.decorations = decorations
        self.printing = printing
        self.catering = catering

    def greet_user(self):
        print("Hello! I am ShubhMilan, your event planning assistant.")
        time.sleep(2)
        print("I am here to help you plan your event within your budget by suggesting venues, food, decorations, printing, and more.")

    def get_event_details(self):
        
        event_type = input("What type of event are you planning (e.g., wedding, birthday, corporate)? ").strip().lower()
        location = input("Where do you want to organize the event? ").strip().lower()
        
        while True:
            try:
                budget = float(input("What is your budget for the event? "))
                if budget <= 0:
                    raise ValueError("Budget must be a positive number.")
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                attendees = int(input("How many people are you expecting to attend? "))
                if attendees <= 0:
                    raise ValueError("Number of attendees must be a positive integer.")
                break
            except ValueError as e:
                print(e)

        return event_type, location, budget, attendees

    def suggest_event_plan(self, event_type, location, budget, attendees):
        print("\nBased on your inputs, here is a plan for your event:")
        
        # Calculate the budget for each category based on a predefined allocation
        venue_budget = budget * 0.4
        catering_budget = budget * 0.3
        decoration_budget = budget * 0.2
        printing_budget = budget * 0.1

        self.suggest_venues(location, venue_budget)
        self.suggest_decorations(location, decoration_budget)
        self.suggest_catering(location, catering_budget)
        self.suggest_printing(location, printing_budget)

        # Get additional suggestions from the API
        suggestions = get_event_suggestions(event_type)
        print("\nHere are some suggestions to make your event even better:")
        print(suggestions)
        return """Try adding live music, themed decoration, and interactive games for guests.
                Ask the staff to be much more attentive
                Add props for guests to take pictures
                Add a photo booth"""

    def suggest_venues(self, location, budget):
        print("\nSuggested Venues:")
        filtered_venues = [venue for venue in self.venues if location in venue["address"].lower() and self.price_in_budget(venue["average_price"], budget)]
        if filtered_venues:
            for venue in filtered_venues:
                print(f"• {venue['name']}\n  - Price Range: {venue['average_price']}\n  - Address: {venue['address']}\n  - Contact: {venue['contact']}\n")
        else:
            print(f"No venues available within your budget in {location}.")

    def suggest_decorations(self, location, budget):
        print("\nSuggested Decoration Vendors:")
        filtered_decorations = [decor for decor in self.decorations if self.price_in_budget(decor["average_price"], budget)]
        if filtered_decorations:
            for decor in filtered_decorations:
                print(f"• {decor['name']}\n  - Price Range: {decor['average_price']}\n  - Address: {decor['address']}\n  - Contact: {decor['contact']}\n")
        else:
            print("No decoration vendors available within your budget.")

    def suggest_catering(self, location, budget):
        print("\nSuggested Catering Vendors:")
        filtered_catering = [caterer for caterer in self.catering if self.price_in_budget(caterer["average_price"], budget)]
        if filtered_catering:
            for caterer in filtered_catering:
                print(f"• {caterer['name']}\n  - Price Range: {caterer['average_price']}\n  - Address: {caterer['address']}\n  - Contact: {caterer['contact']}\n")
        else:
            print("No catering vendors available within your budget.")

    def suggest_printing(self, location, budget):
        print("\nSuggested Printing Vendors:")
        filtered_printing = [printer for printer in self.printing if location in printer["address"].lower()]
        if filtered_printing:
            for printer in filtered_printing:
                print(f"• {printer['name']}\n  - Services: {printer['services']}\n  - Address: {printer['address']}\n  - Contact: {printer['contact']}\n")
        else:
            print(f"No printing vendors found in {location}.")

    def price_in_budget(self, price_range, budget):
        if price_range == "N/A":
            return False
        try:
            if "-" in price_range:
                low, high = map(int, price_range.split("-"))
                return low <= budget <= high
            else:
                return int(price_range) <= budget
        except ValueError:
            return False

# Main function to run the AI
def run_shubhmilan():
    # Load vendor data from CSV files
    venues = load_vendor_data('venues.csv', "venue")
    decorations = load_vendor_data('decoration_vendors.csv', "decoration")
    printing = load_vendor_data('printing_vendors.csv', "printing")
    catering = load_vendor_data('catering_vendors.csv', "catering")

    if venues and decorations and printing and catering:
        # Create an instance of ShubhMilan
        shubhmilan = ShubhMilanAI(venues, decorations, printing, catering)

        # Greet the user and ask for details
        shubhmilan.greet_user()
        event_type, location, budget, attendees = shubhmilan.get_event_details()

        # Suggest a plan based on the inputs
        shubhmilan.suggest_event_plan(event_type, location, budget, attendees)
    else:
        print("Unable to load vendor data.")

# Run the AI model
run_shubhmilan()

# import requests
# import csv
# import time
# import subprocess
# import sys

# # Function to install requests library
# def install_requests():
#     try:
#         import requests
#     except ImportError:
#         print("Requests library not found. Installing...")
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
#     finally:
#         import requests

# install_requests()

# # Function to load vendor data from a CSV file
# def load_vendor_data(file_path, vendor_type):
#     data = []
#     try:
#         with open(file_path, mode='r', encoding='utf-8') as file:
#             csv_reader = csv.DictReader(file)
#             for row in csv_reader:
#                 if vendor_type == "printing":
#                     data.append({
#                         "name": row["name"],
#                         "address": row["address"],
#                         "contact": row["contact"],
#                         "services": row["services"]
#                     })
#                 else:
#                     data.append({
#                         "name": row["name"],
#                         "contact": row["contact"],
#                         "address": row["address"],
#                         "average_price": row.get("average_price", "N/A")
#                     })
#         return data
#     except Exception as e:
#         print(f"Error loading data: {e}")
#         return []

# # ✅ FIXED FUNCTION
# def get_event_suggestions(event_type):
#     API_KEY = "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"  # 🔴 Put your NEW key here

#     endpoint = "https://api.openai.com/v1/chat/completions"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     prompt = f"Provide unique and creative ideas to enhance a {event_type} event. Include activities, themes, and suggestions."

#     data = {
#         "model": "gpt-4.1-mini",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ],
#         "max_tokens": 150
#     }

#     try:
#         response = requests.post(endpoint, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         return result["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         print(f"Error getting suggestions: {e}")
#         return "Sorry, I couldn't fetch suggestions at this time."

# # ShubhMilan AI Model
# class ShubhMilanAI:
#     def __init__(self, venues, decorations, printing, catering):
#         self.venues = venues
#         self.decorations = decorations
#         self.printing = printing
#         self.catering = catering

#     def greet_user(self):
#         print("Hello! I am ShubhMilan, your event planning assistant.")
#         time.sleep(1)
#         print("I will help you plan your event within your budget.")

#     def get_event_details(self):
#         event_type = input("Event type (wedding, birthday, corporate): ").strip().lower()
#         location = input("Location: ").strip().lower()

#         while True:
#             try:
#                 budget = float(input("Budget: "))
#                 if budget <= 0:
#                     raise ValueError
#                 break
#             except:
#                 print("Enter valid budget")

#         while True:
#             try:
#                 attendees = int(input("Number of attendees: "))
#                 if attendees <= 0:
#                     raise ValueError
#                 break
#             except:
#                 print("Enter valid number")

#         return event_type, location, budget, attendees

#     def suggest_event_plan(self, event_type, location, budget, attendees):
#         print("\n--- EVENT PLAN ---")

#         venue_budget = budget * 0.4
#         catering_budget = budget * 0.3
#         decoration_budget = budget * 0.2
#         printing_budget = budget * 0.1

#         self.suggest_venues(location, venue_budget)
#         self.suggest_decorations(location, decoration_budget)
#         self.suggest_catering(location, catering_budget)
#         self.suggest_printing(location)

#         print("\n--- AI Suggestions ---")
#         suggestions = get_event_suggestions(event_type)
#         print(suggestions)

#     def suggest_venues(self, location, budget):
#         print("\nVenues:")
#         filtered = [v for v in self.venues if location in v["address"].lower() and self.price_in_budget(v["average_price"], budget)]
#         if filtered:
#             for v in filtered:
#                 print(f"{v['name']} | {v['average_price']} | {v['address']} | {v['contact']}")
#         else:
#             print("No venues found")

#     def suggest_decorations(self, location, budget):
#         print("\nDecorations:")
#         filtered = [d for d in self.decorations if self.price_in_budget(d["average_price"], budget)]
#         if filtered:
#             for d in filtered:
#                 print(f"{d['name']} | {d['average_price']} | {d['address']} | {d['contact']}")
#         else:
#             print("No decorators found")

#     def suggest_catering(self, location, budget):
#         print("\nCatering:")
#         filtered = [c for c in self.catering if self.price_in_budget(c["average_price"], budget)]
#         if filtered:
#             for c in filtered:
#                 print(f"{c['name']} | {c['average_price']} | {c['address']} | {c['contact']}")
#         else:
#             print("No caterers found")

#     def suggest_printing(self, location):
#         print("\nPrinting:")
#         filtered = [p for p in self.printing if location in p["address"].lower()]
#         if filtered:
#             for p in filtered:
#                 print(f"{p['name']} | {p['services']} | {p['address']} | {p['contact']}")
#         else:
#             print("No printers found")

#     def price_in_budget(self, price_range, budget):
#         if price_range == "N/A":
#             return False
#         try:
#             if "-" in price_range:
#                 low, high = map(int, price_range.split("-"))
#                 return low <= budget <= high
#             return int(price_range) <= budget
#         except:
#             return False

# # Main runner
# def run_shubhmilan():
#     venues = load_vendor_data('venues.csv', "venue")
#     decorations = load_vendor_data('decoration_vendors.csv', "decoration")
#     printing = load_vendor_data('printing_vendors.csv', "printing")
#     catering = load_vendor_data('catering_vendors.csv', "catering")

#     if venues and decorations and printing and catering:
#         ai = ShubhMilanAI(venues, decorations, printing, catering)
#         ai.greet_user()
#         event_type, location, budget, attendees = ai.get_event_details()
#         ai.suggest_event_plan(event_type, location, budget, attendees)
#     else:
#         print("Error loading CSV files")

# run_shubhmilan()




# import requests
# import csv
# import time
# import subprocess
# import sys

# # Install requests if not available
# def install_requests():
#     try:
#         import requests
#     except ImportError:
#         print("Installing requests...")
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# install_requests()

# # Load CSV data
# def load_vendor_data(file_path, vendor_type):
#     data = []
#     try:
#         with open(file_path, mode='r', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if vendor_type == "printing":
#                     data.append({
#                         "name": row["name"],
#                         "address": row["address"],
#                         "contact": row["contact"],
#                         "services": row["services"]
#                     })
#                 else:
#                     data.append({
#                         "name": row["name"],
#                         "contact": row["contact"],
#                         "address": row["address"],
#                         "average_price": row.get("average_price", "N/A")
#                     })
#         return data
#     except Exception as e:
#         print("CSV Error:", e)
#         return []

# # ✅ FINAL FIXED API FUNCTION (handles 429 + retries)
# def get_event_suggestions(event_type):
#     API_KEY = "YOUR_NEW_API_KEY"   # 🔴 PUT NEW KEY HERE

#     url = "https://api.openai.com/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "gpt-4.1-mini",
#         "messages": [
#             {"role": "user", "content": f"Suggest creative ideas for a {event_type} event."}
#         ],
#         "max_tokens": 150
#     }

#     retries = 3

#     for i in range(retries):
#         try:
#             response = requests.post(url, headers=headers, json=payload)

#             if response.status_code == 429:
#                 print("⚠️ Rate limit hit. Retrying...")
#                 time.sleep(5)
#                 continue

#             response.raise_for_status()
#             return response.json()["choices"][0]["message"]["content"]

#         except requests.exceptions.RequestException as e:
#             print(f"Attempt {i+1} failed:", e)
#             time.sleep(3)

#     return "API limit reached. Try again later."

# # Main AI Class
# class ShubhMilanAI:
#     def __init__(self, venues, decorations, printing, catering):
#         self.venues = venues
#         self.decorations = decorations
#         self.printing = printing
#         self.catering = catering

#     def greet_user(self):
#         print("\nWelcome to ShubhMilan AI 🎉")
#         time.sleep(1)

#     def get_event_details(self):
#         event_type = input("Event type: ").lower()
#         location = input("Location: ").lower()

#         while True:
#             try:
#                 budget = float(input("Budget: "))
#                 if budget <= 0:
#                     raise ValueError
#                 break
#             except:
#                 print("Enter valid budget")

#         while True:
#             try:
#                 attendees = int(input("Attendees: "))
#                 if attendees <= 0:
#                     raise ValueError
#                 break
#             except:
#                 print("Enter valid number")

#         return event_type, location, budget, attendees

#     def suggest_event_plan(self, event_type, location, budget, attendees):
#         print("\n--- EVENT PLAN ---")

#         self.suggest_venues(location, budget * 0.4)
#         self.suggest_decorations(budget * 0.2)
#         self.suggest_catering(budget * 0.3)
#         self.suggest_printing(location)

#         print("\n--- AI Suggestions ---")
#         print(get_event_suggestions(event_type))

#     def suggest_venues(self, location, budget):
#         print("\nVenues:")
#         found = False
#         for v in self.venues:
#             if location in v["address"].lower() and self.price_ok(v["average_price"], budget):
#                 print(v["name"], "|", v["average_price"])
#                 found = True
#         if not found:
#             print("No venues found")

#     def suggest_decorations(self, budget):
#         print("\nDecorators:")
#         found = False
#         for d in self.decorations:
#             if self.price_ok(d["average_price"], budget):
#                 print(d["name"], "|", d["average_price"])
#                 found = True
#         if not found:
#             print("No decorators found")

#     def suggest_catering(self, budget):
#         print("\nCatering:")
#         found = False
#         for c in self.catering:
#             if self.price_ok(c["average_price"], budget):
#                 print(c["name"], "|", c["average_price"])
#                 found = True
#         if not found:
#             print("No caterers found")

#     def suggest_printing(self, location):
#         print("\nPrinting:")
#         found = False
#         for p in self.printing:
#             if location in p["address"].lower():
#                 print(p["name"], "|", p["services"])
#                 found = True
#         if not found:
#             print("No printers found")

#     def price_ok(self, price, budget):
#         if price == "N/A":
#             return False
#         try:
#             if "-" in price:
#                 low, high = map(int, price.split("-"))
#                 return low <= budget <= high
#             return int(price) <= budget
#         except:
#             return False

# # Runner
# def run():
#     venues = load_vendor_data("venues.csv", "venue")
#     decorations = load_vendor_data("decoration_vendors.csv", "decoration")
#     printing = load_vendor_data("printing_vendors.csv", "printing")
#     catering = load_vendor_data("catering_vendors.csv", "catering")

#     if not (venues and decorations and printing and catering):
#         print("Error loading data")
#         return

#     ai = ShubhMilanAI(venues, decorations, printing, catering)
#     ai.greet_user()
#     e, l, b, a = ai.get_event_details()
#     ai.suggest_event_plan(e, l, b, a)

# run()


# import requests
# import csv
# import time
# import re

# # ---------------- NLP ENGINE ---------------- #

# class NLPEngine:

#     def detect_intent(self, text):
#         text = text.lower()

#         if any(word in text for word in ["cheap", "low", "budget", "affordable"]):
#             return "low"
#         elif any(word in text for word in ["luxury", "premium", "grand"]):
#             return "high"
#         else:
#             return "medium"

#     def extract_event_type(self, text):
#         events = ["wedding", "birthday", "corporate", "party", "engagement"]
#         for e in events:
#             if e in text.lower():
#                 return e
#         return "general"

#     def extract_location(self, text):
#         # simple extraction (can be upgraded)
#         words = text.lower().split()
#         return words[-1]  # last word as location

# # ---------------- API FUNCTION ---------------- #

# def get_event_suggestions(event_type, budget_type):
#     API_KEY = "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"

#     url = "https://api.openai.com/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     prompt = f"""
#     Suggest creative ideas for a {event_type} event.
#     Budget level: {budget_type}.
#     Give practical, realistic suggestions.
#     """

#     payload = {
#         "model": "gpt-4.1-mini",
#         "messages": [{"role": "user", "content": prompt}],
#         "max_tokens": 200
#     }

#     for _ in range(3):
#         try:
#             r = requests.post(url, headers=headers, json=payload)

#             if r.status_code == 429:
#                 time.sleep(5)
#                 continue

#             r.raise_for_status()
#             return r.json()["choices"][0]["message"]["content"]

#         except Exception as e:
#             print("API error:", e)
#             time.sleep(2)

#     return "Try adding live music, themed decoration, and interactive games for guests."

# # ---------------- DATA LOADER ---------------- #

# def load_csv(file):
#     data = []
#     try:
#         with open(file, encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 data.append(row)
#     except:
#         print("Error loading", file)
#     return data

# # ---------------- MAIN AI ---------------- #

# class ShubhMilanNLP:

#     def __init__(self):
#         self.nlp = NLPEngine()
#         self.venues = load_csv("venues.csv")

#     def start(self):
#         print("\n🎉 Welcome to NLP-based ShubhMilan AI")

#         user_input = input("\nDescribe your event: ")
#         budget = float(input("Enter budget: "))

#         # NLP processing
#         event_type = self.nlp.extract_event_type(user_input)
#         location = self.nlp.extract_location(user_input)
#         budget_type = self.nlp.detect_intent(user_input)

#         print("\n🧠 NLP Analysis:")
#         print("Event:", event_type)
#         print("Location:", location)
#         print("Budget type:", budget_type)

#         self.suggest_venues(location, budget)

#         print("\n✨ AI Suggestions:")
#         print(get_event_suggestions(event_type, budget_type))

#     def suggest_venues(self, location, budget):
#         print("\n🏢 Suggested Venues:")

#         found = False
#         for v in self.venues:
#             if location in v["address"].lower():
#                 print(v["name"], "|", v.get("average_price", "N/A"))
#                 found = True

#         if not found:
#             print("No venues found")

# # ---------------- RUN ---------------- #

# app = ShubhMilanNLP()
# app.start()