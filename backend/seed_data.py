from app.db.database import SessionLocal
from app.models.learn import Learn 

db = SessionLocal() 

topic1 = Learn(
    title="What is Git?",
    topic="Git",
    content="Git is a version control system that tracks changes to your code over time..."
)

topic2 = Learn(
    title="What is SQL?",
    topic="SQL",
    content="SQL (Structured Query Language) is the standard programming language used to manage, manipulate, and retireve data from relational database management systems(RDBMS)"
)

topic3 = Learn(
    title = "What is Linux?",
    topic = "Linux",
    content = "Linux is a free, open source operating system that bridges hardware and applications"
)

db.add(topic1)
db.add(topic2)
db.add(topic3)

db.commit()
db.close()