from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import json
from datetime import datetime
import uuid
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
from flask import send_file
import sqlite3
# ================= ML MODEL (Learning Style Detection) =================

from sklearn.tree import DecisionTreeClassifier

# Training data (dummy but valid for demo)
X = [
    [1, 1, 1, 1],     # slow, practical, visual, deep
    [-1, -1, -1, -1], # fast, theory, reading, shallow
    [1, -1, 1, 0],
    [-1, 1, 0, 1] 
]

y = [
    "practical_slow",
    "theory_fast",
    "visual_balanced",
    "mixed"
]

ml_model = DecisionTreeClassifier()
ml_model.fit(X, y)


app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# -----------------------------
# Expanded Module Catalog (B.Tech relevant)
# All videos use YouTube watch?v= links (embed handled in frontend)
# -----------------------------
MODULE_CATALOG = {
   "cs_m101": {
    "module_id": "cs_m101",
    "title": "Python Programming (Beginner → Advanced)",
    "domain": "python",
    "skill_tag": "python",   # ✅ ADD THIS
    "difficulty": "beginner",
    "prerequisites": [],
    "estimated_hours": 12,
    "resources": [

    # ================= BEGINNER =================

    # --- Practical ---
    {
        "type": "video",
        "title": "Python Beginner Practical (English)",
        "url": "https://youtu.be/j_JuhAWlEaI?si=mo7tzmCEY3VxftM4",
        "level": "beginner",
        "format": "practical",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Python Beginner Practical (Telugu)",
        "url": "https://youtu.be/0c6JXSQKEP4?si=RSKgn6mTwIDJcOnx",
        "level": "beginner",
        "format": "practical",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Python Beginner Practical (Hindi)",
        "url": "https://youtu.be/ERCMXc8x7mc?si=HtrprOGuVkl6Ayar",
        "level": "beginner",
        "format": "practical",
        "language": "hindi"
    },

    # --- Board ---
    {
        "type": "video",
        "title": "Python Beginner Board (English)",
        "url": "https://youtu.be/j_JuhAWlEaI?si=yemF0ItxQ0dNAn_a",
        "level": "beginner",
        "format": "board",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Python Beginner Board (Telugu)",
        "url": "https://youtu.be/l1nmr3QeohI?si=rSKXIrkgkscSCeUc",
        "level": "beginner",
        "format": "board",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Python Beginner Board (Hindi)",
        "url": "https://youtu.be/b97WsOM9BYg?si=mgJgrP9g6WuPAHN8",
        "level": "beginner",
        "format": "board",
        "language": "hindi"
    },

    # ================= INTERMEDIATE =================

    # --- Practical ---
    {
        "type": "video",
        "title": "Python Intermediate Practical (English)",
        "url": "https://youtu.be/nLRL_NcnK-4?si=zv9shMSJ093gQMik",
        "level": "intermediate",
        "format": "practical",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Python Intermediate Practical (Telugu)",
        "url": "https://youtu.be/SkdrCkyq-pY?si=LsuRIy6Sc5nSnk77",
        "level": "intermediate",
        "format": "practical",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Python Intermediate Practical (Hindi)",
        "url": "https://youtu.be/fqF9M92jzUo?si=7gc65dCjnIZ_hRhW",
        "level": "intermediate",
        "format": "practical",
        "language": "hindi"
    },

    # --- Board ---
    {
        "type": "video",
        "title": "Python Intermediate Board (English)",
        "url": "https://youtu.be/oUho9ofP1PY?si=0-9fC9-99isVGpsN",
        "level": "intermediate",
        "format": "board",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Python Intermediate Board (Telugu)",
        "url": "https://youtu.be/MtzSYNHkgcg?si=gljU52tAj4C-WOnR",
        "level": "intermediate",
        "format": "board",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Python Intermediate Board (Hindi)",
        "url": "https://youtu.be/fqF9M92jzUo?si=mSfHHRIefOOtvAXO",
        "level": "intermediate",
        "format": "board",
        "language": "hindi"
    },

    # ================= ADVANCED =================

    {
        "type": "video",
        "title": "Python Advanced (Telugu)",
        "url": "https://youtube.com/playlist?list=PLbMVPNscUopRsjl_O6jce4apc1BoRYAYp&si=gB84W__0jqQwn955",
        "level": "advanced",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Python Advanced (English)",
        "url": "https://youtube.com/playlist?list=PLsyeobzWxl7omDoEYrrf3oXvXxa6MPgek&si=rFFmhaDI4GCZtD7O",
        "level": "advanced",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Python Advanced (Hindi)",
        "url": "https://youtube.com/playlist?list=PLjVLYmrlmjGcQfNj_SLlLV4Ytf39f8BF7&si=E-Ds1Wn9r0TAiNR8",
        "level": "advanced",
        "language": "hindi"
    }

],
    "learning_objectives": [
        "syntax",
        "loops",
        "functions",
        "oops",
        "advanced-concepts"
    ]
}
,
    
"cs_m105": {
    "module_id": "cs_m105",
    "title": "Java Programming (Beginner → Advanced)",
    "domain": "Java",
    "difficulty": "beginner",
    "skill_tag": "java",
    "prerequisites": [],
    "estimated_hours": 14,
    "resources": [

    # ------------------ BEGINNER ------------------
    {
        "title": "Java Beginner Board (English)",
        "url": "https://youtu.be/BGTx91t8q50",
        "level": "beginner",
        "format": "board",
        "language": "english"
    },
    {
        "title": "Java Beginner Practical (English)",
        "url": "https://youtu.be/xTtL8E4LzTQ",
        "level": "beginner",
        "format": "practical",
        "language": "english"
    },
    {
        "title": "Java Beginner Board (Telugu)",
        "url": "https://youtu.be/prfwlnq2vJY",
        "level": "beginner",
        "format": "board",
        "language": "telugu"
    },
    {
        "title": "Java Beginner Practical (Telugu)",
        "url": "https://youtu.be/wXfmWSGE2ok",
        "level": "beginner",
        "format": "practical",
        "language": "telugu"
    },
    {
        "title": "Java Beginner Board (Hindi)",
        "url": "https://youtu.be/ECT-ehj-q7s",
        "level": "beginner",
        "format": "board",
        "language": "hindi"
    },
    {
        "title": "Java Beginner Practical (Hindi)",
        "url": "https://youtu.be/NGFh1tn2Up4",
        "level": "beginner",
        "format": "practical",
        "language": "hindi"
    },

    # ------------------ INTERMEDIATE ------------------
    {
        "title": "Java Intermediate Practical (English)",
        "url": "https://www.youtube.com/live/vIXcT4hbR0U",
        "level": "intermediate",
        "format": "practical",
        "language": "english"
    },
    {
        "title": "Java Intermediate Board (English)",
        "url": "https://www.youtube.com/live/vIXcT4hbR0U",
        "level": "intermediate",
        "format": "board",
        "language": "english"
    },
    {
        "title": "Java Intermediate Board (Telugu)",
        "url": "https://youtu.be/prfwlnq2vJY",
        "level": "intermediate",
        "format": "board",
        "language": "telugu"
    },
    {
        "title": "Java Intermediate Practical (Telugu)",
        "url": "https://youtu.be/ljhWBL9vcWk",
        "level": "intermediate",
        "format": "practical",
        "language": "telugu"
    },
    {
        "title": "Java Intermediate Board (Hindi)",
        "url": "https://youtu.be/4L6IHb1sxOM",
        "level": "intermediate",
        "format": "board",
        "language": "hindi"
    },
    {
        "title": "Java Intermediate Practical (Hindi)",
        "url": "https://youtu.be/0pUQYwdqRYA",
        "level": "intermediate",
        "format": "practical",
        "language": "hindi"
    },

    # ------------------ ADVANCED ------------------
    {
        "title": "Java Advanced Board (English)",
        "url": "https://youtu.be/vJ-Zn4fo0MQ",
        "level": "advanced",
        "format": "board",
        "language": "english"
    },
    {
        "title": "Java Advanced Practical (English)",
        "url": "https://youtu.be/OuBUUkQfBYM",
        "level": "advanced",
        "format": "practical",
        "language": "english"
    },
    {
        "title": "Java Advanced Practical (Telugu)",
        "url": "https://youtu.be/POErIIv7SGY",
        "level": "advanced",
        "format": "practical",
        "language": "telugu"
    },
    {
        "title": "Java Advanced Board (Telugu)",
        "url": "https://youtu.be/9D_PxPRp-gE",
        "level": "advanced",
        "format": "board",
        "language": "telugu"
    },
    {
        "title": "Java Advanced Board (Hindi)",
        "url": "https://youtu.be/FYoBDj4s99E",
        "level": "advanced",
        "format": "board",
        "language": "hindi"
    },
    {
        "title": "Java Advanced Practical (Hindi)",
        "url": "https://youtu.be/TcJZQvDE1ow",
        "level": "advanced",
        "format": "practical",
        "language": "hindi"
    }
],
    "learning_objectives": [
        "oops",
        "collections",
        "multithreading",
        "spring-basics"
    ]
},

"web_m401": {
    "module_id": "web_m401",
    "title": "Web Development (Beginner → Advanced)",
    "domain": "Web Development",
    "difficulty": "beginner",
    "skill_tag": "web",
    "prerequisites": [],
    "estimated_hours": 15,
    "resources": [

    # ================= BEGINNER =================

    # --- Telugu ---
    {
        "type": "video",
        "title": "Web Dev Beginner Practical (Telugu)",
        "url": "https://youtu.be/TIRRNHfcjl8",
        "level": "beginner",
        "format": "practical",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Web Dev Beginner Board (Telugu)",
        "url": "https://youtu.be/7jaQv6xfQjY",
        "level": "beginner",
        "format": "board",
        "language": "telugu"
    },

    # --- Hindi ---
    {
        "type": "video",
        "title": "Web Dev Beginner Board (Hindi)",
        "url": "https://youtu.be/jgfq8OybWZQ",
        "level": "beginner",
        "format": "board",
        "language": "hindi"
    },
    {
        "type": "video",
        "title": "Web Dev Beginner Practical (Hindi)",
        "url": "https://youtu.be/HBqWsrqK89U",
        "level": "beginner",
        "format": "practical",
        "language": "hindi"
    },

    # --- English ---
    {
        "type": "video",
        "title": "Web Dev Beginner Practical (English)",
        "url": "https://youtu.be/G3e-cpL7ofc",
        "level": "beginner",
        "format": "practical",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Web Dev Beginner Board (English)",
        "url": "https://youtu.be/SaKpzjsXSqg",
        "level": "beginner",
        "format": "board",
        "language": "english"
    },

    # ================= INTERMEDIATE =================

    # --- Telugu ---
    {
        "type": "video",
        "title": "Web Dev Intermediate Practical (Telugu)",
        "url": "https://youtube.com/playlist?list=PLXnOxdiocBo9vXiuAtc8lw-8pMBtMgjCY",
        "level": "intermediate",
        "format": "practical",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Web Dev Intermediate Board (Telugu)",
        "url": "https://youtu.be/f_UsNJ1fHw4",
        "level": "intermediate",
        "format": "board",
        "language": "telugu"
    },

    # --- English ---
    {
        "type": "video",
        "title": "Web Dev Intermediate Board (English)",
        "url": "https://youtu.be/zutb5Clb_0Y",
        "level": "intermediate",
        "format": "board",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Web Dev Intermediate Practical (English)",
        "url": "https://youtu.be/kUMe1FH4CHE",
        "level": "intermediate",
        "format": "practical",
        "language": "english"
    },

    # --- Hindi ---
    {
        "type": "video",
        "title": "Web Dev Intermediate Board (Hindi)",
        "url": "https://youtu.be/rklidcZ-aLU",
        "level": "intermediate",
        "format": "board",
        "language": "hindi"
    },
    {
        "type": "video",
        "title": "Web Dev Intermediate Practical (Hindi)",
        "url": "https://youtu.be/ESnrn1kAD4E",
        "level": "intermediate",
        "format": "practical",
        "language": "hindi"
    },

    # ================= ADVANCED =================

    # --- Telugu ---
    {
        "type": "video",
        "title": "Web Dev Advanced Board (Telugu)",
        "url": "https://youtu.be/cS0TG1iksLM",
        "level": "advanced",
        "format": "board",
        "language": "telugu"
    },
    {
        "type": "video",
        "title": "Web Dev Advanced Practical (Telugu)",
        "url": "https://youtu.be/vcjXeqUJUYU",
        "level": "advanced",
        "format": "practical",
        "language": "telugu"
    },

    # --- English ---
    {
        "type": "video",
        "title": "Web Dev Advanced Practical (English)",
        "url": "https://youtu.be/dX8396ZmSPk",
        "level": "advanced",
        "format": "practical",
        "language": "english"
    },
    {
        "type": "video",
        "title": "Web Dev Advanced Board (English)",
        "url": "https://youtu.be/iG2jotQo9NI",
        "level": "advanced",
        "format": "board",
        "language": "english"
    },

    # --- Hindi ---
    {
        "type": "video",
        "title": "Web Dev Advanced Board (Hindi)",
        "url": "https://youtu.be/VlPiVmYuoqw",
        "level": "advanced",
        "format": "board",
        "language": "hindi"
    },
    {
        "type": "video",
        "title": "Web Dev Advanced Practical (Hindi)",
        "url": "https://youtu.be/kkOuRJ69BRY",
        "level": "advanced",
        "format": "practical",
        "language": "hindi"
    }

    ],

    "learning_objectives": [
        "frontend",
        "backend",
        "deployment"
    ]
},

# ---------- END: additional modules ----------

    
    
}

