from .models import Shop


def get_cities():
    """Return distinct city list for the city selector."""
    return (
        Shop.objects
        .filter(is_active=True, is_verified=True)
        .values_list('city', flat=True)
        .distinct()
        .order_by('city')
    )


def get_pincodes_for_city(city):
    return (
        Shop.objects
        .filter(is_active=True, is_verified=True, city__iexact=city)
        .values_list('pincode', flat=True)
        .distinct()
        .order_by('pincode')
    )
