from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCartItem(request):
    # Fetch only the cart items of the logged-in user
    cart_items = models.CartItem.objects.filter(cart__user=request.user)
    cartSer = serializers.CartItemSerializer(cart_items, many=True)
    return Response(cartSer.data, status=status.HTTP_200_OK)


# Add to user cart 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get("product_id")

    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create the user's cart
    cart, _ = models.Cart.objects.get_or_create(user=user)

    # Check if the product is already in cart
    cart_item, created = models.CartItem.objects.get_or_create(
        cart=cart, product_id=product_id,
        defaults={"quantity": 1}
    )

    if not created:
        # Increment quantity if already in cart
        cart_item.quantity += 1
        cart_item.save()

    serializer = serializers.CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Delete cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, item_id):
    try:
        # Only allow the logged-in user to delete their own cart items
        cart_item = models.CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
    except models.CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    try:
        cart_item = models.CartItem.objects.get(id=item_id, cart__user=request.user)
    except models.CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    new_quantity = request.data.get('quantity')
    if new_quantity and int(new_quantity) > 0:
        cart_item.quantity = int(new_quantity)
        cart_item.save()
        return Response({"message": "Quantity updated", "quantity": cart_item.quantity})
    return Response({"error": "Invalid quantity"}, status=400)