# -----------------------------
# Sample Quiz Bank
# -----------------------------

QUESTION_BANK = {
    # ---------------- PYTHON QUIZ QUESTIONS ----------------

# Beginner – Coding basics (2)
"py_beg_1": {
    "question_id": "py_beg_1",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "beginner",
    "weight": 1,
    "text": "What is the output of print(type(5))?",
    "choices": ["int", "<class 'int'>", "number", "integer"],
    "correct_choice": 1
},

"py_beg_2": {
    "question_id": "py_beg_2",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "beginner",
    "weight": 1,
    "text": "Which keyword is used to define a function in Python?",
    "choices": ["func", "define", "def", "function"],
    "correct_choice": 2
},

# Intermediate – Logic & structures (2)
"py_int_1": {
    "question_id": "py_int_1",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "intermediate",
    "weight": 2,
    "text": "Which module supports multithreading in Python?",
    "choices": ["asyncio", "threading", "multiprocessing", "time"],
    "correct_choice": 1
},
"py_int_2": {
    "question_id": "py_int_2",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "intermediate",
    "weight": 2,
    "level": "intermediate",
    "text": "What is the output of len({'a':1,'b':2})?",
    "choices": ["1", "2", "Error", "None"],
    "correct_choice": 1
},

# Advanced – OOP & internals (3)
"py_adv_1": {
    "question_id": "py_adv_1",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "advanced",
    "weight": 3,
    "text": "What is the purpose of __init__ method?",
    "choices": ["Destructor", "Initializer", "Compiler", "Decorator"],
    "correct_choice": 1
},
"py_adv_2": {
    "question_id": "py_adv_2",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "advanced",
    "weight": 3,
    "text": "Which decorator is used to create static methods?",
    "choices": ["@class", "@static", "@staticmethod", "@property"],
    "correct_choice": 2
},
"py_adv_3": {
    "question_id": "py_adv_3",
    "course": "Python",
    "skill_tag": "python",
    "difficulty": "advanced",
    "weight": 3,
    "text": "What does GIL stand for in Python?",
    "choices": [
        "Global Interpreter Lock",
        "General Instruction Loop",
        "Global Index List",
        "None"
    ],
    "correct_choice": 0
},


# Theory – Concepts (3)
"py_theory_1": {
    "question_id": "py_theory_1",
    "course": "Python",
    "level": "theory",
    "text": "Python is which type of language?",
    "choices": ["Compiled", "Interpreted", "Machine-level", "Assembly"],
    "correct_choice": 1
},
"py_theory_2": {
    "question_id": "py_theory_2",
    "course": "Python",
    "level": "theory",
    "text": "Which feature allows Python to handle different data types dynamically?",
    "choices": ["Polymorphism", "Dynamic typing", "Encapsulation", "Abstraction"],
    "correct_choice": 1
},
"py_theory_3": {
    "question_id": "py_theory_3",
    "course": "Python",
    "level": "theory",
    "text": "Who created Python?",
    "choices": ["Dennis Ritchie", "James Gosling", "Guido van Rossum", "Bjarne Stroustrup"],
    "correct_choice": 2
}
,
# ---------------- JAVA QUIZ QUESTIONS ----------------

# Beginner (3)
"java_beg_1": {
    "question_id": "java_beg_1",
    "skill_tag": "java",
    "difficulty": "beginner",
    "text": "Which keyword is used to define a class in Java?",
    "choices": ["class", "define", "struct", "object"],
    "correct_choice": 0
},
"java_beg_2": {
    "question_id": "java_beg_2",
    "skill_tag": "java",
    "difficulty": "beginner",
    "text": "Java is ___ typed language.",
    "choices": ["Dynamically", "Statically", "Loosely", "Weakly"],
    "correct_choice": 1
},
"java_beg_3": {
    "question_id": "java_beg_3",
    "skill_tag": "java",
    "difficulty": "beginner",
    "text": "Which method is the entry point of Java program?",
    "choices": ["start()", "main()", "run()", "init()"],
    "correct_choice": 1
},

# Intermediate (2)
"java_int_1": {
    "question_id": "java_int_1",
    "skill_tag": "java",
    "difficulty": "intermediate",
    "text": "Which concept allows method overloading?",
    "choices": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
    "correct_choice": 1
},
"java_int_2": {
    "question_id": "java_int_2",
    "skill_tag": "java",
    "difficulty": "intermediate",
    "text": "Which collection does NOT allow duplicates?",
    "choices": ["List", "Set", "Map", "Queue"],
    "correct_choice": 1
},

# Advanced (2)
"java_adv_1": {
    "question_id": "java_adv_1",
    "skill_tag": "java",
    "difficulty": "advanced",
    "text": "Which keyword is used for multithreading?",
    "choices": ["thread", "synchronized", "process", "async"],
    "correct_choice": 1
},
"java_adv_2": {
    "question_id": "java_adv_2",
    "skill_tag": "java",
    "difficulty": "advanced",
    "text": "What does JVM stand for?",
    "choices": ["Java Variable Machine", "Java Virtual Machine", "Java Visual Model", "None"],
    "correct_choice": 1
},

# Theory (3)
"java_theory_1": {
    "question_id": "java_theory_1",
    "skill_tag": "java",
    "level": "theory",
    "text": "Who developed Java?",
    "choices": ["Microsoft", "Sun Microsystems", "Google", "IBM"],
    "correct_choice": 1
},
"java_theory_2": {
    "question_id": "java_theory_2",
    "skill_tag": "java",
    "level": "theory",
    "text": "Java supports which paradigm?",
    "choices": ["Procedural", "Object-Oriented", "Functional only", "None"],
    "correct_choice": 1
},
"java_theory_3": {
    "question_id": "java_theory_3",
    "skill_tag": "java",
    "level": "theory",
    "text": "Java bytecode runs on?",
    "choices": ["Compiler", "Interpreter", "JVM", "CPU"],
    "correct_choice": 2
}
,
# ================= WEB DEVELOPMENT QUIZ (10) =================

# Beginner (3)
"web_beg_1": {
    "question_id": "web_beg_1",
    "skill_tag": "web",
    "difficulty": "beginner",
    "text": "Which HTML tag is used to create a hyperlink?",
    "choices": ["<link>", "<a>", "<href>", "<url>"],
    "correct_choice": 1
},
"web_beg_2": {
    "question_id": "web_beg_2",
    "skill_tag": "web",
    "difficulty": "beginner",
    "text": "Which CSS property is used to change text color?",
    "choices": ["font-color", "text-color", "color", "background"],
    "correct_choice": 2
},
"web_beg_3": {
    "question_id": "web_beg_3",
    "skill_tag": "web",
    "difficulty": "beginner",
    "text": "Which language runs in the browser?",
    "choices": ["Python", "Java", "C++", "JavaScript"],
    "correct_choice": 3
},

# Intermediate (2)
"web_int_1": {
    "question_id": "web_int_1",
    "skill_tag": "web",
    "difficulty": "intermediate",
    "text": "Which HTTP method is used to update data?",
    "choices": ["GET", "POST", "PUT", "DELETE"],
    "correct_choice": 2
},
"web_int_2": {
    "question_id": "web_int_2",
    "skill_tag": "web",
    "difficulty": "intermediate",
    "text": "Which React hook is used for state?",
    "choices": ["useEffect", "useState", "useRef", "useContext"],
    "correct_choice": 1
},

# Advanced (2)
"web_adv_1": {
    "question_id": "web_adv_1",
    "skill_tag": "web",
    "difficulty": "advanced",
    "text": "What does CORS stand for?",
    "choices": [
        "Cross-Origin Resource Sharing",
        "Client-Origin Resource Service",
        "Cross-Object Request System",
        "Client-Oriented Resource Sharing"
    ],
    "correct_choice": 0
},
"web_adv_2": {
    "question_id": "web_adv_2",
    "skill_tag": "web",
    "difficulty": "advanced",
    "text": "Which protocol secures HTTP?",
    "choices": ["FTP", "SMTP", "HTTPS", "TCP"],
    "correct_choice": 2
},

# Theory (3)
"web_theory_1": {
    "question_id": "web_theory_1",
    "skill_tag": "web",
    "level": "theory",
    "text": "What does HTML stand for?",
    "choices": [
        "HyperText Markup Language",
        "HighText Machine Language",
        "Hyperlink Text Model Language",
        "Home Tool Markup Language"
    ],
    "correct_choice": 0
},
"web_theory_2": {
    "question_id": "web_theory_2",
    "skill_tag": "web",
    "level": "theory",
    "text": "What does CSS stand for?",
    "choices": [
        "Cascading Style Sheets",
        "Colorful Style Sheets",
        "Computer Style Sheets",
        "Creative Style System"
    ],
    "correct_choice": 0
},
"web_theory_3": {
    "question_id": "web_theory_3",
    "skill_tag": "web",
    "level": "theory",
    "text": "Which is a frontend framework?",
    "choices": ["Django", "Spring Boot", "React", "Flask"],
    "correct_choice": 2
},

    # --- Computer Science ---
    "cs_q1": {
        "question_id": "cs_q1",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "What does len([1,2,3]) return?",
        "choices": ["3", "2", "Error", "None"],
        "correct_choice": 0,
        "difficulty": "beginner",
        "weight": 1
    },
    "cs_q2": {
        "question_id": "cs_q2",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "Which data type is immutable in Python?",
        "choices": ["list", "dict", "set", "tuple"],
        "correct_choice": 3,
        "difficulty": "beginner",
        "weight": 1
      },
    "cs_q3": {
        "question_id": "cs_q3",
        "domain": "Computer Science",
        "skill_tag": "ds_algo",
        "text": "What is the average time complexity of quicksort?",
        "choices": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"],
        "correct_choice": 1,
        "difficulty": "intermediate",
        "weight": 2
    },
    "cs_q4": {
        "question_id": "cs_q4",
        "domain": "Computer Science",
        "skill_tag": "ds_algo",
        "text": "Which data structure uses FIFO order?",
        "choices": ["Stack", "Queue", "Tree", "Graph"],
        "correct_choice": 1,
        "difficulty": "beginner",
        "weight": 1
    },
    "cs_q5": {
        "question_id": "cs_q5",
        "domain": "Computer Science",
        "skill_tag": "os",
        "text": "What does 'context switch' refer to in operating systems?",
        "choices": ["Changing user privilege", "Switching from one process to another", "Switching file contexts", "Saving files"],
        "correct_choice": 1,
        "difficulty": "intermediate",
        "weight": 2
    },
    "cs_q6": {
        "question_id": "cs_q6",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "What is Python primarily used for?",
        "choices": ["Web only", "Mobile apps", "General-purpose programming", "Gaming only"],
        "correct_choice": 2,
        "difficulty": "beginner",
        "weight": 1
    },
    "cs_q7": {
        "question_id": "cs_q7",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "Which keyword is used to define a function in Python?",
        "choices": ["func", "define", "def", "function"],
        "correct_choice": 2,
        "difficulty": "beginner",
        "weight": 1
    },
    "cs_q8": {
         "question_id": "cs_q8",
         "domain": "Computer Science",
         "skill_tag": "python",
         "text": "What does list comprehension return?",
         "choices": ["tuple", "set", "dictionary", "list"],
         "correct_choice": 3,
         "difficulty": "intermediate",
         "weight": 2
    },
    "cs_q9": {
        "question_id": "cs_q9",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "What is the use of __init__ method?",
        "choices": ["Create class", "Initialize object", "Delete object", "Print object"],
        "correct_choice": 1,
        "difficulty": "intermediate",
        "weight": 2       
    },
    "cs_q10": {
        "question_id": "cs_q10",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "Which concept allows functions to accept other functions?",
        "choices": ["Inheritance", "Encapsulation", "Decorators", "Compilation"],
        "correct_choice": 2,
        "difficulty": "advanced",
        "weight": 3
    },
    "cs_q11": {
        "question_id": "cs_q11",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "What does GIL stand for?",
        "choices": ["Global Interpreter Lock", "General Instruction Loop", "Global Index List", "None"],
        "correct_choice": 0,
        "difficulty": "advanced",
        "weight": 3    
    },
    "cs_q12": {
        "question_id": "cs_q12",
        "domain": "Computer Science",
        "skill_tag": "python",
        "text": "Which module supports multithreading?",
        "choices": ["asyncio", "threading", "multiprocessing", "time"],
        "correct_choice": 1,
        "difficulty": "advanced",
        "weight": 3
    },    

    # --- Web Development ---
    "web_q1": {
        "question_id": "web_q1",
        "domain": "Web Development",
        "skill_tag": "html",
        "text": "Which HTML tag is used for the largest heading?",
        "choices": ["<h1>", "<h6>", "<head>", "<title>"],
        "correct_choice": 0,
        "difficulty": "beginner",
        "weight": 1
    },
    "web_q2": {
        "question_id": "web_q2",
        "domain": "Web Development",
        "skill_tag": "css",
        "text": "Which CSS property changes text color?",
        "choices": ["bg-color", "color", "font-color", "text-style"],
        "correct_choice": 1,
        "difficulty": "beginner",
        "weight": 1
    },
    "web_q3": {
        "question_id": "web_q3",
        "domain": "Web Development",
        "skill_tag": "js",
        "text": "Which method adds an element to the end of an array in JavaScript?",
        "choices": ["push()", "pop()", "shift()", "unshift()"],
        "correct_choice": 0,
        "difficulty": "intermediate",
        "weight": 2
    },
    "web_q4": {
        "question_id": "web_q4",
        "domain": "Web Development",
        "skill_tag": "react",
        "text": "Which hook is used to add state in functional React components?",
        "choices": ["useState", "useEffect", "useContext", "useReducer"],
        "correct_choice": 0,
        "difficulty": "intermediate",
        "weight": 2
    },
    "web_q5": {
        "question_id": "web_q5",
        "domain": "Web Development",
        "skill_tag": "http",
        "text": "Which HTTP method is typically used to update a resource?",
        "choices": ["GET", "POST", "PUT", "DELETE"],
        "correct_choice": 2,
        "difficulty": "intermediate",
        "weight": 2
    },
}
COURSE_SKILL_MAP = {
    "python": ["python", "loops", "functions", "oops", "advanced"],
    "java": ["java-basics", "oops", "collections"],
    "web": ["html", "css", "javascript"],
    "genai": ["llm", "transformers", "prompt"],
}


