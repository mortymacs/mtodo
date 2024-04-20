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
// New Todo Window
#include "todo.h"

void
save_todo(GtkWidget *save_btn, gpointer data) {
  todo_items *tmp_data = (todo_items *)data;
  char *title = get_entry_text(tmp_data->title, FALSE);
  char *description = get_entry_text(tmp_data->description, TRUE);
  if (tmp_data->id > 0) {
    //Update action
    update_db(tmp_data->id, title, description,
              get_switch_value(tmp_data->is_done),
              get_switch_value(tmp_data->is_important));
    if(tmp_data->btn != NULL) {
      GList *box = gtk_container_get_children(GTK_CONTAINER(tmp_data->btn));
      GList *lbls = gtk_container_get_children(GTK_CONTAINER(box->data));
      gtk_label_set_markup(GTK_LABEL(lbls->data), create_title_text(title));
      lbls = g_list_next(lbls);
      gtk_label_set_text(GTK_LABEL(lbls->data), description);
    }
  } else {
    //Save action
    signal_data *sd = malloc(sizeof(signal_data));
    sd->box = tmp_data->refresh_box;
    strcpy(sd->action, "edit");

    sd->id = insert_db(title, description, \
                       get_switch_value(tmp_data->is_done), \
                       get_switch_value(tmp_data->is_important));

    if (sd->id > 0) {
      sd->btn = create_bigbutton(get_entry_text(tmp_data->title, FALSE), \
                                 get_entry_text(tmp_data->description, TRUE), \
                                 "todo_item");

      g_signal_connect(G_OBJECT(sd->btn), "clicked", G_CALLBACK(todo_details), sd);

      gtk_box_pack_start(GTK_BOX(sd->box), sd->btn, FALSE, TRUE, 1);
      gtk_widget_show_all(sd->box);

      // if(sd->box != NULL) {
      //   gtk_widget_destroy(no_todo_alert);
      // }
    }
  }
  GtkWidget *window = gtk_widget_get_toplevel(save_btn);
  if(gtk_widget_is_toplevel(window)) {
    gtk_widget_destroy(window);
  }
  free(tmp_data);
}

void
delete_todo(GtkWidget *btn, gpointer sd) {
  if (delete_db(((signal_data *)sd)->id) == TRUE) {
    gtk_widget_destroy(((signal_data *)sd)->btn);
    gtk_widget_show_all(((signal_data *)sd)->box);
    GtkWidget *window = gtk_widget_get_toplevel(btn);
    if(gtk_widget_is_toplevel(window))
      gtk_widget_destroy(window);
  }
}

void todo_details_window(signal_data *sd) {
  GtkWidget *save_btn = create_button("Save", "button_success");
  GtkWidget *header;
  char *window_title = (sd->id == 0)?"New Todo":"Edit Todo";
  if(sd->id == 0) {
    header = create_headerbar(window_title, 1, save_btn);
  } else {
    GtkWidget *delete_btn = create_button("Delete", "button_danger");
    header = create_headerbar(window_title, 2, save_btn, delete_btn);
    g_signal_connect(delete_btn, "clicked", G_CALLBACK(delete_todo), sd);
  }

  GtkWidget *window = create_window("New Todo", 500, 430, header, FALSE, FALSE);

  char *title_data = NULL;
  char *description_data = NULL;
  bool is_done_data = FALSE;
  bool is_important_data = FALSE;

  // Look for data in database
  if(sd->id != 0) {
    todo_data **db_row = select_db(sd->id);
    if(*db_row != NULL) {
      title_data = (*(db_row))->title;
      description_data = (*(db_row))->description;
      is_done_data = ((*(db_row))->is_done == 1)?TRUE:FALSE;
      is_important_data = ((*(db_row))->is_important == 1)?TRUE:FALSE;
    }
  }

  GtkWidget *title = create_input("Todo Title", title_data, FALSE, 50, "text_normal");
  GtkWidget *description = create_input("Todo Description", description_data, TRUE, 1000, "textarea_normal");

  // Switches for is_done & is_important items.
  GtkWidget *is_done_lbl = create_label("Is todo done?", FALSE);
  GtkWidget *is_important_lbl = create_label("Is todo important?", FALSE);
  GtkWidget *is_done = create_switchbox(is_done_data);
  GtkWidget *is_important = create_switchbox(is_important_data);

  gtk_widget_set_halign(is_done_lbl, GTK_ALIGN_START);
  GtkWidget *is_done_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 2);
  gtk_box_set_homogeneous(GTK_BOX(is_done_box), FALSE);
  gtk_box_pack_start(GTK_BOX(is_done_box), is_done_lbl, TRUE, TRUE, 1);
  gtk_box_pack_start(GTK_BOX(is_done_box), is_done, FALSE, FALSE, 1);

  gtk_widget_set_halign(is_important_lbl, GTK_ALIGN_START);
  GtkWidget *is_important_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 2);
  gtk_box_set_homogeneous(GTK_BOX(is_important_box), FALSE);
  gtk_box_pack_start(GTK_BOX(is_important_box), is_important_lbl, TRUE, TRUE, 1);
  gtk_box_pack_start(GTK_BOX(is_important_box), is_important, FALSE, FALSE, 1);

  GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 2);
  gtk_box_pack_start(GTK_BOX(box), title, TRUE, TRUE, 1);
  gtk_box_pack_start(GTK_BOX(box), description, TRUE, TRUE, 1);
  gtk_box_pack_start(GTK_BOX(box), is_done_box, TRUE, TRUE, 1);
  gtk_box_pack_start(GTK_BOX(box), is_important_box, TRUE, TRUE, 1);

  todo_items *input_items = malloc(sizeof(todo_items));
  input_items->id = (sd->id != 0)?sd->id:0;
  input_items->title = title;
  input_items->description = description;
  input_items->is_done = is_done;
  input_items->is_important = is_important;
  input_items->btn = (sd->id != 0)?sd->btn:NULL;
  input_items->refresh_box = sd->box;
  g_signal_connect(save_btn, "clicked", G_CALLBACK(save_todo), input_items);

  gtk_container_add(GTK_CONTAINER(window), box);
  gtk_widget_show_all(window);
}
