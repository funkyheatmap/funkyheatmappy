def calculate_row_positions(row_info, row_height, row_space, row_bigspace):
    row_pos = row_info
    row_pos["group_i"] = row_info.groupby("group").ngroup()
    row_pos["color_background"] = row_info["group_i"] % 2

    return row_pos