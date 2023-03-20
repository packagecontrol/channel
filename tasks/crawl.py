import bz2
import gzip
import datetime
import json
import os
import time
import hashlib

from decimal import Decimal

from pathlib import Path
from urllib.error import HTTPError

from lib.package_control import sys_path
from lib.package_control.downloaders.rate_limit_exception import RateLimitException
from lib.package_control.providers import JsonRepositoryProvider

settings = {
    "debug": False,

    "max_releases": 1,
    "min_api_calls": False,

    "http_cache": True,
    "http_cache_length": 31536000,

    "http_basic_auth": {
        "api.github.com": [os.environ.get("GH_USER"), os.environ.get("GH_PASS")]
    },

    "user_agent": "Package Control Crawler 4.0"
}

class JsonDatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


def store_asset(filename, content):
    """
    Stores an asset uncompressed and as gzip, bzip2 archive.

    :param filename:
        The filename
    :param content:
        The content
    """
    filename         = str(filename)
    new_filename     = filename + '-new'
    new_filename_gz  = filename + '.gz-new'
    new_filename_bz2 = filename + '.bz2-new'
    filename_gz      = filename + '.gz'
    filename_bz2     = filename + '.bz2'
    filename_sha512  = filename + '.sha512'

    encoded_content = content.encode('utf-8')
    content_hash = hashlib.sha512(encoded_content).hexdigest().encode('utf-8')

    # Abort, if content hasn't changed so http server continues to return 304
    # if clients already have a locally cached copy.
    try:
        with open(filename_sha512, 'rb') as f:
            if f.read().strip() == content_hash:
                return False
    except FileNotFoundError:
        pass

    with open(new_filename, 'wb') as f:
        f.write(encoded_content)
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass
    os.rename(new_filename, filename)

    with gzip.open(new_filename_gz, 'w') as f:
        f.write(encoded_content)
    try:
        os.unlink(filename_gz)
    except FileNotFoundError:
        pass
    os.rename(new_filename_gz, filename_gz)

    with bz2.open(new_filename_bz2, 'w') as f:
        f.write(encoded_content)
    try:
        os.unlink(filename_bz2)
    except FileNotFoundError:
        pass
    os.rename(new_filename_bz2, filename_bz2)

    with open(filename_sha512, 'wb') as f:
        f.write(content_hash)

    return True


def run(
    cache_dir=None,
    dist_dir=None
):
    # determine root path
    root = Path().cwd()

    # adjust cache path
    if not cache_dir:
        cache_dir = root / "cache"
    sys_path.set_cache_dir(cache_dir)

    # get list of blacklisted urls
    try:
        with open(root / "blacklist.json", encoding="utf-8") as fp:
            blacklist = json.load(fp)
    except FileNotFoundError:
        blacklist = []

    # # read settings
    # with open(root / "settings.json", encoding="utf-8") as fp:
    #     settings = json.load(fp)

    repo_urls = ["repository.json"]

    broken_libraries = set()
    broken_packages = set()
    failed_sources = set()

    packages_cache = {}
    libraries_cache = {}

    num_packages = 0
    num_libraries = 0

    begin_time = time.time()

    if repo_urls:
        for repo_url in repo_urls:
            repo = JsonRepositoryProvider(repo_url, settings)
            if not repo:
                continue

            print(f"Fetching packages from {repo_url}...")

            try:
                packages = [package for _, package in repo.get_packages(blacklist)]
            except Exception as e:
                print(f"  Failed to fetch packages: {e}")
            else:
                packages_cache[repo_url] = packages
                if packages:
                    print(f"  Fetched {len(packages)} packages.")
                    num_packages += len(packages)

            try:
                libraries = [library for _, library in repo.get_libraries(blacklist)]
            except Exception as e:
                print(f"  Failed to fetch libraries: {e}")
            else:
                libraries_cache[repo_url] = libraries
                if libraries:
                    print(f"  Fetched {len(libraries)} libraries.")
                    num_libraries += len(libraries)

            broken_libraries |= repo.get_broken_libraries()
            broken_packages |= repo.get_broken_packages()
            failed_sources |= repo.get_failed_sources()

    if failed_sources:
        url_to_review = set()
        url_failed = set()

        for url, err in failed_sources:
            if isinstance(err, RateLimitException):
                pass
            if isinstance(err, HTTPError) and err.code == 404:
                url_to_review.add(url)
            else:
                url_failed.add((url, err))

        if url_to_review:
            print("Missing Sources (needs review):")
            url_to_review = sorted(url_to_review)
            for url in url_to_review:
                print(f"  {url}")

            blacklist = sorted(set(blacklist) | set(url_to_review))

            with open(root / "blacklist.json", mode="w", encoding="utf-8") as fp:
                json.dump(blacklist, fp, indent=4)

        if url_failed:
            print("Failed Sources:")
            for url, err in sorted(url_failed):
                print(f"  {url}: {err}")

    if broken_packages:
        print("Broken Packages:")
        for lib, err in sorted(broken_packages, key=lambda s: s[0].lower()):
            print(f"  {lib}: {err}")

    if broken_libraries:
        print("Broken Libraries:")
        for lib, err in sorted(broken_libraries, key=lambda s: s[0].lower()):
            print(f"  {lib}: {err}")

    duration = time.strftime("%H:%M:%S", time.gmtime(time.time() - begin_time))
    print(f"Fetched {num_packages} packages and {num_libraries} libraries in {duration}.")

    json_content = json.dumps(
        {
            "$schema": "sublime://packagecontrol.io/schemas/repository",
            "schema_version": "4.0.0",
            "packages": packages_cache,
            "libraries": libraries_cache
        },
        cls=JsonDatetimeEncoder,
        check_circular=False,
        sort_keys=True
    )

    # setup asset directory
    if not dist_dir:
        dist_dir = root / '_site'
    dist_dir.mkdir(exist_ok=True)

    result = store_asset(dist_dir / 'libraries.json', json_content)
    if result:
        print("Stored resolved repository!")
    else:
        print("Repository unchanged, skipping!")

    return result
