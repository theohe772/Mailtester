import random
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# Load template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('js/email_template.html')

# Där våra filer skall ligga
os.makedirs("generated_emails", exist_ok=True)

# All vår data, satte in lite manuellt men kan legit ba importera listor
namn = [""]
domains_legit = ["microsoft.com", "company.com"]
domains_fake = ["micr0soft-secure.com", "company-support.co", "secure-login-company.com", "ao3.com"]

# Ba fylla på med det vi behöver
subjects = [
    "Password Expiration Notice",
    "Unusual Sign-in Attempt",
    "Account Verification Required"
]

#Exempeltexter på prompt vi vill visa, ämnen etc.
bodies = [
    "Your account requires immediate attention.",
    "We detected unusual activity on your account.",
    "Your password will expire today."
]

#Konsekvenser/Varningar
warnings = [
    "Failure to act may result in account suspension.",
    "Immediate action is required to avoid lockout.",
    "Your account will be disabled if ignored."
]

#Denna kan vi ändra hur mycket som helst, data innehåller alla datapunkter vi kan ändra
#
def generate_email(i):
    is_phishing = random.choice([True, False])

    sender_domain = random.choice(domains_fake if is_phishing else domains_legit)

    data = {
        "sender_name": "IT Support",
        "sender_email": f"it-support@{sender_domain}",
        "recipient_email": "user@company.com",
        "recipient_name": random.choice(namn),
        "date": datetime.now().strftime("%B %d, %Y"),
        "subject": random.choice(subjects),
        "body_text": random.choice(bodies),
        "show_warning": random.choice([True, False]),
        "warning_text": random.choice(warnings),
        "link_url": f"http://{random.choice(domains_fake if is_phishing else domains_legit)}/reset",
        "button_text": "Update Password",
        "closing_text": "Regards,<br>IT Support Team"
    }

    rendered = template.render(data)

    label = "phish" if is_phishing else "legit"
    filename = f"generated_emails/email_{i}_{label}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(rendered)

# Generera mails 
for i in range(100):
    generate_email(i)

print("Emails saved in /generated_emails")