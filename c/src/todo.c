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
//FernSphex Todo Window Form.
#include "todo.h"

void
todo_details(GtkWidget *btn, gpointer sd) {
    todo_details_window((signal_data *)sd);
}

void
todo_window() {
  todo_data **tdata = select_db(0);

  GtkWidget *add_new_btn = create_button("Add New", "button_success");
  GtkWidget *header = create_headerbar("FernSphex Todo", 1, add_new_btn);
  GtkWidget *window = create_window("FernSphex Todo", 500, 400, header, TRUE, TRUE);

  GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 2);
  gtk_box_set_homogeneous(GTK_BOX(box), TRUE);

  signal_data *sdn = malloc(sizeof(signal_data));
  sdn->btn = add_new_btn;
  sdn->box = box;
  sdn->id = 0;
  strcpy(sdn->action, "new");
  g_signal_connect(G_OBJECT(add_new_btn), "clicked", G_CALLBACK(todo_details), sdn);

  signal_data *sd;
  int i = 0;
  if(*tdata == NULL) {
    GtkWidget *no_todo_alert = create_alert("No Todo Found.", \
                                            "Click on 'Add New' button on your top-left side.", \
                                            "alert_normal");
    gtk_box_pack_start(GTK_BOX(box), no_todo_alert, TRUE, FALSE, 1);
  }

  while((*(tdata+i)) != NULL) {
    char *class = malloc(sizeof(char) * 22);
    if((*(tdata+i))->is_done == 1)
      strcpy(class, "todo_item_is_done");
    else if((*(tdata+i))->is_important == 1)
      strcpy(class, "todo_item_is_important");
    else
      strcpy(class, "todo_item_normal");

    GtkWidget *btn = create_bigbutton((*(tdata+i))->title, (*(tdata+i))->description, class);
    sd = malloc(sizeof(signal_data));
    sd->btn = btn;
    sd->box = box;
    sd->id = ((*(tdata+i))->id);
    strcpy(sd->action, "edit");
    g_signal_connect(G_OBJECT(btn), "clicked", G_CALLBACK(todo_details), sd);
    gtk_box_pack_start(GTK_BOX(box), btn, TRUE, FALSE, 1);
    free(class);
    i++;
  }

  gtk_container_add(GTK_CONTAINER(window), box);
  gtk_widget_show_all(window);
}
