import smtplib

EMAIL = "coderfrombr28@gmail.com"
PASSWORD = "pegboroikejlwayx"

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login(
    EMAIL,
    PASSWORD
)

server.sendmail(
    EMAIL,
    EMAIL,
    "Subject: Test\n\nHello"
)

server.quit()

print("DONE")