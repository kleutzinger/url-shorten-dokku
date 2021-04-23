# Url Shortener

Live At: https://u.kevbot.xyz/  

Cli Example:  
`curl -X POST https://u.kevbot.xyz/api/url -d 'url=https://google.com/'`  

## Running Locally:

1. start a local redis server `redis-server`
1. set `REDIS\_URL` environment variable (probably: `redis://localhost:6379`)
1. or `mv .env.example .env` and edit in there
1. start a python [virtual environment](https://docs.python.org/3/tutorial/venv.html)
1. `python -m pip install -r requirements.txt`
1. `python app.py`
1. open https://localhost:5000

## Todo

- [x] store in redis: `s:short_url -> long_url, l:long_url -> {short_hash, salt, pw_hash}`
- [x] find appropriate hashing library
- [x] create index.html
- [x] show shortened link on creation
  - [x] form must send ajax
- [x] allow redirects at /ABC123
- [x] allow post requests to make new links
  - [ ] delete requests
- [x] validate incoming urls?
  - [x] enforce fully qualified urls
  - [ ] max url length (100?)
- [ ] rate limiting?
- [ ] make full post, get, delete backend
- [x] create simple form / frontend to create new link
  - [x] text input box
  - [x] with password box
  - [x] submit button
  - [x] post(?) request
- [ ] create delete link form
- [ ] text input shortened (or long?) url
- [x] submit button
- [x] short url -> big url on page after submit
- [ ] implement salt and delete pw for links
- [ ] prevent shortening https://url-shortener.kevbot.xyz links
  - [ ] prevent redirect loops
