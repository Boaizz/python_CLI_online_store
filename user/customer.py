class Customer:
    def __init__(self, cid: int, name: str, email: str, password: str, is_admin: bool = False):
        self.customer_id = cid
        self.name        = name
        self.email       = email
        self._password   = password
        self.isAdmin     = is_admin

    def __str__(self):
        return f"{self.name} ({self.email})"

    def check_password(self, pw: str) -> bool:
        return pw == self._password