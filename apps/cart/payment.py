"""
Razorpay payment stub for BAZAR.
This module provides payment integration hooks.
Configure RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env for production.
"""

import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_order(request):
    """Create Razorpay order and return order ID."""
    amount = int(request.POST.get('amount', 0))  # Amount in paise
    if amount <= 0:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    order_data = {
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1,
    }

    try:
        order = client.order.create(data=order_data)
        return JsonResponse({
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key_id': settings.RAZORPAY_KEY_ID,
        })
    except Exception:
        return JsonResponse({'error': 'Payment service unavailable'}, status=503)


@csrf_exempt
@require_POST
def payment_callback(request):
    """Verify Razorpay payment signature."""
    try:
        data = json.loads(request.body)
        params = {
            'razorpay_order_id': data.get('razorpay_order_id', ''),
            'razorpay_payment_id': data.get('razorpay_payment_id', ''),
            'razorpay_signature': data.get('razorpay_signature', ''),
        }
        client.utility.verify_payment_signature(params)
        return JsonResponse({'status': 'success'})
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'status': 'failure', 'error': 'Invalid signature'}, status=400)
    except Exception:
        return JsonResponse({'status': 'failure', 'error': 'Verification failed'}, status=400)
