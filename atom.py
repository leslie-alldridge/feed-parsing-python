import feedparser
import json

notifications_filename = "notifications.json"

feeds = [
    "https://github.com/hashicorp/terraform/releases.atom",
    "https://github.com/hashicorp/terraform-provider-aws/releases.atom",
    "https://github.com/newrelic/terraform-provider-newrelic/releases.atom",
    "https://github.com/hashicorp/terraform-provider-time/releases.atom"
]

exclusion_words = [
    "alpha",
    "beta",
    "-rc"
]


def read_previous_feeds():
    """
    Read previous feeds into memory
    """
    f = open(notifications_filename)
    data = json.load(f)
    return data


def write_feeds_to_file(previous_feeds, new_feeds):
    """
    Write feeds to file
    """
    f = open(notifications_filename, "w")
    f.write(json.dumps(previous_feeds + new_feeds))
    f.close()



def filter_entry(entry):
    """
    Filters entries based on exclusion words
    """

    if not any(word for word in exclusion_words if word in entry.id):
        return entry.id


def parse_feeds(feeds, previous_feeds):
    """
    Parse a list of feeds
    Filter the feeds and return filtered list
    Skip the feed if its included in previous feeds
    """
    filtered_entries = []

    for feed in feeds:
        print(f"Processing feed: {feed}")
        response = feedparser.parse(feed)

        latest_release = response.entries[0]
        if filter_entry(latest_release):
            data = {"release": latest_release.id.split("/")[2], "link": latest_release.link}

            if data not in previous_feeds:
                filtered_entries.append(data)
            else:
                print("Feed was already shared. Skipping...")
    
    return filtered_entries


if __name__ == "__main__":
    previous_feeds = read_previous_feeds()
    new_feeds = parse_feeds(feeds, previous_feeds)
    write_feeds_to_file(previous_feeds, new_feeds)
