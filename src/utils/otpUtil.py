import pyotp
## To verify the OTP given by the user generated by the Authenticator
@staticmethod
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)