<div align="center">
     <p style="text-align:center"><h2>MTodo</h2></p>
     <p style="text-align:center">Simple Todo Software For GNU/Linux</p>
     <img src="screenshot.png">
</div>

<h3>Install</h3>

```
$ wget https://github.com/Mortezaipo/MTodo/archive/v1.0.0.tar.gz
$ mkdir /opt/mtodo/ && tar xzf v1.0.0.tar.gz -C /opt/mtodo/ --strip-components 1
$ /opt/mtodo/bin/mtodo
```

Desktop file (save to ~/.local/share/applications/mtodo.desktop):

```
[Desktop Entry]
Version=1.0
Type=Application
Name=MTodo
Icon=/opt/mtodo/mtodo.png
Exec=/opt/mtodo/bin/mtodo
Comment=Simple Todo management
Categories=utility
Terminal=false
```

<h3>Contribute:</h3>
Please create issues on Github to report bugs, send feature requests and so on. If you've developed good git commits after forking on Github, then please create pull requests in order to request a review and merge you commits.

<h3>License:</h3>
GNU GENERAL PUBLIC LICENSE Version 3 (GNU GPLv3)
<br>
<strong>Icon owner:<strong> http://laurareen.com/ <br>
<strong>Icon license:</strong> https://creativecommons.org/licenses/by/3.0/
