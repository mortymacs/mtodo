/* ============================================================
                      FernSphex Todo
                    Todo Tracking Software
Copyright (C) 2016  Morteza Nourelahi Alamdari (Mortezaipo)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
============================================================ */
#include "todo.h"

int main(int argc, char *argv[]) {
  gtk_init(&argc, &argv);
  check_db();
  
  GtkCssProvider *css_provider = gtk_css_provider_new();
  gtk_css_provider_load_from_path(css_provider, "src/style.css", NULL);
  gtk_style_context_add_provider_for_screen(gdk_screen_get_default(), \
                                            GTK_STYLE_PROVIDER(css_provider),
                                            GTK_STYLE_PROVIDER_PRIORITY_USER);
  todo_window();
  gtk_main();
}
