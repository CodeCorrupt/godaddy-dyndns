#!/usr/bin/env python3

import configparser
import ipaddress
import logging
import logging.handlers
import pygodaddy
import requests
import sys

PREVIOUS_IP_FILE = 'previous-ip.txt'


def raise_if_invalid_ip(ip):
   ipaddress.ip_address(ip)


def get_public_ip():
   r = requests.get('https://api.ipify.org')
   r.raise_for_status()
   
   ip = r.text
   raise_if_invalid_ip(ip)

   return ip


def get_previous_public_ip():
   try:
      with open(PREVIOUS_IP_FILE, 'r') as f:
         ip = f.read()
   except FileNotFoundError:
      return None
    
   # Sanity check
   raise_if_invalid_ip(ip)

   return ip


def store_ip_as_previous_public_ip(ip):
   with open(PREVIOUS_IP_FILE, 'w') as f:
      f.write(ip)


def get_public_ip_if_changed():
   current_public_ip = get_public_ip()
   previous_public_ip = get_previous_public_ip()

   if current_public_ip != previous_public_ip:
      return current_public_ip
   else:
      return None


def get_godaddy_client():
   config = configparser.ConfigParser()
   config.read('godaddy-dyndns.conf')

   client = pygodaddy.GoDaddyClient()
   is_logged_in = client.login(config.get('godaddy', 'username'),
                               config.get('godaddy', 'password'))
   if not is_logged_in:
      raise RuntimeError('Could not log in into GoDaddy')

   return client


def init_logging():
   l = logging.getLogger()
   rotater = logging.handlers.RotatingFileHandler('godaddy-dyndns.log', maxBytes=10000000, backupCount=2)
   l.addHandler(rotater)
   l.setLevel(logging.INFO)
   rotater.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

def main():
   init_logging()
   
   ip = get_public_ip_if_changed()
    
   # If the IP hasn't changed then there's nothing to do.
   if ip is None:
      return None

   client = get_godaddy_client()

   logging.info("Changing all domains to %s" % ip)
   
   for domain in client.find_domains():
      for dns_record in client.find_dns_records(domain):
         full_domain = "%s.%s" % (dns_record.hostname, domain)
   
         if ip == dns_record.value:
            # There's a race here (if there are concurrent writers),
            # but there's not much we can do with the current API.
            logging.info("%s unchanged" % full_domain)
         else:
            if not client.update_dns_record(full_domain, ip):
               raise RuntimeError('DNS update failed for %s' % full_domain)

            logging.info("%s changed from %s" % (full_domain, dns_record.value))
            
   store_ip_as_previous_public_ip(ip)


if __name__ == '__main__':
   try:
      main()
   except Exception as e:
      logging.error('Exception: %s' % e)
      logging.shutdown()
      sys.exit(1)
