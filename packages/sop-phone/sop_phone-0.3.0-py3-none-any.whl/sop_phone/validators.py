import re
import phonenumbers

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


__all__ = (
    'PhoneValidator',
    'number_quicksearch',
    'PhoneMaintainerValidator',
)


class PhoneMaintainerValidator:

    @staticmethod
    def check_address(address, name:str) -> None:
        if not address:
            return
        if address.strip() == '':
            return
        if not re.match("^([^\n]* \r?\n)+[^\n]+$", address):
            raise ValidationError({
                f'{name}': _("Address must be multiline and each line must end with a space.")
            })


class PhoneValidator:

    @staticmethod
    def check_site(site) -> None:
        if site is None:
            raise ValidationError({
                'site': _("Site must be set.")
            })

    @staticmethod
    def check_delivery(delivery, site) -> None:
        if delivery and site and delivery.site != site:
            raise ValidationError({
                'delivery': _("Delivery must be set to the same site as the DID.")
            })

    @staticmethod
    def check_number(where:str, number:int) -> None:
        if number is None or number <= 0 :
            raise ValidationError({
                f'{where}': _("Number must be set in E164 format.")
            })
        if not phonenumbers.parse(f'+{number}'):
            raise ValidationError({
                f'{where}': _("Number must be a valid phone number written in E164 format.")
            })

    @staticmethod
    def check_start_end(start:int, end:int) -> None:
        if start is None or end is None:
            return
        if len(str(start))!=len(str(end)):
            raise ValidationError({
                'end': _("End number must be the same length as start number.")
            })
        if start > end:
            raise ValidationError({
                'end': _("End number must be greater than or equal to the start number.")
            })


def number_quicksearch(start: int, end: int, pattern: str) -> bool:
    '''
    Recherche rapide d'un nombre dans une plage donnée
    '''
    pattern_len = len(pattern)
    pattern_int = int(pattern)
    divisor = 10 ** pattern_len

    if start % divisor == pattern_int or end % divisor == pattern_int:
        return True

    current = start
    while current <= end:
        temp = current
        while temp > 0:
            if temp % divisor == pattern_int:
                return True
            temp //= 10
        current += 1

    return False