# In-memory storage (for demo)
USERS = {}
REGISTERED_USERS = {}
ROADMAPS = {}

# -----------------------------
# Utility functions
# -----------------------------
def detect_level(answers, total_question_ids):
    raw = 0
    max_possible = 0

    weight_map = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3
    }

    for qid in total_question_ids:
        q = QUESTION_BANK.get(qid)
        if not q:
            continue

        difficulty = q.get("difficulty", "beginner")
        weight = weight_map.get(difficulty, 1)

        max_possible += weight

        chosen = answers.get(qid)

        if chosen is not None and str(chosen) == str(q.get("correct_choice")):
            raw += weight

    if max_possible == 0:
        return "beginner", 0

    score_pct = (raw / max_possible) * 100

    if score_pct >= 75:
        level = "advanced"
    elif score_pct >= 40:
        level = "intermediate"
    else:
        level = "beginner"

    return level, round(score_pct, 2)
def analyze_weak_areas(answers, total_question_ids):
    
    weak_topics = {}
    strong_topics = {}

    for qid in total_question_ids:
        q = QUESTION_BANK.get(qid)
        if not q:
            continue

        skill = q.get("skill_tag", "general")
        correct = str(answers.get(qid)) == str(q.get("correct_choice"))

        if correct:
            strong_topics[skill] = strong_topics.get(skill, 0) + 1
        else:
            weak_topics[skill] = weak_topics.get(skill, 0) + 1

    return weak_topics, strong_topics

def add_with_prereq(module_id, selected, catalog):
    if module_id in selected:
        return
    for pre in catalog[module_id]["prerequisites"]:
        add_with_prereq(pre, selected, catalog)
    selected.append(module_id)


def topo_sort(mod_ids, catalog):
    visited = {}
    order = []

    def dfs(mid):
        if visited.get(mid) == 1:
            return
        if visited.get(mid) == -1:
            raise Exception("cycle in prerequisites")
        visited[mid] = -1
        for p in catalog[mid]["prerequisites"]:
            if p in mod_ids:
                dfs(p)
        visited[mid] = 1
        order.append(mid)

    for mid in mod_ids:
        if visited.get(mid) is None:
            dfs(mid)

    return order
def score_resource(r, user_style, user_language):
    score = 0

    # ✅ STYLE SCORE
    if "practical" in user_style and r.get("format") == "practical":
        score += 3

    if "theory" in user_style and r.get("format") == "board":
        score += 3

    # ✅ LANGUAGE SCORE (FIXED)
    if r.get("language", "").strip().lower() == user_language:
        score += 5   # HIGH PRIORITY

    return score
