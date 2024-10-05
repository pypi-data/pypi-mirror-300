import phonenumbers


__all__ = (
    'format_number',
    'count_all_did',
    'get_object_or_create',
)


def format_number(number:int) -> str:
    '''
    formats E164 numbers
    and displays a beautiful flag
    depending on their country code
    '''
    def country_code_to_flag(county) -> str:
        '''
        returns the right flag depending on the country code
        '''
        return chr(ord(country[0]) + 127397) + chr(ord(country[1]) + 127397)

    prepare_number:str = f'+{str(number)}'
    parsed_number = phonenumbers.parse(prepare_number)
    country:str = phonenumbers.region_code_for_country_code(parsed_number.country_code)
    flag = country_code_to_flag(country)
    '''
    returns {flag} <spaces> {number}
    '''
    return f'{flag}\u00A0\u00A0\u00A0\u00A0{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}'


def get_object_or_create(model, site) -> object | None:
    '''
    get the model instance or create it
    (for dcim/site extra models)
    '''
    target = model.objects.filter(site=site)

    if target.exists():

        if target.filter(maintainer__isnull=False).exists():
            return target.filter(maintainer__isnull=False).first()

        return target.first()
    
    target = model(site=site)
    target.save()

    return target


class count_all_did:
    """counts all numbers inside a given PhoneDID instance
    
    Args:
        PhoneDID (instance)
    Returns:
```python
    __int__(self):
        return self.phone_coun)
```
    """
    def __init__(self, phone_did) -> None:
        self.phone_did = phone_did
        self.phone_count = self.count()

    def count_range(self, start: int, end: int) -> int:
        '''
        simply counts the number of phone numbers in a range
        '''
                
        if start > end:
            return 0
        if start == end:
            return 1

        if start < end:
            return (end - start) + 1
        return 0

    def count(self) -> int:
        phone_count: int = 0

        try:
            for did in self.phone_did:
                phone_count += self.count_range(did.start, did.end)
        except:
            try:
                phone_count += self.count_range(self.phone_did.start, self.phone_did.end)
            except:pass
        return phone_count

    def __int__(self) -> int:
        '''
        ```python
        return self.phone_count
        ```
        '''
        return self.phone_count
