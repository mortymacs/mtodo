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
//FernSphex Todo Header File.
#ifndef _FERNSPHEX_TODO_HEADER
#define _FERNSPHEX_TODO_HEADER

//Headers
#include <gtk/gtk.h>
#include <gdk/gdk.h>
#include <stdarg.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pwd.h>

//Libs
char *home_dir();
char *db_file();
int is_file_empty(char *, bool);
char *create_title_text(char *);

//Database
typedef struct {
  int id;
  char *title;
  char *description;
  int is_done;
  int is_important;
} todo_data;
sqlite3 *open_db();
void close_db(sqlite3 *);
int insert_db(char *, char *, int, int);
todo_data **select_db(int);
bool delete_db(int);
bool update_db();
bool update_db(int, char *, char *, int, int);
bool create_db();
void check_db();

//Widgets
typedef struct {
  GtkWidget *btn;
  GtkWidget *box;
  int id;
  char action[10]; //new, edit, delete
} signal_data;
typedef struct {
  int id;
  GtkWidget *btn;
  GtkWidget *refresh_box;
  GtkWidget *title;
  GtkWidget *description;
  GtkWidget *is_done;
  GtkWidget *is_important;
} todo_items;
GtkWidget *create_window(char *, int, int, GtkWidget *, bool, bool);
GtkWidget *create_headerbar(char *, int, ...);
GtkWidget *create_bigbutton(char *, char *, char *);
GtkWidget *create_button(char *, char *);
GtkWidget *create_input(char *, char *, bool, int, char *);
GtkWidget *create_switchbox(bool);
GtkWidget *create_label(char *, bool);
GtkWidget *create_alert(char *, char *, char *);
char *get_entry_text(GtkWidget *, bool);
int get_switch_value(GtkWidget *);
void show_no_todo_alert();

//Windows
void todo_window();
void todo_details_window(signal_data *);
void todo_details(GtkWidget *, gpointer);
#endif