def generate_roadmap_for_user(user):
    print("🔥 USER DATA:", user)
    print("🔥 USER LANGUAGE RAW:", user.get("user_language"))
    # ✅ ALWAYS TAKE LATEST COURSE LANGUAGE (FINAL FIX)
    course_id = user.get("goal_domain", "").lower().replace(" ", "_")

    user_language = str(
        user.get("user_language", "")
    ).strip().lower()
    print("🔥 USING LANGUAGE:", user_language)
    print("🔥 FULL USER:", user)

    if not user_language:
        user_language = str(user.get("language", "english")).strip().lower()
    user_style = str(user.get("preferred_style") or "practical").strip().lower()

    print("✅ FINAL LANGUAGE:", user_language)
    print("✅ FINAL STYLE:", user_style)

    print("✅ FINAL USER LANGUAGE:", user_language)
    course_id = user.get("goal_domain", "Python").lower().replace(" ", "_")
    course = user.get("user_courses", {}).get(course_id)

    if course:
        level = course.get("current_level", "beginner")
    else:
        level = user.get("detected_level", "beginner")

    time_per_week = int(user.get("time_per_week_hours", 6))

    # ✅ FIXED: ALWAYS DEFINE FIRST
    domain_modules = [
        m for m in MODULE_CATALOG.values()
        if m.get("skill_tag", "").lower() in user.get("goal_domain", "").lower()
    ]

    # THEN level logic
    if level == "beginner":
        target_counts = {"beginner": 3, "intermediate": 1, "advanced": 0}
    elif level == "intermediate":
        target_counts = {"beginner": 1, "intermediate": 3, "advanced": 1}
    else:
        target_counts = {"beginner": 0, "intermediate": 1, "advanced": 4}

    by_diff = {"beginner": [], "intermediate": [], "advanced": []}
    for m in domain_modules:
        d = m.get("difficulty", "beginner")
        if d in by_diff:
            by_diff[d].append(m)

    # Sort within difficulty to prefer small estimated_hours (fast wins) or explicit ordering
    for k in by_diff:
        by_diff[k] = sorted(by_diff[k], key=lambda x: x.get("estimated_hours", 999))

    # Select modules according to target_counts while avoiding duplicates
    selected = []
    def pick_from(diff, n):
        taken = []
        for m in by_diff.get(diff, []):
            if m["module_id"] not in selected:
                selected.append(m["module_id"])
                taken.append(m)
            if len(taken) >= n:
                break
        return taken

    # Greedy selection for each difficulty in order beginner->intermediate->advanced
    for diff in ("beginner", "intermediate", "advanced"):
        need = target_counts.get(diff, 0)
        pick_from(diff, need)

    # If we didn't find enough (catalog small), fill from other difficulties
    total_needed = sum(target_counts.values())
    if len(selected) < total_needed:
        # gather all domain modules in order of ascending difficulty (begin->int->adv)
        fallback = sorted(domain_modules, key=lambda m: ['beginner','intermediate','advanced'].index(m['difficulty']))
        for m in fallback:
            if m["module_id"] not in selected:
                selected.append(m["module_id"])
            if len(selected) >= total_needed:
                break

    # Ensure prerequisites are included (recursively)
    final_with_prereqs = []
    for mid in list(selected):
        add_with_prereq(mid, final_with_prereqs, MODULE_CATALOG)

    # Keep original selection order but dedupe while preserving prereq ordering
    seen = set()
    selected_unique = []
    for mid in final_with_prereqs:
        if mid not in seen:
            seen.add(mid)
            selected_unique.append(mid)

    # Topologically sort to ensure prereqs come before dependents
    try:
        sequence = topo_sort(selected_unique, MODULE_CATALOG)
    except Exception:
        # fallback: if topo fails (cycle), just use selected_unique
        sequence = selected_unique
            # ✅ REMOVE DUPLICATES
    unique_sequence = []
    seen = set()

# -----------------------------
# MAIN LOOP
# -----------------------------
    roadmap = []
    week = 1
    hours_this_week = 0
    for mid in sequence:

        mod = MODULE_CATALOG.get(mid)

        if not mod:
            continue

        # -----------------------------
        # STEP 1: LEVEL FILTER
        # -----------------------------
        level_filtered = [
            r for r in mod["resources"]
            if str(r.get("level", "")).strip().lower() == level
        ]

        # -----------------------------
        # STEP 2: LANGUAGE FILTER
        # -----------------------------
        lang_filtered = [
            r for r in level_filtered
            if str(r.get("language", "")).strip().lower() == user_language
        ]

        # 🚨 STRICT: DO NOT FALLBACK TO OTHER LANGUAGES
        if not lang_filtered:
            print("⚠️ No exact language match, using available language")
            lang_filtered = level_filtered   # fallback to same level ANY language

        # -----------------------------
        # STEP 3: STYLE FILTER
        # -----------------------------
        if user_style == "practical":
            final_resources = [
                r for r in lang_filtered if r.get("format") == "practical"
            ]

        elif user_style == "theory":
            final_resources = [
                r for r in lang_filtered if r.get("format") == "board"
            ]

        else:
            final_resources = lang_filtered

        # 🚨 FINAL SAFETY (same language only)
        if not final_resources:
            final_resources = lang_filtered

        # -----------------------------
        # PICK ONLY ONE VIDEO
        # -----------------------------
        mod = dict(mod)
        print("🎯 FINAL:", final_resources[0].get("title"), final_resources[0].get("language"))
        mod["resources"] = [final_resources[0]]

        # -----------------------------
        # SCHEDULING
        # -----------------------------
        est = mod.get('estimated_hours', 4)

        if hours_this_week + est > time_per_week and hours_this_week > 0:
            week += 1
            hours_this_week = 0
    
        roadmap.append({'week': week, 'module': mod})
        hours_this_week += est

    # -----------------------------
    # ✅ FALLBACK (ONLY IF EMPTY)
    # -----------------------------
    if not roadmap:
        print("⚠️ No roadmap generated — using fallback")

        fallback_mods = list(MODULE_CATALOG.values())[:4]
        week = 1
        hours_this_week = 0

        for mod in fallback_mods:
            est = mod.get('estimated_hours', 4)

            if hours_this_week + est > time_per_week and hours_this_week > 0:
                week += 1
                hours_this_week = 0

            roadmap.append({'week': week, 'module': mod})
            hours_this_week += est
    return roadmap
# -----------------------------
# Routes & HTML templates
# -----------------------------
HOME_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Learning Path Generator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gradient-to-r from-indigo-50 via-white to-rose-50 min-h-screen">
  <div class="max-w-6xl mx-auto px-6 py-12">
    <header class="flex items-center justify-between">
      <h1 class="text-3xl font-extrabold text-indigo-700">AI-Powered Personalized Learning</h1>
     <nav class="flex gap-3 items-center">
  <span class="text-sm text-gray-600">
    Welcome {{ user_email }}
  </span>

  {% if session_role == "admin" %}
  <a href="/analytics"
     class="px-4 py-2 bg-gray-800 text-white rounded-md shadow hover:bg-gray-900">
    📊 Analytics
  </a>
  {% endif %}

  <a href="/logout"
     class="px-4 py-2 bg-rose-500 text-white rounded-md shadow hover:bg-rose-600">
    Logout
  </a>
</nav>


    </header>

    <main class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
      <section class="p-8 bg-white/80 rounded-2xl shadow-lg">
        <h2 class="text-2xl font-bold text-gray-800">Why this system?</h2>
        <p class="mt-4 text-gray-600">We generate a tailored learning roadmap after assessing your current level with a short quiz. The roadmap includes curated resources and a week-by-week plan.</p>

        <ul class="mt-6 space-y-3 text-gray-700">
          <li class="flex items-start gap-3"><span class="text-indigo-600 font-bold">✓</span> Adaptive learning paths</li>
          <li class="flex items-start gap-3"><span class="text-indigo-600 font-bold">✓</span> Time-aware scheduling</li>
          <li class="flex items-start gap-3"><span class="text-indigo-600 font-bold">✓</span> Resource matching to your preferred style</li>
        </ul>
      </section>

      <section class="p-8 rounded-2xl">
        <div class="bg-white p-6 rounded-xl shadow-lg">
          <h3 class="text-lg font-semibold">Your Learning</h3>
<p class="mt-2 text-sm text-gray-600">
  Add a new course and generate a personalized roadmap.
</p>

<div class="mt-4 flex gap-3">
  <a href="/onboard"
     class="px-4 py-2 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700">
     Add Course
  </a>
</div>

