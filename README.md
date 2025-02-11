# Example Supabase Auth Across Subdomains

## Overview
This project is a simple reverse proxy built using Flask and Requests. It serves as an example to help developers set up Supabase authentication across subdomains. It is intended for development purposes only.

This project is entirely based on the supbase auth nextjs starter template. [Supabase Auth Next.js Starter Template](https://supabase.com/docs/guides/auth/quickstarts/nextjs)

## Installation
To get started, you'll need to install the necessary dependencies.

### Install Flask and Requests

```bash
pip install flask requests
```

### Install npm packages

```bash
npm install
```

## Setup

### Modify /etc/hosts

```bash
sudo nano /etc/hosts
```

Add the following lines:

```bash
# root domain name does not matter, you can set it to anything you want
# but has to be the same for both subdomains. www.digglywumpus.com works
# just as well as www.auth-learn.com. middleware.ts adn server.ts in utils/supabase
# must be udpated to match the domain named in the hosts file.
127.0.0.1 www.auth-learn.com
127.0.0.1 app.auth-learn.com
```

### Add supabase url and anon key to .env.local

```bash
nano .env.local # see .env.example for reference
```

## Running

### Run the proxy

```bash
python proxy.py # must be run by root user and must be python3
```

### Run the subdomains

```bash
npm run www # for the first subdomain

# In a new terminal
npm run app # for the second subdomain
```

## Visiting the subdomains

1. Open a browser page and navigate to http://www.auth-learn.com
2. Sign in to the app, you should be redirected to http://www.auth-learn.com/protected
3. Inspect the cookies, you should see a `sb-<supabase-project-id>-auth-token` cookie.
4. Navigate to http://app.auth-learn.com/protected
5. Your auth status on the www subdomain should be shared with the app subdomain.
6. Signout on either subdomain will sign you out of both.

## Notes

Main change was made to the supabase auth nextjs starter template:

1. The following changes were made to `middleware.ts` and `server.ts` in the `utils/supabase` directory:

```ts
@@ -16,6 +16,14 @@ export const updateSession = async (request: NextRequest) => {
       process.env.NEXT_PUBLIC_SUPABASE_URL!,
       process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
       {
+        cookieOptions: { // 👈 Add this
+          domain: '.auth-learn.com', // Allow auth-learn.com and all subdomains
+          secure: false,
+          sameSite: 'lax',
+          path: '/',
+          maxAge: 60 * 60 * 24 * 30,
+          httpOnly: true,
+        },
         cookies: {
           getAll() {
             return request.cookies.getAll();
```

I created a video walkhrough a live demo of this project [here](https://youtu.be/AhMpIxzF0Yk).