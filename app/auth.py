import hashlib
import hmac
import base64
import json
import time
import os
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status, Depends
from app.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db_cursor, dict_from_row

def hash_password(password: str) -> str:
    """Generate a salted PBKDF2-HMAC-SHA256 password hash."""
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """Verify a stored hash against the provided password."""
    try:
        salt, key_hex = stored_password_hash.split('$', 1)
        test_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hmac.compare_digest(key_hex, test_key.hex())
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Create a tamper-proof cryptographically signed JWT-compatible token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    payload["exp"] = int(time.time()) + (expires_delta_minutes * 60)
    payload["iat"] = int(time.time())

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip('=')

    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')

    return f"{header_b64}.{payload_b64}.{sig_b64}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify the token signature and expiration."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        # Verify signature
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        
        # Add padding back if necessary
        sig_padding = '=' * (4 - len(sig_b64) % 4) if len(sig_b64) % 4 else ''
        actual_sig = base64.urlsafe_b64decode(sig_b64 + sig_padding)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        # Decode payload
        payload_padding = '=' * (4 - len(payload_b64) % 4) if len(payload_b64) % 4 else ''
        payload_json = base64.urlsafe_b64decode(payload_b64 + payload_padding).decode('utf-8')
        payload = json.loads(payload_json)

        # Check expiration
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        return None

def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Extract and authenticate current user if header is provided."""
    if not authorization:
        return None
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        token = authorization  # fallback if raw token passed

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None

    user_id = payload["sub"]
    with get_db_cursor() as cur:
        cur.execute("SELECT id, name, email, mobile, role, department, village, preferred_language FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return dict_from_row(row)

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Dependency that requires a valid authenticated user."""
    user = get_current_user_optional(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def require_citizen(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require user to be a registered Citizen."""
    if current_user.get("role") != "citizen":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to citizen accounts"
        )
    return current_user

def require_authority(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require user to be an Authority or Administrator."""
    if current_user.get("role") not in ("authority", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Authority credentials required"
        )
    return current_user
