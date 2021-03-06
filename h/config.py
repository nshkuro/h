import os
import urlparse


def settings_from_environment():
    settings = {}

    # DATABASE_URL matches the Heroku environment variable
    if 'DATABASE_URL' in os.environ:
        urlparse.uses_netloc.append("postgres")
        urlparse.uses_netloc.append("sqlite")
        url = list(urlparse.urlparse(os.environ["DATABASE_URL"]))
        if url[0] == 'postgres':
            url[0] = 'postgresql+psycopg2'
        settings['sqlalchemy.url'] = urlparse.urlunparse(url)

    if 'ELASTICSEARCH_INDEX' in os.environ:
        settings['es.index'] = os.environ['ELASTICSEARCH_INDEX']

    # ELASTICSEARCH_PORT and MAIL_PORT match Docker container links
    if 'ELASTICSEARCH_PORT' in os.environ:
        es_host = os.environ['ELASTICSEARCH_PORT_9200_TCP_ADDR']
        es_port = os.environ['ELASTICSEARCH_PORT_9200_TCP_PORT']
        settings['es.host'] = 'http://{}:{}'.format(es_host, es_port)

    if 'MAIL_PORT' in os.environ:
        mail_host = os.environ['MAIL_PORT_25_TCP_ADDR']
        mail_port = os.environ['MAIL_PORT_25_TCP_PORT']
        settings['mail.host'] = mail_host
        settings['mail.port'] = mail_port

    if 'REDIS_PORT' in os.environ:
        redis_host = os.environ['REDIS_PORT_6379_TCP_ADDR']
        redis_port = os.environ['REDIS_PORT_6379_TCP_PORT']
        settings['redis.sessions.host'] = redis_host
        settings['redis.sessions.port'] = redis_port

    if 'SESSION_SECRET' in os.environ:
        settings['session.secret'] = os.environ['SESSION_SECRET']
        settings['redis.sessions.secret'] = os.environ['SESSION_SECRET']

    if 'STATSD_PORT' in os.environ:
        statsd_host = urlparse.urlparse(os.environ['STATSD_PORT_8125_UDP'])
        settings['statsd.host'] = statsd_host.hostname
        settings['statsd.port'] = statsd_host.port

    return settings
