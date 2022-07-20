import os
import urllib
from django.core import files
from django.utils import timezone
import robots
import requests
from bs4 import BeautifulSoup


class Metadata:
    def __init__(self, url, get_filename=None):
        self.url = url
        self.get_filename = get_filename

        self.soup = None

        self.metadata = {
            "title": None,
            "icon": None,
            "image": None,
            "image_alt": None,
            "description": None,
            "link_type": None,
        }
        self.fetch_stats = {
            "last_fetched_at": None,
            "is_fetch_allowed": None,
            "is_fetch_image_allowed": None,
            "is_fetch_icon_allowed": None,
        }

    @staticmethod
    def download_file_from_url(source_url, out_filename):
        try:
            request = requests.get(source_url, stream=True)
        except Exception as error:
            raise error

        if request.status_code != requests.codes.ok:
            return None

        # Create a temporary file
        temp_file = files.temp.NamedTemporaryFile(delete=True)

        # Read the streamed image in sections
        for block in request.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break

            # Write image block to temporary file
            temp_file.write(block)

        temp_file.flush()
        return files.File(temp_file, name=out_filename)

    def get_filepath_from_url(self, url):
        path = urllib.parse.urlparse(url).path

        if self.get_filename:
            filename = self.get_filename()
            ext = os.path.splitext(path)[1]
            return f"{filename}{ext}"

        return os.path.basename(path)

    def can_fetch(self, url, namespace=None):
        robotfile_url = urllib.parse.urljoin(self.url, '/robots.txt')
        parser = robots.RobotsParser.from_uri(robotfile_url)
        is_fetchable = parser.can_fetch("*", url)

        match namespace:
            case 'icon':
                self.fetch_stats["is_fetch_icon_allowed"] = is_fetchable
            case 'image':
                self.fetch_stats["is_fetch_image_allowed"] = is_fetchable
            case _:
                self.fetch_stats["is_fetch_allowed"] = is_fetchable

        return is_fetchable

    def fetch(self):
        if not self.can_fetch(self.url):
            return

        try:
            response = requests.get(self.url)
            self.soup = BeautifulSoup(response.text, 'html.parser')

            self.metadata["title"] = self.get_title()
            self.metadata["description"] = self.get_description()
            self.metadata["link_type"] = self.get_link_type()
            self.metadata["icon"] = self.get_icon()
            self.metadata["image"] = self.get_image()
            self.metadata["image_alt"] = self.get_image_alt()
            self.metadata["theme_color"] = self.get_theme_color()

            self.fetch_stats["last_fetched_at"] = timezone.now()

        except Exception as error:
            raise error

    def get_icon_url(self):
        icon = None
        all_icons = self.soup.find_all('link', rel='icon')
        for tmp_icon in all_icons:
            if tmp_icon.get('href') is None:
                continue

            if icon is None:
                icon = tmp_icon
                continue

            icon_size = icon.get('sizes', '16x16').split('x')
            tmp_icon_size = tmp_icon.get('sizes', '16x16').split('x')
            if int(icon_size[0]) < int(tmp_icon_size[0]):
                icon = tmp_icon

        if icon is None:
            return

        return icon.get('href')

    def get_icon(self):
        raw_icon_url = self.get_icon_url()
        if raw_icon_url is None:
            return

        icon_url = urllib.parse.urljoin(self.url, raw_icon_url)

        if not self.can_fetch(icon_url, namespace='icon'):
            return

        icon_filename = self.get_filepath_from_url(icon_url)
        return self.download_file_from_url(icon_url, icon_filename)

    def get_image_url(self):
        image = self.soup.find("meta", property="og:image")
        if image:
            return image.get('content')

        image = self.soup.find("meta", property="og:image:url")
        if image:
            return image.get('content')

        image = self.soup.find("meta", property="og:image:secure_url")
        if image:
            return image.get('content')

        return None

    def get_image(self):
        raw_image_url = self.get_image_url()
        if raw_image_url is None:
            return

        image_url = urllib.parse.urljoin(self.url, raw_image_url)

        if not self.can_fetch(image_url, namespace='image'):
            return

        image_filename = self.get_filepath_from_url(image_url)
        return self.download_file_from_url(image_url, image_filename)

    def get_image_alt(self):
        image_alt = self.soup.find("meta", property="og:image:alt")
        if not image_alt:
            return

        return image_alt.get('content')

    def get_link_type(self):
        link_type = self.soup.find("meta", property="og:type")
        if not link_type:
            return

        return link_type.get('content')

    def get_title(self, default=None):
        og_title = self.soup.find("meta", property="og:title")
        if og_title:
            return og_title.get('content')

        meta_title = self.soup.find("title")
        if meta_title:
            return meta_title.get_text()

        return default

    def get_description(self, default=None):
        og_desc = self.soup.find("meta", property="og:description")
        if og_desc:
            return og_desc.get('content')

        meta_desc = self.soup.find("meta", property="description")
        if meta_desc:
            return meta_desc.get('content')

        return default

    def get_theme_color(self, default=None):
        theme_color = self.soup.find("meta", attrs={"name": "theme-color"})
        if theme_color:
            return theme_color.get('content')

        return default
