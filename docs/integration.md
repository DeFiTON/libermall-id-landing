# Integration guide

Hands-on code snippets for adding "Continue with Libermall ID" to your application. Covers Node.js, Laravel, Next.js, Python, and `curl`. All examples use the **OpenID Connect Authorization Code + PKCE** flow — the modern recommended default.

## Prerequisites

1. Request a client at [`hello@libermall.com`](mailto:hello@libermall.com) (or the developer tier signup flow). You'll receive a `client_id` and `client_secret`.
2. Register at least one **redirect URI** — exact match, including scheme and trailing path. For local development, `http://localhost:3000/oauth/libermall/callback` is fine.
3. Choose your scopes:
   - `openid` *(required)*
   - `profile` — name, avatar, username
   - `email` — verified email if user attached one
   - `wallets` — array of attached TON wallets (Web3 apps)
   - `telegram` — Telegram user id (chat-aware apps)

## OIDC endpoints

You should always discover endpoints rather than hard-coding them:

```
https://id.libermall.com/.well-known/openid-configuration
```

The relevant values:

```
authorization_endpoint   https://id.libermall.com/login/oauth/authorize
token_endpoint           https://id.libermall.com/api/login/oauth/access_token
userinfo_endpoint        https://id.libermall.com/api/userinfo
jwks_uri                 https://id.libermall.com/.well-known/jwks
end_session_endpoint     https://id.libermall.com/api/logout
```

## Node.js (openid-client)

```bash
npm install openid-client
```

```js
import { Issuer, generators } from 'openid-client';

const issuer = await Issuer.discover('https://id.libermall.com');

const client = new issuer.Client({
  client_id: process.env.LIBERMALL_CLIENT_ID,
  client_secret: process.env.LIBERMALL_CLIENT_SECRET,
  redirect_uris: ['https://yourapp.com/oauth/libermall/callback'],
  response_types: ['code'],
});

// 1. Redirect the user
app.get('/login/libermall', (req, res) => {
  const code_verifier = generators.codeVerifier();
  const code_challenge = generators.codeChallenge(code_verifier);
  req.session.code_verifier = code_verifier;

  const url = client.authorizationUrl({
    scope: 'openid profile email wallets',
    code_challenge,
    code_challenge_method: 'S256',
    state: generators.state(),
  });
  res.redirect(url);
});

// 2. Handle the callback
app.get('/oauth/libermall/callback', async (req, res) => {
  const params = client.callbackParams(req);
  const tokenSet = await client.callback(
    'https://yourapp.com/oauth/libermall/callback',
    params,
    { code_verifier: req.session.code_verifier, state: req.query.state },
  );

  const user = await client.userinfo(tokenSet.access_token);
  // user → { sub, name, email, telegram_id, ton_wallets[] }

  req.session.user = user;
  res.redirect('/');
});
```

## Next.js (NextAuth.js)

```bash
npm install next-auth
```

`app/api/auth/[...nextauth]/route.ts`:

```ts
import NextAuth from 'next-auth';

const handler = NextAuth({
  providers: [
    {
      id: 'libermall',
      name: 'Libermall ID',
      type: 'oauth',
      wellKnown: 'https://id.libermall.com/.well-known/openid-configuration',
      authorization: { params: { scope: 'openid profile email wallets' } },
      clientId: process.env.LIBERMALL_CLIENT_ID,
      clientSecret: process.env.LIBERMALL_CLIENT_SECRET,
      idToken: true,
      checks: ['pkce', 'state'],
      profile(profile) {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          telegram_id: profile.telegram_id,
          wallets: profile.ton_wallets,
        };
      },
    },
  ],
});

export { handler as GET, handler as POST };
```

Drop the button:

```tsx
import { signIn } from 'next-auth/react';

<button onClick={() => signIn('libermall')}>
  Continue with Libermall ID
</button>
```

## Laravel (Socialite)

```bash
composer require socialiteproviders/generic
```

`config/services.php`:

```php
'libermall' => [
    'client_id'     => env('LIBERMALL_CLIENT_ID'),
    'client_secret' => env('LIBERMALL_CLIENT_SECRET'),
    'redirect'      => env('APP_URL').'/oauth/libermall/callback',
    'host'          => 'https://id.libermall.com',
],
```

