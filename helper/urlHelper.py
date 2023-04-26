
import validators

def is_valid_domain(url):
    if validators.domain(url):
        return True
    return False