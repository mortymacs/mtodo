#include "../src/todo.h"
#include <assert.h>

void test_home_dir() {
  char *starts_with = "/home/";
  char *tmp = home_dir();
  assert(strncmp(tmp, starts_with, 6) == 0);
}

int main() {
  test_home_dir();
  return 0;
}
