import os
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from ldap3.core.exceptions import LDAPException
from dotenv import load_dotenv

load_dotenv()

AD_SERVER   = os.getenv("AD_SERVER", "localhost")
AD_DOMAIN   = os.getenv("AD_DOMAIN", "RIKKIEE.LOCAL")
AD_USER     = os.getenv("AD_ADMIN_USER", "Administrator")
AD_PASSWORD = os.getenv("AD_ADMIN_PASSWORD", "")
AD_BASE_DN  = os.getenv("AD_BASE_DN", "DC=RIKKIEE,DC=LOCAL")

def get_connection():
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=f"{AD_DOMAIN}\\{AD_USER}",
        password=AD_PASSWORD,
        authentication=NTLM,
        auto_bind=True
    )
    return conn

def user_exists(email: str) -> bool:
    """Check if a user already exists in AD by email."""
    try:
        conn = get_connection()
        conn.search(
            AD_BASE_DN,
            f"(mail={email})",
            search_scope=SUBTREE,
            attributes=["mail"]
        )
        return len(conn.entries) > 0
    except LDAPException as e:
        print(f"[AD] user_exists error: {e}")
        return False

def verify_user(email: str, password: str) -> bool:
    """Verify a user's credentials against AD."""
    try:
        # Extract username from email
        username = email.split("@")[0]
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(
            server,
            user=f"{AD_DOMAIN}\\{username}",
            password=password,
            authentication=NTLM,
            auto_bind=True
        )
        return conn.bound
    except LDAPException:
        return False

def create_user(name: str, email: str, phone: str, password: str) -> bool:
    """Create a new user in AD."""
    try:
        conn = get_connection()
        username = email.split("@")[0]
        dn = f"CN={name},CN=Users,{AD_BASE_DN}"

        conn.add(dn, ["top", "person", "organizationalPerson", "user"], {
            "cn":                name,
            "sAMAccountName":    username,
            "userPrincipalName": email,
            "mail":              email,
            "telephoneNumber":   phone,
            "displayName":       name,
            "userAccountControl": 512,   # Normal enabled account
        })

        if not conn.result["result"] == 0:
            print(f"[AD] create_user failed: {conn.result}")
            return False

        # Set password
        conn.extend.microsoft.modify_password(dn, password)
        return True

    except LDAPException as e:
        print(f"[AD] create_user error: {e}")
        return False

def get_user_phone(email: str) -> str | None:
    """Get phone number from AD for signin OTP flow."""
    try:
        conn = get_connection()
        conn.search(
            AD_BASE_DN,
            f"(mail={email})",
            search_scope=SUBTREE,
            attributes=["telephoneNumber"]
        )
        if conn.entries:
            return str(conn.entries[0].telephoneNumber)
        return None
    except LDAPException as e:
        print(f"[AD] get_user_phone error: {e}")
        return None
