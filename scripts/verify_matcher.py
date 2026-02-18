import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_matching_scenarios():
    candidates = [
        {"name": "Alice ICU", "skill_description": "Registered nurse with 4 years ICU experience and German A2 level", "experience": 4, "location": "India"},
        {"name": "Bob General", "skill_description": "General ward nurse with experience in elderly care, no German language skills", "experience": 3, "location": "Philippines"},
        {"name": "Charlie Electrician", "skill_description": "Professional electrician with industrial wiring experience and solar panel installation", "experience": 10, "location": "Germany"},
        {"name": "Dinesh Plumber", "skill_description": "Experienced plumber specializing in pipe repair, water systems, and emergency maintenance", "experience": 7, "location": "India"},
        {"name": "Elena Sales", "skill_description": "Global sales lead with experience in SaaS, B2B marketing, and closing high-ticket deals", "experience": 8, "location": "Germany"},
        {"name": "Frank Marketing", "skill_description": "Content strategist and social media manager, expert in brand growth and SEO copy", "experience": 2, "location": "USA"},
        {"name": "George Warehouse", "skill_description": "Warehouse supervisor, expert in inventory management, forklift operation, and safety compliance", "experience": 5, "location": "UK"},
        {"name": "Hannah Chef", "skill_description": "Executive chef specialized in French and Italian cuisine, menu design, and kitchen leadership", "experience": 12, "location": "France"},
        {"name": "Ian Python", "skill_description": "Junior backend developer, proficient in Python, FastAPI, and PostgreSQL. Loves AI research.", "experience": 1, "location": "India"},
        {"name": "Julia Caregiver", "skill_description": "Compassionate caregiver for elderly, certified in first aid and medication management.", "experience": 5, "location": "South Africa"},
        {"name": "Kevin Trucker", "skill_description": "Long-haul truck driver with clean CDL and experience in heavy vehicle logistics.", "experience": 15, "location": "Canada"},
        {"name": "Liam Carpenter", "skill_description": "Skilled carpenter specialized in custom furniture, wood framing, and interior design.", "experience": 9, "location": "Australia"},
        {"name": "Mia DataEntry", "skill_description": "Accurate data entry specialist with high typing speed and expertise in Microsoft Excel.", "experience": 3, "location": "Philippines"},
        {"name": "Noah Security", "skill_description": "Licensed security officer with experience in surveillance and emergency response.", "experience": 6, "location": "Nigeria"},
        {"name": "Olivia UIUX", "skill_description": "Creative UI/UX designer focused on user-centric web and mobile app interfaces.", "experience": 4, "location": "Germany"},
        {"name": "Peter Welder", "skill_description": "Certified industrial welder with expertise in MIG, TIG, and structural steel fabrication.", "experience": 11, "location": "USA"},
        {"name": "Quinn HR", "skill_description": "HR professional specialized in talent acquisition, employee relations, and payroll.", "experience": 7, "location": "UK"},
        {"name": "Ryan Delivery", "skill_description": "Efficient delivery driver with knowledge of local routes and excellent customer service.", "experience": 2, "location": "India"},
        {"name": "Sophia Java", "skill_description": "Senior Java developer with 10 years in enterprise software and microservices architecture.", "experience": 10, "location": "Kenya"}
    ]
    
    print("\nRegistering Candidates...")
    for c in candidates:
        print(f"Adding {c['name']}...", end="", flush=True)
        response = requests.post(f"{BASE_URL}/candidates/", json=c)
        if response.status_code == 200:
            print(" OK")
        else:
            print(f"FAILED: {response.text}")

    jobs = [
        {
            "title": "Staff Nurse (ICU)", 
            "country": "Germany", 
            "description": "Searching for ICU nurses for a clinic in Berlin. German proficiency is a must."
        },
        {
            "title": "Field Technician", 
            "country": "Germany", 
            "description": "Looking for experts in electrical wiring and renewable energy installations (solar)."
        },
        {
            "title": "Business Development Manager", 
            "country": "Remote", 
            "description": "Need a result-driven leader to grow our software sales and manage client relationships."
        },
        {
            "title": "Head Chef", 
            "country": "Switzerland", 
            "description": "Waitstaff and kitchen leads needed for a high-end restaurant focused on European cuisine."
        },
         {
            "title": "Junior Backend Engineer", 
            "country": "Remote", 
            "description": "Help us build modern APIs using Python and modern frameworks."
        }
    ]
    
    for i, j in enumerate(jobs, 1):
        print(f"\nTEST CASE {i}: {j['title']} in {j['country']}")
        print(f"   Description: {j['description']}")
        
        # Create Job
        job_response = requests.post(f"{BASE_URL}/jobs/", json=j)
        if job_response.status_code != 200:
            print(f"   FAILED to create job: {job_response.text}")
            continue
            
        job_id = job_response.json()["id"]

        # Get Matches
        match_response = requests.get(f"{BASE_URL}/jobs/{job_id}/match")
        matches = match_response.json()

        print("TOP RANKED MATCHES:")
        for idx, m in enumerate(matches, 1):
            print(f"   {idx}. Candidate ID: {m['candidateId']}, Similarity: {m['similarityScore']:.4f}, Exp: {m['experience']}")

if __name__ == "__main__":
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
        test_matching_scenarios()
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Please run 'python3 main.py' first.")
