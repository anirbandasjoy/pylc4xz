import secrets
import string
from typing import Optional


class PasswordGenerator:
    """Utility class for generating secure random passwords"""

    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.all_chars = self.lowercase + self.uppercase + self.digits + self.special

    def generate(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        avoid_ambiguous: bool = False
    ) -> str:
        """
        Generate a secure random password

        Args:
            length: Password length (default 16, max 72)
            use_uppercase: Include uppercase letters
            use_digits: Include numbers
            use_special: Include special characters
            avoid_ambiguous: Avoid ambiguous chars (0OIl1)

        Returns:
            Generated password string
        """
        # Limit length to 72 for bcrypt compatibility
        length = min(length, 72)
        length = max(length, 6)

        # Build character set
        chars = self.lowercase

        if use_uppercase:
            chars += self.uppercase

        if use_digits:
            chars += self.digits

        if use_special:
            chars += self.special

        if avoid_ambiguous:
            # Remove ambiguous characters
            ambiguous = "0O1lIl"
            chars = ''.join(c for c in chars if c not in ambiguous)

        # Generate password using cryptographically secure random generator
        password = ''.join(secrets.choice(chars) for _ in range(length))

        return password

    def generate_strong(self, length: int = 16) -> str:
        """
        Generate a strong password with all character types

        Args:
            length: Password length (default 16, max 72)

        Returns:
            Strong password with uppercase, lowercase, digits, and special chars
        """
        length = min(length, 72)
        length = max(length, 8)

        # Ensure at least one of each type
        password = [
            secrets.choice(self.lowercase),
            secrets.choice(self.uppercase),
            secrets.choice(self.digits),
            secrets.choice(self.special)
        ]

        # Fill the rest with random characters from all sets
        remaining_length = length - 4
        password.extend(secrets.choice(self.all_chars) for _ in range(remaining_length))

        # Shuffle the password
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)

    def generate_passphrase(self, word_count: int = 4, separator: str = "-") -> str:
        """
        Generate a memorable passphrase using random words

        Args:
            word_count: Number of words (default 4)
            separator: Separator between words (default "-")

        Returns:
            Memorable passphrase
        """
        # Common words for passphrase
        words = [
            "correct", "horse", "battery", "staple", "cloud", "server", "code",
            "python", "fast", "api", "secure", "login", "user", "admin", "token",
            "peace", "ocean", "river", "mountain", "forest", "sky", "star", "moon",
            "fire", "water", "earth", "wind", "stone", "metal", "glass", "wood",
            "night", "day", "sun", "shadow", "light", "dark", "bright", "cold",
            "warm", "cool", "hot", "fresh", "clean", "pure", "clear", "sharp",
            "quick", "slow", "steady", "calm", "brave", "smart", "wise", "kind"
        ]

        word_count = min(word_count, 8)  # Max 8 words to keep it reasonable

        passphrase = separator.join(secrets.choice(words) for _ in range(word_count))

        # Add a number and special char for extra security
        passphrase += str(secrets.choice(range(10, 99)))
        passphrase += secrets.choice(self.special)

        return passphrase

    def check_strength(self, password: str) -> dict:
        """
        Check password strength

        Args:
            password: Password to check

        Returns:
            Dictionary with strength info
        """
        score = 0
        feedback = []

        # Check length
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters")

        if len(password) >= 12:
            score += 1
        else:
            feedback.append("Longer passwords are more secure")

        if len(password) >= 16:
            score += 1

        # Check for lowercase
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")

        # Check for uppercase
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")

        # Check for digits
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")

        # Check for special characters
        if any(c in self.special for c in password):
            score += 1
        else:
            feedback.append("Add special characters (!@#$%^&*)")

        # Determine strength
        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Medium"
        elif score <= 5:
            strength = "Strong"
        else:
            strength = "Very Strong"

        return {
            "strength": strength,
            "score": score,
            "max_score": 7,
            "length": len(password),
            "feedback": feedback if feedback else ["Password looks good!"]
        }


# Singleton instance
password_generator = PasswordGenerator()
