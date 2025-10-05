import re

from django.contrib.auth.decorators import login_required

from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

# Helper to safely convert string/boolean
def str_to_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return default

# Helper to safely convert to float
def str_to_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

# Helper to safely convert date
def str_to_date(value, fmt="%Y-%m-%d"):
    try:
        return datetime.strptime(value, fmt).date()
    except (TypeError, ValueError):
        return None

@api_view(['POST'])
def mobileProduct(request):
    data = request.data

    # --- General Info ---
    productName = data.get("productName", "").strip()
    brandName = data.get("brandName", "").strip()
    modelNumber = data.get("modelNumber", "").strip()
    launchDate = str_to_date(data.get("launchDate"))
    productDescription = data.get("productDescription", "").strip()

    # --- Dimension ---
    height = data.get("height", "").strip()
    width = data.get("width", "").strip()
    thickness = data.get("thickness", "").strip()
    weight = data.get("weight", "").strip()
    build = data.get("build", "").strip()
    simType = data.get("simType", "").strip()

    # --- Display ---
    displayType = data.get("displayType", "").strip()
    displaySize = data.get("displaySize", "").strip()
    displayResolution1 = data.get("displayResolution1", "").strip()
    displayResolution2 = data.get("displayResolution2", "").strip()
    protection = data.get("protection", "").strip()
    refreshRate = data.get("refreshRate", "").strip()

    # --- Platform ---
    os = data.get("os", "").strip()
    chipset = data.get("chipset", "").strip()
    cpu = data.get("cpu", "").strip()
    gpu = data.get("gpu", "").strip()

    # --- Memory ---
    cardSlot = data.get("cardSlot", "").strip()
    internalStorageRam = data.get("internalStorageRam", "").strip()
    internalStorageRom = data.get("internalStorageRom", "").strip()

    # --- Camera ---
    mainLens = data.get("mainLens", "").strip()
    wideAngleLens = data.get("wideAngleLens", "").strip()
    macroLens = data.get("macroLens", "").strip()
    telePhotoLens = data.get("telePhotoLens", "").strip()
    opticalZoom = data.get("opticalZoom", "").strip()
    mainCameraVideo = data.get("mainCameraVideo", "").strip()
    selfieCamera = data.get("selfieCamera", "").strip()
    selfieWideCamera = data.get("selfieWideCamera", "").strip()
    selfieCameraVideo = data.get("selfieCameraVideo", "").strip()

    # --- Sound ---
    loudspeaker = str_to_bool(data.get("loudspeaker"), True)
    stereoSpeakers = str_to_bool(data.get("stereoSpeakers"), True)
    audioJack = str_to_bool(data.get("audioJack"), False)

    # --- Comms ---
    wlan = data.get("wlan", "").strip()
    bluetooth = data.get("bluetooth", "").strip()
    usb = data.get("usb", "").strip()
    gps = str_to_bool(data.get("gps"), True)
    nfc = str_to_bool(data.get("nfc"), False)
    infrared = str_to_bool(data.get("infrared"), False)
    radio = str_to_bool(data.get("radio"), False)

    # --- Security ---
    fingerPrint = data.get("fingerPrint", "").strip()
    faceUnlock = str_to_bool(data.get("faceUnlock"), True)

    # --- Battery ---
    batteryType = data.get("batteryType", "").strip()
    batteryCapacity = data.get("batteryCapacity", "").strip()
    chargingSpeed = data.get("chargingSpeed", "").strip()
    wirelessCharging = str_to_bool(data.get("wirelessCharging"), False)
    wirelessChargingSpeed = data.get("wirelessChargingSpeed", "").strip()

    # --- Other Specifications ---
    colors = data.get("colors", "").strip()
    modelsAvailable = data.get("modelsAvailable", "").strip()
    sar = data.get("sar", "").strip()

    # --- Seller ---
    productSellerName = data.get("productSellerName", "").strip()
    productCompanyName = data.get("productCompanyName", "").strip()
    sellerPhone = data.get("sellerPhone", "").strip()
    sellerEmail = data.get("sellerEmail", "").strip()

    # --- Images ---
    productImage1 = request.FILES.get("productImage1", None)
    productImage2 = request.FILES.get("productImage2", None)
    productImage3 = request.FILES.get("productImage3", None)

    # --- Shipping ---
    productAddress = data.get("productAddress", "").strip()
    productState = data.get("productState", "").strip()
    productCountry = data.get("productCountry", "").strip()
    productPincode = data.get("productPincode", "").strip()

    # --- Pricing ---
    productPrice = str_to_float(data.get("productPrice", 0))
    discountPrice = str_to_float(data.get("discountPrice", 0))

    # --- Create and Save ---
    mobileProduct = models.MobileProduct(
        productName=productName,
        brandName=brandName,
        modelNumber=modelNumber,
        launchDate=launchDate,
        productDescription=productDescription,
        height=height,
        width=width,
        thickness=thickness,
        weight=weight,
        build=build,
        simType=simType,
        displayType=displayType,
        displaySize=displaySize,
        displayResolution1=displayResolution1,
        displayResolution2=displayResolution2,
        protection=protection,
        refreshRate=refreshRate,
        os=os,
        chipset=chipset,
        cpu=cpu,
        gpu=gpu,
        cardSlot=cardSlot,
        internalStorageRam=internalStorageRam,
        internalStorageRom=internalStorageRom,
        mainLens=mainLens,
        wideAngleLens=wideAngleLens,
        macroLens=macroLens,
        telePhotoLens=telePhotoLens,
        opticalZoom=opticalZoom,
        mainCameraVideo=mainCameraVideo,
        selfieCamera=selfieCamera,
        selfieWideCamera=selfieWideCamera,
        selfieCameraVideo=selfieCameraVideo,
        loudspeaker=loudspeaker,
        stereoSpeakers=stereoSpeakers,
        audioJack=audioJack,
        wlan=wlan,
        bluetooth=bluetooth,
        usb=usb,
        gps=gps,
        nfc=nfc,
        infrared=infrared,
        radio=radio,
        fingerPrint=fingerPrint,
        faceUnlock=faceUnlock,
        batteryType=batteryType,
        batteryCapacity=batteryCapacity,
        chargingSpeed=chargingSpeed,
        wirelessCharging=wirelessCharging,
        wirelessChargingSpeed=wirelessChargingSpeed,
        colors=colors,
        modelsAvailable=modelsAvailable,
        sar=sar,
        productSellerName=productSellerName,
        productCompanyName=productCompanyName,
        sellerPhone=sellerPhone,
        sellerEmail=sellerEmail,
        productImage1=productImage1,
        productImage2=productImage2,
        productImage3=productImage3,
        productAddress=productAddress,
        productState=productState,
        productCountry=productCountry,
        productPincode=productPincode,
        productPrice=productPrice,
        discountPrice=discountPrice,
    )
    mobileProduct.save()

    return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)



# get the product
@api_view(['GET'])
def getProduct(request):
    productData=models.MobileProduct.objects.all()
    serProduct=serializers.serProduct(productData,many=True)
    return Response({"mobileProduct":serProduct.data},status=status.HTTP_200_OK)

# get product by ID
@api_view(['GET'])
def getProductByID(request,id):
    productData=models.MobileProduct.objects.get(id=id)
    serProduct=serializers.serProduct(instance=productData)
    return Response({"mobileProduct":serProduct.data},status=status.HTTP_200_OK)
