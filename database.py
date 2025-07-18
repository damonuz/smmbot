from collections import defaultdict

users = {}
balances = defaultdict(int)
referrals = defaultdict(list)
orders = []

def register_user(user_id, ref_id=None):
    if user_id not in users:
        users[user_id] = {"ref": ref_id}
        if ref_id and ref_id != user_id:
            balances[ref_id] += 100
            referrals[ref_id].append(user_id)

def add_order(user_id, category, service, link, quantity):
    orders.append({
        "user_id": user_id,
        "category": category,
        "service": service,
        "link": link,
        "quantity": quantity
    })
