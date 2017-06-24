"""Config handler class."""
import lib


class Config:
    """Config class."""

    __instance = None
    _home_dir = None
    _project_dir = ".mtodo"
    _files = {"config": ".mtodo", "database": ".mtodo.db"}
    
    def __init__(self):
        """Initialize Config class."""
        self._home_dir = lib.home_dir()
        self._base_dir = lib.base_dir()

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
            if not lib.create_file_with_content(project_dir, self._files["config"], "style=default"):
                lib.error("Could'nt create config file in the project({}) directory.".format(project_dir))
                lib.exit_software(1)

        # Check database file
        if not lib.is_exists(project_dir, self._files["database"]):
            if not lib.create_empty_db_file(project_dir, ".mtodo.db"):
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
    def database_path(self):
        """Return database file address."""
        return lib.join_path(self.project_dir, self._files["database"])
