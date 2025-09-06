import os
import smtplib
import ssl
import logging
from datetime import datetime
from email.message import EmailMessage
from typing import Optional, List, Union, Dict, Any

class EmailService:
    def __init__(self, db):
        """
        Initialize the email service with database connection.

        Args:
            db: Database connection object
        """
        self.db = db
        self._smtp_host = "smtp.gmail.com"
        self._smtp_port = 587
        self._email = None
        self._app_password = None
        self._validate_credentials()

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_credentials(self) -> None:
        """Validate Gmail credentials on initialization"""
        self._email = os.getenv("GMAIL_EMAIL_ADDRESS")
        self._app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not self._email or not self._app_password:
            raise ValueError(
                "Missing required environment variables: GMAIL_EMAIL_ADDRESS and/or GMAIL_APP_PASSWORD"
            )

    def _normalize_emails(self, emails: Union[str, List[str], None]) -> List[str]:
        """
        Normalize email addresses to a consistent list format.

        Args:
            emails: Email addresses as string (comma-separated) or list

        Returns:
            List of normalized email addresses
        """
        if not emails:
            return []
        if isinstance(emails, str):
            return [email.strip() for email in emails.split(",") if email.strip()]
        return [email.strip() for email in emails if email.strip()]

    def _create_email_message(
            self,
            recipients: List[str],
            subject: str,
            content: str,
            content_type: str,
            sender_name: str,
            cc_list: List[str],
            bcc_list: List[str]
    ) -> EmailMessage:
        """Create and configure the email message"""
        msg = EmailMessage()

        # Set sender
        msg["From"] = f"{sender_name} <{self._email}>"

        # Set recipients
        msg["To"] = ", ".join(recipients)

        # Set CC if provided
        if cc_list:
            msg["Cc"] = ", ".join(cc_list)

        # Set subject
        msg["Subject"] = subject

        # Set content
        if content_type.lower() == "html":
            msg.set_content(content, subtype="html")
        else:
            msg.set_content(content)

        return msg

    def send_email(
            self,
            recipient: Union[str, List[str]],
            subject: str,
            content: str,
            content_type: str = "plain",
            sender_name: Optional[str] = None,
            cc: Optional[Union[str, List[str]]] = None,
            bcc: Optional[Union[str, List[str]]] = None,
            timeout: int = 30
    ) -> bool:
        """
        Send an email using Gmail SMTP.

        Args:
            recipient: Email address(es) of the recipient(s)
            subject: Email subject line
            content: Email content/body
            content_type: Content type ('plain' or 'html')
            sender_name: Custom sender name
            cc: CC recipients
            bcc: BCC recipients
            timeout: SMTP connection timeout in seconds

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        start_time = datetime.now()

        # Validate inputs
        if not recipient or not subject or content is None:
            raise ValueError("Recipient, subject, and content are required")

        # Normalize email lists
        recipients = self._normalize_emails(recipient)
        cc_list = self._normalize_emails(cc)
        bcc_list = self._normalize_emails(bcc)
        all_recipients = recipients + cc_list + bcc_list

        if not recipients:
            raise ValueError("At least one valid recipient is required")

        # Set default sender name
        sender_name = sender_name or "מערכת המכרזים TendySys"

        try:
            # Create email message
            msg = self._create_email_message(
                recipients, subject, content, content_type,
                sender_name, cc_list, bcc_list
            )

            # Create SSL context
            context = ssl.create_default_context()

            # Send email
            with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=timeout) as server:
                server.starttls(context=context)
                server.login(self._email, self._app_password)
                server.send_message(msg, to_addrs=all_recipients)

            # Log success
            self.logger.info(f"Email sent successfully to {len(all_recipients)} recipient(s): {subject}")

            return True

        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"SMTP authentication failed: {e}")
            raise

        except smtplib.SMTPRecipientsRefused as e:
            self.logger.error(f"Recipients refused: {e}")
            raise

        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            raise

        except Exception as e:
            self.logger.error(f"Unexpected error sending email: {e}")
            raise

    def send_bulk_email(
            self,
            recipients: List[str],
            subject: str,
            content: str,
            content_type: str = "plain",
            sender_name: Optional[str] = None,
            batch_size: int = 50,
            delay_between_batches: float = 1.0
    ) -> Dict[str, Any]:
        """
        Send bulk emails in batches to avoid rate limiting.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject line
            content: Email content/body
            content_type: Content type ('plain' or 'html')
            sender_name: Custom sender name
            batch_size: Number of emails to send per batch
            delay_between_batches: Delay in seconds between batches

        Returns:
            Dict containing success/failure statistics
        """
        import time

        total_recipients = len(recipients)
        successful_sends = 0
        failed_sends = 0
        errors = []

        # Process recipients in batches
        for i in range(0, total_recipients, batch_size):
            batch = recipients[i:i + batch_size]

            try:
                success = self.send_email(
                    recipient=batch,
                    subject=subject,
                    content=content,
                    content_type=content_type,
                    sender_name=sender_name
                )

                if success:
                    successful_sends += len(batch)
                else:
                    failed_sends += len(batch)

            except Exception as e:
                failed_sends += len(batch)
                errors.append(f"Batch {i // batch_size + 1}: {str(e)}")
                self.logger.error(f"Failed to send batch {i // batch_size + 1}: {e}")

            # Add delay between batches (except for the last batch)
            if i + batch_size < total_recipients:
                time.sleep(delay_between_batches)

        result = {
            "total_recipients": total_recipients,
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "success_rate": successful_sends / total_recipients if total_recipients > 0 else 0,
            "errors": errors
        }

        self.logger.info(f"Bulk email completed: {successful_sends}/{total_recipients} sent successfully")
        return result

    def test_connection(self, username: Optional[str] = None) -> bool:
        """
        Test SMTP connection and authentication.

        Args:
            username: Username for logging

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=10) as server:
                server.starttls(context=context)
                server.login(self._email, self._app_password)

            print("""
                "Email service SMTP connection test successful",
                level="INFO",
                username=username
                """
                  )
            return True

        except Exception as e:
            print("""
                f"Email service SMTP connection test failed: {str(e)}",
                level="ERROR",
                username=username
            """
                  )
            return False