<!-- 🔥 My Learning Progress Section -->
<div id="progressSection" class="mt-6"></div>
<script>
async function loadProgress(){
  const res = await fetch('/api/my-progress');
  const data = await res.json();

  if(data.error || !data.course){
      return;
  }

  const section = document.getElementById('progressSection');

  // 🎉 If course completed → show certificate screen
if(data.status === "completed"){

    section.innerHTML = `
      <div class="mt-6 p-6 bg-white rounded-xl shadow text-center">
        <h2 class="text-2xl font-bold text-green-600">🎉 Congratulations!</h2>
        <p class="mt-2 text-gray-600">
          You have successfully completed the ${data.course} course.
        </p>

        <div class="mt-6">
          <a href="/certificate"
             class="px-6 py-3 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700">
             📜 Download Certificate
          </a>
        </div>
      </div>
    `;

    // 👇 ADD BADGES HERE ALSO
    if(data.badges && data.badges.length > 0){
        section.innerHTML += `
            <div class="mt-4 p-4 bg-yellow-50 rounded-xl shadow text-center">
                <h4 class="font-semibold mb-2">🏆 Your Badges</h4>
                <div class="flex gap-3 flex-wrap justify-center">
                    ${data.badges.map(b => `
                        <div class="px-4 py-2 bg-yellow-400 text-white rounded-full text-sm">
                            ${b}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    return;  // keep return AFTER badges
}

  // 📊 Otherwise show normal progress
  section.innerHTML = `
    <div class="mt-6 p-4 bg-white rounded-xl shadow">
      <h3 class="text-lg font-semibold">📊 My Learning Progress</h3>
      <div class="mt-2 text-sm text-gray-600">
        Course: <strong>${data.course}</strong>
      </div>
      <div class="mt-1 text-sm text-gray-600">
        Current Level: <strong>${data.current_level}</strong>
      </div>
      <div class="mt-1 text-sm text-gray-600">
        Status: <strong>${data.status}</strong>
      </div>

      <div class="mt-4">
        <div class="w-full bg-gray-200 rounded-full h-4">
          <div class="bg-indigo-600 h-4 rounded-full text-xs text-white text-center"
               style="width:${data.progress_pct}%">
               ${data.progress_pct}%
          </div>
        </div>
      </div>

      <div class="mt-4">
        <a href="/roadmap?user_id=${data.user_id}&roadmap_id=${data.last_roadmap_id}"
           class="px-4 py-2 bg-green-600 text-white rounded-md shadow hover:bg-green-700">
           ▶ Continue Learning
        </a>
      </div>
    </div>
  `;
  // 🎖️ Show Badges
if(data.badges && data.badges.length > 0){
    section.innerHTML += `
        <div class="mt-4 p-4 bg-yellow-50 rounded-xl shadow">
            <h4 class="font-semibold mb-2">🏆 Your Badges</h4>
            <div class="flex gap-3 flex-wrap">
                ${data.badges.map(b => `
                    <div class="px-3 py-1 bg-yellow-400 text-white rounded-full text-sm">
                        ${b}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}
}

loadProgress();
</script>
<!-- 📚 My Courses Section -->
<div class="mt-10">
  <h3 class="text-lg font-semibold mb-4">📚 My Courses</h3>
  <div id="homeCoursesContainer" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
</div>

<script>
async function loadHomeCourses(){
  const res = await fetch('/api/my-courses');
  const data = await res.json();

  if(data.error || !data.courses){
      return;
  }

  const container = document.getElementById('homeCoursesContainer');
  container.innerHTML = '';

  data.courses.forEach(course => {

    const card = document.createElement('div');
    card.className = 'bg-white p-6 rounded-xl shadow';

    card.innerHTML = `
      <h2 class="text-lg font-semibold capitalize">${course.course_id.replace('_',' ')}</h2>
      <div class="text-sm text-gray-600 mt-1">
        Current Level: <strong>${course.current_level}</strong>
      </div>
      <div class="text-sm text-gray-600">
        Status: <strong>${course.status}</strong>
      </div>

      <div class="mt-3">
        <div class="w-full bg-gray-200 rounded-full h-4">
          <div class="bg-indigo-600 h-4 rounded-full text-xs text-white text-center"
               style="width:${course.progress_pct}%">
               ${course.progress_pct}%
          </div>
        </div>
      </div>

      <div class="mt-4 flex gap-3">
        <a href="/roadmap?user_id=${course.user_id}&roadmap_id=${course.last_roadmap_id}&course_id=${course.course_id}"
           class="px-3 py-2 bg-green-600 text-white rounded-md text-sm">
           ▶ Continue
        </a>
      </div>
    `;

    container.appendChild(card);
  });
}

loadHomeCourses();
// Animate progress bars
setTimeout(() => {
  document.querySelectorAll('[data-progress]').forEach(bar => {
    const value = bar.getAttribute('data-progress');
    bar.style.width = value + '%';
    bar.innerText = value + '%';
  });
}, 300);
</script>
      </section>
    </main>

    <footer class="mt-12 text-center text-sm text-gray-500">Built for demo — extend it for your project report & presentation.</footer>
</div>

</body>
</html>
'''

ONBOARD_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Onboarding - AI Roadmap</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gradient-to-b from-white to-indigo-50 min-h-screen">
  <div class="max-w-3xl mx-auto p-6">
    <div class="bg-white rounded-2xl p-8 shadow">
      <h2 class="text-2xl font-bold">Get started — create your profile</h2>
      <form id="onboardForm" class="mt-6 grid grid-cols-1 gap-4">

  <input required name="name" placeholder="Your name" class="p-3 border rounded-md" />

  <select name="role" class="p-3 border rounded-md">
    <option value="student">Student</option>
    <option value="professional">Professional</option>
  </select>

  <!-- COURSE -->
  <select name="goal_domain" class="p-3 border rounded-md">
    <option value="python">Python</option>
    <option value="java">Java</option>
    <option value="web development">Web</option>
  </select>

  <!-- LANGUAGE -->
  <select name="language" class="p-3 border rounded-md">
    <option value="english">English</option>
    <option value="telugu">Telugu</option>
    <option value="hindi">Hindi</option>
  </select>

  <!-- STYLE -->
  <select name="preferred_style" class="p-3 border rounded-md">
  <option value="practical">Hands-on</option>
  <option value="theory">Theory</option>
</select>

<!-- ✅ ADD THIS INSIDE ONBOARD_HTML -->
<button type="submit" 
  class="mt-4 px-4 py-3 bg-indigo-600 text-white rounded-md w-full">
  🚀 Start Learning
</button>

</form>

    </div>
  </div>

<script>
const form = document.getElementById('onboardForm');
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  const res = await fetch('/api/signup', {
    method:'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
  });
  const j = await res.json();
  if(j.user_id) {
    window.location = `/quiz?user_id=${j.user_id}`
  } else {
    alert('Error creating user');
  }
})
</script>
</body>
</html>
'''

QUIZ_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Quiz - AI Roadmap</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gradient-to-b from-white to-rose-50 min-h-screen">
  <div class="max-w-4xl mx-auto p-6">
    <div class="bg-white rounded-2xl p-6 shadow">
      <h2 class="text-xl font-bold">Short assessment</h2>
      <p class="text-gray-600 mt-1">This quick quiz helps us find your level.</p>

      <form id="quizForm" class="mt-6 space-y-6">
        <div id="questions"></div>
        <div class="flex gap-3 items-center">
          <button type="submit" class="px-4 py-2 bg-rose-500 text-white rounded-md">Submit Answers</button>
          <a id="skipBtn" class="text-sm text-gray-500">Skip quiz (assign Beginner)</a>
        </div>
      </form>
    </div>
  </div>

<script>
const params = new URLSearchParams(window.location.search);
const userId = params.get('user_id');
const isPost = params.get('post') === '1';
if(!userId) window.location = '/';

async function loadQuestions(){
  const params = new URLSearchParams(window.location.search);
  const moduleId = params.get('module_id');       // new
  const userId = params.get('user_id');
  const isPost = params.get('post') === '1';

  if(!userId) { window.location = '/'; return; }

  // build query string and include module_id when present
  let q = `/api/quiz/start?user_id=${encodeURIComponent(userId)}${isPost ? '&post=1' : ''}`;
  if (moduleId) q += `&module_id=${encodeURIComponent(moduleId)}`;

  const res = await fetch(q);
  const j = await res.json();
  const qDiv = document.getElementById('questions');
  qDiv.innerHTML = '';
  j.questions.forEach((qobj, idx)=>{
    const container = document.createElement('div');
    container.className = 'p-4 border rounded-md';
    container.innerHTML = `<div class="font-medium">${idx+1}. ${qobj.text}</div>`;
    qobj.choices.forEach((c, ci)=>{
      const safeText = String(c).replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const input = `<label class='block mt-2'><input type='radio' name='${qobj.question_id}' value='${ci}' class='mr-2'/> ${safeText}</label>`;
      container.innerHTML += input;
    })
    qDiv.appendChild(container);
  })
}

loadQuestions();

document.getElementById('quizForm').addEventListener('submit', async (e)=>{
  e.preventDefault();

  const formData = new FormData(e.target);
const data = Object.fromEntries(formData.entries());

// ✅ FORCE behavior questions (if skipped)
["behav_1","behav_2","behav_3","behav_4"].forEach(q=>{
    if(!data[q]){
        data[q] = "0";  // default value
    }
});
  const payload = { user_id: userId, answers: data, post: isPost };

  const res = await fetch('/api/quiz/submit', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
  });

  const j = await res.json();

  if(j.error){
      alert('Error: '+j.error);
      return;
  }

  if(isPost){
      window.location = `/roadmap?user_id=${userId}&roadmap_id=${j.roadmap_id}`;
      return;
  }

  // Hide quiz form
  document.getElementById('quizForm').style.display = 'none';
  const container = document.createElement('div');
  container.className = "mt-6 p-6 bg-white rounded-xl shadow";

container.innerHTML = `
  <div class="text-lg font-semibold mb-4">Quiz Submitted</div>

  <div class="mt-4">
    <strong>🤖 AI Suggestions:</strong>
    ${j.ai_recommendations ? j.ai_recommendations.map(t => `<div>• ${t}</div>`).join("") : ""}
  </div>

  <div class="flex gap-4 mt-4">
    <button id="reviewBtn" class="px-4 py-2 bg-indigo-600 text-white rounded-md">
      🔍 Review Answers
    </button>
    <button id="skipBtn2" class="px-4 py-2 bg-green-600 text-white rounded-md">
      ⏭️ Skip & Continue
    </button>
  </div>
`;

  document.querySelector('.bg-white.rounded-2xl').appendChild(container);

  document.getElementById('skipBtn2').addEventListener('click', ()=>{
      window.location = `/roadmap?user_id=${userId}&roadmap_id=${j.roadmap_id}`;
  });

  document.getElementById('reviewBtn').addEventListener('click', ()=>{
      const reviewDiv = document.getElementById('reviewSection');
      reviewDiv.classList.remove('hidden');
      reviewDiv.innerHTML = '';

      j.review.forEach((q, index)=>{
          const card = document.createElement('div');
          card.className = "p-4 border rounded-md mb-3";

          const correct = Number(q.user_choice) === Number(q.correct_choice);

          card.innerHTML = `
            <div class="font-medium mb-2">${index+1}. ${q.question}</div>
            ${q.choices.map((choice, idx)=>{
                let color = '';
                if(idx === q.correct_choice){
                    color = 'text-green-600 font-semibold';
                }
                if(idx === q.user_choice && idx !== q.correct_choice){
                    color = 'text-red-600 font-semibold';
                }
                return `<div class="${color}">${choice}</div>`;
            }).join('')}
            <div class="mt-2 ${correct ? 'text-green-600' : 'text-red-600'} font-semibold">
              ${correct ? '✔ Correct' : '✖ Incorrect'}
            </div>
          `;

          reviewDiv.appendChild(card);
      });
  });
});

document.getElementById('skipBtn').addEventListener('click', async ()=>{
  const res = await fetch('/api/quiz/submit', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_id:userId, answers:{}, post: isPost}) });
  const j = await res.json();
  if(j.roadmap_id) window.location = `/roadmap?user_id=${userId}&roadmap_id=${j.roadmap_id}`
})
</script>

