def get_ids():
    time_ranges = {
        0: "File will not be deleted",
        1: "5 minutes",
        2: "15 minutes",
        3: "30 minutes",
        4: "1 hour",
        5: "3 hours",
        6: "6 hours",
        7: "12 hours",
        8: "1 day",
        9: "2 days",
        10: "3 days",
        11: "4 days",
        12: "5 days",
        13: "6 days",
        14: "1 week",
        15: "2 weeks",
        16: "3 weeks",
        17: "1 month",
        18: "2 months",
        19: "3 months",
        20: "4 months",
        21: "5 months",
        22: "6 months",
        23: "1 year"
    }
    
    return time_ranges


def get_id_by_time(seconds):
    time_ranges = {
        0: 0,         # file will not be deleted
        1: 5 * 60,    # 5 minutes
        2: 15 * 60,   # 15 minutes
        3: 30 * 60,   # 30 minutes
        4: 1 * 60 * 60,   # 1 hour
        5: 3 * 60 * 60,   # 3 hours
        6: 6 * 60 * 60,   # 6 hours
        7: 12 * 60 * 60,  # 12 hours
        8: 24 * 60 * 60,  # 1 day
        9: 2 * 24 * 60 * 60,   # 2 days
        10: 3 * 24 * 60 * 60,  # 3 days
        11: 4 * 24 * 60 * 60,  # 4 days
        12: 5 * 24 * 60 * 60,  # 5 days
        13: 6 * 24 * 60 * 60,  # 6 days
        14: 7 * 24 * 60 * 60,  # 1 week
        15: 2 * 7 * 24 * 60 * 60,  # 2 weeks
        16: 3 * 7 * 24 * 60 * 60,  # 3 weeks
        17: 30 * 24 * 60 * 60,  # 1 month
        18: 2 * 30 * 24 * 60 * 60,  # 2 months
        19: 3 * 30 * 24 * 60 * 60,  # 3 months
        20: 4 * 30 * 24 * 60 * 60,  # 4 months
        21: 5 * 30 * 24 * 60 * 60,  # 5 months
        22: 6 * 30 * 24 * 60 * 60,  # 6 months
        23: 365 * 24 * 60 * 60  # 1 year
    }
    
    if seconds <= 0:
        return 0
    elif seconds > time_ranges[23]:
        return 23

    closest_id = min(time_ranges, key=lambda x: abs(time_ranges[x] - seconds))
    
    return closest_id

ids = get_ids()
for id, time in ids.items():
    print(f"ID {id}: {time}")
