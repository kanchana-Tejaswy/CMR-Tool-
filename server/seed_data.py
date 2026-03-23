import requests

try:
    print("Seeding leads...")
    res1 = requests.post("http://localhost:8000/leads/webhook", json={
        "first_name": "Bruce", 
        "last_name": "Wayne", 
        "email": "bruce@wayne.com", 
        "company": "Wayne Enterprises Inc", 
        "source": "Website", 
        "intent": "Need enterprise pricing ASAP"
    })
    print(res1.json())
    
    res2 = requests.post("http://localhost:8000/leads/webhook", json={
        "first_name": "Clark", 
        "last_name": "Kent", 
        "email": "clark@planet.com", 
        "company": "Daily Planet", 
        "source": "Organic", 
        "intent": "Just looking"
    })
    print(res2.json())

    print("Seeding deals...")
    d1 = requests.post("http://localhost:8000/deals/", json={
        "title": "Enterprise Deal", 
        "value": 150000, 
        "stage": "Lead", 
        "contact_id": 1
    })
    print(d1.json())
    
    d2 = requests.post("http://localhost:8000/deals/", json={
        "title": "Website Redesign", 
        "value": 5000, 
        "stage": "Qualified", 
        "contact_id": 2
    })
    print(d2.json())

except Exception as e:
    print(f"Error: {e}")