# Example usage:
if __name__ == "__main__":
    # Example of how to integrate with your existing app utilities
    from db.db import get_db
    from dotenv import load_dotenv

    load_dotenv()
    db = get_db()
    email_service = EmailService(db)

    # Test connection
    if email_service.test_connection():
        print("Email service is ready!")

        # Send single email
        subject = "מכרז חדש: הגש הצעה"

        offer_email_html = """
        <!doctype html>
        <html lang="he" dir="rtl">
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <meta name="viewport" content="width=device-width">
            <title>מכרז חדש: הגש הצעה</title>
            <!-- פריהדר (טקסט תצוגה מקדימה בתיבת הדואר) -->
            <style>
              .preheader { display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0; overflow:hidden; mso-hide:all; }
              /* סגנונות בסיסיים לתאימות רחבה */
              body { margin:0; padding:0; background:#f5f7fa; }
              table { border-spacing:0; border-collapse:collapse; }
              img { border:0; line-height:100%; outline:none; text-decoration:none; }
              a { text-decoration:none; }
              .btn { background:#2563eb; color:#ffffff !important; padding:14px 24px; border-radius:8px; display:inline-block; font-weight:700; }
              .btn:hover { filter: brightness(1.05); }
              .container { width:100%; max-width:640px; margin:0 auto; }
              .card { background:#ffffff; border-radius:12px; box-shadow:0 2px 6px rgba(0,0,0,0.06); }
              .muted { color:#6b7280; }
              .small { font-size:13px; }
              @media screen and (max-width:600px) {
                .p-32 { padding:20px !important; }
              }
            </style>
          </head>
          <body style="direction:rtl; font-family: 'Segoe UI',Tahoma,Arial,Helvetica,sans-serif; color:#111827;">
            <span class="preheader">זוהי בקשה להגשת הצעה במערכת TendySys – לחץ/י כדי להגיש.</span>

            <table role="presentation" class="container" width="100%" aria-hidden="true">
              <tr><td style="height:24px">&nbsp;</td></tr>
              <tr>
                <td>
                  <table role="presentation" width="100%" class="card">
                    <tr>
                      <td class="p-32" style="padding:32px;">
                        <!-- כותרת -->
                        <h1 style="margin:0 0 10px; font-size:24px; line-height:1.3;">מכרז חדש: הגש/י הצעה</h1>
                        <p class="muted" style="margin:0 0 24px; line-height:1.7;">
                          שלום,
                          <br>
                          זוהי הזמנה להגשת הצעה למכרז חדש במערכת <strong>TendySys</strong>.
                        </p>

                        <!-- פרטי מכרז - אופציונלי: החלף משתנים אם יש -->
                        <table role="presentation" width="100%" style="margin:0 0 20px;">
                          <tr>
                            <td class="muted small" style="padding:0 0 6px;">
                              <strong>שם המכרז:</strong> {{tender_name|שם המכרז}}
                            </td>
                          </tr>
                          <tr>
                            <td class="muted small" style="padding:0 0 6px;">
                              <strong>מזהה:</strong> {{tender_id|—}}
                            </td>
                          </tr>
                          <tr>
                            <td class="muted small" style="padding:0 0 6px;">
                              <strong>מועד אחרון להגשה:</strong> {{deadline|—}}
                            </td>
                          </tr>
                        </table>

                        <!-- קריאה לפעולה -->
                        <table role="presentation" cellpadding="0" cellspacing="0">
                          <tr>
                            <td>
                              <a class="btn" href="https://tendysys.streamlit.app/offer_new" target="_blank" rel="noopener">
                                להגשת הצעה במערכת
                              </a>
                            </td>
                          </tr>
                        </table>

                        <!-- טקסט עזר -->
                        <p class="small muted" style="margin:20px 0 0; line-height:1.7;">
                          אם הכפתור לא נפתח, ניתן להעתיק את הקישור ולהדביק בדפדפן:
                          <br>
                          <a href="https://tendysys.streamlit.app/offer_new" target="_blank" style="word-break:break-all;">
                            https://tendysys.streamlit.app/offer_new
                          </a>
                        </p>

                        <!-- הערות ותמיכה (אופציונלי) -->
                        <p class="small muted" style="margin:16px 0 0;">
                          אנא ודא/י שההצעה כוללת את כל המסמכים הנדרשים לפני שליחה.
                        </p>

                        <hr style="border:none; border-top:1px solid #e5e7eb; margin:24px 0;">

                        <!-- חתימה -->
                        <p class="small muted" style="margin:0;">
                          תודה, <br>
                          צוות TendySys
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr><td style="height:24px">&nbsp;</td></tr>
              <tr>
                <td class="small muted" style="text-align:center;">
                  הודעה זו נשלחה אליך מאת מערכת TendySys.
                </td>
              </tr>
              <tr><td style="height:24px">&nbsp;</td></tr>
            </table>
          </body>
        </html>
        """

        try:

            success = email_service.send_email(
                recipient=["tamirzitman@gmail.com","yuvalsayag2@gmail.com"],
                subject=subject,
                content=offer_email_html,
                content_type="html"
            )
            print(f"Email sent: {success}")
        except Exception as e:
            print(f"Failed to send email: {e}")
