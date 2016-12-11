service ProjectHandle {
    string add_projects(1:required string projects),
    string remove_projects(1:required string programs),
    string get_projects(1:required string data),
    string update_project(1:required string data),
    string do_actions(1:required string data),
    string ping(),
}