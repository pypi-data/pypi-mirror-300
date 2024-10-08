def parse(filename):
    sections = []
    current_section = None
    config_data = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current_section = line.strip("[]")
                if current_section == "SESSION":
                    current_section += (
                        f"_{len([s for s in sections if s.startswith('SESSION')])}"
                    )
                sections.append(current_section)
                config_data[current_section] = {}
            else:
                if "=" in line and current_section:
                    key, value = line.split("=", 1)
                    config_data[current_section][key.strip()] = value.strip()

    default_settings = config_data.get("DEFAULT", {})

    sessions = []
    for section in sections:
        if section.startswith("SESSION"):
            session_settings = dict(default_settings)
            session_settings.update(config_data[section])
            sessions.append(session_settings)

    return sessions