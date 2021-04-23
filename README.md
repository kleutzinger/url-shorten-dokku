# Url Shortener

https://u.kevbot.xyz/

## How it works

User visits homepage

- input box to input link
- On input:
  - check if url already exists shortened
    - if so, provide the already shortened link
    - DONE
  - Generate hash of link and use that for the shortening somehow?

## Todo

- [x] store in redis: `s:short_url -> long_url, l:long_url -> {short_hash, salt, pw_hash}`
- [x] find appropriate hashing library
- [ ] implement salt and delete pw for links
- [x] create index.html
- [x] show shortened link on creation
  - [x] form must send ajax
- [x] allow redirects at /ABC123
- [x] allow post requests to make new links
  - [ ] delete requests
- [ ] validate incoming urls?
  - [ ] enforce fully qualified urls
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
- [ ] confirmation message

- [ ] prevent shortening https://url-shortener.kevbot.xyz links
  - [ ] prevent redirect loops
