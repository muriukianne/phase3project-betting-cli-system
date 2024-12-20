def session():
    """Fixture to set up and tear down the database session."""
    create_tables() # Ensure tables are created
    session = Session()
    yield session
    session.close()

def test_add_bettor(session):
    """Test adding a bettor."""
    bettor = Bettor(name="John Doe", wallet=100.0)
    session.add(bettor)
    session.commit()
    
    retrieved = session.query(Bettor).filter_by(name="John Doe").first()
    assert retrieved is not None
    assert retrieved.wallet == 100.0

def test_view_all_bettors(session):
    """Test viewing all bettors."""
    bettors = session.query(Bettor).all()
    assert len(bettors) > 0 # At least one bettor should exist

def test_update_bettor(session):
    """Test updating a bettor's name."""
    bettor = session.query(Bettor).first()
    old_name = bettor.name
    bettor.name = "Updated Name"
    session.commit()
    
    updated = session.query(Bettor).filter_by(id=bettor.id).first()
    assert updated.name == "Updated Name"
    assert updated.name != old_name

def test_delete_bettor(session):
    """Test deleting a bettor."""
    bettor = Bettor(name="Temp Bettor")
    session.add(bettor)
    session.commit()
    
    session.delete(bettor)
    session.commit()
    
    deleted = session.query(Bettor).filter_by(name="Temp Bettor").first()
    assert deleted is None

def test_add_match(session):
    """Test adding a match."""
    match = Match(name="Team A vs Team B", odds_team_a=1.5, odds_team_b=2.0)
    session.add(match)
    session.commit()
    
    retrieved = session.query(Match).filter_by(name="Team A vs Team B").first()
    assert retrieved is not None
    assert retrieved.odds_team_a == 1.5
    assert retrieved.odds_team_b == 2.0

def test_place_bet(session):
    """Test placing a bet."""
    bettor = session.query(Bettor).first()
    match = session.query(Match).first()
    initial_wallet = bettor.wallet

    transaction = Transaction(
        bettor_id=bettor.id,
        match_id=match.id,
        amount=10.0,
        team_bet_on="a",
        status="pending"
    )
    bettor.wallet -= 10.0
    session.add(transaction)
    session.commit()
    
    retrieved_transaction = session.query(Transaction).filter_by(bettor_id=bettor.id).first()
    updated_bettor = session.query(Bettor).filter_by(id=bettor.id).first()
    
    assert retrieved_transaction is not None
    assert retrieved_transaction.amount == 10.0
    assert updated_bettor.wallet == initial_wallet - 10.0

def test_view_transactions(session):
    """Test viewing transaction history."""
    transactions = session.query(Transaction).all()
    assert len(transactions) > 0 # At least one transaction should exist

def test_delete_match(session):
    """Test deleting a match."""
    match = Match(name="Temporary Match", odds_team_a=1.2, odds_team_b=1.8)
    session.add(match)
    session.commit()
    
    session.delete(match)
    session.commit()
    
    deleted = session.query(Match).filter_by(name="Temporary Match").first()
    assert deleted is None