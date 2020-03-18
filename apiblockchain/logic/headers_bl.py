from apiblockchain.models import Header
from django.db.models import Max

def get_last_header():
    try:
        header = Header.objects.order_by('-high').first()
        return header
    except Header.DoesNotExist:
        return None