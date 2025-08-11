Millia Xrd Vods
This webapp isis for hosting and viewing replays of Millia from the video game Guilty Gear Xrd Revelator 2. It's built with a Python/Flask backend, running through gunicorn server and nginx reverse proxy (for ssl and security) in production. 

Once Ranger's videos are public, additional features may be added:
- Personal Bookmarks
- Scoring vods
- Automatic validation of links
- Validating original vod timestamps
- Rate limiting through ngnix

### Prerequisites
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation) is a good alternative to pip, but not needed if simply running through containers

### Installation and Setup
1. Clone the repository
```bash
git clone https://github.com/wbhemingway/milliavod
cd milliavod
```

2. if running in a prod enviorment, get certificates through [letsencrypt](https://letsencrypt.org/getting-started) or your domain registrar and put them in a certs folder in your project directory. You will need to change the nginx.conf file to your own domain name where it references milliaxrdreplays.com

3. Create .prod.env and db.env
- .prod.env needs SECRET_KEY, GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET from [Google](https://developers.google.com/identity/protocals/oauth2), and a DATABASE_URL
- .db.env needs MYSQL_RANDOM_ROOT_PASSWORD="yes", MYSQL_DATABASE and MYSQL_USER both set to milliavod, and a secure MYSQL_PASSWORD

### Running The project
- To start the containers and network locally, run the command
```bash
docker compose up --build -d -f compose-dev.yaml
```

- To run them in production with nginx, run the command
```bash
docker compose up --build -d
```

### Contribute
If you would like to work on the features above, or others not mentioned, feel free to do so! If you're working on this project, it's easiest to reach me through the millia xrd discord server.

License
This project is licensed under the MIT License - see the LICENSE file for details.