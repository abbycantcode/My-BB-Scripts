#! /usr/bin/python3

import http.server
import sys
import random
import string
import argparse
import socket
import logging
import signal
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--hostname", type=str, required=True, help="Specify the hostname for the server")
parser.add_argument("--redirect", type=str)
parser.add_argument("--redirect_code", type=int)
parser.add_argument("--redirect_token", type=str)
parser.add_argument("--verbose", action="store_true")
parser.add_argument("-l", "--log_to_file", action="store_true", help="Save logs to 'server.log'")
args = parser.parse_args()

if args.log_to_file:
    logging.basicConfig(
        filename='server.log',
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

logger = logging.getLogger("custom_server")

redirect_enabled = False
redirect_target = ""
redirect_token = ""
manual_redirect_token = False
redirect_code = 303
verbose = False

url = "http://" + args.hostname + "/"

shutdown_requested = False

def exit_handler(signum, frame):
    global shutdown_requested
    if not shutdown_requested:
        logger.info("Gracefully stopping web_server.py...")
        shutdown_requested = True
        httpd.shutdown()
    else:
        logger.info("Forcing web_server.py to exit.")
        sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

try:
    if args.redirect is not None:
        logger.info("[redirect] Redirecting enabled. Target: '%s'", args.redirect)
        redirect_enabled = True
        redirect_target = args.redirect

    if args.redirect_code is not None:
        if not redirect_enabled:
            raise ValueError("[!] Redirecting is disabled. Can't set 'redirect_code'.")
        logger.info("[redirect] Setting custom redirect response code to '%d'.", args.redirect_code)
        redirect_code = args.redirect_code

    if args.redirect_token is not None:
        if not redirect_enabled:
            raise ValueError("[!] Redirecting is disabled. Can't set 'redirect_token'.")
        logger.info("[redirect] Manually setting redirect token to '%s'. Redirect URL: %s%s", args.redirect_token, url, args.redirect_token)
        redirect_token = args.redirect_token
        manual_redirect_token = True

    if args.verbose is not False:
        logger.info("[verbose] Verbose mode enabled.")
        verbose = True

    if redirect_enabled and not manual_redirect_token:
        redirect_token = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))
        logger.info("[redirect] Random redirect URL: %s%s", url, redirect_token)

    class CustomHTTPServer(http.server.HTTPServer):
        def run(self):
            try:
                self.serve_forever()
            except KeyboardInterrupt:
                pass

    class CustomServer(http.server.SimpleHTTPRequestHandler):
        def do_request(self, method):
            if verbose:
                logger.info("\n\n[verbose]")
                logger.info(self.client_address)
                try:
                    logger.info(socket.gethostbyaddr(self.client_address[0])[0])
                except:
                    logger.warning("[!] Reverse DNS failed.")
                logger.info("")
                logger.info(self.headers)
            if redirect_enabled and self.path == "/" + redirect_token:
                logger.info("[redirect] Redirect path hit! Returning %d to '%s'.", redirect_code, redirect_target)
                self.send_response(redirect_code)
                self.send_header("Location", redirect_target)
                self.end_headers()
            else:
                if method == "GET":
                    super().do_GET()
                else:
                    logger.warning("[!] Can't handle request method '%s'...", method)
                    self.send_response(501)
                    self.end_headers()

        def do_GET(self):
            self.do_request("GET")
        
        def do_POST(self):
            self.do_request("POST")

    server_address = ("0.0.0.0", 6969)
    httpd = CustomHTTPServer(server_address, CustomServer)

    logger.info("[+] Starting server. URL: %s", url)
    httpd.run()

except Exception as e:
    logger.error("[!] An error occurred: %s", str(e))
    sys.exit(1)
