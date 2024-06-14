def referral_handler(referral_code, referred_id, data):
    if referral_code in data and referred_id != referral_code:
        data[referral_code]["referrals"] += 1
        print(f"User {referred_id} referred by {referral_code}")
    else:
        print(f"Invalid referral code {referral_code} or self-referral attempt by {referred_id}")
        