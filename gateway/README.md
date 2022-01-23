## Env Information
Most configuration really isn't about the app -- it's about where the app runs, what keys it needs to communicate with third party API's, the db password and username, etc... They're just deployment details -- and there are lots of tools to help manage environment variables -- not the least handy being a simple .env file with all your settings. Simply source the appropriate env before you launch the app in the given env (you could make it part of a launch script, for instance).

env files look like this:

    SOMEVAR="somevalue"
    ANOTHERVAR="anothervalue"

To source it:
``` Bash
    $ source sample.env  # or staging.env, or production.env, depending on where you're deploying to
```
## Run gateway server
> [!NOTE]
> We used python 3.10.1 64-bit version!
> And don't forget to change your .env settings!
``` Bash
$ pip3 install -r requirements.txt
$ python3 gateway.py
```