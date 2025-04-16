# OwnTickets - Selfhosted Ticketing Discord Bot
#### If you want to use the version I host in my own servers, the link for the invite is here: https://discord.com/oauth2/authorize?client_id=1360877605577818112&scope=bot&permissions=8&redirect_uri=https%3A%2F%2Fgithub.com%2Ffredericodeveloper%2Fowntickets
## Selfhosting guide:
- #### Install [docker](https://www.docker.com/)
- #### Pull the image using `docker pull fredericodeveloper/owntickets:latest`
- #### Create a folder for the bot with file called `docker-compose.yml` inside:
```
services:
  owntickets:
    image: fredericodeveloper/owntickets:latest
    volumes:
      - ./data:/app/data:Z
    environment:
      - BOT_TOKEN=YOUR_BOT_TOKEN_HERE
    restart: always
```
- #### Run the bot using `docker compose up -d` (you might need to run it as root if you have not configured your docker to run rootless)
- #### Invite your bot to server using this link (make sure to edit the application id): https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=bot&permissions=8&redirect_uri=https%3A%2F%2Fgithub.com%2Ffredericodeveloper%2Fowntickets
## Support:
#### I offer free support for both selfhosted version and users of my hosted bot, if you have any issues with the bot, please open a issue here on github.
