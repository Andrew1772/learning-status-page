# This sets up a redis connection

import redis


def connect_to_redis():
    # These are the default redis configs for running on localhost, pulled decode_response and health_check from MCP code
    connection = redis.asyncio.Redis(
        host='localhost',
        port=6379,
        decode_responses=True,
        health_check_interval=30,
    )

    # this is used to check if redis is up and running, will continue this work after i've confirmed redis working normally
    # try:
    #     await connection.ping()
    # except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
    #     return false


    return connection
