FROM python:2

ENV SLACK_CODE_CAMP_BOT_TOKEN=<slack token here>

#used by goatme command
ENV IMGUR_CLIENT_ID=<imgur client id here> 

#optional used by ccbot command
ENV BULLY_USER_ID=<bully slack user id here> 

#optional used by ccbot command
ENV BULLY_NAME=<bully name here> 

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ccbot/bot" ]