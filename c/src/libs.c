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
//FernSphex Todo Extra Library.
#include "todo.h"

// Find user home address
char *home_dir() {
  struct passwd *pw = getpwuid(getuid());
  return pw->pw_dir;
}

// Database file
char *db_file() {
  char *db_file = malloc(strlen(home_dir()) + 19);
  sprintf(db_file, "%s/.fernsphex_todo.db", home_dir());
  return db_file;
}

// Check db file
int
is_file_empty(char *f_path, bool create_it) {
  if(f_path == NULL)
    return -1;

  if(access(f_path, F_OK) == -1) {
    if (create_it == TRUE) {
      FILE *x = fopen(f_path, "w+");
      fclose(x);
      return 2;
    }
    return -1;
  } else {
    struct stat st;
    stat(f_path, &st);
    if(st.st_size == 0)
      return 1;
  }
  return 0;
}

// Generate title text
char *
create_title_text(char *title) {
  char *tmp_title = malloc(sizeof(char *) * strlen(title) + 18);
  sprintf(tmp_title, "<big><b>%s</b></big>", title);
  return tmp_title;
}
