def filter_by_environment(activities, env_pref):
    """
    env_pref:
        0 = no preference
        1 = indoor
        2 = outdoor
    """

    if env_pref == 1:  # indoor
        return [a for a in activities if not a.get("is_outdoor", False)]

    elif env_pref == 2:  # outdoor
        return [a for a in activities if a.get("is_outdoor", False)]

    return activities  # 0 = no preference