</body>
</html>
'''

ROADMAP_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Roadmap - AI Roadmap</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gradient-to-b from-white to-indigo-50 min-h-screen">
  <div class="max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Your Personalized Roadmap</h1>
      <a href="/" class="text-sm text-gray-600">Home</a>
    </div>

    <div id="meta" class="mb-4"></div>
    <div id="roadmapList" class="space-y-4"></div>
  </div>

<script>
const params = new URLSearchParams(window.location.search);
const userId = params.get('user_id');
const roadmapId = params.get('roadmap_id');
const courseId = params.get('course_id');
if(!userId || !roadmapId) window.location = '/';

async function loadRoadmap(){
  const res = await fetch(`/api/roadmap/${roadmapId}?user_id=${userId}`);

const j = await res.json();

console.log(j);

if (j.ai_recommendations) {
    const box = document.createElement("div");
    box.style.marginTop = "20px";
    box.style.padding = "15px";
    box.style.background = "#eef2ff";
    box.style.borderRadius = "10px";

box.innerHTML = `
  <h3>🤖 AI Suggestions</h3>
  ${j.ai_recommendations.map(t => `
    <div>
      • ${t}
      <button onclick="askAI('${t}')">Ask AI</button>
    </div>
  `).join("")}
`;

    document.getElementById("quizForm").appendChild(box);
}
  // 🔥 Check completion status
const progressRes = await fetch('/api/my-progress');
const progressData = await progressRes.json();

if(progressData.status === "completed"){

  document.getElementById('meta').innerHTML = `
    <div class="p-6 bg-white rounded-xl shadow text-center">
      <h2 class="text-2xl font-bold text-green-600">
        🎉 Course Completed Successfully!
      </h2>
      <div class="mt-6">
        <a href="/"
           class="px-6 py-3 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700">
           🏠 Go Home & Download Certificate
        </a>
      </div>
    </div>
  `;

  document.getElementById('roadmapList').innerHTML = '';
  return;
}
  document.getElementById('meta').innerHTML = `<div class='p-4 rounded-lg bg-white shadow'>Detected level: <strong>${j.detected_level}</strong> — Score: <strong>${j.score_pct}%</strong></div>`;
  const container = document.getElementById('roadmapList');
  container.innerHTML = '';
  j.roadmap.forEach(item=>{
    const card = document.createElement('div');
    card.className = 'p-4 bg-white rounded-xl shadow flex justify-between items-center';
    const left = document.createElement('div');
    left.innerHTML = `<div class='text-sm text-gray-500'>Week ${item.week}</div><div class='font-semibold text-lg'>${item.module.title}</div><div class='text-sm text-gray-600 mt-1'>${item.module.learning_objectives.join(', ')}</div>`;
    const right = document.createElement('div');
    right.className = 'flex flex-col items-end';
    right.innerHTML = `<div class='text-sm text-gray-500'>${item.module.difficulty}</div><div class='mt-2 flex gap-2' id="res-${item.module.module_id}"></div>`;

    // add resource buttons
    const resDiv = right.querySelector(`#res-${item.module.module_id}`);
    item.module.resources.slice(0,3).forEach(r=>{
      const btn = document.createElement('button');
      btn.dataset.moduleId = item.module.module_id;
      btn.className = 'px-3 py-1 bg-indigo-600 text-white rounded-md text-sm';
      btn.innerText = r.type + ' • ' + (r.title.length>28 ? r.title.slice(0,28)+'...' : r.title);

      if(r.type === 'video') {
        btn.addEventListener('click', ()=>{
  // Helper function to extract YouTube video ID
  const vid = getYouTubeId(r.url);
  if (!vid) {
    window.open(r.url, '_blank');
    return;
  }

  const embedUrl = `https://www.youtube.com/embed/${vid}?rel=0&modestbranding=1`;

  // Create modal overlay
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black/70 flex items-center justify-center z-50';

  // Modal HTML
  modal.innerHTML = `
    <div class="bg-white rounded-xl p-4 w-11/12 md:w-3/4 lg:w-2/3 max-w-4xl shadow-lg">
      <div class="flex justify-between items-center mb-2">
        <div class="text-lg font-semibold">${r.title}</div>
        <div class="flex items-center gap-2">
          <a id="openOnYouTube" class="px-3 py-1 bg-indigo-600 text-white rounded-md text-sm" href="https://www.youtube.com/watch?v=${vid}" target="_blank" rel="noopener">Open on YouTube</a>
          <a id="takePostQuiz" class="px-3 py-1 bg-green-600 text-white rounded-md text-sm" href="#">Take Post-Quiz</a>
          <button id="closeModalBtn" class="px-3 py-1 bg-rose-500 text-white rounded-md">Close</button>
        </div>
      </div>
      <div style="position:relative;padding-top:56.25%;">
        <iframe id="modalIframe" src="${embedUrl}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Close modal on click
  modal.querySelector('#closeModalBtn').addEventListener('click', ()=> modal.remove());
  modal.addEventListener('click', (ev)=>{ if(ev.target === modal) modal.remove(); });

  // Take Post-Quiz redirect logic
  // inside the btn.addEventListener('click', ()=>{ ... }) where you build the modal
// ensure btn.dataset.moduleId is set earlier when creating the button:
// btn.dataset.moduleId = item.module.module_id;

const takeBtn = modal.querySelector('#takePostQuiz');
if (takeBtn) {
  takeBtn.addEventListener('click', (ev)=>{
    ev.preventDefault();
    const moduleId = btn.dataset.moduleId || (new URLSearchParams(window.location.search)).get('module_id');
    const uid = userId || (new URLSearchParams(window.location.search)).get('user_id');
    if (!uid) {
      alert('User ID missing. Please open roadmap from the normal flow.');
      return;
    }
    // include module_id so server can give a targeted post quiz
    const qurl = `/quiz?user_id=${encodeURIComponent(uid)}&post=1&module_id=${encodeURIComponent(moduleId || '')}`;
    window.location.href = qurl;
  });
}

});

      } else {
        btn.addEventListener('click', ()=> window.open(r.url, '_blank'));
      }

      resDiv.appendChild(btn);
    });
// 🔥 Add Mark as Completed Button
const completeBtn = document.createElement('button');
completeBtn.className = 'mt-2 px-3 py-1 bg-green-600 text-white rounded-md text-sm';
completeBtn.innerText = '✅ Mark as Completed';

completeBtn.addEventListener('click', async () => {
  const level = item.module.difficulty.toLowerCase(); // beginner/intermediate/advanced

  const response = await fetch('/api/module/complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level: level })
  });

  const data = await response.json();
  alert(data.message);

  // Redirect to Post Quiz
  const qurl = `/quiz?user_id=${encodeURIComponent(userId)}&post=1&module_id=${encodeURIComponent(item.module.module_id)}`;
  window.location.href = qurl;
});

right.appendChild(completeBtn);

    card.appendChild(left);
    card.appendChild(right);
    container.appendChild(card);
  })
}

loadRoadmap();
</script>
</body>
</html>
'''

ADMIN_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Admin - AI Roadmap</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style> body { font-family: 'Inter', sans-serif; } </style>
</head>
<body class="bg-gray-50 min-h-screen">
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Admin Dashboard</h1>

    <section class="mb-8">
      <h2 class="text-lg font-semibold mb-2">Users</h2>
      <div id="usersTable" class="bg-white rounded shadow p-4 overflow-auto"></div>
    </section>

    <section class="mb-8">
      <h2 class="text-lg font-semibold mb-2">Roadmaps</h2>
      <div id="roadmapsTable" class="bg-white rounded shadow p-4 overflow-auto"></div>
    </section>

    <section>
      <h2 class="text-lg font-semibold mb-2">Module Catalog (sample)</h2>
      <div id="catalog" class="bg-white rounded shadow p-4 overflow-auto"></div>
    </section>
  </div>

<script>
async function loadAdmin(){
  const res = await fetch('/api/admin');
  const j = await res.json();

  // Users table
  const users = Object.values(j.users || {});
  const ut = `<table class="min-w-full divide-y"><thead class="bg-gray-100"><tr>
    <th class="p-2 text-left">User ID</th><th class="p-2 text-left">Name</th><th class="p-2 text-left">Email</th><th class="p-2 text-left">Domain</th><th class="p-2 text-left">Level</th><th class="p-2 text-left">Score</th>
  </tr></thead><tbody>
  ${users.map(u=>`<tr class="border-t"><td class="p-2">${u.user_id}</td><td class="p-2">${u.name}</td><td class="p-2">${u.email}</td><td class="p-2">${u.goal_domain||''}</td><td class="p-2">${u.detected_level||''}</td><td class="p-2">${u.score_pct||''}</td></tr>`).join('')}
  </tbody></table>`;
  document.getElementById('usersTable').innerHTML = ut;

  // Roadmaps table
  const rms = Object.values(j.roadmaps || {});
  const rt = `<table class="min-w-full divide-y"><thead class="bg-gray-100"><tr>
    <th class="p-2 text-left">Roadmap ID</th><th class="p-2 text-left">User ID</th><th class="p-2 text-left">Domain</th><th class="p-2 text-left">Level</th><th class="p-2 text-left">Created</th>
  </tr></thead><tbody>
  ${rms.map(r=>`<tr class="border-t"><td class="p-2">${r.roadmap_id}</td><td class="p-2">${r.user_id}</td><td class="p-2">${(r.roadmap && r.roadmap[0] && r.roadmap[0].module ? r.roadmap[0].module.domain : '')}</td><td class="p-2">${r.detected_level||''}</td><td class="p-2">${r.generated_on||''}</td></tr>`).join('')}
  </tbody></table>`;
  document.getElementById('roadmapsTable').innerHTML = rt;

  // Catalog (sample)
  const catalogEntries = Object.values(j.catalog || {});
  const catHtml = `<div class="grid grid-cols-1 md:grid-cols-2 gap-4">${catalogEntries.map(m=>`
    <div class="p-3 border rounded">
      <div class="font-semibold">${m.title} <span class="text-xs text-gray-500">(${m.difficulty})</span></div>
      <div class="text-sm text-gray-600 mt-1">Domain: ${m.domain}</div>
      <div class="text-sm text-gray-600 mt-1">Prereq: ${m.prerequisites.join(', ') || 'None'}</div>
      <div class="text-sm text-gray-700 mt-2">Resources:
        <ul class="list-disc ml-5">${(m.resources || []).map(r=>`<li><a class="text-indigo-600" href="${r.url}" target="_blank">${r.type} - ${r.title}</a></li>`).join('')}</ul>
      </div>
    </div>`).join('')}</div>` ;
  document.getElementById('catalog').innerHTML = catHtml;
}

loadAdmin();
</script>
</body>
</html>
'''

REGISTER_HTML = '''
<!doctype html>
<html>
<head>
  <title>Register</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
  <div class="bg-white p-8 rounded shadow w-96">
    <h2 class="text-2xl font-bold mb-4">Register</h2>
    <form method="POST">
      <input name="name" placeholder="Name" class="w-full p-2 border mb-3" required>
      <input name="email" type="email" placeholder="Email" class="w-full p-2 border mb-3" required>
      <input name="password" type="password" placeholder="Password" class="w-full p-2 border mb-3" required>
      <button class="w-full bg-indigo-600 text-white p-2 rounded">Register</button>
    </form>
    <p class="mt-3 text-sm">Already have account?
      <a href="/login" class="text-indigo-600">Login</a>
    </p>
  </div>
</body>
</html>
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in REGISTERED_USERS:
            return "User already exists"

        REGISTERED_USERS[email] = {
    "name": name,
    "password": password,
    "role": "admin" if email == "admin@lms.com" else "student"
}

        return redirect(url_for('login'))

    return render_template_string(REGISTER_HTML)
