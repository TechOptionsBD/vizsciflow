import flask
from xmltodict import parse
try:
    from urllib.parse import urljoin
    from urllib import urlopen
    from urllib import quote
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote
    from urllib.parse import urlencode

def validate(service_url,ticket):
    """
    Will attempt to validate the ticket. If validation fails, then False
    is returned. If validation is successful, then True, CAS User name and CAS Attributes are returned
    """

    cas_username = ""
    cas_attributes= ""

    cas_validate_url = create_cas_validate_url(
        "https://cas.usask.ca",
        "cas/serviceValidate",
        service_url,
        ticket)

    xml_from_dict = {}
    isValid = False

    try:
        xmldump = urlopen(cas_validate_url).read().strip().decode('utf8', 'ignore')
        xml_from_dict = parse(xmldump)
        isValid = True if "cas:authenticationSuccess" in xml_from_dict["cas:serviceResponse"] else False
    except ValueError:
        print("CAS returned unexpected result")

    if isValid:
        xml_from_dict = xml_from_dict["cas:serviceResponse"]["cas:authenticationSuccess"]
        username = xml_from_dict["cas:user"]
        cas_username = username

        if "cas:attributes" in xml_from_dict:
            attributes = xml_from_dict["cas:attributes"]

            if "cas:memberOf" in attributes:
                if not isinstance(attributes["cas:memberOf"], list):
                    attributes["cas:memberOf"] = attributes["cas:memberOf"].lstrip('[').rstrip(']').split(',')
                    for group_number in range(0, len(attributes['cas:memberOf'])):
                        attributes['cas:memberOf'][group_number] = attributes['cas:memberOf'][group_number].lstrip(' ').rstrip(' ')
                else:
                    for index in range(0, len(attributes['cas:memberOf'])):
                        attributes["cas:memberOf"][index] = attributes["cas:memberOf"][index].lstrip('[').rstrip(']').split(',')
                        for group_number in range(0, len(attributes['cas:memberOf'][index])):
                            attributes['cas:memberOf'][index][group_number] = attributes['cas:memberOf'][index][group_number].lstrip(' ').rstrip(' ')

            cas_attributes = attributes
    else:
        print("CAS Authentication Failure.")

    return isValid,cas_username,cas_attributes

def create_cas_validate_url(cas_url, cas_route, service, ticket,
                            renew=None):
    """ Create a CAS validate URL.
    Keyword arguments:
    cas_url -- The url to the CAS (ex. https://cas.usask.ca)
    cas_route -- The route where the CAS lives on server (ex. /cas/serviceValidate)
    service -- (ex.  https://p2irc-data-dev.usask.ca/welcome)
    ticket -- (ex. 'ST-58274-x839euFek492ou832Eena7ee-cas')
    renew -- "true" or "false"
    Example usage:
    >>> create_cas_validate_url(
    ...     'https://cas.usask.ca',
    ...     '/cas/serviceValidate',
    ...     'https://p2irc-data-dev.usask.ca/welcome',
    ...     'ST-58274-x839euFek492ou832Eena7ee-cas'
    ... )
    'https://cas.usask.ca/cas/serviceValidate?service=https%3A%2F%2Fp2irc-data-dev.usask.cat%3A5000%2Fwelcome&ticket=ST-58274-x839euFek492ou832Eena7ee-cas'
    """
    return create_url(
        cas_url,
        cas_route,
        ('service', service),
        ('ticket', ticket),
        ('renew', renew),
    )

def create_url(base, path=None, *query):
    """ Create a url.
    Creates a url by combining base, path, and the query's list of
    key/value pairs. Escaping is handled automatically. Any
    key/value pair with a value that is None is ignored.
    Keyword arguments:
    base -- The left most part of the url (ex. https://cas.usask.ca).
    path -- The path after the base (ex. /foo/bar).
    query -- A list of key value pairs (ex. [('key', 'value')]).
    Example usage:
    >>> create_url(
    ...     'https://cas.usask.ca',
    ...     'cas/serviceValidate',
    ...     ('key1', 'value'),
    ...     ('key2', None),     # Will not include None
    ...     ('url', 'https://p2irc-data-dev.usask.ca'),
    ... )
    'http:https://cas.usask.ca/cas/serviceValidate?key1=value&url=https%3A%2F%2Fp2irc-data-dev.usask.ca'
    """
    url = base
    # Add the path to the url if it's not None.
    if path is not None:
        url = urljoin(url, quote(path))
    # Remove key/value pairs with None values.
    query = filter(lambda pair: pair[1] is not None, query)
    # Add the query string to the url
    url = urljoin(url, '?{0}'.format(urlencode(list(query))))
    return url