`app/Http/Controllers/Auth/LibermallController.php`:

```php
public function redirect()
{
    return Socialite::driver('libermall')
        ->scopes(['openid', 'profile', 'email', 'wallets'])
        ->redirect();
}

public function callback()
{
    $oauth = Socialite::driver('libermall')->user();

    $user = User::updateOrCreate(
        ['external_id' => $oauth->getId()],
        [
            'name'         => $oauth->getName(),
            'email'        => $oauth->getEmail(),
            'avatar'       => $oauth->getAvatar(),
            'telegram_id'  => $oauth->user['telegram_id'] ?? null,
            'password'     => bcrypt(Str::random(40)),
        ],
    );

    auth()->login($user, remember: true);
    return redirect()->intended('/');
}
```

Routes:

```php
Route::get('/oauth/libermall',          [LibermallController::class, 'redirect'])->name('libermall.redirect');
Route::get('/oauth/libermall/callback', [LibermallController::class, 'callback'])->name('libermall.callback');
```

> **Order matters** if your app has a wildcard route like `/{provider}/callback`. Register the explicit Libermall routes *before* the wildcard, otherwise the wildcard catches everything and your handler never runs.

## Python (authlib + FastAPI)

```bash
pip install authlib fastapi 'uvicorn[standard]' itsdangerous
```

```python
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="...")

oauth = OAuth()
oauth.register(
    name="libermall",
    server_metadata_url="https://id.libermall.com/.well-known/openid-configuration",
    client_id="...",
    client_secret="...",
    client_kwargs={"scope": "openid profile email wallets"},
)

@app.get("/login")
async def login(request: Request):
    return await oauth.libermall.authorize_redirect(
        request, "https://yourapp.com/oauth/libermall/callback",
    )

@app.get("/oauth/libermall/callback")
async def callback(request: Request):
    token = await oauth.libermall.authorize_access_token(request)
    user = token["userinfo"]
    request.session["user"] = dict(user)
    return RedirectResponse("/")
```

## curl (test from your terminal)

```bash
# 1. Send the user to authorize
open "https://id.libermall.com/login/oauth/authorize?\
client_id=$LIBERMALL_CLIENT_ID&\
response_type=code&\
scope=openid+profile+email&\
redirect_uri=https://yourapp.com/cb&\
state=demo&\
code_challenge=$CHALLENGE&\
code_challenge_method=S256"

# 2. Exchange code (received at the redirect_uri)
curl -X POST https://id.libermall.com/api/login/oauth/access_token \
  -u "$LIBERMALL_CLIENT_ID:$LIBERMALL_CLIENT_SECRET" \
  -d 'grant_type=authorization_code' \
  -d "code=$CODE" \
  -d "redirect_uri=https://yourapp.com/cb" \
  -d "code_verifier=$VERIFIER"

# 3. Get user info
curl https://id.libermall.com/api/userinfo \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## ID token claims

```json
{
  "iss": "https://id.libermall.com",
  "sub": "internal-uuid-never-changes",
  "aud": "your_client_id",
  "exp": 1746028800,
  "iat": 1746025200,
  "name": "Alice",
  "email": "alice@example.com",
  "email_verified": true,
  "picture": "https://id.libermall.com/avatars/...",
  "telegram_id": 123456789,
  "ton_wallets": ["UQAbc..."],
  "auth_methods": ["telegram", "ton_connect"]
}
```

`sub` is the user's **stable** identifier — use it as the foreign key in your database. Everything else can change.

## Going live

- [ ] Replace test client with production client credentials (different ones).
- [ ] Update redirect URIs to production URLs only.
- [ ] Set token storage to encrypted, HTTP-only cookies (not LocalStorage).
- [ ] Verify the ID token signature against [`/.well-known/jwks`](https://id.libermall.com/.well-known/jwks) before trusting it.
- [ ] Set `Cache-Control: no-store` on auth-related responses.
- [ ] Configure CSP `connect-src https://id.libermall.com` if you call the JWKS endpoint from the browser.

## Help

Stuck? Email [`hello@libermall.com`](mailto:hello@libermall.com) with: language, framework, the request you're sending, and the response you got. We aim to reply within one business day.
