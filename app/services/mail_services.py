from app.core.mail import mail,create_message
from fastapi import BackgroundTasks


class Mail:
    def send_signup_mail(self,token:str,otp:str, recipients:list[str],bg_tasks:BackgroundTasks)->None:
        
        subject = "Verify Your Olympiad Account"
        
        link=f"http://127.0.0.1:8000/user/verify-signup/{token}"
        
        body = f"""<p>Your OTP is: </p> <p>{otp}</p> <a href="{link}"> Click here to verify:</a> <p>{link}</p><p>This OTP expires in 10 minutes.</p>"""
        
        message = create_message(subject,recipients,body)
        
        bg_tasks.add_task(mail.send_message,message)
        
        
    def send_reset_password_mail(self,token:str,recipients:list[str],bg_tasks:BackgroundTasks) -> None:
        
        subject = "Reset Password"

        link=f"http://127.0.0.1:8000/user/reset-password/{token}"
        
        body=f"""<p>We received a request to reset your Olympiad account password.</p><p>Click the link below to reset your password:</p><a href="{link}">Reset Password</a><p>If you did not request a password reset, please ignore this email.</p><p>This link expires in 10 minutes.</p>"""
          
        message = create_message(subject,recipients,body)
        
        bg_tasks.add_task(mail.send_message,message)
        