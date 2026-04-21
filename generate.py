import random
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Load template, Behöver fortfarande implementeras, ligger lokalt temporärt
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('email_template.html')

#Där våra filer skall ligga
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# All vår data, satte in lite manuellt men kan legit ba importera listor, generic genererade fakedomains,
names = ["namn1", "namn2", "namn3", "namn4"]

legit_domains = ["microsoft.com", "company.com"]
fake_domains = ["micr0soft-secure.com", "verify-company.net", "secure-login.co"]

# Ba fylla på med det vi behöver
subjects = [
    "Password Expiration Notice",
    "Unusual Sign-in Attempt",
    "Account Verification Required"
]

# Difficulty config
def generate_email_data(difficulty):
    is_phish = difficulty != "easy" and random.choice([True, False])

    domain = random.choice(fake_domains if is_phish else legit_domains)

    return {
        "sender_name": "IT Support",
        "sender_email": f"it-support@{domain}",
        "recipient_email": "user@company.com",
        "recipient_name": random.choice(names),
        "date": datetime.now().strftime("%B %d, %Y"),
        "subject": random.choice(subjects),
        "body_text": "Your account requires attention.",
        "show_warning": difficulty != "easy",
        "warning_text": "Failure to act may result in account suspension.",
        "link_url": f"http://{domain}/reset",
        "button_text": "Update Password",
        "closing_text": "Regards,<br>IT Support Team"
    }

#Denna kan vi ändra hur mycket som helst, data innehåller alla datapunkter vi kan ändra
#la in lite random exempel för att se konceptet, allt callar konstant rand för att plocka ur dataset.
emails = []
difficulties = ["easy", "medium", "hard", "dodgy", "very_hard"]

for i, diff in enumerate(difficulties, start=1):
    data = generate_email_data(diff)

    filename = f"email_{i}_{diff}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.render(data))

    emails.append((filename, diff))

# Index.html
index_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Email Test Menu</title>
<style>
body { font-family: Arial; background:#f3f2f1; padding:40px; }
.container { max-width:500px; margin:auto; background:#fff; padding:20px; border:1px solid #ccc; }
a { display:block; margin:10px 0; padding:12px; text-decoration:none; color:white; border-radius:4px; text-align:center; }
.easy { background:#107c10; }
.medium { background:#ffaa44; color:black; }
.hard { background:#0078d4; }
.dodgy { background:#d83b01; }
</style>
</head>
<body>
<div class="container">
<h1>Email Scenarios</h1>
"""

for filename, diff in emails:
    index_html += f'<a class="{diff}" href="{filename}">{diff.title()}</a>\n'

index_html += """
</div>
</body>
</html>
"""

with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("Done. Open output/index.html")