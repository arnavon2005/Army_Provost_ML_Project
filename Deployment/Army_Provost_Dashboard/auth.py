
import bcrypt

from database import (
    get_supabase_client
)


# ============================================================
# PASSWORD HELPERS
# ============================================================

def hash_password(password):
    """
    Hash a plaintext password using bcrypt.
    """

    password_bytes = (
        str(password)
        .encode("utf-8")
    )

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode(
        "utf-8"
    )


def verify_password(
    password,
    password_hash
):
    """
    Verify a plaintext password against its bcrypt hash.
    """

    return bcrypt.checkpw(
        str(password).encode("utf-8"),
        str(password_hash).encode("utf-8")
    )


# ============================================================
# REGISTER OPERATOR
# ============================================================

def register_operator(
    *,
    operator_uid,
    password,
    display_name=None
):
    """
    Register a prototype operator in Supabase.

    Returns:
        (True, message)
        or
        (False, error_message)
    """

    operator_uid = str(
        operator_uid
    ).strip()

    password = str(
        password
    )

    display_name = (
        str(display_name).strip()
        if display_name
        else None
    )


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if len(operator_uid) < 3:

        return (
            False,
            "Operator UID must contain at least 3 characters."
        )


    if len(password) < 8:

        return (
            False,
            "Password must contain at least 8 characters."
        )


    client = get_supabase_client()


    # --------------------------------------------------------
    # Check duplicate UID
    # --------------------------------------------------------

    existing = (
        client
        .table("operators")
        .select("operator_uid")
        .eq(
            "operator_uid",
            operator_uid
        )
        .limit(1)
        .execute()
    )


    if existing.data:

        return (
            False,
            "Operator UID already exists."
        )


    # --------------------------------------------------------
    # Store hashed password
    # --------------------------------------------------------

    password_hash = hash_password(
        password
    )


    (
        client
        .table("operators")
        .insert(
            {
                "operator_uid":
                    operator_uid,

                "password_hash":
                    password_hash,

                "display_name":
                    display_name,

                "is_active":
                    True
            }
        )
        .execute()
    )


    return (
        True,
        "Prototype operator registered successfully."
    )


# ============================================================
# AUTHENTICATE OPERATOR
# ============================================================

def authenticate_operator(
    operator_uid,
    password
):
    """
    Authenticate an operator against Supabase.

    Returns:
        (True, operator_record)
        or
        (False, error_message)
    """

    operator_uid = str(
        operator_uid
    ).strip()

    password = str(
        password
    )


    if not operator_uid or not password:

        return (
            False,
            "Operator UID and password are required."
        )


    client = get_supabase_client()


    response = (
        client
        .table("operators")
        .select(
            "operator_uid, "
            "password_hash, "
            "display_name, "
            "is_active"
        )
        .eq(
            "operator_uid",
            operator_uid
        )
        .limit(1)
        .execute()
    )


    if not response.data:

        return (
            False,
            "Invalid Operator UID or password."
        )


    record = response.data[0]


    if not record.get(
        "is_active",
        True
    ):

        return (
            False,
            "Operator account is inactive."
        )


    password_valid = verify_password(
        password,
        record[
            "password_hash"
        ]
    )


    if not password_valid:

        return (
            False,
            "Invalid Operator UID or password."
        )


    return (
        True,
        {
            "operator_uid":
                record[
                    "operator_uid"
                ],

            "display_name":
                record.get(
                    "display_name"
                )
        }
    )
