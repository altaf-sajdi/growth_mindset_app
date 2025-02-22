import streamlit as st
import random
import requests
from datetime import datetime
import json

# Initialize session state for student info
if 'student_info' not in st.session_state:
    st.session_state.student_info = None

# Student Information Input Form
def show_student_form():
    # Add GIAIC Initiative header
    st.markdown("""
    <div style='text-align: center; background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: #1B6B93;'>GIAIC Initiative</h1>
        <p style='color: #4A4A4A;'>Governor Initiative for Artificial Intelligence & Computing</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("student_info_form"):
        st.markdown("### 👨‍🎓 Student Information Form")
        name = st.text_input("Full Name")
        student_id = st.text_input("Student ID (8 digits)", max_chars=8)
        class_time = st.selectbox(
            "Class Time",
            ["Friday 09:00 AM - 12:00 PM", "Other"]
        )
        if class_time == "Other":
            class_time = st.text_input("Enter your class time")
        
        submitted = st.form_submit_button("Start App")
        
        # Validate student ID
        is_valid_id = student_id.isdigit() and len(student_id) == 8
        
        if submitted:
            if not name:
                st.error("Please enter your name")
            if not is_valid_id:
                st.error("Student ID must be exactly 8 digits")
            if not class_time:
                st.error("Please select your class time")
            
            if name and is_valid_id and class_time:
                return {
                    "name": name,
                    "student_id": student_id,
                    "class_time": class_time
                }
        return None

# Main app logic
if not st.session_state.student_info:
    student_data = show_student_form()
    if student_data:
        st.session_state.student_info = student_data
        st.rerun()
else:
    # Streamlit UI
    st.markdown("""
    <div style='text-align: center; background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: #1B6B93;'>GIAIC Initiative</h1>
        <p style='color: #4A4A4A;'>Governor Initiative for Artificial Intelligence & Computing</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("🌱 Growth Mindset Challenge 2.0")

    # Add developer info in sidebar at top
    with st.sidebar:
        st.markdown("### 👨‍💻 Developer Information")
        st.markdown("""
        **Developer:** Altaf Hussain Sajdi  
        **Student ID:** 00280223  
        **Class:** Friday 09:00 AM - 12:00 PM  
        **Contact:** [📞 +92 300 3976568](tel:+923003976568)
        
        *Feel free to reach out for questions or suggestions!*
        """)
        st.markdown("---")
        
        # Add logout button in sidebar
        if st.button("Logout"):
            st.session_state.student_info = None
            st.rerun()

    # Display Student Information
    with st.expander("👨‍🎓 Student Information", expanded=True):
        st.markdown(f"""
        **Student Name:** {st.session_state.student_info['name']}  
        **Student ID:** {st.session_state.student_info['student_id']}  
        **Class Time:** {st.session_state.student_info['class_time']}
        """)

    # Initialize session state for favorites
    if 'favorite_quotes' not in st.session_state:
        st.session_state.favorite_quotes = []

    # Add this after imports
    QUOTES_DATABASE = [
        {
            'content': "Life is 10% what happens to you and 90% how you react to it.",
            'author': "Charles R. Swindoll",
            'tags': ['life', 'attitude']
        },
        {
            'content': "The future belongs to those who believe in the beauty of their dreams.",
            'author': "Eleanor Roosevelt",
            'tags': ['dreams', 'future']
        },
        # ... Add more quotes here ...
    ]

    # Generate 1000 themed quotes programmatically
    THEMES = {
        'success': [
            "Success is {action} when {condition}.",
            "The key to success is {key_point} and {secondary_point}.",
            "Your success is determined by {factor}.",
        ],
        'motivation': [
            "Never give up on {goal}, because {reason}.",
            "The only way to {achieve} is to {method}.",
            "Your potential is {description} when you {action}.",
        ],
        'growth': [
            "Growth happens when {condition}.",
            "The best way to grow is to {action}.",
            "Every challenge is {opportunity} to {grow}.",
        ],
        'wisdom': [
            "The wisest {subject} knows that {wisdom}.",
            "True wisdom comes from {source}.",
            "Learn to {action}, and you will {benefit}.",
        ]
    }

    VARIABLES = {
        'action': [
            "persisting", "learning", "adapting", "growing", "pushing forward",
            "taking action", "staying focused", "embracing change", "working hard",
            "staying committed"
        ],
        'condition': [
            "you stay consistent", "you believe in yourself", "you never give up",
            "you learn from mistakes", "you embrace challenges", "you stay positive",
            "you take responsibility", "you maintain focus", "you help others",
            "you remain patient"
        ],
        'key_point': [
            "persistence", "dedication", "hard work", "continuous learning",
            "positive mindset", "clear vision", "strong determination", "adaptability",
            "emotional intelligence", "strategic thinking"
        ],
        'secondary_point': [
            "unwavering focus", "consistent effort", "resilient attitude",
            "growth mindset", "creative thinking", "effective planning",
            "strong discipline", "passionate drive", "calculated risks",
            "collaborative spirit"
        ],
        # Add more variables as needed
    }

    def generate_quote(theme, template):
        """Generate a quote using template and random variables."""
        quote = template
        for var in VARIABLES:
            if "{" + var + "}" in quote:
                quote = quote.replace("{" + var + "}", random.choice(VARIABLES[var]))
        return {
            'content': quote,
            'author': "Growth Mindset AI",
            'tags': [theme, 'generated']
        }

    # Generate 1000 quotes
    for _ in range(1000):
        theme = random.choice(list(THEMES.keys()))
        template = random.choice(THEMES[theme])
        QUOTES_DATABASE.append(generate_quote(theme, template))

    # Modify the get_quote function
    @st.cache_data(ttl=3600)  # Cache quotes for 1 hour
    def get_quote(category=None):
        # Try API first
        try:
            base_url = "https://api.quotable.io/random"
            if category:
                url = f"{base_url}?tags={category}"
            else:
                url = base_url
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'content': data['content'],
                    'author': data['author'],
                    'tags': data.get('tags', [])
                }
        except Exception:
            pass
        
        # Use local database as fallback or if category specified
        filtered_quotes = QUOTES_DATABASE
        if category and category != 'random':
            filtered_quotes = [q for q in QUOTES_DATABASE if category in q.get('tags', [])]
        
        # Return random quote from filtered quotes or any quote if none match
        return random.choice(filtered_quotes if filtered_quotes else QUOTES_DATABASE)

    # Add quote source indicator
    def get_quote_source(quote_data):
        if quote_data.get('author') == "Growth Mindset AI":
            return "🤖 AI Generated"
        elif 'tags' in quote_data:
            return "📚 Quote Database"
        return "⭐ External API"

    # Daily challenges with progress tracking
    daily_challenges = [
        "Write down three things you learned today.",
        "Try something new and reflect on your experience.",
        "Teach a concept you recently learned to someone else.",
        "Identify a past failure and note what you learned from it.",
        "Practice positive self-talk throughout the day."
    ]

    # Enhanced quiz questions with explanations
    quiz_questions = [
        {
            "question": "Do you believe intelligence can be developed?",
            "options": ["Yes", "No"],
            "answer": "Yes",
            "explanation": "Research shows that intelligence can grow through dedication and learning."
        },
        {
            "question": "How do you react to failure?",
            "options": ["Learn from it", "Give up"],
            "answer": "Learn from it",
            "explanation": "Failures are opportunities for growth and learning."
        },
        {
            "question": "What do you do when you face a difficult task?",
            "options": ["Keep trying", "Avoid it"],
            "answer": "Keep trying",
            "explanation": "Persistence is key to developing new skills."
        },
        {
            "question": "When you see others succeed, how do you feel?",
            "options": ["Inspired", "Threatened"],
            "answer": "Inspired",
            "explanation": "Others' success can motivate and teach us valuable lessons."
        },
        {
            "question": "What's your view on challenges?",
            "options": ["Opportunities to grow", "Things to avoid"],
            "answer": "Opportunities to grow",
            "explanation": "Challenges help us develop new capabilities and strengths."
        },
        {
            "question": "How do you view criticism?",
            "options": ["Valuable feedback", "Personal attacks"],
            "answer": "Valuable feedback",
            "explanation": "Constructive criticism helps us identify areas for improvement."
        },
        {
            "question": "What's your approach to learning new skills?",
            "options": ["Practice regularly", "Give up if not naturally good"],
            "answer": "Practice regularly",
            "explanation": "Skills develop through consistent practice and effort."
        },
        {
            "question": "How do you view mistakes?",
            "options": ["Learning opportunities", "Signs of inadequacy"],
            "answer": "Learning opportunities",
            "explanation": "Mistakes are natural parts of the learning process."
        },
        {
            "question": "What's your belief about talent?",
            "options": ["Can be developed", "Fixed at birth"],
            "answer": "Can be developed",
            "explanation": "Talents can be cultivated through dedication and practice."
        },
        {
            "question": "How do you approach feedback?",
            "options": ["Seek it actively", "Avoid it"],
            "answer": "Seek it actively",
            "explanation": "Regular feedback accelerates growth and learning."
        },
        {
            "question": "What's your view on effort?",
            "options": ["Path to mastery", "Sign of weakness"],
            "answer": "Path to mastery",
            "explanation": "Effort is the key to developing expertise."
        },
        {
            "question": "How do you handle setbacks?",
            "options": ["Persist and adjust", "Give up"],
            "answer": "Persist and adjust",
            "explanation": "Setbacks are opportunities to adjust strategies and grow stronger."
        },
        {
            "question": "What's your approach to new challenges?",
            "options": ["Embrace them", "Stick to what's familiar"],
            "answer": "Embrace them",
            "explanation": "Embracing challenges leads to growth and new opportunities."
        },
        {
            "question": "How do you view your abilities?",
            "options": ["Can improve with effort", "Fixed traits"],
            "answer": "Can improve with effort",
            "explanation": "Abilities can be developed through dedication and practice."
        },
        {
            "question": "What's your reaction to obstacles?",
            "options": ["Find ways around them", "Give up"],
            "answer": "Find ways around them",
            "explanation": "Obstacles are opportunities to develop creative solutions."
        },
        {
            "question": "How do you approach difficult problems?",
            "options": ["Break them down", "Avoid them"],
            "answer": "Break them down",
            "explanation": "Complex problems become manageable when broken into smaller parts."
        },
        {
            "question": "What's your view on practice?",
            "options": ["Essential for growth", "Unnecessary if talented"],
            "answer": "Essential for growth",
            "explanation": "Deliberate practice is crucial for skill development."
        },
        {
            "question": "How do you view success of others?",
            "options": ["Source of learning", "Threat to self-worth"],
            "answer": "Source of learning",
            "explanation": "Others' success can provide valuable insights and inspiration."
        },
        {
            "question": "What's your approach to learning from others?",
            "options": ["Actively seek mentorship", "Prefer to work alone"],
            "answer": "Actively seek mentorship",
            "explanation": "Mentorship and collaboration accelerate personal growth."
        },
        {
            "question": "How do you view your potential?",
            "options": ["Unlimited with effort", "Fixed and predetermined"],
            "answer": "Unlimited with effort",
            "explanation": "Your potential grows as you invest effort in development."
        },
        {
            "question": "What role does persistence play in success?",
            "options": ["Critical", "Optional"],
            "answer": "Critical",
            "explanation": "Persistence is essential for overcoming challenges and achieving goals."
        },
        {
            "question": "How do you approach skill development?",
            "options": ["Continuous improvement", "Natural ability only"],
            "answer": "Continuous improvement",
            "explanation": "Skills can always be improved through dedicated practice."
        },
        {
            "question": "What's your view on brain plasticity?",
            "options": ["Brain can grow", "Brain is fixed"],
            "answer": "Brain can grow",
            "explanation": "Science shows our brains can form new connections throughout life."
        }
    ]

    # Initialize session state
    if 'completed_challenges' not in st.session_state:
        st.session_state.completed_challenges = set()
    if 'daily_streak' not in st.session_state:
        st.session_state.daily_streak = 0

    # Streamlit UI
    st.write("Welcome! Develop a growth mindset through daily challenges, quizzes, and reflections.")

    # Introduction Section
    with st.expander("ℹ️ What is a Growth Mindset?"):
        st.write("A growth mindset is the belief that abilities can be developed through hard work, dedication, and learning from mistakes.")
        st.write("• Embrace challenges\n• Learn from criticism\n• Find inspiration in others' success")

    # Daily Challenge Section
    st.header("📅 Today's Challenge")
    today_challenge = random.choice(daily_challenges)
    st.write(today_challenge)

    if st.button("Mark as Complete"):
        challenge_date = datetime.now().strftime("%Y-%m-%d")
        if challenge_date not in st.session_state.completed_challenges:
            st.session_state.completed_challenges.add(challenge_date)
            st.session_state.daily_streak += 1
            st.success(f"Challenge completed! Current streak: {st.session_state.daily_streak} days")
        else:
            st.info("You've already completed today's challenge!")

    # Enhanced Quiz Section
    st.header("🧠 Growth Mindset Quiz")
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = []

    def reset_quiz():
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.quiz_answers = []

    if not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        progress = st.session_state.current_question / len(quiz_questions)
        st.progress(progress)
        st.write(f"Question {st.session_state.current_question + 1} of {len(quiz_questions)}")
        
        q = quiz_questions[st.session_state.current_question]
        user_answer = st.radio(q["question"], q["options"], key=f"quiz_{st.session_state.current_question}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Next Question"):
                st.session_state.quiz_answers.append({
                    'question': q["question"],
                    'user_answer': user_answer,
                    'correct_answer': q["answer"],
                    'explanation': q["explanation"]
                })
                if st.session_state.current_question < len(quiz_questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    # Quiz completed
                    correct_answers = sum(1 for a in st.session_state.quiz_answers if a['user_answer'] == a['correct_answer'])
                    percentage = (correct_answers / len(quiz_questions)) * 100
                    
                    st.success(f"Quiz completed! Your score: {correct_answers}/{len(quiz_questions)} ({percentage:.0f}%)")
                    
                    # Show detailed results
                    st.subheader("Detailed Results")
                    for idx, answer in enumerate(st.session_state.quiz_answers, 1):
                        with st.expander(f"Question {idx}: {answer['question']}"):
                            if answer['user_answer'] == answer['correct_answer']:
                                st.success(f"✅ Your answer: {answer['user_answer']}")
                            else:
                                st.error(f"❌ Your answer: {answer['user_answer']}")
                                st.info(f"Correct answer: {answer['correct_answer']}")
                            st.write(f"**Explanation:** {answer['explanation']}")
                    
                    # Growth mindset assessment based on score
                    if percentage >= 80:
                        st.success("🌟 Strong Growth Mindset! You understand that abilities can be developed through dedication and hard work!")
                    elif percentage >= 60:
                        st.info("🌱 Developing Growth Mindset! You're on the right track, but there's room for growth.")
                    else:
                        st.warning("💡 Growth Opportunity! Consider embracing more growth-oriented perspectives.")
                    
                    if st.button("Retake Quiz"):
                        reset_quiz()
                        st.rerun()

    # User Input Section with Progress Tracking
    st.header("🎯 Learning Goals")
    user_goal = st.text_input("What skill or concept do you want to improve?")
    target_date = st.date_input("Target completion date")

    if st.button("Save Goal"):
        if user_goal and target_date:
            st.success(f"Goal set: {user_goal}")
            st.write(f"Target completion date: {target_date}")
            
            # Progress tracking
            progress = st.slider("Track your progress (0-100%)", 0, 100, 0)
            st.progress(progress / 100)
            if progress == 100:
                st.balloons()

    # Update the quote categories to match our THEMES
    quote_categories = list(THEMES.keys())  # ['success', 'motivation', 'growth', 'wisdom']

    # Enhanced Motivational Quote Section
    st.header("🌟 Daily Motivation")

    # Quote category selector
    selected_category = st.selectbox(
        "Choose quote category",
        ['random'] + quote_categories,
        help="Select a category for your motivational quote"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        quote_data = get_quote(selected_category if selected_category != 'random' else None)
        quote_text = quote_data['content']
        quote_author = quote_data['author']
        
        # Display quote with author and source
        st.markdown(f">>> *{quote_text}*")
        st.markdown(f"— **{quote_author}** ({get_quote_source(quote_data)})")
        
        # Tags display
        if quote_data.get('tags'):
            st.markdown("Tags: " + " ".join([f"`{tag}`" for tag in quote_data['tags']]))

    with col2:
        # Favorite button
        if st.button("❤️ Save Quote"):
            if quote_text not in [q['quote'] for q in st.session_state.favorite_quotes]:
                st.session_state.favorite_quotes.append({
                    'quote': quote_text,
                    'author': quote_author,
                    'date_saved': datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Quote saved to favorites!")
            else:
                st.info("Quote already in favorites!")

        # Share options
        st.markdown("**Share:**")
        tweet_text = f'"{quote_text}" - {quote_author}'
        tweet_url = f"https://twitter.com/intent/tweet?text={requests.utils.quote(tweet_text)}"
        st.markdown(f"[Tweet 🐦]({tweet_url})")

    # Show favorite quotes in expander
    with st.expander("📚 Your Favorite Quotes"):
        if st.session_state.favorite_quotes:
            for idx, fav in enumerate(st.session_state.favorite_quotes):
                st.markdown(f"*{fav['quote']}*")
                st.markdown(f"— **{fav['author']}**")
                st.caption(f"Saved on: {fav['date_saved']}")
                if st.button("Remove", key=f"remove_{idx}"):
                    st.session_state.favorite_quotes.pop(idx)
                    st.rerun()
                st.markdown("---")
        else:
            st.info("No favorite quotes yet. Save some quotes to see them here!")

    # Daily reflection
    with st.expander("📝 Quote Reflection"):
        st.write("Take a moment to reflect on today's quote:")
        reflection = st.text_area("What does this quote mean to you?")
        if st.button("Save Reflection"):
            if reflection:
                st.success("Reflection saved!")
                # Here you could add code to permanently save reflections if needed
                st.balloons()

    # Add quote statistics
    with st.expander("📊 Quote Statistics"):
        total_quotes = len(QUOTES_DATABASE)
        categories = {}
        for quote in QUOTES_DATABASE:
            for tag in quote.get('tags', []):
                categories[tag] = categories.get(tag, 0) + 1
        
        st.write(f"Total Quotes Available: {total_quotes}")
        st.write("Quotes by Category:")
        for category, count in categories.items():
            st.write(f"- {category}: {count}")
