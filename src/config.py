"""Config handler class."""
import lib


class Config:
    """Config class."""

    __instance = None
    _home_dir = None
    _project_dir = ".mtodo"
    _files = {"config": "mtodo", "database": "mtodo.db"}

    def __init__(self):
        """Initialize Config class."""
        self._home_dir = lib.home_dir()
        self._base_dir = lib.base_dir()
        self._user_preference_file = lib.join_path(lib.join_path(self._home_dir, self._project_dir),
                                                   self._files["config"])

    def __new__(cls):
        """Singletone implementation."""
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls)
        return cls.__instance

    def start(self):
        """Start software by checking required files and directry."""

        # Check user home directory
        if not self._home_dir:
            lib.error("User doesn't have home directory!")
            lib.exit_software(1)

        # Check project directory
        if not lib.is_exists(self._home_dir, self._project_dir):
            if not lib.create_dir(self._home_dir, self._project_dir):
                lib.error("Couldn't create project directory in your home({}) directory.".format(self._home_dir))
                lib.exit_software(1)

        project_dir = lib.join_path(self._home_dir, self._project_dir)

        # Check config file
        if not lib.is_exists(project_dir, self._files["config"]):
            if not lib.create_file_with_content(project_dir, self._files["config"], "style=default\ndark=false"):
                lib.error("Could'nt create config file in the project({}) directory.".format(project_dir))
                lib.exit_software(1)

        # Check database file
        if not lib.is_exists(project_dir, self._files["database"]):
            if not lib.create_empty_db_file(project_dir, self._files["database"]):
                lib.error("Couldn't create empty database in the project({}) directory.".format(project))
                lib.exit_software(1)

    @property
    def project_dir(self):
        """Return project directory path."""
        return lib.join_path(self._home_dir, self._project_dir)

    @property
    def software_style_name(self):
        """Get software style name from config file."""
        with open(lib.join_path(self.project_dir, self._files["config"]), "r") as f:
            for line in f:
                if line.startswith("style"):
                    return line[6:].strip()

    @property
    def software_style_file(self):
        """Return software style file."""
        # user path
        path1 = lib.join_path(self.project_dir, "styles/{}.css".format(self.software_style_name))
        # system path
        path2 = lib.join_path(lib.base_dir(), "styles/{}.css".format(self.software_style_name))

        if lib.is_exists(path1):
            return path1
        return path2

    @property
    def software_icon_file(self):
        """Return software icon file."""
        icon_path = lib.join_path(lib.base_dir(), "mtodo.png")

        if lib.is_exists(icon_path):
            return icon_path

    @property
    def software_is_dark_style(self):
        """Get software style name from config file."""
        with open(lib.join_path(self.project_dir, self._files["config"]), "r") as f:
            for line in f:
                if line.startswith("dark"):
                    return line[5:].strip()

    @property
    def database_path(self):
        """Return database file address."""
        return lib.join_path(self.project_dir, self._files["database"])

    @property
    def height_and_width(self) -> tuple:
        """Return height and width."""
        height = 0
        width = 0
        with open(self._user_preference_file) as f:
            for line in f:
                if not line.strip():
                    continue
                key, value = line.strip().split("=")
                if key == "height":
                    height = int(value)
                if key == "width":
                    width = int(value)
        return height, width

    def update_file(self, data: dict) -> None:
        """Update config file based on data."""
        preferences = {}
        with open(self._user_preference_file) as f:
            for line in f:
                if not line.strip():
                    continue
                key, value = line.strip().split("=")
                preferences.update({key: value})

        # override current key/value by new key/value
        preferences.update(data)

        str_data = ""
        for key, value in preferences.items():
            str_data += f"{key}={value}\n"

        with open(self._user_preference_file, "w") as f:
            f.write(str_data)
