import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.sessions.backends.db import SessionStore

from . import models

@api_view(['POST'])
def seller_signup(request):
    data = request.data  # ✅ use DRF standard
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    company = data.get("company", "").strip()
    owner = data.get("owner", "").strip()
    address = data.get("address", "").strip()
    pincode = data.get("pincode", "").strip()
    business_type = data.get("businessType", "").strip()
    category = data.get("category", "").strip()
    gstin = data.get("gstin", "").strip()
    bank_account = data.get("bank", "").strip()
    ifsc = data.get("ifsc", "").strip()

    # --- Validations ---
    if models.Seller.objects.filter(seller_phone=phone).exists():
        return Response({"phone": "Phone already registered."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError:
        return Response({"email": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    if models.Seller.objects.filter(seller_email=email).exists():
        return Response({"email": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)


    if not password:  # only check when on password step
        return Response({"password": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_password(password)  # ✅ Django built-in password strength rules
    except ValidationError as e:
        return Response({"password": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)


    if gstin and not re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}", gstin):
        return Response({"gstin": "Invalid GSTIN format."}, status=status.HTTP_400_BAD_REQUEST)

    if not re.fullmatch(r"\d{9,18}", bank_account):
        return Response({"bank": "Invalid bank account number."}, status=status.HTTP_400_BAD_REQUEST)

    if not re.fullmatch(r"[A-Z]{4}0\d{6}", ifsc):
        return Response({"ifsc": "Invalid IFSC code."}, status=status.HTTP_400_BAD_REQUEST)

    # --- Save Seller ---
    seller = models.Seller(
        seller_phone=phone,
        seller_email=email,
        business_name=company,
        owner_name=owner,
        seller_address=address,
        seller_pincode=pincode,
        business_type=business_type,
        selling_category=category,
        gstin=gstin,
        bank_account_number=bank_account,
        ifsc_code=ifsc,
    )
    seller.set_password(password) 
    seller.save()

    return Response({"message": "Seller registered successfully", "seller_id": seller.id}, status=status.HTTP_201_CREATED)



# Seller Login

@api_view(["POST"])
def seller_login(request):
    email = request.data.get("seller_email")
    password = request.data.get("seller_password")
    
    try:
        seller = models.Seller.objects.get(seller_email=email)  # fetch seller row
    except models.Seller.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # call check_password on that row
    if seller.check_password(password):
        request.session['seller_id'] = seller.id
        return Response(
            {
                "message": "Login successfully",
                "id": seller.id,
                "email": seller.seller_email,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)



# Seller Logout

@api_view(["POST"])
def seller_logout(request):
    try:
        del request.session['seller_id']  # remove seller_id from session
    except KeyError:
        pass
    return Response({"message": "Logged out successfully"})