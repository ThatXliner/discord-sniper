"""Exercise Requests and the actual Discord HTTP client without app auth.

Only official incident hosts and example.com are contacted. No app configuration,
message handlers, login, gift checks, or Privnote services are executed.
"""
import asyncio
import json
from pathlib import Path
import ssl
import sys
import tempfile

import aiohttp
import discord.http
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sniper.tls import create_connector
from check_ca_bundle import main as check_bundle

HOSTS = ('dv-g3b-emudhra.we-have-a-problem.com',
         'dv-g3b-aaa-emudhra.we-have-a-problem.com', 'example.com')


def requests_probe():
    results = []
    with requests.Session() as session:
        session.trust_env = False
        for host in HOSTS:
            try:
                response = session.get('https://' + host + '/', timeout=8)
                response.raise_for_status()
                verdict = 'https_success' if host == 'example.com' else 'FAIL_accepted'
            except requests.exceptions.SSLError as error:
                verdict = ('certificate_rejected' if 'CERTIFICATE_VERIFY_FAILED' in str(error)
                           else 'inconclusive_tls_error')
            except requests.exceptions.RequestException as error:
                verdict = 'inconclusive_' + type(error).__name__
            results.append(dict(client='requests', host=host, result=verdict))
    return results


async def discord_probe():
    connector = create_connector()
    assert connector._ssl.verify_mode == ssl.CERT_REQUIRED
    assert connector._ssl.check_hostname
    # Verify the exact connector trust store against the archived official chains.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem') as bundle:
        for der in connector._ssl.get_ca_certs(binary_form=True):
            bundle.write(ssl.DER_cert_to_PEM_cert(der))
        bundle.flush()
        saved = sys.argv
        try:
            sys.argv = [saved[0], bundle.name]
            check_bundle()
        finally:
            sys.argv = saved
    client = discord.http.HTTPClient(connector=connector)
    assert client.token is None
    # Populate the library's session without static_login (which contacts Discord).
    client._HTTPClient__session = aiohttp.ClientSession(
        connector=connector, trust_env=False, timeout=aiohttp.ClientTimeout(total=8))
    results = []
    try:
        for host in HOSTS:
            route = discord.http.Route('GET', '/')
            route.url = 'https://' + host + '/'
            try:
                await client.request(route)
                verdict = 'https_success' if host == 'example.com' else 'FAIL_accepted'
            except aiohttp.ClientConnectorCertificateError:
                verdict = 'certificate_rejected'
            except (aiohttp.ClientError, asyncio.TimeoutError) as error:
                verdict = 'inconclusive_' + type(error).__name__
            results.append(dict(client='discord.http.HTTPClient', host=host, result=verdict))
    finally:
        await client.close()
    return results


if __name__ == '__main__':
    results = requests_probe() + asyncio.run(discord_probe())
    print(json.dumps(results, indent=2))
    sys.exit(0 if all(r['result'] == ('https_success' if r['host'] == 'example.com'
                                    else 'certificate_rejected') for r in results) else 1)
