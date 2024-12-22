from sqlmodel import Session, select
from typing import List, Optional
from models import Term
from schemas import TermCreate, TermUpdate


def get_terms(session: Session) -> List[Term]:
    statement = select(Term)
    results = session.exec(statement).all()

    print(results)

    return results


def get_term(session: Session, keyword: str) -> Optional[Term]:
    statement = select(Term).where(Term.keyword == keyword)
    term = session.exec(statement).first()
    return term


def create_term(session: Session, term: TermCreate) -> Term:
    db_term = Term(keyword=term.keyword, description=term.description)
    session.add(db_term)
    session.commit()
    session.refresh(db_term)
    return db_term


def update_term(session: Session, keyword: str, term_update: TermUpdate) -> Optional[Term]:
    term = get_term(session, keyword)
    if not term:
        return None
    if term_update.description is not None:
        term.description = term_update.description
    session.add(term)
    session.commit()
    session.refresh(term)
    return term


def delete_term(session: Session, keyword: str) -> bool:
    term = get_term(session, keyword)
    if not term:
        return False
    session.delete(term)
    session.commit()
    return True
