from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Bettor, Match, Transaction

engine = create_engine("sqlite:///betting.sqlite")

Session = sessionmaker(bind=engine)
session = Session()

def manage_bettors(session):
    while True:
        print("\n=== Bettor Management ===")
        print("1. Add Bettor")
        print("2. View All Bettors")
        print("3. Update Bettor")
        print("4. Delete Bettor")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            name = input("Enter bettor name: ").strip()
            bettor = Bettor(name=name)
            session.add(bettor)
            session.commit()
            print("Bettor added successfully with $100 in their wallet!")


        elif choice == "2":
            bettors = session.query(Bettor).all()
            for bettor in bettors:
                print(f"ID: {bettor.id}, Name: {bettor.name}, Wallet: ${bettor.wallet:.2f}")


        elif choice == "3":
            bettor_id = int(input("Enter bettor ID to update: "))
            bettor = session.query(Bettor).get(bettor_id)
            if bettor:
                bettor.name = input("Enter new name: ").strip()
                session.commit()
                print("Bettor updated successfully!")
            else:
                print("Bettor not found.")


        elif choice == "4":
            bettor_id = int(input("Enter bettor ID to delete: "))
            bettor = session.query(Bettor).get(bettor_id)
            if bettor:
                session.delete(bettor)
                session.commit()
                print("Bettor deleted successfully!")
            else:
                print("Bettor not found.")


        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")



def manage_matches(session):
    while True:
        print("\n=== Match Management ===")
        print("1. Add Match")
        print("2. View All Matches")
        print("3. Update Match")
        print("4. Delete Match")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            name = input("Enter match name (e.g., Team A vs Team B): ").strip()
            odds_team_a = float(input("Enter odds for Team A: "))
            odds_team_b = float(input("Enter odds for Team B: "))
            match = Match(name=name, odds_team_a=odds_team_a, odds_team_b=odds_team_b)
            session.add(match)
            session.commit()
            print("Match added successfully!")


        elif choice == "2":
            matches = session.query(Match).all()
            for match in matches:
                print(f"ID: {match.id}, Name: {match.name}, Team A Odds: {match.odds_team_a:.2f}, Team B Odds: {match.odds_team_b:.2f}")


        elif choice == "3":
            match_id = int(input("Enter match ID to update: "))
            match = session.query(Match).get(match_id)
            if match:
                match.name = input("Enter new match name: ").strip()
                match.odds_team_a = float(input("Enter new odds for Team A: "))
                match.odds_team_b = float(input("Enter new odds for Team B: "))
                session.commit()
                print("Match updated successfully!")
            else:
                print("Match not found.")


        elif choice == "4":
            match_id = int(input("Enter match ID to delete: "))
            match = session.query(Match).get(match_id)
            if match:
                session.delete(match)
                session.commit()
                print("Match deleted successfully!")
            else:
                print("Match not found.")


        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")


def place_bets(session):
    print("\n=== Place Bets ===")

    # Get the bettor
    try:
        bettor_id = int(input("Enter your Bettor ID: "))
        bettor = session.query(Bettor).get(bettor_id)
        if not bettor:
            print("Bettor not found.")
            return
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    # Display available matches
    matches = session.query(Match).all()
    if not matches:
        print("No matches available.")
        return
    print("Available Matches:")
    for match in matches:
        print(f"ID: {match.id}, Name: {match.name}, Team A Odds: {match.odds_team_a:.2f}, Team B Odds: {match.odds_team_b:.2f}")

    # Get the match to bet on
    try:
        match_id = int(input("Enter Match ID to bet on: "))
        match = session.query(Match).get(match_id)
        if not match:
            print("Match not found.")
            return
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    # Choose team to bet on
    team = input("Bet on Team A or Team B? (Enter A or B): ").strip().upper()
    if team not in ["A", "B"]:
        print("Invalid choice. Enter A or B.")
        return

    # Enter bet amount
    try:
        amount = float(input("Enter bet amount: "))
        if amount > bettor.wallet:
            print("Insufficient balance.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Update bettor's wallet and record transaction
    bettor.wallet -= amount
    transaction = Transaction(
        bettor_id=bettor.id,
        match_id=match.id,
        amount=amount,
        team_bet_on=team,
        status='pending'
    )
    session.add(transaction)
    session.commit()

    print(f"Bet placed successfully! ${amount:.2f} deducted from your wallet. Bet recorded for {match.name} on Team {team}.")

    

def main():
   
    session = Session()
    while True:
        print("\n=== Betting Management System ===")
        print("1. Manage Bettors")
        print("2. Manage Matches")
        print("3. Place Bets")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            manage_bettors(session)
        elif choice == "2":
            manage_matches(session)
        elif choice == "3":
            place_bets(session)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()