LOGIN_HTML = '''
<!doctype html>
<html>
<head>
  <title>Login</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
  <div class="bg-white p-8 rounded shadow w-96">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form method="POST">
      <input name="email" type="email" placeholder="Email" class="w-full p-2 border mb-3" required>
      <input name="password" type="password" placeholder="Password" class="w-full p-2 border mb-3" required>
      <button class="w-full bg-indigo-600 text-white p-2 rounded">Login</button>
    </form>
    <p class="mt-3 text-sm">New user?
      <a href="/register" class="text-indigo-600">Register</a>
    </p>
  </div>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = REGISTERED_USERS.get(email)

        if user and user['password'] == password:
            session['user_email'] = email
            session['role'] = user.get('role', 'student')

            # 🔍 Find matching user_id in USERS
            for uid, u in USERS.items():
                if u.get('email') == email:
                    session['user_id'] = uid
                    break

            return redirect(url_for('home'))

        else:
            return "Invalid credentials"

    return render_template_string(LOGIN_HTML)

@app.route('/')
def home():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user_email = session.get('user_email')
    return render_template_string(
    HOME_HTML,
    user_email=user_email,
    session_role=session.get("role")
)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/health')
def api_health():
    return jsonify({"message": "Backend is running successfully!"})
@app.route('/debug-role')
def debug_role():
    return {
        "user_email": session.get("user_email"),
        "role": session.get("role")
    }

@app.route('/onboard')
def onboard():
    return render_template_string(ONBOARD_HTML)

@app.route('/quiz')
def quiz_page():
    return render_template_string(QUIZ_HTML)

@app.route('/roadmap')
def roadmap_page():
    return render_template_string(ROADMAP_HTML)

@app.route('/admin')
def admin_page():
    return render_template_string(ADMIN_HTML)
@app.route('/courses')
def courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template_string(COURSES_HTML)

# -----------------------------
# API endpoints
# -----------------------------
@app.route('/api/signup', methods=['POST'])
def api_signup():
    if 'user_email' not in session:
        return jsonify({'error': 'not logged in'}), 401

    email = session['user_email']
    data = request.get_json() or request.form.to_dict()

    # 🔍 If user already exists → reuse AND set session
    for uid, u in USERS.items():
        if u.get('email') == email:
            new_domain = data.get('goal_domain', u.get('goal_domain'))
            u['goal_domain'] = new_domain

            course_id = new_domain.lower().replace(" ", "_")

            # 🔥 Ensure fresh course progress
            if "user_courses" not in u:
                u["user_courses"] = {}

            if course_id not in u["user_courses"]:
                u["user_courses"][course_id] = {
                    "current_level": "beginner",
                    "completed_levels": [],
                    "status": "in_progress"
                }

            session['user_id'] = uid
            return jsonify({'status': 'ok', 'user_id': uid})


    # 🔥 Otherwise create new
    user_id = str(uuid.uuid4())[:8]

    goal_domain = data.get('goal_domain', 'Python')
    course_id = goal_domain.lower().replace(" ", "_")

    user = {
        "user_language": data.get("language", "english"),
        "goal_domain": data.get("goal_domain", "python").lower(),
        'user_id': user_id,
        'name': data.get('name', 'User'),
        'email': email,
        'role': data.get('role', 'student'),
        'time_per_week_hours': int(data.get('time_per_week_hours', 6)),
        'preferred_style': data.get('preferred_style', 'video'),
        'goal_domain': goal_domain,
        'created_at': datetime.utcnow().isoformat(),
        'user_courses': {
            course_id: {
                "current_level": "beginner",
                "completed_levels": [],
                "status": "in_progress"
            }
        }
    }
    USERS[user_id] = user
    session['user_id'] = user_id  # ✅ IMPORTANT

    return jsonify({'status': 'ok', 'user_id': user_id})

@app.route('/api/quiz/start')
def api_quiz_start():
    user_id = request.args.get('user_id')

    if not user_id or user_id not in USERS:
        return jsonify({'error': 'User not found'}), 404

    user = USERS[user_id]
    domain = user.get("goal_domain", "")
    selected_domain = domain.lower().strip()

    DOMAIN_TO_SKILL = {
        "python": "python",
        "java": "java",
        "c++": "cpp",
        "c language": "c",
        "web development": "web",
        "gen ai": "genai",
        "prompt engineering": "prompt"
    }

    skill = DOMAIN_TO_SKILL.get(selected_domain)

    if not skill:
        return jsonify({'error': f'No quiz available for {domain}'}), 400

    # -------------------------------
    # FILTER QUESTIONS BY SKILL
    # -------------------------------
    questions = []
    for q in QUESTION_BANK.values():
        if q.get("skill_tag", "").lower() == skill.lower():
            questions.append(q)

    # -------------------------------
    # SIMPLE 10 RANDOM QUESTIONS
    # -------------------------------
    # -------------------------------
# FIXED QUIZ GENERATION
# -------------------------------

# Always pick 10 normal questions
    if len(questions) >= 10:
        selected_questions = random.sample(questions, 10)
    else:
        selected_questions = questions


    # ✅ STORE IN SESSION
    question_ids = [q["question_id"] for q in selected_questions]
    session["pre_quiz_questions"] = question_ids

    print("DEBUG stored questions:", question_ids)
        # ✅ STORE QUESTIONS IN SESSION (CRITICAL FIX)
    question_ids = [q["question_id"] for q in selected_questions]
    session["pre_quiz_questions"] = question_ids

    print("DEBUG stored questions:", question_ids)

    if not selected_questions:
        return jsonify({'error': f'No questions available for {domain}'}), 400

    random.shuffle(selected_questions)
    is_post = request.args.get('post') == '1'

    quiz_key = 'post_quiz_questions' if is_post else 'pre_quiz_questions'

    session[quiz_key] = [q['question_id'] for q in selected_questions]
        # REMOVE correct answers before sending to frontend
    public_questions = [
            {k: q[k] for k in q if k != 'correct_choice'}
            for q in selected_questions
        ]

    return jsonify({'questions': public_questions})

@app.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    try:
        payload = request.get_json() or {}

        user_id = payload.get('user_id')
        answers = payload.get('answers', {})
        is_post = bool(payload.get('post', False))

        user = USERS.get(user_id)

        if not user:
            return jsonify({'error': 'user not found'}), 404

        # ✅ STORE LANGUAGE + STYLE PER COURSE (FINAL FIX)
        course_id = user.get("goal_domain", "").lower().replace(" ", "_")

        if "user_courses" not in user:
            user["user_courses"] = {}

        if course_id not in user["user_courses"]:
            user["user_courses"][course_id] = {}

        user["user_courses"][course_id]["language"] = payload.get("language", "english").lower()
        user["user_courses"][course_id]["style"] = payload.get("preferred_style", "practical").lower()

        print("🆕 SAVED COURSE DATA:", user["user_courses"][course_id])
        # ✅ SINGLE CLEAN UPDATE (ONLY ONCE)
        user["user_language"] = payload.get("language", user.get("user_language", "english")).lower()
        user["preferred_style"] = payload.get("preferred_style", user.get("preferred_style", "practical")).lower()

        print("🆕 UPDATED LANGUAGE:", user["user_language"])
        print("🆕 UPDATED STYLE:", user["preferred_style"])
        # Basic validation
        if not isinstance(answers, dict):
            return jsonify({'error': 'answers must be a dictionary'}), 400

        # evaluate level and score
        quiz_key = 'post_quiz_questions' if is_post else 'pre_quiz_questions'
        total_question_ids = session.get(quiz_key, [])
        level, score_pct = detect_level(answers, total_question_ids)

# --- initial (pre) quiz ---
        if not is_post:

            user['initial_level'] = level
            user['initial_score'] = score_pct
            user['detected_level'] = level
            user['score_pct'] = score_pct

            course_id = request.args.get("course_id")

            if not course_id:
                course_id = user.get("goal_domain", "Python").lower().replace(" ", "_")

            course = user.get("user_courses", {}).get(course_id)

            if "user_courses" not in user:
                user["user_courses"] = {}

            user["user_courses"][course_id] = {
                "current_level": level,
                "completed_levels": [],
                "status": "in_progress"
            }

            # Generate roadmap
            roadmap = generate_roadmap_for_user(user)
            roadmap_id = str(uuid.uuid4())[:8]

            ROADMAPS[roadmap_id] = {
                'roadmap_id': roadmap_id,
                'user_id': user_id,
                'generated_on': datetime.utcnow().isoformat(),
                'roadmap': roadmap,
                'detected_level': level,
                'score_pct': score_pct
            }

            user['last_roadmap_id'] = roadmap_id

            # -------- FIXED REVIEW LOGIC ----------
            review = []

            for qid, chosen in answers.items():
                q = QUESTION_BANK.get(qid)
                if not q:
                    continue

                review.append({
                    "question": q.get("text"),
                    "choices": q.get("choices"),
                    "correct_choice": int(q.get("correct_choice")),
                    "user_choice": int(chosen) if str(chosen).isdigit() else None
                })

            return jsonify({
            "status": "ok",
            "score_pct": score_pct,
            "roadmap_id": roadmap_id,
        })

        # --- post quiz (Mastery Unlock System) ---

        course_id = user.get("goal_domain", "Python").lower().replace(" ", "_")
        course = user.get("user_courses", {}).get(course_id)

        if not course:
            return jsonify({"error": "Course not initialized"}), 400

        current_level = course.get("current_level", "beginner")
        level_order = ["beginner", "intermediate", "advanced"]

        user['post_level'] = level
        user['post_score'] = score_pct

        if score_pct >= 60:
            current_index = level_order.index(current_level)

            if current_level not in course["completed_levels"]:
                course["completed_levels"].append(current_level)
                # -------- BADGE SYSTEM --------
            if "badges" not in user:
                user["badges"] = []

            badge_map = {
                "beginner": "🥉 Bronze Badge",
                "intermediate": "🥈 Silver Badge",
                "advanced": "🥇 Gold Badge"
            }

            earned_badge = badge_map.get(current_level)

            if earned_badge and earned_badge not in user["badges"]:
                user["badges"].append(earned_badge)

            if current_index < len(level_order) - 1:
                next_level = level_order[current_index + 1]
                course["current_level"] = next_level
                user['detected_level'] = next_level   # ✅ SYNC LEVEL
                message = f"{current_level.capitalize()} passed! {next_level.capitalize()} unlocked!"
            else:
                course["status"] = "completed"
                user['detected_level'] = "advanced"   # ✅ FINAL SYNC
                message = "🎉 Course Completed Successfully!"

        else:
            message = "You must score at least 60% to unlock next level."

        # regenerate roadmap based on updated current_level
        roadmap = generate_roadmap_for_user(user)
        roadmap_id = str(uuid.uuid4())[:8]

        ROADMAPS[roadmap_id] = {
            'roadmap_id': roadmap_id,
            'user_id': user_id,
            'generated_on': datetime.utcnow().isoformat(),
            'roadmap': roadmap,
            'detected_level': course["current_level"],
            'score_pct': score_pct
        }

        user['last_roadmap_id'] = roadmap_id

        return jsonify({
            'status': 'ok',
            'roadmap_id': roadmap_id,
            'detected_level': course["current_level"],
            'score_pct': score_pct,
            'message': message
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'server exception', 'details': str(e)}), 500
    
@app.route("/api/module/complete", methods=["POST"])
def complete_module():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user_id = session["user_id"]
    user = USERS.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    course_id = user.get("goal_domain", "Python").lower().replace(" ", "_")
    level = request.json.get("level")

    course = user["user_courses"].get(course_id)

    if not course:
        return jsonify({"error": "Course not initialized"}), 400

    if level not in course["completed_levels"]:
        course["completed_levels"].append(level)

    return jsonify({
        "status": "success",
        "message": f"{level} marked as completed. Take post quiz to unlock next level."
    })

@app.route('/api/roadmap/<roadmap_id>')
def api_get_roadmap(roadmap_id):
    user_id = request.args.get('user_id')
    course_id = request.args.get('course_id')

    rm = ROADMAPS.get(roadmap_id)
    if not rm:
        return jsonify({'error': 'roadmap not found'}), 404

    return jsonify({
        'roadmap': rm['roadmap'],
        'detected_level': rm['detected_level'],
        'score_pct': rm['score_pct'],
        'course_id': course_id
    })
# ================= REVIEW API =================
@app.route('/api/review', methods=['POST'])
def review_answers():
    data = request.json

    user_id = data.get("user_id")
    answers = data.get("answers", {})
    question_ids = data.get("question_ids", [])

    review = []

    for qid in question_ids:
        q = QUESTION_BANK.get(qid)
        if not q:
            continue

        review.append({
            "question": q["text"],
            "correct": q["choices"][q["correct_choice"]],
            "your_answer": q["choices"][int(answers.get(qid, -1))] if answers.get(qid) else "Not answered"
        })

    return jsonify({"review": review})
@app.route('/api/admin')
def api_admin():
    return jsonify({'users': USERS, 'roadmaps': ROADMAPS, 'catalog': MODULE_CATALOG, 'questions': QUESTION_BANK})
@app.route('/api/my-progress')
def api_my_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user_id']
    user = USERS.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    course_id = user.get("goal_domain", "Python").lower().replace(" ", "_")
    course = user.get("user_courses", {}).get(course_id)

    if not course:
        return jsonify({'progress': 0})

    level_order = ["beginner", "intermediate", "advanced"]
    completed = len(course.get("completed_levels", []))
    total = len(level_order)

    progress_pct = int((completed / total) * 100)
    badges = []

    completed_levels = course.get("completed_levels", [])

    # Badges for completed levels
    for lvl in completed_levels:
        if lvl == "beginner":
            badges.append("🥉 Bronze")
        elif lvl == "intermediate":
            badges.append("🥈 Silver")
        elif lvl == "advanced":
            badges.append("🥇 Gold")

    # 🔥 Handle direct placement in pre-quiz
    initial_level = user.get("initial_level")

    if initial_level == "intermediate":
        if "🥉 Bronze" not in badges:
            badges.append("🥉 Bronze")

    elif initial_level == "advanced":
        if "🥉 Bronze" not in badges:
            badges.append("🥉 Bronze")
        if "🥈 Silver" not in badges:
            badges.append("🥈 Silver")

    # 🔥 If course completed → ensure Gold badge
    if course.get("status") == "completed":
        if "🥇 Gold" not in badges:
            badges.append("🥇 Gold")

    return jsonify({
    "course": course_id,
    "current_level": course["current_level"],
    "status": course["status"],
    "progress_pct": progress_pct,
    "last_roadmap_id": user.get("last_roadmap_id"),
    "user_id": user_id,
    "badges": badges
})
@app.route('/api/my-courses')
def api_my_courses():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user_id']
    user = USERS.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    courses_data = []
    level_order = ["beginner", "intermediate", "advanced"]

    for course_id, course in user.get("user_courses", {}).items():

        completed = len(course.get("completed_levels", []))
        total = len(level_order)
        progress_pct = int((completed / total) * 100)

        courses_data.append({
            "course_id": course_id,
            "current_level": course.get("current_level"),
            "status": course.get("status"),
            "progress_pct": progress_pct,
            "last_roadmap_id": user.get("last_roadmap_id"),
            "user_id": user_id
        })

    return jsonify({
        "courses": courses_data
    })
@app.route("/certificate")
def generate_certificate():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user = USERS.get(user_id)

    if not user:
        return redirect(url_for("login"))

    course_id = user.get("goal_domain", "Course")
    course_key = course_id.lower().replace(" ", "_")
    course = user.get("user_courses", {}).get(course_key)

    if not course or course.get("status") != "completed":
        return "Course not completed yet."

    name = user.get("name", "Learner")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=26,
        textColor=colors.darkblue,
        alignment=1,
        spaceAfter=20
    )

    center_style = ParagraphStyle(
        'CenterStyle',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=12
    )

    elements.append(Spacer(1, 1.5 * inch))
    elements.append(Paragraph("🎉 CERTIFICATE OF COMPLETION 🎉", title_style))
    elements.append(HRFlowable(width="70%", thickness=2))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("This is proudly presented to", center_style))
    elements.append(Paragraph(name, styles['Heading2']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(
        f"For successfully completing the {course_id} course",
        center_style
    ))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(
        f"Date: {datetime.utcnow().strftime('%d %B %Y')}",
        center_style
    ))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Course_Certificate.pdf",
        mimetype="application/pdf"
    )
@app.route('/analytics')
def analytics_page():
    if session.get('role') != 'admin':
        return "Access Denied. Admins Only.", 403
    return render_template_string(ANALYTICS_HTML)


@app.route('/api/analytics')
def api_analytics():
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    total_users = len(USERS)
    total_roadmaps = len(ROADMAPS)

    scores = []
    completed = 0
    level_count = {"beginner":0, "intermediate":0, "advanced":0}
    domain_count = {}

    for user in USERS.values():
        if user.get("score_pct") is not None:
            scores.append(user.get("score_pct"))

        domain = user.get("goal_domain", "Unknown")
        domain_count[domain] = domain_count.get(domain, 0) + 1

        level = user.get("detected_level", "beginner")
        if level in level_count:
            level_count[level] += 1

        course_id = domain.lower().replace(" ", "_")
        course = user.get("user_courses", {}).get(course_id)
        if course and course.get("status") == "completed":
            completed += 1

    avg_score = round(sum(scores)/len(scores),2) if scores else 0
    completion_rate = round((completed/total_users)*100,2) if total_users else 0

    return jsonify({
        "total_users": total_users,
        "total_roadmaps": total_roadmaps,
        "avg_score": avg_score,
        "completion_rate": completion_rate,
        "domain_distribution": domain_count,
        "level_distribution": level_count
    })
COURSES_HTML = '''
<!doctype html>
<html>
<head>
  <title>My Courses</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen p-6">

