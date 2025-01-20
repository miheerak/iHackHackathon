from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import ReportedContent

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()

def add_reported_content(content, blockchain_hash):
    flagged_content = ReportedContent(content=content, blockchain_hash=blockchain_hash)
    session.add(flagged_content)
    session.commit()
