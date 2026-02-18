#!/usr/bin/env python3
"""
Password Generator CLI Tool

Generate strong passwords and passphrases from the command line.

Usage:
    python generate_password.py                    # Generate 16-char strong password
    python generate_password.py --length 24       # Generate 24-char password
    python generate_password.py --passphrase      # Generate passphrase
    python generate_password.py --check "mypass"  # Check password strength
"""

import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.password_generator import password_generator


def main():
    parser = argparse.ArgumentParser(
        description="Generate secure passwords and passphrases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     Generate 16-char strong password
  %(prog)s -l 24               Generate 24-char password
  %(prog)s --passphrase         Generate memorable passphrase
  %(prog)s --check "mypass"     Check password strength
  %(prog)s --simple             Generate simple password (no special chars)
        """
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Password length (6-72, default: 16)"
    )

    parser.add_argument(
        "--passphrase",
        action="store_true",
        help="Generate passphrase instead of password"
    )

    parser.add_argument(
        "--words",
        type=int,
        default=4,
        help="Number of words in passphrase (default: 4)"
    )

    parser.add_argument(
        "--simple",
        action="store_true",
        help="Generate simple password (no special characters)"
    )

    parser.add_argument(
        "--check",
        metavar="PASSWORD",
        help="Check password strength"
    )

    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="Avoid ambiguous characters (0OIl1)"
    )

    args = parser.parse_args()

    # Check password strength
    if args.check:
        result = password_generator.check_strength(args.check)
        print(f"\n🔒 Password Strength Check")
        print(f"{'=' * 40}")
        print(f"Length:  {result['length']} characters")
        print(f"Strength: {result['strength']} ({result['score']}/{result['max_score']})")
        print(f"\nFeedback:")
        for feedback in result['feedback']:
            print(f"  • {feedback}")
        print()
        return

    # Generate passphrase
    if args.passphrase:
        passphrase = password_generator.generate_passphrase(
            word_count=args.words,
            separator="-"
        )
        strength = password_generator.check_strength(passphrase)

        print(f"\n🔐 Generated Passphrase")
        print(f"{'=' * 40}")
        print(f"{passphrase}")
        print(f"\nStrength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
        print(f"Length: {len(passphrase)} characters")
        print(f"\n⚠️  Store this passphrase securely!")
        print()
        return

    # Generate password
    if args.simple:
        password = password_generator.generate(
            length=args.length,
            use_special=False,
            avoid_ambiguous=args.no_ambiguous
        )
    else:
        password = password_generator.generate_strong(length=args.length)

    strength = password_generator.check_strength(password)

    print(f"\n🔑 Generated Password")
    print(f"{'=' * 40}")
    print(f"{password}")
    print(f"\nStrength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
    print(f"Length: {len(password)} characters")
    print(f"\n⚠️  Store this password securely!")
    print()

    # Copy to clipboard (if pyperclip is available)
    try:
        import pyperclip
        pyperclip.copy(password)
        print("✅ Password copied to clipboard!")
        print()
    except ImportError:
        pass


if __name__ == "__main__":
    main()
