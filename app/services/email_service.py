import os
import smtplib
import ssl
import logging
from datetime import datetime
from email.message import EmailMessage
from typing import Optional, List, Union, Dict, Any
from jinja2 import Template


class EmailService:
    def __init__(self, db, templates_dir):
        """
        Initialize the email service with database connection.

        Args:
            db: Database connection object
            templates_dir: Directory for email templates
        """
        self.db = db
        self._smtp_host = "smtp.gmail.com"
        self._smtp_port = 587
        self._email = None
        self._app_password = None
        self.templates_dir = templates_dir
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
            subject: str,
            content: str,
            recipient: Union[str, List[str]] = None,
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

        # Normalize email lists
        recipients = self._normalize_emails(recipient)
        cc_list = self._normalize_emails(cc)
        bcc_list = self._normalize_emails(bcc)
        all_recipients = recipients + cc_list + bcc_list

        if not all_recipients:
            raise ValueError("At least one valid recipient is required")

        # Validate inputs
        if not all_recipients or not subject or content is None:
            raise ValueError("Recipient, subject, and content are required")

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
            # Add more detailed logging to see what's happening
            self.logger.info(f"Attempting to connect to SMTP server: {self._smtp_host}:{self._smtp_port}")

            # Send email
            with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=timeout) as server:
                self.logger.info("SMTP connection established")
                server.starttls(context=context)
                self.logger.info("TLS started successfully")
                server.login(self._email, self._app_password)
                self.logger.info("SMTP authentication successful")
                server.send_message(msg, to_addrs=all_recipients)
                self.logger.info("Email sent successfully")

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

    def resolve_email_template(self, template_id: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """
        Resolves an email template by replacing variables in the template.

        Args:
            template_id (str): The template file name without extension
            variables (dict): Dictionary of variables to inject into the template

        Returns:
            str: The resolved HTML content
        """
        if variables is None:
            variables = {}

        template_path = os.path.join(self.templates_dir, f"{template_id}.html")

        if not os.path.exists(template_path):
            raise ValueError(f"Template {template_id} not found")

        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        template = Template(template_content)
        return template.render(**variables)


# Example usage:
if __name__ == "__main__":
    # Example of how to integrate with your existing app utilities
    from db.db import get_db
    from dotenv import load_dotenv

    load_dotenv()
    db = get_db()
    email_service = EmailService(db, templates_dir="email_templates")

    # Test connection
    if email_service.test_connection():
        print("Email service is ready!")

        # Send single email
        subject = "מכרז מחברת י. ינקוביץ: הגש הצעה"
        template_id = 'request_offer'

        offer_email_html = email_service.resolve_email_template(template_id=template_id)

        try:

            success = email_service.send_email(
                bcc=["tamirzitman@gmail.com", "yuvalsayag2@gmail.com"],
                subject=subject,
                content=offer_email_html,
                content_type="html"
            )
            print(f"Email sent: {success}")
        except Exception as e:
            print(f"Failed to send email: {e}")
