import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY", "").strip()

# Initialize OpenAI client if key is present
client = None
if api_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")

SYSTEM_PROMPT = """You are SmartCampus AI, a virtual student assistant for SmartCampus AI.
You help students with academic counseling, course registrations, library tracking, campus locations, exam schedules, and attendance guidance.
Keep your answers brief, encouraging, professional, and directly related to college campus life.
If a user asks about their specific attendance or timetable, guide them to check the respective page in the navigation menu.
"""

def query_local_fallback(prompt: str) -> str:
    """
    A smart local rule-based fallback bot that resolves common student inquiries
    when the OpenAI API key is missing, invalid, or offline.
    """
    p = prompt.lower()
    
    # WiFi / IT Support
    if "wifi" in p or "internet" in p or "connect" in p or "network" in p:
        return (
            "📶 **Campus Wi-Fi Information**:\n\n"
            "To connect to the campus internet:\n"
            "1. Connect to the **'SmartCampus_Secure'** network.\n"
            "2. Open a browser and log in using your **Student ID** and your portal password.\n"
            "3. For tech issues, contact the IT helpdesk in Building C, Room 104, or email `it.support@smartcampus.edu`."
        )
        
    # Library
    elif "library" in p or "book" in p or "study" in p or "reading" in p:
        return (
            "📚 **Central Library Information**:\n\n"
            "- **Location**: Building B, 2nd & 3rd Floor.\n"
            "- **Timings**: Weekdays (8:00 AM – 10:00 PM), Weekends (9:00 AM – 5:00 PM).\n"
            "- **Borrowing Policy**: Up to 5 books for 14 days. Renewals can be requested online via the library portal.\n"
            "- **Facilities**: High-speed quiet study zones, computers, and group discussion rooms (reserve online)."
        )
        
    # Attendance Policy
    elif "attendance" in p or "present" in p or "absent" in p or "75" in p or "minimum" in p:
        return (
            "📊 **Attendance Policy**:\n\n"
            "- The university mandates a **minimum of 75% attendance** in each course to qualify for the End Semester Examinations.\n"
            "- Shortfalls can result in academic probation or debarment from exams.\n"
            "- If you missed a class due to illness, submit a medical certificate to your Department Coordinator within 7 days."
        )
        
    # Canteen / Food
    elif "canteen" in p or "food" in p or "lunch" in p or "canteen menu" in p or "eat" in p:
        return (
            "🍔 **Campus Dining Options**:\n\n"
            "1. **Central Canteen** (Near Block A): Open 8:00 AM – 8:00 PM. Serving meals, sandwiches, beverages, and daily hot specials.\n"
            "2. **Tech Cafe** (IT Block): Open 9:00 AM – 6:00 PM. Perfect for coffee, bakery items, and quick snacks.\n"
            "3. **Health Bar** (Gymnasium): Fresh juices, salads, and high-protein bowls.\n\n"
            "*Tip: Today's special in the Central Canteen is Grilled Paneer Wrap / Chicken Teriyaki with Salad.*"
        )
        
    # Exams
    elif "exam" in p or "test" in p or "schedule" in p or "date" in p or "midterm" in p:
        return (
            "📝 **Examinations Information**:\n\n"
            "- **End Semester Exams**: Scheduled to begin on **August 3rd, 2026**.\n"
            "- **Midterm Exams**: Typically held halfway through the semester. Check your syllabus for subject-specific quiz calendars.\n"
            "- **Rules**: Bring your Student ID card. Smartwatches and mobile phones are strictly prohibited in the exam hall."
        )
        
    # Canteen location/maps/dean/contacts
    elif "dean" in p or "contact" in p or "office" in p or "admin" in p or "support" in p:
        return (
            "📞 **Key Contacts & Offices**:\n\n"
            "- **Student Affairs Office**: Building A, Room 102 (Email: `student.affairs@smartcampus.edu` | Phone: ext. 420)\n"
            "- **Dean's Office**: Building A, Room 201 (Office hours: 2:00 PM – 4:00 PM)\n"
            "- **Medical Center**: Ground floor of the Gym Block. Open 24/7 for first-aid and emergencies."
        )

    # Timetable / Class
    elif "timetable" in p or "class" in p or "schedule" in p or "courses" in p:
        return (
            "🗓️ **Class Schedule Guide**:\n\n"
            "You can review your personalized daily classes in the **Timetable** section of this app.\n"
            "For default schedules: core classes usually start at 9:00 AM and run until 4:00 PM. Please check your specific department for lab slot listings."
        )
        
    # Canteen / Hostels / Sports
    elif "sport" in p or "gym" in p or "hostel" in p or "recreation" in p:
        return (
            "🏃‍♂️ **Sports & Recreation**:\n\n"
            "- **Gymnasium**: Free for registered students. Located in the Sports Complex. Open 6:00 AM – 9:00 PM.\n"
            "- **Facilities**: Basketball courts, tennis courts, and an indoor swimming pool.\n"
            "- **Hostel Warden Office**: Located in hostel block D. For housing questions, email `housing@smartcampus.edu`."
        )

    # General campus welcome response
    else:
        return (
            "🤖 **SmartCampus AI Helper (Offline Fallback Mode)**\n\n"
            "I am running in local fallback mode because the `OPENAI_API_KEY` environment variable is not configured or is invalid.\n\n"
            "I can still help you with standard campus information! Try asking me about:\n"
            "- **Library hours and locations**\n"
            "- **Campus Wi-Fi configuration**\n"
            "- **Canteen menu and operating times**\n"
            "- **Attendance policies and rules (75% rule)**\n"
            "- **Exam start dates and guidelines**\n"
            "- **Important campus email contacts**\n\n"
            "*To enable smart LLM conversations, please add a valid OpenAI API Key to your `.env` file and restart the application.*"
        )

def generate_response(prompt: str, chat_history: list = None) -> str:
    """
    Generate response from OpenAI API. If API key is not configured or 
    fails, switches to the local campus assistant logic.
    """
    if not client:
        return query_local_fallback(prompt)

    try:
        # Build messages including conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add history if provided (limit to last 6 messages to keep context short and fast)
        if chat_history:
            for item in chat_history[-6:]:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
                
        # Append current user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Call OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=350
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API Error: {e}. Falling back to rule-based engine.")
        # Fallback to local rule engine if API fails
        fallback_res = query_local_fallback(prompt)
        # Prefix explanation if API failed
        if "🤖 **SmartCampus AI Helper" not in fallback_res:
            return f"*(Note: Encountered OpenAI API call error. Displaying local helper answer.)*\n\n" + fallback_res
        return fallback_res
