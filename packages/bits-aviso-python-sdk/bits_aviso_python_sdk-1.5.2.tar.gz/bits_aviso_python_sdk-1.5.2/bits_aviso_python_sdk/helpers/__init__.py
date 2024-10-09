import datetime
import dns.resolver
import json
import logging
import re
import xmltodict
from urllib.parse import urlparse


def convert_xml_to_dict(xml_string, json_output=False):
    """Converts an XML string to a dictionary.

    Args:
        xml_string (str): The XML string to convert.
        json_output (bool, optional): Whether to output the dictionary as a JSON. Defaults to False.

    Returns:
        dict: The XML string converted to a dictionary.
    """
    if json_output:
        return json.dumps(xmltodict.parse(xml_string))

    else:
        return xmltodict.parse(xml_string)


def initialize_logger(file_handler_path=None):
    """Initializes a logger with a stream handler and an optional file handler.

    Args:
        file_handler_path (str, optional): The path to save the log file if a file handler is desired. Defaults to None.
    """
    # set up logger
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    logger = logging.getLogger()  # root logger

    # check if there's any handlers already
    if not logger.handlers:
        # create file handler if path is provided
        if file_handler_path:
            # check if the path ends with a slash
            if file_handler_path.endswith('/'):
                file_handler = logging.FileHandler(f"{file_handler_path}{today}.log")

            else:
                file_handler = logging.FileHandler(f"{file_handler_path}/{today}.log")
            # set level to DEBUG
            file_handler.setLevel(logging.DEBUG)
            # set format
            file_handler.setFormatter(logging.Formatter(
                "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
            # add file handler to the logger
            logger.addHandler(file_handler)

        # Create stream handler and set level to ERROR
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(
            "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
        # add stream handler to the logger
        logger.addHandler(stream_handler)

    # Set the logger's level to the lowest level among all handlers
    logger.setLevel(logging.DEBUG)

    return logger


def is_ip_address(string_to_check):
    """Check if the given string is a valid IP address.

    Args:
        string_to_check (str): The string to check.

    Returns:
        bool: True if the string is a valid IP address, False otherwise.
    """
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if ip_pattern.match(string_to_check):
        parts = string_to_check.split('.')
        return all(0 <= int(part) <= 255 for part in parts)

    return False


def resolve_dns(domain, dns_server=None, first_result_only=True):
    """Resolves the domain to an IP address. If a DNS server is provided, it will use that server.

    Args:
        domain (str): The domain to resolve.
        dns_server (str, optional): The DNS server to use. Defaults to None.
        first_result_only (bool, optional): Whether to return only the first result. Defaults to True.

    Returns:
        str or list: The resolved IP address(es).
    """
    # Check if the domain is a URL and extract the hostname
    if domain.startswith("http"):
        domain = urlparse(domain).hostname

    # Initialize the resolver
    resolver = dns.resolver.Resolver()

    # Set the DNS server if provided
    if dns_server:
        resolver.nameservers = [dns_server]

    try:
        answer = resolver.resolve(domain)
        # return the first result only if specified
        if first_result_only:
            return answer[0].to_text()

        # otherwise return all results
        return [rdata.to_text() for rdata in answer]

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout) as e:
        return f"Error resolving DNS: {e}"