<h1 class="text-2xl font-bold mb-6">📚 My Courses</h1>

<div id="coursesContainer" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>

<script>
async function reviewQuiz() {
    console.log("🔥 REVIEW CLICKED");

    const answers = {};

    document.querySelectorAll('input[type=radio]:checked').forEach(el => {
        answers[el.name] = el.value;
    });

    const res = await fetch('/api/review', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            user_id: new URLSearchParams(window.location.search).get("user_id"),
            answers: answers,
            question_ids: Object.keys(answers)
        })
    });

    const data = await res.json();

    console.log("🔥 REVIEW RESPONSE:", data);

    alert(JSON.stringify(data.review, null, 2));
}
async function loadCourses(){
  const res = await fetch('/api/my-courses');
  const data = await res.json();

  if(data.error){
      document.getElementById('coursesContainer').innerHTML =
        "<div class='text-red-500'>Not logged in</div>";
      return;
  }

  const container = document.getElementById('coursesContainer');
  container.innerHTML = '';

  data.courses.forEach(course => {

    const card = document.createElement('div');
    card.className = 'bg-white p-6 rounded-xl shadow';

    card.innerHTML = `
      <h2 class="text-lg font-semibold">${course.course_id}</h2>
      <div class="text-sm text-gray-600 mt-1">
        Current Level: <strong>${course.current_level}</strong>
      </div>
      <div class="text-sm text-gray-600">
        Status: <strong>${course.status}</strong>
      </div>

      <div class="mt-3">
        <div class="w-full bg-gray-200 rounded-full h-4">
          <div class="bg-gradient-to-r from-indigo-500 to-purple-600 
            h-4 rounded-full text-xs text-white text-center 
            transition-all duration-1000 ease-out"
     style="width:0%"
     data-progress="${course.progress_pct}">
     0%
</div>
        </div>
      </div>

      <div class="mt-4 flex gap-3">
        <a href="/roadmap?user_id=${course.user_id}&roadmap_id=${course.last_roadmap_id}&course_id=${course.course_id}"
           class="px-3 py-2 bg-green-600 text-white rounded-md text-sm">
           ▶ Continue
        </a>

        ${course.status === "completed" ? `
        <a href="/certificate"
           class="px-3 py-2 bg-indigo-600 text-white rounded-md text-sm">
           📜 Certificate
        </a>` : ''}
      </div>
    `;

    container.appendChild(card);
  });
  // Animate progress bars AFTER cards are created
setTimeout(() => {
  container.querySelectorAll('[data-progress]').forEach(bar => {
    const value = bar.getAttribute('data-progress');
    bar.style.width = value + '%';
    bar.innerText = value + '%';
  });
}, 100);
}

loadCourses();
</script>

</body>
</html>
'''
ANALYTICS_HTML = '''
<!doctype html>
<html>
<head>
  <title>Analytics Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50 min-h-screen p-6">

<h1 class="text-2xl font-bold mb-6">📊 Analytics Dashboard</h1>

<div id="metrics" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div class="bg-white p-4 rounded shadow">
  <canvas id="levelChart" style="max-height:300px;"></canvas>
</div>

<div class="bg-white p-4 rounded shadow">
  <canvas id="domainChart" style="max-height:300px;"></canvas>
</div>
</div>

<script>
async function loadAnalytics(){
  const res = await fetch('/api/analytics');
  const data = await res.json();

  document.getElementById('metrics').innerHTML = `
    <div class="p-4 bg-white rounded shadow">
      <div class="text-sm text-gray-500">Total Users</div>
      <div class="text-xl font-bold">${data.total_users}</div>
    </div>
    <div class="p-4 bg-white rounded shadow">
      <div class="text-sm text-gray-500">Roadmaps Generated</div>
      <div class="text-xl font-bold">${data.total_roadmaps}</div>
    </div>
    <div class="p-4 bg-white rounded shadow">
      <div class="text-sm text-gray-500">Avg Quiz Score</div>
      <div class="text-xl font-bold">${data.avg_score}%</div>
    </div>
    <div class="p-4 bg-white rounded shadow">
      <div class="text-sm text-gray-500">Completion Rate</div>
      <div class="text-xl font-bold">${data.completion_rate}%</div>
    </div>
  `;

new Chart(document.getElementById('levelChart'), {
  type: 'pie',
  data: {
    labels: Object.keys(data.level_distribution),
    datasets: [{
      data: Object.values(data.level_distribution)
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false
  }
});

new Chart(document.getElementById('domainChart'), {
  type: 'bar',
  data: {
    labels: Object.keys(data.domain_distribution),
    datasets: [{
      label: 'Users per Domain',
      data: Object.values(data.domain_distribution)
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false
  }
});
}

loadAnalytics();
</script>
</body>
</html>
'''
if __name__ == "__main__":
    app.run(debug=True)