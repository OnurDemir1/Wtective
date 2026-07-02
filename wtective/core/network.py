import dns.resolver
import socket
import ssl
from urllib.parse import urlparse


class NetworkAnalyzer:
    def __init__(self, target_url: str):
        self.domain = urlparse(target_url).netloc.split(':')[0]

    def check_dns(self) -> dict:
        records = {}
        try:
            answers = dns.resolver.resolve(self.domain, 'CNAME')
            records['CNAME'] = [str(r.target) for r in answers]
        except Exception:
            pass
        try:
            answers = dns.resolver.resolve(self.domain, 'TXT')
            records['TXT'] = [r.to_text() for r in answers]
        except Exception:
            pass
        return records

    def check_ssl(self) -> dict:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer', ()))
                    return {'issuer': issuer.get('organizationName', issuer.get('commonName', ''))}
        except Exception:
            return {}

