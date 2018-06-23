FROM python:2

ENV SLACK_CODE_CAMP_BOT_TOKEN=slack_token_here

#used by goatme command
ENV IMGUR_CLIENT_ID=imgur_client_id_here

#optional used by ccbot command
ENV BULLY_USER_ID=bully_slack_user_id_here

#optional used by ccbot command
ENV BULLY_NAME=bully_name_here
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["ccbot/bot"]