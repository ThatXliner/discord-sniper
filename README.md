<h1 align="center">💫 Discord Multi Sniper V2 💫</h1>
<h3 align="center">Nitro, Giveaway, Privnote Sniper. Usually snipes in 10 - 50ms</h3>
<h4 align="center">⭐ Don't forget to leave a star! ⭐</h4>
<h4 align="center" style="color: red;">Some code changes before v3, sniper should be faster</h4>

## Features:
- Added giveaway botlist, fixed webhooks
- Nitro, Giveaway, Privnote sniper
- Giveaway join delay
- Windows notification
- Webhook notifications (Thanks to [@rondDev](https://github.com/rondDev))
- Support on alt account

## News in v2:
- Added giveaway join delay
- Added Support to more giveaway bots
- Fixed Privnote Sniper
- More info about Sniped Nitro
- Added Webhook notifications (Thanks to [@rondDev](https://github.com/rondDev))
- More customisability
- Added **use on alt**, that means you can run sniper on alt account and if he snipes nitro, code will be reedemed on other account
- Removed some useless code
- If you have enable nitro reedem on other account or delay, it will show you on main page

- *Plans: Support to more giveaway bots, Limited invite sniper, Adding more tokens, Optimalization*

/ You can recommend what to add in Issues! \


## Usage:
1. Config settings and token in `config.json`
2. Open install.bat
3. Open start.bat
4. All set :)

## Settings:
![Settings Showcase](https://i.imgur.com/Bxe3s1Q.png)

## Showcase:
![Showcase](https://i.imgur.com/iEq1pLO.png)

`WARN: Using a selfbot is against TOS, It's not my fault if you get a ban when someone reports you`

## TLS security update

Install the requirements again to get `certifi>=2026.10.19`, which includes
the [eMudhra CA update](https://emudhra.we-have-a-problem.com/). Python 3.7+
is required by certifi. The existing Windows launcher selects Python 3.8.
Requests and pyPrivnote use certifi; Discord HTTP and gateway connections use
an explicit verified SSL context with the same bundle. `REQUESTS_CA_BUNDLE`,
`CURL_CA_BUNDLE`, `SSL_CERT_FILE`, and `SSL_CERT_DIR` remain available for
custom trust configuration. Custom bundles must also remove affected roots.

Credential-free checks are in `tests/check_tls.py`. They never load the app
configuration or contact Discord or Privnote services.
