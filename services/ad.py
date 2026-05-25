import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def _run(cmd: list) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0
        return success, output
    except Exception as e:
        return False, str(e)

def user_exists(email: str) -> bool:
    try:
        username = email.split("@")[0]
        ok, out = _run(["samba-tool", "user", "show", username])
        return ok
    except Exception as e:
        print(f"[AD] user_exists error: {e}")
        return False

def verify_user(email: str, password: str) -> bool:
    try:
        username = email.split("@")[0]
        ok, out = _run(["samba-tool", "user", "show", username])
        return ok
    except Exception as e:
        print(f"[AD] verify_user error: {e}")
        return False

def create_user(name: str, email: str, phone: str, password: str) -> bool:
    try:
        username = email.split("@")[0]
        first_name = name.split()[0]
        last_name = name.split()[-1] if len(name.split()) > 1 else "User"

        ok, out = _run([
            "samba-tool", "user", "create", username, password,
            f"--given-name={first_name}",
            f"--surname={last_name}",
            f"--mail-address={email}",
        ])

        if not ok:
            print(f"[AD] create_user failed: {out}")
            return False

        print(f"[AD] create_user success: {out}")
        return True

    except Exception as e:
        print(f"[AD] create_user error: {e}")
        return False
