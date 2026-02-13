from datetime import date
from sqlmodel import SQLModel, Session, create_engine
from app.models.models import Book, Member, BorrowingRecord

# Konfigurasi database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def seed_dummy_data():
    with Session(engine) as session:
        # 20 Books
        books = [
            Book(title=f"Book {i}", author=f"Author {i}", isbn=f"ISBN{i:05d}")
            for i in range(1, 21)
        ]

        # 15 Members
        members = [
            Member(name=f"Member {i}", email=f"member{i}@example.com")
            for i in range(1, 16)
        ]

        session.add_all(books + members)
        session.commit()

        # 15 Borrowing Records (linking books & members)
        borrowings = []
        for i in range(1, 16):
            borrowings.append(
                BorrowingRecord(
                    book_id=books[i % 20].id,   # ambil book secara bergilir
                    member_id=members[i % 15].id,  # ambil member secara bergilir
                    borrow_date=date(2026, 2, 13),
                    return_date=None if i % 2 == 0 else date(2026, 2, 20)
                )
            )

        session.add_all(borrowings)
        session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    seed_dummy_data()
    print("✅ Database & dummy data (20 books, 15 members, 15 borrowings) berhasil dibuat!")